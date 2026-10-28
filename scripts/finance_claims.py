#!/usr/bin/env python3
"""The finance sector, claim by claim: deficit, extrapolation, verified reference, and worth.

    python3 scripts/finance_claims.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import claims as C  # noqa: E402


def main() -> int:
    summary = C.summary()
    print("PACLAND · the finance sector, claim by claim\n")
    print(f"delta = {summary['delta']}, radius = sqrt(ln(1/delta) / 2m)\n")
    for c in summary["claims"]:
        print(f"{c.worth.upper():18} {c.text}")
        print(f"  oracle {c.oracle:12} m={c.m:<2} radius {c.radius_label:8} "
              f"{'EXTRAPOLATION' if c.extrapolation else 'measured region'}")
        print(f"  verified reference: {c.reference}")
        print(f"  evidence: {c.evidence}")
        if c.hedge:
            print(f"  hedge: {c.hedge}")
        print()
    print(summary["verdict"])
    for check in C.audit()["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']}: {check['detail']}")
    print("\nThe rule: outside the measured region, do not act — whatever m is. Inside with no")
    print("constraints, do not act. Inside with a radius above 0.25, act with a hedge its size.")
    print("Inside with radius at or below 0.25, act.")
    return 0 if C.audit()["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
