"""SU(2) glueball mass ratio m/sqrt(σ) sweep — the continuum ratio conjecture.

Runs the glueball mass + string tension at a grid of β and seeds, printing the RG-invariant
m/sqrt(σ) per (β, N, seed). The weak-coupling plateau across β and N is the continuum prediction.

Usage: python3 scripts/glueball_ratio_sweep.py 2.2 2.4 2.6 2.8 --N 6 --seeds 0 1
"""
from __future__ import annotations

import argparse
import sys

import numpy as np

sys.path.insert(0, "src")
from pacland.glueball import glueball_mass  # noqa: E402
from pacland.lattice_ym_su2 import measure_string_tension  # noqa: E402


def sweep(betas, N, seeds, n_sweeps=20, n_meas=100):
    print(f"beta  N  seed  m          sigma      m/sqrt(sigma)", flush=True)
    rows = []
    for beta in betas:
        for seed in seeds:
            m = glueball_mass(beta, N=N, n_sweeps=n_sweeps, n_meas=n_meas, seed=seed)
            sigma = measure_string_tension(beta, d=4, N=N, n_sweeps=3, seed=seed)
            ratio = m / np.sqrt(sigma) if sigma > 0 and m > 0 else float("nan")
            print(f"{beta:<5.2f} {N}  {seed}   {m:+.4f}  {sigma:.4f}  {ratio:.4f}", flush=True)
            rows.append((beta, N, seed, m, sigma, ratio))
    ratios = [r[5] for r in rows if not np.isnan(r[5])]
    if len(ratios) >= 2:
        print(f"\nmean m/sqrt(sigma) = {np.mean(ratios):.4f}  over {len(ratios)} resolved points", flush=True)
    return rows


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("betas", nargs="*", type=float, default=[2.2, 2.4, 2.6, 2.8])
    ap.add_argument("--N", type=int, default=6)
    ap.add_argument("--seeds", nargs="*", type=int, default=[0, 1])
    ap.add_argument("--n-sweeps", type=int, default=20)
    ap.add_argument("--n-meas", type=int, default=100)
    args = ap.parse_args(argv)
    sweep(args.betas, args.N, args.seeds, args.n_sweeps, args.n_meas)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
