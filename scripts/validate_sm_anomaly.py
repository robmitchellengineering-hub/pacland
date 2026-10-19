#!/usr/bin/env python3
"""Standard-Model anomaly cancellation — the gauge-sector constraint (exact).

Constraint-first, one sector up: the flux sector's only exact structure is the
tadpole (a *constraint*). The Standard Model's exact structure starts with anomaly
cancellation — the hypercharge assignments are NOT predicted, they are *forced* by
the requirement that all gauge/gravitational anomalies vanish. This script verifies,
exactly (Python Fraction, zero floating-point), that the SM fermion content cancels
all five anomaly coefficients per generation.

The five conditions (per generation, Y = hypercharge, Q = T3 + Y):

    [SU(3)]^3       = sum over quarks      chirality * N_w
    [SU(3)]^2 U(1)  = sum over quarks      chirality * N_w * Y
    [SU(2)]^2 U(1)  = sum over doublets    chirality * N_c * Y
    [U(1)]^3        = sum over fermions    chirality * N_c * N_w * Y^3
    [grav]^2 U(1)   = sum over fermions    chirality * N_c * N_w * Y

Each vanishing coefficient is the SM analog of "the tadpole is the unique exact
structure": the theory *forbids* (the anomaly), it does not *predict*. The
hypercharges (1/6, 2/3, -1/3, -1/2, -1) are the unique solution up to overall
normalization.
"""

from fractions import Fraction as F

# (name, N_c [color], N_w [weak], Y [hypercharge], chirality [+1 L / -1 R])
FERMIONS = [
    ("Q_L", 3, 2, F(1, 6), +1),   # (u,d)_L doublet, Y = +1/6
    ("u_R", 3, 1, F(2, 3), -1),   # right-handed up, Y = +2/3
    ("d_R", 3, 1, F(-1, 3), -1),  # right-handed down, Y = -1/3
    ("L_L", 1, 2, F(-1, 2), +1),  # (nu,e)_L doublet, Y = -1/2
    ("e_R", 1, 1, F(-1, 1), -1),  # right-handed electron, Y = -1
]

QUARKS = [f for f in FERMIONS if f[1] == 3]
DOUBLETS = [f for f in FERMIONS if f[2] == 2]


def A333():
    return sum(chir * N_w for (_, _, N_w, _, chir) in QUARKS)


def A331():
    return sum(chir * N_w * Y for (_, _, N_w, Y, chir) in QUARKS)


def A221():
    return sum(chir * N_c * Y for (_, N_c, _, Y, chir) in DOUBLETS)


def A111():
    return sum(chir * N_c * N_w * Y**3 for (_, N_c, N_w, Y, chir) in FERMIONS)


def Agg():
    return sum(chir * N_c * N_w * Y for (_, N_c, N_w, Y, chir) in FERMIONS)


def main():
    checks = [
        ("[SU(3)]^3", A333()),
        ("[SU(3)]^2 U(1)", A331()),
        ("[SU(2)]^2 U(1)", A221()),
        ("[U(1)]^3", A111()),
        ("[grav]^2 U(1)", Agg()),
    ]
    all_ok = True
    for name, coeff in checks:
        ok = coeff == 0
        all_ok &= ok
        print(f"{name:18s} = {coeff}   {'PASS' if ok else 'FAIL'}")
    print(f"\n{'=' * 60}")
    print(f"Standard-Model anomaly cancellation: {sum(c[1] == 0 for c in checks)}/{len(checks)} "
          f"coefficients vanish (exact rational arithmetic).")
    print("The SM's gauge structure is a CONSTRAINT (what the theory forbids),")
    print("not a prediction — the gauge-sector analog of the D3 tadpole being the")
    print("flux sector's unique exact structure.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
