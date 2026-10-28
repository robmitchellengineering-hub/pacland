#!/usr/bin/env python3
"""The Kalman filter for SW: implemented, 8x faster, and refused on a measured test.

    python3 scripts/econ_sw_filter.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import sw_filter as F  # noqa: E402


def main() -> int:
    t0 = time.time()
    solved, measured = F.solved_model(), F.measured_rows()
    space = F.one_step_space(solved, measured)
    q = F.forecast_quality()
    report = F.audit()
    print("PACLAND · economics — SW's Kalman filter\n")
    print(f"state {space['n_state']}, observables {space['n_obs']} "
          f"({', '.join(F.USED)}); wages absent by design")
    print(f"\none-step R^2 against the series mean, on data the model itself generated:")
    for name, row in q["rows"].items():
        print(f"  {name:9} R^2 {row['r2']:+.3f}   obs sd {row['obs_sd']:.3f}   "
              f"forecast error sd {row['err_sd']:.3f}")
    print(f"\nverdict: {q['verdict']}")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:38} {check['detail']}")
    print(f"\n{report['n_pass']}/{report['n']} checks pass; runtime {time.time() - t0:.1f}s")
    print("REFUSED: no out-of-sample forecast is produced from this filter, and the two SW")
    print("slots stay owed. A filter that cannot explain variation it generated itself is not")
    print("a filter that can explain the economy.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
