#!/usr/bin/env python3
"""Route A — the scaling study: which lattice facts survive a change of b3?

    python3 scripts/scaling.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import scaling as S  # noqa: E402


def main() -> int:
    r = S.report()
    print("Route A — the scaling ladder (exact, max_abs = 1)\n")
    print(f"  {'fact':<26} " + "  ".join(f"b3={b}" for b in r["ladder"]) + "   verdict")
    for k, v in r["facts"].items():
        vals = "  ".join(f"{x:>7.4f}" if isinstance(x, float) else f"{x:>7d}" for x in v["values"])
        print(f"  {k:<26} {vals}   {v['verdict']} ({v['direction']})")
    print(f"\n  scale-invariant facts: {r['invariant'] or 'NONE'}")
    print(f"  {r['note']}")
    print("\n  The exact ladder stops at b3 = 6: b3 = 8 is 43M pairs (~5.5 GB). That limit is part of the")
    print("  result, not a footnote — anything needing larger b3 needs a bigger machine or a different argument.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
