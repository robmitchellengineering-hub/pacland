"""Hand-written finite-difference Kähler metric — sidesteps JAX/XLA autodiff.

The blocker in `limits.py`: the instanton-corrected Hessian/mass-matrix hangs (>200 s) because
JAX/XLA traces the second derivatives of the worldsheet-instanton prepotential `F_inst`. The fix
specified there is a *hand-written* metric: finite-difference the Kähler potential (which is
callable), then assemble the complex metric `g_iȷ̄ = ∂²K/∂z^i ∂z̄^ȷ̄` from the real Hessian.

No autodiff, no JAX: pure numpy. Validated against the STU analytic metric (diagonal,
`g_ii = 1/(4 Im τ_i²)`).
"""
from __future__ import annotations

import numpy as np


def real_hessian_of(K, z: list[complex], h: float = 1e-4) -> np.ndarray:
    """The Hessian of a real-valued `K(z)` in the 2n real coords (Re z_i, Im z_i), by central differences."""
    n = len(z)
    z0 = np.array([(c.real, c.imag) for c in z]).ravel()

    def k_of(x):
        zz = [complex(x[2 * i], x[2 * i + 1]) for i in range(n)]
        return float(K(zz))

    H = np.zeros((2 * n, 2 * n))
    for a in range(2 * n):
        for b in range(2 * n):
            xpp = z0.copy(); xpp[a] += h; xpp[b] += h
            xpm = z0.copy(); xpm[a] += h; xpm[b] -= h
            xmp = z0.copy(); xmp[a] -= h; xmp[b] += h
            xmm = z0.copy(); xmm[a] -= h; xmm[b] -= h
            H[a, b] = (k_of(xpp) - k_of(xpm) - k_of(xmp) + k_of(xmm)) / (4 * h * h)
    return 0.5 * (H + H.T)


def kahler_metric_fd(K, z: list[complex], h: float = 1e-4) -> np.ndarray:
    """The complex Kähler metric `g_iȷ̄ = ∂²K/∂z^i ∂z̄^ȷ̄`, hand-written, no autodiff.

    From the real Hessian `H` (coords Re z0, Im z0, Re z1, Im z1, …):

        g[i,j] = ¼ (H[2i,2j] + H[2i+1,2j+1] + i (H[2i,2j+1] − H[2i+1,2j]))
    """
    H = real_hessian_of(K, z, h)
    n = len(z)
    g = np.zeros((n, n), dtype=complex)
    for i in range(n):
        for j in range(n):
            g[i, j] = 0.25 * (H[2 * i, 2 * j] + H[2 * i + 1, 2 * j + 1]
                              + 1j * (H[2 * i, 2 * j + 1] - H[2 * i + 1, 2 * j]))
    return g


__all__ = ["real_hessian_of", "kahler_metric_fd"]
