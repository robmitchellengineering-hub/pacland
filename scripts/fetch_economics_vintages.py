#!/usr/bin/env python3
"""Fetch real-time vintages from ALFRED and write the committed fixture.

No API key: ALFRED's graph endpoint takes a ``vintage_date`` and returns the series *as
published on that date* (verified 2026-10-26). The fixture is committed so the test
suite runs offline and the numbers cannot drift silently.

Run:  python3 scripts/fetch_economics_vintages.py
Out:  data/economics/vintages.json
"""
from __future__ import annotations

import json
import pathlib
import urllib.parse
import urllib.request

SERIES = ["GDPC1", "PCECC96", "GPDIC1", "CPIAUCSL"]
#: Year-start vintages across the window SW evaluate (1990:1-2004:4), plus a 2006 one
#: so the last forecast we form has a realised target available.
VINTAGES = [f"{y}-01-01" for y in range(1990, 2007, 2)] + ["2006-06-01"]
WINDOW = ("1985-01-01", "2006-12-31")
OUT = pathlib.Path("data/economics/vintages.json")
BASE = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"


def fetch(series: str, vintage: str | None, window=WINDOW) -> dict[str, float] | None:
    params = {"id": series, "cosd": window[0], "coed": window[1]}
    if vintage:
        params["vintage_date"] = vintage
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            raw = r.read().decode()
    except Exception as exc:                      # noqa: BLE001 - reported, not raised
        print(f"  {series} {vintage}: {exc}")
        return None
    rows = raw.strip().splitlines()[1:]
    out: dict[str, float] = {}
    for row in rows:
        parts = row.split(",")
        if len(parts) != 2 or parts[1] in (".", "", "NA"):
            continue
        try:
            out[parts[0]] = float(parts[1])
        except ValueError:
            continue
    return out or None


def main() -> int:
    data: dict = {"source": "ALFRED (alfred.stlouisfed.org), graph CSV, keyless",
                  "fetched": "2026-10-26", "window": list(WINDOW),
                  "series": SERIES, "vintages": {}}
    want = list(VINTAGES)
    for series in SERIES:
        for vintage in want:
            obs = fetch(series, vintage)
            if obs is None:
                # ALFRED stores a vintage only on dates it actually revised that series
                for extra in ("02-01", "03-01", "04-01"):
                    alt = vintage[:5] + extra
                    obs = fetch(series, alt)
                    if obs is not None and all(d < alt for d in obs):
                        vintage = alt
                        break
                    obs = None
            if obs is None or not all(d < vintage for d in obs):
                print(f"  {series} {vintage}: rejected (empty or look-ahead)")
                continue
            data["vintages"].setdefault(vintage, {})[series] = obs
            print(f"{series:9} {vintage}  {len(obs)} obs")
    data["current"] = {s: (fetch(s, None) or {}) for s in SERIES}
    # The policy rate is needed to estimate the rule. It is not revised — 1999-01-01 reads
    # 4.63 in both the 2001-01-01 vintage and the current series — so the current vintage is
    # used, with the check recorded in the fixture.
    data["rates"] = fetch("FEDFUNDS", None) or {}
    data["rates_note"] = (
        "FEDFUNDS, current vintage; unrevised (1999-01-01 = 4.63 in the 2001 vintage and now)"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")))
    kb = OUT.stat().st_size / 1024
    print(f"\nwrote {OUT} ({kb:.0f} KB); {len(data['vintages'])} vintages, "
          f"{sum(len(v) for v in data['current'].values())} current observations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
