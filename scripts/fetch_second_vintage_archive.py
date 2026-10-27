#!/usr/bin/env python3
"""Fetch a SECOND real-time vintage archive — the class-5 answer for economics.

ALFRED is one archive. The McCracken–Ng **FRED-MD historical vintages** are a second one: a
different assembly, published monthly as one CSV per vintage, keyless, from the St. Louis Fed.

    python3 scripts/fetch_second_vintage_archive.py      # writes data/economics/second_archive.json

What is compared: the value a vintage reports for a given month, in both archives. FRED-MD ships
*transformed* series (the `Transform:` row says which), so the comparison uses a series whose
transform is trivially reproducible — the unemployment rate, transform 2 (first difference). The
repo's ALFRED archive holds levels, so the same difference is taken on that side.

This is a second *pipeline*, not a second *release*: both ultimately republish the same BLS/BEA
releases. What it can catch is a pipeline error — a wrong vintage, a transcribed column, an API
returning the wrong as-of date. It cannot catch a mistake made by the statistical agency itself.
That distinction is stated wherever the result is used.
"""
from __future__ import annotations

import csv
import io
import json
import pathlib
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "economics" / "second_archive.json"
ZIP_URL = ("https://www.stlouisfed.org/-/media/project/frbstl/stlouisfed/research/fred-md/"
           "historical-vintages-of-fred-md-2015-01-to-2025-12.zip")

#: Six vintages spread across the archive, plus the months each one is asked about.
VINTAGES = ["2016-12", "2018-06", "2020-06", "2022-06", "2024-06", "2025-06"]
SERIES = "UNRATE"          # transform 2 (first difference) in FRED-MD


def _curl(url: str, dest: pathlib.Path) -> None:
    subprocess.run(["curl", "-sS", "--max-time", "300", "-L", "-o", str(dest), url], check=True)


def months_shift(month: str, months: int) -> str:
    """Shift a YYYY-MM vintage by `months` (negative = earlier)."""
    y, m = int(month[:4]), int(month[5:])
    m += months
    while m < 1:
        m += 12
        y -= 1
    while m > 12:
        m -= 12
        y += 1
    return f"{y:04d}-{m:02d}-01"


def weeks_before(month: str, weeks: int) -> str:
    """The ALFRED vintage date we ask for: a few weeks after the month ends, so the release is in."""
    y, m = int(month[:4]), int(month[5:])
    m += 1
    if m > 12:
        y, m = y + 1, 1
    return f"{y:04d}-{m:02d}-01"


def fred_md_values(zip_path: pathlib.Path) -> dict[str, dict[str, float]]:
    """month -> {series: transformed value} for each vintage file in the zip."""
    out = {}
    with zipfile.ZipFile(zip_path) as z:
        names = {n for n in z.namelist() if n.endswith(".csv")}
        for vintage in VINTAGES:
            name = next((n for n in names if n.startswith(vintage)), None)
            if name is None:
                continue
            text = z.read(name).decode("utf-8", "replace")
            rows = list(csv.reader(io.StringIO(text)))
            header = rows[0]
            if SERIES not in header:
                continue
            col = header.index(SERIES)
            obs = {}
            for row in rows[1:]:
                if not row or not row[0] or "/" not in row[0]:
                    continue
                date, value = row[0], row[col]
                if not value:
                    continue
                mm = date.split("/")
                obs[f"{int(mm[2]):04d}-{int(mm[0]):02d}"] = float(value)
            out[vintage] = obs
    return out


def alfred_values(vintage_date: str) -> dict[str, float]:
    """ALFRED monthly UNRATE levels at one vintage, via the keyless CSV endpoint."""
    url = ("https://alfred.stlouisfed.org/graph/alfredgraph.csv"
           f"?id={SERIES}&vintage_date={vintage_date}")
    text = subprocess.run(["curl", "-sS", "--max-time", "120", "-L", url],
                          capture_output=True, text=True, check=True).stdout
    rows = list(csv.reader(io.StringIO(text)))
    out = {}
    for row in rows[1:]:
        if len(row) < 2 or not row[1] or row[1] == ".":
            continue
        out[row[0][:7]] = float(row[1])
    return out


def main() -> int:
    tmp = pathlib.Path("/tmp/fred-md-vintages.zip")
    if not tmp.exists() or tmp.stat().st_size < 1_000_000:
        print(f"downloading {ZIP_URL}")
        _curl(ZIP_URL, tmp)
    md = fred_md_values(tmp)

    payload = {"source": {"product": "FRED-MD historical vintages (McCracken–Ng)",
                          "url": ZIP_URL,
                          "note": "second real-time archive; transformed series"},
               "series": SERIES,
               "value_note": "FRED-MD ships UNRATE as a LEVEL (its Transform row is metadata for "
                             "their modelling dataset, not the published column), so the "
                             "comparison is level against level at the same vintage. "
                             "'alfred_stale' is the same month at the vintage one year earlier, "
                             "kept so the check can prove it notices a wrong as-of date.",
               "vintages": {}}
    for vintage in VINTAGES:
        if vintage not in md:
            continue
        alfred = alfred_values(weeks_before(vintage, 1))
        stale = alfred_values(months_shift(vintage, -12))
        rows = {}
        for mdy_month, md_value in md[vintage].items():
            level = alfred.get(mdy_month)
            if level is None:
                continue
            rows[mdy_month] = {"fred_md": md_value, "alfred": level,
                               "alfred_stale": stale.get(mdy_month)}
        payload["vintages"][vintage] = rows
        print(f"{vintage}: {len(rows)} overlapping months")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
