"""The counterexample engine — the falsifier pointed the other way (D17, second instrument).

A falsifier waits to be pointed at a claim. This **searches**: enumerate an exactly-defined finite window,
apply a conjecture, and either produce the object that breaks it or state precisely what was ruled out.

**The statement it is allowed to make is narrow, and that is the point.** An exhaustive window search
proves *"no counterexample in window W"* — never *"the conjecture is true"*. Every verdict therefore
carries the window it searched and the scope it does not cover. A search whose output cannot be turned into
a counterexample is decoration, so each shipped conjecture is paired with a **known-answer control**: a
predicate that is false in the window and *must* return a counterexample.

Built on `exactness/windows.py` — the enumeration is shared, not re-implemented, so a fix to the window
machinery moves both.

Run:        python3 scripts/counterexample.py
Guarded by: tests/test_counterexample.py
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import windows


@dataclass
class Verdict:
    """What an exhaustive search in a finite window establishes — and what it does not."""
    conjecture: str
    window: str
    searched: int
    counterexample: dict | None
    scope: str

    @property
    def verdict(self) -> str:
        return "BROKEN" if self.counterexample is not None else "no counterexample"

    @property
    def proves(self) -> str:
        if self.counterexample is not None:
            return (f"the conjecture is FALSE: {self.counterexample['what']} at "
                    f"(F,H) = {self.counterexample['flux']}")
        return (f"no counterexample among {self.searched} objects in {self.window}. That is a statement "
                f"about this window and nothing outside it.")


def _flux_row(row) -> list:
    return [int(x) for x in row]


def search(predicate, name: str, b3: int = 6, max_abs: int = 1, limit: int = 1) -> Verdict:
    """Exhaustively apply `predicate` to every integral `(F, H)` pair in the window.

    `predicate(flux, tadpole)` returns `True` when the conjecture *holds*. The first `limit` rows where it
    returns `False` are counterexamples.
    """
    fluxes = windows.enumerate_window(b3, max_abs)
    n = windows.tadpoles(fluxes)
    window = f"b3={b3}, |component| <= {max_abs} ({len(fluxes)} flux pairs)"
    found = []
    for row, t in zip(fluxes, n):
        f = _flux_row(row)
        if not predicate(f, int(t)):
            found.append({"flux": f, "tadpole": int(t),
                          "what": f"{name} fails (N = {int(t)})"})
            if len(found) >= limit:
                break
    return Verdict(conjecture=name, window=window, searched=int(len(fluxes)),
                   counterexample=(found[0] if found else None),
                   scope=("exhaustive over the window; it does NOT prove the conjecture outside it, and it "
                          "does not prove the negation either — one counterexample is required to do that"))


# ---------------------------------------------------------------------------------------
# the shipped conjectures
# ---------------------------------------------------------------------------------------
def tadpole_positive(flux, t) -> bool:
    return t > 0


def tadpole_bounded(limit: int):
    def predicate(flux, t) -> bool:
        return t <= limit
    predicate.__name__ = f"tadpole_bounded({limit})"
    return predicate


def tadpole_nonzero(flux, t) -> bool:
    return t != 0


#: The three shipped searches. Two are **known-answer controls** — they must find a counterexample, or the
#: engine cannot be trusted to report a clean one. The third rules something out in its window.
SHIPPED = (
    ("tadpole is always positive", tadpole_positive),
    ("tadpole is never zero", tadpole_nonzero),
    ("tadpole N <= 3", tadpole_bounded(3)),
    ("tadpole N <= 6", tadpole_bounded(6)),
)


def run_all(b3: int = 6, max_abs: int = 1) -> list:
    return [search(p, name, b3=b3, max_abs=max_abs) for name, p in SHIPPED]


# ---------------------------------------------------------------------------------------
# the same engine, over a stored corpus rather than an enumerated window
# ---------------------------------------------------------------------------------------
def load_corpus(data_dir=None) -> list:
    """Every stored row that carries a `flux`, with its file name — the corpus as the machine found it."""
    import glob
    import json
    import os
    from pathlib import Path

    base = Path(data_dir) if data_dir else Path(__file__).resolve().parents[3] / "data"
    out = []
    for path in sorted(glob.glob(str(base / "*.json"))):
        try:
            d = json.load(open(path))
        except Exception:
            continue
        rows = d["vacua"] if isinstance(d, dict) and "vacua" in d else (d if isinstance(d, list) else [])
        for r in rows:
            if isinstance(r, dict) and "flux" in r:
                out.append({"file": os.path.basename(path), "row": r})
    return out


def scaling_gcd(flux) -> int:
    """The gcd of a flux vector — the scaling class is `(F, H) ~ d(F, H)`, so `gcd > 1` is a copy."""
    import math
    g = 0
    for x in flux:
        g = math.gcd(g, abs(int(round(float(x)))))
    return g


def corpus_primitivity(data_dir=None) -> Verdict:
    """CONJECTURE: every stored vacuum is primitive.

    It is load-bearing: the flux-scaling lemma says `(F, H)` and `d(F, H)` are the **same** vacuum, so any
    non-primitive row is a scaling copy — and if its primitive parent is absent from the corpus, the class
    is represented *only* by a copy. Every per-row fraction then counts that class at a representative the
    sampler never found.
    """
    corpus = load_corpus(data_dir)
    primitives = {tuple(int(round(float(x))) for x in c["row"]["flux"]) for c in corpus}
    broken = []
    for c in corpus:
        g = scaling_gcd(c["row"]["flux"])
        if g <= 1:
            continue
        v = [int(round(float(x))) for x in c["row"]["flux"]]
        parent = tuple(x // g for x in v)
        broken.append({"flux": v, "tadpole": int(c["row"].get("Nflux", 0) or 0),
                       "what": (f"non-primitive (gcd {g}) in {c['file']}; primitive parent "
                                f"{'PRESENT' if parent in primitives else 'ABSENT'} in the corpus")})
    window = f"{len(corpus)} stored rows carrying a flux"
    return Verdict(conjecture="every stored vacuum is primitive", window=window,
                   searched=len(corpus), counterexample=(broken[0] if broken else None),
                   scope=("exhaustive over the stored rows, which are themselves a heuristic sample — so "
                          "this says the corpus CONTAINS non-primitive rows, not how many exist. A "
                          "non-primitive row is the same vacuum as its parent by the scaling lemma."))


def _eigs(row) -> list:
    e = row.get("eigenvalues")
    if not isinstance(e, (list, tuple)):
        return []
    out = []
    for v in e:
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            return []
    return out


def corpus_susy_minima(data_dir=None) -> Verdict:
    """CONJECTURE: every SUSY critical point in the corpus is a minimum.

    It reads as a check on the physics; it turns out to be a check on the **flags**. A SUSY point's Hessian
    is flat to ~1e-30, so `is_minimum` is decided by rounding noise, not by the geometry — and one row has a
    Hessian that is positive *and* not noise, yet is flagged as not a minimum.
    """
    corpus = load_corpus(data_dir)
    susy = [c for c in corpus if c["row"].get("is_susy")]
    broken = []
    for c in susy:
        if c["row"].get("is_minimum"):
            continue
        e = _eigs(c["row"])
        lam = min(e) if e else 0.0
        broken.append({"flux": [int(round(float(x))) for x in c["row"]["flux"]],
                       "tadpole": int(c["row"].get("Nflux", 0) or 0),
                       "lambda_min": lam,
                       "noise": abs(lam) < 1e-20,
                       "what": (f"SUSY but flagged not-minimum in {c['file']} "
                                f"(lambda_min = {lam:.1e}{', numerically zero' if abs(lam) < 1e-20 else ''})")})
    noisy = sum(1 for b in broken if b["noise"])
    real = [b for b in broken if not b["noise"]]
    window = f"{len(corpus)} stored rows, {len(susy)} of them flagged SUSY"
    scope = (f"exhaustive over the stored rows. **{noisy} of the {len(broken)} 'counterexamples' have a "
             f"Hessian eigenvalue within 1e-20 of zero**, so the flag there is decided by floating-point "
             f"noise and is not evidence about the physics: a SUSY point's Hessian is flat, and "
             f"counting minima at SUSY points without a threshold is meaningless. "
             + (f"The remaining {len(real)} row(s) are genuine discrepancies: positive and not noise, yet "
                f"not flagged. " if real else "")
             + "The corpus is itself a heuristic sample.")
    return Verdict(conjecture="every SUSY critical point is a minimum", window=window,
                   searched=len(susy), counterexample=(broken[0] if broken else None), scope=scope)


def _row_key(file, row):
    return (file, tuple(int(round(float(v))) for v in row["flux"]))


def threshold_table(thresholds=(0.0, 1e-12, 1e-8, 1e-6, 1e-4, 1e-3), data_dir=None) -> list:
    """`is_minimum` is a **threshold on the Hessian**, and the threshold was never written down.

    A minimum is `min(eigenvalue) > t`. The corpus stores the resulting boolean and not `t`, so every
    "number of minima" is a number with a silent parameter — and the count moves by a factor of two across
    the plausible range. This table makes the parameter visible and finds the value the corpus actually used.
    """
    corpus = load_corpus(data_dir)
    flagged = {_row_key(c["file"], c["row"]) for c in corpus if c["row"].get("is_minimum")}
    out = []
    for t in thresholds:
        got = set()
        for c in corpus:
            e = _eigs(c["row"])
            if e and min(e) > t:
                got.add(_row_key(c["file"], c["row"]))
        out.append({"threshold": t, "count": len(got), "missing": len(flagged - got),
                    "extra": len(got - flagged), "identical_to_flag": got == flagged})
    return out


def flag_threshold(data_dir=None, candidates=None) -> dict:
    """The threshold that reproduces the stored `is_minimum` column **exactly**, or the closest one.

    Returns the threshold, whether the match is set-exact, and the size of the symmetric difference. If no
    candidate reproduces the column, that is a finding too: it means the stored flag is not a pure
    eigenvalue threshold and something else decided it.
    """
    if candidates is None:
        candidates = (1e-12, 1e-10, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3)
    best = None
    for r in threshold_table(candidates, data_dir):
        diff = r["missing"] + r["extra"]
        if best is None or diff < best["symmetric_difference"]:
            best = {"threshold": r["threshold"], "count": r["count"],
                    "symmetric_difference": diff, "exact": r["identical_to_flag"]}
    return best


__all__ = ["Verdict", "search", "tadpole_positive", "tadpole_bounded", "tadpole_nonzero",
           "SHIPPED", "run_all", "load_corpus", "scaling_gcd", "corpus_primitivity",
           "corpus_susy_minima", "threshold_table", "flag_threshold"]
