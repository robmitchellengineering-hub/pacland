#!/usr/bin/env python3
"""Reproduce the three-way comparison.

Run:  PYTHONPATH=src python3 scripts/economics_three_way.py
Exit: 0 when every arm ran, the null is present, and the reported finding holds.
"""
from __future__ import annotations

import sys

from pacland.economics import meese_rogoff, nk3, three_way

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(three_way.summary())
    print("-" * 62)
    r = three_way.run()

    ok_pi = all(r["sw_subsystem"]["NK3"]["pi"][h] > r["nk3"]["no-change"]["pi"][h]
                for h in (1, 2, 4))
    check("T1  the SW-calibrated subsystem loses to the null on inflation",
          " ".join(f"h={h}: {r['sw_subsystem']['NK3']['pi'][h]/r['nk3']['no-change']['pi'][h]:.2f}x"
                   for h in (1, 2, 4)), ok_pi)

    ok_gap = r["sw_subsystem"]["NK3"]["gap"][4] < r["nk3"]["no-change"]["gap"][4]
    check("T2  ...and beats it on the output gap at 4 quarters",
          f"{r['sw_subsystem']['NK3']['gap'][4]/r['nk3']['no-change']['gap'][4]:.2f}x", ok_gap)

    ok_var = all(r["var1"]["VAR(1)"][h] < r["var1"]["no-change"][h] for h in (1, 2, 4))
    check("T3  the VAR(1) beats the null at every horizon",
          " ".join(f"{r['var1']['VAR(1)'][h]/r['var1']['no-change'][h]:.2f}x" for h in (1, 2, 4)),
          ok_var)

    cal = three_way.sw_calibration()
    ok_cal = (abs(cal["phi_pi"] - 2.04) < 1e-12 and abs(cal["phi_y"] - 0.08) < 1e-12
              and abs(cal["kappa"] - 0.1777) < 1e-3)
    check("T4  the subsystem uses SW's published parameters",
          f"kappa={cal['kappa']:.4f}, phi_pi={cal['phi_pi']:.2f}, phi_y={cal['phi_y']:.2f}",
          ok_cal)

    check("T5  it is labelled as a subsystem, not as SW",
          "NOT the 20-condition SW model" in three_way.summary(),
          "NOT the 20-condition SW model" in three_way.summary())

    print()
    total = 5
    print(f"three-way: {total - FAIL}/{total} — "
          f"{'four arms, one null, and the label is honest' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
