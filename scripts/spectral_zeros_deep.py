#!/usr/bin/env python3
"""The deep run: 22,491 zeros below t = 20,000, in about thirty seconds.

    python3 scripts/spectral_zeros_deep.py

Kept out of the certificate and the test suite because it takes half a minute; the numbers it produces
are quoted in docs/external-claims-padgett.md with the method and the limit stated.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import explicit as E  # noqa: E402
from pacland.spectral import zeros as Z  # noqa: E402


def main() -> int:
    zeros = Z.find_zeros(t_to=20000.0, step=0.05)
    sp = Z.unfolded_spacings(zeros)
    r = Z.ratio_statistic(sp)
    gue = Z.gue_control(len(sp))
    pois = Z.poisson_ratio()
    print("PACLAND · the deep zero run\n")
    print(f"zeros below t = 20,000 : {len(zeros)}   (smooth count {Z.smooth_count(20000.0):.1f})")
    print(f"mean unfolded spacing  : {sum(sp) / len(sp):.5f}")
    print(f"ratio statistic        : {r:.4f}")
    print(f"  synthetic GUE control: {gue['mean']:.4f} +- {gue['sd']:.4f}")
    print(f"  Poisson control      : {pois:.4f}   "
          f"({abs(r - pois) / gue['sd']:.0f} control sd away)")
    print("\nand the primes come out of them:")
    print(f"{'x':>10} {'psi from the primes':>20} {'error, 22k zeros':>18}")
    for x in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
        exact = E.chebyshev_psi(int(x))
        est = E.explicit_formula(x, zeros)
        print(f"{x:>10} {exact:>20.1f} {est - exact:>+18.2f}")
    print("\nThe reconstruction is good to about one unit up to 10^5 and degrades above it: the")
    print("truncation error scales with the square root of x, so each extra decade of x needs far")
    print("more zeros. That limit is a finding, not a failure — it says exactly how many zeros a")
    print("given x requires.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
