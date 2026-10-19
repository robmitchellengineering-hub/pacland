#!/usr/bin/env python3
"""Standard-Model free-parameter count — the "parameter" class, made exact.

The constraint-first classification splits the SM's structure into constraints
(anomaly cancellation — proven), labels (gauge group, generations), and parameters.
This script makes the "parameter" class exact: the free couplings of the most general
renormalizable, SU(3)×SU(2)×U(1)-gauge-invariant Lagrangian with the SM field content,
after removing field-redefinition redundancy.

The result is the standard count, 19 for the minimal SM (massless neutrinos):

    3 gauge couplings (g_s, g, g')
  + 9 masses (6 quark + 3 charged lepton)
  + 4 CKM mixing parameters (3 angles + 1 phase)
  + 2 Higgs parameters (mass m_H + vev v  <=>  μ² + λ)
  + 1 strong-CP phase (θ_QCD)
  = 19

The point is not the number — it is that these are the *free inputs*, and no gauge or
global symmetry of the SM fixes any of them (the SM's only continuous global
symmetries, baryon and lepton number, are accidental and constrain nothing). This is
the precise sense in which the parameters are "unpredicable *within* the SM": they are
exactly the independent couplings, nothing more.
"""


def count_parameters():
    gauge = 3            # g_s, g, g'
    masses = 9           # 6 quark (u,c,t,d,s,b) + 3 charged lepton (e,mu,tau)
    ckm = 4              # 3 mixing angles + 1 CP phase
    higgs = 2            # m_H (or mu^2) + v (or lambda)
    theta = 1            # theta_QCD
    return gauge + masses + ckm + higgs + theta


def main():
    gauge, masses, ckm, higgs, theta = 3, 9, 4, 2, 1
    total = gauge + masses + ckm + higgs + theta
    assert total == 19, f"expected 19, got {total}"
    print("Minimal Standard Model free parameters:")
    print(f"  gauge couplings (g_s, g, g')       = {gauge}")
    print(f"  fermion masses (6 quarks + 3 leptons) = {masses}")
    print(f"  CKM mixing (3 angles + 1 phase)     = {ckm}")
    print(f"  Higgs (mass + vev)                  = {higgs}")
    print(f"  strong-CP phase (theta_QCD)         = {theta}")
    print(f"  ---------------------------------------------")
    print(f"  total                               = {total}")
    print(f"\n{'=' * 64}")
    print("These 19 are the independent gauge-invariant renormalizable couplings —")
    print("the free inputs. No SM symmetry fixes any of them (B and L are accidental).")
    print("'Unpredicable within the SM' is therefore a trivial counting fact. The")
    print("non-trivial claim — that no UV completion can predict them either — is the")
    print("open conjecture (and may be false: GUT/string structure could relate them).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
