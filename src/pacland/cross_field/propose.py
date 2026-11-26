"""The cross-field generator — propose ranked transfer hypotheses for an open problem.

This is the *generate* half that was missing: given an open problem (what it NEEDS), each reusable
mechanism is matched by what it PROVIDES, and a transfer is proposed with the property it predicts
in the destination, a falsifier that would kill it, and a novelty score (distance from the graph).

Honest scope: this is a *structural* matcher over the mechanisms and problems it knows — it proposes
transfers between known mechanisms and known problems, and ranks + falsifies them. It does not invent
a mapping from nothing; that step is the LLM's, which can be dropped in later as the proposer.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transfer:
    mechanism: str
    hypothesis: str
    falsifier: str
    novelty: float          # 1.0 = not in the graph yet, 0.0 = already a known transfer
    predicted_property: str


#: What each reusable mechanism PROVIDES, REQUIRES, and TRANSFERS (its predicted property).
#: ``type`` is the structured match key — the mechanism's type must equal the problem's needed type.
MECHANISMS: dict[str, dict] = {
    "locate_gap_via_positivity": {
        "type": "spectral-gap",
        "provides": "spectral-gap bound",
        "requires": "self-adjoint positive operator",
        "transferable": "a positive spectral gap m = −log(λ₁/λ₀)",
    },
    "count_via_rooted_trees": {
        "type": "connected-subgraph-count",
        "provides": "connected-subgraph count bound",
        "requires": "graph of max degree Δ",
        "transferable": "#{connected subgraphs of size n} ≤ |V|·(Δ+1)^(n−1)",
    },
    "reduce_per_irrep": {
        "type": "character-decomposition",
        "provides": "per-irrep decomposition",
        "requires": "compact group symmetry",
        "transferable": "an observable decomposes into characters",
    },
}

#: What each open problem NEEDS (its type), and the falsifier that would refute a transfer into it.
PROBLEMS: dict[str, dict] = {
    "network-reliability": {
        "type": "connected-subgraph-count",
        "needs": "connected-subgraph count bound",
        "falsifier_target": "a network whose connected-subgraph count exceeds the predicted bound",
    },
    "markov-mixing-time": {
        "type": "spectral-gap",
        "needs": "spectral-gap bound",
        "falsifier_target": "a reversible chain whose mixing time is slower than the predicted gap",
    },
    "mass-gap": {
        "type": "spectral-gap",
        "needs": "spectral-gap bound uniform in volume and continuum",
        "falsifier_target": "a gauge theory whose gap vanishes in the volume/continuum limit",
    },
}


def _matches(mechanism: str, problem: str) -> bool:
    """The structured match: the mechanism's type equals the problem's needed type."""
    return MECHANISMS[mechanism]["type"] == PROBLEMS[problem]["type"]


def _novelty(mechanism: str, problem: str, known_pairs: set[tuple[str, str]]) -> float:
    return 0.0 if (mechanism, problem) in known_pairs else 1.0


def propose_transfers(problem: str, known_pairs: set[tuple[str, str]] | None = None) -> list[Transfer]:
    """Propose ranked transfers for an open problem. ``known_pairs`` are (mechanism, problem) pairs
    already in the graph (novelty 0); a proposed pair not in the graph scores novelty 1."""
    if problem not in PROBLEMS:
        raise ValueError(f"unknown problem {problem!r}; expected one of {list(PROBLEMS)}")
    known = known_pairs or set()
    need = PROBLEMS[problem]
    out = []
    for name, m in MECHANISMS.items():
        if not _matches(name, problem):
            continue
        out.append(Transfer(
            mechanism=name,
            hypothesis=f"{name} → {problem}: the {m['provides']} transfers, predicting "
                       f"{m['transferable']}",
            falsifier=f"fails if {need['falsifier_target']}",
            novelty=_novelty(name, problem, known),
            predicted_property=m["transferable"],
        ))
    return sorted(out, key=lambda t: -t.novelty)


if __name__ == "__main__":
    for problem in PROBLEMS:
        print(f"\n=== {problem} ===")
        for t in propose_transfers(problem):
            print(f"  [novelty {t.novelty:.0f}] {t.hypothesis}")
            print(f"          falsifier: {t.falsifier}")
