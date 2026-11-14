"""SU(2) lattice gauge theory Monte-Carlo — Wilson action, Metropolis, Wilson loop / Creutz ratio.

Measures the lattice string tension (Creutz ratio) at strong vs weak coupling. For SU(2) in d=4
the area law (σ > 0, confinement) is expected at BOTH couplings — this is the numerical anchor for
the confinement-frontier hypothesis (candidate 2: area law ⟺ mass gap).
"""
from __future__ import annotations

import numpy as np


def qmul(p, q):
    a0, a1, a2, a3 = p; b0, b1, b2, b3 = q
    return (a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0)


def qconj(p):
    return (p[0], -p[1], -p[2], -p[3])


def random_su2(rng):
    v = rng.normal(size=4)
    v = v / np.linalg.norm(v)
    return (float(v[0]), float(v[1]), float(v[2]), float(v[3]))


def plaquette_trace(links, mu, nu, idx):
    """Re Tr U_p = 2·a0 for the plaquette at (mu,nu,idx). links[mu][site] is a 4-quaternion."""
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


def wilson_loop(links, R, T):
    """Average 0.5·Re Tr of the R×T rectangular Wilson loop over positions and planes."""
    d, N = links.shape[0], links.shape[1]
    vals = []
    for mu in range(d):
        for nu in range(mu + 1, d):
            for flat in range(N**d):
                x = np.unravel_index(flat, (N,) * d)
                u = np.array([1.0, 0.0, 0.0, 0.0])
                xx = list(x)
                for _ in range(R):
                    u = qmul(u, links[mu][tuple(xx)]); xx[mu] = (xx[mu] + 1) % N
                for _ in range(T):
                    u = qmul(u, links[nu][tuple(xx)]); xx[nu] = (xx[nu] + 1) % N
                for _ in range(R):
                    xx[mu] = (xx[mu] - 1) % N; u = qmul(u, qconj(links[mu][tuple(xx)]))
                for _ in range(T):
                    xx[nu] = (xx[nu] - 1) % N; u = qmul(u, qconj(links[nu][tuple(xx)]))
                vals.append(0.5 * u[0])
    return float(np.mean(vals))


def creutz_ratio(links, R, T):
    """The lattice string tension χ(R,T) — positive iff the Wilson loop obeys an area law."""
    def W(r, t):
        return max(wilson_loop(links, r, t), 1e-12)
    return float(-np.log(W(R, T) * W(R - 1, T - 1) / (W(R, T - 1) * W(R - 1, T))))



def ape_smear(links, alpha=0.5, n_iter=3):
    """Spatial APE smearing: U_mu → P_SU(2)[(1-α)U_mu + α/4 Σ_staples], spatial directions only.

    Suppresses UV/vacuum contamination and boosts the 0++ glueball overlap (the fix for the
    connected-correlator signal-to-noise collapse). The time direction (0) is left untouched."""
    d, N = links.shape[0], links.shape[1]
    links = links.copy()
    for _ in range(n_iter):
        new_links = links.copy()
        for mu in range(1, d):
            for flat in range(N**d):
                idx = np.unravel_index(flat, (N,) * d)
                staple = np.zeros(4)
                for nu in range(1, d):
                    if nu == mu:
                        continue
                    xn = list(idx); xn[nu] = (xn[nu] + 1) % N
                    xm = list(idx); xm[mu] = (xm[mu] + 1) % N
                    fwd = qmul(links[nu][tuple(idx)], links[mu][tuple(xn)])
                    fwd = qmul(fwd, qconj(links[nu][tuple(xm)]))
                    staple += np.array(fwd)
                    xnm = list(idx); xnm[nu] = (xnm[nu] - 1) % N
                    xnm2 = list(xnm); xnm2[mu] = (xnm2[mu] + 1) % N
                    bwd = qmul(qconj(links[nu][tuple(xnm)]), links[mu][tuple(xnm)])
                    bwd = qmul(bwd, links[nu][tuple(xnm2)])
                    staple += np.array(bwd)
                smeared = (1.0 - alpha) * links[mu][tuple(idx)] + (alpha / 4.0) * staple
                n = float(np.linalg.norm(smeared))
                new_links[mu][tuple(idx)] = smeared / n if n > 1e-12 else links[mu][tuple(idx)]
        links = new_links
    return links

def measure_string_tension(beta, d=4, N=8, n_sweeps=6, seed=0):
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(d * N**d)])
    links = links.reshape((d,) + (N,) * d + (4,))
    links = metropolis(links, beta, rng, n_sweeps)
    return creutz_ratio(links, 2, 2)


__all__ = ["qmul", "qconj", "random_su2", "plaquette_trace", "metropolis",
           "wilson_loop", "creutz_ratio", "measure_string_tension"]
