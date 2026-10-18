"""Learnability guards — certify "is this observable learnable?" (guarded, mutation-tested).

Turns the learnability measurement into a guarded claim. ``guard_no_linear_structure``
asserts an observable has linear R^2 below a threshold — "not linearly learnable" —
and its mutation test (``tests/test_learnability_guards.py``) proves the guard
REJECTS a synthetic target that is a known linear function of the features
(required-to-fail).

This is the verification discipline applied to the learnability question itself:
a claim that survives the guard, whose guard is proven to fail on structure, is a
*certified* claim — not just a measured one.
"""
from __future__ import annotations


def _solve(A, b):
    """Solve Ax = b by Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-12:
            continue
        M[c], M[piv] = M[piv], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for cc in range(c, n + 1):
                M[r][cc] -= f * M[c][cc]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        if abs(M[r][r]) < 1e-12:
            x[r] = 0.0
            continue
        x[r] = (M[r][n] - sum(M[r][cc] * x[cc] for cc in range(r + 1, n))) / M[r][r]
    return x


def linreg(features, targets):
    """Multiple linear regression with intercept; returns (R^2, F)."""
    n = len(features)
    p = len(features[0])
    X = [[1.0] + list(f) for f in features]
    k = p + 1
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    Xty = [sum(X[i][a] * targets[i] for i in range(n)) for a in range(k)]
    beta = _solve(XtX, Xty)
    yhat = [sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    ymean = sum(targets) / n
    ss_res = sum((targets[i] - yhat[i]) ** 2 for i in range(n))
    ss_tot = sum((targets[i] - ymean) ** 2 for i in range(n))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    r2 = max(0.0, min(1.0, r2))
    df_res = n - k
    f = (r2 / p) / ((1.0 - r2) / df_res) if (0.0 < r2 < 1.0 and df_res > 0) else 0.0
    return r2, f


def guard_no_linear_structure(features, targets, r2_threshold: float = 0.3):
    """Assert the observable has no linear structure: linear R^2 < threshold.

    A synthetic target that is a known linear function of the features MUST make
    this guard fail — that is the mutation test proving the guard can catch
    structure (required-to-fail).
    """
    r2, f = linreg(features, targets)
    ok = r2 < r2_threshold
    return ok, f"R2={r2:.3f} F={f:.2f} (threshold {r2_threshold})"


def _pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def max_cross_correlation(features, targets):
    """Largest |correlation| between a pairwise product f_i*f_j and the target."""
    dim = len(features[0])
    best = 0.0
    for i in range(dim):
        for j in range(i + 1, dim):
            r = abs(_pearson([f[i] * f[j] for f in features], targets))
            best = max(best, r)
    return best


def guard_no_quadratic_structure(features, targets, r_threshold: float = 0.3):
    """Assert no pairwise-quadratic structure: max cross-term |corr| < threshold.

    Separates "random" (passes) from "nonlinear/quadratic" (fails) — e.g. the D3
    tadpole is quadratic in the flux and must FAIL this guard, while W0 passes.
    """
    m = max_cross_correlation(features, targets)
    ok = m < r_threshold
    return ok, f"max_cross|r|={m:.3f} (threshold {r_threshold})"


__all__ = [
    "linreg",
    "max_cross_correlation",
    "guard_no_linear_structure",
    "guard_no_quadratic_structure",
]
