"""SU(3) lattice Yang-Mills — a complex 3x3-matrix representation (for the large-N ratio falsifier).

Mirrors ``lattice_ym_su2`` but with SU(3) (Gell-Mann algebra, complex 3x3 matrices) instead of SU(2)
quaternions. The observable is the same Creutz ratio (area-law string tension); the update is the
standard Wilson Metropolis with an exact staple.
"""
from __future__ import annotations

import numpy as np


def random_su3(rng: np.random.Generator) -> np.ndarray:
    """A Haar-random SU(3) matrix: QR of a random complex 3x3, phases fixed so det = +1."""
    z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(z)
    lam = np.diag(r) / np.abs(np.diag(r))
    det = np.linalg.det(q) * np.prod(lam)
    lam = lam * np.exp(-1j * np.angle(det) / 3)  # overall cube-root phase => det = +1
    return q @ np.diag(lam)


def staple(links: np.ndarray, mu: int, idx: tuple) -> np.ndarray:
    """The SU(3) staple sum S(x,mu) = sum of the six 3-link products around the link (x,mu)."""
    d, N = links.shape[0], links.shape[1]
    S = np.zeros((3, 3), dtype=complex)
    for nu in range(d):
        if nu == mu:
            continue
        x = np.array(idx)
        xn = x.copy(); xn[nu] = (xn[nu] + 1) % N
        xm = x.copy(); xm[mu] = (xm[mu] + 1) % N
        # forward: U_nu(x) U_mu(x+nu) U_nu^dag(x+mu)
        S += links[nu][tuple(x)] @ links[mu][tuple(xn)] @ links[nu][tuple(xm)].conj().T
        xnm = x.copy(); xnm[nu] = (xnm[nu] - 1) % N
        xnm2 = xnm.copy(); xnm2[mu] = (xnm2[mu] + 1) % N
        # backward: U_nu^dag(x-nu) U_mu(x-nu) U_nu(x-nu+mu)
        S += links[nu][tuple(xnm)].conj().T @ links[mu][tuple(xnm)] @ links[nu][tuple(xnm2)]
    return S


def _proj_su3(m: np.ndarray) -> np.ndarray:
    """Project a 3x3 complex matrix back onto SU(3) (QR with unit determinant)."""
    q, r = np.linalg.qr(m)
    lam = np.diag(r) / np.abs(np.diag(r))
    det = np.linalg.det(q) * np.prod(lam)
    lam = lam * np.exp(-1j * np.angle(det) / 3)
    return q @ np.diag(lam)


def ape_smear(links: np.ndarray, alpha: float = 0.5, n_iter: int = 3) -> np.ndarray:
    """Spatial APE smearing: U_mu → P_SU(3)[(1-α)U_mu + α/4 Σ_staples], spatial directions only.

    Suppresses UV/vacuum contamination and boosts the 0++ glueball overlap (the standard fix for the
    connected-correlator signal-to-noise collapse). The time direction (0) is left untouched."""
    d, N = links.shape[0], links.shape[1]
    links = links.copy()
    for _ in range(n_iter):
        new_links = links.copy()
        for mu in range(1, d):
            for flat in range(N ** d):
                idx = np.unravel_index(flat, (N,) * d)
                staple = np.zeros((3, 3), dtype=complex)
                for nu in range(1, d):
                    if nu == mu:
                        continue
                    xn = list(idx); xn[nu] = (xn[nu] + 1) % N
                    xm = list(idx); xm[mu] = (xm[mu] + 1) % N
                    fwd = links[nu][tuple(idx)] @ links[mu][tuple(xn)] @ links[nu][tuple(xm)].conj().T
                    staple += fwd
                    xnm = list(idx); xnm[nu] = (xnm[nu] - 1) % N
                    xnm2 = list(xnm); xnm2[mu] = (xnm2[mu] + 1) % N
                    bwd = links[nu][tuple(xnm)].conj().T @ links[mu][tuple(xnm)] @ links[nu][tuple(xnm2)]
                    staple += bwd
                smeared = (1.0 - alpha) * links[mu][tuple(idx)] + (alpha / 4.0) * staple
                new_links[mu][tuple(idx)] = _proj_su3(smeared)
        links = new_links
    return links


def metropolis(links: np.ndarray, beta: float, rng: np.random.Generator, n_sweeps: int,
               eps: float = 0.25) -> np.ndarray:
    """Wilson Metropolis: propose U' = exp(i eps H) U (H traceless Hermitian), accept by exp(-beta dS)."""
    d, N = links.shape[0], links.shape[1]
    for _ in range(n_sweeps):
        for mu in range(d):
            for flat in range(N ** d):
                idx = tuple(np.unravel_index(flat, (N,) * d))
                old = links[mu][idx]
                S = staple(links, mu, idx)
                # a random traceless Hermitian generator
                z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
                H = z - z.conj().T  # anti-Hermitian; i*H is Hermitian
                U_new = _proj_su3((np.eye(3) + 1j * eps * H) @ old)
                # dS = Re Tr[(U_new - U_old) @ staple] > 0 means U_new INCREASES Re Tr[U @ staple],
                # i.e. lowers the Wilson action — accept it; otherwise accept with exp(beta * dS).
                dS = np.real(np.trace((U_new - old) @ S))
                if dS >= 0 or rng.random() < np.exp(beta * dS):
                    links[mu][idx] = U_new
    return links


def plaquette_trace(links: np.ndarray, mu: int, nu: int, idx: tuple) -> float:
    """Real trace of the plaquette in the (mu,nu) plane at site idx."""
    d, N = links.shape[0], links.shape[1]
    x = np.array(idx)
    xn = x.copy(); xn[nu] = (xn[nu] + 1) % N
    xm = x.copy(); xm[mu] = (xm[mu] + 1) % N
    p = links[mu][tuple(x)] @ links[nu][tuple(xn)] @ links[mu][tuple(xm)].conj().T @ links[nu][tuple(x)].conj().T
    return float(np.real(np.trace(p)))


def wilson_loop(links: np.ndarray, R: int, T: int) -> float:
    """Average real trace of an R x T rectangular Wilson loop (the area-law observable)."""
    d, N = links.shape[0], links.shape[1]
    tot = 0.0
    n = 0
    for flat in range(N ** d):
        x = np.array(np.unravel_index(flat, (N,) * d))
        # R x T loop in the (0,1) plane, product of links around the rectangle
        p = np.eye(3, dtype=complex)
        for i in range(R):
            p = p @ links[0][tuple(x)]
            x[0] = (x[0] + 1) % N
        for j in range(T):
            p = p @ links[1][tuple(x)]
            x[1] = (x[1] + 1) % N
        for i in range(R):
            x[0] = (x[0] - 1) % N
            p = p @ links[0][tuple(x)].conj().T
        for j in range(T):
            x[1] = (x[1] - 1) % N
            p = p @ links[1][tuple(x)].conj().T
        tot += float(np.real(np.trace(p)))
        n += 1
    return tot / n if n else 0.0


def creutz_ratio(links: np.ndarray, R: int, T: int) -> float:
    """Creutz ratio sigma a^2 ≈ -log[W(R,T) W(R-1,T-1) / (W(R,T-1) W(R-1,T))]."""
    w_rt = wilson_loop(links, R, T)
    w_r1t1 = wilson_loop(links, R - 1, T - 1)
    w_rt1 = wilson_loop(links, R, T - 1)
    w_r1t = wilson_loop(links, R - 1, T)
    num = w_rt * w_r1t1
    den = w_rt1 * w_r1t
    return float(-np.log(num / den)) if num > 0 and den > 0 else 0.0


def measure_string_tension(beta: float, d: int = 4, N: int = 6, n_sweeps: int = 10,
                           n_meas: int = 10, seed: int = 0) -> float:
    """The SU(3) string tension (mean Creutz ratio 2x2) — thermalized, then averaged over n_meas
    separated measurements so the area-law signal is not drowned by single-trace noise."""
    rng = np.random.default_rng(seed)
    links = np.array([random_su3(rng) for _ in range(d * N ** d)])
    links = links.reshape((d,) + (N,) * d + (3, 3))
    links = metropolis(links, beta, rng, n_sweeps)  # thermalize
    vals = []
    for _ in range(n_meas):
        links = metropolis(links, beta, rng, 2)
        vals.append(creutz_ratio(links, 2, 2))
    return float(np.mean(vals))


__all__ = ["random_su3", "staple", "metropolis", "plaquette_trace", "wilson_loop",
           "creutz_ratio", "measure_string_tension", "ape_smear"]
