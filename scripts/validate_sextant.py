#!/usr/bin/env python3
"""SEXTANT guard — the theorem registry is well-formed and the CHSH control is exact.

A guard that cannot fail is not a guard: this one runs on the catalog and fails if any claim
is missing a field, has a bad verdict, or if the CHSH control drifts off 2√2."""
import sys, math
sys.path.insert(0, "src")
from pacland import sextant

required = {"claim", "theorem", "falsifier", "oracle", "verdict", "why"}
problems = []
for name, e in sextant.CATALOG.items():
    missing = required - set(e)
    if missing:
        problems.append(f"{name}: missing {sorted(missing)}")
    if e["verdict"] not in {"FORCED", "FREE", "IMPOSSIBLE"}:
        problems.append(f"{name}: bad verdict {e['verdict']!r}")

# known-truth control: the CHSH simulated value must be exactly 2√2
expected = 2 * math.sqrt(2)
got = float(sextant.CATALOG["chsh"]["value"].split("= ")[1])
if abs(got - expected) > 1e-6:
    problems.append(f"chsh: value {got} drifted from 2√2 ({expected})")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"sextant catalog OK: {len(sextant.CATALOG)} claims, CHSH control exact (2√2 = {expected:.6f})")
