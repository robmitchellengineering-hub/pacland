#!/usr/bin/env python3
"""Standard-Model hypercharge uniqueness — the gauge-sector analog of Mitchell's Uniqueness.

Mitchell's Uniqueness Theorem: the D3 tadpole FᵀJH is the UNIQUE bilinear symplectic
invariant of the flux — the constraint is the only exact structure. This script proves
the gauge-sector analog: given the SM's matter content (gauge reps + chirality), the
anomaly-cancellation conditions determine the hypercharge assignment uniquely, up to
overall normalization and the u↔d flavor swap — *among solutions with Y_Q ≠ 0* (the
correct electric-charge assignment). There is a third, unphysical branch Y_Q = 0,
giving (0, t, −t, 0, 0); it is anomaly-free but exotic, so the uniqueness claim is
scoped to Y_Q ≠ 0.

The argument (exact, sympy):
  1. The three LINEAR conditions — [grav]²U(1), [SU(2)]²U(1), [SU(3)]²U(1) — solve to
     Y_L = −3Y_Q,  Y_e = −6Y_Q,  Y_d = 2Y_Q − Y_u,  leaving a 2-dimensional family.
  2. The cubic [U(1)]³ restricted to that family factors as
     18·Y_Q·(8Y_Q² + 2Y_Q·Y_u − Y_u²) = −18·Y_Q·(Y_u − 4Y_Q)(Y_u + 2Y_Q).
     The factor Y_Q gives the unphysical branch Y_Q = 0 (excluded); the other two factors
     give the physical solutions.
  3. Hence Y_u = 4Y_Q or Y_u = −2Y_Q — two 1-dimensional families, the SM assignment
     and its u↔d swap:
        SM:      (Y_Q, 4Y_Q, −2Y_Q, −3Y_Q, −6Y_Q)   =  (1/6, 2/3, −1/3, −1/2, −1)
        swapped: (Y_Q, −2Y_Q, 4Y_Q, −3Y_Q, −6Y_Q)

So the hypercharges are FORCED by anomaly cancellation (the gauge-sector constraint),
not predicted — the same "the only exact structure is the constraint" statement that
symplectic geometry forces in the flux sector.
"""

import sympy as sp


def main():
    YQ, Yu, Yd, YL, Ye = sp.symbols("Y_Q Y_u Y_d Y_L Y_e")

    # ---- anomaly conditions (chirality-signed, per generation) ----
    grav = 6 * YQ - 3 * Yu - 3 * Yd + 2 * YL - Ye          # [grav]^2 U(1)
    su2 = 3 * YQ + YL                                      # [SU(2)]^2 U(1)
    su3 = 2 * YQ - Yu - Yd                                 # [SU(3)]^2 U(1)
    cubic = 6 * YQ**3 - 3 * Yu**3 - 3 * Yd**3 + 2 * YL**3 - Ye**3   # [U(1)]^3

    # ---- Step 1: the linear equations leave a 2-dim family ----
    lin_sol = sp.solve([grav, su2, su3], [YL, Ye, Yd], dict=True)[0]
    assert sp.simplify(YL - (-3 * YQ)).subs(lin_sol) == 0
    assert sp.simplify(Ye - (-6 * YQ)).subs(lin_sol) == 0
    assert sp.simplify(Yd - (2 * YQ - Yu)).subs(lin_sol) == 0
    print("Step 1: linear conditions ->  Y_L = -3 Y_Q,  Y_e = -6 Y_Q,  Y_d = 2 Y_Q - Y_u")
    print("         (a 2-dimensional family parametrized by Y_Q, Y_u)  -> PASS")

    # ---- Step 2: the cubic restricted to the family factors ----
    cubic_red = sp.expand(cubic.subs(lin_sol))
    fac = sp.factor(cubic_red)
    # expected: -18 Y_Q (Y_u - 4 Y_Q)(Y_u + 2 Y_Q)
    expected = -18 * YQ * (Yu - 4 * YQ) * (Yu + 2 * YQ)
    assert sp.expand(fac - expected) == 0, f"unexpected factorization: {fac}"
    print(f"Step 2: [U(1)]^3 reduced = {fac}  -> PASS")

    # ---- Step 3: the two 1-dim families ----
    # branch 1: Y_u = 4 Y_Q  ->  Y = (1/6, 2/3, -1/3, -1/2, -1) at Y_Q = 1/6
    sm_assign = {YQ: sp.Rational(1, 6), Yu: 4 * sp.Rational(1, 6),
                 Yd: -2 * sp.Rational(1, 6), YL: -3 * sp.Rational(1, 6),
                 Ye: -6 * sp.Rational(1, 6)}
    assert all(sp.simplify(eq.subs(sm_assign)) == 0 for eq in [grav, su2, su3, cubic])
    print("Step 3a: Y_u = 4 Y_Q branch  ->  (1/6, 2/3, -1/3, -1/2, -1)  = the SM  -> PASS")
    # branch 2: Y_u = -2 Y_Q  (u <-> d swap)
    swap_assign = {YQ: sp.Rational(1, 6), Yu: -2 * sp.Rational(1, 6),
                   Yd: 4 * sp.Rational(1, 6), YL: -3 * sp.Rational(1, 6),
                   Ye: -6 * sp.Rational(1, 6)}
    assert all(sp.simplify(eq.subs(swap_assign)) == 0 for eq in [grav, su2, su3, cubic])
    print("Step 3b: Y_u = -2 Y_Q branch  ->  the u<->d swap, also a solution  -> PASS")

    print(f"\n{'=' * 64}")
    print("SM hypercharge uniqueness: the anomaly conditions force the hypercharges")
    print("uniquely up to overall normalization and the u<->d flavor swap. The gauge")
    print("constraint is UNIQUE — the gauge-sector analog of Mitchell's Uniqueness.")
    print("4/4 symbolic checks PASS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
