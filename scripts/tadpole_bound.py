#!/usr/bin/env python3
"""max |N| = b3, as a theorem rather than a table.

    python3 scripts/tadpole_bound.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import tadpole_bound as T  # noqa: E402


def main() -> int:
    print("max |N| = b3 — proof, not enumeration\n")
    print("  N = sum_{i=1..n} (F_i H_{i+n} - F_{i+n} H_i),  n = b3/2")
    print("  each bracket lies in [-2, 2]  ->  |N| <= 2n = b3")
    print("  attained by F_i = F_{i+n} = 1, H_i = -1, H_{i+n} = 1  ->  N = b3\n")
    print(f"  {'b3':>3} {'theorem':>8} {'construction':>13} {'exhaustive':>11}")
    for b3 in (2, 4, 6, 8):
        F, H = T.attain(b3)
        print(f"  {b3:>3} {T.bound(b3):>8} {T.tadpole(F, H):>13} {T.measured(b3):>11}")
    print("\nThe earlier ladder (b3 = 2, 4, 6) was three samples of a theorem. The cap is LINEAR in the")
    print("dimension, which is why a count over flux vectors overestimates what the topology can carry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
