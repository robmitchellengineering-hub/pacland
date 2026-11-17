#!/usr/bin/env python3
"""Vacuity linter for the pacland QM theorem tower.

Flags theorems that are vacuously true, tautological, or proved by unfolding a definition that bakes
in the answer — the class of "theorems" that a falsifier-before-believe discipline must not let pass
as results (e.g. `orbit_spectral_gap_derived : ∃ κ > 0`, `connection_space_flat : 0 = 0 := rfl`,
`gribovGhost_zero` proved by `simp [gribovGhost]`).

Usage: python3 scripts/vacuity_linter.py
Exit 0 = nothing flagged; exit 1 = suspicious theorems found.
"""

import re
import sys
from pathlib import Path

QM = Path("pacland-proof/PaclandProof/QM")

# A "declaration block" starts at a `theorem`/`lemma`/`def` and ends at its `:= ...` body term or
# the next top-level declaration. We scan line-by-line for the simple, high-precision patterns.
PATTERNS = [
    # trivial existence of a positive real (∃ κ : ℝ, 0 < κ — satisfied by κ = 1)
    (re.compile(r"∃\s*\w+\s*:\s*ℝ\s*,\s*0\s*<\s*\w+"), "trivial positivity witness (∃ κ > 0)"),
    # tautology by rfl
    (re.compile(r":=\s*rfl\b"), "tautology (:= rfl)"),
    # body that is only an rfl tactic
    (re.compile(r":=\s*by\s+rfl\b"), "tautology (:= by rfl)"),
    # a bare `:= by simp` / `:= by simp [...]` — unfolding a definition to prove a statement about it
    (re.compile(r":=\s*by\s+simp\b"), "definition-unfolding (:= by simp ...)"),
    # literal 0 = 0 or a = a statement
    (re.compile(r"\(\s*0\s*:\s*ℝ\s*\)\s*=\s*0"), "tautology (0 = 0)"),
]

def scan(path: Path):
    hits = []
    try:
        text = path.read_text()
    except Exception:
        return hits
    for i, line in enumerate(text.splitlines(), 1):
        for pat, label in PATTERNS:
            if pat.search(line):
                hits.append((i, label, line.strip()))
    return hits

def main():
    files = sorted(QM.glob("*.lean"))
    total = 0
    for f in files:
        hits = scan(f)
        if hits:
            total += len(hits)
            print(f"{f}:")
            for i, label, line in hits:
                print(f"  {i}: [{label}] {line[:100]}")
            print()
    if total:
        print(f"vacuity linter: {total} suspicious declaration(s) in {len(files)} files.")
        print("Review each: is it a real theorem, or does it unfold a definition that bakes in the answer?")
        sys.exit(1)
    print(f"vacuity linter: nothing flagged in {len(files)} files.")
    sys.exit(0)

if __name__ == "__main__":
    main()
