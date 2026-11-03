"""The evaluability profile — how much of the lattice each framework can actually be scored on.

The programme's original stopping clause asked for a framework killed with evidence or surviving all
thirteen conditions. That clause is unreachable, and the reason is now a result rather than a complaint:
**every framework has at least one condition it cannot be evaluated on.** This module is that statement
as a computation rather than a sentence.

The profile separates three things that are easy to blur:

    blocked       CONTESTED / NOT-ESTABLISHED / NO-PREDICTION
                  a finding ABOUT THE FRAMEWORK — its literature disputes the condition, has not
                  solved it, or does not address it at all
    computable    COMPUTED-HERE / COMPUTED-ELSEWHERE
                  a computation exists that could decide the cell, so the cell is scorable
    unresearched  NOT-RESEARCHED
                  a gap in THIS REPO, not in the framework. It must never be used to claim a
                  framework is blocked: "we have not looked" is not a property of the framework.

The headline claim is therefore checked against `blocked` only. A framework whose only non-scores are
`NOT-RESEARCHED` is **not** blocked by this profile, however many of them there are — that would be the
repo marking its own homework.

Run:
    python3 -m pacland.energy.profile
"""
from __future__ import annotations

from .evidence import (
    COMPUTED_ELSEWHERE,
    COMPUTED_HERE,
    CONTESTED,
    NO_PREDICTION,
    NOT_ESTABLISHED,
    NOT_RESEARCHED,
    class_for,
    note_for,
)
from .lattice import CANDIDATES, CONSTRAINTS

BLOCKING = (CONTESTED, NOT_ESTABLISHED, NO_PREDICTION)
COMPUTABLE = (COMPUTED_HERE, COMPUTED_ELSEWHERE)


class FrameworkProfile:
    """One framework's row of the profile."""

    def __init__(self, candidate_id: str, name: str) -> None:
        self.candidate_id = candidate_id
        self.name = name
        self.blocked: list[tuple[str, str]] = []   # (constraint id, reason class)
        self.computable: list[str] = []
        self.unresearched: list[str] = []

    @property
    def is_blocked(self) -> bool:
        return bool(self.blocked)

    @property
    def scoring_total(self) -> int:
        """Conditions that could be scored today (blocked ones could not)."""
        return len(CONSTRAINTS) - len(self.blocked)

    def blocker(self) -> tuple[str, str] | None:
        """The first blocking condition, and its class. Deterministic: C1 before C13."""
        return self.blocked[0] if self.blocked else None


def profile() -> list[FrameworkProfile]:
    rows: list[FrameworkProfile] = []
    for cand in CANDIDATES:
        row = FrameworkProfile(cand.id, cand.name)
        for con in CONSTRAINTS:
            cls = class_for(cand.id, con.id)
            if cls in BLOCKING:
                row.blocked.append((con.id, cls))
            elif cls in COMPUTABLE:
                row.computable.append(con.id)
            else:
                row.unresearched.append(con.id)
        rows.append(row)
    return rows


def every_framework_is_blocked() -> bool:
    """The programme's claim: no framework is fully evaluable."""
    return all(row.is_blocked for row in profile())


def summary() -> dict:
    rows = profile()
    return {
        "frameworks": len(rows),
        "blocked": sum(1 for r in rows if r.is_blocked),
        "unblocked": [r.candidate_id for r in rows if not r.is_blocked],
        "total_blocked_cells": sum(len(r.blocked) for r in rows),
        "claim_holds": every_framework_is_blocked(),
    }


def render() -> str:
    rows = profile()
    lines = [
        "| framework | conditions it cannot be evaluated on | class | evaluable | unresearched |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        if r.blocked:
            cid, cls = r.blocker()
            extra = f" (+{len(r.blocked) - 1})" if len(r.blocked) > 1 else ""
            blocked = f"**{cid}**{extra}"
        else:
            cls, blocked = "—", "**none**"
        lines.append(f"| `{r.candidate_id}` | {blocked} | `{cls}` | "
                     f"{len(r.computable)} | {len(r.unresearched)} |")
    s = summary()
    lines += [
        "",
        f"**{s['blocked']}/{s['frameworks']} frameworks are blocked** — "
        f"{s['total_blocked_cells']} blocking cells in total.",
        "",
        "A blocker is `CONTESTED`, `NOT-ESTABLISHED` or `NO-PREDICTION`: a finding about the framework.",
        "`NOT-RESEARCHED` never counts — that is a gap in this repo, not a property of the framework.",
    ]
    return "\n".join(lines)


def main() -> int:
    print(render())
    print()
    for row in profile():
        print(f"{row.candidate_id}:")
        for cid, cls in row.blocked:
            print(f"  {cid:4s} {cls:15s} {note_for(row.candidate_id, cid).note[:110]}")
    return 0 if every_framework_is_blocked() else 1


if __name__ == "__main__":
    raise SystemExit(main())
