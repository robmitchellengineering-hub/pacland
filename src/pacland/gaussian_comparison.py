"""gaussian_comparison.py — the mass gap as a Gaussian comparison for non-Abelian characters.

The mass gap is the spectral gap of the SU(N) Wilson measure `e^(β·Re Tr U)`. The Gaussian comparison
(Bakry–Émery) bounds the gap by the curvature of the measure's potential; for the Wilson measure the
potential is `Re Tr U` = the FUNDAMENTAL CHARACTER, which is NON-LINEAR (`2·cos θ` for SU(2)). The
curvature is `κ(θ) = 1/4 + 2β·cos θ`, negative at the antipode θ = π for β > 1/8 — that is the
non-linearity. Solving the mass gap means proving the Gaussian comparison SURVIVES this non-linearity:
the negative curvature lives only on the measure-negligible antipode, so it does not kill the gap
(Wang's criterion).
"""
from __future__ import annotations

import math

from pacland import registry


def su2_character(theta: float) -> float:
    """χ(θ) = Tr U = 2·cos θ — the SU(2) fundamental character, NON-LINEAR in θ."""
    return 2.0 * math.cos(theta)


def wilson_potential(beta: float, theta: float) -> float:
    """V(θ) = −β·χ(θ) = −2β·cos θ — the Wilson potential (the trace is non-quadratic)."""
    return -beta * su2_character(theta)


def bakry_emery_curvature(beta: float, theta: float) -> float:
    """κ(θ) = 1/4 + 2β·cos θ — the Bakry–Émery curvature (Ricci of S³ + Hessian of the potential)."""
    return 0.25 + 2.0 * beta * math.cos(theta)


def naive_comparison_bound(beta: float) -> float:
    """The naive Gaussian comparison: spectral gap ≥ min_θ κ(θ) = 1/4 − 2β — NEGATIVE for β > 1/8."""
    return 0.25 - 2.0 * beta


def antipode_measure(beta: float) -> float:
    """The antipode's Wilson weight e^(−2β) — the measure suppression of the non-linear (negative) region."""
    return math.exp(-2.0 * beta)


def check_nonlinearity(beta: float) -> dict:
    """The precise obstruction: the naive comparison bound is negative for β > 1/8, but the antipode
    carries weight e^(−2β). The comparison survives iff the negative region's measure is negligible."""
    naive = naive_comparison_bound(beta)
    return {
        "naive_bound": naive,
        "naive_negative": naive < 0.0,
        "antipode_weight": antipode_measure(beta),
        "survives_condition": "the negative-curvature region (antipode) has measure e^(−2β) → 0, so the "
                              "comparison survives via Wang's criterion (measure-negligible negative curvature)",
    }


TARGET = {
    "hypothesis": "the Gaussian comparison survives the non-linearity of the trace: the spectral gap of "
                  "the SU(N) Wilson measure is positive (β-uniform) despite κ(θ) being negative at the "
                  "measure-negligible antipode",
    "typed_inequality": "spectral_gap ≥ (Gaussian comparison constant) for the character potential Re Tr U",
    "nonlinearity": "Tr U = 2·cos θ is non-quadratic, so the Bakry–Émery curvature 1/4 + 2β·cos θ is "
                    "negative at the antipode for β > 1/8",
    "mechanisms": ["Bakry–Émery Gaussian comparison", "Wang's criterion (measure-negligible negative curvature)"],
    "falsifier": "a full-lattice configuration where the curvature stays negative on a measure-NON-negligible set",
}


def run_target(beta: float = 1.0) -> dict:
    """Run the engine on the Gaussian-comparison target: the non-linearity and the survival condition."""
    result = check_nonlinearity(beta)
    registry.record_claim(
        "claim-gaussian-comparison",
        TARGET["hypothesis"],
        "open",  # the survival of the comparison is the open non-perturbative step
        problem="ym-mass-gap",
        reason=f"naive comparison bound {result['naive_bound']:.4f} is negative; survival needs the "
               f"antipode's measure suppression (Wang's criterion)",
        produced_by="gaussian-comparison",
    )
    return {"target": TARGET["hypothesis"], "typed_inequality": TARGET["typed_inequality"],
            **result, "status": "open — the comparison must survive the non-linearity (Wang's criterion)"}
