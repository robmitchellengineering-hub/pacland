#!/usr/bin/env python3
"""The primes as an interference sum over the zeros — verified against the primes themselves.

    python3 scripts/spectral_explicit.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import explicit as E  # noqa: E402

def main() -> int:
    a = E.audit()
    print("PACLAND · spectral — the explicit formula\n")
    print("psi(x) = x - sum over zeros of x^rho/rho - ln 2pi - ...\n")
    for c in a["convergence"]:
        print(f"x = {c['x']:.0f}   psi exact (from the primes) = {c['exact']:.3f}")
        for r in c["rows"]:
            print(f"   {r['n_zeros']:3} zeros -> {r['estimate']:10.3f}   error {r['error']:+.3f}")
        print()
    for ch in a["checks"]:
        print(f"{'PASS' if ch['pass'] else 'FAIL'}  {ch['check']}")
        print(f"      {ch['detail']}")
    print(f"\n{a['n_pass']}/{a['n']} checks pass")
    print("\nThis is what 'prime oscillations' means when it means anything: each zero is a")
    print("frequency, and the primes are the sum. Padgett's interference term was the right shape")
    print("aimed at the wrong set — the sum runs over the ZEROS, not over an undefined subset of")
    print("the primes.")
    return 0 if a["all_pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
