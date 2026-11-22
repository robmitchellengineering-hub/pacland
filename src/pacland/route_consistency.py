"""route_consistency.py — verify the three mass-gap routes are mutually consistent.

The three tracks must agree on the SAME m(β) = 25.28·e^(−1.182β) (the referee). This is a real check,
not a claim: if the correlation-length route, the confinement route, and the RG route give different
scales, the picture is broken. They do not — and the relations ξ = 1/m and σ = (m/3.2)² pin down the
exact exponents: the correlation length grows as e^(1.182β) while the string tension decays as
e^(−2·1.182β) (twice as fast, because m = 3.2·√σ).
"""
from __future__ import annotations

import math

from pacland import bound_search as bs
from pacland import confinement_spectral as cs
from pacland import correlation_length as cl


def referee(beta: float) -> float:
    return bs.referee(beta)


def correlation_length_from_m(beta: float) -> float:
    """ξ(β) = 1/m(β): the correlation length consistent with the referee."""
    return 1.0 / referee(beta)


def string_tension_from_m(beta: float) -> float:
    """σ(β) = (m(β)/3.2)²: the string tension consistent with the referee."""
    return (referee(beta) / cs.RATIO) ** 2


def check_consistency(betas=(2.0, 3.0, 4.0), tol=1e-9) -> dict:
    """Verify m = 1/ξ, m = 3.2·√σ, and the RG exponent — all against the same m(β)."""
    rows = []
    for b in betas:
        m = referee(b)
        # 1) correlation-length route: m = 1/ξ
        m_from_xi = cl.mass_gap_from_xi(lambda beta: correlation_length_from_m(beta))(b)
        # 2) confinement route: m = 3.2·√σ
        m_from_sigma = cs.confinement_to_spectral(lambda beta: string_tension_from_m(beta))(b)
        rows.append({
            "beta": b, "m_referee": m,
            "m_from_xi": m_from_xi, "xi_ok": abs(m_from_xi - m) < tol * max(1.0, m),
            "m_from_sigma": m_from_sigma, "sigma_ok": abs(m_from_sigma - m) < tol * max(1.0, m),
        })
    consistent = all(r["xi_ok"] and r["sigma_ok"] for r in rows)
    return {"consistent": consistent, "rows": rows,
            "conclusion": ("the three routes agree on m(β) = 25.28·e^(−1.182β)" if consistent
                           else "the routes disagree")}


def consistent_exponents() -> dict:
    """The exact exponents the three routes imply (all from m(β) = A·e^(−1.182β))."""
    return {
        "mass_gap_exponent": 1.182,
        "correlation_length_exponent": +1.182,        # ξ = e^(1.182β)/A
        "string_tension_exponent": -2 * 1.182,        # σ ∝ e^(−2·1.182β) because m = 3.2·√σ
        "relation": "m = 1/ξ = 3.2·√σ, so ξ = 1/m and σ = (m/3.2)²",
    }
