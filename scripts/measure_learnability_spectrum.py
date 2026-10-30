"""Learnability spectrum — linear flux->observable R^2 + F-test (verification angle).

For each scalar observable (log_W0, log_gs, tadpole) fit a linear model from the
12 flux features and report R^2 and the F-statistic. This *certifies* whether an
observable carries linear structure (learnable) or is random — the rigorous,
certification-flavoured complement to non-linear structure mining.

Built-in sanity check: ``tadpole`` is a deterministic function of flux, so it
should give R^2 ~ 1; ``log_W0`` should give R^2 ~ 0 (Denef-Douglas random);
``log_gs`` in between (the other session found non-linear structure there).

Pure stdlib. n = 107 vacua, p = 12 flux features, residual df = n - p - 1 = 94.
Critical F(12, 94) ~ 1.85 at p=0.05.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "flux_observables.json")


def solve(A, b):
    """Solve Ax = b by Gaussian elimination with partial pivoting (in-place copies)."""
    import copy
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]  # augmented
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-12:
            continue  # singular; leave zeros
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
    """Multiple linear regression: returns R^2, F, and the fitted coefficients."""
    n = len(features)
    p = len(features[0])
    # design matrix with intercept
    X = [[1.0] + list(f) for f in features]
    k = p + 1
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    Xty = [sum(X[i][a] * targets[i] for i in range(n)) for a in range(k)]
    beta = solve(XtX, Xty)
    yhat = [sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    ymean = sum(targets) / n
    ss_res = sum((targets[i] - yhat[i]) ** 2 for i in range(n))
    ss_tot = sum((targets[i] - ymean) ** 2 for i in range(n))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    r2 = max(0.0, min(1.0, r2))
    df_res = n - k
    f = (r2 / p) / ((1.0 - r2) / df_res) if (r2 < 1.0 and df_res > 0 and r2 > 0) else 0.0
    return r2, f


def main() -> int:
    with open(DATA) as fh:
        data = json.load(fh)

    rows = []
    for d in data.values():
        rows.extend(d)

    # scalar observables
    targets = {
        "log_W0": [r["log_W0"] for r in rows],
        "log_gs": [r["log_gs"] for r in rows],
        "tadpole": [r["tadpole"] for r in rows],
        # summaries of the variable-length observables
        "n_gauge_couplings": [len(r.get("log_g2_inv", [])) for r in rows],
        "n_masses": [len(r.get("log_mass2", [])) for r in rows],
    }
    features = [r["flux"] for r in rows]
    n = len(rows)

    out = {"n_vacua": n, "p_flux_features": 12, "residual_df": n - 13}
    for name, ys in targets.items():
        r2, f = linreg(features, ys)
        out[name] = {"R2": round(r2, 4), "F": round(f, 2), "verdict": _verdict(r2, f)}
    print(json.dumps(out, indent=2))
    return 0


def _verdict(r2, f):
    if f > 1.85:  # p < 0.05
        return "linearly learnable (structure)"
    if f > 1.0:
        return "weak / marginal"
    return "random (no linear structure)"


if __name__ == "__main__":
    sys.exit(main())
