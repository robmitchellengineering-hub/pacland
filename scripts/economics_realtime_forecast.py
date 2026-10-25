#!/usr/bin/env python3
"""Reproduce the real-time Meese–Rogoff run (the committed vintage fixture).

No network: reads ``data/economics/vintages.json``, which
``scripts/fetch_economics_vintages.py`` writes from ALFRED's keyless graph endpoint.

Run:  PYTHONPATH=src python3 scripts/economics_realtime_forecast.py
Exit: 0 when the run completes and the null is present in the table, 1 otherwise.
"""
from __future__ import annotations

import sys

from pacland.economics import meese_rogoff, vintages

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<58} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    data = vintages.load()
    print(meese_rogoff.summary())
    print()
    print("-" * 62)

    # every vintage must be look-ahead free
    bad = [v.as_of for v in vintages.vintages(data) if not vintages.guard_no_lookahead(v)[0]]
    check("V1  no vintage contains an observation from its own future",
          f"{len(vintages.vintages(data))} vintages checked", not bad)

    res = meese_rogoff.evaluate(data)
    ok, msg = vintages.guard_benchmark_present(res)
    check("V2  the no-change null is present in the table", msg, ok)
    ok, msg = meese_rogoff.guard_growth_not_levels(res)
    check("V3  errors are growth-scale, not level-scale", msg, ok)

    base = res["no-change"]
    ratios_ok = all(
        res[m][h] / base[h] < 1.0 for m in ("AR(1)", "VAR(1)") for h in (1, 2, 4)
    )
    check("V4  both statistical models beat the null at every horizon",
          "ratios " + ", ".join(f"{m}:{res[m][1]/base[1]:.2f}x" for m in ("AR(1)", "VAR(1)")),
          ratios_ok)

    wins = res["VAR(1)"]["wins"]
    check("V5  paired wins favour the VAR over the null",
          ", ".join(f"h={h}: {wins[h]}/{res['VAR(1)']['n'][h]}" for h in (1, 2, 4)),
          all(wins[h] > res["VAR(1)"]["n"][h] / 2 for h in (1, 2, 4)))

    print()
    total = 5
    print(f"real-time run: {total - FAIL}/{total} checks — "
          f"{'the null is in the table and is beaten' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
