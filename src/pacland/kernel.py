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


@nb.njit(inline="always")
def _rect(links, d, N, mu, nu, idx):
    """Re Tr of the 1x2 rectangle (two mu links, one nu link) at flat site idx."""
    x1 = _shift(idx, d, N, mu, 1)
    x2 = _shift(x1, d, N, mu, 1)
    xn = _shift(idx, d, N, nu, 1)
    xn2 = _shift(x1, d, N, nu, 1)
    a = _mul(links[mu, idx, 0], links[mu, idx, 1], links[mu, idx, 2], links[mu, idx, 3],
             links[mu, x1, 0], links[mu, x1, 1], links[mu, x1, 2], links[mu, x1, 3])
    b = _mul(a[0], a[1], a[2], a[3],
             links[nu, x2, 0], links[nu, x2, 1], links[nu, x2, 2], links[nu, x2, 3])
    c = _mul(b[0], b[1], b[2], b[3],
             links[mu, xn2, 0], -links[mu, xn2, 1], -links[mu, xn2, 2], -links[mu, xn2, 3])
    e = _mul(c[0], c[1], c[2], c[3],
             links[mu, xn, 0], -links[mu, xn, 1], -links[mu, xn, 2], -links[mu, xn, 3])
    f = _mul(e[0], e[1], e[2], e[3],
             links[nu, idx, 0], -links[nu, idx, 1], -links[nu, idx, 2], -links[nu, idx, 3])
    return 2.0 * f[0]


@nb.njit
def _spatial_rect_sum(links, d, N, t):
    """Sum of spatial 1x2 rectangles at time slice t (a second 0++ interpolator)."""
    total = 0.0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                idx = t*N*N*N + x*N*N + y*N + z
                for mu in range(1, d):
                    for nu in range(mu + 1, d):
                        total += _rect(links, d, N, mu, nu, idx)
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


@nb.njit
def ape_smear_nb(links, d, N, alpha, n_iter):
    """Spatial APE smearing (Numba): U_mu → P_SU(2)[(1-α)U_mu + α/4 Σ staples], mu in 1..d-1."""
    links = links.copy()
    n = N**d
    for _ in range(n_iter):
        new = links.copy()
        for mu in range(1, d):
            for idx in range(n):
                st = np.zeros(4)
                for nu in range(1, d):
                    if nu == mu:
                        continue
                    xn = _shift(idx, d, N, nu, 1)
                    xm = _shift(idx, d, N, mu, 1)
                    fwd = _mul(links[nu, idx, 0], links[nu, idx, 1], links[nu, idx, 2], links[nu, idx, 3],
                               links[mu, xn, 0], links[mu, xn, 1], links[mu, xn, 2], links[mu, xn, 3])
                    fwd = _mul(fwd[0], fwd[1], fwd[2], fwd[3],
                               links[nu, xm, 0], -links[nu, xm, 1], -links[nu, xm, 2], -links[nu, xm, 3])
                    st[0] += fwd[0]; st[1] += fwd[1]; st[2] += fwd[2]; st[3] += fwd[3]
                    xnm = _shift(idx, d, N, nu, -1)
                    xnm2 = _shift(xnm, d, N, mu, 1)
                    bwd = _mul(links[nu, xnm, 0], -links[nu, xnm, 1], -links[nu, xnm, 2], -links[nu, xnm, 3],
                               links[mu, xnm, 0], links[mu, xnm, 1], links[mu, xnm, 2], links[mu, xnm, 3])
                    bwd = _mul(bwd[0], bwd[1], bwd[2], bwd[3],
                               links[nu, xnm2, 0], links[nu, xnm2, 1], links[nu, xnm2, 2], links[nu, xnm2, 3])
                    st[0] += bwd[0]; st[1] += bwd[1]; st[2] += bwd[2]; st[3] += bwd[3]
                s0 = (1.0 - alpha) * links[mu, idx, 0] + (alpha / 4.0) * st[0]
                s1 = (1.0 - alpha) * links[mu, idx, 1] + (alpha / 4.0) * st[1]
                s2 = (1.0 - alpha) * links[mu, idx, 2] + (alpha / 4.0) * st[2]
                s3 = (1.0 - alpha) * links[mu, idx, 3] + (alpha / 4.0) * st[3]
                norm = math.sqrt(s0*s0 + s1*s1 + s2*s2 + s3*s3)
                if norm > 1e-12:
                    new[mu, idx, 0] = s0 / norm; new[mu, idx, 1] = s1 / norm
                    new[mu, idx, 2] = s2 / norm; new[mu, idx, 3] = s3 / norm
        links = new
    return links


@nb.njit
def measure_variational(beta, d, N, n_sweeps, n_meas, seed, smears):
    """Numba variational: smeared-operator cross-correlator matrix + GEVP ground-state masses.

    smears: array of smear iterations (e.g. [0, 3, 6]). Returns (masses, gbar)."""
    n = N**d
    links = np.empty((d, n, 4), dtype=np.float64)
    state = np.array([seed + 1, seed + 123456789], dtype=np.uint64)
    for mu in range(d):
        for idx in range(n):
            q = _rand4(state)
            links[mu, idx, 0] = q[0]; links[mu, idx, 1] = q[1]; links[mu, idx, 2] = q[2]; links[mu, idx, 3] = q[3]
    sweep(links, beta, state, d, N, n_sweeps)
    n_op = smears.shape[0]
    C = np.zeros((n_op, n_op, N))
    g_mean = np.zeros((n_op, N))
    for _ in range(n_meas):
        sweep(links, beta, state, d, N, 3)
        gs = np.empty((n_op, N))
        for i in range(n_op):
            sm = ape_smear_nb(links, d, N, 0.5, smears[i])
            for t in range(N):
                gs[i, t] = _spatial_plaq_sum(sm, d, N, t)
        for i in range(n_op):
            g_mean[i] += gs[i]
            for j in range(n_op):
                for dt in range(N):
                    s = 0.0
                    for t in range(N):
                        s += gs[i, t] * gs[j, (t + dt) % N]
                    C[i, j, dt] += s
    g_mean /= n_meas
    gbar = np.empty(n_op)
    for i in range(n_op):
        gbar[i] = g_mean[i].mean()
    for i in range(n_op):
        for j in range(n_op):
            for dt in range(N):
                C[i, j, dt] = C[i, j, dt] / (n_meas * N) - gbar[i] * gbar[j]
    return C, gbar


def gevp_masses(C, N, t0=1):
    """Python GEVP: solve C(t) v = λ C(t0) v, ground state = largest |λ|. Returns the masses."""
    masses = []
    for t in range(t0 + 1, N // 2):
        Ct = C[:, :, t]
        Ct0 = C[:, :, t0]
        try:
            lam = np.linalg.eigvals(np.linalg.solve(Ct0, Ct))
            lam_max = float(np.abs(lam).max())
            if lam_max > 1e-9:
                masses.append(-math.log(lam_max) / (t - t0))
        except np.linalg.LinAlgError:
            pass
    return np.array(masses)


@nb.njit
def measure_variational_2(beta, d, N, n_sweeps, n_meas, seed, smears):
    """Two-shape variational: basis = {plaquette, rectangle} × smears; returns C (cross-correlator)."""
    n = N**d
    links = np.empty((d, n, 4), dtype=np.float64)
    state = np.array([seed + 1, seed + 123456789], dtype=np.uint64)
    for mu in range(d):
        for idx in range(n):
            q = _rand4(state)
            links[mu, idx, 0] = q[0]; links[mu, idx, 1] = q[1]; links[mu, idx, 2] = q[2]; links[mu, idx, 3] = q[3]
    sweep(links, beta, state, d, N, n_sweeps)
    n_sm = smears.shape[0]
    n_op = 2 * n_sm
    C = np.zeros((n_op, n_op, N))
    g_mean = np.zeros((n_op, N))
    for _ in range(n_meas):
        sweep(links, beta, state, d, N, 3)
        gs = np.empty((n_op, N))
        for i in range(n_sm):
            sm = ape_smear_nb(links, d, N, 0.5, smears[i])
            for t in range(N):
                gs[i, t] = _spatial_plaq_sum(sm, d, N, t)
                gs[n_sm + i, t] = _spatial_rect_sum(sm, d, N, t)
        for i in range(n_op):
            g_mean[i] += gs[i]
            for j in range(n_op):
                for dt in range(N):
                    s = 0.0
                    for t in range(N):
                        s += gs[i, t] * gs[j, (t + dt) % N]
                    C[i, j, dt] += s
    g_mean /= n_meas
    gbar = np.empty(n_op)
    for i in range(n_op):
        gbar[i] = g_mean[i].mean()
    for i in range(n_op):
        for j in range(n_op):
            for dt in range(N):
                C[i, j, dt] = C[i, j, dt] / (n_meas * N) - gbar[i] * gbar[j]
    return C, gbar
