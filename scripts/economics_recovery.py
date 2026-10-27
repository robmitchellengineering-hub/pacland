#!/usr/bin/env python3
"""Class-4 oracle: can each of our estimators recover a truth we invented?

Five subjects, five seeded faults:

  VAR(1)          recover a known transition matrix from noiseless data
  policy rule     recover a known Taylor rule
  attenuation     measurement error in the regressor: the bias does NOT shrink with n
  scorer          MAE and the null ratio must be 0 and 1.0 on a perfect forecast
  sampling law    how fast the error falls, and the n a 1% estimate needs

    python3 scripts/economics_recovery.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import recovery  # noqa: E402


def main() -> int:
    report = recovery.audit()
    print("PACLAND · economics — synthetic recovery (the class-4 oracle)\n")
    for check in report["checks"]:
        print(f"{'PASS' if check['pass'] else 'FAIL'}  {check['check']:14} {check['detail']}")
    law = recovery.sampling_law()
    att = recovery.attenuation_demo()
    print(f"\nhow much data: the VAR error falls as n^{law['exponent']:+.2f}, so a 1% "
          f"estimate needs n ~ {law['n_for_1pct']:,}")
    print(f"and it does not always help: with measurement error the estimate stays near "
          f"{att['mean_estimate']:.2f} of a true {att['truth']:.0f}, at every n")
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print("verdict:", "RECOVERABLE (where claimed)" if report["all_pass"] else "NOT RECOVERABLE")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
