"""cluster_expansion_constant.py — point the engine at K, the cluster-expansion convergence constant.

The cluster expansion converges when the Mayer condition holds: the sum of cluster weights is < 1. The
convergence constant K is the boundary where that sum reaches 1 — equivalently, the radius of convergence
in the activity `z(β)`. Deriving K is a COMBINATORIAL problem (the Mayer expansion: counting clusters of
each size with their gauge-group weights), and it is the single open quantity that turns the candidate
`m/Λ ≥ t·c − K·e^(−2β)/β` into an actual bound. This module encodes the structure, the target, and the
falsifier — and states the derivation path (the cluster-weight combinatorics) rather than fabricating K.
"""
from __future__ import annotations

import math

from pacland import registry


def activity(beta: float) -> float:
    """The cluster-expansion activity z(β) = e^(−β): the weight of a single-plaquette cluster."""
    return math.exp(-beta)


def mayer_condition(cluster_sum: float) -> bool:
    """The Mayer condition: the cluster sum < 1 ⟹ the expansion converges (its remainder is bounded)."""
    return cluster_sum < 1.0


def convergence_radius_from_activity(z: float) -> float:
    """The convergence radius ρ is the activity value at which the Mayer sum reaches 1; K = 1/ρ is the
    convergence constant (the prefactor in the bound). For z < ρ the expansion converges and the
    correlation decays exponentially with a V-independent constant."""
    return 1.0 / z if z > 0.0 else float("inf")


TARGET = {
    "hypothesis": "the cluster-expansion convergence constant K (the radius of convergence in the "
                  "activity) is a finite, V-independent constant",
    "open_quantity": "K — the cluster-expansion convergence constant",
    "derivation_path": "the Mayer expansion: count the clusters of each size with their SU(N) character "
                       "weights, and locate where the Mayer sum reaches 1",
    "falsifier": "an activity z where the Mayer sum ≥ 1 (the expansion diverges) or a volume where the "
                 "convergence constant becomes V-dependent",
    "role_in_bound": "K replaces the union bound's V·e^(−2β) with K·e^(−2β), making m/Λ ≥ t·c − "
                     "K·e^(−2β)/β volume-uniform",
}


def run_target(beta_boundary: float = 1.0, probe_betas: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0)) -> dict:
    """Run the engine on the K target: locate where the Mayer condition (cluster sum < 1) holds.

    This is the honest scaffold: the cluster sum is the activity z(β) summed over cluster sizes with their
    combinatorial weights. The ACTUAL weights are the SU(N) character-expansion coefficients (the open
    combinatorics); here we state the structure and the falsifier, not a fabricated K.
    """
    activities = {b: activity(b) for b in probe_betas}
    # the Mayer condition on a SINGLE-plaquette cluster is z < 1 (trivially true for β > 0);
    # the non-trivial content is the MULTI-cluster combinatorics that determines the actual radius.
    scaffold = {b: {"activity": round(z, 6), "single_cluster_converges": z < 1.0}
                for b, z in activities.items()}
    registry.record_claim(
        "claim-cluster-expansion-constant-K",
        TARGET["hypothesis"],
        "open",  # K is not derived — it is the open quantity
        problem="ym-mass-gap",
        reason="K is the cluster-expansion convergence constant; its value needs the Mayer-expansion "
               "combinatorics (the SU(N) character weights), which is the open step",
        produced_by="cluster-expansion-constant",
    )
    return {"target": TARGET["open_quantity"], "activities": scaffold,
            "derivation_path": TARGET["derivation_path"],
            "status": "open — K requires the Mayer-expansion combinatorics"}
