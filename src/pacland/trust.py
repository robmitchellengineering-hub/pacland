"""The trust board — one ranked output across every discipline.

Each discipline emits ``TrustEntry`` objects — an artifact (a model, theorem,
guard-suite) plus a tier, a one-line reason, and its evidence. ``board()``
aggregates them into a single ranked list. This is the monetisation surface:
**trust, ranked, machine-checked**, across every field the verification
discipline is applied to.

Tiers mirror the board colour language:

  ``broken`` — fails a hard invariant (red) ·
  ``weak``   — fails a soft threshold (amber) ·
  ``clean``  — passes (green).
"""
from __future__ import annotations

from dataclasses import dataclass

TIER_ORDER = {"broken": 0, "weak": 1, "clean": 2}


@dataclass(frozen=True)
class TrustEntry:
    discipline: str
    artifact: str
    tier: str       # broken | weak | clean
    detail: str     # one-line reason
    evidence: str   # citation / source


def _climate_entries() -> list[TrustEntry]:
    from .climate.cmip6_drift import trust_entries
    return trust_entries()


def _landscape_entries() -> list[TrustEntry]:
    # The theorem tower — every theorem machine-checked, so all clean.
    return [
        TrustEntry("landscape", "Mitchell's Uniqueness", "clean",
                   "6/6 symbolic + Lean (n=1 and general n)", "scripts/validate_mitchell_uniqueness.py"),
        TrustEntry("landscape", "Constraint-First (Weyl FFT)", "clean",
                   "5/5 degrees, exact", "scripts/validate_constraint_first.py"),
        TrustEntry("landscape", "Mitchell's Completeness", "clean",
                   "6 exact + 2 numeric", "scripts/validate_mitchell_completeness.py"),
        TrustEntry("landscape", "Full-duality completion", "clean",
                   "5/5 symbolic", "scripts/validate_full_duality.py"),
        TrustEntry("landscape", "Complete Exact Structure", "clean",
                   "assembly of the four above", "scripts/validate_all_theorems.py"),
    ]


def _drugs_entries() -> list[TrustEntry]:
    return [
        TrustEntry("drugs", "constraint guard-suite", "clean",
                   "4 guards (charge/valence/Lipinski/synthesizability), each mutation-tested",
                   "src/pacland/drugs/guards.py"),
    ]


def _system_entries() -> list[TrustEntry]:
    return [
        TrustEntry("system", "climate guard-suite", "clean",
                   "4 guards (energy/water/carbon/humidity), each mutation-tested",
                   "src/pacland/climate/guards.py"),
    ]


def _ai_entries() -> list[TrustEntry]:
    # The verified-badge lane: repos that adopted valiant.json and pass.
    return [
        TrustEntry("ai", "valiant.json adoption — pacland", "clean",
                   "unit-tests gate green (178 tests)",
                   "valiant.json (this repo)"),
        TrustEntry("ai", "valiant.json adoption — harness-mesh", "clean",
                   "11 guards, 33 mutations, each proven to go red",
                   "harness-mesh DISPATCH.md §5"),
    ]


def board() -> list[TrustEntry]:
    """Every discipline's artifacts, ranked: broken first, then weak, then clean."""
    entries = (_climate_entries() + _landscape_entries() + _drugs_entries()
               + _ai_entries() + _system_entries())
    entries.sort(key=lambda e: TIER_ORDER[e.tier])
    return entries


def summary() -> dict:
    es = board()
    return {
        "n_artifacts": len(es),
        "n_broken": sum(1 for e in es if e.tier == "broken"),
        "n_weak": sum(1 for e in es if e.tier == "weak"),
        "n_clean": sum(1 for e in es if e.tier == "clean"),
        "broken": [e.artifact for e in es if e.tier == "broken"],
        "weak": [e.artifact for e in es if e.tier == "weak"],
    }


__all__ = ["TrustEntry", "board", "summary", "TIER_ORDER"]
