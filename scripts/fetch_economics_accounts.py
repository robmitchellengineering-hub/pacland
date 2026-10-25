#!/usr/bin/env python3
"""Fetch the national-accounts components the expenditure identity needs.

Nominal: GDP, GPDI, GCE, NETEXP are quarterly on FRED; PCE is monthly, and BEA's
quarterly PCE is the average of the three monthly values — so the month list is kept and
the average is taken, which closes the identity to BEA rounding.

Real: GDPC1, GPDIC1, GCEC1, EXPGSC1, IMPGSC1 are quarterly; PCECC96 is monthly and is
averaged the same way.

Run:  python3 scripts/fetch_economics_accounts.py
Out:  data/economics/accounts.json
"""
from __future__ import annotations

import json
import pathlib
import urllib.request

QUARTERS = [(y, q) for y in range(2018, 2026) for q in range(1, 5)]
#: Real PCE (PCECC96) is already quarterly; only nominal PCE is monthly.
QUARTERLY = ["GDP", "GPDI", "GCE", "NETEXP", "GDPC1", "GPDIC1", "GCEC1", "EXPGSC1",
             "IMPGSC1", "PCECC96"]
MONTHLY = ["PCE"]
OUT = pathlib.Path("data/economics/accounts.json")


def fetch(series: str, cosd: str = "2017-10-01", coed: str = "2026-03-31") -> dict[str, float]:
    url = (f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
           f"&cosd={cosd}&coed={coed}")
    raw = urllib.request.urlopen(url, timeout=30).read().decode()
    out = {}
    for line in raw.strip().splitlines()[1:]:
        parts = line.split(",")
        if len(parts) == 2 and parts[1] not in (".", "", "NA"):
            out[parts[0]] = float(parts[1])
    return out


def main() -> int:
    data = {s: fetch(s) for s in QUARTERLY + MONTHLY}
    out = {"source": "FRED (fred.stlouisfed.org), graph CSV, keyless",
           "fetched": "2026-10-26", "quarters": []}
    for y, q in QUARTERS:
        start = f"{y}-{(q - 1) * 3 + 1:02d}-01"
        months = [f"{y}-{m:02d}-01" for m in range((q - 1) * 3 + 1, q * 3 + 1)]
        rec = {"quarter": f"{y}Q{q}", "start": start, "nominal": {}, "real": {}}
        for s in ("GDP", "GPDI", "GCE", "NETEXP"):
            rec["nominal"][s] = data[s].get(start)
        for s in ("GDPC1", "GPDIC1", "GCEC1", "EXPGSC1", "IMPGSC1", "PCECC96"):
            rec["real"][s] = data[s].get(start)
        for s in MONTHLY:
            vals = [data[s].get(m) for m in months]
            vals = [v for v in vals if v is not None]
            rec["nominal"][s] = (sum(vals) / len(vals)) if len(vals) == 3 else None
        if all(v is not None for v in rec["nominal"].values()) and \
                all(v is not None for v in rec["real"].values()):
            out["quarters"].append(rec)
    OUT.write_text(json.dumps(out, sort_keys=True, separators=(",", ":")))
    print(f"{len(out['quarters'])} quarters written to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
