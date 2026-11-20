"""memory.py — the search memory: the "learn" stage of the discovery loop.

What this machine has tried and what happened, persisted so the radar and the generator can consult it.
The belief layer already calibrates priors; this records the *search history* (problem → strategy →
candidate → verdict) and the per-strategy success rate. Minimal and honest: an append-only JSONL log +
recall helpers. The full cross-field memory (learning across the five registries) is gated on the
registries being built.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

MEMORY_PATH = Path.home() / ".dsh" / "sextant-memory.jsonl"


def remember(entry: dict) -> None:
    """Append one search event: {problem, strategy, candidate, verdict, ts}."""
    entry = dict(entry)
    entry.setdefault("ts", time.time())
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MEMORY_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def recall(limit: int = 100) -> list[dict]:
    """Most recent search events, newest last."""
    if not MEMORY_PATH.exists():
        return []
    lines = MEMORY_PATH.read_text().splitlines()[-limit:]
    out: list[dict] = []
    for ln in lines:
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def strategy_success() -> dict[str, dict[str, int]]:
    """Per strategy: {survived, falsified, open} counts across the whole history."""
    counts: dict[str, dict[str, int]] = {}
    for e in recall(limit=10000):
        s = e.get("strategy", "?")
        v = e.get("verdict", "?")
        c = counts.setdefault(s, {"survived": 0, "falsified": 0, "open": 0})
        if v in c:
            c[v] += 1
    return counts
