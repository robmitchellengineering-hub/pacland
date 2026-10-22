#!/usr/bin/env python3
"""Economics forecast failure — the empirical axis (axis 1), the runnable check.

Proves the check can fire both ways (H17: a check that cannot fail proves nothing):

  F1  a no-skill model does not beat the no-change benchmark -> axis-1 claim stands
      (the forecast is extrapolation, not verification).
  F2  an oracle (perfect one-step-ahead forecast) beats the benchmark -> the guard
      goes red, falsifying axis-1 for that model.
  F3  the no-change benchmark is exactly the random walk (RMSE of first differences).

The real-data confirmation of axis 1 is the field's own record: Meese–Rogoff 1983,
Rossi 2013, Gürkaynak et al. (cited in docs/economics-verification-deficit.md) — a
structural model fails to beat a random walk out of sample.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics.forecast import (  # noqa: E402
    forecast_failure,
    guard_forecast_is_extrapolation,
    rmse,
)

# A short random-walk-like series (noise around a drift).
ACTUALS = [10.0, 10.2, 9.8, 10.5, 10.3, 10.8]
# A no-skill model: the no-change forecast plus a constant +0.5 bias (worse than naive).
NO_SKILL = [10.5, 10.7, 10.3, 11.0, 10.8]
# An oracle: perfect one-step-ahead forecasts (knows the future).
ORACLE = ACTUALS[1:]


def main():
    checks = []

    r_no_skill = forecast_failure(NO_SKILL, ACTUALS)
    ok1, _ = guard_forecast_is_extrapolation(NO_SKILL, ACTUALS)
    checks.append((f"F1 no-skill model is extrapolation (model {r_no_skill['model_rmse']:.3f} "
                   f">= naive {r_no_skill['naive_rmse']:.3f})", ok1 and not r_no_skill["beat"]))

    r_oracle = forecast_failure(ORACLE, ACTUALS)
    ok2, _ = guard_forecast_is_extrapolation(ORACLE, ACTUALS)
    checks.append((f"F2 oracle falsifies axis-1 (model {r_oracle['model_rmse']:.3f} "
                   f"< naive {r_oracle['naive_rmse']:.3f})", (not ok2) and r_oracle["beat"]))

    diffs = [ACTUALS[t] - ACTUALS[t - 1] for t in range(1, len(ACTUALS))]
    checks.append(("F3 naive benchmark == random walk", r_no_skill["naive_rmse"] == rmse(diffs)))

    all_ok = True
    for name, ok in checks:
        all_ok &= ok
        print(f"{name:62s} {'PASS' if ok else 'FAIL'}")

    print()
    print("=" * 68)
    print(f"Economics forecast failure: {sum(1 for _, ok in checks if ok)}/{len(checks)} pass.")
    print("Axis 1 (empirical): a forecast that cannot beat the no-change benchmark is")
    print("extrapolation, not verification (Meese-Rogoff 1983; Rossi 2013).")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
