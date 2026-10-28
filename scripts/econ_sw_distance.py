#!/usr/bin/env python3
"""Minimum distance on the observables: a perfect moment fit and unidentified parameters.

    python3 scripts/econ_sw_distance.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import sw_distance as D  # noqa: E402


def main() -> int:
    rec = D.recovery()
    fit = D.fit_scales()
    report = D.audit()
    print("PACLAND · economics — minimum distance on SW's observables\n")
    print("control (simulate with known scales, then recover them):")
    print(f"  truth    {[round(x, 3) for x in rec['truth']]}")
    print(f"  estimate {[round(x, 3) for x in rec['estimate']]}")
    print(f"  R^2 {rec['r2']:.3f}   worst scale error {rec['worst_relative_error']:.0%}")
    print(f"\nagainst the real vintages: {fit['verdict']}")
    print(f"  recovered scales {[round(x, 3) for x in fit['scales']]}")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:34} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass; usable = {report['usable']}")
    print("VERDICT: minimum distance fits SW's reduced form to the data perfectly AND recovers the")
    print("shock scales to no better than ~40% — the parameters are not identified at this sample")
    print("size. Like the filter, this route is closed with a measured reason rather than a number")
    print("presented as a result.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
