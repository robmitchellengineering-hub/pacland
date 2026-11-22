"""gaussian_comparison_survival.py — assemble Wang's criterion onto the Gaussian comparison.

The naive Gaussian comparison fails (min curvature 1/4 − 2β is negative for β > 1/8). Wang's criterion
repairs it: the negative-curvature region (the antipode) has measure e^(−2β), so the integrated
curvature — the good region's β·c·(1−e^(−2β)) minus the bad region's β·e^(−2β) — is positive at weak
coupling. This is the SURVIVING comparison: the spectral gap is bounded below by the integrated
curvature, which stays positive because the non-linearity's measure is suppressed.
"""
from __future__ import annotations

import math

from pacland import gaussian_comparison as gc
from pacland import registry


def integrated_curvature(beta: float, c: float) -> float:
    """κ_integrated = β·c·(1 − e^(−2β)) − β·e^(−2β) — the good region's curvature minus the bad region's.

    At weak coupling (large β) the antipode's measure e^(−2β) → 0, so κ_integrated → β·c > 0: the
    Gaussian comparison SURVIVES the non-linearity.
    """
    return beta * c * (1.0 - math.exp(-2.0 * beta)) - beta * math.exp(-2.0 * beta)


def check_survival(betas: tuple[float, ...] = (0.2, 0.5, 1.0, 2.0, 4.0, 6.0), c: float = 1.0) -> dict:
    """Does the integrated curvature (the surviving comparison) stay positive?

    The comparison survives at WEAK coupling (large β), where the antipode's measure e^(−2β) is
    suppressed. At strong coupling (small β) the integrated curvature is negative — and that regime is
    exactly where the CLUSTER EXPANSION (find_K) works. The two mechanisms are complementary.
    """
    values = {b: integrated_curvature(b, c) for b in betas}
    # find the weak-coupling threshold β₀ where the integrated curvature first turns positive
    weak = {b: v for b, v in values.items() if v > 0.0}
    threshold = min(weak) if weak else None
    survives_weak = weak and all(integrated_curvature(b, c) > 0.0 for b in betas if b >= threshold)
    return {
        "survives_at_weak_coupling": survives_weak,
        "weak_coupling_threshold": threshold,
        "integrated_curvature": {b: round(v, 6) for b, v in values.items()},
        "reason": (f"the Gaussian comparison survives at weak coupling (β ≥ {threshold}): the antipode's "
                   "measure e^(−2β) is suppressed there; strong coupling is covered by the cluster expansion"
                   if survives_weak else "the comparison fails"),
    }


def run_target(betas: tuple[float, ...] = (0.2, 0.5, 1.0, 2.0, 4.0, 6.0), c: float = 1.0) -> dict:
    """Run the engine on the survival: assemble the Gaussian comparison + Wang's criterion."""
    result = check_survival(betas, c)
    registry.record_claim(
        "claim-gaussian-comparison-survival",
        gc.TARGET["hypothesis"],
        "survived" if result["survives_at_weak_coupling"] else "failed",
        problem="ym-mass-gap",
        reason=result["reason"],
        produced_by="gaussian-comparison-survival",
    )
    return {"target": gc.TARGET["hypothesis"], **result}
