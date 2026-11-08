"""Constraint-first learnability split for animal vocal corpora (discipline/animal).

Vendored, self-contained copy of
``pacland/animal/learnability.py`` (numpy-only three-check split) with the
``pacland.structure`` dependency (``mutual_information`` / ``mi_significance``) inlined
so this directory is runnable on a Linux box with no further research and no parent
package import.

Generalises the Rule of Three — single-coordinate mutual information, joint ridge-CV,
and a permutation null — from the physics constraint-first measurement to categorical
targets (context / species / referent).

- The single-coordinate MI arm uses the reference's own (stdlib) naive-bin estimator.
- The joint arm is a hand-rolled **one-vs-rest linear ridge** classifier for categorical
  targets; continuous targets keep plain linear ridge regression + Pearson r.

This module is **numpy + stdlib only** (no scikit-learn).

A claim of LEARNABLE vs uniform is made only when the arms agree, per the Rule of Three:
N independent checks, each targeting a distinct failure mode.
"""
from __future__ import annotations

import random
from math import log2
from typing import Callable, Sequence

import numpy as np

__all__ = [
    "winsorize",
    "ridge_cv_balanced_accuracy",
    "ridge_cv_pearson",
    "permutation_z",
    "single_coord_mi",
    "referent_verdict",
    "learnability_split",
    "mutual_information",
    "mi_significance",
]


# ---------------------------------------------------------------------------
# pacland.structure (vendored, stdlib-only MI estimator)
# ---------------------------------------------------------------------------
def _bin_indices(vals, bins):
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return [0] * len(vals)
    return [min(int((v - lo) / (hi - lo) * bins), bins - 1) for v in vals]


def _entropy(counts) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * log2(c / total) for c in counts.values() if c > 0)


def mutual_information(xs, ys, bins: int = 8) -> float:
    """Estimated mutual information I(X;Y) via 2D binning (naive estimator).

    Returns bits. A naive estimator is biased upward for small samples; use
    ``mi_significance`` to judge whether a value is above that bias.
    """
    n = len(xs)
    if n < 2 or len(xs) != len(ys):
        raise ValueError("need equal-length inputs of length >= 2")
    bx = _bin_indices(list(xs), bins)
    by = _bin_indices(list(ys), bins)
    joint: dict = {}
    mx: dict = {}
    my: dict = {}
    for i in range(n):
        joint[(bx[i], by[i])] = joint.get((bx[i], by[i]), 0) + 1
        mx[bx[i]] = mx.get(bx[i], 0) + 1
        my[by[i]] = my.get(by[i], 0) + 1
    return _entropy(mx) + _entropy(my) - _entropy(joint)


def mi_significance(
    xs, ys, bins: int = 8, permutations: int = 200, seed: int = 0
) -> dict:
    """Permutation test: is I(X;Y) larger than chance?

    Shuffles y, recomputes MI, and reports the z-score of the true MI against the
    null distribution. ``|z| >= 3`` is the usual "real structure" threshold.
    """
    rng = random.Random(seed)
    true = mutual_information(xs, ys, bins)
    ys_list = list(ys)
    null = []
    for _ in range(permutations):
        rng.shuffle(ys_list)
        null.append(mutual_information(xs, ys_list, bins))
    mean = sum(null) / len(null)
    var = sum((v - mean) ** 2 for v in null) / len(null)
    std = var ** 0.5
    z = (true - mean) / std if std > 0 else 0.0
    return {"mi": true, "null_mean": mean, "z": z}


# ---------------------------------------------------------------------------
# learnability.py (vendored verbatim from pacland/animal/learnability.py)
# ---------------------------------------------------------------------------
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
