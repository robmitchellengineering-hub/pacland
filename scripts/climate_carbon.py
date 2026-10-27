#!/usr/bin/env python3
"""The carbon budget — the fourth measured conservation law.

    fossil emissions + land-use emissions = atmospheric growth + ocean sink + land sink

Two terms are observed and the sinks are the residual, so the check is on the *fraction*: the
share of what we emitted that stayed in the air. It must be a fraction — between none and all —
and its mean has to sit near the observed 0.44, or the accounting is broken.

    python3 scripts/climate_carbon.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.climate import carbon  # noqa: E402


def main() -> int:
    r = carbon.budget()
    print("PACLAND · climate — the carbon budget\n")
    print(f"window            {r['window'][0]}-{r['window'][1]}  ({r['years']} paired years)")
    print(f"emitted           {r['emitted_gtco2']:.0f} GtCO2")
    print(f"stayed airborne   {r['airborne_gtco2']:.0f} GtCO2  "
          f"(fraction {r['airborne_fraction']:.3f})")
    print(f"taken up by sinks {r['sinks_gtco2']:.0f} GtCO2")
    print(f"per-year range    {r['fraction_min']:.3f} - {r['fraction_max']:.3f}  "
          f"(s.d. {r['fraction_stdev']:.3f})")
    print(f"\nmean fraction in {carbon.AIRBORNE_RANGE} = {r['in_range']}")
    print(f"every year a fraction (0,1)        = {r['every_year_physical']}")
    print("verdict:", r["verdict"])
    ok, msg = carbon.guard_budget()
    print(f"\nseeded fault (a budget with no sinks): {msg.split(';')[-1].strip()}")
    return 0 if r["in_range"] and r["every_year_physical"] and ok else 1


if __name__ == "__main__":
    sys.exit(main())
