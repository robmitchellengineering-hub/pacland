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


def polyakov_loops(links):
    """The Polyakov loops P(x) = prod_t U_0(t, x), one 4-quaternion per spatial site."""
    d, N = links.shape[0], links.shape[1]
    P = np.ones((N,) * (d - 1) + (4,))
    for flat in range(N ** (d - 1)):
        xs = tuple(np.unravel_index(flat, (N,) * (d - 1)))
        u = np.array([1.0, 0.0, 0.0, 0.0])
        for t in range(N):
            u = qmul(u, links[0][(t,) + xs])
        P[xs] = u
    return P


def polyakov_correlator(links, R_max):
    """Connected Polyakov-loop correlator C(R) = <TrP(0) TrP(R)> - <TrP>^2, spatial separation R."""
    d, N = links.shape[0], links.shape[1]
    trP = 2.0 * polyakov_loops(links)[..., 0]  # Tr P = 2*a0, shape (N,)*(d-1)
    meanP = float(np.mean(trP))
    C = []
    for R in range(1, R_max + 1):
        acc = 0.0
        cnt = 0
        for mu in range(1, d):
            for flat in range(N ** (d - 1)):
                x = np.unravel_index(flat, (N,) * (d - 1))
                y = list(x); y[mu - 1] = (y[mu - 1] + R) % N; y = tuple(y)
                acc += trP[tuple(x)] * trP[y]
                cnt += 1
        C.append(acc / cnt - meanP * meanP)
    return np.array(C)


def _polyakov_config(args):
    """One config's Polyakov correlator (module-level, for ProcessPoolExecutor)."""
    beta, N, n_sweeps, R_max, seed = args
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(4 * N ** 4)])
    links = links.reshape((4,) + (N,) * 4 + (4,))
    try:
        from pacland.lattice_ym_su2_fast import metropolis_fast
        links = metropolis_fast(links, beta, n_sweeps, seed)
    except ImportError:
        links = metropolis(links, beta, rng, n_sweeps)
    return np.maximum(polyakov_correlator(links, R_max), 1e-12)


def string_tension_from_polyakov(beta, N=8, n_configs=20, n_sweeps=12, R_max=3, seed=0):
    """The string tension sigma from the Polyakov-loop potential V(R) = -ln C(R) ~ sigma R + c.

    Configs run in parallel (ProcessPoolExecutor) — the pure-Python Metropolis is the bottleneck, and
    the configs are independent, so this is ~ncores faster. Averaged over configs; a linear fit of V(R)
    over R = 1..R_max gives sigma. This is the Phase-2 scale-setting observable for SU(2)."""
    import os
    from concurrent.futures import ProcessPoolExecutor

    d = 4
    workers = min(6, os.cpu_count() or 1)
    args = [(beta, N, n_sweeps, R_max, seed + i) for i in range(n_configs)]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        C_sum = np.sum(np.array(list(ex.map(_polyakov_config, args))), axis=0)
    C_avg = C_sum / n_configs
    V = -np.log(C_avg)
    R = np.arange(1, R_max + 1)
    # linear fit V = sigma * R + c
    A = np.vstack([R, np.ones_like(R)]).T
    sigma, c = np.linalg.lstsq(A, V, rcond=None)[0]
    return {"sigma": float(sigma), "V": V.tolist(), "R": R.tolist(),
            "beta": beta, "N": N, "n_configs": n_configs}


def scale_a(sigma: float, sigma_ref: float, a_ref: float = 1.0) -> float:
    """The lattice spacing a = a_ref * sqrt(sigma_ref / sigma) — the Phase-2 renormalisation.

    `lambda_phys = lambda / a^2`; this converts a lattice-unit FP eigenvalue to physical units once
    sigma(beta) is measured."""
    return float(a_ref * np.sqrt(sigma_ref / sigma))


def staple_sum(links, mu, x):
    """The sum of the 2(d-1) staples around the link U_mu(x) — a 4-quaternion (the force direction
    of the Wilson flow)."""
    d, N = links.shape[0], links.shape[1]
    Z = np.zeros(4)
    for nu in range(d):
        if nu == mu:
            continue
        xn = list(x); xn[nu] = (xn[nu] + 1) % N; xn = tuple(xn)
        xm = list(x); xm[mu] = (xm[mu] + 1) % N; xm = tuple(xm)
        fwd = qmul(links[nu][tuple(x)], links[mu][xn])
        fwd = qmul(fwd, qconj(links[nu][xm]))
        Z += np.array(fwd)
        xnm = list(x); xnm[nu] = (xnm[nu] - 1) % N; xnm = tuple(xnm)
        xnm2 = list(xnm); xnm2[mu] = (xnm2[mu] + 1) % N; xnm2 = tuple(xnm2)
        bwd = qmul(qconj(links[nu][xnm]), links[mu][xnm])
        bwd = qmul(bwd, links[nu][xnm2])
        Z += np.array(bwd)
    return Z


def wilson_flow_step(links, epsilon=0.05):
    """One Euler step of the Wilson (gradient) flow: V_mu -> exp(-epsilon * F) V_mu, where F is the
    traceless anti-hermitian part of (staple * V^dag). Minimises the action, so the energy density
    decreases with flow time."""
    d, N = links.shape[0], links.shape[1]
    out = links.copy()
    for mu in range(d):
        for flat in range(N ** d):
            x = tuple(np.unravel_index(flat, (N,) * d))
            V = links[mu][x]
            Z = staple_sum(links, mu, x)
            w = qmul(Z, qconj(V))          # Z V^dag = (w0, w1, w2, w3)
            f = np.array([w[1], w[2], w[3]])  # the anti-hermitian part
            norm = float(np.linalg.norm(f))
            if norm < 1e-12:
                continue
            theta = epsilon * norm
            c, s = np.cos(theta), np.sin(theta) / norm   # rotate TOWARD the staple (descent)
            r = (c, s * f[0], s * f[1], s * f[2])
            out[mu][x] = qmul(r, V)
    return out


def energy_density(links):
    """The Wilson-flow energy density E(t) = <1 - 1/2 Re Tr U_plaq> — decreases with flow time."""
    d, N = links.shape[0], links.shape[1]
    total = 0.0
    count = 0
    for mu in range(d):
        for nu in range(mu + 1, d):
            for flat in range(N ** d):
                x = tuple(np.unravel_index(flat, (N,) * d))
                total += 1.0 - 0.5 * plaquette_trace(links, mu, nu, x)
                count += 1
    return total / count


def wilson_flow_scale(beta, N=8, n_flow_steps=200, epsilon=0.05, target=0.08,
                      n_sweeps=10, seed=0):
    """The Wilson-flow scale t0 where t^2 E(t) = target, in lattice units.

    NOTE: this uses the SIMPLE plaquette energy density, whose t^2 E plateaus at ~0.11 (the clover
    definition reaches the standard 0.3). So the target here is 0.08 — a fixed convention; the
    renormalisation only uses the RATIO t0(beta) across beta, so the absolute target cancels.
    Returns t0, or None if the target is not reached within n_flow_steps."""
    d = 4
    rng = np.random.default_rng(seed)
    links = np.array([random_su2(rng) for _ in range(d * N ** d)])
    links = links.reshape((d,) + (N,) * d + (4,))
    try:
        from pacland.lattice_ym_su2_fast import metropolis_fast
        links = metropolis_fast(links, beta, n_sweeps, seed)
    except ImportError:
        links = metropolis(links, beta, rng, n_sweeps)
    t = 0.0
    E_prev = energy_density(links)
    t2E_prev = 0.0
    eps_eff = epsilon * (4.0 / float(beta))  # g0^2 = 4/beta: the Wilson-flow rate
    for _ in range(n_flow_steps):
        links = wilson_flow_step(links, eps_eff)
        t += epsilon
        E = energy_density(links)
        t2E = t * t * E
        if t2E >= target:
            # linear interpolation in t2E between the previous and current step
            if t2E > t2E_prev:
                frac = (target - t2E_prev) / (t2E - t2E_prev)
                return t - epsilon + epsilon * frac
            return t
        E_prev = E
        t2E_prev = t2E
    return None


__all__ = ["qmul", "qconj", "random_su2", "plaquette_trace", "metropolis",
           "wilson_loop", "creutz_ratio", "measure_string_tension",
           "polyakov_loops", "polyakov_correlator", "string_tension_from_polyakov", "scale_a",
           "staple_sum", "wilson_flow_step", "energy_density", "wilson_flow_scale"]
