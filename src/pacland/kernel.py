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
def _plaquette(links, d, N, mu, nu, idx):
    """Re Tr of the (mu,nu) plaquette at flat site idx."""
    # coords of idx (little-endian base N)
    c0 = idx % N
    c1 = (idx // N) % N
    c2 = (idx // (N*N)) % N
    c3 = idx // (N*N*N)
    coords = (c0, c1, c2, c3)
    # +mu neighbor
    cm = list(coords); cm[mu] = (cm[mu] + 1) % N
    xm = cm[0] + cm[1]*N + cm[2]*N*N + cm[3]*N*N*N
    # +nu neighbor
    cn = list(coords); cn[nu] = (cn[nu] + 1) % N
    xn = cn[0] + cn[1]*N + cn[2]*N*N + cn[3]*N*N*N
    # U_mu(x) U_nu(x+mu) U_mu(x+nu)^† U_nu(x)^†
    a = _mul(links[mu, idx, 0], links[mu, idx, 1], links[mu, idx, 2], links[mu, idx, 3],
             links[nu, xm, 0], links[nu, xm, 1], links[nu, xm, 2], links[nu, xm, 3])
    b = _mul(a[0], a[1], a[2], a[3],
             -links[mu, xn, 0], -links[mu, xn, 1], -links[mu, xn, 2], -links[mu, xn, 3])
    c = _mul(b[0], b[1], b[2], b[3],
             -links[nu, idx, 0], -links[nu, idx, 1], -links[nu, idx, 2], -links[nu, idx, 3])
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
                    for delta in (1, -1):
                        # neighbor in nu by delta (flat index)
                        c0 = idx % N; c1 = (idx // N) % N; c2 = (idx // (N*N)) % N; c3 = idx // (N*N*N)
                        cc = [c0, c1, c2, c3]
                        cc[nu] = (cc[nu] + delta) % N
                        xn = cc[0] + cc[1]*N + cc[2]*N*N + cc[3]*N*N*N
                        links[mu, idx, 0] = old[0]; links[mu, idx, 1] = old[1]
                        links[mu, idx, 2] = old[2]; links[mu, idx, 3] = old[3]
                        s_old = _plaquette(links, d, N, mu, nu, xn)
                        links[mu, idx, 0] = new[0]; links[mu, idx, 1] = new[1]
                        links[mu, idx, 2] = new[2]; links[mu, idx, 3] = new[3]
                        s_new = _plaquette(links, d, N, mu, nu, xn)
                        dS += -0.5 * (s_new - s_old)
                dS *= beta
                r = _next(state)
                if not (dS > 0.0 and r > math.exp(-dS)):
                    links[mu, idx, 0] = new[0]; links[mu, idx, 1] = new[1]
                    links[mu, idx, 2] = new[2]; links[mu, idx, 3] = new[3]
    return links


def metropolis_nb(links, beta, n_sweeps, seed=0):
    """Numba Metropolis. links: (d, N^d, 4) float64 → mutated copy."""
    d = links.shape[0]
    N = int(round(links.shape[1] ** (1.0 / d)))
    state = np.array([seed + 1, seed + 123456789], dtype=np.uint64)
    return sweep(links.copy(), beta, state, d, N, n_sweeps)
