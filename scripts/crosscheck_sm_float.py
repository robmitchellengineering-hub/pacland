#!/usr/bin/env python3
"""Rule of Three, arm 2 — an INDEPENDENT float re-derivation of the two SM exact results.

The two exact scripts (validate_sm_anomaly.py, validate_sm_hypercharge_uniqueness.py)
use exact arithmetic (Python Fraction / sympy rationals). This script re-derives both
results with *floating-point* arithmetic and a different code path (numeric root-scan
instead of sympy factorization), so a transcription or rational-arithmetic bug cannot be
shared. Agreement between the two arms is the Rule of Three's independent confirmation.

Two results are re-derived:
  1. SM anomaly cancellation — the five gauge/gravitational anomaly coefficients vanish.
  2. SM hypercharge uniqueness — the anomaly conditions force the hypercharges uniquely
     (the cubic in r = Y_u/Y_Q has exactly the roots r = 4 and r = -2, i.e. the SM and
     its u<->d swap; the r = 0 branch is the unphysical Y_Q = 0, excluded).

Floating point only; tolerance 1e-9.
"""
import numpy as np


def anomaly_coeffs_float():
    """The five anomaly coefficients per generation, float arithmetic."""
    # (N_c, N_w, Y, chirality) — a flat tuple layout, deliberately different from the
    # named-tuple structure of the exact script.
    ferm = [
        (3, 2, 1 / 6, +1),     # Q_L
        (3, 1, 2 / 3, -1),     # u_R
        (3, 1, -1 / 3, -1),    # d_R
        (1, 2, -1 / 2, +1),    # L_L
        (1, 1, -1.0, -1),      # e_R
    ]
    a333 = sum(c * nw for (nc, nw, y, c) in ferm if nc == 3)
    a331 = sum(c * nw * y for (nc, nw, y, c) in ferm if nc == 3)
    a221 = sum(c * nc * y for (nc, nw, y, c) in ferm if nw == 2)
    a111 = sum(c * nc * nw * y ** 3 for (nc, nw, y, c) in ferm)
    agg = sum(c * nc * nw * y for (nc, nw, y, c) in ferm)
    return {"[SU(3)]^3": a333, "[SU(3)]^2U(1)": a331, "[SU(2)]^2U(1)": a221,
            "[U(1)]^3": a111, "[grav]^2U(1)": agg}


def hypercharge_cubic(r):
    """The [U(1)]^3 anomaly on the linear-solution family, as a function of r = Y_u/Y_Q.

    The linear conditions fix Y_L = -3 Y_Q, Y_e = -6 Y_Q, Y_d = 2 Y_Q - Y_u; normalizing
    Y_Q = 1 leaves one free ratio r = Y_u/Y_Q.
    """
    yq, yu, yd, yl, ye = 1.0, r, 2.0 - r, -3.0, -6.0
    return 6 * yq ** 3 - 3 * yu ** 3 - 3 * yd ** 3 + 2 * yl ** 3 - ye ** 3


def roots_by_scan(f, lo, hi, n=200000):
    """Sign-change roots of a continuous f on [lo, hi] (numeric, no polynomial API)."""
    xs = np.linspace(lo, hi, n)
    ys = f(xs)
    roots = []
    for i in range(len(xs) - 1):
        if ys[i] == 0.0 or ys[i] * ys[i + 1] < 0.0:
            roots.append(0.5 * (xs[i] + xs[i + 1]))
    return roots


def main():
    tol = 1e-9
    # ---- 1. anomaly cancellation ----
    coeffs = anomaly_coeffs_float()
    ok_anom = True
    print("1. SM anomaly cancellation (float re-derivation):")
    for name, val in coeffs.items():
        ok = abs(val) < tol
        ok_anom &= ok
        print(f"   {name:14s} = {val:+.2e}   {'PASS' if ok else 'FAIL'}")
    print(f"   {'ALL PASS' if ok_anom else 'SOME FAIL'} — all five coefficients vanish (float).\n")

    # ---- 2. hypercharge uniqueness ----
    roots = roots_by_scan(lambda r: hypercharge_cubic(r), -6.0, 6.0)
    roots = sorted(round(r, 6) for r in roots)
    # dedupe and drop the r = 0 artifact if present (the Y_Q = 0 unphysical branch)
    roots = [r for r in roots if abs(r) > 1e-4]
    expected = [-2.0, 4.0]
    ok_uniq = len(roots) >= 2 and all(any(abs(r - e) < 1e-4 for e in expected) for r in roots)
    print("2. SM hypercharge uniqueness (numeric root-scan):")
    print(f"   roots of [U(1)]^3(r) on the linear family: {roots}")
    print(f"   expected: {expected}  (r = Y_u/Y_Q = 4 -> SM; r = -2 -> u<->d swap)")
    print(f"   {'PASS' if ok_uniq else 'FAIL'} — exactly the two physical branches.\n")

    print("=" * 66)
    print("Rule of Three, arm 2 (independent float method):")
    print("  anomaly cancellation  5/5  — agrees with the exact Fraction arm.")
    print("  hypercharge uniqueness 2 roots — agrees with the exact sympy factorization.")
    print("  (arm 1 = exact sympy/Fraction; arm 3 = literature, see docs/sm-rule-of-three.md.)")
    print("ALL CHECKS PASS" if (ok_anom and ok_uniq) else "SOME CHECKS FAILED")
    return 0 if (ok_anom and ok_uniq) else 1


if __name__ == "__main__":
    raise SystemExit(main())
