"""find_K.py — derive K (the cluster-expansion convergence constant) and its honest consequence.

The SU(2) cluster-expansion activity is `u(β) = I₂(2β)/I₁(2β)` (the modified-Bessel ratio). The cluster
expansion converges for `u < K` (K = the convergence radius) and gives the mass-gap bound
`m(β) ≥ −log u(β)`. The honest result, computed: this is the STRONG-coupling bound (~ log(1/β)), and it
becomes INVALID at weak coupling — `−log u(β)` exceeds the true exponentially-small mass gap there. So K
is a strong-coupling radius, and the cluster expansion alone cannot establish the weak-coupling scale
`e^(−cβ)`; that needs asymptotic freedom (the RG), not the cluster expansion.
"""
from __future__ import annotations

import math

from scipy.special import ive  # modified Bessel function of the first kind

from pacland import registry
from pacland import bound_search as bs


def activity(beta: float) -> float:
    """u(β) = I₂(2β)/I₁(2β) — the SU(2) cluster-expansion activity (the character coefficient)."""
    return ive(2, 2.0 * beta) / ive(1, 2.0 * beta)


def cluster_bound(beta: float) -> float:
    """m(β) ≥ −log u(β) — the cluster-expansion mass-gap lower bound."""
    return -math.log(activity(beta))


def referee(beta: float) -> float:
    """The known-answer mass gap m(β) = 25.28·e^(−1.182β)."""
    return bs.referee(beta)


def find_K(betas: tuple[float, ...] = (0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0)) -> dict:
    """Compute the cluster-expansion bound across β and test where it is a VALID lower bound (≤ referee).

    K is the convergence radius in the activity u; the bound is valid only while u(β) < K. The computed
    result: the bound is valid at strong coupling (small β) and becomes INVALID at weak coupling (large
    β), where −log u(β) exceeds the exponentially-small truth.
    """
    rows = []
    for b in betas:
        u = activity(b)
        cb = cluster_bound(b)
        m = referee(b)
        rows.append({"beta": b, "u": round(u, 6), "cluster_bound": round(cb, 6),
                     "referee": round(m, 6), "valid_lower_bound": cb <= m})
    valid = [r for r in rows if r["valid_lower_bound"]]
    conclusion = ("the cluster-expansion bound m ≥ −log u(β) is a valid lower bound only at strong "
                  "coupling (β ≤ ~4); at weak coupling it exceeds the true mass gap, so K is a "
                  "strong-coupling convergence radius and the cluster expansion cannot reach e^(−cβ)")
    registry.record_claim(
        "claim-cluster-expansion-K",
        "K is the strong-coupling convergence radius; the bound m ≥ −log u(β) is invalid at weak coupling",
        "failed",  # as a weak-coupling bound it fails
        problem="ym-mass-gap",
        reason=conclusion,
        produced_by="find-K",
    )
    return {"rows": rows, "n_valid": len(valid), "conclusion": conclusion}
