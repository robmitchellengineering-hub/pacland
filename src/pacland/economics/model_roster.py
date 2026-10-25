"""The physics-level bar, and the macro-finance models scored against it.

The landscape core earns its claims a fixed way: an exact-structure inventory that is
*proven* (`scripts/validate_all_theorems.py`), a verification deficit `m` computed
two-tier, the Rule of Three, a mutation-tested guard-suite, a trust-board tier, a
falsifiable prediction, and a one-command reproduce. Climate added the missing idea —
score **every named model** on hard axes rather than averaging a crowd
(`docs/climate-trust-board.md`, 53 CMIP6 models, 14 trusted).

This module is the same machine for macro-finance. It does not estimate anything; it
records, for each named model, which slots of the bar are *actually* satisfied and
which evidence supports them. `audit()` then refuses the overclaim: a slot whose
evidence is a repo path that does not exist is a violation, and a model carrying one is
`broken` regardless of what else it passes.

The point is that the roster cannot flatter itself. Today most of it is `weak` — the
models are named and their exact content is known, but their deficits are not yet
computed. That is the honest state, and the tests pin it.
"""
from __future__ import annotations

from ..bar import (  # the machinery is shared: one bar, any discipline
    KINDS,
    REQUIRED,
    SLOTS,
    Model,
    audit_model,
)
from ..bar import audit as _audit
from ..bar import build_order as _build_order
from ..bar import models_sorted as _models_sorted
from ..bar import summary as _summary

# ---------------------------------------------------------------------------
# The roster. Six named models, three of which we start with.
# ---------------------------------------------------------------------------

# Smets–Wouters (2007) observe exactly these seven series. They are the model's m by
# construction — the published observation set *is* its claimed measured+computable
# list — and all seven pull keyless from FRED (verified 2026-10-25).
SW_OBSERVABLES = {
    "output growth": "GDPC1",
    "consumption growth": "PCECC96",
    "investment growth": "GPDIC1",
    "hours worked": "HOANBS",
    "real wage growth": "COMPRNFB",
    "inflation": "CPIAUCSL",
    "nominal policy rate": "FEDFUNDS",
}


def _random_walk() -> Model:
    return Model(
        name="random walk (no change)",
        kind="control",
        role="the null every forecast must beat; the field's own benchmark (Meese–Rogoff 1983)",
        exact_content="none — it asserts tomorrow equals today",
        free="none",
        done=frozenset({"benchmark", "guard_suite", "reproduce"}),
        evidence={
            "benchmark": "src/pacland/economics/forecast.py",
            "guard_suite": "tests/test_economics_forecast.py",
            "reproduce": "scripts/validate_economics_forecast.py",
        },
        priority=0,
    )


def _sfc() -> Model:
    return Model(
        name="Godley–Lavoie SFC (SIM/SIMEX)",
        kind="oracle",
        role="the always-true reference: every stock-flow identity holds by construction",
        exact_content="all sectoral and stock-flow identities + the budget constraint (double-entry)",
        free="behavioural parameters (propensities α1, α2, tax rate θ) — they move the path, not the identities",
        done=frozenset({"exact_structure", "rule_of_three", "guard_suite", "trust_entry", "reproduce"}),
        evidence={
            "exact_structure": "scripts/economics_accounting_closure.py",
            "rule_of_three": "scripts/economics_accounting_closure.py",
            "guard_suite": "src/pacland/economics/guards.py",
            "trust_entry": "src/pacland/trust.py",
            "reproduce": "scripts/economics_accounting_closure.py",
        },
        priority=1,
    )


def _nk3() -> Model:
    return Model(
        name="New Keynesian 3-equation (Taylor 1993; Clarida–Galí–Gertler)",
        kind="forecast",
        role="the positive control of the discipline: small enough to enumerate every constraint and every free parameter exactly",
        exact_content=(
            "Fisher equation i = r* + π; steady-state neutrality (π* = target, y = y_n); "
            "long-run Phillips π = π^e; the Taylor rule's long-run coefficients"
        ),
        free="5 — κ (slope), σ (IS), φπ, φy, ρ (rate smoothing)",
        observables=("output gap", "CPI inflation", "policy rate"),
        # Built: the exact structure is proven (7/7 sympy), the deficit ceiling and
        # today's validated count are computed, five guards are mutation-tested, the
        # determinacy boundary is reproduced by eigen-search, and two claims are on the
        # falsifiable register. Still owed: out_of_sample, benchmark, trust_entry.
        done=frozenset({
            "exact_structure", "deficit", "rule_of_three", "guard_suite",
            "benchmark", "out_of_sample", "trust_entry", "falsifiable_prediction",
            "reproduce",
        }),
        evidence={
            "exact_structure": "scripts/validate_economics_nk3.py",
            "deficit": "src/pacland/economics/nk3.py",
            "rule_of_three": "scripts/validate_economics_nk3.py",
            "guard_suite": "src/pacland/economics/nk3.py",
            "falsifiable_prediction": "docs/falsifiable-predictions.md",
            "benchmark": "src/pacland/economics/nk3_oos.py",
            "out_of_sample": "data/economics/vintages.json (ALFRED real-time vintages)",
            "trust_entry": "src/pacland/trust.py",
            "reproduce": "scripts/economics_nk3_oos.py",
        },
        # measured, and it lost: the calibrated model is worse than "no change" on
        # real-time inflation at every horizon (1.03x, 1.03x, 1.28x)
        outcome="loses_to_null",
        priority=2,
    )


def _sw() -> Model:
    return Model(
        name="Smets–Wouters (2007) DSGE",
        kind="forecast",
        role="the workhorse central-bank policy model — the one whose forecasts policy actually acts on",
        exact_content=(
            "the linearized equilibrium conditions ~20: Euler, NK Phillips, Taylor rule, Fisher, "
            "capital accumulation, resource constraint, AR exogenous processes; labels: the 7 observed series"
        ),
        free="~40 (published posterior means; 7 shocks + 3 structural)",
        observables=tuple(SW_OBSERVABLES),
        # Built to the point the source permits: the published posterior record is
        # re-derived and cross-checked against the paper's own prose (11/11), the
        # Calvo-implied slope and the published policy rule give a determinacy check,
        # and the m=7 ceiling is computed both ways. Still owed: the ~20-condition
        # inventory (exact_structure), the out-of-sample run, the benchmark, a clean
        # board row, and a registered falsifiable prediction.
        done=frozenset({"exact_structure", "deficit", "rule_of_three", "guard_suite",
                        "trust_entry", "falsifiable_prediction", "reproduce"}),
        evidence={
            # the nonlinear derivation AND the authors' own linearised file (34/34
            # equilibrium conditions vanish at the steady state)
            "exact_structure": "scripts/verify_sw_mod.py",
            "deficit": "src/pacland/economics/sw2007.py",
            "rule_of_three": "scripts/validate_economics_sw.py",
            "trust_entry": "src/pacland/trust.py",
            "falsifiable_prediction": "docs/falsifiable-predictions.md",
            "guard_suite": "src/pacland/economics/sw2007.py",
            "reproduce": "scripts/validate_economics_sw.py",
        },
        priority=3,
    )


def _bvar() -> Model:
    return Model(
        name="VAR(1) (statistical benchmark)",
        kind="statistical",
        role="the baseline the structural model is measured against — now run out of sample on real-time vintages",
        exact_content="none — pure fit; no identity is imposed",
        free="all coefficients (a BVAR prior would add more)",
        observables=("GDPC1, PCECC96, GPDIC1 — levels, jointly",),
        # Run on ALFRED real-time vintages (1990–2006) against today's revised values,
        # with the no-change null in the same table: beats the null at every horizon and
        # wins more paired comparisons than it loses (21/27, 23/27, 22/24).
        done=frozenset({"benchmark", "out_of_sample", "reproduce"}),
        evidence={
            "benchmark": "src/pacland/economics/meese_rogoff.py",
            "out_of_sample": "data/economics/vintages.json (ALFRED real-time vintages)",
            "reproduce": "scripts/economics_realtime_forecast.py",
        },
        outcome="beats_null",
        priority=4,
    )


def _gdpnow() -> Model:
    return Model(
        name="GDPNow (Atlanta Fed)",
        kind="forecast",
        role="a real, published, replicable nowcast — the cleanest test of the word 'verified'",
        exact_content="national-accounts identities + the bridge equations from source data to GDP",
        free="bridge-equation coefficients, re-estimated each quarter",
        observables=("GDP growth, advance estimate",),
        # Scored on the real-time record (37 quarters, 2016Q2-2025Q4): the nowcast
        # precedes the vintage carrying its target, the null shares its vintage, the
        # targets are first publications, and the edge survives excluding 2020.
        done=frozenset({
            "exact_structure", "deficit", "rule_of_three", "guard_suite", "benchmark",
            "out_of_sample", "trust_entry", "falsifiable_prediction", "reproduce",
        }),
        evidence={
            # the accounting half is proved (additivity, contributions, shares); the bridge
            # equations are its specification and are named as such, not implemented
            "exact_structure": "scripts/economics_accounts.py",
            "deficit": "src/pacland/economics/gdpnow.py",
            "rule_of_three": "scripts/economics_gdpnow.py",
            "guard_suite": "src/pacland/economics/gdpnow.py",
            "benchmark": "src/pacland/economics/gdpnow.py",
            "out_of_sample": "data/economics/gdpnow.json (ALFRED real-time vintages)",
            "trust_entry": "src/pacland/trust.py",
            "falsifiable_prediction": "docs/falsifiable-predictions.md",
            "reproduce": "scripts/economics_gdpnow.py",
        },
        # measured and it won: 0.25x MAE, 0.14x RMSE, 28/37 paired wins
        outcome="beats_null",
        priority=5,
    )


ROSTER: list[Model] = [_random_walk(), _sfc(), _nk3(), _sw(), _bvar(), _gdpnow()]


def audit(models: list[Model] | None = None, root: str | None = None) -> list[str]:
    """The economics roster's audit — no unsupported claim survives."""
    return _audit(models if models is not None else ROSTER, root)


def summary(root: str | None = None) -> list[dict]:
    """The roster scored — economics' own rows, rendered by the shared bar."""
    return _summary(ROSTER, root)


def build_order() -> list[str]:
    return _build_order(ROSTER)


def models_sorted() -> list[Model]:
    return _models_sorted(ROSTER)


def trust_entries(root: str | None = None) -> list:
    """One board entry per named model — the same shape climate uses for its models,
    so a reader sees macro-finance scored beside CMIP6."""
    from ..trust import TrustEntry  # deferred: the board imports this module back

    notes = {
        "control": "benchmark only (a null is not a model)",
        "oracle": "identities exact by construction; the reference, not a forecast",
        "forecast": "owes the full bar",
        "statistical": "no exact content; scored on out-of-sample skill only",
    }
    out = []
    for m in models_sorted():
        out.append(
            TrustEntry(
                discipline="economics",
                artifact=m.name,
                tier=m.tier(root),
                detail=(
                    f"{m.kind}: {len(m.observables)} observables, {len(m.missing())} bar slots owed"
                    + (f"; out-of-sample run {m.outcome.replace('_', ' ')}" if m.outcome else "")
                    + f" — {notes[m.kind]}"
                ),
                evidence=m.evidence.get("reproduce", "—"),
            )
        )
    return out


def models_sorted(models: list[Model] | None = None) -> list[Model]:
    return sorted(models or ROSTER, key=lambda m: m.priority)
