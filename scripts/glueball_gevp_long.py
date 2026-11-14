"""The long glueball GEVP run — resolve the 0++ plateau.

Usage: python3 scripts/glueball_gevp_long.py beta N n_meas seed
"""
from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, "src")
from pacland import kernel as nb  # noqa: E402
from pacland import lattice_ym_su2 as py  # noqa: E402


def main(argv):
    beta = float(argv[0]) if len(argv) > 0 else 2.4
    N = int(argv[1]) if len(argv) > 1 else 8
    n_meas = int(argv[2]) if len(argv) > 2 else 20000
    seed = int(argv[3]) if len(argv) > 3 else 0
    print(f"beta={beta} N={N} n_meas={n_meas} seed={seed}", flush=True)
    C, gbar = nb.measure_variational_2(beta, 4, N, 30, n_meas, seed, np.array([0, 3, 6], dtype=np.int64))
    masses = nb.gevp_masses(C, N)
    print("gbar =", np.round(gbar, 0), flush=True)
    print("GEVP masses:", np.round(masses, 4), flush=True)
    sigma = py.measure_string_tension(beta, d=4, N=N, n_sweeps=3, seed=seed)
    pos = masses[masses > 0]
    if pos.size:
        m = float(np.median(pos))
        print(f"m = {m:.4f}  m/sqrt(sigma) = {m/np.sqrt(sigma):.4f}  (sigma={sigma:.2f})", flush=True)
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
