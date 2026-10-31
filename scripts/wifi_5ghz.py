"""The engine pointed at 5 GHz WiFi: how many streams can a room actually carry?

5 GHz WiFi is the case where the mode count stops being interesting and the *identifiability* starts. A room
at 5 GHz holds millions of modes, so "how many modes" answers nothing. The question a link faces is:

    with N transmit and N receive antennas over an 80 MHz channel at a given SNR,
    how many INDEPENDENT STREAMS does this room support?

That is the singular-value spectrum of the modal channel matrix, and it is the same Fisher-information
question this engine already answers for acoustics and for cavity identification - asked about a MIMO matrix
instead of mode amplitudes.

Validation target, from practice: a 4x4 link in a normal room carries 2-3 streams, not 4. If the engine
says 2-3 at a realistic SNR, it is measuring something real.

    python3 scripts/wifi_5ghz.py
"""
import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np  # noqa: E402

from pacland.spectral import em_modes as E  # noqa: E402

ROOM = (3.0, 4.0, 2.5)
F_CARRIER = 5.18e9
CHANNEL_BW = 80e6
Q_ROOM = 200.0        # a normal furnished room is lossy; 200 is a generous, stated value


def channel_matrix(a, b, d, f, n_tx, n_rx, q=Q_ROOM):
    """H[rx, tx] at one subcarrier, from the room's own modes."""
    lo, hi = f - 1.0e9, f + 1.0e9
    modes = [(f0, idx) for f0, _, idx in E.cavity_modes(a, b, d, hi) if f0 >= lo]
    seen, chosen = set(), []
    for f0, idx in modes:
        key = round(f0, 3)
        if key in seen:
            continue
        seen.add(key)
        chosen.append((f0, idx))
    chosen = chosen[:120]

    def shape(idx, x, y, z):
        m, n, p = idx
        return (math.sin(m * math.pi * x / a) * math.sin(n * math.pi * y / b)
                * math.sin(p * math.pi * z / d))

    tx = [(a * (0.2 + 0.6 * i / max(n_tx - 1, 1)), b * (0.2 + 0.6 * j / max(n_tx - 1, 1)), d * 0.5)
          for i, j in zip(range(n_tx), reversed(range(n_tx)))]
    rx = [(a * (0.25 + 0.5 * i / max(n_rx - 1, 1)), b * (0.75 - 0.5 * j / max(n_rx - 1, 1)), d * 0.5)
          for i, j in zip(range(n_rx), reversed(range(n_rx)))]
    h = np.zeros((n_rx, n_tx), dtype=complex)
    for t, (xt, yt, zt) in enumerate(tx):
        for r, (xr, yr, zr) in enumerate(rx):
            acc = 0j
            for f0, idx in chosen:
                w0, w = 2 * math.pi * f0, 2 * math.pi * f
                acc += shape(idx, xt, yt, zt) * shape(idx, xr, yr, zr) / complex(w0 * w0 - w * w, w0 * w / q)
            h[r, t] = acc
    return h, len(chosen), len(seen)


def streams_at(h, snr_db):
    """How many singular values of H clear the noise floor."""
    sv = np.linalg.svd(h, compute_uv=False)
    if sv[0] == 0:
        return 0, sv
    snr = 10 ** (snr_db / 10.0)
    normed = sv / sv[0]
    return int((normed ** 2 * snr > 1.0).sum()), sv


def main() -> int:
    a, b, d = ROOM
    print("=" * 96)
    print(f"5 GHz WiFi in a {a} x {b} x {d} m room, {CHANNEL_BW/1e6:.0f} MHz channel")
    print("=" * 96)

    v = a * b * d
    s = 2 * (a * b + b * d + a * d)
    n_hi = E.exact_count(a, b, d, F_CARRIER + CHANNEL_BW / 2)
    n_lo = E.exact_count(a, b, d, F_CARRIER - CHANNEL_BW / 2)
    weyl = E.weyl_count(F_CARRIER, v, s) - E.weyl_count(F_CARRIER - CHANNEL_BW, v, s)
    print(f"modes in the channel        {n_hi - n_lo:,}   (Weyl estimate {weyl:,.0f})")
    print(f"wavelength                  {E.C_LIGHT/F_CARRIER*100:.1f} cm  -> the room is "
          f"{a/(E.C_LIGHT/F_CARRIER):.0f} x {b/(E.C_LIGHT/F_CARRIER):.0f} x "
          f"{d/(E.C_LIGHT/F_CARRIER):.0f} wavelengths")

    print("\nstreams vs antennas (room modes only, Q = " + f"{Q_ROOM:.0f})")
    print(f"{'antennas':>8} " + " ".join(f"{snr:>10}" for snr in ("10 dB", "20 dB", "30 dB")))
    for n in (2, 3, 4):
        h, used, distinct = channel_matrix(a, b, d, F_CARRIER, n, n)
        cells = []
        for snr_db in (10, 20, 30):
            k, _ = streams_at(h, snr_db)
            cells.append(f"{k} of {n}")
        print(f"{n:>8} " + " ".join(f"{c:>10}" for c in cells))

    print("\nValidation target from practice: a 4x4 link in a normal room carries 2-3 streams, not 4.")
    print("If the table shows 2-3 at 20 dB, the engine is measuring something real.")
    print("\nWhat this is: modes and a singular-value spectrum computed from the room's own field.")
    print("What it is not: a channel model with scattering, furniture or people - those ADD degrees of")
    print("freedom, so this is a LOWER bound on usable streams for a given antenna count.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
