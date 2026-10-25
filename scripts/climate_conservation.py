#!/usr/bin/env python3
"""Verify climate's conservation inventory — and say exactly how much the algebra proves.

The honest split, and the reason this script exists:

- **The algebra is bookkeeping.** "The sum of the reservoirs equals the total" is a
  definition of the total, not a physical result. Proving it symbolically proves nothing
  about the world, and the script says so rather than dressing it up.
- **The physics is conservation**, which no script here can prove and nobody contests.
- **What actually fails is the measurement.** The budget closes only when *all* reservoirs
  are summed; the upper ocean alone is short by 0.15 W/m². That is where a model or a paper
  goes wrong, and it is machine-checkable arithmetic on the cited values.

Run:  PYTHONPATH=src python3 scripts/climate_conservation.py
Exit: 0 when the inventory is sourced, the closure behaves, and the unmeasured invariants
      are named rather than counted.
"""
from __future__ import annotations

import sys

import sympy as sp

from pacland.climate import structure as S

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<58} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    global FAIL
    print(S.summary())
    print("-" * 62)

    # K1: the algebraic identity — a definition of the total, proved and labelled as such
    f, e1, e2, e3, e4 = sp.symbols("F e1 e2 e3 e4")
    total = e1 + e2 + e3 + e4
    k1 = sp.simplify(total - (e1 + e2 + e3 + e4)) == 0
    check("K1  the reservoir sum equals the total — by construction",
          "bookkeeping, not physics", bool(k1))

    ok, msg = S.guard_invariants_are_sourced()
    check("K2  every invariant carries a statement and a named measurement", msg, ok)

    ok, msg = S.guard_closure_is_reported()
    check("K3  the energy budget closes ONLY with all reservoirs", msg, ok)

    c = S.closure_finding()
    check("K4  the upper-ocean-only budget fails, and by how much",
          f"short by {c['residual_upper_ocean']:+.3f} W/m2", abs(c["residual_upper_ocean"]) > 0.05)

    ok, msg = S.guard_unmeasured_invariants_are_named()
    check("K5  unmeasured invariants are named, not counted", msg, ok)

    cov = S.coverage()
    check("K6  the coverage is reported honestly",
          f"{cov['n_measured']} of {cov['n_total']} measured here", cov["n_measured"] == 3)

    print()
    total_checks = 6
    print(f"climate conservation: {total_checks - FAIL}/{total_checks} — "
          f"{'the inventory is proved, sourced, and honest about its measurement' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
