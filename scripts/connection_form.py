#!/usr/bin/env python3
"""The connection matrix: is there a closed algebraic form?

    python3 scripts/connection_form.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.periods import exact_series as E  # noqa: E402


def main() -> int:
    f = E.connection_form()
    print("The connection matrix — attempted, and bounded\n")
    print(f"  basis    : {{{', '.join(f['basis'])}}}")
    print(f"  bound    : coefficients below {f['maxcoeff']}, {f['dps']} dps\n")
    for r in f["rows"]:
        print(f"    {r['value']:>24}  relation: {r['relation']}")
    print(f"\n  {f['statement']}")
    print(f"  {f['consequence']}")
    print("\nPSLQ returns SMALL integers for a genuine relation and large ones when there is none — a hit at")
    print("1e12 is a numerical artefact, not a discovery. Tight bounds return nothing, so on this evidence the")
    print("connection coefficients are not in this span, and the mirror-map residual stays 'measured'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
