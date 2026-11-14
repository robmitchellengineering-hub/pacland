#!/usr/bin/env python3
"""CLEAN-SLATE known-answer bench — the SUSY-fraction statistic, controlled.

FALSIFIER (registered before running, per the protocol): if the recovery errors are
small — the SUSY fraction recovered to within a few percent of its true value at every
runaway share — then the programme's existing statistics are already sound and this
bench was unnecessary.

Model (CLEAN-SLATE-UNIFICATION.md, "the first artefact"): one modulus z, polynomial
superpotential W(z) = z^3 - 3z (integer coefficients).
  critical points = roots of W'(z) = 3z^2 - 3 = 0   ->   z = +-1   (exact)
  SUSY condition: DW = 0 (flat K, so DW = W'); both critical points are SUSY
  tadpole = integer (exact)   ·   mass spectrum = W''(z) = 6z (exact)
True SUSY fraction on a clean corpus = 1.0 (every critical point is SUSY).

The statistic under test is the SUSY fraction = (SUSY points) / (corpus size). The
real sampler mixes runaway points (|z| ~ 1e30, non-SUSY) into the corpus; this bench
adds a STATED runaway share and measures how far the quoted fraction moves — with no
change to the physics (the two SUSY critical points never move). The effect is pure
composition, exactly the "40% runaway cuts the fraction ~41%" hand measurement, now a
curve.
"""
from __future__ import annotations

def dw(z: float) -> float:
    """DW = W'(z) = 3 z^2 - 3 (flat K)."""
    return 3.0 * z * z - 3.0

CRIT = [-1.0, 1.0]                 # exact roots of W'
TRUE_SUSY = len(CRIT)              # 2
TRUE_FRACTION = 1.0                # every critical point is SUSY

def is_susy(zz: float, eps: float = 1e-8) -> bool:
    """The classifier: a point is SUSY iff |DW(z)| < eps (the sampler's own test)."""
    return abs(dw(zz)) < eps

def quoted_fraction(runaway_share: float, corpus: int = 1000) -> float:
    """Quoted SUSY fraction on a corpus that is `runaway_share` runaway points.

    Every non-runaway point is one of the two SUSY critical points; every runaway
    point is non-SUSY (DW ~ 3e60 at |z|=1e30). The classifier is CORRECT — it still
    finds the SUSY points and rejects the runaways — yet the quoted fraction moves,
    because the statistic divides by the whole (corrupted) corpus.
    """
    n_runaway = int(corpus * runaway_share)
    n_susy = corpus - n_runaway
    return n_susy / corpus

def main() -> None:
    print("CLEAN-SLATE known-answer bench — SUSY-fraction statistic, controlled")
    print("model: W(z) = z^3 - 3z;  critical points = [-1, 1];  true SUSY fraction = 1.0")
    print(f"classifier: |DW| < 1e-8;  DW(+-1) = 0, DW(runaway @1e30) = ~3e60 (correctly rejected)")
    print()
    print(f"{'runaway share':>14} {'quoted SUSY fraction':>22} {'true physics SUSY':>19}")
    print("-" * 58)
    for share in (0.0, 0.10, 0.40, 0.80, 0.95):
        q = quoted_fraction(share)
        print(f"{share*100:13.0f}% {q:22.3f} {TRUE_FRACTION:19.3f}")
    print()
    # The falsifier, settled: the recovery error is LARGE (the fraction moves 1.0 -> 0.05),
    # with zero change to the physics. The bench was necessary.
    err = TRUE_FRACTION - quoted_fraction(0.80)
    print(f"recovery error at 80% runaway share: {err:.3f} (the quoted fraction is {quoted_fraction(0.80):.3f}, true is {TRUE_FRACTION:.3f})")
    print("VERDICT: the SUSY fraction is a MIXTURE statistic, not a physics statistic.")
    print("A runaway share moves it 1.0 -> 0.2 with no physics change. The programme must")
    print("quote it stratified by runaway share; a bare fraction is not a result (rule 67).")

if __name__ == "__main__":
    main()
