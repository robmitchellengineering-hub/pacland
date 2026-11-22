"""full_lattice_ratio.py — the full-lattice extension of the ratio bound (the V → ∞ obstacle, honestly).

The 1-plaquette candidate m/Λ ≥ t·c − e^(−2β)/β is positive and V-independent by construction. The full
lattice is the real test: with V plaquettes, the naive union bound gives a correction V·e^(−2β), so the
ratio m/Λ ≥ t·c − V·e^(−2β)/β is positive only while V grows slower than e^(2β). Removing that
V-dependence — so the bound holds uniformly in V — is precisely the role of the cluster expansion (whose
convergence is V-independent). This module states that obstacle and the condition for volume-uniformity.
"""
from __future__ import annotations

import math

from pacland import volume_uniform_ratio as vur


def full_lattice_correction(V: int, beta: float) -> float:
    """The naive (union-bound) full-lattice antipode correction: V plaquettes, each bad with measure
    e^(−2β), so the bad region has measure ≲ V·e^(−2β)."""
    return V * math.exp(-2.0 * beta)


def full_lattice_ratio(t: float, c: float, V: int, beta: float) -> float:
    """The full-lattice candidate m/Λ ≥ t·c − V·e^(−2β)/β (naive union bound)."""
    return max(0.0, t * c - V * math.exp(-2.0 * beta) / beta)


def volume_uniformity_condition(t: float, c: float, V: int, beta: float) -> bool:
    """The ratio is positive at (V, β) iff V·e^(−2β) < t·c·β, i.e. V < t·c·β·e^(2β).

    Uniformity in V FAILS under the union bound: as V → ∞ faster than e^(2β), the correction overtakes
    t·c. The volume-uniform bound therefore needs the cluster expansion's V-INDEPENDENT correction, not
    the union bound."""
    return V * math.exp(-2.0 * beta) < t * c * beta


def check_full_lattice_uniform(t: float, c: float, betas: tuple[float, ...],
                               volumes: tuple[int, ...]) -> dict:
    """Run the naive full-lattice candidate across (V, β) and report where uniformity breaks."""
    c = c if c is not None else vur.asymptotic_freedom_exponent(2.0) if c is None else c
    rows = []
    uniform = True
    for V in volumes:
        for b in betas:
            ratio = full_lattice_ratio(t, c, V, b)
            ok = volume_uniformity_condition(t, c, V, b)
            uniform = uniform and ok
            rows.append({"V": V, "beta": b, "ratio": ratio, "positive": ratio > 0.0})
    return {
        "uniform_under_union_bound": uniform,
        "rows": rows,
        "obstacle": ("the union-bound correction V·e^(−2β) breaks volume-uniformity: the bound holds only "
                     "for V < t·c·β·e^(2β). The cluster expansion (V-independent convergence) is the "
                     "mechanism that removes this V-dependence."),
    }
