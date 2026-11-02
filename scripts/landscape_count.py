#!/usr/bin/env python3
"""Does the discrete gauge symmetry shrink the 10^500?

    python3 scripts/landscape_count.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import landscape_count as L  # noqa: E402


def main() -> int:
    v = L.verdict()
    print("The landscape count — does the gauge symmetry shrink 10^500?\n")
    print(f"  {'b3':>3} {'flux pairs':>11} {'orbits':>9} {'orbits/pairs':>13} {'0<N<=1':>8}")
    for r in v["rows"]:
        print(f"  {r['b3']:>3} {r['flux_pairs']:>11} {r['orbits']:>9} "
              f"{r['quotient_ratio']:>13.5f} {r['up_to_1']:>8}")
    print(f"\n  claim tested: {v['claim_tested']}")
    print(f"  VERDICT: {v['verdict']}")
    print(f"  window:  {v['window']}")
    print("\nTwo independent reasons, both exact:")
    print("  1. the gauge quotient removes ONE pair out of 531,441 at b3=6 — flux vectors are almost all")
    print("     distinct orbits, so 10^500 is not inflated by gauge copies;")
    print("  2. at fixed 0 < N <= 1 the orbit count runs 20 -> 1,480 -> 107,100 across b3 = 2,4,6, so the")
    print("     content is NOT a function of the tadpole bound alone — it carries a window dependence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
