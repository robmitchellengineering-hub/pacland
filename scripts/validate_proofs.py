#!/usr/bin/env python3
"""Proofs guard — every contributed claim in proofs/ is well-formed.

A claim with no falsifier is NOT_DEMONSTRATED (doc 27 §2.1): each proofs/*.md must carry a claim,
a verdict in {FORCED, FREE, IMPOSSIBLE}, a falsifier, and a why. Fails on a malformed contribution.
"""
import re
import sys
from pathlib import Path

PROOFS = Path("proofs")
FIELDS = ("claim", "verdict", "falsifier", "why")
VALID = {"FORCED", "FREE", "IMPOSSIBLE"}

problems: list[str] = []
files = sorted(p for p in (PROOFS.glob("*.md") if PROOFS.is_dir() else []) if p.name != "README.md")

for f in files:
    text = f.read_text()
    for field in FIELDS:
        if f"- **{field}:**" not in text:
            problems.append(f"{f.name}: missing {field}")
    m = re.search(r"- \*\*verdict:\*\* (\w+)", text)
    if m and m.group(1) not in VALID:
        problems.append(f"{f.name}: bad verdict {m.group(1)!r}")

if problems:
    print("FAIL:\n" + "\n".join(problems))
    sys.exit(1)
print(f"proofs OK: {len(files)} contributed claim(s) well-formed")
