#!/usr/bin/env python3
"""B1 fixed - the GV basis convention.

    python3 scripts/gv_basis.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.periods import gv_basis as G  # noqa: E402


def main() -> int:
    r = G.report()
    print("B1 - the GV basis convention\n")
    print("  F_inst = sum_d n_d Li_3(q^d)   =>   c_m = (1/m^3) sum_{d|m} d^3 n_d\n")
    print(f"  {'d':>2}  {'c_m (the coefficient)':>22}  {'inverse multi-cover':>20}  {'naive m^3 c_m':>14}")
    for row in r["rows"]:
        flag = "  <- integral and WRONG" if row["naive_is_wrong"] else ""
        print(f"  {row['degree']:>2}  {str(row['c_m']):>22}  {str(row['correct']):>20}  {str(row['naive']):>14}{flag}")
    print(f"\n  round trip exact: {r['round_trip']}")
    print(f"  the naive read-off is all-integer: {r['naive_all_integer']}  and wrong: {r['naive_any_wrong']}")
    print("\n  THE FINDING: integrality is not a sufficient check. On composite degrees the naive read-off")
    print("  returns whole numbers that are off by a factor of the degree -- so an 'all integers' pass")
    print("  says nothing unless the extraction used the inverse multi-cover relation. That is why #209's")
    print("  check fired on the non-primitive degrees, and why a green tick there would have misled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
