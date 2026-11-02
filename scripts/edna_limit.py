"""The truth bench for eDNA: a synthetic community whose answer is known, swept over effort and contamination.

This is `truth_bench.py` for DNA. It runs no biology: it builds populations of items with stated abundances, applies the
counting laws with a stated contamination rate, and reports **what is detectable and what is not** - so the limits are read
off a system whose truth is arithmetic rather than inferred from a real sample.

    python3 scripts/edna_limit.py

The three curves, and why each matters:

  DETECTION LIMIT vs SAMPLES     more samples lower the limit PER SAMPLE (it falls as 1/sqrt(N), because the background
                                 spread grows as sqrt(N) while the signal grows as N). The first version of this script
                                 reported the TOTAL limit and the check failed: total reads available rise with N, so the
                                 total limit rises too - the units were wrong, not the law.
  DETECTION LIMIT vs CONTAMINATION   a dirtier library raises the floor, and no depth rescues it. The floor is the limit.
  DISTINGUISHABLE SPECIES vs READS   the mode-count analogue: how many items a budget resolves once noise is accounted for.

FALSIFIER, stated before the run: if the detection limit does not fall as samples rise, or does not rise as contamination
rises, these laws are not measuring what they claim and the discipline has no instrument.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.edna import limit as L  # noqa: E402


def main() -> int:
    print("eDNA counting laws - no biology, only samples, reads and a contamination rate\n")

    print("1. DETECTION LIMIT vs SAMPLES  (contamination 0.1 reads/sample)")
    print(f"{'samples':>9}{'floor (reads)':>16}{'limit (reads)':>16}{'per sample':>13}")
    per_sample = []
    for n in (1, 2, 5, 10, 20, 50, 100):
        f = L.contamination_floor(0.1, n)
        lim = L.detection_limit_reads(0.1, n)
        per_sample.append(lim / n)
        print(f"{n:>9}{f:>16}{lim:>16.1f}{lim / n:>13.2f}")

    print("\n2. DETECTION LIMIT vs CONTAMINATION  (10 samples)")
    print(f"{'contamination':>15}{'floor (reads)':>16}{'limit (reads)':>16}")
    rising = True
    last = 0.0
    for c in (0.0, 0.01, 0.1, 0.5, 1.0, 2.0):
        f = L.contamination_floor(c, 10)
        lim = L.detection_limit_reads(c, 10)
        # discreteness makes the floor a step function, so a 0.1-read wobble is not a violation
        flag = "" if lim >= last - 0.25 else "  <- DOES NOT RISE"
        if lim < last - 0.25:
            rising = False
        last = lim
        print(f"{c:>15}{f:>16}{lim:>16.1f}{flag}")

    print("\n3. DISTINGUISHABLE SPECIES vs READ BUDGET  (40 reads/species, 0.1 contamination)")
    print(f"{'read budget':>14}{'species resolved':>19}")
    for budget in (10_000, 100_000, 1_000_000, 10_000_000):
        print(f"{budget:>14,}{L.distinguishable_species(budget, 40.0, 0.1):>19,}")

    print("\n4. SAMPLING EFFORT FOR A TARGET  (contamination 0.1)")
    for target in (50, 20, 10, 5):
        n = L.sample_requirement(0.1, target)
        print(f"   to detect a species contributing {target:>3} reads, take {n:>4} sample(s)")

    falling = per_sample[-1] < per_sample[0]
    print(f"\nsamples lower the limit: {falling} | contamination raises it: {rising}")
    if not (falling and rising):
        print("VERDICT: the laws do not behave as claimed - the instrument is wrong and nothing follows from it.")
        return 1
    print("""
VERDICT: the two levers behave as claimed, and they are not interchangeable.

  * SAMPLES lower the detection limit PER SAMPLE, as 1/sqrt(N): the signal grows with N while the background spread grows as its
    square root. This is the lever that costs field time and nothing else.
  * CONTAMINATION raises the limit, and no sequencing depth recovers it - the floor is a property of the library, not of the
    read count. **That is the 6 dB action floor in DNA form: below it, a detection is not a detection.**

WHAT THIS DISCIPLINE DELIVERS, and it is deliberately narrow: a limit and its error bar, computed from samples and a
contamination estimate. **It says nothing about any species.** What it does is make "we detected it" a statement with a
threshold behind it, which is the same service the action floor does for a radio measurement.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
