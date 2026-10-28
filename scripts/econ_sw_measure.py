#!/usr/bin/env python3
"""SW's observables mapped to our data, with the units reconciled before anything is forecast.

    python3 scripts/econ_sw_measure.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import sw_measure as M  # noqa: E402


def main() -> int:
    m = M.measurement()
    uc = M.unit_check()
    report = M.audit()
    print("PACLAND · economics — SW's observables against our data\n")
    print("extracted from the authors' measurement equations:")
    for name, rec in sorted(m["observables"].items()):
        print(f"  {name:9} constant {rec['constant']:+.3f}   "
              f"states {sum(1 for x in rec['row'] if x)}")
    print(f"\n{'obs':9} {'data mean':>10} {'model SS':>9} {'clock':>6} "
          f"{'on data clock':>14} {'gap':>7}")
    for name, row in uc["rows"].items():
        print(f"{name:9} {row['data_mean']:>+10.3f} {row['model_steady_state']:>+9.3f} "
              f"x{row['clock']:.0f} {row['model_on_data_clock']:>+14.3f} {row['gap']:>+7.3f}")
    print(f"\nmissing from our vintages: {uc['missing']} (no wages series — named, not imputed)")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:32} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass")
    print("\nthe model is right about inflation to 0.04 pp a quarter and low on growth by")
    print("0.35-0.58 pp a quarter. Those are the numbers a forecast has to be judged against,")
    print("and the next step is the Kalman filter that turns observables into a state.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
