"""PASS-2 for the polarised stream count: does 3-4 of 4 survive a different Q?

docs/polarisation.md records 3-4 of 4 at 20 dB for Q = 200, converged over the full resonance window. A PASS-2
claim needs the same answer from a DIFFERENT parameterisation, so this repeats it at Q = 100 and Q = 400 — a factor
of four apart, which also changes the window size by that factor.

    /home/rob/cytools-venv/bin/python scripts/node_polarisation_q.py

FALSIFIER, stated before the run: if the count moves by more than one stream between Q = 100 and Q = 400, the
polarised answer is a property of the assumed damping and stays PASS-1.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402

A, B, D = 3.0, 4.0, 2.5
F = 5.18e9
N = 4
QS = (100.0, 200.0, 400.0)
CAP = 20000
SEEDS = (11, 23, 37)
HEIGHTS = (0.5, 0.75, 0.9)
V = (0.0, 0.0, 1.0)


def lattice(zf):
    return [(A * (0.2 + 0.6 * i / (N - 1)), B * (0.2 + 0.6 * j / (N - 1)), zf * D)
            for i, j in zip(range(N), reversed(range(N)))]


def mirrored(tx, zf):
    return [((A - x) * 0.8 + 0.1 * A, (B - y) * 0.8 + 0.1 * B, min(D - 0.15, zf * D)) for (x, y, _z) in tx]


def main() -> int:
    out = {"caps": CAP, "seeds": list(SEEDS), "heights": list(HEIGHTS),
           "falsifier": "more than one stream of movement between Q=100 and Q=400 keeps this at PASS-1",
           "runs": []}
    t0 = time.time()
    for q in QS:
        row = {"q": q, "heights": {}}
        for zf in HEIGHTS:
            vals = [E.streams(E.channel_matrix_polarised(
                A, B, D, F, lattice(zf), mirrored(lattice(zf), zf), [V] * N, [V] * N,
                q_factor=q, max_modes=CAP, seed=s), 20.0) for s in SEEDS]
            row["heights"][str(zf)] = vals
            print(f"  Q={q:>5.0f} z={zf:.2f}: streams {vals}  ({time.time()-t0:.0f}s)", flush=True)
        out["runs"].append(row)
    all_vals = [v for r in out["runs"] for vs in r["heights"].values() for v in vs]
    spread = max(all_vals) - min(all_vals)
    out["spread"] = spread
    out["verdict"] = "PASS-2" if spread <= 1 else "STAYS PASS-1"
    print(f"\n  spread across Q and height: {spread} stream(s) -> {out['verdict']}")
    with open("polarisation_q.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote polarisation_q.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
