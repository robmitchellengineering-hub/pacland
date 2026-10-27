#!/usr/bin/env python3
"""Fetch the global carbon accounting series and keep only what the check needs.

Source: Our World in Data's CO2 dataset (CC BY 4.0), which republishes the Global Carbon
Budget's fossil and land-use emissions alongside NOAA/GCB concentrations. One file, keyless,
and it is a *dataset* rather than a rendered page — which matters, because this repository has
already been burned by a figure that needed someone else's server.

    python3 scripts/fetch_carbon_budget.py      # writes data/climate/carbon.json

Kept: the World rows, annual, with emissions (fossil, land-use) and the atmospheric growth the
Global Carbon Budget reports. Concentrations come from the existing baseline.json, so the two
files are independent inputs to the same check.
"""
from __future__ import annotations

import csv
import io
import json
import pathlib
import subprocess
import sys

URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "climate" / "carbon.json"
KEEP = ("co2", "co2_including_luc", "co2_growth_abs", "land_use_change_co2", "methane")


def main() -> int:
    raw = subprocess.run(["curl", "-sS", "--max-time", "180", "-L", URL],
                         capture_output=True, text=True, check=True).stdout
    rows = [r for r in csv.DictReader(io.StringIO(raw)) if r.get("country") == "World"]
    series = {}
    for row in rows:
        year = int(row["year"])
        rec = {}
        for key in KEEP:
            value = row.get(key, "")
            if value not in ("", None):
                rec[key] = float(value)
        if rec:
            series[str(year)] = rec
    payload = {
        "source": "Our World in Data CO2 dataset (CC BY 4.0), republishing the Global Carbon "
                  "Budget: fossil CO2, CO2 including land-use change, and annual growth.",
        "url": URL,
        "unit": "million tonnes CO2 (MtCO2); growth in MtCO2/yr",
        "note": "World rows only. Concentrations are NOT taken from here — they come from "
                "data/climate/baseline.json (NOAA GML), so the two are independent inputs.",
        "years": sorted(int(y) for y in series),
        "world": series,
    }
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(f"wrote {OUT.relative_to(OUT.parents[2])}: {len(series)} annual rows, "
          f"{payload['years'][0]}-{payload['years'][-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
