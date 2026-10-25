#!/usr/bin/env python3
"""Reproduce the GDPNow real-time record.

Run:  PYTHONPATH=src python3 scripts/economics_gdpnow.py
Exit: 0 when the record is real-time, fair, and the result is reported.
"""
from __future__ import annotations

import sys

from pacland.economics import gdpnow as G

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(G.summary())
    print("-" * 62)
    ok, msg = G.guard_nowcast_predates_release()
    check("G1  every nowcast predates the vintage carrying its target", msg, ok)
    ok, msg = G.guard_benchmark_shares_the_vintage()
    check("G2  the null shares the nowcast's vintage", msg, ok)
    ok, msg = G.guard_target_is_the_first_publication()
    check("G3  targets are first publications", msg, ok)
    ok, msg = G.guard_units_are_growth()
    check("G4  both series are growth rates, not levels", msg, ok)

    r = G.evaluate()
    check("G5  the nowcast beats the null on both metrics",
          f"MAE {r['ratio']['mae']:.2f}x · RMSE {r['ratio']['rmse']:.2f}x",
          r["ratio"]["mae"] < 1 and r["ratio"]["rmse"] < 1)
    r20 = G.evaluate(exclude_2020=True)
    check("G6  and the edge survives without 2020",
          f"{r20['wins']}/{r20['n']} wins, MAE {r20['ratio']['mae']:.2f}x",
          r20["ratio"]["mae"] < 1)
    print()
    total = 6
    print(f"gdpnow: {total - FAIL}/{total} — "
          f"{'a fair real-time test with a real result' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
