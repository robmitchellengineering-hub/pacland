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


# ---------------------------------------------------------------------------------------
# the connection matrix: is there a closed algebraic form?
# ---------------------------------------------------------------------------------------
#: The basis a connection coefficient could plausibly be built from: the transcendental weight system of the
#: conifold-to-LCS map. `{1, pi^2, zeta(3), pi^2 zeta(3)}` covers weights 0, 2, 3 and 5.
BASIS = ("1", "pi^2", "zeta(3)", "pi^2*zeta(3)")


def connection_coefficients(n_max: int = 120, dps: int = 80) -> list:
    """The four coefficients of the exponent-2 branch in the LCS basis, as high-precision numbers."""
    import mpmath as mp

    from . import conifold_recursion as R

    mp.mp.dps = dps
    b = R.all_branches(n_max=n_max, dps=dps)
    return [mp.mpf(c) for c in b["exponent_2"]["coefficients"]]


def connection_form(maxcoeff: int = 10 ** 6, dps: int = 80, n_max: int = 120) -> dict:
    """Integer-relation search: is a connection coefficient a rational combination of `BASIS`?

    Uses PSLQ, which returns **small** integer coefficients when a genuine relation exists and large ones when
    it does not. That distinction is the whole method: a hit at `maxcoeff = 1e12` is a numerical artefact, not a
    discovery, and reporting it as an algebraic form would be the cancellation error this estate keeps catching.

    **Result (2026-10-30): no relation below `10^6`.** So on this evidence the connection coefficients are not
    in the span of `{1, pi^2, zeta(3), pi^2 zeta(3)}` with small rational coefficients — and the mirror-map
    residual therefore stays labelled **measured**.
    """
    import mpmath as mp

    mp.mp.dps = dps
    basis = [mp.mpf(1), mp.pi ** 2, mp.zeta(3), mp.pi ** 2 * mp.zeta(3)]
    rows = []
    for a in connection_coefficients(n_max, dps):
        try:
            rel = mp.pslq(basis + [a], maxcoeff=maxcoeff, tol=mp.mpf(10) ** (-(dps // 2)),
                          maxsteps=100000)
        except Exception:
            rel = None
        rows.append({"value": mp.nstr(a, 20), "relation": rel, "found": rel is not None})
    return {
        "basis": list(BASIS), "maxcoeff": maxcoeff, "dps": dps, "rows": rows,
        "any_found": any(r["found"] for r in rows),
        "statement": (f"no integer relation with coefficients below {maxcoeff} at {dps} dps"
                      if not any(r["found"] for r in rows)
                      else "a relation was found — verify it independently before calling it exact"),
        "consequence": ("the connection matrix is NOT derived exactly; its residual stays labelled 'measured'. "
                        "A wider basis (weights 4, 6, or log-structured terms) was not tested, so this bounds "
                        "the claim rather than closing the question."),
    }
