"""SU(2) 0++ glueball mass — the 'cost of the first glueball' (the mass-gap VALUE).

Runs the SU(2) lattice MC (reusing lattice_ym_su2), measures the connected
plaquette-plaquette correlation in the time direction, and extracts the effective mass
m_eff(dt) = -ln( C(dt+1) / C(dt) ). The plateau at large dt is the glueball mass m in
lattice units; divide by sqrt(sigma) (from measure_string_tension) for m/sqrt(sigma).

Usage:
    python3 scripts/glueball_mass.py N beta n_sweeps n_meas [seed]

This is the numerical half of the mass-gap problem — independent of the Lean existence proof,
and embarrassingly parallel (run many seeds on the mesh and average).
"""
from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, "src")
from pacland.lattice_ym_su2 import metropolis, plaquette_trace, random_su2  # noqa: E402


def glueball_op(links, t):
    """The 0++ glueball operator at time slice t: the sum of SPATIAL plaquettes over
    all spatial sites. The time direction is 0; spatial directions are 1..d-1."""
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
    # thermalize
    links = metropolis(links, beta, rng, n_sweeps)

    # accumulate G(t) and G(t)^2 per time slice, plus the cross-correlations
    g_sum = np.zeros(N)
    g_sq = np.zeros(N)
    # connected correlator: <G(t)G(0)> - <G>^2, accumulate <G(t)G(0)> via the products
    cross = np.zeros(N)  # <G(t) G(0)> (translation-averaged over t0)
    for _ in range(n_meas):
        links = metropolis(links, beta, rng, 3)
        g = np.array([glueball_op(links, t) for t in range(N)])
        g_sum += g
        g_sq += g * g
        # <G(t) G(0)> for all t, then translation-average: sum over t0 of G(t0+t)G(t0)
        for dt in range(N):
            cross[dt] += np.sum(g * np.roll(g, -dt))

    g_mean = g_sum / n_meas            # <G(t)> per time slice
    g_bar = float(np.mean(g_mean))     # translation-averaged <G>
    # <G(0) G(dt)> = cross[dt] / (n_meas * N); connected = <G(0)G(dt)> - <G>^2
    c_connected = cross / (n_meas * N) - g_bar ** 2
    c_connected = np.maximum(c_connected, 1e-12)
    m_eff = np.array([-np.log(c_connected[dt + 1] / c_connected[dt])
                      for dt in range(N - 1)])
    return c_connected, m_eff, g_bar


def main(argv: list[str]) -> int:
    N = int(argv[0]) if len(argv) > 0 else 6
    beta = float(argv[1]) if len(argv) > 1 else 2.4
    n_sweeps = int(argv[2]) if len(argv) > 2 else 30
    n_meas = int(argv[3]) if len(argv) > 3 else 200
    seed = int(argv[4]) if len(argv) > 4 else 0
    c, m_eff, gbar = glueball_correlation(N=N, beta=beta, n_sweeps=n_sweeps, n_meas=n_meas, seed=seed)
    print(f"SU(2) glueball mass  N={N} beta={beta} sweeps={n_sweeps} meas={n_meas} seed={seed}")
    print(f"  <G> = {gbar:.4f}")
    print("  dt  C(dt)         m_eff(dt)")
    for dt in range(len(m_eff)):
        print(f"  {dt:<3} {c[dt]:.4e}   {m_eff[dt]:.4f}")
    # plateau = last effective mass (furthest from the noise)
    print(f"  glueball mass m (lattice units) ~ {m_eff[-2]:.4f}  (effective-mass plateau, last two bins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
