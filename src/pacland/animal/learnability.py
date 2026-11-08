"""Constraint-first learnability split for animal vocal corpora (discipline/animal).

Generalises the Rule of Three — single-coordinate mutual information, joint ridge-CV,
and a permutation null — from the physics constraint-first measurement
(``docs/constraint-learnability.md``) to categorical targets (context / species / referent).

- The single-coordinate MI arm reuses ``pacland.structure.mutual_information`` /
  ``mi_significance`` — the reference's own (stdlib) estimator.
- The joint arm is a hand-rolled **one-vs-rest linear ridge** classifier for categorical
  targets (the physics arm in ``pacland.structure.ridge_cv_predictability`` is regression-only);
  continuous targets keep plain linear ridge regression + Pearson r.

This module is **numpy + stdlib only**, matching the rest of ``pacland`` and its CI (which
installs numpy but not scikit-learn). The full C1 pipeline's unit-inventory arm (k-means +
silhouette) is the one place scikit-learn is needed, and that lives in
``scripts/measure_animal_constraints.py``, not here.

A claim of LEARNABLE vs uniform is made only when the arms agree, per the Rule of Three
(``pacland/AGENTS.md``): N independent checks, each targeting a distinct failure mode.
"""
from __future__ import annotations

from typing import Callable, Sequence

import numpy as np

from ..structure import mi_significance

__all__ = [
    "winsorize",
    "ridge_cv_balanced_accuracy",
    "ridge_cv_pearson",
    "permutation_z",
    "single_coord_mi",
    "referent_verdict",
    "learnability_split",
]


def winsorize(vals, lo: float = 1.0, hi: float = 99.0) -> np.ndarray:
    """Clip to the [lo, hi] percentiles — robust to data-entry outliers."""
    a = np.asarray(vals, dtype=float)
    l, h = np.percentile(a, [lo, hi])
    return np.clip(a, l, h)


def _ridge_coef(X, y, lam: float = 1.0) -> np.ndarray:
    """Linear ridge coefficients with intercept: (Xb^T Xb + lam I)^-1 Xb^T y."""
    X = np.asarray(X, dtype=float)
    Xb = np.column_stack([np.ones(len(X)), X])
    d = Xb.shape[1]
    A = Xb.T @ Xb + lam * np.eye(d)
    A[0, 0] -= lam  # do not regularize the intercept
    return np.linalg.solve(A, Xb.T @ np.asarray(y, dtype=float))


def _balanced_accuracy(y_true, y_pred) -> float:
    """Mean per-class recall — robust to class imbalance (chance = 1/n_classes)."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean([np.mean(y_pred[y_true == c] == c) for c in np.unique(y_true)]))


def _predict_ovr(Xtr, ytr, Xte, classes):
    """One-vs-rest linear ridge: argmax over per-class ridge scores."""
    scores = []
    for c in classes:
        beta = _ridge_coef(Xtr, (ytr == c).astype(float))
        scores.append(np.column_stack([np.ones(len(Xte)), Xte]) @ beta)
    return classes[np.argmax(np.column_stack(scores), axis=1)]


def ridge_cv_balanced_accuracy(X, y, folds: int = 5, seed: int = 0) -> float:
    """5-fold CV balanced accuracy of a one-vs-rest linear ridge classifier."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    classes = np.unique(y)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y))
    preds = np.empty(len(y), dtype=classes.dtype)
    for fold in np.array_split(idx, folds):
        tr = np.setdiff1d(idx, fold)
        preds[fold] = _predict_ovr(X[tr], y[tr], X[fold], classes)
    return _balanced_accuracy(y, preds)


def ridge_cv_pearson(X, y, folds: int = 5, seed: int = 0) -> float:
    """5-fold CV Pearson r of linear ridge regression (continuous target)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y))
    preds = np.empty(len(y))
    for fold in np.array_split(idx, folds):
        tr = np.setdiff1d(idx, fold)
        beta = _ridge_coef(X[tr], y[tr])
        preds[fold] = np.column_stack([np.ones(len(fold)), X[fold]]) @ beta
    return float(np.corrcoef(preds, y)[0, 1])


def permutation_z(metric: Callable, X, y, n_perm: int = 300, seed: int = 0) -> dict:
    """z-score of ``metric(X, y)`` against the label-permutation null.

    The null preserves the feature matrix and destroys only the label association — the
    "is the signal real, or finite-sample bias" test.
    """
    true = metric(X, y)
    rng = np.random.default_rng(seed)
    yarr = np.asarray(y)
    null = [metric(X, rng.permutation(yarr)) for _ in range(n_perm)]
    null = np.asarray(null)
    z = (true - null.mean()) / null.std() if null.std() > 0 else 0.0
    return {"value": float(true), "null_mean": float(null.mean()),
            "null_std": float(null.std()), "z": float(z)}


def single_coord_mi(X, y, features: Sequence[str], n_perm: int = 200, seed: int = 0):
    """Per-coordinate MI + permutation z (reuses ``pacland.structure``), plus the max."""
    rows = []
    best = {"mi": 0.0, "z": 0.0, "feature": None}
    for j, name in enumerate(features):
        r = mi_significance(list(X[:, j]), list(y), bins=8, permutations=n_perm, seed=seed)
        rows.append({"feature": name, "mi": r["mi"], "z": r["z"]})
        if r["mi"] > best["mi"]:
            best = {"mi": r["mi"], "z": r["z"], "feature": name}
    return rows, best


def referent_verdict(value: float, z: float, threshold: float = 0.90) -> str:
    """The registered falsifier bands for the context-free acoustic -> referent map.

    >= threshold AND z >= 3 -> REFUTED (a Rosetta unit) · z < 3 -> uniform (within null) ·
    otherwise -> graded (statistically real, nowhere near deterministic).
    """
    if value >= threshold and z >= 3:
        return "REFUTED (Rosetta unit)"
    if z < 3:
        return "uniform (within null)"
    return "graded (no Rosetta unit)"


def learnability_split(X, y, features: Sequence[str], continuous: bool = False,
                       n_perm: int = 300, seed: int = 0) -> dict:
    """Run the Rule of Three on a feature matrix -> target; return a structured dict."""
    mi_rows, best_mi = single_coord_mi(X, y, features, seed=seed)
    metric = ridge_cv_pearson if continuous else ridge_cv_balanced_accuracy
    joint = permutation_z(metric, X, y, n_perm=n_perm, seed=seed)
    verdict = "LEARNABLE" if joint["z"] >= 3 else "uniform"
    return {"mi_rows": mi_rows, "best_mi": best_mi, "joint": joint, "verdict": verdict}
