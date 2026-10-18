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
    Boundary(
        "Reconstruct the compactification from observables (inverse problem)",
        LimitType.UNDERDETERMINED,
        "The self-validated structure miner finds no strong fingerprint in W0, gs, "
        "or the gauge couplings (docs/new-approach.md) — these observables do not "
        "determine the geometry.",
        "Constraints eliminate fast (small-W0 removes ~57%); the inverse problem "
        "is answerable-by-elimination once richer observables exist.",
    ),
    Boundary(
        "Compute the full EFT spectrum (masses, instanton corrections)",
        LimitType.INTRACTABLE,
        "The DEGREE-0 spectrum (complex-structure + axio-dilaton, 6 eigenvalues) IS "
        "computable — measured 2026-10-18 (322 critical points, 34 SUSY, 128 s). The "
        "INSTANTON-CORRECTED spectrum (maximum_degree=1, the Kähler-moduli masses) is "
        "INTRACTABLE, not unmeasurable: FluxEFT accepts maximum_degree (the computation "
        "EXISTS), but building it and evaluating mass_matrix at a SINGLE vacuum times "
        "out at 300 s (measured 2026-10-19 on studio-linux). No feasible computation.",
        "The way around an intractable wall is to find structure that shortcuts it: a "
        "leading-instanton approximation, the LCS limit, or a single-Kähler-modulus "
        "model. The CS+dilaton half is already the structure miner's input.",
    ),
    Boundary(
        "Measure whether small Lambda is typical (Weinberg anthropic argument)",
        LimitType.UNMEASURABLE,
        "Measured 2026-10-19: at the no-scale SUSY point V = 0 (machine precision, "
        "10^-31..10^-26) — Minkowski, not AdS. The AdS value -3 e^K |W|^2 arises only "
        "AFTER Kaehler-moduli stabilization (KKLT), and the de Sitter uplift after "
        "that; both are beyond the degree-0 FluxEFT.",
        "The no-scale theorem is CONFIRMED from data (V = 0 at SUSY); the log-uniform "
        "W0 prior is measured; the Lambda distribution is a derived question once the "
        "uplift chain exists.",
    ),
    Boundary(
        "Is there an algorithm to decide whether a flux configuration admits a "
        "supersymmetric vacuum?",
        LimitType.UNDECIDABLE,
        "The vacuum conditions are Diophantine: flux quanta are integers and the "
        "F-term equations are polynomial in the moduli with flux-dependent "
        "coefficients. Deciding solvability of Diophantine equations is undecidable "
        "in general (Matiyasevich's resolution of Hilbert's 10th problem), so the "
        "landscape's decidability cannot be assumed — though no specific reduction "
        "of a landscape question to an undecidable Diophantine problem is proven yet.",
        "The fourth wall is now named, not left empty: the honest move here is to "
        "prove-or-name a reduction (an impossibility certificate), not to search. "
        "The boundary map covers all four senses.",
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
