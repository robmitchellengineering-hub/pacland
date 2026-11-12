"""KKLT single-Kähler-modulus mass — the instanton-corrected mass gap.

The CS-side no-scale oracle (`potential_t6`) leaves the Kähler moduli flat (zero modes). The
instanton superpotential `W = W0 + A e^{-aT}` (a = 2π) lifts that flat direction, and the mass
of the stabilized Kähler modulus is the smallest nonzero mass the EFT predicts — the mass gap.

This computes it *without* the autodiff that hangs in `limits.py`: the Kähler metric is the
hand-written finite-difference `kahler_metric_fd`, and the SUSY minimum is the root of `D_T W = 0`
solved exactly. The mass is the canonically-normalized Hessian `m² = g^{-1} ∂²V/∂σ²` at that root.

The result is a *measurement of the free parameter W0*, not a derivation — consistent with the
"mass scale is a value, not a relation" theorem (MassGap.lean).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from .kahler_metric_fd import kahler_metric_fd

A_CYCLE = 2.0 * np.pi


def kaehler(z) -> float:
    """K = -3 ln(2 sigma), the single-Kähler-modulus Kähler potential (T = sigma, axion fixed at 0)."""
    sigma = z[0].real
    return float(-3.0 * np.log(2.0 * sigma))


def superpotential(sigma: float, W0: float, A: float) -> complex:
    """W = W0 + A e^{-a sigma}."""
    return W0 + A * np.exp(-A_CYCLE * sigma)


def potential(sigma: float, W0: float, A: float) -> float:
    """V = e^K (g^{-1} |D_T W|^2 - 3 |W|^2)."""
    g = kahler_metric_fd(kaehler, [sigma + 0j])[0, 0].real
    W = superpotential(sigma, W0, A)
    dK = -3.0 / (2.0 * sigma)
    dW = -A_CYCLE * A * np.exp(-A_CYCLE * sigma)
    DTW = dW + dK * W
    return float(np.exp(kaehler([sigma + 0j])) * (np.abs(DTW) ** 2 / g - 3.0 * np.abs(W) ** 2))


def stabilize(W0: float, A: float = 1.0) -> tuple[float, float]:
    """The SUSY AdS minimum: solve D_T W = 0 ⇔ A e^{-a sigma} (2 a sigma + 3) = -3 W0."""
    f = lambda s: A * np.exp(-A_CYCLE * s) * (2.0 * A_CYCLE * s + 3.0) + 3.0 * W0
    s = brentq(f, 1e-4, 100.0)
    return float(s), abs(f(s))


def mass_sq(sigma: float, W0: float, A: float = 1.0, h: float = 1e-4) -> float:
    """m² = g^{-1} ∂²V/∂σ² — the canonically-normalized Kähler-modulus mass²."""
    g = kahler_metric_fd(kaehler, [sigma + 0j])[0, 0].real
    d2 = (potential(sigma + h, W0, A) - 2 * potential(sigma, W0, A) + potential(sigma - h, W0, A)) / (h * h)
    return d2 / g


def mass_gap(W0: float, A: float = 1.0) -> dict:
    """The full measurement: stabilized volume, AdS V, and the mass gap."""
    sigma, resid = stabilize(W0, A)
    m2 = mass_sq(sigma, W0, A)
    return {"W0": W0, "A": A, "sigma": sigma, "susu_residual": resid,
            "V": potential(sigma, W0, A), "m2": m2, "mass": float(np.sqrt(max(m2, 0.0)))}


__all__ = ["kaehler", "superpotential", "potential", "stabilize", "mass_sq", "mass_gap"]
