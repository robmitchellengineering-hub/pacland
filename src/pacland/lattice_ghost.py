"""The lattice Faddeev–Popov operator + the horizon-concentration measurement.

The open Clay rung (`docs/MASS-GAP-METHODS.md`) is the infinite-dimensional Gribov–Zwanziger horizon
condition: the measure restricted to the Gribov region concentrates at the horizon where the lowest
eigenvalue of the Faddeev–Popov operator `M = −∇·D` tends to zero. This is its lattice form: `M` is
the covariant Laplacian in the adjoint representation, and the horizon is `λ_min(M) → 0`.

`horizon_concentration` measures `P(λ_min < ε)` over thermalized configurations as a function of `N`
— if it stays away from zero as `N` grows, the horizon concentrates (the open rung, computationally).
"""
from __future__ import annotations

import numpy as np

from pacland import lattice_ym_su2 as su2


def adjoint_matrix(q: tuple) -> np.ndarray:
    """The SO(3) rotation matrix of an SU(2) quaternion (its adjoint representation)."""
    a0, a1, a2, a3 = q
    return np.array([
        [a0*a0 + a1*a1 - a2*a2 - a3*a3, 2*(a1*a2 - a0*a3), 2*(a1*a3 + a0*a2)],
        [2*(a1*a2 + a0*a3), a0*a0 - a1*a1 + a2*a2 - a3*a3, 2*(a2*a3 - a0*a1)],
        [2*(a1*a3 - a0*a2), 2*(a2*a3 + a0*a1), a0*a0 - a1*a1 - a2*a2 + a3*a3],
    ])


def fp_operator(links: np.ndarray) -> np.ndarray:
    """The lattice Faddeev–Popov operator (covariant Laplacian, adjoint rep), a (3·N^d)² matrix.

    `(M φ)(x) = Σ_μ [ 2 φ(x) − R(U_μ(x)) φ(x+μ) − R(U_μ(x−μ))ᵀ φ(x−μ) ]` with `R` the adjoint matrix.
    """
    d, N = links.shape[0], links.shape[1]
    nsites = N ** d
    dim = 3 * nsites
    M = np.zeros((dim, dim))
    for flat in range(nsites):
        idx = np.unravel_index(flat, (N,) * d)
        row = 3 * flat
        M[row:row + 3, row:row + 3] += 2 * d * np.eye(3)
        for mu in range(d):
            # forward neighbour
            u = links[mu][tuple(idx)]
            R = adjoint_matrix(u)
            fwd = list(idx); fwd[mu] = (fwd[mu] + 1) % N
            col = 3 * int(np.ravel_multi_index(fwd, (N,) * d))
            M[row:row + 3, col:col + 3] -= R
            # backward neighbour
            bwd = list(idx); bwd[mu] = (bwd[mu] - 1) % N
            ub = links[mu][tuple(bwd)]
            Rb = adjoint_matrix(ub)
            colb = 3 * int(np.ravel_multi_index(bwd, (N,) * d))
            M[row:row + 3, colb:colb + 3] -= Rb.T
    return (M + M.T) / 2  # symmetrise


def lowest_fp_eigenvalue(links: np.ndarray) -> float:
    """The lowest eigenvalue of the FP operator (the Gribov-horizon observable)."""
    w = np.linalg.eigvalsh(fp_operator(links))
    return float(w[0])


def landau_gauge_fix(links: np.ndarray, n_iter: int = 20) -> np.ndarray:
    """Iterative Landau gauge fixing: at each site choose `g(x)` to maximise the local trace.

    The local maximum is `g(x) = S†/|S|` with `S = Σ_μ [U_μ(x) + U_μ(x−μ)†]` (the staple sum). The
    Gribov horizon is the boundary of the gauge orbit where the FP operator's lowest eigenvalue → 0.
    """
    d, N = links.shape[0], links.shape[1]
    links = links.copy()
    for _ in range(n_iter):
        for flat in range(N ** d):
            x = tuple(np.unravel_index(flat, (N,) * d))
            S = np.zeros(4)
            for mu in range(d):
                S += np.array(links[mu][x])
                xm = list(x); xm[mu] = (xm[mu] - 1) % N
                S += np.array(su2.qconj(links[mu][tuple(xm)]))
            norm = float(np.linalg.norm(S))
            if norm < 1e-12:
                continue
            g = np.array([S[0], -S[1], -S[2], -S[3]]) / norm  # S†/|S|
            for mu in range(d):
                links[mu][x] = su2.qmul(tuple(g), links[mu][x])
                xm = list(x); xm[mu] = (xm[mu] - 1) % N
                xm = tuple(xm)
                links[mu][xm] = su2.qmul(links[mu][xm], su2.qconj(tuple(g)))
    return links


def horizon_concentration(beta: float, N: int, n_configs: int = 40, eps: float = 0.1,
                          n_sweeps: int = 10, seed: int = 0) -> dict:
    """`P(λ_min(M) < ε)` over thermalized configurations — the horizon-concentration probe."""
    rng = np.random.default_rng(seed)
    lams = []
    for _ in range(n_configs):
        links = np.array([su2.random_su2(rng) for _ in range(4 * N ** 4)])
        links = links.reshape((4,) + (N,) * 4 + (4,))
        links = su2.metropolis(links, beta, rng, n_sweeps)
        lams.append(lowest_fp_eigenvalue(links))
    lams = np.array(lams)
    return {"P_lambda_min_lt_eps": float(np.mean(lams < eps)),
            "mean_lambda_min": float(np.mean(lams)),
            "min_lambda_min": float(np.min(lams)),
            "N": N, "n_configs": n_configs, "eps": eps}


def horizon_concentration_landau(beta: float, N: int, n_configs: int = 20, eps: float = 0.1,
                                 n_sweeps: int = 10, n_gf: int = 20, seed: int = 0) -> dict:
    """The horizon probe IN LANDAU GAUGE: fix the gauge, then measure `λ_min` of the FP operator.

    This is the true open rung — on the unfixed field `λ_min` is just the covariant Laplacian's gap;
    after Landau fixing, a concentration of `λ_min → 0` is the Gribov horizon.
    """
    rng = np.random.default_rng(seed)
    lams = []
    for _ in range(n_configs):
        links = np.array([su2.random_su2(rng) for _ in range(4 * N ** 4)])
        links = links.reshape((4,) + (N,) * 4 + (4,))
        links = su2.metropolis(links, beta, rng, n_sweeps)
        links = landau_gauge_fix(links, n_gf)
        lams.append(lowest_fp_eigenvalue(links))
    lams = np.array(lams)
    return {"P_lambda_min_lt_eps": float(np.mean(lams < eps)),
            "mean_lambda_min": float(np.mean(lams)),
            "min_lambda_min": float(np.min(lams)),
            "N": N, "n_configs": n_configs, "eps": eps, "landau": True}


__all__ = ["adjoint_matrix", "fp_operator", "lowest_fp_eigenvalue", "horizon_concentration"]
