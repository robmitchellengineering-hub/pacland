"""Reverberation-chamber analysis — the one confined space where the peak-based mode test is valid.

A reverberation chamber is judged on its modes: below a certain frequency it is *under-moded*, the field is not
statistically uniform, and a test result from it carries an unbounded error. Above it, the field is diffuse and
the chamber can be used. That boundary — the lowest usable frequency — is a mode-counting question, which is
exactly what this engine computes.

    python3 scripts/chamber.py [L W H] [f_max_GHz]

Two LUF estimates are reported, because there are two in practice and they disagree:

    f0 = c / (2 * largest dimension)      the fundamental
    LUF_rule = 3 f0                        the common rule of thumb (a heuristic, stated as such)
    LUF_density: the first frequency where the mode count in a 1/Q-wide window is >= 1,
                 i.e. where modes OVERLAP so the field is diffuse rather than a set of isolated resonances

FALSIFIER, stated before the run: if LUF_density is far below 3 f0 for a normal chamber, the rule of thumb is
conservative and chambers are being specified larger than they need to be. If it is far above, the rule is
optimistic and measurements below LUF_density were taken in a field that was never diffuse.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402


def fundamental(a: float, b: float, d: float, c: float = E.C_LIGHT) -> float:
    return c / (2.0 * max(a, b, d))


def mode_density_per_hz(f: float, volume: float, c: float = E.C_LIGHT) -> float:
    """dN/df from the Weyl volume term: 8 pi f^2 V / c^3 (two polarisations)."""
    return 8.0 * math.pi * f * f * volume / c ** 3


def luf_density(volume: float, q_factor: float, f_lo: float, f_hi: float,
                c: float = E.C_LIGHT) -> float:
    """First frequency where modes overlap: density * modal width >= 1.

    A mode has width ~ f/Q. The field is diffuse when at least one other mode sits inside that width, i.e.
    `density(f) * f/Q >= 1`. Below that, the chamber is a set of isolated resonances and the field is not
    uniform - which is exactly what "under-moded" means.
    """
    lo, hi = f_lo, f_hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mode_density_per_hz(mid, volume, c) * mid / q_factor >= 1.0:
            hi = mid
        else:
            lo = mid
    return hi


def luf_closed_form(volume: float, q_factor: float, c: float = E.C_LIGHT) -> float:
    """LUF in closed form: where the mode density times the modal width equals one.

    Setting `density(f) * f/Q = 1` with `density(f) = 8 pi f^2 V / c^3`:

        8 pi f^3 V / (Q c^3) = 1      ->      f = ( Q c^3 / (8 pi V) )^(1/3)

    So **LUF ~ (Q/V)^(1/3)**: the cube root of the quality factor over the volume. Doubling Q raises the usable
    frequency by 26%, not by 100%; doubling the volume lowers it by 21%. That is a scaling law, and the
    bisection in `luf_density` should agree with it to numerical precision - which is the test.
    """
    return (q_factor * c ** 3 / (8.0 * math.pi * volume)) ** (1.0 / 3.0)


def analyse(a: float, b: float, d: float, f_max: float, q_factor: float = 200.0,
            c: float = E.C_LIGHT) -> dict:
    volume = a * b * d
    surface = 2.0 * (a * b + b * d + a * d)
    f0 = fundamental(a, b, d, c)
    luf_r = 3.0 * f0
    luf_d = luf_density(volume, q_factor, 1e6, f_max, c)
    n_exact = E.exact_count(a, b, d, f_max, c)
    weyl = E.weyl_count(f_max, volume, surface, c, surface_coefficient=0.05)
    deg = E.degeneracy(a, b, d, f_max, c)
    # modes in a 1/Q window at the top of the band: is the field diffuse up there?
    width = f_max / q_factor
    n_window = E.exact_count(a, b, d, f_max, c) - E.exact_count(a, b, d, f_max - width, c)
    return {"dimensions": (a, b, d), "volume": volume, "surface": surface, "q_factor": q_factor,
            "fundamental_hz": f0, "luf_rule_hz": luf_r, "luf_density_hz": luf_d,
            "luf_ratio": luf_d / luf_r if luf_r else float("inf"),
            "modes_to_f_max": n_exact, "weyl": weyl,
            "weyl_error": (weyl - n_exact) / max(n_exact, 1),
            "distinct": deg["distinct"], "degenerate_fraction": deg["fraction"],
            "modes_in_one_modal_width_at_f_max": n_window}


def main(argv) -> int:
    a, b, d = ([float(x) for x in argv[1].split(",")] if len(argv) > 1 else [3.0, 2.5, 2.2])
    f_max = (float(argv[2]) if len(argv) > 2 else 1.0) * 1e9
    for q in (100.0, 200.0, 400.0):
        r = analyse(a, b, d, f_max, q)
        print("=" * 92)
        print(f"chamber {a} x {b} x {d} m   (V = {r['volume']:.2f} m3, S = {r['surface']:.1f} m2), "
              f"band to {f_max/1e9:.1f} GHz, Q = {q:.0f}")
        print(f"  fundamental            {r['fundamental_hz']/1e6:8.1f} MHz")
        print(f"  LUF, rule of thumb     {r['luf_rule_hz']/1e6:8.1f} MHz   (3 x fundamental - a heuristic)")
        print(f"  LUF, mode density      {r['luf_density_hz']/1e6:8.1f} MHz   "
              f"({r['luf_ratio']:.2f} x the rule of thumb)")
        print(f"  modes to f_max         {r['modes_to_f_max']:8d}   Weyl {r['weyl']:.0f} "
              f"({r['weyl_error']:+.2%})")
        print(f"  distinct frequencies   {r['distinct']:8d}   ({r['degenerate_fraction']:.1%} degenerate)")
        print(f"  modes within one modal width at f_max {r['modes_in_one_modal_width_at_f_max']:d} "
              f"({'diffuse' if r['modes_in_one_modal_width_at_f_max'] > 1 else 'NOT diffuse'})")
    print("\nWhat this is: mode count, spacing and the two LUF estimates, computed from the chamber's")
    print("dimensions. What it is not: a field-uniformity measurement - that needs the chamber.")
    print("The falsifier: if LUF_density sits far from 3 x fundamental, one of the two numbers is wrong")
    print("and the specification built on it is wrong with it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
