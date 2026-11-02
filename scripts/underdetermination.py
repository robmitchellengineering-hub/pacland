#!/usr/bin/env python3
"""The exact dimension of the measure space.

    python3 scripts/underdetermination.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import underdetermination as U  # noqa: E402


def main() -> int:
    v = U.verdict()
    print("Is the measure underdetermined? An exact count, not an opinion.\n")
    print(f"  {'b3':>3} {'orbits':>9} {'distinct N':>11} {'distinct |N|':>13} {'measure dim':>12}")
    for r in v["rows"]:
        print(f"  {r['b3']:>3} {r['orbits']:>9} {r['distinct_N']:>11} {r['distinct_absN']:>13} "
              f"{r['measure_dimension']:>12}")
    print(f"\n  every tadpole in [-b3, b3] attained: {v['every_tadpole_attained']}")
    print(f"\n  {v['statement']}")
    print(f"\n  {v['citation']}")
    print(f"  falsifier: {v['falsifier']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
