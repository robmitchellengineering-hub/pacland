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
        C, m_eff, _ = nb.measure_glueball(beta, 4, 8, 30, 3000, 0)
        ms.append(m_eff[0])
    ms = np.array(ms)
    betas_np = np.array(betas)

    # fit m(β) = A·e^(−c′β)
    def af(b, A, c):
        return A * np.exp(-c * b)
    popt, _ = curve_fit(af, betas_np, ms, p0=[25, 1.1], maxfev=10000)
    A, c = popt

    # the ratio m/√σ at the clean couplings
    sigma = py.measure_string_tension(2.0, d=4, N=8, n_sweeps=3, seed=0)
    ratio = ms[1] / np.sqrt(sigma)

    print(f"fit: m(β) = {A:.2f}·e^(−{c:.3f}β)   (referee: 25.28·e^(−1.182β))")
    print(f"m/√σ = {ratio:.2f}   (referee: ≈3.2)")

    ok = abs(A - 25.28) < 2.0 and abs(c - 1.182) < 0.05 and abs(ratio - 3.2) < 0.5
    print("REFEREE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
