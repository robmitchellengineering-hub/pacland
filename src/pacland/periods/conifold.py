"""The conifold's local exponents — computed exactly, not quoted.

`docs/plan-facts.md` F2, milestone 2a. The z = 0 series cannot certify the conifold: `quintic.Z_CONIFOLD`
sits exactly on its radius of convergence, and the tail bound there is 9.4e-05 against 1.5e-97 at
`z_c/2` (measured, 300 terms). The conifold needs its own expansion, and the first thing that expansion
needs is the **indicial exponents** — the powers of `u = 1 - z/z_c` at which solutions can start.

They are computed here by applying the operator to `u^s` exactly, in sympy, with

    Theta(u^(s+n)) = -(s+n) u^(s+n-1) + (s+n) u^(s+n)

which is `theta = z d/dz` rewritten in `u`. The lowest power of `u` in `L(u^s)` carries the indicial
polynomial; the exponents are its roots.

**Result.** The singular points of the one-parameter family are at `z = 0` (large complex structure) and
`z = z_c` (conifold), and in the `u` coordinate the conifold is a regular singular point with a simple
zero in the leading coefficient. The exponents are

    0, 1, 1, 2

— two simple roots and a **double root at 1**. All four are integers, which is what a conifold's
Picard-Lefschetz monodromy requires: every eigenvalue of `exp(2 pi i s)` is 1, so the monodromy is
unipotent. The double root is where the single logarithm lives, i.e. the monodromy has index 2.

**What this buys.** The exponents fix the shape of the four local solutions and tell you the log structure
before a single coefficient is computed. It also fixes the **radius** of the local expansion: in `u` the
other singular point is at `u = 1` (that is `z = 0`), so the conifold series is bounded for `|u| < 1`
and — unlike the `z = 0` series at the conifold — it can be pushed toward `z = 0` with a real bound. The
next step is the connection: match the two expansions at a point where both converge (`|z| < z_c` and
`|u| < 1`, e.g. `z = z_c/2`) and solve a 4x4 system, which determines the conifold periods **without**
needing a literature constant.

Run:        python3 scripts/conifold_exponents.py
Guarded by: tests/test_conifold_exponents.py
"""
from __future__ import annotations

import sympy as sp

from .quintic import Z_CONIFOLD

#: `z`-plane singular points of the one-parameter family, in the `z = 1/(5 psi)^5` coordinate.
SINGULAR_POINTS = {"large complex structure": sp.Integer(0), "conifold": sp.Rational(1, 5 ** 5)}

S = sp.symbols("s")


def _theta_series(f: dict) -> dict:
    """`u d/du`-style action: `Theta = -(1-u) d/du` on `sum_n c_n u^(s+n)`."""
    out: dict = {}
    for n, c in f.items():
        out[n - 1] = sp.simplify(out.get(n - 1, 0) - (S + n) * c)
        out[n] = sp.simplify(out.get(n, 0) + (S + n) * c)
    return {k: v for k, v in out.items() if v != 0}


def _lin(a: dict, b: dict, ca=1, cb=1) -> dict:
    out: dict = {}
    for k, v in a.items():
        out[k] = sp.simplify(out.get(k, 0) + ca * v)
    for k, v in b.items():
        out[k] = sp.simplify(out.get(k, 0) + cb * v)
    return {k: v for k, v in out.items() if v != 0}


def _times_zc_1mu(f: dict, zc=sp.Rational(1, 5 ** 5)) -> dict:
    """Multiply by `z_c (1-u)`."""
    return _lin({n: zc * c for n, c in f.items()}, {n + 1: -zc * c for n, c in f.items()})


def apply_L_at_conifold(zc=sp.Rational(1, 5 ** 5)) -> dict:
    """`L = Theta^4 - 5 z P(Theta)` acting on `u^s`, as a dict `{index: coefficient}`."""
    f = {0: sp.Integer(1)}
    t4 = f
    for _ in range(4):
        t4 = _theta_series(t4)
    p = f
    for k in (1, 2, 3, 4):
        p = _lin({n: 5 * c for n, c in _theta_series(p).items()}, {n: k * c for n, c in p.items()})
    return _lin(t4, _times_zc_1mu(p, zc), 1, -5)


def indicial_polynomial() -> sp.Expr:
    """The coefficient of the lowest power of `u` in `L(u^s)` — the indicial polynomial."""
    Lf = apply_L_at_conifold()
    return sp.factor(sp.expand(Lf[min(Lf)]))


def exponents() -> list:
    """The roots of the indicial polynomial, sorted, with multiplicity."""
    Lf = apply_L_at_conifold()
    poly = sp.Poly(Lf[min(Lf)], S)
    roots = []
    for root, mult in sp.roots(poly, S).items():
        roots.extend([sp.nsimplify(root)] * mult)
    return sorted(roots, key=lambda r: sp.Rational(r))


def structure() -> dict:
    """The report: exponents, multiplicities, integer-ness, and the monodromy consequence."""
    ex = exponents()
    from collections import Counter
    mult = Counter(str(e) for e in ex)
    integral = all(sp.denom(sp.nsimplify(e)) == 1 for e in ex)
    return {"exponents": ex, "multiplicities": dict(mult),
            "indicial": indicial_polynomial(), "all_integer": integral,
            "unipotent": integral,
            "double_root": [k for k, v in mult.items() if v > 1],
            "singular_points": SINGULAR_POINTS,
            "local_radius": "|u| < 1 (the next singular point is u = 1, i.e. z = 0)",
            "z_conifold": Z_CONIFOLD}


__all__ = ["SINGULAR_POINTS", "apply_L_at_conifold", "indicial_polynomial", "exponents", "structure"]
