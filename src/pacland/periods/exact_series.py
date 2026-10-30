"""Route C, exact sub-item — the conifold coefficients are **rational**, not transcendental.

The conifold recursion is solved numerically (mpmath, 60 dps) everywhere else in this repo, and the connection
is then quoted as "residual 2.3e-21" — a measurement. But the recursion's inputs are sympy rationals and the
only non-rational step is `_exact()`, which converts each rational to a float. Solving the same recursion
without that conversion produces the coefficients **exactly**, and the question "is this measured or proven"
disappears for them.

**What this establishes.** Every coefficient of the exponent-`s0` conifold series is a rational number. The
transcendental structure (`zeta(3)`, `pi^2`) does *not* live in the series — it enters only when the series is
expressed in the large-complex-structure basis, which is a different (and larger) computation. So the honest
split is:

    conifold coefficients   exact rationals        -- proven here
    connection matrix       rationals x {1, zeta(3), pi^2, pi^2 zeta(3)}   -- NOT done here, see below

**What is not claimed.** The connection coefficients are not derived exactly. That needs the LCS period basis in
exact form (the `log`-branch values include `zeta(3)` terms), which is a separate build; until it exists, the
connection's residual stays labelled *measured*.

**Hybrid, stated.** Exact rationals to order `N`; beyond that the recursion fixes every later coefficient
uniquely from the same matrix, so the exactness is not order-limited in principle — only the printed list is.

Run:        python3 scripts/exact_series.py
Guarded by: tests/test_exact_series.py
"""
from __future__ import annotations

from fractions import Fraction

import sympy as sp

from . import conifold_recursion as R

S = R.S


def conifold_coefficients(n_max: int = 12, s0: int = 2) -> list[Fraction]:
    """The exponent-`s0` conifold series coefficients, **exactly**, in `Q`."""
    A = R.A_matrix(n_max)
    c: list = [Fraction(0)] * (n_max + 1)
    c[0] = Fraction(1)
    for n in range(-2, n_max - 2):
        m = n + 3
        if m > n_max:
            break
        acc = Fraction(0)
        for k in range(m):
            if (n, k) not in A:
                continue
            acc += Fraction(sp.Rational(A[(n, k)].subs(S, s0))) * c[k]
        diag = A.get((n, m))
        if diag is None:
            raise ArithmeticError(f"missing diagonal at n={n}")
        dv = Fraction(sp.Rational(diag.subs(S, s0)))
        if dv == 0:
            raise ArithmeticError(f"resonance at n={n} for s0={s0}")
        c[m] = -acc / dv
    return c


def against_numeric(n_max: int = 12, s0: int = 2, dps: int = 60) -> dict:
    """The exact coefficients against the numeric ones the rest of the repo uses."""
    import mpmath as mp

    mp.mp.dps = dps
    exact = conifold_coefficients(n_max, s0)
    numeric = R.numeric_series(n_max=n_max, s0=s0, dps=dps)
    worst = mp.mpf(0)
    for e, nv in zip(exact, numeric):
        if e == 0:
            continue
        em = mp.mpf(int(e.numerator)) / mp.mpf(int(e.denominator))
        worst = max(worst, abs(em - nv) / abs(em))
    return {"n_max": n_max, "worst_relative": float(worst),
            "all_rational": all(isinstance(x, Fraction) for x in exact),
            "exact": exact}


def form() -> dict:
    """What the exact answer says about where the transcendental structure lives."""
    r = against_numeric(12)
    return {
        "statement": ("every conifold coefficient is a rational number; the transcendental structure "
                      "(zeta(3), pi^2) enters only when the series is expressed in the LCS basis"),
        "first_coefficients": [str(x) for x in r["exact"][:5]],
        "agreement_with_numeric": r["worst_relative"],
        "connection_matrix": ("NOT derived exactly here: it needs the LCS period basis in exact form, so its "
                              "residual stays labelled 'measured'"),
    }


__all__ = ["conifold_coefficients", "against_numeric", "form"]
