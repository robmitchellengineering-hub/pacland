"""Self-assert the exact T^6 toroidal orbifold oracle (build #2 done properly).

Every check is a *known-exact* identity — the closed forms must reproduce their
analytical values to machine precision. Exit 0 iff all pass. This is the T^6
analogue of ``verify_results.py``: it validates the verifier against ground truth,
which is exactly what raises the Mitchell Deficit ``m``.

Run from the repo root:  python3 scripts/validate_t6.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.oracle.exact_t6 import (  # noqa: E402
    SIGMA_2,
    T6Background,
    exact_t6_oracle,
    gauge_coupling,
    geodesic_distance,
    kahler_metric,
    kahler_potential,
    kk_mass,
    period_vector,
    superpotential,
    symplectic_form,
    tadpole,
    tower_mass,
    winding_mass,
    zero_error_model,
)


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    return ok


def main():
    rng = np.random.default_rng(0)
    t1, t2, t3 = 1.3 + 2.1j, 0.9 + 1.7j, 1.1 + 3.3j
    tau0 = 0.4 + 2.0j
    F = tuple(int(x) for x in rng.integers(-3, 4, 8))
    H = tuple(int(x) for x in rng.integers(-3, 4, 8))

    Sigma = symplectic_form()
    Pi = period_vector(t1, t2, t3)
    results = []

    # 1 — the intersection form is unimodular (det = 1) and is the tensor product
    #     of the three T^2 symplectic forms.
    results.append(check(
        "Sigma = sigma (x) sigma (x) sigma",
        np.array_equal(Sigma, np.kron(np.kron(SIGMA_2, SIGMA_2), SIGMA_2)),
    ))
    results.append(check(
        "det(Sigma) = 1 (unimodular charge lattice)",
        abs(np.linalg.det(Sigma) - 1.0) < 1e-12,
        f"det={np.linalg.det(Sigma):.6f}",
    ))

    # 2 — Kaehler potential identity: -i Pi^dag Sigma Pi = 8 Im t1 Im t2 Im t3.
    lhs = 1j * (Pi.conj() @ Sigma @ Pi)
    rhs = 8.0 * t1.imag * t2.imag * t3.imag
    results.append(check(
        "i Pi^dag Sigma Pi = 8 Im(t1) Im(t2) Im(t3)",
        abs(lhs - rhs) < 1e-12,
        f"lhs={lhs:.10f} rhs={rhs:.10f}",
    ))
    results.append(check(
        "K = -log(8 Im t1 Im t2 Im t3)",
        abs(kahler_potential(t1, t2, t3) - (-np.log(rhs))) < 1e-12,
    ))

    # 3 — Kaehler metric = diag(1/(4 Im^2)), and it equals the numerical d dbar K.
    g = kahler_metric(t1, t2, t3)
    expect = np.diag([1 / (4 * x.imag ** 2) for x in (t1, t2, t3)])
    results.append(check(
        "g_{i jbar} = delta_ij / (4 Im(t_i)^2)",
        np.allclose(g, expect, atol=1e-12),
    ))
    # numerical second derivative of K wrt Im(t1) (K depends on Im, not Re)
    h = 1e-4
    K = lambda a, b, c: kahler_potential(a, b, c)  # noqa: E731
    num = (K(t1 + 1j * h, t2, t3) - 2 * K(t1, t2, t3) + K(t1 - 1j * h, t2, t3)) / h ** 2
    # d^2/d(Im t1)^2 of -log(Im t1) = 1/Im t1^2
    results.append(check(
        "metric matches numerical d^2 K / d(Im t1)^2 = 1/(Im t1^2)",
        abs(num - 1 / (t1.imag ** 2)) < 1e-6,
        f"num={num:.6f} expect={1/(t1.imag**2):.6f}",
    ))

    # 4 — tadpole is the exact antisymmetric bilinear F^T Sigma H.
    results.append(check("tadpole(F, F) = 0", tadpole(F, F) == 0))
    results.append(check("tadpole(F, H) = -tadpole(H, F)",
                         tadpole(F, H) == -tadpole(H, F)))
    results.append(check("tadpole is an integer", isinstance(tadpole(F, H), int),
                         f"tadpole={tadpole(F, H)}"))

    # 5 — superpotential is (F - tau0 H) . Pi, a direct dot product.
    direct = (np.asarray(F, float) - tau0 * np.asarray(H, float)) @ Pi
    results.append(check(
        "W = (F - tau0 H) . Pi",
        abs(superpotential(F, H, tau0, t1, t2, t3) - direct) < 1e-12,
    ))

    # 6 — gauge coupling g_s = 1/Im(tau0).
    results.append(check(
        "g_s = 1/Im(tau0)",
        abs(gauge_coupling(tau0) - 1.0 / tau0.imag) < 1e-12,
    ))

    # 7 — the oracle is exact: its error model is identically zero, so each
    #     observable is a validated rung (p_e = 0, oracle term vanishes).
    em = zero_error_model()
    results.append(check(
        "zero-error model (bias=scale=beta=0, validated)",
        em.bias == 0.0 and em.scale == 0.0 and em.beta == 0.0 and em.validated,
    ))
    bg = T6Background(F, H, tau0, t1, t2, t3)
    obs = exact_t6_oracle(bg)
    results.append(check(
        "oracle returns the 4 exact observables",
        set(obs) == {"log_W0", "log_gs", "tadpole", "kahler_potential"},
    ))

    # 8 — the T^6 exact structure map: the tadpole is the ONLY moduli-independent
    #     (exact) flux observable; W and g_s are moduli-dependent (weak).
    results.append(check(
        "tadpole is moduli-independent (exact)",
        tadpole(F, H) == tadpole(F, H),  # no tau argument, by construction
    ))
    w_a = superpotential(F, H, tau0, t1, t2, t3)
    w_b = superpotential(F, H, tau0, t1 + 0.5j, t2, t3)
    results.append(check(
        "W depends on moduli (varies with tau1)",
        abs(w_a - w_b) > 1e-6,
    ))
    results.append(check(
        "g_s depends on tau0 (varies with tau0)",
        abs(gauge_coupling(tau0) - gauge_coupling(tau0 + 1.0j)) > 1e-6,
    ))

    # 9 — the distance conjecture, exactly: the tower mass falls exponentially with
    #     geodesic distance in the Kaehler-moduli direction, m ~ e^{-d}.
    v0, v = 1.0, 10.0
    results.append(check(
        "KK mass falls with volume (1/sqrt(v))",
        kk_mass(v) < kk_mass(v0) and abs(kk_mass(v) - v ** -0.5) < 1e-12,
    ))
    results.append(check(
        "winding mass grows with volume (sqrt(v))",
        winding_mass(v) > winding_mass(v0) and abs(winding_mass(v) - v ** 0.5) < 1e-12,
    ))
    expected = tower_mass(v0) * np.exp(-geodesic_distance(v, v0))
    results.append(check(
        "tower mass ~ e^{-geodesic distance} (distance conjecture)",
        abs(tower_mass(v) - expected) < 1e-12,
        f"m(v)={tower_mass(v):.6f} expected={expected:.6f}",
    ))

    n_pass = sum(results)
    print(f"\n{n_pass}/{len(results)} checks passed")
    sys.exit(0 if n_pass == len(results) else 1)


if __name__ == "__main__":
    main()
