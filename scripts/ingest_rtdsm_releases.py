#!/usr/bin/env python3
"""Ingest the Fed's own first/second/third release table into JSON.

The Philadelphia Fed's Real-Time Data Set publishes, for real GNP/GDP, one worksheet with the
**First, Second, Third and Most-Recent** release values of quarterly growth (annual rate,
percentage points) from 1965. It is the construct this repo had only been approximating with 37
quarters of BEA advances.

The workbook is not committed (it is a download, and a binary); this script reads it from disk and
writes the numbers the analysis needs:

    python3 scripts/ingest_rtdsm_releases.py [path-to-routput_first_second_third.xlsx]

Default path: ~/Downloads/routput_first_second_third.xlsx. Output: data/economics/release_archive.json
Read with the standard library only — xlsx is a zip of XML.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
T = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "economics" / "release_archive.json"
DEFAULT = pathlib.Path.home() / "Downloads" / "routput_first_second_third.xlsx"


def _shared(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(T)) for si in root.findall("m:si", NS)]


def _cell(cell, shared: list[str]):
    v = cell.find("m:v", NS)
    if v is None:
        return None
    return shared[int(v.text)] if cell.get("t") == "s" else v.text


def read_rows(path: pathlib.Path, sheet: str = "xl/worksheets/sheet2.xml") -> list[list]:
    z = zipfile.ZipFile(path)
    shared = _shared(z)
    root = ET.fromstring(z.read(sheet))
    return [[_cell(c, shared) for c in row.findall("m:c", NS)]
            for row in root.findall(".//m:row", NS)]


def main() -> int:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        print(f"cannot find {path} — pass the workbook path as an argument", file=sys.stderr)
        return 2
    rows = read_rows(path)
    quarters = []
    for row in rows:
        if len(row) < 5 or not isinstance(row[0], str) or ":Q" not in row[0]:
            continue
        try:
            first, second, third, recent = (float(x) for x in row[1:5])
        except (TypeError, ValueError):
            continue
        quarters.append({"quarter": row[0], "first": first, "second": second,
                         "third": third, "most_recent": recent})
    payload = {
        "source": {
            "product": "Philadelphia Fed Real-Time Data Set — Real GNP/GDP (ROUTPUT)",
            "file": "routput_first_second_third.xlsx",
            "url": "https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-full-time-series-history",
            "units": "quarter-over-quarter growth, annual rate, percentage points",
            "columns": "First, Second, Third, Most_Recent releases",
        },
        "note": "Not committed as a workbook: only these numbers. Re-run "
                "scripts/ingest_rtdsm_releases.py after downloading the file.",
        "n": len(quarters),
        "quarters": quarters,
    }
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(quarters)} quarters "
          f"({quarters[0]['quarter']} .. {quarters[-1]['quarter']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
