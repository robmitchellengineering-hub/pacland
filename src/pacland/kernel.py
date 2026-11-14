"""Numba-accelerated SU(2) lattice kernel — the fast path for the MC.

Links are a flat float64 array of shape (d, N^d, 4) (unit quaternions). The sweep, staple and
plaquette are compiled; a xorshift128+ RNG avoids the numpy Generator (not Numba-compatible).
"""
from __future__ import annotations

import math

import numpy as np
import numba as nb


@nb.njit(inline="always")
def _next(state):
    s1 = state[0]
    s0 = state[1]
    state[0] = s0
    s1 ^= (s1 << np.uint64(23))
    state[1] = s1 ^ s0 ^ (s1 >> np.uint64(17)) ^ (s0 >> np.uint64(26))
    return (state[1] + s0) / 18446744073709551616.0


@nb.njit(inline="always")
def _rand4(state):
    """One unit quaternion from the RNG (Box-Muller on 4 gaussians, normalized)."""
    u1 = _next(state); u2 = _next(state); u3 = _next(state); u4 = _next(state)
    r = math.sqrt(-2.0 * math.log(1.0 - u1))
    th = 2.0 * math.pi * u2
    g0 = r * math.cos(th)
    g1 = r * math.sin(th)
    r2 = math.sqrt(-2.0 * math.log(1.0 - u3))
    th2 = 2.0 * math.pi * u4
    g2 = r2 * math.cos(th2)
    g3 = r2 * math.sin(th2)
    n = math.sqrt(g0*g0 + g1*g1 + g2*g2 + g3*g3)
    return (g0/n, g1/n, g2/n, g3/n)


@nb.njit(inline="always")
def _mul(a0, a1, a2, a3, b0, b1, b2, b3):
    return (a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0)


@nb.njit(inline="always")
def _shift(idx, d, N, axis, delta):
    """Row-major flat index of the neighbor: idx = c0*N^3 + c1*N^2 + c2*N + c3."""
    c3 = idx % N
    c2 = (idx // N) % N
    c1 = (idx // (N * N)) % N
    c0 = idx // (N * N * N)
    if axis == 0:
        c0 = (c0 + delta) % N
    elif axis == 1:
        c1 = (c1 + delta) % N
    elif axis == 2:
        c2 = (c2 + delta) % N
    else:
        c3 = (c3 + delta) % N
    return c0 * N * N * N + c1 * N * N + c2 * N + c3


@nb.njit(inline="always")
def _plaquette(links, d, N, mu, nu, idx):
    """Re Tr of the (mu,nu) plaquette at flat site idx (row-major)."""
    xm = _shift(idx, d, N, mu, 1)
    xn = _shift(idx, d, N, nu, 1)
    # U_mu(x) U_nu(x+mu) U_mu(x+nu)^† U_nu(x)^†
    a = _mul(links[mu, idx, 0], links[mu, idx, 1], links[mu, idx, 2], links[mu, idx, 3],
             links[nu, xm, 0], links[nu, xm, 1], links[nu, xm, 2], links[nu, xm, 3])
    b = _mul(a[0], a[1], a[2], a[3],
             links[mu, xn, 0], -links[mu, xn, 1], -links[mu, xn, 2], -links[mu, xn, 3])
    c = _mul(b[0], b[1], b[2], b[3],
             links[nu, idx, 0], -links[nu, idx, 1], -links[nu, idx, 2], -links[nu, idx, 3])
    return 2.0 * c[0]


@nb.njit
def sweep(links, beta, state, d, N, n_sweeps):
    n = N**d
    for _ in range(n_sweeps):
        for mu in range(d):
            for idx in range(n):
                old = (links[mu, idx, 0], links[mu, idx, 1], links[mu, idx, 2], links[mu, idx, 3])
                nq = _rand4(state)
                new = _mul(nq[0], nq[1], nq[2], nq[3], old[0], old[1], old[2], old[3])
                dS = 0.0
                for nu in range(d):
                    if nu == mu:
                        continue
                    for delta in (0, -1):
                        xn = _shift(idx, d, N, nu, delta)
                        links[mu, idx, 0] = old[0]; links[mu, idx, 1] = old[1]
                        links[mu, idx, 2] = old[2]; links[mu, idx, 3] = old[3]
                        s_old = _plaquette(links, d, N, mu, nu, xn)
                        links[mu, idx, 0] = new[0]; links[mu, idx, 1] = new[1]
                        links[mu, idx, 2] = new[2]; links[mu, idx, 3] = new[3]
                        s_new = _plaquette(links, d, N, mu, nu, xn)
                        dS += -0.5 * (s_new - s_old)
                dS *= beta
                r = _next(state)
                if dS > 0.0 and r > math.exp(-dS):
                    # reject: the staple left the link as `new`, restore `old`
                    links[mu, idx, 0] = old[0]; links[mu, idx, 1] = old[1]
                    links[mu, idx, 2] = old[2]; links[mu, idx, 3] = old[3]
    return links


def metropolis_nb(links, beta, n_sweeps, seed=0):
    """Numba Metropolis. links: (d, N^d, 4) float64 → mutated copy."""
    d = links.shape[0]
    N = int(round(links.shape[1] ** (1.0 / d)))
    state = np.array([seed + 1, seed + 123456789], dtype=np.uint64)
    return sweep(links.copy(), beta, state, d, N, n_sweeps)


@nb.njit
def _spatial_plaq_sum(links, d, N, t):
    """Sum of spatial plaquettes at time slice t (the 0++ glueball operator), zero-momentum."""
    total = 0.0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                idx = t*N*N*N + x*N*N + y*N + z
                for mu in range(1, d):
                    for nu in range(mu + 1, d):
                        total += _plaquette(links, d, N, mu, nu, idx)
    return total


@nb.njit
def measure_glueball(beta, d, N, n_sweeps, n_meas, seed, n_between=3):
    """Full Numba glueball measurement: thermalize + measure the connected plaquette correlator.

    Returns (C, m_eff, gbar): C[dt] is the connected <G(t)G(t+dt)> - <G>², m_eff the effective mass."""
    n = N**d
    links = np.empty((d, n, 4), dtype=np.float64)
    state = np.array([seed + 1, seed + 123456789], dtype=np.uint64)
    # initialize + thermalize
    for mu in range(d):
        for idx in range(n):
            q = _rand4(state)
            links[mu, idx, 0] = q[0]; links[mu, idx, 1] = q[1]; links[mu, idx, 2] = q[2]; links[mu, idx, 3] = q[3]
    sweep(links, beta, state, d, N, n_sweeps)
    g_sum = np.zeros(N)
    cross = np.zeros(N)
    for _ in range(n_meas):
        sweep(links, beta, state, d, N, n_between)
        g = np.empty(N)
        for t in range(N):
            g[t] = _spatial_plaq_sum(links, d, N, t)
        g_sum += g
        for dt in range(N):
            s = 0.0
            for t in range(N):
                s += g[t] * g[(t + dt) % N]
            cross[dt] += s
    g_mean = g_sum / n_meas
    gbar = g_mean.mean()
    C = np.empty(N)
    for dt in range(N):
        C[dt] = cross[dt] / (n_meas * N) - gbar * gbar
    m_eff = np.empty(N - 1)
    for dt in range(N - 1):
        m_eff[dt] = -math.log(max(C[dt + 1], 1e-12) / max(C[dt], 1e-12))
    return C, m_eff, gbar
