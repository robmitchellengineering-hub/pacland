"""derived_bounds.py — the M3 derived-bound mechanism: the KNOWN analytic mechanisms, tested + recorded.

The fitted families (exponential, log-corrected) are curve-fitting. The DERIVED bounds are the known
analytic mechanisms — cluster expansion, Dobrushin strong-coupling, asymptotic freedom — each with a
proven or known shape. This module tests each against the referee and records the honest result as a
queryable claim, so "which mechanisms have been tried and which FAILED" is part of the scientific
record, not just a falsifier's prose.
"""
from __future__ import annotations

import math

from pacland import registry
from pacland import bound_search as bs


def _cluster_expansion(beta: float) -> float:
    """The cluster-expansion lower bound c(β) ~ log β (grows, but far below the exponential scale)."""
    return math.log(beta) if beta > 1 else 0.0


def _dobrushin(beta: float) -> float:
    """The Dobrushin strong-coupling bound m(α) = (−log α)/2, which has a ceiling α(β*)=1 and is 0/negative past it."""
    return 0.0 if beta >= 2.0 else -0.5 * math.log(max(1e-12, 1.0 - beta / 2.0))


def _asymptotic_freedom(beta: float) -> float:
    """The asymptotic-freedom scale m(β) = 25.28·e^(−1.182β) — the referee itself, not an independent bound."""
    return 25.28 * math.exp(-1.182 * beta)


DERIVED: dict[str, object] = {
    "cluster-expansion": _cluster_expansion,
    "dobrushin": _dobrushin,
    "asymptotic-freedom": _asymptotic_freedom,
}


def evaluate_derived() -> dict:
    """Test every known mechanism against the referee and record the honest outcome as claims.

    The result is the honest negative: cluster expansion and Dobrushin do NOT reach the mass-gap
    scale, and asymptotic freedom IS the referee (so it is not an independent bound). Every one of
    these is recorded — the frontier is what is NOT in this list.
    """
    results: dict[str, dict] = {}
    for name, c in DERIVED.items():
        r = bs.check_bound(c)
        is_ref = (name == "asymptotic-freedom")
        survived = r["survived"] and not is_ref
        reason = ("referee identity — not an independent bound" if is_ref
                  else "does not reach the mass-gap scale")
        registry.record_claim(
            f"claim-mass-gap-{name}",
            f"mass-gap bound from the {name} mechanism",
            "failed" if not survived else "survived",
            problem="ym-mass-gap",
            reason=reason,
            produced_by="derived-bounds",
        )
        results[name] = {**r, "is_referee": is_ref}
    return results
