"""Finite-temperature SU(3): the Polyakov loop and its correlator (for the clustering falsifier).

A finite-T lattice is N_t x N_s^3 with N_t small (T = 1/(N_t a)). The Polyakov loop is the product of
timelike links around the compact time direction; its connected correlator decays as exp(-m |x|) when
there is exponential clustering. The falsifier extracts m and checks it is nonzero (clustering) versus
vanishing (the clustering claim fails).
"""
from __future__ import annotations

import numpy as np

from pacland import lattice_ym_su3 as su3


def init_links(Nt: int, Ns: int, rng: np.random.Generator) -> np.ndarray:
    """A random finite-T SU(3) gauge field, shape (4, Nt, Ns, Ns, Ns, 3, 3)."""
    n = 4 * Nt * Ns ** 3
    links = np.array([su3.random_su3(rng) for _ in range(n)])
    return links.reshape((4, Nt, Ns, Ns, Ns, 3, 3))


def _staple_ft(links: np.ndarray, mu: int, idx: tuple) -> np.ndarray:
    """The SU(3) staple for link (mu, idx) on the anisotropic N_t x N_s^3 lattice."""
    shape = links.shape[1:5]  # (Nt, Ns, Ns, Ns)
    S = np.zeros((3, 3), dtype=complex)
    for nu in range(4):
        if nu == mu:
            continue
        x = list(idx)
        xn = x.copy(); xn[nu] = (xn[nu] + 1) % shape[nu]
        xm = x.copy(); xm[mu] = (xm[mu] + 1) % shape[mu]
        S += links[nu][tuple(x)] @ links[mu][tuple(xn)] @ links[nu][tuple(xm)].conj().T
        xnm = x.copy(); xnm[nu] = (xnm[nu] - 1) % shape[nu]
        xnm2 = xnm.copy(); xnm2[mu] = (xnm2[mu] + 1) % shape[mu]
        S += links[nu][tuple(xnm)].conj().T @ links[mu][tuple(xnm)] @ links[nu][tuple(xnm2)]
    return S


def metropolis_ft(links: np.ndarray, beta: float, rng: np.random.Generator, n_sweeps: int,
                  eps: float = 0.25) -> np.ndarray:
    """Wilson Metropolis on the finite-T lattice (same acceptance as the bulk SU(3) code)."""
    shape = links.shape[1:5]
    for _ in range(n_sweeps):
        for mu in range(4):
            for flat in range(int(np.prod(shape))):
                idx = tuple(np.unravel_index(flat, shape))
                old = links[mu][idx]
                S = _staple_ft(links, mu, idx)
                z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
                H = z - z.conj().T
                U_new = su3._proj_su3((np.eye(3) + 1j * eps * H) @ old)
                dS = np.real(np.trace((U_new - old) @ S))
                if dS >= 0 or rng.random() < np.exp(beta * dS):
                    links[mu][idx] = U_new
    return links


def polyakov_loop(links: np.ndarray, x: tuple) -> float:
    """Re Tr of the Polyakov loop P(x) = Tr[prod_{t=0}^{N_t-1} U_0(t, x)]. x is (x1,x2,x3)."""
    Nt = links.shape[1]
    p = np.eye(3, dtype=complex)
    for t in range(Nt):
        p = p @ links[0][(t,) + x]
    return float(np.real(np.trace(p)))


def polyakov_correlator(links: np.ndarray, sep: int) -> float:
    """Connected Polyakov correlator C(sep) = <P(x) P(x+sep e1)>_c, averaged over the spatial slice."""
    Ns = links.shape[2]
    vals = []
    for x1 in range(Ns):
        for x2 in range(Ns):
            for x3 in range(Ns):
                P1 = polyakov_loop(links, (x1, x2, x3))
                P2 = polyakov_loop(links, ((x1 + sep) % Ns, x2, x3))
                vals.append(P1 * P2)
    mean = np.mean(vals)
    p1 = np.mean([polyakov_loop(links, (x1, x2, x3)) for x1 in range(Ns)
                  for x2 in range(Ns) for x3 in range(Ns)])
    return float(mean - p1 ** 2)


def correlation_mass(links: np.ndarray, sep: int = 1) -> float:
    """The screening mass m = -log[C(sep+1)/C(sep)] from the connected correlator."""
    c0 = polyakov_correlator(links, sep)
    c1 = polyakov_correlator(links, sep + 1)
    if c0 <= 0 or c1 <= 0:
        return 0.0
    ratio = c1 / c0
    if ratio <= 0:
        return 0.0
    return float(-np.log(ratio))


def measure_correlation_mass(beta: float, Nt: int = 2, Ns: int = 6, n_sweeps: int = 10,
                             n_meas: int = 6, seed: int = 0) -> float:
    """The Polyakov screening mass at coupling beta on an N_t x N_s^3 lattice, averaged over n_meas."""
    rng = np.random.default_rng(seed)
    links = init_links(Nt, Ns, rng)
    links = metropolis_ft(links, beta, rng, n_sweeps)
    masses = []
    for _ in range(n_meas):
        links = metropolis_ft(links, beta, rng, 2)
        masses.append(correlation_mass(links))
    return float(np.mean(masses))


__all__ = ["init_links", "metropolis_ft", "polyakov_loop", "polyakov_correlator",
           "correlation_mass", "measure_correlation_mass"]
