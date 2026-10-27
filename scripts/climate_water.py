#!/usr/bin/env python3
"""Water — the fifth conservation invariant, with free data (no key, no netCDF).

    python3 scripts/climate_water.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.climate import water  # noqa: E402


def main() -> int:
    data = water.load()
    r = water.balance()
    print("PACLAND · climate — the water budget\n")
    print(f"{'month':9} {'P (GPCP)':>10} {'E (NCEP)':>10} {'P/E':>7}")
    for month, v in sorted(data["samples"].items()):
        print(f"{month:9} {v['precip_mm_day']:>10.3f} {v['evap_mm_day']:>10.3f} "
              f"{v['precip_mm_day'] / v['evap_mm_day']:>7.3f}")
    print(f"\nglobal means: P {r['mean_precip_mm_day']:.3f} mm/day, "
          f"E {r['mean_evap_mm_day']:.3f} mm/day")
    print(f"worst imbalance {r['worst_imbalance']:.1%} (tolerance {water.TOLERANCE:.0%})")
    report = water.audit()
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:10} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print("verdict:", r["verdict"])
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
