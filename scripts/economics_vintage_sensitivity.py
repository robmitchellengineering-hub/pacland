#!/usr/bin/env python3
"""Is our forecasting finding about forecasting, or about one archive's revisions?

The class-5 gap is real and open: the vintages come from ONE archive. What can be tested with
one archive is nearly as useful — hold the forecast fixed and change what counts as the truth:

  latest   the newest vintage (what the data says now)
  next     the vintage published immediately after the forecast (the FIRST revision)

    python3 scripts/economics_vintage_sensitivity.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import vintage_sensitivity as vs  # noqa: E402


def main() -> int:
    s = vs.stability()
    print("PACLAND · economics — vintage sensitivity\n")
    print(f"{'model':8} {'h':>2}  {'ratio (latest)':>14}  {'ratio (next)':>12}  stable")
    for model, per_h in s["verdict"].items():
        for h, v in per_h.items():
            print(f"{model:8} {h:>2}  {v['latest']:>14.2f}  {v['next']:>12.2f}  "
                  f"{'yes' if v['beats_null_both'] else 'NO'}")
    print(f"\nforecasts scored: {s['forecasts']}")
    print(f"worst ratio shift across regimes: {s['worst_ratio_shift']:.3f}")
    print("verdict:", "ROBUST to the revision regime" if s["pass"] else "REGIME-DEPENDENT")
    print("\nNot class 5: one archive cannot cross-check itself. This is the same claim under a")
    print("different description of the target — and the gap stays on the record as open.")
    return 0 if s["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
