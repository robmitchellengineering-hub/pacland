#!/usr/bin/env python3
"""Cross-species "decodability deficit" benchmark.

For each corpus in ``corpora.json``: load the acoustic feature table + behavioural /
species label, run the vendored numpy-only three-check split
(``learnability.py``), and append one result row.

Roles (from the brief):
  - ``context`` / ``referent``  -> DEFICIT.  D = 1 - (balanced_acc - chance) / (1 - chance),
                                     chance = 1 / n_classes.  D=0 means the label is
                                     (linearly) decodable to ceiling; D=1 means at chance.
  - ``species`` / ``dialect`` / ``call-type`` -> CONSTRAINT learnability.
                                     Report balanced accuracy + permutation z, not a deficit.
  - ``sequence`` -> SEQUENCE constraints (Zipf / temporal MI / combinatorial MDL),
                                     reported separately, never as a deficit.

Outputs:
  - ``results.json``  machine-readable rows + a ``sequences`` block.
  - ``ranking.md``    deficit rows sorted by D ascending (most decodable first).

Runnable self-contained:
    python3 -m venv venv
    ./venv/bin/pip install numpy scipy scikit-learn pandas openpyxl
    ./venv/bin/python benchmark.py
"""
from __future__ import annotations

import csv
import collections
import hashlib
import json
import math
import os
import sys

import numpy as np
import pandas as pd

import learnability as inst

HERE = os.path.dirname(os.path.abspath(__file__))
N_PERM = int(os.environ.get("BENCH_N_PERM", "300"))
SEED = 0
SEQ_N_PERM = int(os.environ.get("BENCH_SEQ_N_PERM", "500"))
SEQ_RNG_SEED = 20261108


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def md5_of(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def deficit(bal_acc: float, chance: float) -> float:
    """D = 1 - (bal_acc - chance) / (1 - chance). D=0 fully decodable, D=1 at chance."""
    if (1.0 - chance) <= 1e-12:
        return 0.0
    return 1.0 - (bal_acc - chance) / (1.0 - chance)


def _load_table(spec: dict) -> pd.DataFrame:
    fmt = spec.get("format", "csv").lower()
    path = os.path.join(HERE, spec["file"])
    sep = spec.get("delimiter")
    if fmt == "xlsx":
        return pd.read_excel(path)
    if fmt == "csv":
        return pd.read_csv(path, sep=sep or ",")
    if fmt == "txt":
        return pd.read_csv(path, sep=sep or "\t")
    raise ValueError(f"unsupported format {fmt}")


def _extract_label(df: pd.DataFrame, lab: dict):
    """Return (df_subset, y_values). Supports a derived label via value mapping.

    String labels are whitespace-stripped; original nulls are preserved (not turned
    into the literal "nan" class) so the NaN-drop step can remove them.
    """
    col = lab["column"]
    mapping = lab.get("mapping")
    if mapping:
        s = df[col].astype(str).str.strip()
        keep = s.isin(mapping.keys())
        sub = df[keep].copy()
        y = sub[col].astype(str).str.strip().map(mapping).to_numpy()
        return sub, y
    sub = df.copy()
    y = sub[col].copy()
    if y.dtype == object:
        notna = y.notna().to_numpy()
        y = y.astype(str).str.strip()
        y = y.where(notna)  # restore nulls (-> NaN) for downstream drop
    return sub, y.to_numpy()


def _to_numeric_feature_matrix(df: pd.DataFrame, features: list[str]):
    """Coerce each feature column to float (non-numeric -> NaN). No winsorize here:
    NaN rows must be dropped FIRST, otherwise winsorize's percentile poisons the
    whole column."""
    cols = []
    for f in features:
        if f not in df.columns:
            raise KeyError(f"missing feature column {f!r}")
        cols.append(pd.to_numeric(df[f], errors="coerce").to_numpy(dtype=float))
    return np.column_stack(cols)


def _clean_and_winsorize(X, y):
    """Drop rows with a NaN feature/label, then winsorize (1/99) each clean column."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    finite = np.isfinite(X).all(axis=1)
    if y.dtype.kind in "fc":
        finite &= np.isfinite(y)
    else:
        finite &= ~pd.isna(y)
    X, y = X[finite], y[finite]
    Xw = np.column_stack([inst.winsorize(X[:, j]) for j in range(X.shape[1])])
    return Xw, y


def run_tabular(corpus: dict, lab: dict) -> dict:
    """Run the three-check split for one (corpus, label) pair."""
    features = corpus["feature_columns"]
    try:
        df = _load_table(corpus)
    except Exception as e:  # noqa: BLE001
        return _error_row(corpus, lab, f"load-error: {e}")
    try:
        df, y = _extract_label(df, lab)
    except Exception as e:  # noqa: BLE001
        return _error_row(corpus, lab, f"label-error: {e}")
    try:
        Xraw = _to_numeric_feature_matrix(df, features)
    except Exception as e:  # noqa: BLE001
        return _error_row(corpus, lab, f"feature-error: {e}")

    X, y = _clean_and_winsorize(Xraw, y)
    classes = np.unique(y)
    if len(classes) < 2:
        return _error_row(corpus, lab, "insufficient-classes (<2)", n=len(y))

    y_codes = pd.Categorical(y).codes  # 0..k-1, stable ordering
    n = len(y)
    n_classes = len(classes)
    chance = 1.0 / n_classes
    try:
        result = inst.learnability_split(X, y_codes, features, continuous=False,
                                         n_perm=N_PERM, seed=SEED)
    except Exception as e:  # noqa: BLE001
        return _error_row(corpus, lab, f"instrument-error: {e}", n=n)

    joint = result["joint"]
    bal_acc = float(joint["value"])
    z = float(joint["z"])
    role = lab["role"]
    is_deficit = role in ("context", "referent")

    d = deficit(bal_acc, chance) if is_deficit else None
    if is_deficit:
        verdict = inst.referent_verdict(bal_acc, z)
        deficit_or_z = d
    else:
        verdict = "LEARNABLE" if z >= 3 else "uniform"
        deficit_or_z = z

    row = {
        "corpus": corpus["id"],
        "species": corpus["species"],
        "title": corpus["title"],
        "label": lab["name"],
        "role": role,
        "n": n,
        "n_classes": n_classes,
        "bal_acc": round(bal_acc, 6),
        "chance": round(chance, 6),
        "deficit": round(d, 6) if d is not None else None,
        "z": round(z, 3),
        "deficit_or_z": round(deficit_or_z, 6) if is_deficit else round(deficit_or_z, 3),
        "best_mi_feature": result["best_mi"]["feature"],
        "best_mi": round(result["best_mi"]["mi"], 4),
        "verdict": verdict,
    }
    return row


def _error_row(corpus: dict, lab: dict, verdict: str, n=None) -> dict:
    return {
        "corpus": corpus["id"],
        "species": corpus["species"],
        "title": corpus["title"],
        "label": lab["name"],
        "role": lab["role"],
        "n": n,
        "n_classes": None,
        "bal_acc": None,
        "chance": None,
        "deficit": None,
        "z": None,
        "deficit_or_z": None,
        "best_mi_feature": None,
        "best_mi": None,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# sequence constraints (sperm-whale coda sequences — ported from c1c)
# ---------------------------------------------------------------------------
def _zipf_alpha(counts):
    c = np.sort(np.asarray(counts, dtype=float))[::-1]
    c = c[c > 0]
    k = len(c)
    if k < 3:
        return np.nan, np.nan
    x = np.log10(np.arange(1, k + 1))
    y = np.log10(c)
    b, a = np.polyfit(x, y, 1)
    yhat = b * x + a
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return b, r2


def run_sequence(corpus: dict) -> dict:
    rng = np.random.default_rng(SEQ_RNG_SEED)
    ratio_thresh = 1.5

    def ici_list(row, ncols=28):
        n = int(float(row["nClicks"]))
        return [float(row[f"ICI{i}"]) for i in range(1, n)]

    def rhythm_string(row):
        icis = ici_list(row)
        if len(icis) == 0:
            return ""
        med = np.median(icis)
        if med <= 0:
            return "S" * len(icis)
        return "".join("L" if (x / med) >= ratio_thresh else "S" for x in icis)

    rows = []
    with open(os.path.join(HERE, corpus["file"]), newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r["_rhythm"] = rhythm_string(r)
            rows.append(r)
    N = len(rows)
    vocab = sorted({r["_rhythm"] for r in rows})
    V = len(vocab)
    vid = {s: i for i, s in enumerate(vocab)}
    type_ids = np.array([vid[r["_rhythm"]] for r in rows])

    # T1 Zipf
    counts_obs = np.bincount(type_ids, minlength=V)
    alpha_obs, r2_obs = _zipf_alpha(counts_obs)
    alpha_null = np.empty(SEQ_N_PERM)
    for i in range(SEQ_N_PERM):
        t = rng.integers(0, V, N)
        alpha_null[i], _ = _zipf_alpha(np.bincount(t, minlength=V))
    alpha_z = (alpha_obs - alpha_null.mean()) / alpha_null.std()

    # T2 temporal MI within (REC, Whale)
    groups = collections.defaultdict(list)
    for r in rows:
        groups[(r["REC"], r["Whale"])].append(r)
    for g in groups.values():
        g.sort(key=lambda r: float(r["TsTo"]))

    def transitions_from_groups(grp):
        C = collections.Counter()
        for g in grp.values():
            seq = [vid[r["_rhythm"]] for r in g]
            for a, b in zip(seq[:-1], seq[1:]):
                C[(a, b)] += 1
        return C

    C = transitions_from_groups(groups)
    T = sum(C.values())

    def mutual_info_bigram(C, T):
        if T == 0:
            return np.nan, 0.0, 0.0
        rowsum = collections.Counter(); colsum = collections.Counter()
        for (a, b), n in C.items():
            rowsum[a] += n; colsum[b] += n
        mi = 0.0
        for (a, b), n in C.items():
            p_ab = n / T; p_a = rowsum[a] / T; p_b = colsum[b] / T
            mi += p_ab * math.log2(p_ab / (p_a * p_b))
        best_succ = {}
        for a in rowsum:
            best_succ[a] = max((b for (a2, b) in C.keys() if a2 == a), key=lambda b: C[(a, b)])
        correct = sum(n for (a, b), n in C.items() if b == best_succ[a])
        majority = colsum.most_common(1)[0][0] if colsum else None
        majority_correct = sum(n for (a, b), n in C.items() if b == majority)
        return mi, correct / T if T else 0.0, majority_correct / T if T else 0.0

    mi_obs, bigram_acc, unigram_acc = mutual_info_bigram(C, T)
    mi_null = np.empty(SEQ_N_PERM)
    for i in range(SEQ_N_PERM):
        shuf = collections.defaultdict(list)
        for key, g in groups.items():
            ids = [vid[r["_rhythm"]] for r in g]
            rng.shuffle(ids)
            shuf[key] = ids
        C2 = collections.Counter()
        for key, seq in shuf.items():
            for a, b in zip(seq[:-1], seq[1:]):
                C2[(a, b)] += 1
        mi_null[i], _, _ = mutual_info_bigram(C2, sum(C2.values()))
    mi_z = (mi_obs - mi_null.mean()) / mi_null.std()

    # T3 combinatoriality (grammar MDL)
    strings = [r["_rhythm"] for r in rows]

    def nll_flat(ss):
        c = collections.Counter(ss); tot = len(ss)
        return -sum(math.log2(c[s] / tot) for s in ss), len(c) - 1

    def nll_markov(ss):
        first = collections.Counter(); trans = collections.Counter()
        for s in ss:
            if len(s) == 0:
                continue
            first[s[0]] += 1
            for a, b in zip(s[:-1], s[1:]):
                trans[(a, b)] += 1
        ALPHA = 1.0
        nll = 0.0
        for s in ss:
            if len(s) == 0:
                continue
            nll -= math.log2((first[s[0]] + ALPHA) / (sum(first.values()) + ALPHA * 2))
            for a, b in zip(s[:-1], s[1:]):
                denom = sum(trans[(a, x)] for x in "SL") + ALPHA * 2
                nll -= math.log2((trans[(a, b)] + ALPHA) / denom)
        return nll, 4

    nllA, kA = nll_flat(strings)
    nllB, kB = nll_markov(strings)

    def shuffle_symbols(s):
        if len(s) <= 1:
            return s
        arr = list(s); rng.shuffle(arr)
        return "".join(arr)

    nllB_null = np.empty(SEQ_N_PERM)
    for i in range(SEQ_N_PERM):
        nllB_null[i], _ = nll_markov([shuffle_symbols(s) for s in strings])
    nllB_z = (nllB - nllB_null.mean()) / nllB_null.std()

    total_sym = sum(len(s) for s in strings)
    def mdl(nll, k, npts):
        return nll + 0.5 * k * math.log2(npts) if npts > 1 else nll
    mdlA = mdl(nllA, kA, total_sym); mdlB = mdl(nllB, kB, total_sym)

    # classic CodaType Zipf (robustness)
    ctype = collections.Counter()
    with open(os.path.join(HERE, corpus["file2"]), newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            ctype[r["CodaType"]] += 1
    classic_alpha, classic_r2 = _zipf_alpha(list(ctype.values()))
    classic_V = len(ctype)

    # T1: a real Zipf is STEEPER than the flat-inventory null (which itself has a
    # slightly negative slope, null_mean ~ -0.167), so significance is z <= -3.
    t1_learn = (alpha_obs <= -0.8) and (alpha_z <= -3)
    t2_learn = (mi_obs >= 0.01) and (mi_z >= 3)
    t3_learn = (nllB < nllA) and (nllB_z <= -3)

    return {
        "corpus": corpus["id"],
        "species": corpus["species"],
        "title": corpus["title"],
        "role": "sequence",
        "n_codas": N,
        "V_types": V,
        "zipf": {"alpha": round(float(alpha_obs), 4), "r2": round(float(r2_obs), 4),
                 "z": round(float(alpha_z), 2), "verdict": "LEARNABLE" if t1_learn else "graded/uniform"},
        "temporal_mi": {"mi": round(float(mi_obs), 4), "z": round(float(mi_z), 2),
                        "bigram_acc": round(float(bigram_acc), 4),
                        "unigram_acc": round(float(unigram_acc), 4),
                        "verdict": "LEARNABLE" if t2_learn else "graded/uniform"},
        "combinatorial_mdl": {"nll_flat": round(float(nllA), 2), "nll_markov": round(float(nllB), 2),
                              "mdl_flat": round(float(mdlA), 2), "mdl_markov": round(float(mdlB), 2),
                              "z": round(float(nllB_z), 2),
                              "verdict": "LEARNABLE" if t3_learn else "graded/uniform"},
        "classic_zipf": {"alpha": round(float(classic_alpha), 4), "r2": round(float(classic_r2), 4),
                         "V": classic_V},
        "verdict": "LEARNABLE" if (t1_learn and t2_learn and t3_learn) else "partial",
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    with open(os.path.join(HERE, "corpora.json")) as f:
        manifest = json.load(f)
    corpora = manifest["corpora"]

    rows = []
    sequences = []
    for corpus in corpora:
        if corpus.get("kind") == "sequence":
            try:
                sequences.append(run_sequence(corpus))
            except Exception as e:  # noqa: BLE001
                sequences.append({"corpus": corpus["id"], "species": corpus["species"],
                                  "role": "sequence", "verdict": f"sequence-error: {e}"})
            continue
        for lab in corpus["labels"]:
            rows.append(run_tabular(corpus, lab))

    # machine-readable
    out = {"rows": rows, "sequences": sequences,
           "meta": {"n_perm": N_PERM, "seed": SEED,
                    "deficit_definition": "D = 1 - (bal_acc - chance)/(1 - chance); "
                                          "chance = 1/n_classes; D=0 decodable, D=1 chance"}}
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=2)

    # ranking.md — deficit rows only, sorted by D ascending
    deficit_rows = [r for r in rows if r["role"] in ("context", "referent")
                    and r["deficit"] is not None]
    deficit_rows.sort(key=lambda r: r["deficit"])
    lines = ["# Decodability deficit — ranking (most decodable first)\n",
             "`D = 1 - (balanced_accuracy - chance)/(1 - chance)`, `chance = 1/n_classes`.",
             "`D = 0` → the label is decodable to ceiling from the acoustic features; "
             "`D = 1` → at chance.",
             "",
             "| # | species | label role | n | bal_acc | deficit |",
             "|---|---------|------------|---|---------|---------|"]
    for i, r in enumerate(deficit_rows, 1):
        lines.append(f"| {i} | {r['species']} | {r['role']} ({r['label']}) | {r['n']} "
                     f"| {r['bal_acc']:.3f} | {r['deficit']:.3f} |")
    lines.append("")
    lines.append("_Constraint labels (species / dialect / call-type) and sequence corpora "
                 "are reported in `results.json`, not ranked here as deficits._\n")
    with open(os.path.join(HERE, "ranking.md"), "w") as f:
        f.write("\n".join(lines))

    # console summary
    print("=" * 80)
    print("decodability-benchmark — results")
    print("=" * 80)
    print(f"{len(rows)} label rows, {len(deficit_rows)} deficit rows, "
          f"{len(sequences)} sequence corpora")
    for r in rows:
        if r["deficit"] is not None:
            print(f"  [{r['corpus']:<16}] {r['label']:<10} {r['role']:<9} "
                  f"n={r['n']:<6} bal_acc={r['bal_acc']:.3f} D={r['deficit']:.3f} "
                  f"z={r['z']:.1f} {r['verdict']}")
        else:
            print(f"  [{r['corpus']:<16}] {r['label']:<10} {r['role']:<9} "
                  f"n={r['n']:<6} bal_acc={r['bal_acc'] if r['bal_acc'] is not None else 'NA'} "
                  f"z={r['z']} {r['verdict']}")
    for s in sequences:
        print(f"  [SEQ] {s['corpus']}: {s['verdict']} "
              f"(zipf_z={s['zipf']['z']}, mi_z={s['temporal_mi']['z']}, "
              f"mdl_z={s['combinatorial_mdl']['z']})")
    print("[wrote results.json, ranking.md]")


if __name__ == "__main__":
    main()
