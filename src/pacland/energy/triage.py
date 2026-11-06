"""Move 1 — which ``NOT-RESEARCHED`` cell to look at next.

The referee leaves most cells ``NOT-RESEARCHED`` — a gap in *this repository*, not a property of the
framework (``profile.py`` states that distinction and a test enforces it). This module orders those
cells, so "the 62 unresearched cells" stops being a bare count and becomes a task list with a head.

It is deliberately **not** a Bayesian expected-information-gain ranking, and the reason is computed,
not asserted: ``detect_mode`` on the cell space returns ``UNDERDETERMINED`` (no honest per-cell
likelihood exists a priori — "would this framework's literature fully demonstrate this condition"
is exactly the thing nobody has measured yet). So ``rank_by_eig`` refuses, and that refusal is the
point: the belief layer exists to refuse a number that cannot be honestly stated, and this module
honours it rather than fabricate 62 likelihoods.

What runs instead is a **structural triage**::

    score = discrimination * decidability / cost

three named inputs, documented below, sourced to the lattice's own notes — a decision rubric, not a
posterior. Where a likelihood *is* honestly stateable — the Mode-C slice, the constraints with a
clean binary oracle and a known answer (C3 unitarity/ghost with its Stelle control; C5 entropy
coefficient 1) — EIG is shown separately and, under the uniform base-rate prior, reduces to
"cheapest first", which is the cross-check that the triage is the informative order.

Run:
    python3 -m pacland.energy.triage
"""
from __future__ import annotations

from dataclasses import dataclass

from pacland.belief import Belief, Likelihood, Mode, detect_mode, rank_by_eig
from .evidence import NOT_RESEARCHED, class_for
from .lattice import CANDIDATES, CONSTRAINTS, PENDING_BOUNDS, STAGE_TWO_ONLY

# --------------------------------------------------------------------------------------------
# The three rubric inputs. None of these is a probability, and none is hidden:
# they are triage weights, documented here so the ordering can be argued with rather than trusted.
# --------------------------------------------------------------------------------------------

# How much a definitive verdict on this condition moves the SEXTANT bet ("which framework is
# alive/dead"). Sourced to the Constraint.notes in lattice.py: C2 "most asserted, least exhibited",
# C12 "standing open problem for spin foams", C3 "positive control: Stelle must be KILLED",
# C5 "coefficient 1, not a free normalisation fitted to the answer".
DISCRIMINATION: dict[str, float] = {
    "C1": 6, "C2": 9, "C3": 9, "C4": 5, "C5": 8, "C6": 3, "C7": 4,
    "C8": 4, "C9": 4, "C10": 6, "C11": 8, "C12": 9, "C13": 4,
}

# Prior weight that a DEFINITIVE (KILLED / SURVIVES) verdict is reachable for this condition,
# rather than another CONTESTED. Anchored by the base rate: 11 cells researched, 0 definitive.
# A triage weight, not a calibrated probability — the C/P detector would refuse to treat it as a
# likelihood, and so does this module.
DECIDABILITY: dict[str, float] = {
    "C1": 0.40, "C2": 0.35, "C3": 0.60, "C4": 0.50, "C5": 0.70, "C6": 0.20,
    "C7": 0.50, "C8": 0.50, "C9": 0.40, "C10": 0.40, "C11": 0.80, "C12": 0.30,
    "C13": 0.30,
}

# Research hours per cell: read the framework's literature, determine whether the condition is
# demonstrated in full, in a limit/model/leading order, or not at all. A derivation that must be
# checked against the framework's defining equations (C2, C12) is expensive; a clean theorem check
# with known answers (C5) is cheap.
COST: dict[str, float] = {
    "C1": 5, "C2": 6, "C3": 4, "C4": 2, "C5": 2, "C6": 2, "C7": 3,
    "C8": 3, "C9": 3, "C10": 6, "C11": 1, "C12": 8, "C13": 5,
}

# Literature-size multiplier: how hard it is to find the one result that scores the cell. A large,
# well-indexed literature (strings) is ~1.0; a small niche one is cheaper to sweep.
LITERATURE: dict[str, float] = {
    "strings-adscft": 1.0, "lqg-spinfoam": 1.0, "asymptotic-safety": 0.8,
    "cdt": 0.7, "causal-sets": 0.7, "gft": 0.7,
}


@dataclass(frozen=True)
class TriageRow:
    """One NOT-RESEARCHED cell, with its triage score and the cost of researching it."""

    candidate: str
    constraint: str
    name: str
    score: float
    cost: float
    blocked: bool  # the constraint's measured bound is unread (PENDING_BOUNDS)


def researchable() -> list[tuple[str, str]]:
    """Every (candidate, constraint) pair that is actually asked of that candidate."""
    out: list[tuple[str, str]] = []
    for cand in CANDIDATES:
        for con in CONSTRAINTS:
            gate = STAGE_TWO_ONLY.get(con.id)
            if gate and not getattr(cand, gate):
                continue  # a string-only condition is not asked of a non-string candidate
            out.append((cand.id, con.id))
    return out


def unresearched() -> list[tuple[str, str]]:
    """The researchable cells that still carry no citation — the actual task list."""
    return [(c, k) for c, k in researchable() if class_for(c, k) == NOT_RESEARCHED]


def triage() -> list[TriageRow]:
    """The researchable NOT-RESEARCHED cells, ordered by the structural triage score.

    Deterministic: ties break on constraint id then candidate id, so the head never depends on
    insertion order.
    """
    rows: list[TriageRow] = []
    for cand_id, con_id in unresearched():
        con = next(k for k in CONSTRAINTS if k.id == con_id)
        cost = COST[con_id] * LITERATURE[cand_id]
        score = DISCRIMINATION[con_id] * DECIDABILITY[con_id] / cost
        rows.append(TriageRow(cand_id, con_id, con.name, score, cost, con_id in PENDING_BOUNDS))
    rows.sort(key=lambda r: (-r.score, r.constraint, r.candidate))
    return rows


def mode_verdict() -> Mode:
    """The honest regime of the cell space, computed by the C/P detector.

    Returns ``UNDERDETERMINED`` (no honest per-cell likelihood), which is *why* this module does not
    run ``rank_by_eig`` over the whole space. The verdict is the guard, not an inconvenience.
    """
    beliefs = [
        Belief(name=f"{c}/{k}", prior=0.15, likelihood=None,
               cost=COST[k] * LITERATURE[c], ground_truth_available=True)
        for c, k in unresearched()
    ]
    return detect_mode(beliefs).mode


def mode_c_slice() -> list[tuple[str, float]]:
    """EIG/cost on the one honestly-scoreable slice: C3 and C5.

    These two conditions have a clean binary oracle and a known answer, so a likelihood model can be
    stated without fabrication. Under the uniform base-rate prior the EIG ranking collapses to
    "cheapest first" — which is the cross-check that the structural triage (not the EIG number) is
    the informative order for the rest of the lattice.
    """
    beliefs = [
        Belief(name=f"{c}/{k}", prior=0.15,
               likelihood=Likelihood(true_positive=0.9, false_positive=0.1),
               cost=COST[k] * LITERATURE[c], ground_truth_available=True)
        for c, k in unresearched() if k in ("C3", "C5")
    ]
    if not beliefs:
        return []  # the two honestly-scoreable rows are now fully researched
    return rank_by_eig(beliefs)


def render() -> str:
    rows = triage()
    lines = [
        f"**{len(rows)} NOT-RESEARCHED cells**, ordered by the structural triage "
        "(score = discrimination x decidability / cost).",
        "",
        "| # | candidate | constraint | name | score | hours |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        flag = "  ⚠ bound unread" if r.blocked else ""
        lines.append(f"| {i} | `{r.candidate}` | {r.constraint} | {r.name} | "
                     f"{r.score:.3f} | {r.cost:.1f}{flag} |")
    lines += [
        "",
        f"C/P mode of the cell space: **{mode_verdict().value}** — a full EIG ranking is refused, "
        "so the order above is a triage rubric, not a posterior.",
        "",
        "EIG on the honest Mode-C slice (C3, C5), uniform base-rate prior:",
    ]
    slice_results = mode_c_slice()
    if slice_results:
        for name, eig_per_cost in slice_results:
            lines.append(f"  {name:24s} EIG/cost = {eig_per_cost:.4f}")
    else:
        lines.append("  (the Mode-C slice is empty — C3 and C5 are now fully researched)")
    lines += [
        "",
        "The head of the list is the next cell to research. Cells flagged 'bound unread' are blocked:",
        "their measured bound has not been read from its primary source (PENDING_BOUNDS), so they",
        "cannot be scored until that gap is closed first.",
    ]
    return "\n".join(lines)


def main() -> int:
    print(render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
