"""Compare the engine's stream prediction against MEASURED streams — the test the whole plan waits on.

The plan says, for a room and an SNR, how many streams a link supports. This takes a table of measured stream
counts at known positions and asks whether the prediction holds.

    python3 scripts/validate_streams.py --room 3,4,2.5 --band 5.18 --ap 1.5,2.0,2.4 positions.csv

`positions.csv` — one row per measurement, header required:

    x,y,z,nss,snr_db
    0.5,1.2,0.8,3,21.0
    2.6,3.4,0.8,2,18.5

FALSIFIER, stated before the run: if any measured count EXCEEDS the predicted ceiling, the model is wrong on the
low side (the ceiling is not a ceiling). If the mean shortfall is two or more streams, the model is wrong on the
high side and polarisation/sounding must be re-examined. Between those, the model is consistent with the data.

A note on what "consistent" can mean: this compares the CEILING to what hardware agreed. Hardware agreeing FEWER
than the ceiling is the expected, documented behaviour (channel sounding), so the test checks the ORDER, not the
absolute value.
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import em_modes as E  # noqa: E402


def parse_triple(text, name):
    parts = [float(x) for x in text.split(",")]
    if len(parts) != 3:
        raise SystemExit(f"--{name} needs x,y,z, got {text!r}")
    return parts[0], parts[1], parts[2]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate predicted streams against measured ones.")
    ap.add_argument("--room", required=True)
    ap.add_argument("--band", type=float, default=5.18)
    ap.add_argument("--ap", default=None, help="access-point position x,y,z (default: room centre at ceiling)")
    ap.add_argument("--q", type=float, default=200.0)
    ap.add_argument("--ap-antennas", type=int, default=4, help="AP array elements (default 4)")
    ap.add_argument("--client-antennas", type=int, default=4, help="client array elements (default 4)")
    ap.add_argument("--data", required=True)
    args = ap.parse_args(argv)

    a, b, d = [float(x) for x in args.room.split(",")]
    f = args.band * 1e9
    apx, apy, apz = parse_triple(args.ap, "ap") if args.ap else (a / 2, b / 2, min(d - 0.1, 0.95 * d))

    rows = []
    with open(args.data) as fh:
        for row in csv.DictReader(fh):
            rows.append({"pos": (float(row["x"]), float(row["y"]), float(row["z"])),
                         "nss": int(float(row["nss"])), "snr": float(row["snr_db"])})
    if not rows:
        print("REFUSED: no rows in the data file")
        return 0

    # A 1x1 link cannot carry more than one stream, so the FIRST version of this harness predicted 1 for every
    # row - it was modelling a single element, not the MIMO link the measurements come from. Both ends are now
    # arrays at half-wavelength spacing, which is what a real AP and client present.
    lam = E.C_LIGHT / f
    half = lam / 2.0

    def array(px, py, pz, n):
        return [(px + half * (i - (n - 1) / 2.0), py, pz) for i in range(n)]

    print("=" * 90)
    print(f"VALIDATION  {a} x {b} x {d} m at {args.band:.2f} GHz, AP at "
          f"({apx:.2f},{apy:.2f},{apz:.2f}), Q = {args.q:.0f}")
    print("=" * 90)
    print(f"{'#':>2} {'position':>18} {'snr dB':>7} {'nss':>4} {'predicted':>10} {'delta':>6}")
    deltas = []
    for i, r in enumerate(rows, 1):
        h = E.channel_matrix(a, b, d, f, array(apx, apy, apz, args.ap_antennas),
                             array(*r["pos"], args.client_antennas), q_factor=args.q)
        pred = E.streams(h, r["snr"])
        delta = r["nss"] - pred
        deltas.append(delta)
        print(f"{i:>2} ({r['pos'][0]:.2f},{r['pos'][1]:.2f},{r['pos'][2]:.2f})"
              f"{r['snr']:>8.1f}{r['nss']:>5}{pred:>11}{delta:>+6}")

    over = [x for x in deltas if x > 0]
    mean_short = sum(-x for x in deltas if x < 0) / max(len(deltas), 1)
    print()
    print("FALSIFIER CHECK")
    print(f"  measurements exceeding the ceiling : {len(over)}"
          + ("   <-- THE CEILING IS NOT A CEILING; the model is wrong on the low side" if over else "   (none — ceiling holds)"))
    print(f"  mean shortfall vs ceiling          : {mean_short:.2f} streams"
          + ("   <-- two or more: the model is wrong on the high side" if mean_short >= 2 else ""))
    if over:
        print("\n  VERDICT: FALSIFIED — a measurement beat the predicted ceiling.")
    elif mean_short >= 2:
        print("\n  VERDICT: FALSIFIED — hardware is two or more streams below the ceiling everywhere;")
        print("  the ceiling is too high and polarisation/sounding must be re-examined.")
    else:
        print("\n  VERDICT: CONSISTENT — no measurement beat the ceiling, and the shortfall is within the")
        print("  documented channel-sounding gap. This confirms the model's ORDER, not its absolute value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
