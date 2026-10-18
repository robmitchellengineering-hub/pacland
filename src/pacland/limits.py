"""Computing the uncomputable — the boundary map.

The object we actually want (pin down the compactification) is, in several
distinct senses, *uncomputable*. The answer is not to compute it, but to compute
its **boundary**: for each question, certify which sense of "uncomputable" applies
and what positive content remains computable. The accumulation of boundary points
is itself a theory of the problem — a cartography of the uncomputable.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LimitType(str, Enum):
    COMPUTABLE = "computable"            # an answer exists and we can compute it
    INTRACTABLE = "intractable"          # answer exists, no feasible algorithm
    UNMEASURABLE = "unmeasurable"        # answer exists, ground truth / data absent
    UNDERDETERMINED = "underdetermined"  # no unique answer exists
    UNDECIDABLE = "undecidable"          # provably no algorithm


@dataclass(frozen=True)
class Boundary:
    question: str
    limit: LimitType
    justification: str
    positive: str  # what REMAINS computable despite the limit


BOUNDARIES = [
    Boundary(
        "Find our vacuum by searching the flux landscape over W0",
        LimitType.INTRACTABLE,
        "W0 is log-uniform (measured R2=0.92) -> not learnable -> by Valiant's "
        "contrapositive, not evolvable (docs/learnability-negative.md).",
        "The verifier survives: hand-us-a-candidate verification is untouched.",
    ),
    Boundary(
        "Verify a candidate vacuum today",
        LimitType.UNMEASURABLE,
        "m=0 validated oracle outputs -> the certificate radius is infinite "
        "(docs/verification-deficit.md).",
        "The deficit is computable, and it closes as calibrated oracles are built.",
    ),
    Boundary(
        "Measure the KKLT tuning probability (|W0| ~ 1e-4)",
        LimitType.UNMEASURABLE,
        "The target is 7.6 nats below the observed |W0| range; the tail is "
        "unreachable by any feasible sample (docs/denef-douglas-test.md).",
        "The log-uniform prior is measured over 3.7 nats; extrapolation is "
        "explicitly flagged, never hidden.",
    ),
    Boundary(
        "Why this vacuum (the landscape measure / selection)",
        LimitType.UNDERDETERMINED,
        "Verification and selection are separate; the measure is a physics "
        "principle to be discovered, not a computation (docs/selection.md).",
        "Candidate measures are evaluable: the measure-verifier certifies "
        "typicality and elimination without deriving the measure.",
    ),
]


def boundary_map() -> list[Boundary]:
    """The certified computable/uncomputable boundary to date."""
    return list(BOUNDARIES)


def certify(question: str) -> Boundary | None:
    """Return the certified boundary for a question, or None if uncertified."""
    for b in BOUNDARIES:
        if question in b.question:
            return b
    return None
