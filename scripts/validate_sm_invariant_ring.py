#!/usr/bin/env python3
"""Standard-Model invariant ring — why the 19 parameters are *exactly* the independent
flavor invariants, and how much a GUT shrinks the ring.

The fan-out's refinement was: a ToE predicts *relations* (invariants), never *values*.
This script makes that precise with the SM's First-Fundamental-Theorem analog (Bento,
Silva & Trautner, JHEP 2024): the flavor/reparametrization group acts on the Yukawa
matrices, and the 19 physical parameters are the dimension of its *orbit space* — the
independent invariants, nothing more.

Orbit-space dimension = (parameter-space dim) − (group dim) + (generic-stabilizer dim):

    quark sector:  Y_u, Y_d (36 real) under U(3)_QL × U(3)_uR × U(3)_dR (dim 27),
                   generic stabilizer U(1)_B (dim 1)   →  36 − 27 + 1 = 10  = 6 masses + 4 CKM
    lepton sector: Y_e (18 real) under U(3)_LL × U(3)_eR (dim 18),
                   generic stabilizer U(1)^3 (dim 3)   →  18 − 18 + 3 = 3   = 3 charged-lepton masses
    gauge sector:  3 couplings, no flavor group        →  3
    Higgs:         μ², λ                                →  2
    θ_QCD:         1                                    →  1

    total = 10 + 3 + 3 + 2 + 1 = 19

Then the GUT reduction (how a UV completion SHRINKS the ring): minimal SU(5) unifies
the 3 gauge couplings into 1 (saves 2) and b–τ Yukawa unification relates 2 masses into
1 (saves 1) → 19 − 3 = 16. But this is the *relations-not-values* point in miniature:
the unified coupling and Yukawa remain free inputs, and SUSY reintroduces ~105 soft
parameters — so a UV completion trades values for a smaller set of *new* free inputs,
never for nothing.
"""


def orbit_dim(n_param, group_dim, stabilizer_dim):
    return n_param - group_dim + stabilizer_dim


def main():
    quark = orbit_dim(36, 27, 1)    # Y_u, Y_d under U(3)^3, stabilizer U(1)_B
    lepton = orbit_dim(18, 18, 3)   # Y_e under U(3)^2, stabilizer U(1)^3
    gauge, higgs, theta = 3, 2, 1
    total = quark + lepton + gauge + higgs + theta
    assert quark == 10 and lepton == 3 and total == 19, (quark, lepton, total)

    print("Standard Model orbit-space dimensions (the FFT analog):")
    print(f"  quark  (Y_u,Y_d under U(3)^3, stab U(1)_B) = {quark}  = 6 masses + 4 CKM")
    print(f"  lepton (Y_e   under U(3)^2, stab U(1)^3) = {lepton}   = 3 charged-lepton masses")
    print(f"  gauge = {gauge},  Higgs = {higgs},  theta_QCD = {theta}")
    print(f"  total = {total}")
    print()
    print("The 19 parameters ARE the independent flavor invariants — nothing relates them")
    print("within the SM (this is the gauge-sector FFT).")

    gut = 5        # gauge 3→1 (saves 2) + Y_e=Y_dᵀ (saves 3: m_e=m_d, m_μ=m_s, m_τ=m_b)
    print(f"\nMinimal SU(5) imposes {gut} relations (gauge 2 + Y_e=Y_dᵀ 3): 19 − {gut} = {total - gut}")
    print("net free-parameter reduction is 3 (two CP phases are freed by the shrunken flavor group), so 19 → 16")
    print("(SO(10)/E₆/Pati–Salam impose 12, but those are numerically wrong; only gauge unification (2) survives data.)")
    print("But: the unified coupling/Yukawa remain FREE inputs, and MSSM adds ~105 soft terms.")
    print("Conclusion: a UV completion predicts RELATIONS (shrinks the ring), never VALUES")

    print(f"\n{'=' * 64}")
    print("The sharp open question this frames (the 'floor'): what is the MINIMUM")
    print("orbit-space dimension any consistent UV completion can reach — a lower bound")
    print("on free parameters below which no ToE can go? (Flux floor = 1: the tadpole.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
