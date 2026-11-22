"""ratio_positivity.py — point the engine at C > 0 (the dimensionless ratio is positive, V-uniform).

C = m/Λ is the dimensionless mass gap — the ratio of the mass gap to the asymptotic-freedom scale.
Because Λ > 0, C > 0 is EQUIVALENT to m > 0: proving the ratio is positive is proving the mass gap is
positive, which is the Clay problem's core. The mechanisms that establish it are (1) reflection
positivity — the transfer matrix is positive, so the spectral gap m > 0 — and (2) Wang's criterion — the
β-uniform spectral gap. The open step is the Osterwalder–Schrader ⟹ Wightman reconstruction in the
continuum (Rung B).
"""
from __future__ import annotations

import math

from pacland import registry
from pacland import rg_side as rs


def ratio(m_gap: float, scale: float) -> float:
    """C = m/Λ — the dimensionless ratio (the mass gap in units of the AF scale)."""
    return m_gap / scale if scale != 0.0 else float("inf")


def ratio_positive_iff_gap_positive(m_gap: float, scale: float) -> tuple[bool, bool]:
    """C > 0 ⟺ m > 0 (since Λ > 0): the equivalence that reduces C > 0 to the mass gap's positivity."""
    c_positive = ratio(m_gap, scale) > 0.0
    m_positive = m_gap > 0.0
    return c_positive, (c_positive == m_positive) if scale > 0.0 else False


TARGET = {
    "hypothesis": "C > 0 — the dimensionless ratio m/Λ is positive, uniformly in volume",
    "equivalent": "C > 0 ⟺ m > 0 (Λ > 0), so this is the mass gap's positivity — the Clay core",
    "mechanisms": ["reflection positivity (the transfer matrix is positive → m > 0)",
                   "Wang's criterion (the β-uniform spectral gap)"],
    "open_step": "the Osterwalder–Schrader ⟹ Wightman reconstruction in the continuum (Rung B)",
    "falsifier": "a volume or β where the ratio m/Λ → 0 (the spectral gap closes)",
}


def run_target(m_gap: float = 1.0, scale: float = 1.0) -> dict:
    """Run the engine on C > 0: state the equivalence and record the honest status.

    C > 0 is equivalent to m > 0 (the mass gap is positive). The mechanisms (reflection positivity,
    Wang's criterion) are the candidates; the open step is the OS ⟹ Wightman reconstruction, which is
    the non-perturbative core. This is recorded as OPEN — it is the Clay statement itself.
    """
    c_positive, equivalence = ratio_positive_iff_gap_positive(m_gap, scale)
    registry.record_claim(
        "claim-ratio-positivity-C",
        TARGET["hypothesis"],
        "open",  # C > 0 is the Clay core — not proven, not falsified
        problem="ym-mass-gap",
        reason=f"C = m/Λ is positive iff m > 0 (equivalence holds: {equivalence}); the proof needs the "
               f"OS ⟹ Wightman reconstruction (Rung B)",
        produced_by="ratio-positivity",
    )
    return {"target": TARGET["hypothesis"], "C_positive_for_test_gap": c_positive,
            "equivalence_holds": equivalence, "open_step": TARGET["open_step"],
            "status": "open — C > 0 is the Clay statement (mass-gap positivity)"}
