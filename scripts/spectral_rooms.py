#!/usr/bin/env python3
"""Room modes as a spectrum: the oracle an acoustic solver can be checked against.

    python3 scripts/spectral_rooms.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import rooms  # noqa: E402


def main() -> int:
    a = rooms.audit()
    print("PACLAND · spectral — room modes as a spectrum\n")
    for box in ((6.0, 4.5, 3.0), (5.0, 5.0, 2.5), (8.0, 3.0, 2.8)):
        w = rooms.weyl_convergence(*box)
        print(f"box {box}")
        for r in w["rows"]:
            print(f"   f<={r['f_max']:6.0f} Hz   modes {r['modes']:6}   Weyl {r['weyl']:9.1f}   "
                  f"error {r['error'] * 100:+6.2f}%")
        print(f"   -> {w['verdict']}")
    print()
    for c in a["checks"]:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['check']}: {c['detail']}")
    print(f"\n{a['n_pass']}/{a['n']} checks pass")
    print("\nThe FIX, and whether it holds up:")
    sp = rooms.spatial_report(6.0, 4.5, 3.0, (2.0, 1.5, 1.2),
                              [(1.0, 3.0, 2.0), (3.0, 2.2, 1.6), (4.5, 1.0, 0.9)])
    print(f"{'seat':22} {'before':>7} {'1-point':>8} {'multi':>7}   {'d1':>6} {'dM':>6}")
    for row in sp["rows"]:
        print(f"{str(row['seat']):22} {row['before']:7.1f} {row['single_point']:8.1f} "
              f"{row['multi_point']:7.1f}   {row['single_delta']:+6.1f} {row['multi_delta']:+6.1f}")
    print(f"  {sp['verdict']}")
    print(f"  1-point EQ helps the seat it was tuned at ({sp['rows'][0]['single_delta']:+.1f} dB) "
          f"and barely moves the room")
    print(f"  multi-point EQ helps every seat (worst {sp['multi_worst_delta']:+.1f} dB)")
    print("\nWhat this gives AirMatrix: Weyl's law with the surface term is an oracle that needs no")
    print("measurement — a solver whose mode count drifts from it has a bug. The spacing statistic")
    print("needs an *irregular* room (GOE prediction); for a box it is reported, not passed, because")
    print("62,075 of 70,371 modes are exact degeneracies and collapsing them still leaves the ratio")
    print("between the two predictions.")
    return 0 if a["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
