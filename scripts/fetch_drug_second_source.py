#!/usr/bin/env python3
"""Fetch the same compound's published potency from TWO independent databases.

Why: drug discovery has no class-5 evidence in this repo, and a potency value is the obvious
candidate — it is published, numeric, and supposedly the same quantity. The two sources are
independent pipelines over independent curation:

  ChEMBL   EMBL-EBI's curated bioactivity database   (keyless REST, JSON)
  PubChem  NCBI's BioAssay warehouse                 (keyless REST, CSV)

    python3 scripts/fetch_drug_second_source.py      # writes data/drugs/second_source.json

The compound is imatinib (ChEMBL ID CHEMBL941, PubChem CID 5291) — the canonical example of a
targeted drug, and one with hundreds of published IC50s across many assays.
"""
from __future__ import annotations

import csv
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "drugs" / "second_source.json"
CHEMBL_ID = "CHEMBL941"
PUBCHEM_CID = "5291"
NAME = "imatinib"


def _curl(url: str) -> str:
    return subprocess.run(["curl", "-sS", "--max-time", "180", "-L", url],
                          capture_output=True, text=True, check=True).stdout


def chembl_values() -> list[dict]:
    """Every IC50 ChEMBL records for this compound, in nM, with its target and assay."""
    out = []
    offset = 0
    while offset < 1200:
        url = ("https://www.ebi.ac.uk/chembl/api/data/activity.json"
               f"?molecule_chembl_id={CHEMBL_ID}&standard_type=IC50&limit=200&offset={offset}")
        page = json.loads(_curl(url))
        acts = page.get("activities", [])
        if not acts:
            break
        for a in acts:
            value = a.get("standard_value")
            if value in (None, ""):
                continue
            try:
                out.append({"value_nm": float(value),
                            "target": a.get("target_chembl_id"),
                            "assay": a.get("assay_chembl_id"),
                            "relation": a.get("standard_relation") or "="})
            except (TypeError, ValueError):
                continue
        offset += 200
    return out


def pubchem_values() -> list[dict]:
    """IC50 rows PubChem BioAssay reports for this CID, converted from uM to nM."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{PUBCHEM_CID}/assaysummary/CSV"
    raw = _curl(url)
    out = []
    for row in csv.DictReader(io.StringIO(raw)):
        if (row.get("Activity Name") or "").strip().upper() != "IC50":
            continue
        value = (row.get("Activity Value [uM]") or "").strip()
        if not value:
            continue
        try:
            out.append({"value_nm": float(value) * 1000.0,
                        "aid": row.get("AID"), "target": row.get("Target Accession")})
        except ValueError:
            continue
    return out


def main() -> int:
    chembl = chembl_values()
    pubchem = pubchem_values()
    payload = {
        "compound": NAME,
        "chembl_id": CHEMBL_ID,
        "pubchem_cid": PUBCHEM_CID,
        "note": "Two independent curation pipelines for the same nominal quantity (IC50).",
        "units": "nM",
        "sources": {
            "chembl": {"url": f"https://www.ebi.ac.uk/chembl/api/data/activity.json"
                              f"?molecule_chembl_id={CHEMBL_ID}&standard_type=IC50",
                       "values": chembl},
            "pubchem": {"url": "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"
                               f"{PUBCHEM_CID}/assaysummary/CSV",
                        "values": pubchem},
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(chembl)} ChEMBL IC50s, "
          f"{len(pubchem)} PubChem IC50s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
