#!/usr/bin/env python3
"""C1 — animal communication learnability split (macaque corpus), via the reusable instrument.

Corpus: "Acoustic data in four species of macaques" (Zenodo 3877581, CC0) — Rebout et al. 2020,
Proc. R. Soc. B 287:20200439. Reproduces the headline numbers of docs/animal-constraint-first.md.

The three-check split (MI · ridge-CV · permutation null) comes from the numpy-only module
``pacland.animal.learnability``; the unit-inventory arm (k-means + silhouette) additionally
needs scikit-learn, which is imported here (the script is a manual run, not part of the CI suite).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pacland.animal.learnability import (  # noqa: E402
    winsorize,
    ridge_cv_balanced_accuracy,
    ridge_cv_pearson,
    permutation_z,
    referent_verdict,
    learnability_split,
)
from pacland.structure import mi_significance  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "animal" / "Rebout_et_al_data_excel.xlsx"
FEATURES = ["duration", "Q2_ratio", "q2_frequency", "q1_frequency",
            "q3_frequency", "aggregate_entropy", "average_entropy"]
N_PERM = 300


def _silhouette_vs_null(X, ks=range(2, 9), n_perm: int = 60, seed: int = 0) -> dict:
    """Mean silhouette per k against a per-feature-shuffle null (unit-inventory arm)."""
    rng = np.random.default_rng(seed)
    sil_real = [silhouette_score(X, KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X))
                for k in ks]
    null = []
    for _ in range(n_perm):
        Xsh = np.column_stack([rng.permutation(X[:, j]) for j in range(X.shape[1])])
        for k in ks:
            lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(Xsh)
            null.append(silhouette_score(Xsh, lab))
    null = np.asarray(null)
    best_idx = int(np.argmax(sil_real))
    z = (sil_real[best_idx] - null.mean()) / null.std() if null.std() > 0 else 0.0
    return {"best_silhouette": float(sil_real[best_idx]), "best_k": best_idx + min(ks),
            "null_mean": float(null.mean()), "z": float(z)}


def main() -> None:
    df = pd.read_excel(DATA)
    print(f"n calls = {len(df)}  context = {dict(df['context'].value_counts())}")

    X = StandardScaler().fit_transform(
        np.column_stack([winsorize(df[f].to_numpy()) for f in FEATURES]))
    ctx_map = {"negative": 0, "neutral": 1, "positive": 2}
    y_ctx = df["context"].map(ctx_map).to_numpy()
    y_sp = pd.Categorical(df["species"]).codes

    # 1. positive control — quantile ordering q1<=q2<=q3 (structural, exact by def)
    q1, q2, q3 = (df["q1_frequency"].to_numpy(), df["q2_frequency"].to_numpy(),
                  df["q3_frequency"].to_numpy())
    n_ord = int(np.sum((q1 <= q2) & (q2 <= q3)))
    X_noq3 = StandardScaler().fit_transform(np.column_stack(
        [winsorize(df[f].to_numpy()) for f in FEATURES if f != "q3_frequency"]))
    ctrl = permutation_z(ridge_cv_pearson, X_noq3, q3, n_perm=N_PERM, seed=0)
    mi_ctrl = mi_significance(list(q2), list(q3), bins=8, permutations=200, seed=0)
    print(f"POSITIVE CONTROL q1<=q2<=q3: holds {n_ord}/{len(q1)} "
          f"({100 * n_ord / len(q1):.1f}%); ridge r={ctrl['value']:+.3f} z={ctrl['z']:+.1f}; "
          f"MI(q2;q3)={mi_ctrl['mi']:.3f} z={mi_ctrl['z']:+.1f}")

    # 2. unit-inventory (discrete cluster structure — the one sklearn-dependent arm)
    sil = _silhouette_vs_null(X, seed=0)
    print(f"UNIT-INVENTORY: silhouette={sil['best_silhouette']:+.3f} (k={sil['best_k']}) "
          f"vs null {sil['null_mean']:+.3f}, z={sil['z']:+.1f}")

    # 3. dialect (acoustic -> species, 4-class, chance 0.25)
    sp = learnability_split(X, y_sp, FEATURES, seed=0)
    print(f"DIALECT acoustic->species: bal-acc={sp['joint']['value']:.3f} (chance 0.25) "
          f"z={sp['joint']['z']:+.1f} -> {sp['verdict']}")

    # 4. context-dependence (acoustic -> context, 3-class, chance 0.33)
    ctx = learnability_split(X, y_ctx, FEATURES, seed=0)
    print(f"CONTEXT-DEPENDENCE acoustic->context: bal-acc={ctx['joint']['value']:.3f} "
          f"(chance 0.33) z={ctx['joint']['z']:+.1f} -> {ctx['verdict']}")

    # 5. meaning / falsifier (context-free acoustic -> referent)
    best_single = {"acc": 0.0, "feature": None, "z": None}
    for j, name in enumerate(FEATURES):
        a = permutation_z(ridge_cv_balanced_accuracy, X[:, j].reshape(-1, 1), y_ctx,
                          n_perm=N_PERM, seed=0)
        if a["value"] > best_single["acc"]:
            best_single = {"acc": a["value"], "feature": name, "z": a["z"]}
    print(f"MEANING (falsifier): joint bal-acc={ctx['joint']['value']:.3f} "
          f"z={ctx['joint']['z']:+.1f} -> {referent_verdict(ctx['joint']['value'], ctx['joint']['z'])}; "
          f"best single={best_single['feature']} acc={best_single['acc']:.3f} z={best_single['z']:+.1f}")


if __name__ == "__main__":
    main()
