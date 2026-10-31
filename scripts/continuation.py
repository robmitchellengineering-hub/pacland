#!/usr/bin/env python3
"""Route C — a period outside the large-complex-structure radius.

    python3 scripts/continuation.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.periods import continuation as C  # noqa: E402

def main() -> int:
    s = C.truncation_study()
    w = C.where_both_converge()
    print("Route C — the transfer payoff\n")
    print(f"  LCS converges      : {w['lcs']}")
    print(f"  conifold converges : {w['conifold']}")
    print(f"  computed at        : z = {float(s['z_over_zc']):.2f} z_c  (u = {float(s['u']):+.2f})")
    print("  -> outside the LCS radius, inside the conifold chart\n")
    for n in s["orders"]:
        print(f"  order {n:<4} Phi = {s['values'][n]}")
    print("\n  movement against the highest order:")
    for n, m in s["moves"].items():
        print(f"    {n:<4} -> {m:.2e}")
    print(f"\n  worst move = {s['worst_move']:.2e}   pass mark (<1e-10): {s['pass_mark_1e-10']}")
    print(f"\n  {s['note']}")
    print("\nA number that the LCS expansion cannot produce, computed by translating into the frame where it")
    print("converges. That is a capability, not a restatement.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
