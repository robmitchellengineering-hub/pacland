#!/usr/bin/env python3
"""The tadpole distribution as a closed form.

    python3 scripts/tadpole_distribution.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import tadpole_distribution as T  # noqa: E402


def main() -> int:
    v = T.verdict()
    print("The tadpole distribution is a closed form\n")
    print("  P(x) = 4x^2 + 20x + 33 + 20x^-1 + 4x^-2")
    print("  count(N) = [x^N] P(x)^(b3/2)  minus 1 at N = 0\n")
    print(f"  {'b3':>3} {'orbits':>10} {'matches enumeration':>22}")
    for r in v["rows"]:
        print(f"  {r['b3']:>3} {r['orbits']:>10} {str(r['matches']):>22}")
    print(f"\n  {v['statement']}")
    print(f"\n  {v['consequence']}")
    c = T.counts(100)
    print(f"\n  b3 = 100: {sum(c.values()):.3e} orbits, computed by 50 polynomial multiplications")
    return 0


if __name__ == "__main__":
    sys.exit(main())
