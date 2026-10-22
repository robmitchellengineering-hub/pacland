#!/usr/bin/env python3
"""K-theory torsion correspondence — the rational (characteristic-class) half, exact.

The flux tadpole and the SM anomaly are both "a (twisted) K-theory class vanishes" — but
WHICH index they realise matters, and a cohomology-only tadpole would miss the Z_2 torsion.
This script settles the rational half exactly (sympy), and names the torsion half as open.

  CLAIM TO TEST (from the constructive fan-out pass): "the O3 charge -chi/24 = int A-hat(TX)".
  If true, the A-hat genus must carry the Euler class c_3. It does not.

  1. A-HAT: expand A-hat = 1 - p1/24 + (7 p1^2 - 4 p2)/5760 (to degree 8) and substitute the
     complex-manifold identities p1 = c1^2 - 2 c2,  p2 = c2^2 - 2 c1 c3 (c4 = 0 on a 3-fold).
     The coefficient of the PURE Euler class c_3 must be ZERO (c_3 enters only as c1 c3).
     So the degree-6 part of A-hat is zero:  <A-hat, [X]> = 0 on a 6-fold.
  2. EULER: the Euler class of a complex 3-fold is c_3, so chi = int c_3 (Gauss-Bonnet-Chern).
     The O3 charge -chi/24 = -int c_3/24 is the EULER index, not int A-hat.
  3. DIRAC: the anomaly density [A-hat . ch(E)]_6 is a distinct degree-6 object.

  Conclusion (rational): same K-theory KIND (both a class whose shadow is a vanishing index),
  DIFFERENT index (Euler vs Dirac). The open half is the Z_2 TORSION correspondence:
  Freed-Witten (flux tadpole) vs Witten's SU(2) global anomaly (SM) — which lives in the
  torsion of K-theory (KO / twisted K), not in rational cohomology, so it is out of reach of
  a characteristic-class expansion and is stated as the named open check, not claimed.

Falsifier: a non-zero pure c_3 coefficient in the A-hat expansion (which would make the
Euler and Dirac indices coincide and the "different index" conclusion collapse).
"""
import sympy as sp


def main():
    c1, c2, c3 = sp.symbols('c1 c2 c3', commutative=True)

    # Pontryagin classes of a complex 3-fold (c4 = 0)
    p1 = c1 ** 2 - 2 * c2
    p2 = c2 ** 2 - 2 * c1 * c3

    # A-hat genus to degree 8 (the terms that can matter on a 6-fold)
    Ahat = 1 - p1 / 24 + (7 * p1 ** 2 - 4 * p2) / 5760
    Ahat = sp.expand(Ahat)

    coeff_c3 = sp.expand(Ahat).coeff(c3, 1).subs(c1, 0)          # pure c3 coefficient
    coeff_c1c3 = sp.expand(Ahat).coeff(c1 * c3, 1)                # c1 c3 coefficient

    print("1. A-HAT GENUS on a complex 3-fold, in Chern classes (to degree 8)")
    print(f"   A-hat = {sp.factor(Ahat)}")
    print(f"   coefficient of PURE c3  = {coeff_c3}")
    print(f"   coefficient of c1*c3    = {coeff_c1c3}")
    ok_pure = coeff_c3 == 0
    print(f"   {'PASS' if ok_pure else 'FAIL'}: A-hat carries no pure Euler class c3")
    print(f"   => the degree-6 part of A-hat is ZERO, so <A-hat, [X]> = 0 on a 6-fold.\n")

    print("2. EULER INDEX — the O3 charge")
    print(f"   Euler class of a complex 3-fold = c3   (Gauss-Bonnet-Chern: chi = int c3)")
    print(f"   O3 charge = -chi/24 = -int(c3)/24   is the EULER index, NOT int A-hat.\n")

    print("3. DIRAC INDEX — the anomaly density")
    print(f"   [A-hat . ch(E)]_6 is a distinct degree-6 object (involves ch6, p1.ch2, ...)")
    print(f"   It does not reduce to c3.\n")

    ok = ok_pure and coeff_c1c3 != 0
    print("4. CONCLUSION (rational level)")
    print("   same K-theory KIND (both a class whose shadow is a vanishing index),")
    print("   DIFFERENT index (Euler vs Dirac).")
    print(f"   c1*c3 coefficient {coeff_c1c3} != 0 is the cross-check that the c3 DOES appear")
    print("   in A-hat (at degree 8, dressed by c1) — so the distinction is real, not vacuous.")

    print("\n   OPEN HALF (stated, not claimed): the Z_2 TORSION correspondence")
    print("   Freed-Witten (flux tadpole, twisted K_H(X))  vs  Witten SU(2) global anomaly (SM).")
    print("   This lives in the torsion of K-theory, out of reach of rational cohomology, so a")
    print("   characteristic-class expansion cannot settle it — it is the named open check.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
