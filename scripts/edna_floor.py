"""The one parameter still assumed: how much the contamination floor moves the answer.

The mock community gave the detection law a real test and corrected it at the edge. **It cannot test the contamination
floor**, because a mock community has no blanks: every species in it is supposed to be there, so there is no observation of
"reads arriving for something that is not there".

Rather than pretend otherwise, this quantifies **what the assumption costs**. If the floor is wrong by a factor of ten, does
the answer move by 1% or by 10x? That decides whether finding a negative-control dataset is worth doing at all.

    python3 scripts/edna_floor.py

FALSIFIER, stated before the run: if the detection limit and the resolved-species count barely move across a hundredfold range
of contamination, then the floor is not a consequential parameter, the assumption is harmless, and the search for blank data
should stop. That would be a genuinely useful negative result.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.edna import limit as L  # noqa: E402

#: Contamination rates to sweep, in reads per sample, spanning "clean" to "obviously dirty".
RATES = (0.001, 0.01, 0.1, 1.0, 10.0)
SAMPLES = (1, 10, 100)


def main() -> int:
    print("how much the contamination floor matters (10 samples unless stated)\n")
    print(f"{'contamination':>14}{'floor':>8}{'limit':>10}{'limit/sample':>14}{'species @1e6 reads':>21}")
    limits, species = [], []
    for c in RATES:
        floor = L.contamination_floor(c, 10)
        lim = L.detection_limit_reads(c, 10)
        n = L.distinguishable_species(1e6, 40.0, c)
        limits.append(lim)
        species.append(n)
        print(f"{c:>14}{floor:>8}{lim:>10.1f}{lim / 10:>14.2f}{n:>21,}")

    print("\nthe cost of being wrong about the floor:")
    ratio = limits[-1] / limits[0]
    drop = 1.0 - species[-1] / species[0]
    print(f"  a 10,000x range of contamination changes the detection limit by {ratio:.1f}x")
    print(f"  and the resolved species count by {100 * drop:.0f}%")

    print("\nthe same for sample counts (contamination 0.1):")
    print(f"{'samples':>9}{'floor':>8}{'limit/sample':>14}")
    per_sample = []
    for n in SAMPLES:
        f = L.contamination_floor(0.1, n)
        lim = L.detection_limit_reads(0.1, n)
        per_sample.append(lim / n)
        print(f"{n:>9}{f:>8}{lim / n:>14.3f}")

    consequential = ratio > 1.5 or drop > 0.2
    print(f"\nis the floor consequential? {consequential}")
    if not consequential:
        print("""
VERDICT: the floor is NOT a consequential parameter on these scales - the limit and the species count barely move - so the
assumption is harmless and the search for blank data should stop. **That is a useful negative result: it says the discipline
can proceed with an assumed floor.**""")
        return 0
    print(f"""
VERDICT: the floor IS consequential - a 10,000x range in contamination moves the limit {ratio:.1f}x and the resolved species
count by {100 * drop:.0f}%. **So the assumed floor is the weakest number in the discipline**, and a negative-control dataset is
worth finding: it is the difference between "we can see 20 species" and "we can see 40", or between a limit of 3 reads and one
of 30.

WHAT A NEGATIVE CONTROL HAS TO LOOK LIKE, since it is now the named gap:
  * field / extraction / PCR blanks from a real survey, with the reads each taxon drew in the blanks;
  * the same primer set as the sample being analysed - the floor is amplicon-specific;
  * enough blanks that the per-sample rate can be estimated, not assumed: one blank gives an upper bound, not a rate.

Until one arrives, every number this discipline produces carries the floor as a **stated assumption with its consequence
computed**, which is the next best thing to measuring it.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
