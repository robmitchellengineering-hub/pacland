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

try:
    from pacland import lattice_ym_su2 as su2
except ImportError:  # standalone (flat) import when run outside the package, e.g. on a mesh node
    import lattice_ym_su2 as su2


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


def fp_operator_sparse(links: np.ndarray):
    """The FP operator as a `scipy.sparse` matrix, built VECTORIZED (no per-site Python loop)."""
    import scipy.sparse as sp

    d, N = links.shape[0], links.shape[1]
    nsites = N ** d
    dim = 3 * nsites
    strides = [N ** (d - 1 - mu) for mu in range(d)]

    # adjoint (SO(3)) matrices for every link, vectorized: R[mu, site, a, b]
    R = np.zeros((d, nsites, 3, 3))
    for mu in range(d):
        U = links[mu].reshape(nsites, 4)
        a0, a1, a2, a3 = U[:, 0], U[:, 1], U[:, 2], U[:, 3]
        R[mu, :, 0, 0] = a0*a0 + a1*a1 - a2*a2 - a3*a3
        R[mu, :, 0, 1] = 2*(a1*a2 - a0*a3); R[mu, :, 0, 2] = 2*(a1*a3 + a0*a2)
        R[mu, :, 1, 0] = 2*(a1*a2 + a0*a3); R[mu, :, 1, 1] = a0*a0 - a1*a1 + a2*a2 - a3*a3
        R[mu, :, 1, 2] = 2*(a2*a3 - a0*a1)
        R[mu, :, 2, 0] = 2*(a1*a3 - a0*a2); R[mu, :, 2, 1] = 2*(a2*a3 + a0*a1)
        R[mu, :, 2, 2] = a0*a0 - a1*a1 - a2*a2 + a3*a3

    site = np.arange(nsites)
    rows, cols, vals = [], [], []
    # diagonal: +2d on every component
    for a in range(3):
        rows.append(3 * site + a); cols.append(3 * site + a); vals.append(np.full(nsites, 2.0 * d))
    # off-diagonal: forward (+mu) and backward (-mu) couplings
    for mu in range(d):
        st = strides[mu]
        x_mu = (site // st) % N
        fwd = site + st - (N * st) * (x_mu == N - 1)
        bwd = site - st + (N * st) * (x_mu == 0)
        for a in range(3):
            for b in range(3):
                rows.append(3 * site + a); cols.append(3 * fwd + b)
                vals.append(-R[mu, :, a, b])
                rows.append(3 * site + a); cols.append(3 * bwd + b)
                vals.append(-R[mu, bwd, b, a])  # R(U_mu(x-mu))^T
    rows = np.concatenate(rows); cols = np.concatenate(cols); vals = np.concatenate(vals)
    return sp.coo_matrix((vals, (rows, cols)), shape=(dim, dim)).tocsr()


def lowest_fp_eigenvalue(links: np.ndarray) -> float:
    """The lowest eigenvalue of the FP operator via LOBPCG (matvec-only, no factorization).

    Uses the constant mode as the initial guess (it is the near-zero mode for a near-flat gauge field)
    and a Jacobi preconditioner — converges in a few iterations instead of the shift-invert `eigsh`
    whose LU factorization fills in for a 4d Laplacian.
    """
    from scipy.sparse.linalg import lobpcg

    M = fp_operator_sparse(links)
    n = M.shape[0]
    X = np.ones((n, 1)) / np.sqrt(n)  # constant-mode guess
    # Jacobi preconditioner: inverse diagonal (the diagonal is 2d = 8, constant)
    diag = M.diagonal()
    P = (1.0 / np.where(diag > 0, diag, 1.0))
    from scipy.sparse import diags as sp_diags
    Pre = sp_diags(P)
    w, _ = lobpcg(M, X, largest=False, M=Pre, maxiter=60, tol=1e-3)
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


def fp_spectrum(links: np.ndarray, k: int = 40) -> np.ndarray:
    """The lowest `k` eigenvalues of the FP operator via sparse Lanczos — the near-zero spectral
    density is the Gribov-horizon observable (`ρ(λ) ~ λ^{-1/2}` is the open rung)."""
    from scipy.sparse.linalg import eigsh

    M = fp_operator_sparse(links)
    w = eigsh(M, k=min(k, M.shape[0] - 1), which="SA", return_eigenvectors=False)
    return np.sort(w)


def horizon_density(beta: float, N: int, n_configs: int = 10, k: int = 40,
                    n_sweeps: int = 10, seed: int = 0) -> dict:
    """Gather the lowest `k` FP eigenvalues over configurations — the empirical near-zero density."""
    rng = np.random.default_rng(seed)
    all_w = []
    for _ in range(n_configs):
        links = np.array([su2.random_su2(rng) for _ in range(4 * N ** 4)])
        links = links.reshape((4,) + (N,) * 4 + (4,))
        links = su2.metropolis(links, beta, rng, n_sweeps)
        all_w.extend(fp_spectrum(links, k))
    all_w = np.array(all_w)
    return {"lowest": float(np.min(all_w)),
            "median": float(np.median(all_w)),
            "count_below_0p1": int(np.sum(all_w < 0.1)),
            "count_below_1": int(np.sum(all_w < 1.0)),
            "n_eigs": len(all_w),
            "N": N, "beta": beta}


def gauge_functional(links: np.ndarray) -> float:
    """The lattice Landau-gauge functional `Σ Re(Tr U)/2 = Σ a0` — *maximised* by Landau gauge.

    The FMR is the set of global maxima of this functional over each gauge orbit; the Gribov
    horizon is its boundary, where the FP operator's lowest eigenvalue touches zero.
    """
    return float(np.sum(links[..., 0]))


def random_gauge_transform(links: np.ndarray, rng) -> np.ndarray:
    """Apply an independent random SU(2) gauge transformation `g(x)` at every site.

    Same convention as `landau_gauge_fix`: `U_μ(x) → g(x) U_μ(x)` and
    `U_μ(x−μ) → U_μ(x−μ) g(x)†`.
    """
    d, N = links.shape[0], links.shape[1]
    out = links.copy()
    for flat in range(N ** d):
        x = tuple(np.unravel_index(flat, (N,) * d))
        g = tuple(su2.random_su2(rng))
        for mu in range(d):
            out[mu][x] = su2.qmul(g, out[mu][x])
            xm = list(x); xm[mu] = (xm[mu] - 1) % N
            xm = tuple(xm)
            out[mu][xm] = su2.qmul(out[mu][xm], su2.qconj(g))
    return out


def fmr_gauge_fix(links: np.ndarray, n_copies: int = 5, n_gf: int = 20, seed=None) -> np.ndarray:
    """Gribov-copy search toward the FMR: `n_copies` random transforms, Landau-fix each, keep the
    copy with the *highest* gauge functional (closest to the global maximum / fundamental modular
    region).

    This is Phase 1 of `docs/MASS-GAP-HORIZON-PLAN.md` — the horizon is at the FMR boundary, so an
    arbitrary Landau copy (first Gribov region) is not enough.
    """
    rng = np.random.default_rng(seed)
    best = landau_gauge_fix(links, n_gf)
    best_F = gauge_functional(best)
    for _ in range(max(0, n_copies - 1)):
        cand = landau_gauge_fix(random_gauge_transform(links, rng), n_gf)
        F = gauge_functional(cand)
        if F > best_F:
            best, best_F = cand, F
    return best


__all__ = ["adjoint_matrix", "fp_operator", "fp_operator_sparse", "lowest_fp_eigenvalue",
           "fp_spectrum", "landau_gauge_fix", "gauge_functional", "random_gauge_transform",
           "fmr_gauge_fix", "horizon_concentration", "horizon_concentration_landau",
           "horizon_density"]
