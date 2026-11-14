"""SU(2) 0++ glueball mass — the effective mass from the plaquette-plaquette correlation.

The glueball mass ``m`` in lattice units; ``m/sqrt(sigma)`` is the RG-invariant ratio whose
weak-coupling plateau is the continuum prediction.
"""
from __future__ import annotations

import numpy as np

from pacland.lattice_ym_su2 import ape_smear, metropolis, plaquette_trace, random_su2


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


def glueball_correlation(d=4, N=6, beta=2.4, n_sweeps=30, n_meas=200, seed=0, n_smear=3):
    """Measure the connected glueball correlation C(dt) and effective mass m_eff(dt)."""
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(d * N**d)])
    links = links.reshape((d,) + (N,) * d + (4,))
    links = metropolis(links, beta, rng, n_sweeps)
    links = ape_smear(links, alpha=0.5, n_iter=n_smear)

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


def glueball_mass(beta, N=6, n_sweeps=30, n_meas=200, seed=0, n_smear=3):
    """The glueball mass in lattice units: the median of the MIDDLE effective-mass bins (where the
    backward-propagating state is negligible and the signal survives)."""
    _, m_eff, _ = glueball_correlation(N=N, beta=beta, n_sweeps=n_sweeps, n_meas=n_meas, seed=seed, n_smear=n_smear)
    lo, hi = N // 3, 2 * N // 3
    return float(np.median(m_eff[lo:hi]))


def glueball_variational(N=6, beta=2.4, n_sweeps=15, n_meas=200, seed=0, smears=(0, 3)):
    """Variational glueball mass via the GEVP: a basis of APE-smeared operators isolates the 0++
    ground state from the excited-state contamination that makes the single operator oscillate.

    Returns (masses, C, gbar): masses is the ground-state effective mass -ln(λ_max(t)/λ_max(t₀))/(t-t₀)."""
    from pacland.lattice_ym_su2 import ape_smear, metropolis, random_su2
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(4 * N**4)])
    links = links.reshape((4,) + (N,) * 4 + (4,))
    links = metropolis(links, beta, rng, n_sweeps)
    n_op = len(smears)
    C = np.zeros((n_op, n_op, N))
    g_mean = np.zeros((n_op, N))
    for _ in range(n_meas):
        links = metropolis(links, beta, rng, 3)
        gs = []
        for s in smears:
            sm = ape_smear(links, alpha=0.5, n_iter=s)
            gs.append(np.array([glueball_op(sm, t) for t in range(N)]))
        for i in range(n_op):
            g_mean[i] += gs[i]
            for j in range(n_op):
                for dt in range(N):
                    C[i][j][dt] += np.sum(gs[i] * np.roll(gs[j], -dt))
    g_mean /= n_meas
    gbar = np.array([g_mean[i].mean() for i in range(n_op)])
    for i in range(n_op):
        for j in range(n_op):
            C[i][j] = C[i][j] / (n_meas * N) - gbar[i] * gbar[j]
    # GEVP: C(t) v = λ C(t₀) v — ground state is the largest generalized eigenvalue.
    t0 = 1
    masses = []
    for t in range(t0 + 1, N // 2):
        Ct = C[:, :, t]
        Ct0 = C[:, :, t0]
        try:
            lam = np.linalg.eigvals(np.linalg.solve(Ct0, Ct))
            lam_max = float(np.max(np.abs(lam)))
            if lam_max > 1e-9:
                masses.append(-np.log(lam_max) / (t - t0))
        except np.linalg.LinAlgError:
            pass
    return masses, C, gbar
