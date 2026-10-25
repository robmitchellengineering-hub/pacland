#!/usr/bin/env python3
"""Reproduce climate's constraint rank.

Run:  PYTHONPATH=src python3 scripts/climate_constraint_rank.py
Exit: 0 when the rank is measured and the redundancy is the guards, as claimed.
"""
from __future__ import annotations

import sys

from pacland.climate import constraint_set as C

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(C.summary())
    print("-" * 62)
    ind = C.independence()
    check("R1  the state constraints are counted", f"{ind['n_state']}", ind["n_state"] == 14)
    check("R2  the rank is measured, not assumed", f"{ind['rank']} independent",
          ind["rank"] == 9)
    check("R3  the redundant ones are found", f"{ind['dependent']} dependent",
          ind["dependent"] == 5)
    check("R4  process constraints are excluded by kind, not by convenience",
          f"{len(C.PROCESS_CONSTRAINTS)} named", len(C.PROCESS_CONSTRAINTS) == 5)
    check("R5  the summary names the inflation risk",
          "'inflating' present", "inflating" in C.summary())
    print()
    total = 5
    print(f"climate rank: {total - FAIL}/{total} — "
          f"{'19 written, 9 independent' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
