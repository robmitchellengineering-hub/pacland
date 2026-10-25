#!/usr/bin/env python3
"""Fetch the GDPNow real-time record: nowcast vs advance estimate vs the null.

For each target quarter, two vintages are pulled from ALFRED (keyless):

- **nowcast_as_of** — about two weeks after the quarter ends, before the advance
  estimate is released. Two series: ``GDPNOW`` (the Atlanta Fed's nowcast, annualised
  quarterly growth) and ``GDPC1`` (last quarter's growth *as known then*, the no-change
  benchmark).
- **advance_vintage** — after the advance estimate is published and before the second
  estimate, so ``GDPC1`` there is the first published number for the quarter: the truth.

ALFRED only stores vintages on release dates, so each request walks backwards up to 25
days and records the vintage date it actually used — the guard needs that date, not the
one we asked for.

Run:  python3 scripts/fetch_gdpnow.py
Out:  data/economics/gdpnow.json
"""
from __future__ import annotations

import concurrent.futures
import json
import pathlib
import urllib.parse
import urllib.request

OUT = pathlib.Path("data/economics/gdpnow.json")
BASE = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
#: GDPNow begins in 2011; start a year later so the benchmark always has a prior quarter.
QUARTERS = [(y, q) for y in range(2016, 2026) for q in range(1, 5)]
#: Step back a week at a time (release dates cluster on weeks, not arbitrary days) and
#: stop after six tries — 42 days of slack. Requests run in parallel; day-by-day
#: sequential walking made thousands of calls and took longer than the patience for it.
STEP_DAYS = 7
MAX_STEPS = 6


def _shift(date: str, days: int) -> str:
    import datetime as dt

    d = dt.date.fromisoformat(date) + dt.timedelta(days=days)
    return d.isoformat()


def fetch(series: str, as_of: str, back: int = MAX_STEPS) -> tuple[str, dict[str, float]] | None:
    """Nearest available vintage at or before ``as_of``, within ``back`` weekly steps."""
    for k in range(back + 1):
        day = _shift(as_of, -STEP_DAYS * k)
        params = {"id": series, "vintage_date": day,
                  "cosd": _shift(as_of, -400), "coed": _shift(as_of, 200)}
        url = f"{BASE}?{urllib.parse.urlencode(params)}"
        raw = None
        for _attempt in range(2):
            try:
                with urllib.request.urlopen(url, timeout=25) as r:
                    raw = r.read().decode()
                break
            except Exception:                               # noqa: BLE001
                continue
        if raw is None:
            continue
        rows = {}
        for line in raw.strip().splitlines()[1:]:
            parts = line.split(",")
            if len(parts) == 2 and parts[1] not in (".", "", "NA"):
                try:
                    rows[parts[0]] = float(parts[1])
                except ValueError:
                    pass
        if rows:
            return day, rows
    return None


def quarter_dates(y: int, q: int) -> tuple[str, str, str, str]:
    """(quarter start, nowcast as-of, advance vintage, previous quarter start)."""
    qs = f"{y}-{(q - 1) * 3 + 1:02d}-01"
    after = f"{y + 1}-01-15" if q == 4 else f"{y}-{q * 3 + 1:02d}-15"
    advance = f"{y + 1}-02-20" if q == 4 else f"{y}-{q * 3 + 2:02d}-20"
    # the previous quarter's START — quarter starts are Jan/Apr/Jul/Oct, nothing else
    prev = f"{y - 1}-10-01" if q == 1 else f"{y}-{(q - 2) * 3 + 1:02d}-01"
    return qs, after, advance, prev


def growth(levels: dict[str, float], start: str) -> float | None:
    import math

    if start not in levels:
        return None
    keys = sorted(levels)
    i = keys.index(start)
    if i == 0:
        return None
    return 400.0 * math.log(levels[start] / levels[keys[i - 1]])


def _one(y: int, q: int) -> dict | None:
    qs, after, advance, prev = quarter_dates(y, q)
    now = fetch("GDPNOW", after)
    # the benchmark MUST be built from the vintage the nowcast was published in, so
    # fetch GDPC1 at the vintage date that was actually found — not at the date we asked
    # for, which can land a release earlier.
    gdp_now = fetch("GDPC1", now[0]) if now else None
    gdp_adv = fetch("GDPC1", advance)
    if not (now and gdp_now and gdp_adv):
        return None
    if True:
        pass
    nowcast_date, now_rows = now
    bench_date, bench_rows = gdp_now
    adv_date, adv_rows = gdp_adv
    record = {
            "quarter": f"{y}Q{q}", "quarter_start": qs,
        "nowcast": now_rows.get(qs),
        "nowcast_vintage": nowcast_date,
        "benchmark_growth": growth(bench_rows, prev),
        "benchmark_vintage": bench_date,
        "advance": growth(adv_rows, qs),
        "advance_vintage": adv_date,
    }
    if record["nowcast"] is None or record["advance"] is None \
            or record["benchmark_growth"] is None:
        return None
    return record


def main() -> int:
    out = {"source": "ALFRED (alfred.stlouisfed.org), graph CSV, keyless",
           "fetched": "2026-10-26", "quarters": []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(_one, y, q): (y, q) for y, q in QUARTERS}
        for fut in concurrent.futures.as_completed(futures):
            rec = fut.result()
            if rec is None:
                continue
            out["quarters"].append(rec)
            print(f"{rec['quarter']}  nowcast {rec['nowcast']:>7.3f} "
                  f"(as of {rec['nowcast_vintage']})  advance {rec['advance']:>7.3f} "
                  f"(vintage {rec['advance_vintage']})  null "
                  f"{rec['benchmark_growth']:>7.3f}", flush=True)
    out["quarters"].sort(key=lambda r: r["quarter"])
    OUT.write_text(json.dumps(out, sort_keys=True, separators=(",", ":")))
    print(f"\n{len(out['quarters'])} quarters written to {OUT}; "
          f"{len(QUARTERS) - len(out['quarters'])} skipped", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
