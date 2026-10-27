#!/usr/bin/env python3
"""The climate invariance gate — the economics gate, on a second discipline.

Three checks, each with a seeded fault:

  baseline period  move the 1951-80 reference: offsets change, the trend rate must not
  units            Celsius to Kelvin: levels shift by 273.15, skill scores must not
  window           shift the hindcast start years: assert what is robust (the trend beats
                   persistence everywhere) and REPORT what is not (the trend-vs-emulator
                   ranking flips with the window, so it is not claimed)

    python3 scripts/climate_invariance.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.climate import invariance  # noqa: E402


def main() -> int:
    report = invariance.audit()
    print("PACLAND · climate — the invariance gate\n")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:16} {check['detail']}")
    w = invariance.window_invariance()
    print(f"\nrobust: trend beats persistence in every window = "
          f"{w['trend_beats_persistence_everywhere']}")
    print(f"NOT robust: the trend-vs-emulator ranking flips with the window "
          f"({w['emulator_wins']}/{len(w['windows'])} windows won by an emulator) — not claimed")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print("verdict:", "INVARIANT (where claimed)" if report["all_pass"] else "NOT INVARIANT")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
