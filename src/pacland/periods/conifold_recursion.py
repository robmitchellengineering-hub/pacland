"""The conifold recursion as a matrix in `rho` — the scaffolding the log branches need.

`docs/plan-facts.md` F2 M2d. Three of the four conifold branches carry logarithms (M2b), and the standard
way through a double root is to make the resonance cancel by taking `c_0(rho) = rho - s0`, then read the
two solutions off the first two terms of the expansion in `rho - s0`. That needs the recursion written as
a **matrix of polynomials in rho**, not as a sequence of numbers — which is what this module builds.

    A[n][m](rho) = the coefficient of `u^(s+n)` in `L(u^(s+m))`, with `L` in the `u` coordinate

so the recursion is `sum_m A[n][m](rho) c_m = 0` for every output index `n`, and the next coefficient is
`c_{n+3} = -sum_{m<n+3} A[n][m] c_m / A[n][n+3]`.

**Nothing here is a result yet.** What it is: the exact object the double-root construction will divide
by, checked against two computations that already exist — the indicial polynomial from M2a, and the
numeric exponent-2 series from M2c. If those two agree, the matrix is right and the Laurent-jet step that
follows has a foundation; if they disagree, the log construction would have been built on sand.

Run:        python3 scripts/conifold_recursion.py
Guarded by: tests/test_conifold_recursion.py
"""
from __future__ import annotations

import sympy as sp

from .conifold import S, apply_L_at_conifold, indicial_polynomial

#: How many coefficients of the series the recursion is built for.
N_DEFAULT = 20


def A_matrix(n_max: int = N_DEFAULT) -> dict:
    """`{(n, m): polynomial in rho}` — the recursion's matrix, for `-3 <= n <= n_max-3`, `0 <= m <= n+3`."""
    base = apply_L_at_conifold()          # L(u^s) = sum_k base[k] u^(s+k)
    lo = min(base)
    out = {}
    for m in range(n_max + 1):
        # L(u^(s+m)) = sum_k base[k] u^(s+m+k) with s -> s+m inside the coefficients
        for k, coeff in base.items():
            n = m + k
            if n < lo or n > n_max - 3:
                continue
            if m > n + 3:
                continue
            out[(n, m)] = sp.expand(coeff.subs(S, S + m))
    return out


def diagonal(n_max: int = N_DEFAULT) -> dict:
    """`A[n][n+3](rho)` — the coefficient the recursion divides by."""
    A = A_matrix(n_max)
    return {n: A.get((n, n + 3), sp.Integer(0)) for n in range(-2, n_max - 2)}


def indicial_from_matrix() -> sp.Expr:
    """`A[lowest][0]` — which must reproduce the indicial polynomial from M2a."""
    A = A_matrix()
    lo = min(n for (n, _m) in A)
    return sp.factor(sp.expand(A[(lo, 0)]))


def consistency(n_max: int = N_DEFAULT) -> dict:
    """Checks the matrix against the computations that already exist.

    Two things must hold, and neither is fitted:

    1. `A[lowest][0]` is the indicial polynomial from M2a;
    2. the diagonal `A[n][n+3]` vanishes at exactly the exponents M2b says resonate at that order —
       `s0 = 0` at `n = -2` and `n = -1`, `s0 = 1` at `n = -2` only, and never at `s0 = 2`.
    """
    A = A_matrix(n_max)
    lo = min(n for (n, _m) in A)
    ind = sp.factor(sp.expand(A[(lo, 0)]))
    known = indicial_polynomial()
    diag = diagonal(n_max)

    def vanishes(n, s0):
        poly = diag.get(n)
        return poly is not None and sp.simplify(poly.subs(S, s0)) == 0

    pattern = {
        "n=-2, s0=0": vanishes(-2, 0),
        "n=-2, s0=1": vanishes(-2, 1),
        "n=-1, s0=0": vanishes(-1, 0),
        "n=-1, s0=1": vanishes(-1, 1),
        "s0=2 nowhere": all(not vanishes(n, 2) for n in diag),
    }
    expected = {"n=-2, s0=0": True, "n=-2, s0=1": True, "n=-1, s0=0": True,
                "n=-1, s0=1": False, "s0=2 nowhere": True}
    return {"lowest_index": lo, "indicial_from_matrix": ind, "indicial_known": known,
            "indicial_matches": sp.simplify(ind - known) == 0,
            "resonance_pattern": pattern, "resonance_expected": expected,
            "pattern_matches": pattern == expected,
            "all_pass": sp.simplify(ind - known) == 0 and pattern == expected}


def _exact(expr):
    """Convert a sympy rational to `mpf` exactly, with no decimal round-trip."""
    import mpmath as mp
    r = sp.Rational(expr)
    return mp.mpf(int(r.p)) / mp.mpf(int(r.q))


def numeric_series(n_max: int = 20, s0: int = 2, dps: int = 40) -> list:
    """Solve the recursion at `rho = s0` from the matrix — must reproduce M2c's numeric series."""
    import mpmath as mp
    mp.mp.dps = dps
    A = A_matrix(n_max)
    c = [None] * (n_max + 1)
    c[0] = mp.mpf(1)
    for n in range(-2, n_max - 2):
        m = n + 3
        if m > n_max:
            break
        acc = mp.mpf(0)
        for k in range(m):
            if (n, k) not in A:
                continue
            acc += _exact(A[(n, k)].subs(S, s0)) * c[k]
        diag = A.get((n, m))
        if diag is None or sp.simplify(diag.subs(S, s0)) == 0:
            raise ArithmeticError(f"resonance at index {n} for s0={s0}")
        c[m] = -acc / _exact(diag.subs(S, s0))
    return c


# ---------------------------------------------------------------------------------------
# the double root at 1: two branches, and their connections
# ---------------------------------------------------------------------------------------
def _solve(s0, c0, A: dict, n_max: int, dps: int = 50):
    import mpmath as mp
    mp.mp.dps = dps
    c = [mp.mpf(0)] * (n_max + 1)
    c[0] = c0
    for n in range(-2, n_max - 2):
        m = n + 3
        if m > n_max:
            break
        acc = mp.mpf(0)
        for k in range(m):
            if (n, k) in A:
                acc += _exact(A[(n, k)].subs(S, s0)) * c[k]
        diag = A.get((n, m))
        if diag is None:
            raise ArithmeticError(f"missing diagonal at n={n}")
        dv = _exact(diag.subs(S, s0))
        if dv == 0:
            raise ArithmeticError(f"resonance at n={n} for s0={s0}")
        c[m] = -acc / dv
    return c


def double_root(n_max: int = 80, eps: str = "1e-15", dps: int = 50) -> dict:
    """The two branches at the double root `rho = 1`, by the resonant-cancelling normalisation.

    Taking `c_0 = delta` with `rho = 1 + delta` cancels the resonance at `n = -2` (`A[-2][1]` vanishes
    linearly there while the numerator vanishes quadratically), so every coefficient is analytic in
    `delta`. Evaluating at `+delta` and `-delta` then gives the even and odd parts, i.e. the two branches:

        Phi_A = u   sum_n d_n(0) u^n
        Phi_B = u ( log u sum_n d_n(0) u^n + sum_n d_n'(0) u^n )

    with `d_n = c_n / delta`. `u = 1 - z/z_c`.
    """
    import mpmath as mp
    mp.mp.dps = dps
    A = A_matrix(n_max)
    e = mp.mpf(eps)
    cp = _solve(1 + e, e, A, n_max, dps)
    cm = _solve(1 - e, -e, A, n_max, dps)
    d0 = [(cp[n] - cm[n]) / (2 * e) for n in range(n_max + 1)]
    d1 = [(cp[n] + cm[n]) / (2 * e * e) for n in range(n_max + 1)]
    return {"d0": d0, "d1": d1, "n_max": n_max}


def phi_series(z, d: dict):
    """The exponent-1 branch with no logarithm."""
    import mpmath as mp
    from .connection import ZC
    u = 1 - mp.mpf(z) / ZC
    return u * sum(d["d0"][n] * u ** n for n in range(d["n_max"] + 1))


def phi_log(z, d: dict):
    """The exponent-1 branch carrying `log u` — the one a conifold period is made of."""
    import mpmath as mp
    from .connection import ZC
    u = 1 - mp.mpf(z) / ZC
    return u * (mp.log(u) * sum(d["d0"][n] * u ** n for n in range(d["n_max"] + 1)) +
                sum(d["d1"][n] * u ** n for n in range(d["n_max"] + 1)))


def connect_function(f, n_max_lcs: int = 140, dps: int = 50) -> dict:
    """Express any conifold-side function in the LCS basis and test the fit away from the fit points."""
    import mpmath as mp
    from .connection import FIT_POINTS, TEST_POINTS, ZC, lcs_basis
    mp.mp.dps = dps
    M = mp.matrix(4, 4)
    b = mp.matrix(4, 1)
    for i, frac in enumerate(FIT_POINTS):
        z = ZC * mp.mpf(frac)
        w = lcs_basis(z, n_max_lcs, dps)
        b[i] = f(z)
        for k in range(4):
            M[i, k] = w[k]
    a = mp.lu_solve(M, b)
    rows = []
    for frac in TEST_POINTS:
        z = ZC * mp.mpf(frac)
        w = lcs_basis(z, n_max_lcs, dps)
        pred = sum(a[k] * w[k] for k in range(4))
        exact = f(z)
        rows.append({"z": frac, "relative": abs(pred - exact) / abs(exact)})
    return {"coefficients": [a[k] for k in range(4)], "rows": rows,
            "worst": max(r["relative"] for r in rows),
            "closes": max(r["relative"] for r in rows) < 1e-10}


def all_branches(n_max: int = 80, dps: int = 50) -> dict:
    """The three conifold branches reachable today, each with its connection and its residual."""
    d = double_root(n_max, dps=dps)
    return {"exponent_2": connect_function(lambda z: __import__("pacland.periods.connection",
                                                               fromlist=["conifold_value"])
                                           .conifold_value(z, __import__(
                                               "pacland.periods.connection", fromlist=["conifold_series"]
                                           ).conifold_series(160)), dps=dps),
            "exponent_1_series": connect_function(lambda z: phi_series(z, d), dps=dps),
            "exponent_1_log": connect_function(lambda z: phi_log(z, d), dps=dps)}


__all__ = ["N_DEFAULT", "A_matrix", "diagonal", "indicial_from_matrix", "consistency",
           "numeric_series", "double_root", "phi_series", "phi_log", "connect_function",
           "all_branches"]
