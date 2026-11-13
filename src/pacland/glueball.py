"""SU(2) 0++ glueball mass — the effective mass from the plaquette-plaquette correlation.

The glueball mass ``m`` in lattice units; ``m/sqrt(sigma)`` is the RG-invariant ratio whose
weak-coupling plateau is the continuum prediction.
"""
from __future__ import annotations

import numpy as np

from pacland.lattice_ym_su2 import metropolis, plaquette_trace, random_su2


def glueball_op(links, t):
    """The 0++ glueball operator at time slice t: the sum of SPATIAL plaquettes."""
    d, N = links.shape[0], links.shape[1]
    total = 0.0
    for flat in range(N ** (d - 1)):
        xyz = np.unravel_index(flat, (N,) * (d - 1))
        idx = (t,) + tuple(xyz)
        for mu in range(1, d):
            for nu in range(mu + 1, d):
                total += plaquette_trace(links, mu, nu, idx)
    return total


def glueball_correlation(d=4, N=6, beta=2.4, n_sweeps=30, n_meas=200, seed=0):
    """Measure the connected glueball correlation C(dt) and effective mass m_eff(dt)."""
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(d * N**d)])
    links = links.reshape((d,) + (N,) * d + (4,))
    links = metropolis(links, beta, rng, n_sweeps)

    g_sum = np.zeros(N)
    g_sq = np.zeros(N)
    cross = np.zeros(N)
    for _ in range(n_meas):
        links = metropolis(links, beta, rng, 3)
        g = np.array([glueball_op(links, t) for t in range(N)])
        g_sum += g
        g_sq += g * g
        for dt in range(N):
            cross[dt] += np.sum(g * np.roll(g, -dt))

    g_mean = g_sum / n_meas
    g_bar = float(np.mean(g_mean))
    c_connected = cross / (n_meas * N) - g_bar ** 2
    c_connected = np.maximum(c_connected, 1e-12)
    m_eff = np.array([-np.log(c_connected[dt + 1] / c_connected[dt])
                      for dt in range(N - 1)])
    return c_connected, m_eff, g_bar


def glueball_mass(beta, N=6, n_sweeps=30, n_meas=200, seed=0):
    """The glueball mass in lattice units: the effective-mass plateau (last two bins)."""
    _, m_eff, _ = glueball_correlation(N=N, beta=beta, n_sweeps=n_sweeps, n_meas=n_meas, seed=seed)
    return float(m_eff[-2])
