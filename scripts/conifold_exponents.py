#!/usr/bin/env python3
"""F2 M2a - the conifold's local exponents, computed exactly.

    python3 scripts/conifold_exponents.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import sympy as sp  # noqa: E402

from pacland.periods import conifold as C  # noqa: E402


def main() -> int:
    r = C.structure()
    print("F2 M2a - the conifold's local exponents at u = 1 - z/z_c\n")
    print("    singular points:", {k: str(v) for k, v in r["singular_points"].items()})
    print("    indicial polynomial:", r["indicial"])
    print("    exponents:", [str(e) for e in r["exponents"]],
          " with multiplicities", r["multiplicities"])
    print("    all integers:", r["all_integer"], "-> monodromy unipotent:",
          r["unipotent"], " (eigenvalues of exp(2 pi i s) all 1)")
    print("    double root at:", r["double_root"], "-> that is where the single logarithm lives")
    print("    local radius:", r["local_radius"])
    print()
    print("Why it matters: the z = 0 series cannot certify the conifold (its radius ends there), but the")
    print("conifold's own expansion is bounded for |u| < 1 and reaches z = 0. The next step is the")
    print("connection: match the two expansions at z = z_c/2, where both converge, and solve a 4x4")
    print("system. That determines the conifold periods WITHOUT a literature constant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
