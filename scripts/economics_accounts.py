#!/usr/bin/env python3
"""Reproduce the national-accounts check.

Run:  PYTHONPATH=src python3 scripts/economics_accounts.py
Exit: 0 when the identity closes, the contributions add, and the leak is reported.
"""
from __future__ import annotations

import sys

from pacland.economics import national_accounts as N

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<58} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(N.summary())
    print("-" * 62)
    for label, guard in (
        ("A1  the expenditure identity closes", N.guard_additivity),
        ("A2  nominal contributions sum to nominal growth", N.guard_contributions_sum),
        ("A3  the nominal shares sum to one", N.guard_shares_sum_to_one),
        ("A4  the real decomposition's leak is reported", N.guard_the_leak_is_reported),
    ):
        ok, msg = guard()
        check(label, msg, ok)
    cov = N.coverage()
    check("A5  every condition is settled (proved or specification)",
          f"{cov['n_proved']} proved, {cov['n_specification']} specifications",
          cov["complete"])
    print()
    total = 5
    print(f"national accounts: {total - FAIL}/{total} — "
          f"{'the exact half closes and the leaking half says so' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
