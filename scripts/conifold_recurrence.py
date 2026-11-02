#!/usr/bin/env python3
"""H-C's artefact: does the conifold coefficient sequence have a rational generating function?

Tested the only way that means anything: **out of sample and at low order**. A Berlekamp-Massey run on n terms always
returns an order-n/2 recurrence and "verifies" perfectly -- that is overfitting, not evidence.

    python3 scripts/conifold_recurrence.py
"""
import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.periods import conifold_recursion as R  # noqa: E402

MAX_ORDER = 7


def coefficients(n: int = 36) -> list:
    mp.mp.dps = 120
    out = []
    for x in R.numeric_series(n_max=n, s0=2, dps=120):
        f = x if isinstance(x, Fraction) else Fraction(str(mp.nstr(x, 90)))
        out.append(f.limit_denominator(10 ** 30))
    return out


def fit(c: list, k: int):
    """Solve for a_1..a_k with c[n] = sum a_i c[n-i] using the first k equations."""
    M = [[c[k + n - i - 1] for i in range(k)] + [c[k + n]] for n in range(k)]
    for col in range(k):
        piv = next((r for r in range(col, k) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(k):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][k] for i in range(k)]


def main() -> int:
    c = coefficients()
    print(f"H-C: rational generating function for {len(c)} conifold coefficients?")
    print(f"  c0..c4 = {', '.join(str(x) for x in c[:5])}\n")
    found = None
    for k in range(1, MAX_ORDER + 1):
        a = fit(c, k)
        if a is None:
            print(f"  order {k}: singular")
            continue
        holds = all(sum(a[i] * c[n - i - 1] for i in range(k)) == c[n] for n in range(k, len(c)))
        print(f"  order {k}: holds on all {len(c)} terms = {holds}")
        if holds and found is None:
            found = k
    if found is None:
        print(f"\n  no constant-coefficient recurrence of order <= {MAX_ORDER} holds out of sample.")
        print("  So the GF is not a small rational function and the arithmetic null stands as a bounded wall.")
        print("  NOTE: a Berlekamp-Massey run on these terms WOULD return an order-~18 recurrence that verifies")
        print("  perfectly -- that is overfitting, not evidence. This test is out of sample at low order for that reason.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
