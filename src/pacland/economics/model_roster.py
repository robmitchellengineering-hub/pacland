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

import os
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parents[3])


def _root(root: str | None) -> str:
    """Repo root, so evidence paths resolve the same from any cwd."""
    return root or _REPO_ROOT

# ---------------------------------------------------------------------------
# The bar. Eight slots, in the order a model earns them.
# ---------------------------------------------------------------------------

SLOTS = (
    "exact_structure",        # constraints + labels, proven not asserted
    "deficit",                # m computed two-tier (backcast / forecast)
    "rule_of_three",          # N independent checks, distinct failure modes, agreeing
    "guard_suite",            # what the model forbids, each mutation-proven
    "out_of_sample",          # measured vs a real-time vintage, benchmarked
    "benchmark",              # the no-change null it must beat
    "trust_entry",            # a board tier with named evidence
    "falsifiable_prediction", # a registered claim that could die
    "reproduce",              # one command, green
)

# A model's *kind* decides which slots it owes. An oracle is not a forecaster; a
# benchmark is not a model; a statistical model has no exact content to inventory.
REQUIRED = {
    "control": ("benchmark", "guard_suite", "reproduce"),
    "oracle": ("exact_structure", "rule_of_three", "guard_suite", "trust_entry", "reproduce"),
    "forecast": SLOTS,
    "statistical": ("benchmark", "out_of_sample", "reproduce"),
}

KINDS = tuple(REQUIRED)


@dataclass(frozen=True)
class Model:
    """One named model, with the bar-slots it satisfies and the evidence for each."""

    name: str
    kind: str
    role: str                     # one line: why it is on the roster
    exact_content: str            # what is exact (constraints + labels) — or "none"
    free: str                     # the parameters that are free
    observables: tuple[str, ...] = ()   # the measured series a deficit would count
    done: frozenset[str] = frozenset()
    evidence: dict[str, str] = field(default_factory=dict)
    priority: int = 0             # build order; lower starts first

    def missing(self) -> tuple[str, ...]:
        return tuple(s for s in REQUIRED[self.kind] if s not in self.done)

    def tier(self, root: str | None = None) -> str:
        """broken if any claim lacks evidence; clean if every owed slot is done;
        weak otherwise. Overclaiming is worse than not having started."""
        violations = audit_model(self, root)
        if violations:
            return "broken"
        return "clean" if not self.missing() else "weak"


def _repo_path(evidence: str, root: str) -> str | None:
    """Evidence is a repo-relative path when it looks like one; None if it is a
    citation (a URL, or prose naming a published result)."""
    if "://" in evidence or " " in evidence.strip():
        return None
    if "/" not in evidence and "." not in evidence:
        return None
    return os.path.join(root, evidence)


def audit_model(model: Model, root: str | None = None) -> list[str]:
    """Refuse the overclaim. A claimed slot must carry evidence; evidence that is a
    repo path must exist. Out-of-sample evidence must name a real-time vintage source,
    because a current-vintage backtest is not an out-of-sample test (Meese–Rogoff)."""
    root = _root(root)
    out: list[str] = []
    if model.kind not in REQUIRED:
        out.append(f"{model.name}: unknown kind {model.kind!r}")
        return out
    for slot in sorted(model.done):
        if slot not in SLOTS:
            out.append(f"{model.name}: unknown slot {slot!r}")
            continue
        ev = model.evidence.get(slot, "")
        if not ev:
            out.append(f"{model.name}: claims {slot} with no evidence")
            continue
        path = _repo_path(ev, root)
        if path is not None and not os.path.exists(path):
            out.append(f"{model.name}: claims {slot} but {ev} does not exist")
        if slot == "out_of_sample" and not any(
            k in ev.lower() for k in ("vintage", "real-time", "realtime", "alfred", "rtdsm")
        ):
            out.append(
                f"{model.name}: claims out_of_sample but {ev!r} names no real-time vintage "
                "source — a current-vintage backtest is not out of sample"
            )
    return out


def audit(models: list[Model] | None = None, root: str | None = None) -> list[str]:
    root = _root(root)
    out: list[str] = []
    for m in models if models is not None else ROSTER:
        out.extend(audit_model(m, root))
    return out


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
            "falsifiable_prediction", "reproduce",
        }),
        evidence={
            "exact_structure": "scripts/validate_economics_nk3.py",
            "deficit": "src/pacland/economics/nk3.py",
            "rule_of_three": "scripts/validate_economics_nk3.py",
            "guard_suite": "src/pacland/economics/nk3.py",
            "falsifiable_prediction": "docs/falsifiable-predictions.md",
            "reproduce": "scripts/validate_economics_nk3.py",
        },
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
        done=frozenset({"deficit", "rule_of_three", "guard_suite", "reproduce"}),
        evidence={
            "deficit": "src/pacland/economics/sw2007.py",
            "rule_of_three": "scripts/validate_economics_sw.py",
            "guard_suite": "src/pacland/economics/sw2007.py",
            "reproduce": "scripts/validate_economics_sw.py",
        },
        priority=3,
    )


def _bvar() -> Model:
    return Model(
        name="Bayesian VAR",
        kind="statistical",
        role="the baseline the DSGE fails to beat out of sample (Gürkaynak–Kısacıkoğlu–Rossi)",
        exact_content="none — pure fit; no identity is imposed",
        free="all coefficients and the prior",
        observables=("the same 3–7 series, as a VAR of them",),
        done=frozenset(),
        evidence={},
        priority=4,
    )


def _gdpnow() -> Model:
    return Model(
        name="GDPNow (Atlanta Fed)",
        kind="forecast",
        role="a real, published, replicable nowcast — the cleanest test of the word 'verified'",
        exact_content="national-accounts identities + the bridge equations from source data to GDP",
        free="bridge-equation coefficients, re-estimated each quarter",
        observables=("GDP growth (advance estimate)",),
        done=frozenset(),
        evidence={},
        priority=5,
    )


ROSTER: list[Model] = [_random_walk(), _sfc(), _nk3(), _sw(), _bvar(), _gdpnow()]


def build_order(models: list[Model] | None = None) -> list[str]:
    """Start order: the benchmark, then the oracle, then the smallest forecast model,
    then the workhorse, then the baselines."""
    return [m.name for m in sorted(models or ROSTER, key=lambda m: m.priority)]


def summary(models: list[Model] | None = None, root: str | None = None) -> list[dict]:
    models = models or ROSTER
    return [
        {
            "name": m.name,
            "kind": m.kind,
            "tier": m.tier(root),
            "missing": list(m.missing()),
            "observables": len(m.observables),
        }
        for m in models
    ]


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
                detail=f"{m.kind}: {len(m.observables)} observables, {len(m.missing())} bar slots owed"
                       f" — {notes[m.kind]}",
                evidence=m.evidence.get("reproduce", "—"),
            )
        )
    return out


def models_sorted(models: list[Model] | None = None) -> list[Model]:
    return sorted(models or ROSTER, key=lambda m: m.priority)
