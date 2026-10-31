"""Converge the polarised stream count — the computation that decides whether a number exists at all.

The truncation study found the stream count wandering 2/4/3/4 as the mode cap went 60/120/240/480. This runs it
up to the FULL resonance window (~19,000 modes at 5.18 GHz, Q = 200) and asks whether it plateaus.

FALSIFIER, stated before the run: if the stream count is still moving at the largest cap, then no converged
polarised stream count exists at this Q from a mode sum, and the approach must change (a different Green's
function, or a statistical (random-matrix) treatment instead of a deterministic sum).

Run on pacland-rog (numpy, no display):
    /home/rob/cytools-venv/bin/python scripts/node_polarisation_converge.py
"""
import json
import math
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402

from pacland.spectral import em_modes as E  # noqa: E402

A, B, D = 3.0, 4.0, 2.5
F = 5.18e9
Q = 200.0
N = 4
CAPS = (1000, 2500, 5000, 10000, 20000)
SEEDS = (11, 23, 37)


def lattice(zf):
    return [(A * (0.2 + 0.6 * i / (N - 1)), B * (0.2 + 0.6 * j / (N - 1)), zf * D)
            for i, j in zip(range(N), reversed(range(N)))]


def mirrored(tx, zf):
    return [((A - x) * 0.8 + 0.1 * A, (B - y) * 0.8 + 0.1 * B, min(D - 0.15, zf * D)) for (x, y, _z) in tx]


def fields(pool, pos, pol):
    """(M, len(pos)) array of pol . E_mode at each position, vectorised over modes."""
    m = len(pool)
    out = np.zeros((m, len(pos)))
    for j, (x, y, z) in enumerate(pos):
        for i, (f0, kind, idx) in enumerate(pool):
            e = E.mode_field(idx, kind, x, y, z, A, B, D)
            out[i, j] = pol[0] * e[0] + pol[1] * e[1] + pol[2] * e[2]
    return out


def h_from(pool, tx, rx, tx_pol, rx_pol, q=Q, f=F):
    f0 = np.array([p[0] for p in pool])
    w0 = 2 * math.pi * f0
    w = 2 * math.pi * f
    denom = (w0 * w0 - w * w) + 1j * (w0 * w / q)
    ft = fields(pool, tx, tx_pol)      # (M, n)
    fr = fields(pool, rx, rx_pol)      # (M, n)
    return (fr.T * (1.0 / denom)) @ ft


def main() -> int:
    width = F / Q
    lo, hi = F - width, F + width
    t0 = time.time()
    pool_all = [(f0, kind, idx) for f0, kind, idx in E.cavity_modes(A, B, D, hi) if f0 >= lo]
    print(f"resonance window {lo/1e9:.4f}-{hi/1e9:.4f} GHz holds {len(pool_all)} modes "
          f"(built in {time.time()-t0:.1f}s)", flush=True)
    out = {"window": [lo, hi], "pool": len(pool_all), "q": Q, "f": F,
           "falsifier": "a stream count still moving at the largest cap means no converged number exists",
           "runs": []}
    V = (0.0, 0.0, 1.0)
    for zf in (0.5, 0.75, 0.9):
        tx, rx = lattice(zf), mirrored(lattice(zf), zf)
        row = {"z_fraction": zf, "caps": {}}
        for cap in CAPS:
            vals = []
            for seed in SEEDS:
                rng = random.Random(seed)
                pool = pool_all if len(pool_all) <= cap else rng.sample(pool_all, cap)
                pool.sort()
                h = h_from(pool, tx, rx, [V] * N, [V] * N)
                vals.append(E.streams(h, 20.0))
            row["caps"][str(cap)] = vals
            print(f"  z={zf:.2f} cap={cap:>6}: streams {vals}", flush=True)
        out["runs"].append(row)
    with open("polarisation_converge.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote polarisation_converge.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
