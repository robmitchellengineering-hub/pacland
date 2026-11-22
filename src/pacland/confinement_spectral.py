"""confinement_spectral.py — the confinement × spectral combination (m = 3.2·√σ).

The synthesis upgrade: instead of generic *products* of bound shapes, combine STRUCTURES with their real
mathematical relation. The confinement→spectral bridge is `m = 3.2·√σ`: a lower bound on the string
tension σ(β) gives a lower bound on the mass gap m(β). This is Track C's core mechanism, and it encodes
the correct scaling: the string tension decays with exponent `2·c` when the mass gap decays with `c`
(because `m = 3.2·√σ`), so a string-tension bound reaching `e^(−2.364β)` gives a mass-gap bound reaching
the referee's `e^(−1.182β)`.
"""
from __future__ import annotations

import math

from pacland import registry
from pacland import bound_search as bs

RATIO = 3.2  # m/√σ ≈ 3.2 (the known glueball-to-string-tension ratio)


def confinement_to_spectral(sigma_bound, ratio: float = RATIO):
    """m(β) = ratio·√σ(β): the string-tension lower bound → mass-gap lower bound."""
    return lambda beta: ratio * math.sqrt(max(0.0, sigma_bound(beta)))


def string_tension(sigma0: float, k: float):
    """A string-tension lower bound σ(β) = σ₀·e^(−kβ)."""
    return lambda beta: sigma0 * math.exp(-k * beta)


def search_confinement(sigma0_values: list[float], k_values: list[float],
                       source: str = "confinement-spectral") -> dict:
    """Search string-tension bounds σ = σ₀·e^(−kβ) → m = 3.2·√σ against the referee + record.

    The honest result: the derived mass-gap bound reaches the scale iff k = 2·1.182 = 2.364 (the string
    tension decays twice as fast as the mass gap), so the referee-equivalent is marked is_referee.
    """
    survivors: list[dict] = []
    failures: list[dict] = []
    for s0 in sigma0_values:
        for k in k_values:
            m_bound = confinement_to_spectral(string_tension(s0, k))
            r = bs.check_bound(m_bound)
            is_ref = abs(3.2 * math.sqrt(s0) - 25.28) < 1e-6 and abs(k / 2.0 - 1.182) < 1e-6
            entry = {"sigma0": s0, "k": k, "mass_amplitude": 3.2 * math.sqrt(s0),
                     **r, "is_referee": is_ref}
            (survivors if (r["survived"] and not is_ref) else failures).append(entry)
    conclusion = ("no new confinement-derived bound reaches the scale" if not survivors
                  else f"{len(survivors)} independent survivor(s)")
    registry.record_claim(
        "claim-mass-gap-confinement-spectral",
        "confinement × spectral: σ(β) ≥ σ₀·e^(−kβ) → m(β) ≥ 3.2·√σ₀·e^(−kβ/2)",
        "failed" if not survivors else "survived",
        problem="ym-mass-gap",
        reason=conclusion,
        produced_by="confinement-spectral",
    )
    return {"n_survivors": len(survivors), "n_failures": len(failures),
            "conclusion": conclusion, "survivors": survivors}
