"""The discovery loop — priority 3's thin driver over the frontier schema.

The loop is deliberately thin: it reads the open obligations from the guarded frontier
(`web/research-frontier.json`), finds each one's falsifier in the SEXTANT registry, runs it, and
records the result as evidence. It does *not* invent approaches or write proofs — those are the
engine's later stages, which sit on top of this. What this gives is the one thing priority 3 needs
first: a single command that says, truthfully, what is open and whether the open thing still
survives its falsifier.

Usage:
    python -m pacland.discovery --list            # the open obligations + their tasks
    python -m pacland.discovery --run             # run each obligation's falsifier and report
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FRONTIER = ROOT / "web" / "research-frontier.json"


def _frontier() -> dict:
    return json.loads(FRONTIER.read_text())


def open_obligations() -> list[dict]:
    """The open obligations (state == 'open') from the guarded frontier."""
    return [o for o in _frontier()["obligations"] if o.get("state") == "open"]


def _catalog():
    sys.path.insert(0, str(ROOT / "src"))
    from pacland import sextant
    return sextant.CATALOG


def list_open() -> str:
    lines = []
    for o in open_obligations():
        e = _catalog().get(o["name"], {})
        falsifier = e.get("falsifier") or "(no falsifier wired)"
        tier = e.get("tier", "-")
        lines.append(f"◐ {o['name']}  [tier {tier}]")
        lines.append(f"    rung:      {o['rung']}")
        lines.append(f"    falsifier: {falsifier}")
    return "\n".join(lines)


def run_falsifiers() -> str:
    lines = []
    for o in open_obligations():
        e = _catalog().get(o["name"])
        simulate = e.get("simulate") if e else None
        if simulate is None:
            lines.append(f"◐ {o['name']:<32} NO-FALSIFIER  ({e.get('falsifier','') if e else ''})")
            continue
        try:
            survived, evidence = simulate()
            status = "SURVIVES" if survived else "REFUTED"
        except Exception as exc:  # a falsifier that errors is information too
            status, evidence = "ERROR", f"{type(exc).__name__}: {exc}"
        lines.append(f"◐ {o['name']:<32} {status}  {evidence}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="the discovery loop over the open obligations")
    ap.add_argument("--list", action="store_true", help="list the open obligations")
    ap.add_argument("--run", action="store_true", help="run each obligation's falsifier")
    args = ap.parse_args()
    if args.run:
        print(run_falsifiers())
    else:
        print(list_open())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
