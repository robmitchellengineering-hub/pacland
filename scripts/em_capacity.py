"""The electromagnetic twin of the room analysis: mode count, statistics, identifiability, and the
thermal-noise ceiling for confined spaces.

    python3 scripts/em_capacity.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402
from pacland.spectral import zeros as Z  # noqa: E402

GEOMETRIES = [
    ("metal cabinet", 0.5, 0.5, 0.5, 3e9),
    ("small room", 3.0, 4.0, 2.5, 3e9),
    ("implant-scale phantom", 0.10, 0.10, 0.20, 3e9),
]


def main() -> int:
    print("=" * 104)
    print("EM mode capacity — the same engine as the room work, with c instead of sound speed")
    print("=" * 104)
    for name, a, b, d, f_max in GEOMETRIES:
        n = E.exact_count(a, b, d, f_max)
        v, s = a * b * d, 2 * (a * b + b * d + a * d)
        fit = E.fit_surface_coefficient(a, b, d, f_max)["surface_coefficient"]
        weyl = E.weyl_count(f_max, v, s, surface_coefficient=fit)
        err = (weyl - n) / max(n, 1)
        deg = E.degeneracy(a, b, d, f_max)
        print(f"\n{name}  ({a} x {b} x {d} m, to {f_max/1e9:.0f} GHz)")
        print(f"  exact modes                 {n}")
        print(f"  distinct frequencies        {deg['distinct']}  ({deg['fraction']:.1%} are exact degeneracies)")
        print(f"  Weyl fit surface coefficient {fit:+.4f}")
        print(f"  Weyl count                  {weyl:.1f}   error {err:+.3%}")
        modes = [f for f, _, _ in E.cavity_modes(a, b, d, f_max)]
        if len(modes) > 20:
            sp = Z.unfolded_spacings(sorted(set(modes)))
            r = Z.ratio_statistic(sp)
            gue = Z.gue_control(len(sp))
            print(f"  ratio statistic             {r:.4f}  (GUE control {gue['mean']:.4f}, "
                  f"Poisson {Z.poisson_ratio():.4f})")
        for mics in (2, 3):
            u = E.usable_modes(a, b, d, f_max * 0.4, f_max, mics, -60.0)
            print(f"  usable modes @-60 dB, {mics} probes  {u['usable_10pct']} of {u['cap']} "
                  f"(at 25%: {u['usable_25pct']})")
        tc = E.thermal_capacity(contrast=0.1, bandwidth=1e6)
        print(f"  thermal ceiling (eta=0.1, 1 MHz)  {tc['samples_per_bit']:.0f} samples/bit, "
              f"tau = {tc['integration_s']*1e3:.2f} ms")
    print("\nWhat this is: a design table for a space BEFORE anyone runs a full-wave solver.")
    print("What it is not: a simulation. It is the exact mode structure plus the bounds that follow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
