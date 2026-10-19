#!/usr/bin/env python3
"""GUT parameter tabulation — unification *shuffles* free parameters, it does not
reduce them.

The floor-fan-out's GUT-ladder angle cautioned that unification "shuffles parameters
across sectors, not a demonstrated total-count floor below 19." This script makes that
precise with a single counting convention: total = gauge + Yukawa(orbit-space dim) +
Higgs + theta. The key result is that minimal SU(5) stays at ~19 — the gauge reduction
(3 couplings -> 1) is exactly offset by the Higgs-sector growth (1 doublet -> 5_H + 24_H).

SM (baseline):
    gauge  3  (g_s, g, g')
    Yukawa 13 = quark orbit-space 10 (6 masses + 4 CKM) + lepton 3 (3 masses)
    Higgs  2  (mu^2, lambda)
    theta  1
    total 19

Minimal SU(5):
    gauge  1  (alpha_GUT; unification saves 2)
    Yukawa 13 = Y_u (10.10.5_H, symmetric) + Y_d (5bar.10.5bar_H), Y_e = Y_d^T
                -> orbit-space 13 (6 up + 3 down + 4 CKM; lepton masses = down masses)
                i.e. the b-tau relation is a RELATION, not a reduction: 13 stays 13
    Higgs ~4  (5_H + 24_H potential: quadratic + quartic each, plus 5_H-24_H coupling)
    theta  1
    total ~19

The honest conclusion: the b-tau "prediction" ties m_b to m_tau (a relation) but does
not lower the count, because the SM already counts the 3 lepton masses as 3 of its 13.
Gauge unification genuinely removes 2, but the Higgs sector grows by ~2 to break SU(5),
so the total is unchanged. A real reduction below 19 would need the Yukawa sector to
shrink (e.g. a mechanism computing Y_u, Y_d from fewer inputs) — which is the "relations,
not values" question, not a GUT question.
"""


def sm():
    return {"gauge": 3, "yukawa": 13, "higgs": 2, "theta": 1}


def minimal_su5():
    return {"gauge": 1, "yukawa": 13, "higgs": 4, "theta": 1}  # higgs count is ~4 (uncertain)


def total(d):
    return sum(d.values())


def main():
    sm_d = sm()
    su5 = minimal_su5()
    assert total(sm_d) == 19, total(sm_d)
    print("Parameter tabulation (one convention: gauge + Yukawa-orbit + Higgs + theta)\n")
    print(f"{'model':16s} {'gauge':>6s} {'Yukawa':>7s} {'Higgs':>6s} {'theta':>6s} {'total':>6s}")
    for name, d in [("SM", sm_d), ("minimal SU(5)", su5)]:
        print(f"{name:16s} {d['gauge']:6d} {d['yukawa']:7d} {d['higgs']:6d} {d['theta']:6d} "
              f"{total(d):6d}")
    print()
    print("Shuffle, not reduction:")
    print("  gauge  3 -> 1  (saves 2)  but  Higgs 2 -> ~4  (adds ~2)  =>  net ~0")
    print("  Yukawa stays 13: the b-tau relation (Y_e = Y_d^T) ties m_b to m_tau,")
    print("  but the SM already counts those 3 lepton masses — a relation, not a reduction.")
    print()
    print("=> minimal SU(5) leaves ~19 free parameters, NOT 14. A genuine drop below 19")
    print("   needs the Yukawa sector itself to shrink (compute Y_u, Y_d from fewer inputs),")
    print("   which is the 'relations, not values' question, not a GUT question.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
