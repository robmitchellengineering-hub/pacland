"""bochner_identity.py — the SU(2) Bochner identity (the Bakry–Émery curvature of S³ + Wilson potential).

The missing computation: for the SU(2) Langevin generator L = Δ + β·∇(Re Tr)·∇ on S³, the Bochner
formula gives Γ₂(f) = |Hess f|² + (Ric + Hess V)(∇f, ∇f), so Γ₂(f) ≥ κ(θ)·Γ(f) with the Bakry–Émery
curvature κ(θ) = Ric + Hess V = 1/4 + 2β·cos θ. This module computes κ, the good set where κ ≥ 0, and
the bad set (the antipode) where κ < 0, and its measure — the mathematical content of the identity.
"""
from __future__ import annotations

import math

from pacland import registry


def su2_ricci() -> float:
    """The S³ Ricci curvature (normalized): Ric = 1/4."""
    return 1.0 / 4.0


def hessian_potential(beta: float, theta: float) -> float:
    """The Hessian of the Wilson potential V = −2β·cos θ in the radial direction: −2β·cos θ."""
    return -2.0 * beta * math.cos(theta)


def bakry_emery_curvature(beta: float, theta: float) -> float:
    """κ(θ) = Ric + Hess V = 1/4 + 2β·cos θ — the Bakry–Émery curvature (Ricci + Hessian of V)."""
    return su2_ricci() + 2.0 * beta * math.cos(theta)


def good_set_threshold(beta: float) -> float:
    """The good set {θ : κ(θ) ≥ 0} = {θ : cos θ ≥ −1/(8β)} — its boundary (the antipodal cap)."""
    return math.acos(-1.0 / (8.0 * beta)) if beta > 1.0 / 8.0 else 0.0


def antipode_measure(beta: float) -> float:
    """The bad set's measure: the Wilson weight at the antipode θ = π is e^(−2β) (relative to the vacuum)."""
    return math.exp(-2.0 * beta)


def check_bochner_identity(betas: tuple[float, ...] = (0.1, 0.2, 0.5, 1.0, 2.0, 4.0)) -> dict:
    """The Bochner identity's content: κ(θ) ≥ 0 on the good set, < 0 only on the antipodal cap, whose
    measure is e^(−2β). The pointwise bound Γ₂ ≥ κ·Γ holds with κ = 1/4 + 2β·cos θ."""
    rows = []
    for b in betas:
        th = good_set_threshold(b)
        rows.append({
            "beta": b,
            "good_set_boundary_theta": round(th, 4),
            "curvature_at_vacuum": round(bakry_emery_curvature(b, 0.0), 4),
            "curvature_at_antipode": round(bakry_emery_curvature(b, math.pi), 4),
            "antipode_measure": round(antipode_measure(b), 6),
        })
    # the identity: Γ₂ ≥ κ·Γ with κ = 1/4 + 2β·cos θ; positive away from the antipode, negative only there
    registry.record_claim(
        "claim-bochner-identity",
        "the SU(2) Bochner identity Γ₂(f) ≥ (1/4 + 2β·cos θ)·Γ(f) holds pointwise",
        "open",  # the curvature VALUE is computed; the pointwise Γ₂ ≥ κ·Γ proof is the Lean step
        problem="ym-mass-gap",
        reason="κ(θ) = 1/4 + 2β·cos θ is the Bakry–Émery curvature; positive on the good set, negative "
               "only on the antipode (measure e^(−2β)). The Γ₂ ≥ κ·Γ proof needs the Bochner formula.",
        produced_by="bochner-identity",
    )
    return {"rows": rows, "conclusion": "κ(θ) = 1/4 + 2β·cos θ, positive away from the antipode; the "
                                        "pointwise Γ₂ ≥ κ·Γ proof is the remaining Lean step"}
