#!/usr/bin/env python3
"""The invariance gate — the oracle a field has when it has no ground truth.

Four checks, each with a seeded fault, on the committed national accounts:

  units           share every nominal level by 1000 -> shares and residual unchanged
  base year       rebase the price index -> the inflation rates are untouched
  deflator        nominal components add; chained-dollar ones do not, and that asymmetry
                  is asserted rather than hoped for
  parametrisation invent a power law, then demand the estimator recover its elasticity —
                  and refuse the level-OLS reading, which does not

    python3 scripts/economics_invariance.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import invariance  # noqa: E402


def main() -> int:
    report = invariance.audit()
    print("PACLAND · economics — the invariance gate\n")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:16} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} invariance checks pass, each with its seeded fault fired")
    print("verdict:", "INVARIANT" if report["all_pass"] else "NOT INVARIANT")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
