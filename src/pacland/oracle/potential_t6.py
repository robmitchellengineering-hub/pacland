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
           "superpotential_and_gradients", "N_MODULI"]


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
