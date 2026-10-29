#!/usr/bin/env python3
"""Modal identifiability with a noise model: how many parameters survive real measurement noise.

    python3 scripts/spectral_rooms_crb.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import identify as I  # noqa: E402


def main() -> int:
    box = I.Box3()
    triples = box.modes_below(100.0)
    params = []
    for i, (_, _, _, _f) in enumerate(triples):
        params += [0.06, 1.0 / (1.0 + 0.1 * i)]
    grid = [(box.lx * (0.15 + 0.23 * ix), box.ly * (0.17 + 0.22 * iy), box.lz * (0.22 + 0.45 * iz))
            for ix in range(4) for iy in range(4) for iz in range(2)]
    freqs = [40.0 + 60.0 * i / 59 for i in range(60)]
    n = len(params)
    print(f"PACLAND · modal identifiability with noise\n")
    print(f"{len(triples)} modes below 100 Hz, {n} parameters, 60 frequencies per capture\n")
    print("SNR sweep, 3 microphones, complex data:")
    for noise in (1e-4, 3e-4, 1e-3, 3e-3):
        r = I.cramer_rao(box, triples, params, grid[:3], freqs, False, noise=noise, complex_data=True)
        print(f"  {20*math.log10(noise):+4.0f} dB   usable@10% {r['usable_10pct']:2}/{n}   "
              f"@25% {r['usable_25pct']:2}   median bound {r['median_dir_sd']:.2f}")
    print("\nmicrophone sweep, -60 dB, complex data:")
    for k in (1, 2, 3, 4):
        r = I.cramer_rao(box, triples, params, grid[:k], freqs, False, noise=1e-3, complex_data=True)
        print(f"  {k} mic(s)   usable@10% {r['usable_10pct']:2}/{n}   @25% {r['usable_25pct']:2}   "
              f"median bound {r['median_dir_sd']:.2f}")
    print("\nThe honest reading: rank said one capture identifies everything and conditioning said two")
    print("were enough. With a noise model, identifying 36 modal parameters to 10% needs about -70 dB")
    print("and roughly one microphone per usable direction; at a realistic -60 dB you get three, and")
    print("at -50 dB you get none. What survives is a handful of COMBINATIONS, which is what an")
    print("equaliser needs and not what a parameter table needs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
