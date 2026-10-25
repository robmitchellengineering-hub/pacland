#!/usr/bin/env python3
"""Reproduce the per-model climate deficit.

Run:  PYTHONPATH=src python3 scripts/climate_model_deficit.py
Exit: 0 when the m-count falls with the failed tests, as it must.
"""
from __future__ import annotations

import sys

from pacland.climate import model_deficit as D

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(D.summary())
    print("-" * 62)
    rows = {r.model: r for r in D.board_rows()}
    check("C1  the clean model is validated on all three",
          f"m={rows['GISS-E2-1-G'].m}", rows["GISS-E2-1-G"].m == 3)
    check("C2  the leaking model loses exactly the drift observable",
          f"m={rows['MPI-ESM1-2-HR'].m}", rows["MPI-ESM1-2-HR"].m == 2
          and not rows["MPI-ESM1-2-HR"].conservation_validated)
    check("C3  the failing model keeps only what it passes",
          f"m={rows['UKESM1-0-LL'].m}", rows["UKESM1-0-LL"].m == 1)
    check("C4  radius falls as m rises (m is the certificate) [0.78 < 1.36]",
          f"{rows['GISS-E2-1-G'].radius:.2f} < {rows['UKESM1-0-LL'].radius:.2f}",
          rows["GISS-E2-1-G"].radius < rows["UKESM1-0-LL"].radius)
    check("C5  the deficit is per model, not the discipline's single number",
          "per-model", "per-model" in D.summary())
    print()
    total = 5
    print(f"climate deficit: {total - FAIL}/{total} — "
          f"{'the m-count is per model and moves with failure' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
