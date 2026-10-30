#!/usr/bin/env python3
"""Route C exact sub-item — the conifold coefficients, exactly.

    python3 scripts/exact_series.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.periods import exact_series as E  # noqa: E402


def main() -> int:
    f = E.form()
    r = E.against_numeric(10)
    print("Route C, exact sub-item\n")
    print(f"  {f['statement']}\n")
    print("  the first coefficients, in Q:")
    for i, c in enumerate(r["exact"][:6]):
        print(f"    c_{i} = {c}")
    print(f"\n  agreement with the numeric series: {r['worst_relative']:.2e}")
    print(f"  connection matrix: {f['connection_matrix']}")
    print("\nThe transcendental structure is not in the series — it is in the basis change. That is a")
    print("statement about where the algebra lives, and it says exactly which part of the connection audit")
    print("is still a measurement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
