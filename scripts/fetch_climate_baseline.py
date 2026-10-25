#!/usr/bin/env python3
"""Fetch the two series a climate null needs: observed GMST and global CO2.

Both are keyless. GMST is NASA GISTEMP v4 land-ocean annual means (the J-D column);
CO2 is the NOAA global annual mean. Annual values only — the hindcast works in years.

Run:  python3 scripts/fetch_climate_baseline.py
Out:  data/climate/baseline.json
"""
from __future__ import annotations

import json
import pathlib
import subprocess

GMST = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
CO2 = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.txt"
OUT = pathlib.Path("data/climate/baseline.json")


def _get(url: str) -> str:
    """Fetch with curl.

    The GISTEMP host refuses this Python build's TLS negotiation (``TLSV1_ALERT``), while
    curl works — so the fetch shells out rather than pretending the environment is uniform.
    """
    out = subprocess.run(["curl", "-sS", "--max-time", "40", url],
                         capture_output=True, text=True, check=True)
    return out.stdout


def gmst() -> dict[int, float]:
    raw = _get(GMST)
    out = {}
    for line in raw.splitlines():
        parts = line.split(",")
        if len(parts) < 14 or not parts[0].strip().isdigit():
            continue
        try:
            year, jd = int(parts[0]), float(parts[13])
        except ValueError:
            continue                     # '***' = incomplete year
        out[year] = jd
    return out


def co2() -> dict[int, float]:
    raw = _get(CO2)
    out = {}
    for line in raw.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            out[int(parts[0])] = float(parts[1])
    return out


def main() -> int:
    data = {
        "gmst": {str(k): v for k, v in sorted(gmst().items())},
        "co2": {str(k): v for k, v in sorted(co2().items())},
        "sources": {
            "gmst": "NASA GISTEMP v4 land-ocean annual mean anomaly (J-D column), "
                    "1951-1980 baseline, deg C",
            "co2": "NOAA GML global annual mean CO2, ppm",
        },
        "fetched": "2026-10-26",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, sort_keys=True))
    print(f"gmst {len(data['gmst'])} years {min(data['gmst'])}..{max(data['gmst'])}")
    print(f"co2  {len(data['co2'])} years {min(data['co2'])}..{max(data['co2'])}")
    print(f"written to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
