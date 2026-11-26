#!/usr/bin/env python3
"""Generate web/claims.json from the sextant.py CATALOG — the single source of truth.

The sextant.html page had a hard-coded CLAIMS array that drifted (38 vs 56). This script derives
the claims JSON from the registry so the page (and any consumer) reads the same data the engine
verifies. The plain-English 'plain' field is a separate concern; this carries the machine-checkable
fields (verdict, theorem, claim, falsifier, oracle, tier).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland import sextant  # noqa: E402

claims = [
    {
        "id": name,
        "verdict": e.get("verdict"),
        "theorem": e.get("theorem"),
        "claim": e.get("claim"),
        "falsifier": e.get("falsifier"),
        "oracle": e.get("oracle"),
        "tier": e.get("tier"),
    }
    for name, e in sorted(sextant.CATALOG.items())
]

out = Path(__file__).resolve().parents[1] / "web" / "claims.json"
out.write_text(json.dumps({"claims": claims}, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(claims)} claims)")
