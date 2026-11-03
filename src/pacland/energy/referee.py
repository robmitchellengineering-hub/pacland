"""The SEXTANT referee — run every candidate against every condition, and say what is unknown.

The referee adds no physics. Its whole value is that it refuses three specific moves that the field
makes constantly:

1. **survivorship by absence** — a framework that has not been tested is not a framework that passed;
2. **the unrun condition** — a condition whose bound was never read from its source cannot produce a
   verdict, however confident anyone is about it;
3. **the checked-after-the-fact claim** — a prediction is frozen before the comparison is computed, or
   it is not a prediction.

Point 3 is not enforced here, because it is a process rule: it lives in ``docs/energy-sextant.md`` as
the pre-registration step, and the frozen hash is the evidence that it happened first.

Run:
    python3 -m pacland.energy.referee            # the table, as it stands today
    python3 -m pacland.energy.referee --self-test
    python3 -m pacland.energy.referee --json
"""
from __future__ import annotations

import json
import sys

from .lattice import (
    CANDIDATES,
    CONSTRAINTS,
    DERIVATION,
    KILLED,
    MEASURED,
    SURVIVES,
    TESTABLE_NOW,
    UNKNOWN,
    Constraint,
    Evidence,
    table,
    verdict,
)

SHORT = {KILLED: "KILL", SURVIVES: "SURV", UNKNOWN: "  ? "}


def summarise(rows: list[dict]) -> dict:
    out = {KILLED: 0, SURVIVES: 0, UNKNOWN: 0, "cells": len(rows)}
    for r in rows:
        out[r["verdict"]] += 1
    return out


def render(rows: list[dict]) -> str:
    canonical = [c.id for c in CANDIDATES]
    keys = [c.id for c in CONSTRAINTS]
    cell = {(r["candidate"], r["constraint"]): r["verdict"] for r in rows}
    lines = ["| candidate | " + " | ".join(keys) + " |", "|---|" + "---|" * len(keys)]
    for cand in canonical:
        lines.append(f"| `{cand}` | " + " | ".join(SHORT[cell[(cand, k)]] for k in keys) + " |")
    s = summarise(rows)
    lines += [
        "",
        f"**{s['cells']} cells — KILLED {s[KILLED]} · SURVIVES {s[SURVIVES]} · UNKNOWN {s[UNKNOWN]}**",
        "",
        "? = no verifier has run against a verified bound. Not a pass.",
    ]
    return "\n".join(lines)


def run(evidence: dict[tuple[str, str], Evidence] | None = None) -> list[dict]:
    return table(evidence)


def self_test() -> int:
    """Prove the referee can fail a candidate, and cannot pass one by absence.

    Two checks, yes, and not three — so this is not a Rule-of-Three result. It is a wiring test of a
    machine, and the machine's claims are about its own ordering, not about the world.
    """
    verified = Constraint("C3", "unitarity-no-ghost", "no ghost", "a ghost", DERIVATION, TESTABLE_NOW,
                          bound_kind=MEASURED, source="a primary source", verified_on="2026-11-03")
    unverified = Constraint("C12", "semiclassical-limit-exists", "a limit exists", "no limit",
                            DERIVATION, TESTABLE_NOW)

    ghost = verdict(verified, Evidence(False, "propagating ghost in the spectrum"))
    never_run = verdict(unverified, None)
    checks = [
        ("a failing verifier KILLs", ghost[0] == KILLED),
        ("an unverified bound is UNKNOWN, never SURVIVES", never_run[0] == UNKNOWN),
    ]
    ok = True
    for name, passed in checks:
        print(f"  [{'ok' if passed else 'FAIL'}] {name}")
        ok &= passed
    print(f"\nself-test {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    rows = run()
    if "--json" in argv:
        print(json.dumps({"summary": summarise(rows), "cells": rows}, indent=2))
    else:
        print(render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
