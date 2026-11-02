"""How well does the phone measure a ceiling? Rob's house answers it, because every ceiling is the same height.

Three rooms measured floor-to-ceiling in separate ARCore sessions:

    2.65 m   2.47 m   2.62 m

**The ceilings are identical, so that spread is the instrument's error, not the building's.** This is a free calibration
the estate would otherwise have to buy a laser for, and it is the error bar that every vertical claim inherits — including
design 36's finding that the receive **height** is worth a full stream, which cannot be stated honestly without it.

    python3 scripts/height_error.py 2.65 2.47 2.62

FALSIFIER, stated before the run: if the spread were larger than about 15% of the mean, the measurements would not be
measuring the ceiling at all and the honest output would be "no usable height", not an error bar.
"""
from __future__ import annotations

import statistics
import sys

MAX_RELATIVE_SPREAD = 0.15


def summarise(heights: list[float]) -> dict:
    mean = statistics.mean(heights)
    spread = max(heights) - min(heights)
    half = spread / 2.0
    return {
        "n": len(heights),
        "mean_m": round(mean, 3),
        "min_m": min(heights),
        "max_m": max(heights),
        "spread_m": round(spread, 3),
        "half_spread_m": round(half, 3),
        "stdev_m": round(statistics.stdev(heights), 3) if len(heights) > 1 else 0.0,
        "relative_half_spread": round(half / mean, 4) if mean else 0.0,
        "usable": bool(mean) and half / mean <= MAX_RELATIVE_SPREAD,
    }


def main(argv) -> int:
    values = [float(a) for a in argv[1:] if a.replace(".", "", 1).isdigit()]
    if len(values) < 2:
        values = [2.65, 2.47, 2.62]          # the three measured on 2026-11-02
    s = summarise(values)
    print(f"{s['n']} heights: {values}")
    print(f"mean {s['mean_m']:.2f} m, spread {s['spread_m']:.2f} m, stdev {s['stdev_m']:.3f} m")
    if not s["usable"]:
        print("\nNO USABLE HEIGHT: the spread is more than "
              f"{MAX_RELATIVE_SPREAD:.0%} of the mean, so these are not measuring the same ceiling.")
        return 1
    print(f"\nIf every ceiling is the same height, the phone's height error is "
          f"+/-{100 * s['half_spread_m']:.0f} cm ({100 * s['relative_half_spread']:.1f}%).")
    print(f"Site ceiling height: {s['mean_m']:.2f} m +/- {s['half_spread_m']:.2f} m")
    print("This is the error bar every vertical claim inherits - including the receive height that design 36 says is "
          "worth a whole stream.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
