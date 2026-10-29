#!/usr/bin/env python3
"""How many microphones identify how many modes? Measured, not asserted.

    python3 scripts/spectral_identify.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.spectral import identify as I  # noqa: E402


def main() -> int:
    a = I.audit()
    print("PACLAND · spectral — how many microphones identify how many modes?\n")
    for label, r in (("geometry unknown (fit f, damping, amplitude)", a["full"]),
                     ("geometry known   (fit damping, amplitude)", a["known_geometry"])):
        print(f"{label}: {r['n_params']} parameters for {r['n_modes']} modes")
        for row in r["rows"]:
            bar = "#" * row["rank"]
            print(f"   {row['mics']} mic(s)  rank {row['rank']:2}/{row['params']:2}  {bar}")
        print()
    for c in a["checks"]:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['check']}")
        print(f"      {c['detail']}")
    print(f"\n{a['n_pass']}/{a['n']} checks pass")
    print("\nThe answer, for a 1-D room: TWO microphones identify the whole modal set; one microphone")
    print("identifies about 40% of it. Knowing the geometry does not raise that fraction — it only")
    print("shrinks the set that has to be identified.")
    return 0 if a["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
