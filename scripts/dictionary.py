#!/usr/bin/env python3
"""The dictionary engine — first entry: flux scaling.

    python3 scripts/dictionary.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.periods import dictionary as D  # noqa: E402


def main() -> int:
    for d in (2, 3):
        e = D.flux_scaling(d)
        print(f"\nENTRY  {e.name}")
        print(f"  from : {e.frame_a}")
        print(f"  to   : {e.frame_b}")
        print(f"  {e.t_note}")
        print(f"  {e.tinv_note}")
        print(f"  identity  T-inv(T(x)) = x        residual {e.identity_residual:.1e}")
        for c in e.carries:
            print(f"  carry     {c.name:<28} {c.law:<12} "
                  f"{c.value_a:.6g} -> {c.value_b:.6g}   residual {c.residual:.1e}  "
                  f"{'PASS' if c.passes else 'FAIL'}")
        print(f"  boundary  {e.boundary}")
        print(f"  entry passes: {e.passes}")
    print("\nThe law is the lemma's own (W -> dW, N -> d^2 N), not a fit. The boundary is what keeps it")
    print("from overclaiming: d must be a positive INTEGER, and the zero set being invariant means this is")
    print("a relabelling of one vacuum, not a second one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
