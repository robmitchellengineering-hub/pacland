"""The verification bar — one machine, any discipline.

Written for macro-finance (see ``docs/economics-model-roster.md``) and extracted here
because the *machine* is what transfers, not the answer. A model is scored on nine slots;
its **kind** decides which it owes; and ``audit`` refuses three specific overclaims:

1. a claimed slot with no evidence;
2. a claimed slot whose evidence is a repo path that does not exist;
3. an ``out_of_sample`` claim that names no real-time vintage source — a current-vintage
   backtest is not an out-of-sample test (Meese–Rogoff).

A model with every slot earned that **lost** to its null is still ``weak``: taking the test
is not passing it. That rule cost a clean badge once and was worth it.

Nothing here knows any economics. ``economics/model_roster.py`` and
``climate/model_roster.py`` each supply their own rows.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parents[2])


def root_dir(root: str | None = None) -> str:
    """Repo root, so evidence paths resolve the same from any cwd."""
    return root or _REPO_ROOT


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

#: A model's *kind* decides which slots it owes. An oracle is not a forecaster; a
#: benchmark is not a model; a statistical model has no exact content to inventory.
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
    observables: tuple[str, ...] = ()
    done: frozenset[str] = frozenset()
    evidence: dict[str, str] = field(default_factory=dict)
    priority: int = 0
    #: What the out-of-sample run *found*, when there is one: "beats_null" or
    #: "loses_to_null".
    outcome: str | None = None

    def missing(self) -> tuple[str, ...]:
        return tuple(s for s in REQUIRED[self.kind] if s not in self.done)

    def tier(self, root: str | None = None) -> str:
        """broken if any claim lacks evidence; clean if every owed slot is done;
        weak otherwise. Overclaiming is worse than not having started."""
        if audit_model(self, root):
            return "broken"
        if self.missing():
            return "weak"
        if self.outcome == "loses_to_null":
            return "weak"
        return "clean"


def _repo_path(evidence: str, root: str) -> str | None:
    """Evidence is a repo-relative path when it looks like one; None if it is a
    citation (a URL, or prose naming a published result)."""
    if "://" in evidence or " " in evidence.strip():
        return None
    if "/" not in evidence and "." not in evidence:
        return None
    return os.path.join(root, evidence)


def audit_model(model: Model, root: str | None = None) -> list[str]:
    root = root_dir(root)
    out: list[str] = []
    if model.kind not in REQUIRED:
        return [f"{model.name}: unknown kind {model.kind!r}"]
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


def audit(models: list[Model], root: str | None = None) -> list[str]:
    root = root_dir(root)
    out: list[str] = []
    for m in models:
        out.extend(audit_model(m, root))
    return out


def summary(models: list[Model], root: str | None = None) -> list[dict]:
    return [
        {"name": m.name, "kind": m.kind, "tier": m.tier(root),
         "missing": list(m.missing()), "observables": len(m.observables)}
        for m in models
    ]


def build_order(models: list[Model]) -> list[str]:
    return [m.name for m in sorted(models, key=lambda m: m.priority)]


def models_sorted(models: list[Model]) -> list[Model]:
    return sorted(models, key=lambda m: m.priority)
