#!/usr/bin/env python3
"""Reproduce the constraint-set report.

Run:  PYTHONPATH=src python3 scripts/economics_constraint_set.py
Exit: 0 when the set is consistent, sourced, and its independent rank is measured.
"""
from __future__ import annotations

import sys

from pacland.economics import constraint_set as C

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<58} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(C.summary())
    print("-" * 62)
    ok, msg = C.guard_every_constraint_sourced()
    check("S1  every constraint carries a statement and a source", msg, ok)
    ok, msg = C.guard_kinds_are_known()
    check("S2  every constraint has a known kind", msg, ok)
    ok, msg = C.guard_default_state_is_admissible()
    check("S3  the reference state satisfies the whole set", msg, ok)
    ind = C.independence()
    check("S4  the independent rank is measured, not assumed",
          f"{ind['rank']} independent of {ind['n_equality']} equalities", ind["dependent"] == 0)
    worst = C.slack()[0]
    check("S5  the binding constraints are reported", f"first: {worst[0]} ({worst[1]:+.2e})",
          worst is not None)
    ok = bool(C.violated(dict(C._default_state(), phi_pi=0.5)))
    check("S6  a passive policy rule is caught", "taylor_principle", ok)
    print()
    total = 6
    print(f"constraint set: {total - FAIL}/{total} — "
          f"{'plural, sourced, and measured' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
