#!/usr/bin/env python3
"""Is the ~0.8 minima rate derivable from the lattice?

    python3 scripts/minima_correlation.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import minima_correlation as M  # noqa: E402


def main() -> int:
    r = M.correlations()
    print(f"Is the minima rate derivable from the lattice?  (n = {r['n']}, rate = {r['minima_rate']:.3f})\n")
    print(f"  {'invariant':<12}{'corr with is_minimum':>22}")
    for k, v in r["correlations"].items():
        print(f"  {k:<12}{'constant' if v is None else f'{v:>22.3f}'}")
    print(f"\n  strongest lattice correlation: {r['strongest_lattice']:.3f}")
    print(f"  {r['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
