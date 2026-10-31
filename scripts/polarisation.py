"""Does polarisation explain why a real 4x4 link carries 2-3 streams where the scalar model says 4?

The scalar model treats every antenna as sampling every mode perfectly. Real elements are polarised, so a mode
whose electric field is perpendicular to an element contributes nothing to it - which REMOVES degrees of freedom.

    python3 scripts/polarisation.py

FALSIFIER, stated before the run: if polarisation leaves the stream count unchanged at 20 dB, it is not the
missing physics and the ceiling has another cause (pattern, mutual coupling, loss). If it lowers the count to
the 2-3 that practice reports, polarisation is the leading term.

CAVEAT, found on the first run and kept: with every antenna at mid-height the vertical (Ez) coupling nearly
vanishes, because TM_mnp's Ez carries a factor cos(p pi z/d) that is zero at z = d/2 for odd p. That is a GEOMETRY
artefact, not a polarisation result - the same mid-plane trap that made the first identifiability run return
zero. The table therefore reports several heights, and no single row is a result.
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402

A, B, D = 3.0, 4.0, 2.5
F = 5.18e9
V = (0.0, 0.0, 1.0)
H = (1.0, 0.0, 0.0)


def lattice(n, zfrac):
    return [(A * (0.2 + 0.6 * i / max(n - 1, 1)), B * (0.2 + 0.6 * j / max(n - 1, 1)), zfrac * D)
            for i, j in zip(range(n), reversed(range(n)))]


def mirrored(tx, zfrac):
    return [((A - x) * 0.8 + 0.1 * A, (B - y) * 0.8 + 0.1 * B, min(D - 0.15, zfrac * D))
            for (x, y, _z) in tx]


def random_pol(rng):
    th, ph = rng.uniform(0, 2 * math.pi), rng.uniform(0, math.pi)
    return (math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph))


def main() -> int:
    rng = random.Random(5)
    print("=" * 96)
    print(f"polarisation vs stream count — {A} x {B} x {D} m, {F/1e9:.2f} GHz, 20 dB")
    print("falsifier: unchanged stream count at 20 dB means polarisation is NOT the missing physics")
    print("=" * 96)
    print(f"{'antennas':>8} {'z frac':>7} {'vertical':>9} {'horizontal':>11} {'random':>7} {'scalar':>7}")
    for n in (3, 4):
        for zf in (0.5, 0.75, 0.9):
            tx = lattice(n, zf)
            rx = mirrored(tx, zf)
            v = E.streams(E.channel_matrix_polarised(A, B, D, F, tx, rx, [V] * n, [V] * n), 20.0)
            h = E.streams(E.channel_matrix_polarised(A, B, D, F, tx, rx, [H] * n, [H] * n), 20.0)
            rp = E.streams(E.channel_matrix_polarised(
                A, B, D, F, tx, rx, [random_pol(rng) for _ in range(n)], [random_pol(rng) for _ in range(n)]), 20.0)
            sc = E.streams(E.channel_matrix(A, B, D, F, tx, rx), 20.0)
            print(f"{n}x{n:<6} {zf:>7.2f} {v:>9} {h:>11} {rp:>7} {sc:>7}")
    print("\nReading: the SCALAR column is the ceiling. The polarised columns are what a real element gets.")
    print("The z-fraction rows exist because vertical coupling vanishes at mid-height (cos(p pi/2) = 0 at z=d/2")
    print("for odd p) - a geometry artefact, so a single height is not a result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
