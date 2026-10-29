"""The connection at the conifold — the conifold branch expressed in the LCS basis.

`docs/plan-facts.md` F2 M2c. The z = 0 series cannot reach the conifold (it sits on the radius, #213), so
the conifold needs its own expansion; M2a gave its exponents (0, 1, 1, 2) and M2b the resonances (only
the exponent-2 branch is free of logarithms). This is the payoff: build that branch numerically, express
it in the four z = 0 branches, and demand the coefficients be **independent of where you evaluate**.

**The test is the point.** There is no literature constant anywhere in here. If the two expansions are
both right, a constant 4-vector reproduces the conifold series from the LCS basis at every point where
both converge; if anything is wrong, the residual grows. It does not close by construction — it closes
because both sides are solutions of the same ODE.

**What it caught.** The first version did not close: 6.4e-2 at z = 0.7 z_c rising to 124 at 0.95 z_c. The
cause was the log normalisation of `omega_1..omega_3` — the k-th Frobenius solution is
`d^k/drho^k (z^rho Phi)` = `sum_j C(k,j) L^j Phi^(k-j)`, and the binomial weight had been dropped, leaving
`omega_2` and `omega_3` outside the solution space. With the weight restored the connection closes to
**5e-26** at z = 0.7 z_c. That is why the gate exists.

Run:        python3 scripts/conifold_connection.py
Guarded by: tests/test_conifold_connection.py
"""
from __future__ import annotations

import mpmath as mp

from . import quintic as Q

ZC = Q.Z_CONIFOLD

#: Points used to fit the connection, as fractions of `z_c`. All < 1 so both expansions converge.
FIT_POINTS = ("0.3", "0.4", "0.5", "0.6")

#: Points the fitted connection is tested at, none of them used in the fit and all far enough inside the
#: conifold's radius that its own truncation is negligible.
TEST_POINTS = ("0.55", "0.65", "0.7", "0.75")

#: Reported but excluded from the verdict: at these the *conifold series* truncation dominates
#: (`0.95^160 ~ 3e-4`), so a residual here is a statement about term count, not about the physics.
TRUNCATION_LIMITED = ("0.8", "0.9", "0.95")


def operator_action(coeffs: list, s0: int) -> dict:
    """`L(u^s0 sum c_m u^m)` -> output coefficients by offset, with `Theta = -(1-u) d/du`."""
    def theta(f):
        out = {}
        for m, c in f.items():
            out[m - 1] = out.get(m - 1, 0) - (s0 + m) * c
            out[m] = out.get(m, 0) + (s0 + m) * c
        return out

    def lin(a, b, ca=1, cb=1):
        out = {}
        for k, v in a.items():
            out[k] = out.get(k, 0) + ca * v
        for k, v in b.items():
            out[k] = out.get(k, 0) + cb * v
        return {k: v for k, v in out.items() if v != 0}

    f = {m: c for m, c in enumerate(coeffs)}
    t4 = f
    for _ in range(4):
        t4 = theta(t4)
    p = f
    for k in (1, 2, 3, 4):
        p = lin({n: 5 * c for n, c in theta(p).items()}, {n: k * c for n, c in p.items()})
    zcp = lin({m: ZC * c for m, c in p.items()}, {m + 1: -ZC * c for m, c in p.items()})
    return lin(t4, zcp, 1, -5)


def conifold_series(n_max: int = 160, s0: int = 2) -> list:
    """The exponent-`s0` conifold series, by a numerical triangular solve of the recursion.

    Only `s0 = 2` is free of resonances (M2b), so only this branch is reachable this way; the other three
    need the log algebra in `u`.
    """
    A: dict = {}
    for m in range(n_max + 1):
        e = [mp.mpf(0)] * (n_max + 1)
        e[m] = mp.mpf(1)
        for n, v in operator_action(e, s0).items():
            A.setdefault(n, {})[m] = v
    c = [mp.mpf(0)] * (n_max + 1)
    c[0] = mp.mpf(1)
    for n in range(-2, n_max - 2):          # n = -3 is the indicial equation, satisfied identically
        m = n + 3
        if m > n_max:
            break
        acc = sum(A.get(n, {}).get(k, 0) * c[k] for k in range(m))
        diag = A.get(n, {}).get(m, 0)
        if diag == 0:
            raise ArithmeticError(f"resonance at index {n} on the s0={s0} branch")
        c[m] = -acc / diag
    return c


def conifold_value(z, c: list, s0: int = 2):
    """The conifold series at `z`, in `u = 1 - z/z_c`."""
    u = 1 - mp.mpf(z) / ZC
    return sum(c[n] * u ** (s0 + n) for n in range(len(c)))


def lcs_basis(z, n_max: int = 140, dps: int = 50) -> list:
    """The four z = 0 branches at `z`, as numbers (they carry `log z`)."""
    z = mp.mpf(z)
    out = []
    for k in range(4):
        parts = Q.as_log_parts(k, n_max, dps=dps)
        out.append(sum(mp.log(z) ** j / mp.factorial(j) *
                       sum(f[n] * z ** n for n in range(n_max + 1))
                       for j, f in enumerate(parts) if j <= k))
    return out


def connect(n_max: int = 160, dps: int = 50) -> dict:
    """Fit the conifold branch against the LCS basis and report where the fit fails.

    Returns the coefficients, the conditioning of the fit, and the residual at points **not** used in it.
    A correct pair of expansions gives residuals at the truncation level; anything else is a finding.
    """
    mp.mp.dps = dps
    c = conifold_series(n_max)
    M = mp.matrix(4, 4)
    b = mp.matrix(4, 1)
    for i, frac in enumerate(FIT_POINTS):
        z = ZC * mp.mpf(frac)
        w = lcs_basis(z, n_max, dps)
        b[i] = conifold_value(z, c)
        for k in range(4):
            M[i, k] = w[k]
    a = mp.lu_solve(M, b)
    rows = []
    for frac in TEST_POINTS + TRUNCATION_LIMITED:
        z = ZC * mp.mpf(frac)
        w = lcs_basis(z, n_max, dps)
        pred = sum(a[k] * w[k] for k in range(4))
        exact = conifold_value(z, c)
        rows.append({"z": frac, "predicted": pred, "series": exact,
                     "relative": abs(pred - exact) / abs(exact),
                     "in_verdict": frac in TEST_POINTS})
    worst = max(r["relative"] for r in rows if r["in_verdict"])
    return {"coefficients": [a[k] for k in range(4)], "cond": mp.cond(M), "det": mp.det(M),
            "fit_points": FIT_POINTS, "rows": rows, "n_max": n_max,
            "worst": worst, "worst_reporting_only": max(r["relative"] for r in rows),
            "closes": worst < 1e-12}


__all__ = ["ZC", "FIT_POINTS", "TEST_POINTS", "TRUNCATION_LIMITED", "operator_action", "conifold_series", "conifold_value",
           "lcs_basis", "connect"]
