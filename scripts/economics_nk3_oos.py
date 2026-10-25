#!/usr/bin/env python3
"""Reproduce the NK3 real-time out-of-sample run.

Run:  PYTHONPATH=src python3 scripts/economics_nk3_oos.py
Exit: 0 when the run completes, the null is present, and the reported finding matches
      the numbers (the model loses on inflation, wins on the gap at 4 quarters).
"""
from __future__ import annotations

import sys

from pacland.economics import nk3, nk3_oos, vintages

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    global FAIL
    print(nk3_oos.summary())
    print("-" * 62)

    ok, msg = vintages.guard_benchmark_present({m: {} for m in nk3_oos.MODELS})
    check("N1  the null is in the table", msg, ok)

    r = nk3_oos.evaluate()
    base_pi = r["no-change"]["pi"]
    loses_pi = all(r["NK3"]["pi"][h] > base_pi[h] for h in (1, 2, 4))
    check("N2  the calibrated model LOSES to the null on inflation",
          " ".join(f"h={h}: {r['NK3']['pi'][h]/base_pi[h]:.2f}x" for h in (1, 2, 4)),
          loses_pi)

    base_gap = r["no-change"]["gap"]
    wins_gap4 = r["NK3"]["gap"][4] < base_gap[4]
    check("N3  it beats the null on the output gap at 4 quarters",
          f"{r['NK3']['gap'][4]/base_gap[4]:.2f}x", wins_gap4)

    pf = nk3.policy_function()
    check("N4  the policy function is non-degenerate",
          f"a_r={pf['a_r']:.4f}, a_u={pf['a_u']:.4f}, det={pf['determinant']:.4f}",
          abs(pf["determinant"]) > 1e-6)

    sample_ok = r["_meta"]["forecasts"] >= 20
    check("N5  the sample is reported and is not empty",
          f"{r['_meta']['forecasts']} forecasts from {r['_meta']['vintages']} vintages",
          sample_ok)

    print()
    total = 5
    print(f"nk3 out of sample: {total - FAIL}/{total} — "
          f"{'the model is measured against the null and the result is reported' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
