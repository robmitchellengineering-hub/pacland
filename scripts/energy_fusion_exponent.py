#!/usr/bin/env python3
"""Fusion: is the 0.93 current exponent physics, or cross-machine collinearity?

    python3 scripts/energy_fusion_exponent.py [--data PATH]

REGISTERED, NOT RUN. Claim (docs/energy-conjectures.md): in the ITPA H-mode database the I_p exponent of
IPB98(y,2) (0.93) is carried by collinearity of I_p with B_T, R and n across machines. With per-machine
offsets the within-machine exponent is 0.55 +/- 0.12 and the B_T exponent rises from 0.15 to ~0.40, which
predicts tau_E = 0.85 +/- 0.08 x IPB98 at ITER's point, so the 15 MA baseline needs H98 ~ 1.15.

This script refuses until the database is present. It does not print a number it has not earned:
the numbers above are a registered prediction, not a measurement.

Falsifier: a within-machine exponent >= 0.85 (95% CI), or SPARC's first H-mode tau_E within +/-10% of
the IPB98 line at 8.7 MA / 12.2 T.

The database is not in this repository and is not redistributable here. Supply a CSV with at least
  machine, shot, I_p_MA, B_T_T, R_m, a_m, n_e_1e19, P_loss_MW, tau_E_s, H98
either at --data PATH or at data/fusion/itpa_hmode.csv.
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "fusion" / "itpa_hmode.csv"
REQUIRED = ("machine", "I_p_MA", "B_T_T", "R_m", "a_m", "n_e_1e19", "P_loss_MW", "tau_E_s", "H98")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Within-machine IPB98 exponent test (registered).")
    ap.add_argument("--data", default=str(DEFAULT))
    args = ap.parse_args(argv[1:])
    path = pathlib.Path(args.data)

    if not path.is_file():
        print("REFUSED: the ITPA H-mode database is not present, so nothing can be measured here.")
        print(f"  looked for: {path}")
        print()
        print("What this claim needs, and what it would produce:")
        print("  prediction : within-machine I_p exponent 0.55 +/- 0.12 (vs 0.93 between-machine)")
        print("               -> tau_E = 0.85 +/- 0.08 x IPB98 at ITER's point -> H98 ~ 1.15")
        print("  method     : mixed-effects power law, 5 exponents + per-machine offsets, bootstrap CI")
        print("  rows needed: the ITPA global H-mode confinement database (Kaye et al.), 10^3-10^4 rows")
        print("  columns    : " + ", ".join(REQUIRED))
        print()
        print("Falsifier (registered): within-machine exponent >= 0.85 (95% CI), or SPARC's first")
        print("H-mode tau_E within +/-10% of the IPB98 line at 8.7 MA / 12.2 T.")
        return 2
    print(f"REFUSED: data found at {path}, but the mixed-effects fit is not implemented in this")
    print("change. Registering a falsifier is not the same as running the test; implement the fit")
    print("before this script is allowed to print a verdict.")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
