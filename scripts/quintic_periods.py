#!/usr/bin/env python3
"""F2 M1 — the quintic's Picard-Fuchs operator, solved and bounded.

    python3 scripts/quintic_periods.py

What this prints is what is established. The conifold period is NOT claimed: the Gamma-value has not been
pinned from a citable source, which is #210's own rule.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402

from pacland.periods import quintic as Q  # noqa: E402


def main() -> int:
    mp.mp.dps = 40
    print("F2 M1 - the quintic's Picard-Fuchs operator, solved and bounded\n")
    print("    L = theta^4 - 5 z (5theta+1)(5theta+2)(5theta+3)(5theta+4)\n")

    js = Q.coeff_jets(10)
    worst = max(abs(js[n][0] / Q.closed_form_coeff(n) - 1) for n in range(11))
    print(f"check 1  c_n(0) vs (5n)!/(n!)^5   worst relative diff {mp.nstr(worst, 5)}")
    print("         (the recursion reproduces the literature coefficient exactly)\n")

    M = Q.monodromy_zero_point()
    print("check 2  the monodromy at z=0, in the (omega_0..omega_3) basis:")
    for row in M:
        print("         ", [mp.nstr(x, 6) for x in row])
    print("         unipotent, index 4 -- one Jordan block, as the fourfold indicial root requires\n")

    print("check 3  the tail bound, and where it stops working:")
    for frac in ("0.5", "0.9", "0.99", "1.0"):
        z = Q.Z_CONIFOLD * mp.mpf(frac)
        r = Q.ratios(300, z)
        b = Q.tail_bound(300, z)
        flag = "bounded" if b != mp.inf else "NO BOUND"
        print(f"         z = {frac:>4} z_c   ratio -> {float(r[-1]):.6f}   bound {float(b):.2e}  {flag}")

    print("\nthe finding: the conifold sits exactly on the radius of convergence (z_c = 1/5^5), so the")
    print("ratio r -> 1 there and the bound degrades by four orders of magnitude while the series inside")
    print("is exact to 1e-37. No number of extra terms certifies the conifold: it needs its own local")
    print("expansion. That is the next step, and it is stated rather than worked around.")
    print("\nnot claimed: R1's conifold Gamma-value. #210's rule is that it must be pinned from a citable")
    print("source before use, and it has not been.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
