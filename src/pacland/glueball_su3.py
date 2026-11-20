"""SU(3) 0++ glueball mass — the effective mass from the spatial-plaquette correlation.

Mirrors ``glueball.py`` (SU(2)) but on SU(3) links, so ``m/sqrt(sigma)`` can be compared across gauge
groups (the large-N ratio falsifier).
"""
from __future__ import annotations

import numpy as np

from pacland import lattice_ym_su3 as su3


def glueball_op_su3(links: np.ndarray, t: int) -> float:
    """The 0++ glueball operator at time slice t: the sum of SPATIAL plaquettes."""
    d, N = links.shape[0], links.shape[1]
    total = 0.0
    for flat in range(N ** (d - 1)):
        xyz = np.unravel_index(flat, (N,) * (d - 1))
        idx = (t,) + tuple(xyz)
        for mu in range(1, d):
            for nu in range(mu + 1, d):
                total += su3.plaquette_trace(links, mu, nu, idx)
    return total


def glueball_mass_su3(beta: float, N: int = 6, n_sweeps: int = 20, n_meas: int = 100,
                      seed: int = 0, smear: bool = True) -> float:
    """The SU(3) glueball mass in lattice units: the median of the MIDDLE effective-mass bins (where
    the backward-propagating state is negligible). Spatial APE smearing is ON by default — it is the
    standard fix for the connected-correlator signal-to-noise collapse that made the raw mass noise."""
    rng = np.random.default_rng(seed)
    links = np.array([su3.random_su3(rng) for _ in range(4 * N ** 4)])
    links = links.reshape((4,) + (N,) * 4 + (3, 3))
    links = su3.metropolis(links, beta, rng, n_sweeps)

    g_sum = np.zeros(N)
    cross = np.zeros(N)
    for _ in range(n_meas):
        links = su3.metropolis(links, beta, rng, 3)
        smeared = su3.ape_smear(links) if smear else links
        g = np.array([glueball_op_su3(smeared, t) for t in range(N)])
        g_sum += g
        for dt in range(N):
            cross[dt] += np.sum(g * np.roll(g, -dt))
    g_mean = g_sum / n_meas
    g_bar = float(np.mean(g_mean))
    c_connected = np.maximum(cross / (n_meas * N) - g_bar ** 2, 1e-12)
    m_eff = np.array([-np.log(c_connected[dt + 1] / c_connected[dt]) for dt in range(N - 1)])
    lo, hi = N // 3, 2 * N // 3
    return float(np.median(m_eff[lo:hi]))


__all__ = ["glueball_op_su3", "glueball_mass_su3"]
