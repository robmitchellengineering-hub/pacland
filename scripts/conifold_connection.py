#!/usr/bin/env python3
"""F2 M2c - the connection at the conifold, and the test that it closes.

    python3 scripts/conifold_connection.py

The z = 0 series cannot reach the conifold (it sits on the radius). The conifold's own expansion can reach
z = 0. So the two must agree where both converge, and the conifold branch must be a CONSTANT linear
combination of the four z = 0 branches. Nothing in this file uses a literature constant: the check is that
the coefficients do not depend on where you evaluate them.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402

from pacland.periods import connection as C  # noqa: E402


def main() -> int:
    r = C.connect()
    print("F2 M2c - the conifold connection\n")
    print("  fit at z =", ", ".join(f + " z_c" for f in r["fit_points"]))
    print(f"  system: det {mp.nstr(r['det'], 6)}  cond {mp.nstr(r['cond'], 6)}  ({r['n_max']} terms)")
    print("  coefficients of the conifold (exponent-2) branch in the LCS basis:")
    for k, a in enumerate(r["coefficients"]):
        print(f"    a[{k}] = {mp.nstr(a, 20)}")
    print("\n  constancy test at points NOT used in the fit:")
    for row in r["rows"]:
        tag = "" if row["in_verdict"] else "   (truncation-limited, reported only)"
        print(f"    z = {row['z']:>4} z_c   relative {mp.nstr(row['relative'], 3):>10}{tag}")
    print(f"\n  worst inside the verdict: {mp.nstr(r['worst'], 3)}")
    print(f"  closes: {r['closes']}")
    print("\n  The weight is load-bearing: dropping the binomial factor in the log normalisation of")
    print("  omega_1..omega_3 leaves omega_2 and omega_3 outside the solution space and the residual jumps")
    print("  to 6e-2. That is the mutation test in tests/test_conifold_connection.py, and it is how this")
    print("  gate failed and then passed.")
    return 0 if r["closes"] else 1


if __name__ == "__main__":
    sys.exit(main())
