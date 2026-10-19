#!/usr/bin/env python3
"""Swampland bound — does the D3 tadpole give a lower bound (N >= 1) or only an upper bound?

The floor-fan-out's swampland angle asked whether tadpole cancellation gives a strict
lower bound on the flux integer or only an upper bound. This script answers it exactly:
the tadpole N_flux = F^T J H is an integer symplectic pairing that can be zero or negative,
so tadpole cancellation imposes ONLY the upper bound N_flux <= L (the orientifold charge
must be cancelled by D3-branes). There is no lower bound N_flux >= 1 from tadpole
cancellation itself; a positive lower bound (N_flux > 0) comes only from the extra
ISD/supersymmetry assumption, not from the constraint.
"""


def tadpole(F, H, half=3):
    """N = F^T J H = sum_i (F_i H_{i+half} - F_{i+half} H_i) for the symplectic form."""
    return sum(F[i] * H[i + half] - F[i + half] * H[i] for i in range(half))


def main():
    cases = [
        ("no flux (F = 0, H = 0)", [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]),
        ("negative (F = e_3, H = e_0)", [0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 0, 0]),
        ("positive (F = e_0, H = e_3)", [1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]),
    ]
    print("The D3 tadpole N_flux = F^T J H is an integer, and it can take:")
    for name, F, H in cases:
        print(f"   {name:28s} ->  N = {tadpole(F, H):+d}")

    lo = min(tadpole(F, H) for _, F, H in cases)
    hi = max(tadpole(F, H) for _, F, H in cases)
    ok = (lo <= 0) and (hi >= 1)   # negative-or-zero exists, positive exists
    print(f"\n   range of the examples: [{lo}, {hi}]  ->  N is NOT bounded below by 1.\n")
    print("=" * 66)
    print("SWAMPLAND BOUND (the floor question):")
    print("  tadpole cancellation is N_flux + N_D3 = Q, with N_D3 >= 0, Q > 0.")
    print("  => N_flux <= Q is an UPPER bound only; N_flux can be 0 (no flux) or negative.")
    print("  => there is NO lower bound N_flux >= 1 from tadpole cancellation itself.")
    print("  => the discrete 'floor' is N = 0 (or negative), NOT N = 1; a >= 1 bound")
    print("     requires the extra ISD / supersymmetry assumption, not the constraint.")
    print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
