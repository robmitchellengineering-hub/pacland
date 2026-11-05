"""The allocator — EIG ranking over the research arm's bold claims (build 3).

The belief layer's job in one function: which unproven hypothesis do we test next?
This applies ``belief.rank_by_eig`` to ``docs/plan-bold-claims.md``'s still-open
claims, with an explicit prior, likelihood and cost per claim, and compares the
result to the hand-sequenced order the doc already lists.

The likelihoods and costs are ASSIGNED (documented, prior-flagged), not estimated —
the point of the belief layer is to make them explicit so outcomes can calibrate
them later (build 2's ledger is where that lands).
"""
from __future__ import annotations

from .belief import Belief, Likelihood, eig, rank_by_eig

#: Still-open bold claims (B1 is refuted, so it is not a next-test candidate).
#: Cost is in hours: B4 is "~30-minute node jobs" (0.5), B3 closed-form algebra,
#: B2 "a Mac day", B5 the b3=2,4,6 enumeration.
BOLD_CLAIMS = (
    Belief("B2 exactness = recursion, broken by normalisation", prior=0.70,
           likelihood=Likelihood(0.70, 0.30), cost=8.0),
    Belief("B3 dS needs a Kaehler modulus, not an uplift", prior=0.85,
           likelihood=Likelihood(0.90, 0.20), cost=2.0),
    Belief("B4 the wall is geometric, warm start multiplies reach", prior=0.85,
           likelihood=Likelihood(0.80, 0.30), cost=0.5),
    Belief("B5 invariant content is countable and bounded", prior=0.50,
           likelihood=Likelihood(0.60, 0.40), cost=4.0),
)

#: The hand sequence in docs/plan-bold-claims.md (B1 first, then B4, B3, B2/B5).
HAND_ORDER = ("B4", "B3", "B2", "B5")


def dispatch_order() -> list[tuple[str, float, float]]:
    """Rank by EIG/cost (descending). Returns ``(name, eig, eig_per_cost)``."""
    ranked = rank_by_eig(list(BOLD_CLAIMS))
    out: list[tuple[str, float, float]] = []
    for name, per_cost in ranked:
        b = next(x for x in BOLD_CLAIMS if x.name == name)
        out.append((name, eig(b.prior, b.likelihood), per_cost))
    return out


def compare_to_hand() -> str:
    """One sentence: does the EIG order agree with the hand order?"""
    order = [name.split()[0] for name, _, _ in dispatch_order()]
    agree = order == list(HAND_ORDER)
    return (
        f"EIG order {order} vs hand order {list(HAND_ORDER)} — "
        f"{'agrees' if agree else 'diverges'}; the divergence (if any) is the value."
    )


__all__ = ["BOLD_CLAIMS", "HAND_ORDER", "compare_to_hand", "dispatch_order"]
