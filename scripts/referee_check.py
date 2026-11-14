"""The referee: a candidate gap theorem must reproduce these two numbers.

    python3 scripts/referee_check.py

Re-measures the SU(2) glueball mass across β, fits m(β) = A·e^(−c′β), and asserts the two referee
numbers hold:
  · m/√σ ≈ 3.2 (β = 1.8–2.0, the SU(2) 0⁺⁺ ratio — validated, not new)
  · m(β) = 25.28·e^(−1.182β) (the scaling law, c = 1.182 > 0)

Any candidate proof of the volume-uniform join must reproduce these when instantiated at the lattice
numbers. This script is that check, re-runnable and exact.
"""
from __future__ import annotations

import sys

import numpy as np
from scipy.optimize import curve_fit

sys.path.insert(0, "src")
from pacland import kernel as nb  # noqa: E402
from pacland import lattice_ym_su2 as py  # noqa: E402


def main(argv) -> int:
    betas = [1.8, 2.0, 2.2, 2.4]
    ms = []
    for beta in betas:
        C, m_eff, _ = nb.measure_glueball(beta, 4, 8, 30, 4000, 0)
        ms.append(m_eff[0])
    ms = np.array(ms)
    betas_np = np.array(betas)

    # fit m(β) = A·e^(−c′β)
    def af(b, A, c):
        return A * np.exp(-c * b)
    popt, _ = curve_fit(af, betas_np, ms, p0=[25, 1.1], maxfev=10000)
    A, c = popt

    # the ratio m/√σ at β = 2.0, with a thermalized Creutz ratio (40 sweeps, not 3)
    rng = np.random.default_rng(0)
    links = np.array([py.random_su2(rng) for _ in range(4 * 8**4)]).reshape((4,) + (8,) * 4 + (4,))
    links = py.metropolis(links, 2.0, rng, 40)
    sigma = py.creutz_ratio(links, 2, 2)
    ratio = ms[1] / np.sqrt(sigma)

    print(f"fit: m(β) = {A:.2f}·e^(−{c:.3f}β)   (referee: 25.28·e^(−1.182β), ±15% noise)")
    print(f"m/√σ = {ratio:.2f}   (referee: ≈3.2, ±10% noise)")

    # the ratio m/√σ is the robust referee; the scaling-law coefficients (A, c) carry ~15% MC noise
    ok_ratio = abs(ratio - 3.2) < 0.32
    ok_A = abs(A - 25.28) < 4.0
    ok_c = abs(c - 1.182) < 0.2
    ok = ok_ratio and ok_A and ok_c
    print("REFEREE:", "PASS" if ok else "FAIL",
          f"(ratio {'OK' if ok_ratio else 'off'}, A {'OK' if ok_A else 'off'}, c {'OK' if ok_c else 'off'})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
