#!/usr/bin/env python3
"""GUT parameter ladder — unification *shuffles* free parameters, it does not reduce them.

The floor-fan-out's GUT-ladder angle cautioned that unification "shuffles parameters
across sectors, not a demonstrated total-count floor below 19." This script makes that
precise with a single counting convention: total = gauge + Yukawa(orbit-space dim) +
Higgs + theta. The key result: every GUT on the ladder stays at ~19 — the gauge reduction
(3 couplings -> 1) is offset by the Higgs-sector growth (the extra reps needed to break
the GUT back to the SM), and the Yukawa orbit-space stays 13 (unification *relations* are
relations, not reductions).

CONVENTION (same for all rows):
    gauge   = number of independent gauge couplings
    Yukawa  = orbit-space dimension of the flavor sector = 13 (6 masses + 4 CKM + 3 lepton)
              — the unification relations (b-tau, SO(10)/E6 Yukawa unification) RELATE the
              masses but do not lower the orbit-space count: the SM already counts each mass.
    Higgs   = real parameters in the minimal symmetry-breaking Higgs potential (ESTIMATE —
              the exact count is chain-dependent; the estimate is the point, not the number)
    theta   = the strong-CP phase (1)

ROBUST conclusion (the exact numbers are model-dependent; the pattern is not): gauge
unification saves at most 2, the Higgs sector grows ~2-4, the Yukawa stays 13 — so no GUT
drops below ~17, and none reaches the naive "14". Unification shuffles, it does not reduce.
"""


def sm():
    return {"gauge": 3, "yukawa": 13, "higgs": 2, "theta": 1}


def minimal_su5():
    # 5_H + 24_H (complex + real adjoint) to break SU(5) -> SM.
    return {"gauge": 1, "yukawa": 13, "higgs": 4, "theta": 1}


def so10():
    # 10_H + 126_H (two complex irreps) to break SO(10) -> SM.
    return {"gauge": 1, "yukawa": 13, "higgs": 5, "theta": 1}


def e6():
    # 27_H + 27bar_H + 78_H (two complex + a real adjoint) to break E6 -> SM.
    return {"gauge": 1, "yukawa": 13, "higgs": 6, "theta": 1}


def pati_salam():
    # SU(4) x SU(2)_L x SU(2)_R with L<->R symmetry: color unified (g_4), weak doubled.
    # Gauge 3 -> 2 (saves 1); Higgs = bidoublet + SU(4) sextets.
    return {"gauge": 2, "yukawa": 13, "higgs": 5, "theta": 1}


def trinification():
    # SU(3)_C x SU(3)_L x SU(3)_R with the Z_3 permutation symmetry: gauge 3 -> 1.
    return {"gauge": 1, "yukawa": 13, "higgs": 5, "theta": 1}


def total(d):
    return sum(d.values())


def main():
    models = [
        ("SM", sm()),
        ("minimal SU(5)", minimal_su5()),
        ("SO(10)", so10()),
        ("E6", e6()),
        ("Pati-Salam", pati_salam()),
        ("trinification", trinification()),
    ]
    print("Parameter ladder (one convention: gauge + Yukawa-orbit + Higgs + theta)\n")
    print(f"{'model':16s} {'gauge':>6s} {'Yukawa':>7s} {'Higgs':>6s} {'theta':>6s} {'total':>6s}")
    for name, d in models:
        print(f"{name:16s} {d['gauge']:6d} {d['yukawa']:7d} {d['higgs']:6d} "
              f"{d['theta']:6d} {total(d):6d}")
    print()
    print("Shuffle, not reduction:")
    print("  gauge: 3 -> 1 (SU(5)/SO(10)/E6/trinification save 2; Pati-Salam saves 1).")
    print("  Yukawa: stays 13 everywhere — b-tau / SO(10) / E6 relations tie masses")
    print("          but do NOT lower the orbit-space count (the SM already counts them).")
    print("  Higgs: grows 2 -> ~4-6 to break the GUT back to the SM.")
    print()
    print("=> every GUT on the ladder stays ~19 (no row below 17; none at the naive 14).")
    print("   A genuine drop below 19 needs the Yukawa sector itself to shrink (compute")
    print("   Y_u, Y_d from fewer inputs), which is the 'relations, not values' question,")
    print("   not a GUT question.")
    # assert the robust pattern (not the exact Higgs estimates)
    for name, d in models:
        assert total(d) >= 17, (name, total(d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
