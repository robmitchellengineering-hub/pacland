"""Chamber analysis as one command: is this chamber usable at this frequency, and by how much?

    python3 scripts/chamber_plan.py --chamber 3,2.5,2.2 --frequency 0.3 --q 200
    python3 scripts/chamber_plan.py --chamber 6,4,3 --frequency 0.2 --q 400 --ber 0.01

The engine answers a question a test house already asks — *is the chamber over-moded here* — but answers it from
the chamber's own dimensions and its measured Q, instead of from a rule of thumb that ignores Q.

FALSIFIER, stated before the run: if the chamber is declared usable and a field-uniformity measurement at that
frequency shows unacceptable uniformity, the criterion is too loose. If it is declared unusable and the measured
uniformity is fine, the criterion is too strict. Either way the verdict is checkable in one measurement.
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402


def luf_rule(a, b, d):
    return 3.0 * E.C_LIGHT / (2.0 * max(a, b, d))


def luf_density(volume, q):
    """The closed form — exact for the Weyl DENSITY, but only valid where Weyl itself is."""
    return (q * E.C_LIGHT ** 3 / (8.0 * math.pi * volume)) ** (1.0 / 3.0)


def modes_in_window(a, b, d, f, q) -> int:
    """How many real modes sit inside one modal width at f. The ground truth for 'is it diffuse'."""
    width = f / q
    return E.exact_count(a, b, d, f) - E.exact_count(a, b, d, max(f - width, 1.0))


def luf_exact(a, b, d, q, n_needed: int = 2, steps: int = 160):
    """The LUF by COUNTING: the lowest frequency above which a 1/Q window always holds `n_needed` modes.

    A bisection is NOT valid here: the window count is not monotonic in f, because different frequencies sample
    different degenerate mode clusters. The first version bisected and returned 290 MHz for a chamber whose window
    at 300 MHz holds ZERO modes - the tool then printed 'USABLE' beside 'NOT diffuse'. So this SCANS upward and
    remembers the last frequency that FAILED, which is robust to the clusters.
    """
    f0 = E.C_LIGHT / (2.0 * max(a, b, d))
    lo = max(f0 * 1.01, 1.0e5)
    hi = max(lo * 3.0, luf_density(a * b * d, q) * 6.0)
    last_fail = lo
    for i in range(steps):
        f = lo * (hi / lo) ** (i / (steps - 1))
        if modes_in_window(a, b, d, f, q) < n_needed:
            last_fail = f
    return last_fail


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Chamber usability at a frequency.")
    ap.add_argument("--chamber", required=True, help="L,W,H in metres")
    ap.add_argument("--frequency", type=float, required=True, help="frequency to assess, in GHz")
    ap.add_argument("--q", type=float, default=200.0, help="measured modal quality factor")
    args = ap.parse_args(argv)

    dims = [float(x) for x in args.chamber.split(",")]
    if len(dims) != 3 or any(x <= 0 for x in dims):
        raise SystemExit("--chamber needs three positive dimensions in metres")
    a, b, d = dims
    f = args.frequency * 1e9
    vol = a * b * d
    surf = 2 * (a * b + b * d + a * d)

    n_exact = E.exact_count(a, b, d, f)
    weyl = E.weyl_count(f, vol, surf, surface_coefficient=0.05)
    deg = E.degeneracy(a, b, d, f)
    rule = luf_rule(a, b, d)
    dens = luf_density(vol, args.q)
    width = f / args.q
    in_window = n_exact - E.exact_count(a, b, d, max(f - width, 1.0))

    print("=" * 84)
    print(f"CHAMBER   {a} x {b} x {d} m   V = {vol:.2f} m3   S = {surf:.1f} m2   Q = {args.q:.0f}")
    print(f"          assessed at {args.frequency:.3f} GHz")
    print("=" * 84)
    print(f"  fundamental c/(2 Lmax)        {E.C_LIGHT/(2*max(a,b,d))/1e6:8.1f} MHz")
    print(f"  modes below the frequency     {n_exact:8d}   Weyl {weyl:,.0f} ({(weyl-n_exact)/max(n_exact,1):+.2%})")
    print(f"  distinct frequencies          {deg['distinct']:8d}   ({deg['fraction']:.1%} degenerate)")
    print(f"  modal width at this Q         {width/1e6:8.2f} MHz")
    print(f"  modes inside one width        {in_window:8d}"
          + ("   -> diffuse" if in_window > 1 else "   -> NOT diffuse"))
    print()
    exact_luf = luf_exact(a, b, d, args.q)
    print(f"  LUF by rule of thumb          {rule/1e6:8.1f} MHz")
    print(f"  LUF by closed form (Weyl)     {dens/1e6:8.1f} MHz   ({dens/rule:.2f}x the rule)")
    print(f"  LUF by exact mode count       {exact_luf/1e6:8.1f} MHz   ({exact_luf/rule:.2f}x the rule)")
    if abs(exact_luf - dens) / max(dens, 1.0) > 0.05:
        print(f"  -> the closed form DISAGREES with the count by "
              f"{(dens-exact_luf)/max(exact_luf,1.0):+.0%}; at this mode count Weyl's density overestimates")
        print("     and the COUNT is the ground truth. The verdict below uses the count.")
    dens = exact_luf
    print()
    if in_window >= 2:
        head = f / dens if dens else float("inf")
        print(f"  VERDICT: USABLE at {args.frequency:.3f} GHz — {head:.2f}x the exact LUF, "
              f"{in_window} modes inside one modal width")
    elif f >= rule:
        print(f"  VERDICT: MARGINAL at {args.frequency:.3f} GHz — above the rule of thumb "
              f"({rule/1e6:.1f} MHz) but BELOW the mode-density LUF ({dens/1e6:.1f} MHz)")
        print("           the rule would pass this chamber here; the criterion this engine uses would not.")
    else:
        print(f"  VERDICT: UNUSABLE at {args.frequency:.3f} GHz — below both LUF estimates")
    print()
    print("  FALSIFIER: if a measured field-uniformity run at this frequency is acceptable while this says")
    print("  MARGINAL or UNUSABLE, the criterion is too strict. If uniformity is unacceptable while this says")
    print("  USABLE, it is too loose. One uniformity-versus-frequency measurement settles it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
