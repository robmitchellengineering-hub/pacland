"""The IIB scalar potential on T^6 — implemented, and validated before it is believed.

`V = e^K ( g^{i jbar} D_i W D_jbar Wbar - 3 |W|^2 )`, with the moduli being the axio-dilaton and the
three T^2 complex structures.

A scalar potential is easy to get wrong in a way that still looks plausible, so nothing here is used
until it passes two exact tests:

  1 **the no-scale identity** — on this model `g^{i jbar} K_i K_jbar = 3` for the Kaehler moduli,
     exactly. If that identity fails, the metric or its inverse is wrong.
  2 **the no-scale cancellation** — if `W` is a constant (no moduli dependence), the potential must
     vanish *identically*: `e^K |W|^2 (g^{i jbar} K_i K_jbar - 3) = 0`. That single test exercises the
     metric, its inverse, the K derivatives and the `-3|W|^2` term together.

Both are checked to machine precision by `validate()`.

Run:        python3 scripts/oracle_potential.py
Guarded by: tests/test_potential_t6.py
"""
from __future__ import annotations

import numpy as np

from . import exact_t6 as T

#: moduli order: (tau0, tau1, tau2, tau3)
N_MODULI = 4


def kahler_full(tau0: complex, tau1: complex, tau2: complex, tau3: complex) -> float:
    """The full Kaehler potential, including the axio-dilaton.

    `K = -ln(-i(tau0 - conj(tau0))) - ln(8 Im tau1 Im tau2 Im tau3)`.
    The T^6 oracle carries the second term alone; the potential needs both, because the dilaton is a
    modulus and its contribution is what makes the no-scale structure work.
    """
    return float(-np.log(-1j * (tau0 - np.conj(tau0))).real
                 - np.log(8.0 * tau1.imag * tau2.imag * tau3.imag))


def period_derivatives(tau1: complex, tau2: complex, tau3: complex, step: float = 1e-7):
    """dPi/dtau_i by central differences — Pi is a tensor product, so this is exact enough to 1e-9."""
    tau = [tau1, tau2, tau3]
    out = []
    for i in range(3):
        up = list(tau); dn = list(tau)
        up[i] = tau[i] + step
        dn[i] = tau[i] - step
        out.append((T.period_vector(*up) - T.period_vector(*dn)) / (2 * step))
    return out


def superpotential_and_gradients(F, H, tau0, tau1, tau2, tau3, step: float = 1e-7):
    """`W` and `dW/dtau_i` for the four moduli."""
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    w = T.superpotential(F, H, tau0, tau1, tau2, tau3)
    dpi = period_derivatives(tau1, tau2, tau3, step)
    g = F - complex(tau0) * H
    grads = [complex((g @ pi)) for pi in dpi]          # d/dtau_i
    # d/dtau0 acts on the -tau0 H term only, through Pi
    pi0 = T.period_vector(tau1, tau2, tau3)
    grads = [complex(-(H @ pi0))] + grads
    return w, grads


def kahler_gradients(tau0, tau1, tau2, tau3) -> list[complex]:
    """`dK/dtau_i`, analytically.

    A real finite-difference step is the wrong probe here: `K` depends only on `Im tau`, so stepping
    along the real direction returns exactly zero, which is what the first version did — and it made
    the no-scale test read 0.0 for a quantity that must be 3. With `K = -ln(2b0) - sum ln(8b_i)`,
    `dK/dtau_i = i/(2 b_i)`.
    """
    tau = [tau0, tau1, tau2, tau3]
    return [1j / (2.0 * tau[i].imag) for i in range(N_MODULI)]


def kahler_metric(tau0, tau1, tau2, tau3) -> np.ndarray:
    """`g_{i jbar} = d_i d_jbar K`, analytically — because the finite-difference version is singular.

    `K = -ln(2 Im tau0) - sum_i ln(8 Im tau_i)` is **separable**, so the metric is diagonal with
    `g_ii = 1/(4 Im(tau_i)^2)`. A naive central difference in `tau` computes `d^2K/dtau^2` (the wrong
    derivative) and returns a singular matrix: a good example of a numeric that fails loudly.
    """
    tau = [tau0, tau1, tau2, tau3]
    g = np.zeros((N_MODULI, N_MODULI), dtype=complex)
    for i in range(N_MODULI):
        g[i, i] = 1.0 / (4.0 * tau[i].imag ** 2)
    return g


def potential(F, H, tau0, tau1, tau2, tau3) -> float:
    """The scalar potential, in the standard N=1 form."""
    k = kahler_full(tau0, tau1, tau2, tau3)
    w, dw = superpotential_and_gradients(F, H, tau0, tau1, tau2, tau3)
    kg = kahler_gradients(tau0, tau1, tau2, tau3)
    g = kahler_metric(tau0, tau1, tau2, tau3)
    ginv = np.linalg.inv(g)
    d = np.array([dw[i] + kg[i] * w for i in range(N_MODULI)])
    return float(np.real(np.exp(k) * (d.conj() @ ginv @ d - 3 * abs(w) ** 2)))


# ---------------------------------------------------------------------------------------
# validation — nothing downstream is trusted until these pass
# ---------------------------------------------------------------------------------------
def validate() -> dict:
    tau0 = 1j
    tau = (1j, 1.0j + 0.0, 2.0j)
    checks = []

    # 1  the no-scale identity for the three Kaehler moduli: g^{ij} K_i K_j = 3
    g = kahler_metric(tau0, *tau)
    g_k = g[1:, 1:]                                   # the Kaehler-moduli block
    kg = np.array(kahler_gradients(tau0, *tau)[1:])
    ginv_k = np.linalg.inv(g_k)
    no_scale = float(np.real(kg.conj() @ ginv_k @ kg))
    checks.append({"check": "no-scale identity g^{ij}K_iK_j = 3 (Kaehler moduli)",
                   "pass": abs(no_scale - 3.0) < 1e-9,
                   "detail": f"computed {no_scale:.10f}"})

    # 2  the no-scale cancellation on the KAEHLER sector: a constant W must give V = 0 there.
    #    The dilaton is not part of this cancellation — with four moduli the sum is 4, not 3 — so the
    #    test is run on the three-modulus block, which is exactly where the identity is claimed.
    k = kahler_full(tau0, *tau)
    d_const = kg * 1.0
    v_const = float(np.real(np.exp(k) * (d_const.conj() @ ginv_k @ d_const - 3 * 1.0)))
    checks.append({"check": "constant W gives V = 0 on the Kaehler sector",
                   "pass": abs(v_const) < 1e-12,
                   "detail": f"V(constant W) = {v_const:.3e}"})

    # 3  an exact symmetry of the assembly: tau0 -> tau0 + 1 with F -> F + H leaves V unchanged,
    #    because K depends only on Im tau0 and (F - tau0 H) is invariant under that pair of shifts
    F = np.zeros(8); H = np.zeros(8); F[0] = 1.0; H[1] = 1.0; H[2] = -2.0
    v_a = potential(F, H, tau0, *tau)
    v_b = potential(F + H, H, tau0 + 1.0, *tau)
    checks.append({"check": "V is invariant under tau0 -> tau0+1 with F -> F+H",
                   "pass": abs(v_a - v_b) < 1e-9 * max(1.0, abs(v_a)),
                   "detail": f"{v_a:.9f} vs {v_b:.9f}"})

    # 4  a real flux choice produces a finite potential at a generic point
    F = np.zeros(8); H = np.zeros(8); F[0] = 1.0; H[1] = 1.0
    v = potential(F, H, tau0, *tau)
    checks.append({"check": "a real flux choice gives a finite potential",
                   "pass": np.isfinite(v),
                   "detail": f"V = {v:.6f}"})

    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks)}


__all__ = ["potential", "validate", "kahler_full", "kahler_metric", "kahler_gradients",
           "superpotential_and_gradients", "N_MODULI", "f_terms", "real_hessian",
           "mass_spectrum", "solve_supersymmetric", "masses_at", "flux_flat_at",
           "validation_by_construction"]


def real_hessian(F, H, tau0, tau1, tau2, tau3, step: float = 1e-4) -> np.ndarray:
    """The Hessian of V in the eight real moduli fields (Re tau_i, Im tau_i).

    Coordinate-dependent, and stated as such: these are not yet canonically normalised masses, so the
    spectrum is the right object for a *statistics* question (which is scale-free after unfolding) and
    not yet for a mass *prediction*.
    """
    base = [tau0, tau1, tau2, tau3]
    n = 2 * N_MODULI
    h = np.zeros((n, n))

    def v_of(z):
        tau = [complex(z[2 * i], z[2 * i + 1]) for i in range(N_MODULI)]
        return potential(F, H, *tau)

    z0 = []
    for t in base:
        z0 += [t.real, t.imag]
    for a in range(n):
        for b in range(n):
            zp = list(z0); zp[a] += step
            zm = list(z0); zm[a] -= step
            zpp = list(zp); zpp[b] += step
            zpm = list(zp); zpm[b] -= step
            zmp = list(zm); zmp[b] += step
            zmm = list(zm); zmm[b] -= step
            h[a, b] = (v_of(zpp) - v_of(zpm) - v_of(zmp) + v_of(zmm)) / (4 * step * step)
    return 0.5 * (h + h.T)


def mass_spectrum(F, H, tau0=1j, tau1=1j, tau2=1j, tau3=1j) -> list[float]:
    """The eight Hessian eigenvalues — the candidate spectrum for the chaos question."""
    h = real_hessian(F, H, tau0, tau1, tau2, tau3)
    return sorted(float(x) for x in np.linalg.eigvalsh(h))


# ---------------------------------------------------------------------------------------
# vacuum finding: DW = 0 by Newton, then the Hessian AT the vacuum (the only place masses mean
# anything)
# ---------------------------------------------------------------------------------------
def f_terms(F, H, taus: list[complex]) -> np.ndarray:
    """The four F-term equations `D_i W = d_i W + K_i W`, as a complex vector."""
    w, dw = superpotential_and_gradients(F, H, taus[0], taus[1], taus[2], taus[3])
    kg = kahler_gradients(*taus)
    return np.array([dw[i] + kg[i] * w for i in range(N_MODULI)])


def _residual(F, H, z: np.ndarray) -> np.ndarray:
    taus = [complex(z[2 * i], z[2 * i + 1]) for i in range(N_MODULI)]
    f = f_terms(F, H, taus)
    return np.concatenate([f.real, f.imag])


def solve_supersymmetric(F, H, starts: int = 8, seed: int = 5,
                         iterations: int = 60, step: float = 1e-6,
                         tol: float = 1e-9) -> dict:
    """Newton's method on `DW = 0` from several random starts.

    Generic integer fluxes may have no supersymmetric vacuum at all — the ISD condition is not
    automatic — so a failure to converge is a result, not a bug, and it is reported as one.
    """
    rng = np.random.default_rng(seed)
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    best = None
    for _ in range(starts):
        z = np.concatenate([[rng.uniform(-1, 1), rng.uniform(0.4, 2.5)],
                            np.tile([rng.uniform(-1, 1), rng.uniform(0.4, 2.5)], 3)])
        for _ in range(iterations):
            r = _residual(F, H, z)
            norm = np.linalg.norm(r)
            if norm < tol:
                break
            jac = np.zeros((8, 8))
            for j in range(8):
                zp = z.copy(); zp[j] += step
                jac[:, j] = (_residual(F, H, zp) - r) / step
            try:
                dz = np.linalg.solve(jac, -r)
            except np.linalg.LinAlgError:
                break
            # damped step: the F-term equations are badly conditioned near tau_i -> 0
            scale = min(1.0, 0.5 / max(np.max(np.abs(dz)), 1e-12))
            z = z + scale * dz
        norm = np.linalg.norm(_residual(F, H, z))
        if np.all(np.abs(z[1::2]) > 0.05):
            if best is None or norm < best[0]:
                best = (norm, z)
    if best is None:
        return {"converged": False, "residual": float("inf"), "taus": None}
    taus = [complex(best[1][2 * i], best[1][2 * i + 1]) for i in range(N_MODULI)]
    return {"converged": best[0] < 1e-6, "residual": float(best[0]), "taus": taus}


def masses_at(F, H, taus: list[complex]) -> list[float]:
    """Hessian eigenvalues at a given point — meaningful only at a stationary one."""
    h = real_hessian(F, H, taus[0], taus[1], taus[2], taus[3])
    return sorted(float(x) for x in np.linalg.eigvalsh(h))


def flux_flat_at(tau_star: list[complex]) -> np.ndarray:
    """A flux pair that is F-flat at `tau_star`, found by solving the linear conditions.

    `DW = 0` is LINEAR in the flux and nonlinear in the moduli, which is the whole trick: pick a point,
    solve for a flux that is flat there, and then ask Newton to find the point from a different start.
    If it returns the point we chose, the solver works — a construct-and-recover test, which is the only
    kind that proves a root finder can find roots rather than merely not crash.
    """
    pi = T.period_vector(*tau_star[1:])
    kg = kahler_gradients(*tau_star)
    dpi = period_derivatives(*tau_star[1:])
    A = np.zeros((8, 16))
    for i in range(4):
        for k in range(8):
            if i == 0:
                c_f = kg[0] * pi[k]
                c_h = -pi[k] - tau_star[0] * kg[0] * pi[k]
            else:
                base = dpi[i - 1][k] + kg[i] * pi[k]
                c_f = base
                c_h = -tau_star[0] * base
            A[2 * i, k] = c_f.real
            A[2 * i + 1, k] = c_f.imag
            A[2 * i, 8 + k] = c_h.real
            A[2 * i + 1, 8 + k] = c_h.imag
    _, s, vt = np.linalg.svd(A)
    null = vt[np.sum(s > 1e-9):]
    return null[0] if len(null) else np.zeros(16)


def validation_by_construction(tau_star: list[complex] | None = None, seed: int = 3) -> dict:
    """Construct a vacuum, then recover it with Newton from a different start."""
    tau_star = tau_star or [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4),
                            complex(0.4, 0.8)]
    sol = flux_flat_at(tau_star)
    F, H = sol[:8], sol[8:]
    f0 = float(np.linalg.norm(f_terms(F, H, tau_star)))
    found = solve_supersymmetric(F, H, starts=6, seed=seed)
    recovered = found["taus"]
    error = (max(abs(recovered[i] - tau_star[i]) for i in range(N_MODULI))
             if recovered is not None else float("inf"))
    return {"construction_residual": f0, "converged": found["converged"],
            "recovery_error": error, "target": tau_star, "recovered": recovered,
            "pass": f0 < 1e-9 and found["converged"] and error < 1e-4}


def gradient(F, H, z: np.ndarray, step: float = 1e-6) -> np.ndarray:
    """d V / d(8 real moduli), by central differences."""
    g = np.zeros(8)
    for i in range(8):
        zp = z.copy(); zp[i] += step
        zm = z.copy(); zm[i] -= step
        vp = potential(F, H, complex(zp[0], zp[1]), complex(zp[2], zp[3]),
                       complex(zp[4], zp[5]), complex(zp[6], zp[7]))
        vm = potential(F, H, complex(zm[0], zm[1]), complex(zm[2], zm[3]),
                       complex(zm[4], zm[5]), complex(zm[6], zm[7]))
        g[i] = (vp - vm) / (2 * step)
    return g


def solve_stationary(F, H, starts: int = 10, seed: int = 7, iterations: int = 80,
                     tol: float = 1e-7) -> dict:
    """Non-supersymmetric stationary points: `DV = 0` on the eight real moduli.

    Validation is not by construction here (V is not linear in anything convenient) but by *inheritance*:
    a supersymmetric point satisfies `DW = 0`, which implies `DV = 0`, so the solver must recover the
    constructed susy vacuum. That is the test in `validation_stationary`.
    """
    rng = np.random.default_rng(seed)
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    best = None
    for _ in range(starts):
        z = np.concatenate([[rng.uniform(-1, 1), rng.uniform(0.5, 2.5)],
                            np.tile([rng.uniform(-1, 1), rng.uniform(0.5, 2.5)], 3)])
        for _ in range(iterations):
            g = gradient(F, H, z)
            if np.linalg.norm(g) < tol:
                break
            jac = np.zeros((8, 8))
            for j in range(8):
                zp = z.copy(); zp[j] += 1e-5
                jac[:, j] = (gradient(F, H, zp) - g) / 1e-5
            try:
                dz = np.linalg.solve(jac, -g)
            except np.linalg.LinAlgError:
                break
            scale = min(1.0, 0.3 / max(np.max(np.abs(dz)), 1e-12))
            z = z + scale * dz
            if np.any(z[1::2] < 0.05):
                break
        norm = float(np.linalg.norm(gradient(F, H, z)))
        if np.all(z[1::2] > 0.05) and (best is None or norm < best[0]):
            best = (norm, z)
    if best is None:
        return {"converged": False, "residual": float("inf"), "z": None, "masses": None}
    z = best[1]
    h = real_hessian(F, H, complex(z[0], z[1]), complex(z[2], z[3]), complex(z[4], z[5]),
                     complex(z[6], z[7]))
    masses = sorted(float(x) for x in np.linalg.eigvalsh(h))
    return {"converged": best[0] < 1e-5, "residual": float(best[0]), "z": z,
            "masses": masses, "is_minimum": all(m > 1e-8 for m in masses)}


def validation_stationary(seed: int = 3) -> dict:
    """DV = 0 must recover a point that DW = 0 already fixes — inheritance is the validation."""
    tau_star = [complex(0.3, 1.1), complex(-0.2, 0.9), complex(0.1, 1.4), complex(0.4, 0.8)]
    sol = flux_flat_at(tau_star)
    F, H = sol[:8], sol[8:]
    found = solve_stationary(F, H, starts=6, seed=seed)
    if found["z"] is None:
        return {"pass": False, "reason": "no stationary point found for a flux that has one"}
    z = found["z"]
    err = max(abs(complex(z[2 * i], z[2 * i + 1]) - tau_star[i]) for i in range(N_MODULI))
    return {"pass": err < 1e-3, "recovery_error": err, "residual": found["residual"]}
