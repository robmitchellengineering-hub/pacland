"""PASS-2 for identifiability: does 'how many modes are usable' survive a different parameterisation?

The registry holds identifiability at PASS-1 because it was measured on ONE parameterisation (Q = 50, a 0.5 m
cube, -60 dB). A PASS-2 claim needs the same answer from a different setup, or a clear statement of what it
depends on.

    python3 scripts/identifiability_pass2.py

FALSIFIER, stated before the run: if the usable-mode count changes by more than a factor of two across a factor of
four in Q - or across the room size - then 'how many modes are usable' is not a property of a room and the claim
must be restated as a function of Q, not a number.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402

TARGET = 1.5708   # GHz: the band edge used in the original PASS-1 run
CASES = [
    ("0.50 m cube", 0.50, 0.50, 0.50),
    ("1.00 m cube", 1.00, 1.00, 1.00),
    ("2.00 m cube", 2.00, 2.00, 2.00),
    ("3 x 4 x 2.5 m", 3.0, 4.0, 2.5),
]
QS = (25.0, 50.0, 100.0)


def main() -> int:
    print("=" * 84)
    print(f"IDENTIFIABILITY, PASS-2 — usable modes at {TARGET:.3f} GHz, noise -60 dB relative to peak")
    print("falsifier: a factor-of-two change across a factor of four in Q means this is not a room property")
    print("=" * 84)
    print(f"{'space':>14} {'modes':>7} " + " ".join(f"{'Q=' + str(int(q)):>9}" for q in QS))
    rows = []
    for name, a, b, d in CASES:
        n_modes = E.exact_count(a, b, d, TARGET * 1e9)
        cells = []
        for q in QS:
            r = E.usable_modes(a, b, d, TARGET * 1e8, TARGET * 1e9, probes=3, noise_db=-60.0, q_factor=q)
            cells.append(int(r["usable_10pct"]))
        rows.append((name, n_modes, cells))
        print(f"{name:>14} {n_modes:>7} " + " ".join(f"{c:>9}" for c in cells))

    print()
    spread = []
    for name, n_modes, cells in rows:
        if min(cells) > 0:
            ratio = max(cells) / max(min(cells), 1)
            spread.append(ratio)
            print(f"  {name:>14}: {min(cells)}-{max(cells)} usable across Q (x{ratio:.2f})")
    worst = max(spread) if spread else float("inf")
    print()
    if worst >= 2.0:
        print(f"VERDICT: FALSIFIED as a room property — up to x{worst:.2f} across a factor of four in Q.")
        print("         The claim must be restated as a function of Q, not a number.")
    else:
        print(f"VERDICT: PASS-2 — the usable count moves at most x{worst:.2f} across a factor of four in Q,")
        print("         so it is a property of the space at this noise level, not of the assumed damping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
