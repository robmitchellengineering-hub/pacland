"""WiFi planning: where to put the antennas, and how many streams you get.

    python3 scripts/wifi_plan.py [L W H] [GHz] [n_antennas] [snr_db]

The engine already answers "how many streams does this room carry". A planning tool answers the question an
installer actually has: **where**, and does it matter?

FALSIFIER, stated before the run: if a random search over placements finds no better configuration than a
regular lattice, then at this geometry and SNR placement is not a design variable and the tool should say so
rather than manufacture an optimum.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402

GRID = 0.15   # metres: no antenna closer to a wall than this


def lattice(a, b, d, n):
    """A regular placement — the baseline an installer would use without thinking."""
    return [(a * (0.2 + 0.6 * i / max(n - 1, 1)), b * (0.2 + 0.6 * j / max(n - 1, 1)), d * 0.5)
            for i, j in zip(range(n), reversed(range(n)))]


def random_placement(a, b, d, n, rng):
    return [(rng.uniform(GRID, a - GRID), rng.uniform(GRID, b - GRID),
             rng.uniform(GRID, d - GRID)) for _ in range(n)]


def rx_of(tx, a, b, d):
    """Receive positions, mirrored and raised: NEVER co-located with the transmitters.

    The first version placed tx and rx at the same points, which makes the channel matrix symmetric. A
    symmetric matrix has a degenerate singular-value structure that flatters its rank, and the planner duly
    reported 4 of 4 streams where the two-lattice version of the same room reported 3 of 4.
    """
    return [((a - x) * 0.8 + 0.1 * a, (b - y) * 0.8 + 0.1 * b,
             min(d - GRID, z + 0.35 * d)) for (x, y, z) in tx]


def main(argv):
    a, b, d = ([float(x) for x in argv[1].split(",")] if len(argv) > 1 else [3.0, 4.0, 2.5])
    f_ghz = float(argv[2]) if len(argv) > 2 else 5.18
    n = int(argv[3]) if len(argv) > 3 else 4
    snr_db = float(argv[4]) if len(argv) > 4 else 20.0
    f = f_ghz * 1e9
    rng = random.Random(7)

    print("=" * 92)
    print(f"WiFi plan — {a} x {b} x {d} m, {f_ghz:.2f} GHz, {n} x {n} antennas, {snr_db:.0f} dB")
    print("=" * 92)

    base = lattice(a, b, d, n)
    h_base = E.channel_matrix(a, b, d, f, base, rx_of(base, a, b, d))
    s_base = E.streams(h_base, snr_db)
    print(f"regular lattice:      {s_base} of {n} streams")
    print("  positions: " + " ".join(f"({x:.2f},{y:.2f},{z:.2f})" for x, y, z in base))

    best_s, best_pos = s_base, base
    tries = 40
    for _ in range(tries):
        pos = random_placement(a, b, d, n, rng)
        try:
            s = E.streams(E.channel_matrix(a, b, d, f, pos, rx_of(pos, a, b, d)), snr_db)
        except Exception:
            continue
        if s > best_s:
            best_s, best_pos = s, pos
    print(f"\nsearched placement:   {best_s} of {n} streams  (best of {tries} random layouts)")
    print("  positions: " + " ".join(f"({x:.2f},{y:.2f},{z:.2f})" for x, y, z in best_pos))

    if best_s == s_base:
        print(f"\nFALSIFIER FIRED: no placement beat the lattice. At {snr_db:.0f} dB in this geometry,")
        print("placement is not the lever — the room already supports what it supports. Do not sell a search.")
    else:
        gain = best_s - s_base
        print(f"\nplacement is worth +{gain} stream(s) here: {s_base} -> {best_s} of {n}.")
        print("That is the planning answer, and it is falsifiable: another layout can beat it.")
    print("\nNot modelled: furniture, people, scattering (all ADD streams, so this is a floor), and Q is")
    print("stated (200), not measured. A lower Q spreads resonances and generally helps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
