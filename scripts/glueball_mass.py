"""SU(2) 0++ glueball mass — the 'cost of the first glueball' (the mass-gap VALUE).

Self-contained: inlines the SU(2) lattice MC (quaternion Wilson action, Metropolis) so it runs
anywhere with only numpy. Measures the connected spatial-plaquette correlation in the time direction
and extracts the effective mass m_eff(dt) = -ln( C(dt+1) / C(dt) ). The plateau at large dt is the
glueball mass m in lattice units.

Usage:
    python3 glueball_mass.py N beta n_sweeps n_meas [seed]

This is the numerical half of the mass-gap problem — independent of the Lean existence proof, and
embarrassingly parallel (run many seeds and average).
"""
from __future__ import annotations

import sys

import numpy as np


# --- SU(2) quaternion lattice MC (inlined; no repo import) ---
def qmul(p, q):
    a0, a1, a2, a3 = p
    b0, b1, b2, b3 = q
    return np.array([a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2,
                     a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0])


def qconj(p):
    return np.array([p[0], -p[1], -p[2], -p[3]])


def random_su2(rng):
    v = rng.normal(size=4)
    return v / np.linalg.norm(v)


def plaquette_trace(links, mu, nu, idx):
    d, N = links.shape[0], links.shape[1]
    x = list(idx)
    xm = list(x); xm[mu] = (xm[mu] + 1) % N; xm = tuple(xm)
    xn = list(x); xn[nu] = (xn[nu] + 1) % N; xn = tuple(xn)
    u = links[mu][tuple(x)]
    u = qmul(u, links[nu][xm])
    u = qmul(u, qconj(links[mu][xn]))
    u = qmul(u, qconj(links[nu][tuple(x)]))
    return 2.0 * u[0]


def metropolis(links, beta, rng, n_sweeps):
    d, N = links.shape[0], links.shape[1]
    for _ in range(n_sweeps):
        for mu in range(d):
            for flat in range(N**d):
                idx = np.unravel_index(flat, (N,) * d)
                old = links[mu][idx].copy()
                new = qmul(random_su2(rng), old)
                dS = 0.0
                for nu in range(d):
                    if nu == mu:
                        continue
                    for base in (0, -1):
                        x = list(idx); x[nu] = (x[nu] + base) % N; x = tuple(x)
                        s_old = plaquette_trace(links, mu, nu, x)
                        links[mu][idx] = new
                        s_new = plaquette_trace(links, mu, nu, x)
                        links[mu][idx] = old
                        dS += -0.5 * (s_new - s_old)
                dS *= beta
                if not (dS > 0 and rng.random() > np.exp(-dS)):
                    links[mu][idx] = new
    return links


def glueball_op(links, t):
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
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(d * N**d)])
    links = links.reshape((d,) + (N,) * d + (4,))
    links = metropolis(links, beta, rng, n_sweeps)

    g_sum = np.zeros(N)
    cross = np.zeros(N)
    for _ in range(n_meas):
        links = metropolis(links, beta, rng, 3)
        g = np.array([glueball_op(links, t) for t in range(N)])
        g_sum += g
        for dt in range(N):
            cross[dt] += np.sum(g * np.roll(g, -dt))

    g_mean = g_sum / n_meas
    g_bar = float(np.mean(g_mean))
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
    print(f"  glueball mass m (lattice units) ~ {m_eff[-2]:.4f}  (plateau, last two bins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
