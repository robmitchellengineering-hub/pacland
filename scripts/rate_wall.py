#!/usr/bin/env python3
"""The rate wall — where the sampler loses candidates as h12 grows.

    python3 scripts/rate_wall.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import rate_wall as W  # noqa: E402


def main() -> int:
    w = W.the_wall()
    print("The rate wall — T1's open question\n")
    print(f"  {'h12':>4} {'b3':>3} {'tries':>6} {'valid':>6} {'points':>7} {'pts/valid':>10}")
    for r in w["rows"]:
        print(f"  {r['h12']:>4} {r['b3']:>3} {r['tries']:>6} {r['valid']:>6} {r['points']:>7} "
              f"{r['points_per_valid']:>10.4f}")
    print(f"\n  {w['statement']}")
    print(f"  loss is at: {w['where_the_loss_is']}")
    print(f"  degree is not the cause: {w['degree_is_not_the_cause']}")
    print(f"\n  HYPOTHESIS: {w['hypothesis']}")
    print(f"\n  TEST THAT WOULD SETTLE IT: {w['test_that_would_settle_it']}")
    a = W.arrivals()
    print("\n  ARRIVAL EXPERIMENT (20 calls, h12=5, degree 1):")
    print(f"    counts        : {list(W.ARRIVALS_20)}")
    print(f"    points/calls  : {a['points']}/{a['calls']}  mean {a['mean']:.2f}  variance {a['variance']:.2f}")
    print(f"    var/mean      : {a['variance_over_mean']:.2f}   (1 = Poisson, >>1 = clustered)")
    print(f"    calls with >=2: {a['observed_calls_with_two_or_more']} observed, "
          f"{a['expected_calls_with_two_or_more']:.1f} expected at Poisson")
    print(f"    VERDICT       : {a['verdict']}")
    print(f"    rate per try  : {a['rate_per_try']:.5f}  (1 in {1/a['rate_per_try']:.0f})")
    print(f"    note          : {a['note']}")

    print("\nThe proposal stage is fine — 90% of tries remain valid at h12=5. What fails is driving a candidate")
    print("to DW = 0. That is a solver question, and the sampler does not currently expose the per-trial data")
    print("needed to answer it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
