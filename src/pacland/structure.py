"""Structure mining — which observables carry geometric information?

The new approach (``docs/new-approach.md``) is constraint-first: find the observables
whose values are *structured* (dependent on the flux / geometry) as opposed to *random*
(uniform, like W0 — the negative result). The tool here is **non-linear**: mutual
information, not Pearson correlation, so it catches structure that linear correlation
misses. Significance is judged by a permutation test against the null "observable is
independent of flux".

Pure stdlib. Finite-sample mutual information is biased; the permutation test is what
separates real structure from that bias.
"""
from __future__ import annotations

import random
from math import log2


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


def classify_observable(
    flux_cols, y, bins: int = 8, permutations: int = 200, z_threshold: float = 3.0
) -> dict:
    """Classify one observable as ``structured`` or ``random``.

    ``flux_cols`` is a list of lists — one per flux coordinate, each the same length
    as ``y``. Returns the max MI over coordinates, its z-score, and the verdict.
    """
    best = {"mi": 0.0, "z": 0.0, "coord": -1}
    for i, col in enumerate(flux_cols):
        r = mi_significance(col, y, bins=bins, permutations=permutations)
        if r["mi"] > best["mi"]:
            best = {"mi": r["mi"], "z": r["z"], "coord": i}
    verdict = "structured" if best["z"] >= z_threshold else "random"
    return {
        "verdict": verdict,
        "max_mi": best["mi"],
        "max_z": best["z"],
        "coord": best["coord"],
    }


def _pearson(xs, ys) -> float:
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def _knn_predict(train_x, train_y, test_x, k: int):
    preds = []
    for tx in test_x:
        near = sorted(
            range(len(train_x)),
            key=lambda i: sum((a - b) ** 2 for a, b in zip(train_x[i], tx)),
        )[:k]
        preds.append(sum(train_y[i] for i in near) / k)
    return preds


def cv_predictability(fluxes, y, k: int = 5, n_folds: int = 5, seed: int = 0) -> float:
    """Cross-validated learnability: can flux predict the observable?

    K-nearest-neighbour regression, 5-fold CV, reporting the Pearson correlation
    between held-out predictions and the true values. ``> 0`` (well above the null)
    means the map ``flux -> y`` is *learnable* (predictable), not random — the
    "structured" branch confirmed by prediction, not just dependence.

    ``fluxes``: list of equal-length numeric vectors; ``y``: list of the same length.
    """
    rng = random.Random(seed)
    idx = list(range(len(fluxes)))
    rng.shuffle(idx)
    folds = [idx[i::n_folds] for i in range(n_folds)]
    preds = [0.0] * len(fluxes)
    for fold in folds:
        train = [i for i in idx if i not in set(fold)]
        train_x = [fluxes[i] for i in train]
        train_y = [y[i] for i in train]
        test_x = [fluxes[i] for i in fold]
        p = _knn_predict(train_x, train_y, test_x, k)
        for j, i in enumerate(fold):
            preds[i] = p[j]
    return _pearson(preds, y)


def _poly_features(f, degree: int = 2):
    """[1, f_i, f_i^2, f_i f_j] — the degree-2 monomial basis."""
    feats = [1.0]
    n = len(f)
    for i in range(n):
        feats.append(float(f[i]))
    if degree >= 2:
        for i in range(n):
            feats.append(float(f[i]) * float(f[i]))
        for i in range(n):
            for j in range(i + 1, n):
                feats.append(float(f[i]) * float(f[j]))
    return feats


def _gauss_solve(A, b):
    """Solve A x = b by Gaussian elimination with partial pivoting (stdlib)."""
    n = len(A)
    M = [list(row) + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-12:
            continue
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        for r in range(c + 1, n):
            factor = M[r][c] / pv
            for cc in range(c, n + 1):
                M[r][cc] -= factor * M[c][cc]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        if abs(M[r][r]) < 1e-12:
            x[r] = 0.0
            continue
        s = M[r][n] - sum(M[r][cc] * x[cc] for cc in range(r + 1, n))
        x[r] = s / M[r][r]
    return x


def _ridge_predict(train_x, train_y, test_x, lam: float = 1.0):
    """Ridge regression on degree-2 monomial features; predict test_x."""
    X = [_poly_features(f) for f in train_x]
    d = len(X[0])
    XtX = [[0.0] * d for _ in range(d)]
    Xty = [0.0] * d
    for xi, yi in zip(X, train_y):
        for a in range(d):
            Xty[a] += xi[a] * yi
            for b in range(d):
                XtX[a][b] += xi[a] * xi[b]
    for a in range(d):
        XtX[a][a] += lam
    beta = _gauss_solve(XtX, Xty)
    out = []
    for tf in test_x:
        feats = _poly_features(tf)
        out.append(sum(beta[k] * feats[k] for k in range(d)))
    return out


def ridge_cv_predictability(
    fluxes, y, lam: float = 1.0, n_folds: int = 5, seed: int = 0
) -> float:
    """Joint learnability: cross-validated ridge regression on quadratic features.

    The per-coordinate miner is blind to multi-coordinate structure (a quadratic
    form has weak per-coordinate dependence). This is the stronger test: it can
    fit any degree-2 function of the whole flux vector. Returns the CV Pearson r
    between predictions and truth — near 1 for deterministic quadratic structure
    (the tadpole control), near 0 for random observables.
    """
    rng = random.Random(seed)
    idx = list(range(len(fluxes)))
    rng.shuffle(idx)
    folds = [idx[i::n_folds] for i in range(n_folds)]
    preds = [0.0] * len(fluxes)
    for fold in folds:
        train = [i for i in idx if i not in set(fold)]
        train_x = [fluxes[i] for i in train]
        train_y = [y[i] for i in train]
        test_x = [fluxes[i] for i in fold]
        p = _ridge_predict(train_x, train_y, test_x, lam)
        for j, i in enumerate(fold):
            preds[i] = p[j]
    return _pearson(preds, y)
