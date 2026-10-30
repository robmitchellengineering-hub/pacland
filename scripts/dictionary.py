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
    e2 = D.mirror_map()
    print(f"\nENTRY  {e2.name}")
    print(f"  from : {e2.frame_a}")
    print(f"  to   : {e2.frame_b}")
    print(f"  {e2.t_note}")
    print(f"  {e2.tinv_note}")
    print(f"  identity  residual {e2.identity_residual:.1e}")
    for c in e2.carries:
        print(f"  carry     {c.name:<46} residual {c.residual:.1e}  {'PASS' if c.passes else 'FAIL'}")
    print(f"  boundary  {e2.boundary}")
    print(f"  entry passes: {e2.passes}")

    e3 = D.s_t_duality()
    print(f"\nENTRY  {e3.name}")
    print(f"  from : {e3.frame_a}")
    print(f"  to   : {e3.frame_b}")
    print(f"  {e3.t_note}")
    print(f"  {e3.tinv_note}")
    print(f"  identity  residual {e3.identity_residual:.1e}")
    for c in e3.carries:
        print(f"  carry     {c.name:<28} {c.law:<18} residual {c.residual:.1e}  {'PASS' if c.passes else 'FAIL'}")
    print(f"  boundary  {e3.boundary}")
    print(f"  entry passes: {e3.passes}")

    print("\nThe law is the lemma's own (W -> dW, N -> d^2 N), not a fit. The boundary is what keeps it")
    print("from overclaiming: d must be a positive INTEGER, and the zero set being invariant means this is")
    print("a relabelling of one vacuum, not a second one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
