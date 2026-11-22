"""correlation_length.py — the correlation-length ↔ mass-gap route (m ≥ 1/ξ).

The standard bridge: a PROVEN upper bound on the correlation length ξ(β) ≤ C·e^(cβ) gives a LOWER bound
on the mass gap m(β) ≥ (1/C)·e^(−cβ). This is the route the cluster expansion and strong-coupling
bounds use, and it is the most direct way a proven bound reaches the exponential scale. This module
tests correlation-length bounds and derives the mass-gap bound, so the search is over ξ (the physical
quantity the established methods bound) rather than only over m directly.
"""
from __future__ import annotations

import math

from pacland import registry
from pacland import bound_search as bs


def mass_gap_from_xi(xi):
    """m(β) ≥ 1/ξ(β): the standard correlation-length → mass-gap bridge."""
    return lambda beta: 1.0 / xi(beta)


def correlation_length(c: float, c_exp: float):
    """A correlation-length upper bound ξ(β) = C·e^(c·β)."""
    return lambda beta: c * math.exp(c_exp * beta)


def search_correlation_length(c_values: list[float], cexp_values: list[float],
                              source: str = "correlation-length") -> dict:
    """Test ξ(β)=C·e^(cβ) → m(β) ≥ (1/C)·e^(−cβ) against the referee + record the honest result.

    The mass-gap bound derived from the correlation length reaches the scale iff the exponent c equals
    the asymptotic-freedom coefficient 1.182 — so the honest result is that only the referee-equivalent
    survives, and it is marked is_referee (not a new bound).
    """
    survivors: list[dict] = []
    failures: list[dict] = []
    for c in c_values:
        for c_exp in cexp_values:
            m_bound = mass_gap_from_xi(correlation_length(c, c_exp))
            r = bs.check_bound(m_bound)
            is_ref = abs((1.0 / c) - 25.28) < 1e-6 and abs(c_exp - 1.182) < 1e-6
            entry = {"C": c, "c": c_exp, "mass_gap_amplitude": 1.0 / c, **r, "is_referee": is_ref}
            (survivors if (r["survived"] and not is_ref) else failures).append(entry)
    conclusion = ("no new correlation-length bound reaches the scale" if not survivors
                  else f"{len(survivors)} independent survivor(s)")
    registry.record_claim(
        "claim-mass-gap-correlation-length",
        "correlation-length route: ξ(β) ≤ C·e^(cβ) → m(β) ≥ (1/C)·e^(−cβ)",
        "failed" if not survivors else "survived",
        problem="ym-mass-gap",
        reason=conclusion,
        produced_by="correlation-length",
    )
    return {"n_survivors": len(survivors), "n_failures": len(failures),
            "conclusion": conclusion, "survivors": survivors}
