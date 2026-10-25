"""Climate models, scored on the same bar as the macro-finance roster.

This is the **transfer test**: the bar was written for macro-finance and extracted to
``pacland.bar`` because the machine is what transfers. Here it runs on three CMIP6 models,
and the result is diagnostic rather than flattering — climate's exact content is *stronger*
than macro-finance's (conservation laws are genuine invariants), but its verification
surface is **thinner**: no no-change null and no real-time out-of-sample test, so two of the
nine slots cannot be claimed by any of these models.

The three rows are chosen to show the scoring doing real work:

- **GISS-E2-1-G** — passes sensitivity, forcing and all three conservation ledgers (the
  trust board's clean case). It is the only one that can claim the conservation Rule of
  Three.
- **MPI-ESM1-2-HR** — passes sensitivity and forcing but **leaks one ledger**. It therefore
  cannot claim `rule_of_three` or `guard_suite`, and drops a tier for it. That is the same
  model the climate trust board excludes, seen through the bar.
- **UKESM1-0-LL** — fails sensitivity and conservation. It claims only what is true of it.

What none of them can claim, and why: `exact_structure` (the invariants are physical
conservation laws, measured not proved in symbols), `deficit` (climate's `m` is computed for
the discipline, not per model), `out_of_sample` and `benchmark` (nobody has run these models
against a no-change projection on real-time data), and `falsifiable_prediction` (none
registered per model). Those are gaps in the field, surfaced by a bar it has never been
scored on.
"""
from __future__ import annotations

from ..bar import Model, audit, models_sorted, summary

TRUST_BOARD = "src/pacland/climate/trust_board.py"
GUARDS = "src/pacland/climate/guards.py"
DRIFT = "src/pacland/climate/cmip6_drift.py"
DRIFT_DOC = "docs/climate-cmip6-drift.md"
REPRODUCE = "scripts/climate_drift_second_source.py"

#: Slots a CMIP6 model can claim *today*, given what the repo holds: the trust board scores
#: it, the conservation ledgers are measured for 17 of 53, and the guard-suite is the
#: discipline's. Nothing else exists at the per-model level.
COMMON = ("trust_entry", "reproduce")


def _giss() -> Model:
    return Model(
        name="CMIP6 GISS-E2-1-G",
        kind="forecast",
        role="a clean model on every available axis — the positive control of the transfer test",
        exact_content="energy, mass and salt conservation (exact physical invariants, measured)",
        free="the model's own 100+ tuned parameters",
        observables=("ECS", "ERF2x", "energy/mass/salt drift"),
        done=frozenset(COMMON + ("rule_of_three", "guard_suite")),
        evidence={"rule_of_three": DRIFT, "guard_suite": GUARDS, "trust_entry": TRUST_BOARD,
                  "reproduce": REPRODUCE},
        priority=0,
    )


def _mpi() -> Model:
    return Model(
        name="CMIP6 MPI-ESM1-2-HR",
        kind="forecast",
        role="passes sensitivity and forcing, leaks one conservation ledger — excluded by the "
             "trust board, and by the bar for the same reason",
        exact_content="energy, mass and salt conservation (exact physical invariants, measured)",
        free="the model's own 100+ tuned parameters",
        observables=("ECS", "ERF2x", "energy/mass/salt drift"),
        # it LEAKS a ledger, so it cannot claim the conservation checks
        done=frozenset(COMMON),
        evidence={"trust_entry": TRUST_BOARD, "reproduce": REPRODUCE},
        priority=1,
    )


def _ukesm() -> Model:
    return Model(
        name="CMIP6 UKESM1-0-LL",
        kind="forecast",
        role="fails sensitivity and conservation — on the roster so the bar can say so",
        exact_content="energy, mass and salt conservation (exact physical invariants, measured)",
        free="the model's own 100+ tuned parameters",
        observables=("ECS", "ERF2x", "energy/mass/salt drift"),
        done=frozenset(COMMON),
        evidence={"trust_entry": TRUST_BOARD, "reproduce": REPRODUCE},
        priority=2,
    )


CLIMATE_ROSTER: list[Model] = [_giss(), _mpi(), _ukesm()]


def summary_rows(root: str | None = None) -> list[dict]:
    return summary(CLIMATE_ROSTER, root)


def audit_rows(root: str | None = None) -> list[str]:
    return audit(CLIMATE_ROSTER, root)


def transfer_finding() -> dict:
    """What scoring climate on the macro-finance bar reveals."""
    rows = summary_rows()
    owed = {r["name"]: r["missing"] for r in rows}
    common_owed = set.intersection(*(set(v) for v in owed.values()))
    return {
        "rows": rows,
        "owed_by_every_model": sorted(common_owed),
        "n_clean": sum(1 for r in rows if r["tier"] == "clean"),
        "n_weak": sum(1 for r in rows if r["tier"] == "weak"),
        "verdict": (
            "climate's exact content is stronger than macro-finance's, but its verification "
            "surface is thinner: no no-change null and no real-time out-of-sample test exist "
            "at the per-model level"
        ),
    }


def trust_entries(root: str | None = None) -> list:
    from ..trust import TrustEntry

    out = []
    for m in models_sorted(CLIMATE_ROSTER):
        out.append(TrustEntry(
            discipline="climate",
            artifact=m.name,
            tier=m.tier(root),
            detail=f"{len(m.observables)} observables, {len(m.missing())} bar slots owed"
                   f" — {m.role[:60]}",
            evidence=m.evidence.get("trust_entry", "—"),
        ))
    return out
