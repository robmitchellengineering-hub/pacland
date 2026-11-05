"""Set-identification — the theoretical axis (axis 2) of the economics Rule of Three.

Axis 1 (empirical) is the forecast-failure record (Meese–Rogoff / Rossi / Gürkaynak);
axis 3 (structural) is the accounting guard-suite. This module is axis 2: the claim
that a macro model is only *set-identified* from aggregate data, never point-identified,
so a model that reports a point where only a set is identified is over-claiming.

Two concrete, exact results:

  * Gorman aggregation — with identical homothetic preferences (Cobb–Douglas a=1/2),
    aggregate excess demand depends only on the TOTAL endowment, not its distribution
    across agents. So the distribution is not identified from aggregates (the
    microfoundation of Sonnenschein–Mantel–Debreu).
  * Sectoral balances — the private balance S−I is identified by the identity, but S
    and I individually are not (only their difference is fixed).

Pure stdlib + Fraction, zero floating point.
"""
from __future__ import annotations

from fractions import Fraction as F


def cobb_douglas_aggregate_excess_demand(total, ratio):
    """Aggregate excess demand for agents with identical Cobb–Douglas (a=1/2)
    preferences and total endowment ``total``. Depends only on the TOTAL, not the
    distribution across agents (Gorman aggregation)."""
    r = F(ratio)
    t0, t1 = F(total[0]), F(total[1])
    income = t0 + r * t1              # p·e / p1 (total income in good-1 units)
    z1 = income / 2 - t0              # aggregate demand for good 1 minus endowment
    z2 = income / (2 * r) - t1        # aggregate demand for good 2 minus endowment
    return [z1, z2]


def aggregate_from_distribution(distribution, ratio):
    """Aggregate excess demand from an explicit list of agent endowments. For
    identical Cobb–Douglas tastes this equals the total-endowment aggregate — the
    distribution drops out, which is the non-identification."""
    total = [F(0), F(0)]
    for e in distribution:
        total[0] += F(e[0])
        total[1] += F(e[1])
    return cobb_douglas_aggregate_excess_demand(total, ratio)


def guard_point_identified(claimed, alternatives):
    """A point claim is justified only when no alternative parameter value produces
    the same observable aggregate (SMD/Gorman). Fails when alternatives exist — the
    value is set-identified, not point-identified. Returns ``(ok, message)``."""
    if alternatives:
        return (False,
                f"set-identified: {len(alternatives)} alternative(s) give the same aggregate")
    return True, "point-identified (no alternative)"


def sectoral_balance_set(government_balance, foreign_balance):
    """The private balance S−I is identified by the sectoral identity, but S and I
    individually are not. Returns ``(private_balance, message)``."""
    private = -(F(government_balance)) - F(foreign_balance)
    return private, (f"S − I = {private} (identified); S and I are set-identified — "
                     "only their difference is fixed")


def constraint_set_model(government_balance, foreign_balance):
    """The 'better model': emit the identified constraints and the identified set,
    and refuse to emit a point inside an unidentified region."""
    private, split_msg = sectoral_balance_set(government_balance, foreign_balance)
    return {
        "identified": {
            "private_balance": private,   # S−I, point-identified by the identity
        },
        "set_identified": {
            "saving_vs_investment": split_msg,
            "distribution": "any distribution of the measured total (Gorman aggregation)",
        },
        "refused": "no point forecast inside an unidentified region",
    }


def prior_weighted_set(candidates, prior_weights):
    """The belief layer's Mode-P answer to a set-identified parameter (build 7).

    ``guard_point_identified`` / ``constraint_set_model`` refuse a point where only a
    set is identified. This is what the refusal leaves open: weight the identified set
    by a PRIOR and report that weighted set, flagged as a prior — never a point, and
    never a data update. A set-identified model has an empty likelihood (the data
    cannot separate the candidates), so the posterior IS the normalised prior.

    ``candidates``     the identified set (a list of candidate values).
    ``prior_weights``  the prior weight of each candidate (non-negative, sum > 0).
    Returns a report whose ``posterior`` is the normalised prior, ``mode`` is
    ``"pluralism"`` (the belief layer's Mode P), and ``flag`` states that the
    weighting is a prior, not a likelihood.
    """
    if not candidates:
        raise ValueError("the identified set is empty — nothing to weight")
    if len(candidates) != len(prior_weights):
        raise ValueError("every candidate needs a prior weight")
    total = sum(prior_weights)
    if total <= 0:
        raise ValueError("prior weights must sum to something positive")
    posterior = [w / total for w in prior_weights]
    return {
        "mode": "pluralism",            # set-identified -> empty likelihood -> Mode P
        "set": candidates,
        "prior": list(prior_weights),   # flagged: the weighting is a prior
        "posterior": posterior,         # prior-weighted (== normalised prior)
        "flag": "the weighting is a PRIOR: no data separated these candidates",
        "refused": "no point emitted from an unidentified region",
    }


def sectoral_balance_prior_weighted(government_balance, foreign_balance,
                                    saving_candidates, saving_prior):
    """``S − I`` is identified; ``S`` and ``I`` are not. Weight candidate ``S`` values
    by a prior and return the prior-weighted ``(S, I)`` set on the identified line.

    This is the concrete instance of the mantle answer for economics: the identified
    line ``S − I = private_balance`` is the declared universe, the prior over ``S`` is
    the declared weighting, and the output is the weighted set — never a point.
    """
    private, _ = sectoral_balance_set(government_balance, foreign_balance)
    candidates = [(s, s - private) for s in saving_candidates]
    return prior_weighted_set(candidates, saving_prior)


__all__ = [
    "cobb_douglas_aggregate_excess_demand",
    "aggregate_from_distribution",
    "guard_point_identified",
    "sectoral_balance_set",
    "constraint_set_model",
    "prior_weighted_set",
    "sectoral_balance_prior_weighted",
]
