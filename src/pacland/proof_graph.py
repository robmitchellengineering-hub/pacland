"""The proof dependency graph — derived from the frontier data, not hand-maintained.

``build()`` reads ``web/research-frontier.json`` and returns the mermaid diagram source, so the
sextant page's flow chart cannot drift from the accounting the drift test guards.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
FRONTIER = REPO / "web" / "research-frontier.json"


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build() -> str:
    d = json.loads(FRONTIER.read_text(encoding="utf-8"))
    lines = ["flowchart TB"]

    proved = d.get("proved_layer", [])
    lines.append('  subgraph TP["TIER 2-3 · proved (kernel-checked)"]')
    for i, name in enumerate(proved[:12]):
        lines.append(f'    P{i}["{_esc(str(name))}"]')
    lines.append("  end")

    transports = d.get("transports", [])
    lines.append('  subgraph TT["TIER 4 · conditional (proved-transport)"]')
    for i, t in enumerate(transports[:12]):
        lines.append(f'    T{i}["{_esc(t.get("name", "?"))}<br/>{_esc(t.get("hypothesis", "")[:60])}"]')
    lines.append("  end")

    obligations = d.get("obligations", [])
    for i, o in enumerate(obligations):
        lines.append(f'  H{i}["{_esc(o.get("name", "?"))}<br/>{_esc(o.get("rung", "")[:70])} — OPEN"]:::open')

    root = _esc(d.get("root_obligation", "")[:90])
    lines.append(f'  R["Yang–Mills mass gap<br/>{root}"]')

    for i in range(len(transports[:12])):
        lines.append(f"  T{i} --> R")
    for i in range(len(obligations)):
        lines.append(f"  H{i} --> R")
    lines.append("  classDef open fill:#ff8585,stroke:#ff8585,color:#080d16,font-weight:700")
    return "\n".join(lines) + "\n"
