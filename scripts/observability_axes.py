#!/usr/bin/env python3
"""H-B: is measure-invariance the same as observability?

    python3 scripts/observability_axes.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import observability_axes as A  # noqa: E402


def main() -> int:
    v = A.verdict()
    t = A.crosstab()
    print("H-B: does invariance equal exactness?\n")
    print(f"  {'':22}{'EXACT':>10}{'not exact':>12}")
    print(f"  {'INVARIANT':<22}{len(t[(True, True)]):>10}{len(t[(True, False)]):>12}")
    print(f"  {'DEPENDENT':<22}{len(t[(False, True)]):>10}{len(t[(False, False)]):>12}")
    print(f"\n  {v['verdict']}")
    print(f"\n  invariant but not exact : {v['invariant_not_exact']}")
    print(f"  exact but not invariant : {v['exact_not_invariant']}")
    print(f"\n  surviving: {v['surviving_weaker_claim']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
