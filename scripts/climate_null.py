#!/usr/bin/env python3
"""Reproduce climate's no-change null and the hindcast against it.

Run:  PYTHONPATH=src python3 scripts/climate_null.py
Exit: 0 when the hindcast is real-time-safe and the table is produced.
"""
from __future__ import annotations

import sys

from pacland.climate import baseline

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(baseline.summary())
    print("-" * 62)
    data = baseline.load()
    for y0, h in ((1980, 20), (2000, 20), (2010, 10)):
        ok, msg = baseline.guard_no_lookahead(data, y0, h)
        check(f"N1  no look-ahead at start {y0}", msg, ok)
    ok, msg = baseline.guard_truth_is_outside_the_window(data, 2000, 20)
    check("N2  the target lies outside the forecast window", msg, ok)
    ok, msg = baseline.guard_units(data)
    check("N3  units are degrees C", msg, ok)

    r = baseline.evaluate()
    trend = r["methods"]["trend"]
    emulators = [m for m in r["methods"] if m.startswith("emulator:")]
    beat = [m for m in emulators if r["methods"][m]["mae"] < trend["mae"]]
    check("N4  the trend null is the benchmark every method must beat",
          f"trend MAE {trend['mae']:.3f} deg C over {r['n']} hindcasts", trend["mae"] > 0)
    check("N5  no emulator beats the trend null on this sample",
          f"beat it: {beat or 'none'}", not beat)
    check("N6  but they do beat persistence",
          f"persistence MAE {r['methods']['persistence']['mae']:.3f} vs "
          f"{min(r['methods'][m]['mae'] for m in emulators):.3f}",
          all(r["methods"][m]["mae"] < r["methods"]["persistence"]["mae"] for m in emulators))
    print()
    total = 6
    print(f"climate null: {total - FAIL}/{total} — "
          f"{'the null exists, and it is hard to beat' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
