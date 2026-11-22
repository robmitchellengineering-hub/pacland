"""numba-accelerated SU(2) Metropolis — a drop-in faster twin of `lattice_ym_su2.metropolis`.

The pure-Python Metropolis is the bottleneck for every lattice measurement in this thread. This
module JIT-compiles the same Wilson-action Metropolis over a FLAT link array `(d, N^d, 4)` and is
~50-100x faster. `metropolis_fast` converts to/from the `(d,)+(N,)*d+(4,)` shape so it is a drop-in
replacement.

Requires numba (installed on the Mac; `pip install numba` on a node).
"""
from __future__ import annotations

import math

import numpy as np

try:
    from numba import njit
    _HAVE_NUMBA = True
except ImportError:  # pragma: no cover - the fast path is optional
    njit = None
    _HAVE_NUMBA = False


if _HAVE_NUMBA:

    @njit
    def _qmul(p, q):
        return np.array([
            p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3],
            p[0]*q[1] + p[1]*q[0] + p[2]*q[3] - p[3]*q[2],
            p[0]*q[2] - p[1]*q[3] + p[2]*q[0] + p[3]*q[1],
            p[0]*q[3] + p[1]*q[2] - p[2]*q[1] + p[3]*q[0],
        ])

    @njit
    def _qconj(p):
        return np.array([p[0], -p[1], -p[2], -p[3]])

    @njit
    def _random_su2():
        v = np.random.normal(0.0, 1.0, 4)
        n = np.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2] + v[3]*v[3])
        return v / n

    @njit
    def _plaquette(links, mu, nu, flat, strides, N):
        """Re Tr of the plaquette at (mu, nu, flat): 2 * a0 of U_mu U_nu U_mu^dag U_nu^dag."""
        s = strides
        fmu = flat + s[mu]
        if (flat // s[mu]) % N == N - 1:
            fmu -= N * s[mu]
        fnu = flat + s[nu]
        if (flat // s[nu]) % N == N - 1:
            fnu -= N * s[nu]
        u = links[mu, flat]
        u = _qmul(u, links[nu, fmu])
        u = _qmul(u, _qconj(links[mu, fnu]))
        u = _qmul(u, _qconj(links[nu, flat]))
        return 2.0 * u[0]

    @njit
    def _metropolis_flat(links, beta, n_sweeps, seed):
        """The Wilson-action Metropolis over a flat (d, N^d, 4) link array (numba)."""
        d = links.shape[0]
        nsites = links.shape[1]
        N = round(nsites ** (1.0 / d))
        strides = np.empty(d, dtype=np.int64)
        for mu in range(d):
            strides[mu] = N ** (d - 1 - mu)
        np.random.seed(seed)
        for _ in range(n_sweeps):
            for mu in range(d):
                for flat in range(nsites):
                    old = links[mu, flat].copy()
                    new = _qmul(_random_su2(), old)
                    dS = 0.0
                    for nu in range(d):
                        if nu == mu:
                            continue
                        # base = 0 (forward) and base = -1 (backward) plaquettes
                        for base in (0, -1):
                            x = flat
                            if base == -1:
                                x = flat - strides[nu]
                                if (flat // strides[nu]) % N == 0:
                                    x += N * strides[nu]
                            s_old = _plaquette(links, mu, nu, x, strides, N)
                            links[mu, flat] = new
                            s_new = _plaquette(links, mu, nu, x, strides, N)
                            links[mu, flat] = old
                            dS += -0.5 * (s_new - s_old)
                    dS *= beta
                    if not (dS > 0 and np.random.random() > np.exp(-dS)):
                        links[mu, flat] = new
        return links

    @njit
    def _staple_sum_flat(links, mu, flat, strides, N):
        """The sum of the 2(d-1) staples around link (mu, flat) — a 4-vector (numba)."""
        d = links.shape[0]
        Z = np.zeros(4)
        for nu in range(d):
            if nu == mu:
                continue
            s = strides[nu]
            # forward staple: U_nu(x) U_mu(x+nu) U_nu(x+mu)^dag
            xn = flat + s
            if (flat // s) % N == N - 1:
                xn -= N * s
            xm = flat + strides[mu]
            if (flat // strides[mu]) % N == N - 1:
                xm -= N * strides[mu]
            fwd = _qmul(links[nu, flat], links[mu, xn])
            fwd = _qmul(fwd, _qconj(links[nu, xm]))
            Z += fwd
            # backward staple: U_nu(x-nu)^dag U_mu(x-nu) U_nu(x-nu+mu)
            xnm = flat - s
            if (flat // s) % N == 0:
                xnm += N * s
            xnm2 = xnm + strides[mu]
            if (xnm // strides[mu]) % N == N - 1:
                xnm2 -= N * strides[mu]
            bwd = _qmul(_qconj(links[nu, xnm]), links[mu, xnm])
            bwd = _qmul(bwd, links[nu, xnm2])
            Z += bwd
        return Z

    @njit
    def _wilson_flow_step_flat(links, epsilon):
        """One Euler Wilson-flow step over a flat (d, N^d, 4) link array (numba)."""
        d = links.shape[0]
        nsites = links.shape[1]
        N = round(nsites ** (1.0 / d))
        strides = np.empty(d, dtype=np.int64)
        for mu in range(d):
            strides[mu] = N ** (d - 1 - mu)
        out = links.copy()
        for mu in range(d):
            for flat in range(nsites):
                V = links[mu, flat]
                Z = _staple_sum_flat(links, mu, flat, strides, N)
                w = _qmul(Z, _qconj(V))
                f0, f1, f2 = w[1], w[2], w[3]
                norm = math.sqrt(f0 * f0 + f1 * f1 + f2 * f2)
                if norm < 1e-12:
                    continue
                theta = epsilon * norm
                c = math.cos(theta)
                s = math.sin(theta) / norm
                out[mu, flat] = _qmul(np.array([c, s * f0, s * f1, s * f2]), V)
        return out

    @njit
    def _energy_density_flat(links):
        """The Wilson-flow energy density <1 - 1/2 Re Tr U_plaq> over a flat link array (numba)."""
        d = links.shape[0]
        nsites = links.shape[1]
        N = round(nsites ** (1.0 / d))
        strides = np.empty(d, dtype=np.int64)
        for mu in range(d):
            strides[mu] = N ** (d - 1 - mu)
        total = 0.0
        count = 0
        for mu in range(d):
            for nu in range(mu + 1, d):
                for flat in range(nsites):
                    total += 1.0 - 0.5 * _plaquette(links, mu, nu, flat, strides, N)
                    count += 1
        return total / count


def metropolis_fast(links: np.ndarray, beta: float, n_sweeps: int, seed: int = 0) -> np.ndarray:
    """Drop-in numba replacement for `lattice_ym_su2.metropolis` (same shape in/out).

    Falls back to the pure-Python metropolis if numba is missing."""
    if not _HAVE_NUMBA:
        from pacland import lattice_ym_su2 as lm
        import numpy as _np
        rng = _np.random.default_rng(seed)
        return lm.metropolis(links, beta, rng, n_sweeps)

    d = links.shape[0]
    N = links.shape[1]
    nsites = N ** d
    flat = links.reshape(d, nsites, 4)
    flat = _metropolis_flat(flat, float(beta), int(n_sweeps), int(seed))
    return flat.reshape(links.shape)


def wilson_flow_scale_fast(beta: float, N: int = 8, n_flow_steps: int = 200,
                           epsilon: float = 0.05, target: float = 0.08,
                           n_sweeps: int = 10, seed: int = 0):
    """The Wilson-flow t0 scale (t^2 E = target) using the numba flow + metropolis.

    Falls back to the pure-Python `lattice_ym_su2.wilson_flow_scale` if numba is missing."""
    if not _HAVE_NUMBA:
        from pacland import lattice_ym_su2 as lm
        return lm.wilson_flow_scale(beta, N=N, n_flow_steps=n_flow_steps, epsilon=epsilon,
                                    target=target, n_sweeps=n_sweeps, seed=seed)
    from pacland import lattice_ym_su2 as lm

    d = 4
    nsites = N ** d
    rng = np.random.default_rng(seed)
    links = np.array([lm.random_su2(rng) for _ in range(d * nsites)])
    links = links.reshape((d,) + (N,) * d + (4,))
    flat = metropolis_fast(links, beta, n_sweeps, seed).reshape(d, nsites, 4)
    eps_eff = epsilon * (4.0 / float(beta))  # g0^2 = 4/beta: the Wilson-flow rate
    t = 0.0
    t2E_prev = 0.0
    for _ in range(n_flow_steps):
        flat = _wilson_flow_step_flat(flat, eps_eff)
        t += epsilon
        E = _energy_density_flat(flat)
        t2E = t * t * E
        if t2E >= target:
            if t2E > t2E_prev:
                frac = (target - t2E_prev) / (t2E - t2E_prev)
                return t - epsilon + epsilon * frac
            return t
        t2E_prev = t2E
    return None


__all__ = ["metropolis_fast", "wilson_flow_scale_fast", "HAVE_NUMBA"]

HAVE_NUMBA = _HAVE_NUMBA
