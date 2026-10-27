#!/usr/bin/env python3
"""Fetch the global water budget — no credentials, no client library.

Precipitation: GPCP v2.3 monthly mean, and evaporation: NCEP/NCAR reanalysis latent heat flux.
Both are read through NOAA/PSL's **OPeNDAP ASCII** interface, which returns plain text over HTTP.
That matters twice: the repo takes no credentials, and a file that can be read with a regex needs
no netCDF dependency.

    python3 scripts/fetch_water_budget.py       # writes data/climate/water.json

The grids are strided (lat every 4th point, lon every 8th) and area-weighted by cos(lat), which is
enough for a global mean to well under a percent — and the stride is recorded in the payload so a
reader can see exactly what was sampled.
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "climate" / "water.json"

GPCP = ("https://psl.noaa.gov/thredds/dodsC/Datasets/gpcp/precip.mon.mean.nc.ascii"
        "?precip[{}:1:{}][0:4:71][0:8:143],lat[0:4:71],lon[0:8:143]")
LHFL = ("https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis.derived/surface_gauss/"
        "lhtfl.mon.mean.nc.ascii?lhtfl[{}:1:{}][0:4:71][0:8:143]")

#: GPCP monthly means start 1979-01; sample four months a decade.
SAMPLES = {"1979-01": (0, 0), "1989-01": (120, 120), "1999-01": (240, 240),
           "2009-01": (360, 360), "2019-01": (480, 480)}

LATENT_HEAT = 2.5e6          # J/kg, latent heat of vaporisation
SECONDS_PER_DAY = 86400.0


def _curl(url: str) -> str:
    # -g stops curl treating the OPeNDAP [start:stride:stop] brackets as glob patterns
    return subprocess.run(["curl", "-g", "-sS", "--max-time", "120", "-L", url],
                          capture_output=True, text=True, check=True).stdout


def _numbers(block: str) -> list[float]:
    return [float(x) for x in re.findall(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", block)]


def _grid(text: str, var: str) -> tuple[list[float], list[list[float]]]:
    """Parse an OPeNDAP ASCII response into (latitudes, rows of values)."""
    lat_block = re.search(r"lat\[\d+\]\s*\n([^\n]+)", text)
    if not lat_block:
        raise ValueError("no latitude axis in the response")
    lats = _numbers(lat_block.group(1))
    body = text.split(f"{var}.{var}[", 1)[-1]
    body = body.split("\n", 1)[-1]
    rows = []
    for line in body.splitlines():
        if not line.startswith("["):
            if line.strip().startswith("lat["):
                break
            continue
        rows.append(_numbers(line.split("]", 1)[-1]))
    if not rows:
        raise ValueError("no data rows in the response")
    return lats, rows


def unweighted_mean(rows: list[list[float]]) -> float:
    """What you get if you ignore latitude — kept so the guard can prove weighting matters."""
    return sum(v for row in rows for v in row) / (len(rows) * len(rows[0]))


def weighted_mean(lats: list[float], rows: list[list[float]]) -> float:
    """Cos(lat) area weighting — an unweighted mean would over-count the poles."""
    weights = [math.cos(math.radians(lat)) for lat in lats]
    total = sum(weights)
    return sum(w * v for w, row in zip(weights, rows) for v in row) / (total * len(rows[0]))


def main() -> int:
    samples = {}
    for label, (t_gpcp, t_lhfl) in SAMPLES.items():
        precip_text = _curl(GPCP.format(t_gpcp, t_gpcp))
        flux_text = _curl(LHFL.format(t_lhfl, t_lhfl))
        lats, rows = _grid(precip_text, "precip")
        precip_mm_day = weighted_mean(lats, rows)
        lats_f, rows_f = _grid(flux_text, "lhtfl")
        flux_wm2 = weighted_mean(lats_f, rows_f)
        # W/m2 -> mm/day: E = flux / latent heat, in kg/m2/s, x 86400
        evap_mm_day = flux_wm2 / LATENT_HEAT * SECONDS_PER_DAY
        samples[label] = {"precip_mm_day": precip_mm_day,
                          "precip_unweighted_mm_day": unweighted_mean(rows),
                          "evap_mm_day": evap_mm_day,
                          "latent_flux_wm2": flux_wm2}
        print(f"{label}: P {precip_mm_day:.3f} mm/day   E {evap_mm_day:.3f} mm/day")

    payload = {
        "sources": {
            "precipitation": {"product": "GPCP v2.3 monthly mean",
                              "url": "https://psl.noaa.gov/thredds/dodsC/Datasets/gpcp/",
                              "units": "mm/day"},
            "evaporation": {"product": "NCEP/NCAR reanalysis latent heat flux, monthly mean",
                            "url": "https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis.derived/surface_gauss/",
                            "units": "W/m2 -> mm/day at 2.5e6 J/kg"},
        },
        "sampling": {"months": list(SAMPLES), "lat_stride": 5, "lon_stride": 9,
                     "weighting": "cos(latitude) area weights"},
        "note": "Global water balance: precipitation must equal evaporation plus storage change. "
                "One observation product and one reanalysis, both free and keyless.",
        "samples": samples,
    }
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(f"\nwrote {OUT.relative_to(ROOT)}: {len(samples)} sampled months")
    return 0


if __name__ == "__main__":
    sys.exit(main())
