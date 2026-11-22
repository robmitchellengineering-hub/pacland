"""renormalized_action.py — Rung A's reconciliation: why the mass gap follows 12π²/11, not 8π²/g².

The mass gap is set by the RG scale (dimensional transmutation), NOT by the single-instanton tunneling
amplitude. The two exponents are different objects:

  * the beta-function exponent  c = 1/(2β₀) = 24π²/(11N)  — the running coupling's scale, m ~ Λ;
  * the instanton action        S = 8π²/g²               — the single-instanton tunneling weight.

For SU(2), c = 12π²/11 ≈ 10.77 while 8π² ≈ 78.96 — the instanton action is 22/3 ≈ 7.33× larger. The
mass gap follows the beta function, not the instanton, because the gap is the SPECTRAL gap of the soft
mode (the collective instanton), whose renormalized action carries the running coupling's exponent —
not the single instanton's.
"""
from __future__ import annotations

import math


def beta0(n: float) -> float:
    """The one-loop β-function coefficient b₀ = 11N/(48π²)."""
    return 11.0 * n / (48.0 * math.pi ** 2)


def mass_gap_exponent(n: float) -> float:
    """The mass-gap exponent c = 1/(2b₀) = 24π²/(11N) — from the β-function (dimensional transmutation)."""
    return 1.0 / (2.0 * beta0(n))


def instanton_action() -> float:
    """The single-instanton action S = 8π²/g² (the exponent 8π² in the g² convention)."""
    return 8.0 * math.pi ** 2


def renormalized_scale(mu: float, lam: float, n: float) -> float:
    """The RG-invariant scale Λ = μ·e^(−c/g²(μ)) with c = 1/(2b₀) — the mass gap's scale, renormalized."""
    g2 = 1.0 / (2.0 * beta0(n) * math.log(mu / lam))
    return mu * math.exp(-mass_gap_exponent(n) / g2)


def reconcile(n: float = 2.0) -> dict:
    """State the reconciliation: the mass gap follows 12π²/11 (β-function), not 8π²/g² (instanton)."""
    c = mass_gap_exponent(n)
    s = instanton_action()
    return {
        "N": n,
        "mass_gap_exponent": c,          # 12π²/11 for SU(2)
        "instanton_exponent": s,         # 8π²
        "ratio_instanton_over_gap": s / c,  # 22/3 ≈ 7.33 for SU(2)
        "conclusion": (
            "the mass gap follows the β-function exponent c = 1/(2β₀), NOT the instanton 8π²/g²: "
            "the instanton is the single-tunneling amplitude (power-suppressed), while the mass gap is "
            "the soft mode's spectral gap, whose renormalized action carries the running coupling's "
            "exponent c = 1/(2β₀) = 12π²/11"
        ),
    }
