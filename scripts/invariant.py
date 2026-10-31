#!/usr/bin/env python3
"""The invariant I(b3) — one integer behind classification and accessibility.

    python3 scripts/invariant.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import invariant as I  # noqa: E402


def main() -> int:
    v = I.verdict()
    print("The invariant I(b3) — the unification-shaped target\n")
    print(f"  law      : rate(b3) = rate(6) * exp(-c (b3-6)),  c = {v['c']:.4f}")
    print(f"  anchors  : 0.1325/try at h12=2 (b3=6);  0.00137/try at h12=5 (b3=12)\n")
    print(f"  {'h12':>4} {'b3':>4} {'predicted/try':>15} {'per 400-call':>13} {'measured':>10}")
    for r in I.prediction_table():
        print(f"  {r['h12']:>4} {r['b3']:>4} {r['rate_per_try']:>15.4f} {r['points_per_400']:>13.1f} "
              f"{'-':>10}")
    print(f"\n  status   : {v['status'].upper()}")
    print(f"  {v['note']}")
    print("\nPredictions written BEFORE the run (dispatch 2026-10-31T0502Z). Stated after seeing the data, a")
    print("law is a description; stated before, it is a test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
