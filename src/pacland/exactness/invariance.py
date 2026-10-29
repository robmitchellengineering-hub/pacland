"""X4 + X5 — invariance and identity checks on the scalar potential, in the interior.

Four checks. The first three are properties the assembly must have **everywhere**, not only at a
special point, which is what makes them useful where the vacua are:

1. **the F-term is the covariant one** — `D_i W = d_i W + K_i W`. `f_terms` is compared against an
   independent derivative of `W` (through the period vector, not through `period_derivatives`) plus
   the analytic `K_i`. Drop the `K_i W` term — or use `K_i` of the wrong modulus — and this goes red.
2. **a constant Kaehler transformation is invisible** — `W -> e^{i theta} W` with `K` fixed is the
   constant case of `K -> K + f + fbar`. `V` is manifestly invariant; an assembly whose two terms
   scale differently (the classic mismatched-conjugation bug) is not.
3. **V is homogeneous of degree 2 in the flux** — `V(dF, dH) = d^2 V(F, H)`, exactly, because `D_i W`
   is linear in the flux. This is the base of the `d`-scaling control below.
4. **the unfolded spacing statistic is invariant under that scaling** — `M^2 -> d^2 M^2` at a shared
   critical point, and an overall scale drops out of unfolded spacings. So an ensemble that mixes
   `d` values is provably clean for a level-statistics question: the flux-scaling content cannot
   contaminate the chaos question.

Plus one identity that only holds *at* a supersymmetric point, and is therefore a check on the solver
as much as on the potential:

5. **at `DW = 0`, `V = -3 e^K |W|^2` exactly.** The `-3|W|^2` no-scale term cancels only when the
   Kaehler sector is flat; with `D_i W = 0` every term in `g^{i jbar} D_i W D_jbar Wbar` vanishes, so
   what remains is the negative piece. A supersymmetric vacuum on this model is **AdS4 with a
   cosmological constant fixed by `e^K |W|^2`** — not Minkowski, and not tunable. `docs/plan-exact-terms.md`
   said "Minkowski" in v2; this module is where that was measured and corrected.

Run:        python3 scripts/exactness.py
Guarded by: tests/test_exactness_invariance.py
"""
from __future__ import annotations

import numpy as np

from ..oracle import exact_t6 as T
from ..oracle import potential_t6 as P
from ..spectral import zeros as Z


def _w(F, H, taus) -> complex:
    return complex(T.superpotential(F, H, taus[0], taus[1], taus[2], taus[3]))


def f_term_covariance(F, H, taus: list[complex], step: float = 1e-7) -> dict:
    """Compare `f_terms` with an independent `d_i W + K_i W`.

    The independent route differentiates `W` itself, through the period vector and the `F - tau0 H`
    combination, so it shares no code with `period_derivatives`.
    """
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    w = _w(F, H, taus)
    kg = P.kahler_gradients(*taus)
    expected = []
    for i in range(P.N_MODULI):
        up = list(taus)
        dn = list(taus)
        up[i] = taus[i] + step
        dn[i] = taus[i] - step
        dw_i = (_w(F, H, up) - _w(F, H, dn)) / (2.0 * step)
        expected.append(dw_i + kg[i] * w)
    expected = np.array(expected)
    actual = P.f_terms(F, H, taus)
    scale = max(float(np.max(np.abs(expected))), float(np.max(np.abs(actual))), 1e-30)
    residual = float(np.max(np.abs(actual - expected)) / scale)
    return {"check": "D_i W is the covariant derivative (the K_i W term is present and correct)",
            "pass": residual < 1e-6, "detail": f"max relative residual {residual:.2e}",
            "residual": residual}


def phase_invariance(F, H, taus: list[complex], theta: float = 0.7) -> dict:
    """`W -> e^{i theta} W` (a constant Kaehler transformation) must leave `V` unchanged."""
    k = P.kahler_full(*taus)
    w, dw = P.superpotential_and_gradients(F, H, taus[0], taus[1], taus[2], taus[3])
    kg = P.kahler_gradients(*taus)
    ginv = np.linalg.inv(P.kahler_metric(*taus))
    d = np.exp(1j * theta) * np.array([dw[i] + kg[i] * w for i in range(P.N_MODULI)])
    v_rotated = float(np.real(np.exp(k) * (d.conj() @ ginv @ d - 3.0 * abs(w) ** 2)))
    v = P.potential(F, H, *taus)
    scale = max(abs(v), abs(v_rotated), 1e-30)
    residual = abs(v - v_rotated) / scale
    return {"check": "V is invariant under the constant Kaehler transformation W -> e^{i theta} W",
            "pass": residual < 1e-10, "detail": f"{v:.12e} vs {v_rotated:.12e}", "residual": residual}


def homogeneity(F, H, taus: list[complex], d: float = 3.0) -> dict:
    """`V(dF, dH) = d^2 V(F, H)`, exactly, because `D_i W` is linear in the flux."""
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    v1 = P.potential(F, H, *taus)
    vd = P.potential(d * F, d * H, *taus)
    expected = d * d * v1
    scale = max(abs(expected), abs(vd), 1e-30)
    residual = abs(vd - expected) / scale
    return {"check": f"V is homogeneous of degree 2: V({d:g}F, {d:g}H) = {d:g}^2 V(F, H)",
            "pass": residual < 1e-10, "detail": f"{vd:.12e} vs {expected:.12e}", "residual": residual}


def unfolded_spacings(values: list[float]) -> list[float]:
    """Sorted spacings divided by their own mean — mean 1 by construction, so scale-free."""
    v = sorted(float(x) for x in values)
    s = [b - a for a, b in zip(v, v[1:])]
    mean = sum(s) / len(s) if s else 0.0
    return [x / mean for x in s] if mean else []


def spacing_invariance(F, H, taus: list[complex] | None = None, d: float = 2.0) -> dict:
    """The unfolded spectrum and the ratio statistic are invariant under `(F, H) -> d(F, H)`.

    This is the flux-scaling lemma's consequence for level statistics: the content `d` multiplies
    `M^2` by `d^2` at a shared critical point, and unfolding removes the scale. So mixing `d` in an
    ensemble cannot manufacture or hide a spacing distribution.
    """
    taus = taus or [1j, 1j, 2j, 1.5j]
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    m1 = P.mass_spectrum(F, H, *taus)
    md = P.mass_spectrum(d * F, d * H, *taus)
    ratio = [md[i] / m1[i] for i in range(len(m1)) if abs(m1[i]) > 1e-14]
    scale_ok = all(abs(r - d * d) <= 1e-6 * d * d for r in ratio) if ratio else False
    s1 = unfolded_spacings(m1)
    sd = unfolded_spacings(md)
    unfolded_ok = (len(s1) == len(sd) and
                   all(abs(a - b) <= 1e-9 * max(1.0, abs(a)) for a, b in zip(s1, sd)))
    r1 = Z.ratio_statistic(s1) if len(s1) > 1 else float("nan")
    rd = Z.ratio_statistic(sd) if len(sd) > 1 else float("nan")
    return {"check": f"the unfolded spectrum is invariant under (F,H) -> {d:g}(F,H)",
            "pass": bool(scale_ok and unfolded_ok),
            "detail": f"eigenvalue ratio {min(ratio) if ratio else float('nan'):.9f} vs {d*d:g}; "
                      f"ratio statistic {r1:.12f} vs {rd:.12f}",
            "ratio_statistic": r1, "ratio_statistic_scaled": rd}


def susy_value_identity(tau_star: list[complex] | None = None) -> dict:
    """At a supersymmetric point, `V = -3 e^K |W|^2` exactly — AdS4, not Minkowski.

    The point is *constructed* (a flux that is F-flat there) and then *recovered* by Newton, so this
    is the same construct-and-recover test the solver carries, plus the identity.
    """
    r = P.validation_by_construction(tau_star) if tau_star else P.validation_by_construction()
    taus = r.get("recovered")
    if taus is None:
        return {"check": "at DW = 0, V = -3 e^K |W|^2", "pass": False,
                "detail": "the solver did not recover the constructed vacuum, so the identity is "
                          "not testable here — reported as a failure, not a skip",
                "value": None, "expected": None}
    target = r["target"]
    sol = P.flux_flat_at(target)
    F, H = sol[:8], sol[8:]
    k = P.kahler_full(*taus)
    w = _w(F, H, taus)
    v = P.potential(F, H, *taus)
    expected = -3.0 * float(np.exp(k)) * abs(w) ** 2
    scale = max(abs(expected), 1e-30)
    residual = abs(v - expected) / scale
    return {"check": "at DW = 0, V = -3 e^K |W|^2  (a SUSY vacuum here is AdS4, not Minkowski)",
            "pass": residual < 1e-6, "detail": f"V {v:.12e} vs -3e^K|W|^2 {expected:.12e} "
                                              f"(relative {residual:.2e}), V < 0: {v < 0}",
            "value": v, "expected": expected, "residual": residual}


def report() -> dict:
    """Every check in this module, on one flux choice."""
    taus = [0.3 + 1.1j, -0.2 + 0.9j, 0.1 + 1.4j, 0.4 + 0.8j]
    F = np.zeros(8); H = np.zeros(8)
    F[0], F[3], H[1], H[5] = 1.0, -2.0, 1.0, 3.0
    checks = [
        f_term_covariance(F, H, taus),
        phase_invariance(F, H, taus),
        homogeneity(F, H, taus),
        spacing_invariance(F, H, taus),
        susy_value_identity(),
    ]
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks)}


__all__ = ["f_term_covariance", "phase_invariance", "homogeneity", "unfolded_spacings",
           "spacing_invariance", "susy_value_identity", "report"]
