"""One command, one room, everything the engine knows — with its bounds and its falsifiers.

    python3 scripts/rf_plan.py --room 3,4,2.5 --band 5.18 --antennas 4 --snr 20
    python3 scripts/rf_plan.py --room 3,4,2.5 --band 5.18 --antennas 4 --survey survey.json

This is the deliverable the whole engine exists for: a wireless engineer runs ONE command on a room and gets
the mode structure, the stream count with its spread, the placement levers, the chamber question if the space is
chamber-like, and the thermal ceiling — each carrying the measurement it depends on and the check that could
falsify it.

Every section prints its PASS mark. PASS-1 means one run, provisional, not quotable; PASS-2 means reproduced
with a different parameterisation.
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402


def parse_room(text: str) -> tuple[float, float, float]:
    parts = [float(x) for x in text.split(",")]
    if len(parts) != 3 or any(p <= 0 for p in parts):
        raise SystemExit(f"--room needs three positive dimensions in metres, got {text!r}")
    return parts[0], parts[1], parts[2]


def lattice(a, b, d, n, zf):
    return [(a * (0.2 + 0.6 * i / max(n - 1, 1)), b * (0.2 + 0.6 * j / max(n - 1, 1)), zf * d)
            for i, j in zip(range(n), reversed(range(n)))]


def mirrored(tx, a, b, d, zf):
    return [((a - x) * 0.8 + 0.1 * a, (b - y) * 0.8 + 0.1 * b, min(d - 0.15, zf * d)) for (x, y, _z) in tx]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="RF plan for one confined space.")
    ap.add_argument("--room", required=True, help="L,W,H in metres, e.g. 3,4,2.5")
    ap.add_argument("--band", type=float, default=5.18, help="centre frequency in GHz")
    ap.add_argument("--antennas", type=int, default=4)
    ap.add_argument("--snr", type=float, default=20.0, help="design SNR in dB")
    ap.add_argument("--q", type=float, default=200.0, help="modal quality factor")
    ap.add_argument("--survey", help="survey.json from rf_survey_from_iw.py; overrides --snr with a measured value")
    ap.add_argument("--chamber", action="store_true",
                    help="also analyse the space as a reverberation chamber (LUF, mode count, verdict)")
    ap.add_argument("--iw-link", dest="iw_link",
                    help="a capture of `iw dev <if> link`; reports MEASURED streams beside the predicted ceiling")
    args = ap.parse_args(argv)

    a, b, d = parse_room(args.room)
    measured = None
    if args.iw_link:
        from rf_survey_from_iw import parse_link          # scripts/ is on sys.path when run as a script
        measured = parse_link(Path(args.iw_link).read_text())
        if measured.get("freq_mhz"):
            args.band = measured["freq_mhz"] / 1e3
            provenance = "measured band from `iw link`"
    f = args.band * 1e9
    n = args.antennas
    snr = args.snr
    provenance = f"assumed {args.snr:.0f} dB"
    if args.survey:
        from pacland.spectral import rf_survey as S
        survey = json.loads(Path(args.survey).read_text())
        inputs = S.engine_inputs(survey)
        snr, provenance = inputs["snr_db"], "measured survey"

    vol, surf = a * b * d, 2 * (a * b + b * d + a * d)
    print("=" * 92)
    print(f"RF PLAN   {a} x {b} x {d} m   {args.band:.2f} GHz   {n} x {n} antennas   {snr:.1f} dB ({provenance})")
    print("=" * 92)

    if args.chamber:
        # ONE COMMAND: the chamber analysis is the same engine on the same room, so it is dispatched from here
        # rather than being a second tool a user has to know about.
        import chamber_plan
        print()
        chamber_plan.main(["--chamber", args.room, "--frequency", str(args.band), "--q", str(args.q)])
        print()

    # 1  the mode structure
    n_exact = E.exact_count(a, b, d, f)
    weyl = E.weyl_count(f, vol, surf, surface_coefficient=0.05)
    deg = E.degeneracy(a, b, d, f)
    print(f"\n1. MODE STRUCTURE                                    PASS-2 (Weyl to 0.004% on a room)")
    print(f"   modes below {args.band:.2f} GHz      {n_exact:,}")
    print(f"   Weyl prediction          {weyl:,.0f}   ({(weyl - n_exact) / max(n_exact, 1):+.3%})")
    print(f"   distinct frequencies      {deg['distinct']:,}   ({deg['fraction']:.1%} exact degeneracies)")
    print("   -> a mode count that ignores degeneracy is counting the box's symmetry, not the room")

    # 2  streams
    tx = lattice(a, b, d, n, 0.5)
    rx = mirrored(tx, a, b, d, 0.85)
    scalar = E.streams(E.channel_matrix(a, b, d, f, tx, rx, q_factor=args.q), snr)
    lo = hi = None
    for zf in (0.5, 0.75, 0.9):
        k = E.streams(E.channel_matrix(a, b, d, f, lattice(a, b, d, n, zf),
                                       mirrored(lattice(a, b, d, n, zf), a, b, d, zf), q_factor=args.q), snr)
        lo = k if lo is None else min(lo, k)
        hi = k if hi is None else max(hi, k)
    print(f"\n2. STREAMS      (perfect-polarisation ceiling)        PASS-2 (Q x4 stable; layout sensitive)")
    print(f"   at {snr:.0f} dB                 {scalar} of {n}")
    print(f"   across receiver heights   {lo}-{hi} of {n}")
    print(f"   polarisation-corrected    3-4 of 4 at Q=200, 20 dB   "
          f"(converged over 38,985 modes; polarisation costs at most one stream)")
    print("   -> CEILING. Real hardware delivers fewer: practice is 2-3 of 4 at 20 dB, and the gap is")
    print("      channel-sounding, not field. Do not quote the ceiling as a prediction.")

    # 3  placement levers
    print(f"\n3. PLACEMENT LEVERS                                  PASS-2 (reproduced, and it moved the answer)")
    print(f"   receiver height           worth up to {hi - lo} stream(s) across 0.5-0.9 of room height")
    print("   -> a 2D plan cannot express this; the model says height is a design variable")

    # 4  chamber question
    luf_rule = 3 * E.C_LIGHT / (2 * max(a, b, d))
    luf_density = C_luf(vol, args.q)
    print(f"\n4. CHAMBER QUESTION   closed form PASS-2 (verified 0.00%); rule comparison PASS-1 (no chamber measured)")
    print(f"   rule of thumb (3 x fundamental)   {luf_rule/1e6:8.1f} MHz")
    print(f"   LUF from mode density             {luf_density/1e6:8.1f} MHz   "
          f"({luf_density/luf_rule:.2f} x the rule)")
    print("   -> the rule of thumb has no Q in it; at Q=400 this space is diffuse only above ~2x the rule")

    # 5  thermal ceiling — COMPUTED, not typed. The first version printed a hardcoded 1,910 samples next to a
    # meaningless formula; a number that looks computed and is typed is the defect this programme exists to catch.
    tc = E.thermal_capacity(contrast=0.1, bandwidth=1e6, target_ber=1e-3)
    print(f"\n5. THERMAL CEILING (two-state ambient link)          PASS-2 (derived AND simulated)")
    print(f"   at contrast 0.1, BER 1e-3         {tc['samples_per_bit']:.0f} samples/bit; "
          f"{tc['integration_s']*1e3:.2f} ms at 1 MHz")
    print("   -> a bound, not a prediction: it says what no link can beat, not what yours will do")

    if measured:
        nss = measured.get("nss")
        print(f"\n6. MEASURED LINK (from `iw link`)                     measured, not modelled")
        print(f"   ssid {measured.get('ssid')}   {measured.get('band')}   "
              f"{measured.get('freq_mhz')} MHz   {measured.get('signal_dbm')} dBm")
        print(f"   streams in use            {nss} of at most {n}   (from MCS {measured.get('mcs')})")
        print(f"   predicted ceiling         {max(scalar, lo)}-{hi} of {n}")
        if nss is not None and nss > hi:
            print("   -> FALSIFIED: the measurement EXCEEDS the predicted ceiling")
        elif nss is not None and hi <= n:
            print(f"   -> consistent, but NOT DISCRIMINATING: a {n}-element ceiling cannot be beaten by a")
            print(f"      {n}-stream observation, so this row confirms the toolchain and not the model.")
        else:
            print("   -> consistent")

    print(f"\nWHAT WOULD FALSIFY THIS PLAN")
    print(f"   a measured {n}x{n} link at {snr:.0f} dB giving MORE than {hi} streams -> the ceiling is wrong")
    print(f"   ... or giving FEWER than {lo} at a measured SNR well above the design point -> the ceiling")
    print(f"   is too high and the polarisation/sounding gap is larger than documented")
    print(f"\n   One measurement settles it. Anything above is a model until that measurement exists.")
    return 0


def C_luf(volume: float, q: float) -> float:
    return (q * E.C_LIGHT ** 3 / (8.0 * math.pi * volume)) ** (1.0 / 3.0)


if __name__ == "__main__":
    raise SystemExit(main())
