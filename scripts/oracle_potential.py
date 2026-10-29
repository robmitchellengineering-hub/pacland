#!/usr/bin/env python3
"""The IIB scalar potential on T^6 — validated before it is believed.

    python3 scripts/oracle_potential.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.oracle import potential_t6 as P  # noqa: E402


def main() -> int:
    r = P.validate()
    print("PACLAND · the scalar potential on T^6\n")
    print("V = e^K ( g^{i jbar} D_i W D_jbar Wbar - 3 |W|^2 )\n")
    for c in r["checks"]:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['check']}")
        print(f"      {c['detail']}")
    print(f"\n{r['n_pass']}/{r['n']} validations pass")
    print("\nTwo of them are exact identities, which is why they are worth running:")
    print("  - the no-scale identity must give 3 on the Kaehler moduli, not 'about 3'")
    print("  - a constant W must give V = 0 on that sector to machine precision")
    print("The first version of this file failed both: a real finite-difference step probes Re(tau),")
    print("and K depends only on Im(tau), so every gradient came out zero and the identity read 0.0.")
    return 0 if r["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
