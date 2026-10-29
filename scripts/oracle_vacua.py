#!/usr/bin/env python3
"""Solving the vacua: DW = 0 by Newton, validated by construction, and what the integer lattice gives.

    python3 scripts/oracle_vacua.py
"""
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.oracle import potential_t6 as P  # noqa: E402


def main() -> int:
    print("PACLAND · solving the vacua\n")
    r = P.validation_by_construction()
    print("the solver, validated by construction:")
    print(f"   a flux made F-flat at a chosen point: |DW| = {r['construction_residual']:.1e}")
    print(f"   Newton, from a different start: converged {r['converged']}, "
          f"recovered the point to {r['recovery_error']:.1e}")
    print(f"   -> {'PASS' if r['pass'] else 'FAIL'}\n")

    rng = np.random.default_rng(4)
    t0 = time.time()
    found, tried = 0, 0
    for _ in range(10):
        F = rng.integers(-2, 3, size=8).astype(float)
        H = rng.integers(-2, 3, size=8).astype(float)
        tried += 1
        if P.solve_supersymmetric(F, H, starts=3, seed=tried)["converged"]:
            found += 1
    print("the integer lattice:")
    print(f"   {found} of {tried} generic integer fluxes admit a supersymmetric vacuum "
          f"({round(time.time() - t0, 1)} s)")
    print("\nThat zero is a result, not a failure. Supersymmetric vacua require ISD fluxes, which is a")
    print("measure-zero condition on the integer lattice — so a small integer flux is generically not")
    print("F-flat anywhere. To build a spectrum for the chaos question we must EITHER work on the ISD")
    print("locus (where fluxes are real-valued, not integers) OR look for non-supersymmetric vacua")
    print("with DV = 0, which do not require ISD.")
    print("\nAnd there is a trap waiting on the ISD route: supersymmetric Minkowski vacua have flat")
    print("directions, so their mass spectrum is full of zero modes — which would make the spacing")
    print("statistic a statement about degeneracies, not about chaos, exactly like the |W| lattice.")
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
