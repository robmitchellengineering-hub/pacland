#!/usr/bin/env python3
"""F2 M2c (in progress) - the connection between the z=0 and conifold expansions.

    python3 scripts/conifold_connection.py

WHAT THIS DOES. Builds the conifold solution of exponent 2 by a numerical triangular solve of the
recursion (the approach F2 M2b said to take), then asks the only question that both expansions can be
held to: **is the conifold branch a constant linear combination of the four z=0 branches?** If the two
sides are right, the coefficients must not depend on where you evaluate them.

WHAT IT CURRENTLY REPORTS. The LCS side is converged (identical to 12 digits at 60, 140 and 300 terms)
and its 4x4 system is well conditioned (1.4e7 at 60 digits). The conifold series satisfies its own
recursion to all retained orders. **And the connection does not close**: the residual grows from 6% at
z=0.7 z_c to 124% at z=0.95 z_c. So ONE SIDE IS WRONG, and this script is what catches it. No number
from it may be quoted.

MOST LIKELY SUSPECT. Only omega_0 was ever independently verified (its coefficients match
(5n)!/(n!)^5 exactly). omega_1..omega_3 come from the rho-jets and have only passed structural checks,
so their **log normalisation** is the unverified ingredient. The next step is to verify each omega_k
against the operator in z (complex-step differentiation, not nested finite differences - see F2 M1's
method finding) before rebuilding the connection.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402

from pacland.periods import quintic as Q  # noqa: E402

ZC = Q.Z_CONIFOLD


def operator_action(coeffs, s0):
    """`L(u^s0 sum c_m u^m)` -> output coefficients by offset, using Theta = -(1-u)d/du."""
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


def conifold_series(n_max: int, s0: int = 2):
    """The exponent-`s0` series by a numerical triangular solve — the clean branch only."""
    A = {}
    for m in range(n_max + 1):
        e = [mp.mpf(0)] * (n_max + 1)
        e[m] = mp.mpf(1)
        for n, v in operator_action(e, s0).items():
            A.setdefault(n, {})[m] = v
    c = [mp.mpf(0)] * (n_max + 1)
    c[0] = mp.mpf(1)
    for n in range(-2, n_max - 2):        # n = -3 is the indicial equation, satisfied identically
        m = n + 3
        if m > n_max:
            break
        acc = sum(A.get(n, {}).get(k, 0) * c[k] for k in range(m))
        diag = A.get(n, {}).get(m, 0)
        if diag == 0:
            raise ArithmeticError(f"resonance at index {n}")
        c[m] = -acc / diag
    return c


def phi(z, c):
    u = 1 - mp.mpf(z) / ZC
    return sum(c[n] * u ** (2 + n) for n in range(len(c)))


def omegas(z, n_max=140, dps=50):
    z = mp.mpf(z)
    out = []
    for k in range(4):
        parts = Q.as_log_parts(k, n_max, dps=dps)
        out.append(sum(mp.log(z) ** j / mp.factorial(j) *
                       sum(f[n] * z ** n for n in range(n_max + 1))
                       for j, f in enumerate(parts) if j <= k))
    return out


def main() -> int:
    mp.mp.dps = 60
    c = conifold_series(160)
    zs = [ZC * mp.mpf(f) for f in ("0.3", "0.4", "0.5", "0.6")]
    M = mp.matrix(4, 4)
    b = mp.matrix(4, 1)
    for i, z in enumerate(zs):
        w = omegas(z)
        b[i] = phi(z, c)
        for k in range(4):
            M[i, k] = w[k]
    print("F2 M2c - the conifold connection (IN PROGRESS, no result may be quoted)\n")
    print(f"  LCS system: det {mp.nstr(mp.det(M), 6)}   cond {mp.nstr(mp.cond(M), 6)}")
    a = mp.lu_solve(M, b)
    print("  fitted connection:", [mp.nstr(x, 12) for x in a])
    print("\n  constancy test at points NOT used in the fit:")
    worst = mp.mpf(0)
    for f in ("0.7", "0.8", "0.9", "0.95"):
        z = ZC * mp.mpf(f)
        w = omegas(z)
        pred = sum(a[k] * w[k] for k in range(4))
        rel = abs(pred - phi(z, c)) / abs(phi(z, c))
        worst = max(worst, rel)
        print(f"    z = {f:>4} z_c   predicted {mp.nstr(pred, 14):>18}   series {mp.nstr(phi(z, c), 14):>18}   rel {mp.nstr(rel, 3)}")
    print(f"\n  worst relative residual: {mp.nstr(worst, 4)}")
    print("\n  A constant combination would give ~1e-20 here. It does not. One side is wrong, and only")
    print("  omega_0 has ever been independently verified - the log normalisation of omega_1..omega_3 is")
    print("  the unverified ingredient. Diagnose that before anything is quoted.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
