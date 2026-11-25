#!/usr/bin/env python3
"""Generate `web/frontier-view.json` — the consolidated node-schema view.

The canonical schema is the set of guarded files (`research-frontier.json`, `approaches.json`,
`rejections.json`, `evidence.json`); this script DERIVES the single view the site and the engine
consume, so there is one source of truth and the view cannot drift by hand-editing.

Run after changing any schema file:

    python3 scripts/build_frontier_view.py

`tests/test_research_frontier.py` fails if the committed view is stale.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "frontier-view.json"


def build() -> dict:
    fr = json.loads((ROOT / "web" / "research-frontier.json").read_text())
    ap = json.loads((ROOT / "web" / "approaches.json").read_text())
    rej = json.loads((ROOT / "web" / "rejections.json").read_text())
    ev_path = ROOT / "web" / "evidence.json"
    ev = json.loads(ev_path.read_text()) if ev_path.exists() else {"runs": []}
    att_path = ROOT / "web" / "attempts.json"
    attempts = json.loads(att_path.read_text()).get("attempts", []) if att_path.exists() else []
    bev_path = ROOT / "web" / "build-evidence.json"
    bev = json.loads(bev_path.read_text()) if bev_path.exists() else None

    build_evidence = None
    if bev is not None:
        build_evidence = {
            "commit": bev.get("commit"),
            "dirty": bev.get("dirty", []),
            "lean_version": bev.get("lean_version"),
            "build_exit": bev.get("build_exit"),
            "tests_exit": bev.get("tests_exit"),
            "theorem_count": len(bev.get("theorems", [])),
            "ok": bev.get("ok"),
        }

    approaches_by_name = {o["name"]: o.get("routes", []) for o in ap["obligations"]}
    evidence_by_name: dict = {}
    for r in ev.get("runs", []):
        evidence_by_name.setdefault(r["name"], []).append(r)

    obligations = []
    for o in fr["obligations"]:
        name = o["name"]
        obligations.append({
            "name": name,
            "state": o.get("state", "open"),
            "rung": o.get("rung", ""),
            "routes": approaches_by_name.get(name, []),
            "evidence": evidence_by_name.get(name, []),
        })

    return {
        "schema": "sextant-frontier-view",
        "root_obligation": fr["root_obligation"],
        "proved_layer": fr.get("proved_layer", []),
        "transports": fr.get("transports", []),
        "obligations": obligations,
        "rejections": rej.get("rejections", []),
        "attempts": attempts,
        "build_evidence": build_evidence,
    }


def main() -> None:
    OUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
