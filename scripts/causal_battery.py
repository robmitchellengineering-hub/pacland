#!/usr/bin/env python3
"""The known-truth battery: score causal estimators against effects that were planted.

    python3 scripts/causal_battery.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.causal import battery as B  # noqa: E402


def main() -> int:
    res = B.run()
    board = B.scoreboard(res)
    print("PACLAND · the known-truth battery for causal estimators\n")
    print(f"{res['reps']} replications per cell, tolerance {res['tolerance']:.0%} of the planted effect\n")
    print(f"{'design':22} {'estimator':17} {'median':>8} {'truth':>6} {'recover':>8}  verdict")
    for c in res["cells"]:
        print(f"{c.dgp:22} {c.estimator:17} {c.estimate:>+8.3f} {c.truth:>6.2f} "
              f"{c.recovery_rate:>7.0%}  {'recovers' if c.recovered else 'FAILS'}")
    print(f"\n{board['verdict']}")
    sens = B.staggered_sensitivity()
    print(f"\nstaggered timing, by effect growth: {sens['detail']}")
    print(f"  -> the bias is a mechanism, not a number: {sens['pass']}")
    for check in B.audit()["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']}")
    print("\nread it as a matrix, not a verdict: each estimator wins the designs matched to it and")
    print("loses the others. A method that has never been through this battery is an act of faith.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
