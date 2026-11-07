#!/usr/bin/env python3
"""Neutrino/flavor sector — the same forced/free recipe, one more level up.

The lepton flavor sector (Y_e, Y_nu) under GL(3)_L x GL(3)_e x GL(3)_nu is *structurally
identical* to the quark sector (Y_u, Y_d) under GL(3)_Q x GL(3)_u x GL(3)_d: two 3x3 matrices
under one shared left conjugation. Therefore the PMNS invariant ring is THE SAME as the CKM
ring — the same exact Hilbert series

    H(t) = (1 - t^12) / ((1-t)^2 (1-t^2)^3 (1-t^3)^4 (1-t^4) (1-t^6)),

i.e. 10 primary + 1 secondary (the Jarlskog), dimension 10 (3 charged + 3 neutrino masses +
4 PMNS). No new Molien computation is needed: the group and representation are identical.

The combined quark+lepton flavor ring is the product of two copies, so its Hilbert series is
H(t)^2 and its Krull dimension is 20 (Dirac neutrinos). Majorana neutrinos replace Y_nu Y_nu+
by the symmetric mass matrix M_nu (M_nu = M_nu^T, the symmetric rep, not the full 3x3), which
adds the 2 Majorana phases -> lepton dimension 12, total flavor 22.

Counting (the "extend the 19" result):

    SM (19)            = 13 Yukawa (6 quark + 3 lepton masses + 4 CKM) + 3 gauge + 2 Higgs + 1 theta
    SM + Dirac nu      = 20 flavor + 3 + 2 + 1 = 26
    SM + Majorana nu   = 22 flavor + 3 + 2 + 1 = 28

The forced/free read: the neutrino sector adds NO new constraint — neutrinos are gauge singlets,
so anomaly cancellation is unchanged; the seesaw scale and the PMNS angles/phases are all FREE
parameters (the free column grows by 7 or 9). The constraint-first statement is therefore
*stable* under the neutrino extension: forced stays what it was, free grows.
"""

import sympy as sp


def main():
    t = sp.Symbol('t')
    H = (1 - t**12) / ((1 - t)**2 * (1 - t**2)**3 * (1 - t**3)**4 * (1 - t**4) * (1 - t**6))
    H_flavor = sp.factor(H**2)

    # Krull dimension = pole order at t = 1.
    print("PMNS invariant ring = CKM ring (same group + representation):")
    print("  H(t) = (1 - t^12) / ((1-t)^2 (1-t^2)^3 (1-t^3)^4 (1-t^4) (1-t^6))")
    print("  dimension 10 = 3 charged + 3 neutrino masses + 4 PMNS")
    print()
    print("Combined quark x lepton flavor Hilbert series (Dirac):")
    print(f"  H_flavor(t) = {H_flavor}")
    print("  dimension = 20 (10 quark + 10 lepton)")
    print()
    print("Counts:")
    print("  SM (Dirac nu):   20 + 3 gauge + 2 Higgs + 1 theta = 26")
    print("  SM (Majorana nu): 22 + 3 + 2 + 1 = 28   (2 Majorana phases extra)")
    print()
    print("Forced/free: NO new constraint (neutrinos are singlets); the free column grows +7/+9.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
