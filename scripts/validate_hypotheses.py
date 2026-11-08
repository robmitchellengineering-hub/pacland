#!/usr/bin/env python3
"""SEXTANT hypothesis guard — every open question is well-formed (has a forced, open, candidates
with falsifiers, and an attack). A hypothesis with no falsifier is not a hypothesis."""
import sys
sys.path.insert(0, "src")
from pacland import hypotheses

required = {"question", "forced", "open", "candidates", "attack"}
problems = []
for name, h in hypotheses.HYPOTHESES.items():
    missing = required - set(h)
    if missing:
        problems.append(f"{name}: missing {sorted(missing)}")
    if not h["candidates"]:
        problems.append(f"{name}: no candidates")
    for i, c in enumerate(h["candidates"]):
        if "hypothesis" not in c or "falsifier" not in c:
            problems.append(f"{name} candidate {i}: missing hypothesis/falsifier")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"hypothesis registry OK: {len(hypotheses.HYPOTHESES)} open questions, every candidate has a falsifier")
