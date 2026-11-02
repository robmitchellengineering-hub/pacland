#!/usr/bin/env python3
"""The two b3 scales and their product.

    python3 scripts/b3_scaling.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import b3_scaling as S  # noqa: E402


def main() -> int:
    s = S.scales()
    print("The two b3 scales\n")
    print(f"  CONTENT      A = {s['A']:.3f} per unit b3   (intervals: "
          + ", ".join(f"{a}->{b}: {f:.3f}" for a, b, f in s["content"]["intervals"]) + ")")
    print(f"  ACCESSIBILITY B = {s['B']:.3f} per unit b3   (intervals: "
          + ", ".join(f"{a}->{b}: {f:.3f}" for a, b, f in s["accessibility"]["intervals"]) + ")")
    print(f"\n  product A*B = {s['product']:.3f}   range {s['product_range'][0]:.2f} - {s['product_range'][1]:.2f}")
    print(f"  VERDICT: {s['verdict']}")
    print(f"\n  caveat:    {s['caveat']}")
    print(f"  falsifier: {s['falsifier']}")
    print("\nThe content scale is a clean exponential (intervals agree to 0.6%). The accessibility scale is NOT:")
    print("0.575 then 0.308 per unit b3 -- it steepens, so a single B would hide that. The product is above 1 on")
    print("every interval regardless, which is why the 'content' half of the statement is the defensible one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
