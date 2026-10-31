"""Converge the polarised stream count — caps 1k to 20k over the full resonance window.

The truncation study left the count wandering 2/4/3/4 as the cap went 60/120/240/480. This sweeps the cap with
three seeds per cap and three receiver heights, on the node, because the full window holds ~39,000 modes.

FALSIFIER, stated before the run: if the count is still moving at the largest cap, no converged polarised
stream count exists at this Q from a deterministic mode sum, and the treatment must change.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_polarisation_converge.py
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402

A, B, D = 3.0, 4.0, 2.5
F = 5.18e9
Q = 200.0
N = 4
CAPS = (1000, 2500, 5000, 10000, 20000)
SEEDS = (11, 23, 37)
V = (0.0, 0.0, 1.0)


def lattice(zf):
    return [(A * (0.2 + 0.6 * i / (N - 1)), B * (0.2 + 0.6 * j / (N - 1)), zf * D)
            for i, j in zip(range(N), reversed(range(N)))]


def mirrored(tx, zf):
    return [((A - x) * 0.8 + 0.1 * A, (B - y) * 0.8 + 0.1 * B, min(D - 0.15, zf * D)) for (x, y, _z) in tx]


def main() -> int:
    out = {"q": Q, "f": F, "caps": list(CAPS), "seeds": list(SEEDS),
           "falsifier": "a count still moving at the largest cap means no converged number exists",
           "runs": []}
    t0 = time.time()
    for zf in (0.5, 0.75, 0.9):
        row = {"z_fraction": zf, "caps": {}}
        for cap in CAPS:
            vals = []
            for seed in SEEDS:
                h = E.channel_matrix_polarised(A, B, D, F, lattice(zf), mirrored(lattice(zf), zf),
                                               [V] * N, [V] * N, q_factor=Q, max_modes=cap, seed=seed)
                vals.append(E.streams(h, 20.0))
            row["caps"][str(cap)] = vals
            print(f"  z={zf:.2f} cap={cap:>6}: streams {vals}  ({time.time()-t0:.0f}s)", flush=True)
        out["runs"].append(row)
    with open("polarisation_converge.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote polarisation_converge.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
