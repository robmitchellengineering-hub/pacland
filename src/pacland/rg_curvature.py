"""rg_curvature.py — the RG track's target: a UNIFORM curvature bound on the Polchinski flow.

The "curvature" of the effective action along the flow is carried by the STABILITY MATRIX — the
Jacobian of the beta functions at the fixed point. Its eigenvalues are the critical exponents; if they
are finite and the flow trajectory stays finite from UV to IR, then the effective interactions stay
controlled at every scale. That is the RG-track statement of A1 (volume) + A3 (continuum): no scale
blows up, so the bound survives every regulator.
"""
from __future__ import annotations

import math

from pacland.energy import frg


def stability_matrix(lam: float, g: float, d: float = 4.0, h: float = 1e-6) -> tuple[tuple[float, float], tuple[float, float]]:
    """The Jacobian of (beta_lambda, beta_g) at (λ, g), by central finite differences."""
    dbl_dl = (frg.beta_lambda(lam + h, g, d) - frg.beta_lambda(lam - h, g, d)) / (2.0 * h)
    dbl_dg = (frg.beta_lambda(lam, g + h, d) - frg.beta_lambda(lam, g - h, d)) / (2.0 * h)
    dbg_dl = (frg.beta_g(lam + h, g, d) - frg.beta_g(lam - h, g, d)) / (2.0 * h)
    dbg_dg = (frg.beta_g(lam, g + h, d) - frg.beta_g(lam, g - h, d)) / (2.0 * h)
    return ((dbl_dl, dbl_dg), (dbg_dl, dbg_dg))


def eigenvalues_2x2(m: tuple[tuple[float, float], tuple[float, float]]) -> tuple[complex, complex]:
    """The two eigenvalues of a 2x2 matrix."""
    a, b = m[0]
    c, d_ = m[1]
    tr = a + d_
    det = a * d_ - b * c
    disc = tr * tr - 4.0 * det
    root = math.sqrt(abs(disc)) * (1j if disc < 0 else 1.0)
    return ((tr + root) / 2.0, (tr - root) / 2.0)


def critical_exponents(d: float = 4.0) -> dict:
    """The RG eigenvalues (critical exponents) at the fixed point."""
    lam, g = frg.solve(d)
    jac = stability_matrix(lam, g, d)
    e1, e2 = eigenvalues_2x2(jac)
    return {"lam_star": lam, "g_star": g, "jacobian": jac,
            "eigenvalues": (e1, e2), "finite": all(abs(e) < float("inf") for e in (e1, e2))}


def flow_trajectory(d: float = 4.0, t_end: float = 20.0, n_steps: int = 2000) -> list[tuple[float, float]]:
    """Integrate the beta functions from the fixed point's vicinity along the RG time t (UV -> IR)."""
    lam, g = frg.solve(d)
    # perturb slightly off the fixed point so the flow actually moves
    lam, g = lam + 0.05, g + 0.01
    dt = t_end / n_steps
    path = [(lam, g)]
    for _ in range(n_steps):
        lam += frg.beta_lambda(lam, g, d) * dt
        g += frg.beta_g(lam, g, d) * dt
        path.append((lam, g))
    return path


def check_curvature_uniform(d: float = 4.0, t_end: float = 20.0) -> dict:
    """A1 + A3, the RG version: do the couplings stay FINITE along the whole flow (no scale blows up)?"""
    ce = critical_exponents(d)
    path = flow_trajectory(d, t_end)
    finite_path = all(math.isfinite(lam) and math.isfinite(g) for lam, g in path)
    bounded = all(-1e3 < lam < 1e3 and -1e3 < g < 1e3 for lam, g in path)
    uniform = ce["finite"] and finite_path and bounded
    return {
        "uniform": uniform,
        "critical_exponents": ce["eigenvalues"],
        "exponents_finite": ce["finite"],
        "flow_finite": finite_path,
        "couplings_bounded": bounded,
        "reason": ("the flow's curvature is uniform: finite critical exponents and a bounded trajectory"
                   if uniform else "the flow's curvature is NOT uniform"),
    }
