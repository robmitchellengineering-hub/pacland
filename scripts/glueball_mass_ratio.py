"""SU(2) 0++ glueball mass in string-tension units — the reproducible measurement.

    python3 scripts/glueball_mass_ratio.py [beta ...] [--N 8] [--n-meas 3000]

Measures m (glueball effective mass, Numba kernel) and sigma (Wilson-loop Creutz ratio) at each
beta, and prints m/sqrt(sigma). Reproduces the known SU(2) 0++ ratio ~3.3-3.7 at beta=1.8-2.0.

This is VALIDATION of the stack, not a new result — the SU(2) glueball mass is known (Michael 1980s,
Teper et al.).
"""
from __future__ import annotations

import argparse
import sys

import numpy as np

sys.path.insert(0, "src")
from pacland import kernel as nb  # noqa: E402
from pacland import lattice_ym_su2 as py  # noqa: E402


def string_tension(links, R=2):
    """The Wilson-loop Creutz ratio chi(R,R) — the area-law string tension estimate."""
    return py.creutz_ratio(links, R, R)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("betas", nargs="*", type=float, default=[1.8, 2.0])
    ap.add_argument("--N", type=int, default=8)
    ap.add_argument("--n-meas", type=int, default=3000)
    args = ap.parse_args(argv)
    print(f"{'beta':>6} {'m':>8} {'chi(2,2)':>9} {'m/sqrt(sigma)':>13}")
    for beta in args.betas:
        C, m_eff, _ = nb.measure_glueball(beta, 4, args.N, 30, args.n_meas, 0)
        m = m_eff[0]
        rng = np.random.default_rng(0)
        links = np.array([py.random_su2(rng) for _ in range(4 * args.N**4)])
        links = links.reshape((4,) + (args.N,) * 4 + (4,))
        links = py.metropolis(links, beta, rng, 50)
        sigma = string_tension(links)
        print(f"{beta:>6} {m:>8.4f} {sigma:>9.4f} {m/np.sqrt(sigma):>13.4f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
