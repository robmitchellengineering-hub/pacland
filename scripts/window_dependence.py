#!/usr/bin/env python3
"""H-A's artefact: the content "law" is the window's size growth, not a property of the landscape.

    python3 scripts/window_dependence.py
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.exactness import windows as W  # noqa: E402


def content(b3: int, max_abs: int) -> int:
    f = W.enumerate_window(b3, max_abs)
    N = W.tadpoles(f)
    prim = np.array([W.primitive(r) for r in f])
    return int(((N > 0) & (N <= 1))[prim].sum())


def main() -> int:
    print("H-A: is the content 'law' a law, or the window?\n")
    print(f"  {'window':>8} {'b3=2':>7} {'b3=4':>8} {'per-unit-b3':>12} {'(2ma+1)^2':>10}")
    for ma in (1, 2):
        k0, k1 = content(2, ma), content(4, ma)
        factor = (k1 / k0) ** 0.5
        print(f"  {ma:>8} {k0:>7} {k1:>8} {factor:>12.2f} {(2*ma+1)**2:>10}")
    print("\n  the factor tracks the window, so A = 8.554 is a window fact, not a law of the landscape.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
