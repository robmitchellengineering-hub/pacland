"""Minimal lattice Yang-Mills Monte-Carlo (U(1), Wilson action, Metropolis) — the falsifier for
the ym-mass-gap hypothesis candidates 2/3.

Measures the plaquette-plaquette connected correlation vs the inverse coupling β. Strong coupling
(small β) is the regime `lgt` proves has a mass gap; past the Dobrushin ceiling (larger β) the
correlation's decay class is the open question.

This is a *starting point*, not a result: at the current statistics it resolves the plaquette
variance C(0) (which correctly decreases with β — strong coupling is disordered, weak coupling is
ordered) but the r>0 correlation signal is below the Monte-Carlo noise. The clean physics it is
meant to reach is the known U(1) Coulomb phase: in d=4, weak coupling is deconfined (massless
photon, Wilson perimeter law), so the mass gap does NOT persist to all β for the Abelian group.
That single fact refines hypothesis candidate 2 ("mass gap for all β, all gauge groups") to
"non-Abelian only" — the confinement conjecture.
"""
from __future__ import annotations

import numpy as np


def plaquette_cos(links: np.ndarray) -> np.ndarray:
    """cos(theta_p) for every plaquette; returns (n_planes, *lattice)."""
    d, N = links.shape[0], links.shape[1]
    out = []
    for mu in range(d):
        for nu in range(mu + 1, d):
            u_mu = links[mu]
            u_nu = links[nu]
            u_mu_shift_nu = np.roll(u_mu, -1, axis=nu)
            u_nu_shift_mu = np.roll(u_nu, -1, axis=mu)
            theta = u_mu + u_nu_shift_mu - u_mu_shift_nu - u_nu
            out.append(np.cos(theta))
    return np.array(out)


def link_plaquette_angles(links, mu, idx):
    """The 2(d-1) plaquette angles containing link (mu, idx)."""
    d, N = links.shape[0], links.shape[1]
    affected = []
    for nu in range(d):
        if nu == mu:
            continue
        for base in (0, -1):
            x = list(idx)
            x[nu] = (x[nu] + base) % N
            x = tuple(x)
            xn = list(x); xn[nu] = (xn[nu] + 1) % N; xn = tuple(xn)
            xm = list(x); xm[mu] = (xm[mu] + 1) % N; xm = tuple(xm)
            theta = links[mu][x] + links[nu][xm] - links[mu][xn] - links[nu][x]
            affected.append(theta)
    return affected


def action(links: np.ndarray, beta: float) -> float:
    return float(beta * np.sum(1.0 - plaquette_cos(links)))


def metropolis(links, beta, rng, n_sweeps):
    d, N = links.shape[0], links.shape[1]
    for _ in range(n_sweeps):
        for mu in range(d):
            for flat in range(N**d):
                idx = np.unravel_index(flat, (N,) * d)
                old = links[mu][idx]
                new = old + rng.uniform(-1.0, 1.0)
                th_old = link_plaquette_angles(links, mu, idx)
                links[mu][idx] = new
                th_new = link_plaquette_angles(links, mu, idx)
                dS = beta * np.sum(np.cos(th_old) - np.cos(th_new))
                if dS > 0 and rng.random() > np.exp(-dS):
                    links[mu][idx] = old
    return links


def plaquette_corr(links, max_r):
    """Connected plaquette-plaquette correlation C(r) along the first axis."""
    pc = plaquette_cos(links)[0]
    mean = pc.mean()
    return np.array([np.mean(pc * np.roll(pc, -r, axis=0)) - mean**2 for r in range(max_r)])


def measure(beta, d=4, N=8, n_sweeps=40, n_seeds=4):
    """Averaged plaquette correlation C(r) at coupling beta."""
    Cs = []
    for seed in range(n_seeds):
        rng = np.random.default_rng(seed)
        links = rng.uniform(0, 2 * np.pi, size=(d,) + (N,) * d)
        links = metropolis(links, beta, rng, n_sweeps)
        Cs.append(plaquette_corr(links, max_r=4))
    return np.mean(Cs, axis=0)


__all__ = ["plaquette_cos", "action", "metropolis", "plaquette_corr", "measure"]
