#!/usr/bin/env python3
"""The identifiability wall, measured: classes 4, 1 and 2 in epidemiology.

    python3 scripts/epidemiology_identifiability.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.epidemiology import recovery  # noqa: E402


def main() -> int:
    report = recovery.audit()
    print("PACLAND · epidemiology — the identifiability wall\n")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:22} {check['detail']}")
    r = recovery.recovery()
    wall = recovery.binning_invariance(heterogeneity=2.0)
    print(f"\nthe truth we wrote:            RR {r['truth']:.2f}")
    print(f"the crude estimate:            RR {r['crude']:.4f}  ({r['crude_relative_error']:+.0%} wrong)")
    print(f"the stratified estimate:       RR {r['adjusted']:.6f}")
    print(f"the wall (effect modification): {wall['drift']:.1%} of the estimate, from the binning alone")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print("verdict:", "IDENTIFIED (where claimed)" if report["all_pass"] else "NOT IDENTIFIED")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
