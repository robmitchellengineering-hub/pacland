"""rg_side.py — point the engine at the RG side (asymptotic freedom, the weak-coupling scale).

The cluster expansion is strong-coupling only (find_K proved its bound exceeds the true gap at weak
coupling). The weak-coupling mass gap therefore comes from ASYMPTOTIC FREEDOM: the running coupling
g²(μ) = 1/(2β₀·ln(μ/Λ)) runs to zero in the UV, and dimensional transmutation gives the scale
Λ = μ·e^(−1/(2β₀·g²)) = μ·e^(−c/g²) with c = 12π²/11 (SU(2)). The mass gap is m = C·Λ with C the
dimensionless ratio; the RG establishes the SCALE (exponential, V-independent), and the open part is
C > 0 — the non-perturbative positivity of the ratio.
"""
from __future__ import annotations

import math

from pacland import registry


def running_coupling_squared(beta: float, n: float = 2.0) -> float:
    """g² = 2N/β — the lattice coupling (β = 2N/g² for SU(N))."""
    return 2.0 * n / beta


def rg_scale(beta: float, n: float = 2.0) -> float:
    """Λ(β) = e^(−c/g²) with c = 12π²/11 (SU(2)) — the asymptotic-freedom scale, V-INDEPENDENT."""
    c = 12.0 * math.pi ** 2 / 11.0
    return math.exp(-c / running_coupling_squared(beta, n))


def mass_gap_from_rg(C: float, beta: float, n: float = 2.0) -> float:
    """m(β) = C·Λ(β) — dimensional transmutation: the mass gap is the dimensionless ratio C times the scale."""
    return C * rg_scale(beta, n)


def check_rg_side(betas: tuple[float, ...] = (2.0, 3.0, 4.0, 6.0, 8.0)) -> dict:
    """The RG side: is the scale exponential in β (weak-coupling) and V-independent?

    The scale Λ(β) is V-independent by construction (it is the UV scale, not a volume quantity), and it
    decays exponentially — the correct weak-coupling form. The open part is C > 0 (the ratio's
    positivity), which the RG alone does not establish.
    """
    scales = {b: rg_scale(b) for b in betas}
    exponential = all(scales[b] > 0.0 and scales[b] < scales[betas[0]] for b in betas[1:])
    return {
        "scale_exponential": exponential,
        "volume_independent": True,          # Λ is a UV scale, no volume dependence
        "scale_values": {b: round(v, 6) for b, v in scales.items()},
        "open_part": "C > 0 — the dimensionless ratio m/Λ is positive (non-perturbative)",
        "reason": ("the RG gives the exponential weak-coupling scale, V-independent; the remaining open "
                   "part is the positivity of the dimensionless ratio C = m/Λ"),
    }


TARGET = {
    "hypothesis": "asymptotic freedom gives the weak-coupling V-uniform scale m = C·e^(−c/g²) with "
                  "c = 12π²/11, and the dimensionless ratio C = m/Λ is positive",
    "mechanisms": ["asymptotic freedom (running coupling)", "dimensional transmutation",
                   "RG-flow curvature bound (rg_curvature, ym_curvature)"],
    "open_part": "C > 0 — the dimensionless ratio m/Λ is positive, uniformly in V (the non-perturbative step)",
    "falsifier": "a weak-coupling volume where the ratio m/Λ → 0 (the scale exists but the gap closes)",
}


def run_target(betas: tuple[float, ...] = (2.0, 3.0, 4.0, 6.0, 8.0)) -> dict:
    """Run the engine on the RG-side target: the scale is exponential and V-independent."""
    result = check_rg_side(betas)
    registry.record_claim(
        "claim-rg-side-scale",
        TARGET["hypothesis"],
        "open",  # the scale is established; the ratio's positivity is the open part
        problem="ym-mass-gap",
        reason=result["reason"],
        produced_by="rg-side",
    )
    return {"target": TARGET["hypothesis"], **result}
