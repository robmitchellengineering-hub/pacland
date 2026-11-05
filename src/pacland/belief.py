"""The belief layer — subjective probability on the verification spine.

PACLAND's verification instruments answer "what is proven / refuted". This module
answers "how much should I believe each *unproven* hypothesis, and which do I test
next". It is a different *species* from the verifiers, not a seventh one: the
Hamkins/Woodin debate shows two camps can agree on every theorem and differ only on
report-as-truth, and this module owns the belief side of that boundary.

The spine (``PLANS/PLAN-subjective-probability-belief-layer.md``):

  prior -> Bayes factor -> posterior -> expected-information-gain ranking ->
  proper-scoring calibration -> (later) a PAC-Bayes bound.

The C/P detector (``detect_mode``) runs FIRST and gates the Bayesian stages. The
fan-out synthesis (``research/hamkins-belief-layer-synthesis.md``) proved that
convergence vs pluralism is a dichotomy, not a preference:

  * Mode C (convergence) — shared ground truth + a stated likelihood. Blackwell-
    Dubins merging holds, so priors wash out and calibration is checkable.
  * Mode P (pluralism)   — no shared ground truth / no dominating measure; merging
    provably fails (Kakutani; forcing validities are S4.2, not S5). The honest
    output is a credal set, not a converging posterior.
  * Underdetermined      — a certified-underdetermined hypothesis: the likelihood
    is EMPTY (the measure gap, T1), so Bayes cannot move and the report is
    {set, invariants, reachability, prior-flagged}, never a fake posterior.

``detect_mode`` is a NECESSARY-conditions test, not the full Kakutani/Hellinger
singularity test (that needs the measure structure and is a later build). It refuses
to admit Mode C when a hypothesis lacks ground truth or a likelihood.
"""
from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass
from enum import Enum


class Mode(str, Enum):
    """Which regime a hypothesis space is in (the C/P detector's output)."""

    CONVERGENCE = "convergence"        # Mode C: full Bayesian chain is permitted
    PLURALISM = "pluralism"            # Mode P: no shared ground truth, no merge
    UNDERDETERMINED = "underdetermined"  # empty likelihood — Bayes short-circuits


class ModeRefusal(Exception):
    """Raised when a Bayesian stage is asked to run outside Mode C."""


@dataclass(frozen=True)
class ModeVerdict:
    """``detect_mode`` output: the regime plus the reasons that put us there."""

    mode: Mode
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Likelihood:
    """A binary test's likelihood: how it answers under H and under ¬H.

    ``true_positive  = P(test says H | H)``
    ``false_positive = P(test says H | ¬H)``
    """

    true_positive: float
    false_positive: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.true_positive <= 1.0 and 0.0 <= self.false_positive <= 1.0):
            raise ValueError("likelihood probabilities must be in [0, 1]")


@dataclass(frozen=True)
class Belief:
    """One hypothesis with a numeric prior and (optionally) a likelihood model.

    ``likelihood is None`` means the likelihood is EMPTY — a certified
    underdetermination (T1). ``ground_truth_available=False`` means no verifier can
    ever settle it, so calibration and merging are impossible (Mode P).
    """

    name: str
    prior: float
    likelihood: Likelihood | None = None
    cost: float = 1.0
    ground_truth_available: bool = True

    def __post_init__(self) -> None:
        if not (0.0 <= self.prior <= 1.0):
            raise ValueError("prior must be in [0, 1]")
        if self.cost <= 0.0:
            raise ValueError("cost must be positive")


def detect_mode(beliefs: list[Belief]) -> ModeVerdict:
    """Classify a hypothesis space into a regime (the C/P detector, build 1).

    Necessary conditions for Mode C, each refusing on absence:

    1. every hypothesis has a ground-truth oracle (else PLURALISM — nothing to
       score or merge against);
    2. every hypothesis has a likelihood (else UNDERDETERMINED — the measure gap).

    Returns ``UNDERDETERMINED`` only when ground truth is present but a likelihood
    is missing; any missing ground truth is the more severe ``PLURALISM``.
    """
    if not beliefs:
        return ModeVerdict(Mode.UNDERDETERMINED, ("no hypotheses registered",))
    reasons: list[str] = []
    if any(not b.ground_truth_available for b in beliefs):
        reasons.append("no ground-truth oracle: at least one hypothesis can never be scored or merged")
    if any(b.likelihood is None for b in beliefs):
        reasons.append("empty likelihood: at least one hypothesis is certified-underdetermined")
    if not reasons:
        return ModeVerdict(Mode.CONVERGENCE, ())
    if all(b.ground_truth_available for b in beliefs):
        return ModeVerdict(Mode.UNDERDETERMINED, tuple(reasons))
    return ModeVerdict(Mode.PLURALISM, tuple(reasons))


def require_convergence(mode: Mode) -> None:
    """Refuse to run a Bayesian stage outside Mode C."""
    if mode is not Mode.CONVERGENCE:
        raise ModeRefusal(
            f"mode {mode.value}: Bayes update, expected-information-gain and "
            "calibration require convergence (shared ground truth + a likelihood)"
        )


def bayes_factor(likelihood: Likelihood, positive: bool) -> float:
    """``B = P(result | H) / P(result | ¬H)`` for one test result."""
    if positive:
        num, den = likelihood.true_positive, likelihood.false_positive
    else:
        num, den = 1.0 - likelihood.true_positive, 1.0 - likelihood.false_positive
    if den == 0.0:
        raise ValueError("likelihood denominator is zero — the test is degenerate")
    return num / den


def posterior(prior: float, likelihood: Likelihood, positive: bool) -> float:
    """``P(H | result)`` via Bayes' theorem, robust at perfect/absorbing boundaries.

    Equivalent to ``posterior odds = prior odds x B``, written in product form so a
    perfect test (``tp=1, fp=0``) yields ``1.0``/``0.0`` instead of dividing by zero.
    """
    if prior <= 0.0:
        return 0.0
    if prior >= 1.0:
        return 1.0
    if positive:
        num = likelihood.true_positive * prior
        den = num + likelihood.false_positive * (1.0 - prior)
    else:
        num = (1.0 - likelihood.true_positive) * prior
        den = num + (1.0 - likelihood.false_positive) * (1.0 - prior)
    if den == 0.0:
        raise ValueError("likelihood gives a zero-probability result")
    return num / den


def _binary_entropy(p: float) -> float:
    """Shannon entropy (nats) of a Bernoulli with success probability ``p``."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p))


def eig(prior: float, likelihood: Likelihood) -> float:
    """Expected information gain (nats) of the test: ``H(prior) - E[H(posterior|result)]``."""
    p_pos = prior * likelihood.true_positive + (1.0 - prior) * likelihood.false_positive
    post_pos = posterior(prior, likelihood, True)
    post_neg = posterior(prior, likelihood, False)
    return _binary_entropy(prior) - (p_pos * _binary_entropy(post_pos)
                                     + (1.0 - p_pos) * _binary_entropy(post_neg))


def brier_score(p: float, truth: bool) -> float:
    """Brier (quadratic) score of a reported probability against a realized truth."""
    y = 1.0 if truth else 0.0
    return (p - y) ** 2


def log_score(p: float, truth: bool) -> float:
    """Logarithmic (proper) score; lower is better."""
    q = p if truth else (1.0 - p)
    return -math.log(q)


def mean_brier(forecasts: list[tuple[float, bool]]) -> float:
    """Mean Brier score over a forecaster's (probability, truth) record."""
    if not forecasts:
        raise ValueError("no forecasts to score")
    return sum(brier_score(p, t) for p, t in forecasts) / len(forecasts)


def rank_by_eig(beliefs: list[Belief]) -> list[tuple[str, float]]:
    """Rank hypotheses by ``EIG / cost`` (descending), refusing outside Mode C."""
    require_convergence(detect_mode(beliefs).mode)
    scored: list[tuple[str, float]] = []
    for b in beliefs:
        assert b.likelihood is not None  # CONVERGENCE guarantees it
        scored.append((b.name, eig(b.prior, b.likelihood) / b.cost))
    scored.sort(key=lambda item: -item[1])
    return scored


def update(belief: Belief, positive: bool) -> Belief:
    """Return the belief after one test result (refuses an empty likelihood)."""
    if belief.likelihood is None:
        raise ModeRefusal("cannot update a hypothesis with an empty likelihood")
    return dataclasses.replace(
        belief, prior=posterior(belief.prior, belief.likelihood, positive)
    )


def kl_bernoulli(q: float, p: float) -> float:
    """``KL(Bernoulli(q) || Bernoulli(p))`` — the cost of moving a belief from prior
    ``p`` to posterior ``q``.

    Zero iff ``q == p``; infinite when the posterior assigns probability 1 to an event
    the prior calls impossible (the pluralism/divergence signal). This is the term the
    PAC-Bayes bound charges for how far the evidence moved the belief.
    """
    if q <= 0.0 or q >= 1.0:
        return 0.0 if q == p else float("inf")
    if p <= 0.0 or p >= 1.0:
        return 0.0 if q == p else float("inf")
    return q * math.log(q / p) + (1.0 - q) * math.log((1.0 - q) / (1.0 - p))


def pac_bayes_bound(prior: float, posterior: float, m: int, delta: float) -> float:
    """McAllester's additive PAC-Bayes bound (the crown, build 8).

    With probability >= ``1 - delta``, the generalization error of a posterior
    ``posterior`` (moved from prior ``prior`` after ``m`` observations) exceeds its
    empirical error by at most this gap::

        sqrt((KL(q||p) + ln(m/delta)) / (2m))

    The gap charges ``KL(q||p)`` — how far the evidence moved the belief — plus a
    sample-size term, amortised over twice the evidence. This is what makes the belief
    layer *PACLAND* rather than "we added Bayes": a degree of belief now carries a
    "probably approximately correct" guarantee, not just a number.
    """
    if m <= 0:
        raise ValueError("m must be positive")
    if not (0.0 < delta <= 1.0):
        raise ValueError("delta must be in (0, 1]")
    kl = kl_bernoulli(posterior, prior)
    return math.sqrt((kl + math.log(m / delta)) / (2.0 * m))


__all__ = [
    "Belief",
    "Likelihood",
    "Mode",
    "ModeRefusal",
    "ModeVerdict",
    "bayes_factor",
    "brier_score",
    "detect_mode",
    "eig",
    "kl_bernoulli",
    "log_score",
    "mean_brier",
    "pac_bayes_bound",
    "posterior",
    "rank_by_eig",
    "require_convergence",
    "update",
]
