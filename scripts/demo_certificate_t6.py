"""Run the two-level Valiant certificate on the exact T^6 oracle (build #2 -> #3 seam).

Demonstrates what an *exact* verifier buys: the oracle term collapses from an
error (``p_hat_e + radius``) to a pure confidence interval (``radius``), and the
whole thing is vacuous at m = 0 and finite the moment one rung is validated.

Run:  python3 scripts/demo_certificate_t6.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.certificate import hoeffding_radius, two_level_certificate  # noqa: E402
from pacland.oracle.exact_t6 import T6Background, exact_t6_oracle  # noqa: E402


def main():
    # A candidate "model" predicts log_gs with a small additive bias; the T^6 oracle
    # computes the exact value. p_hat_g = disagreement rate over N candidates.
    rng = np.random.default_rng(3)
    N = 200
    eps = 0.05
    bias = 0.02  # a good candidate: bias < eps, so it mostly agrees

    p_hat_g = 0.0
    for _ in range(N):
        F = tuple(int(x) for x in rng.integers(-3, 4, 8))
        H = tuple(int(x) for x in rng.integers(-3, 4, 8))
        tau0 = 0.3 + (1.5 + rng.random()) * 1j
        oracle = exact_t6_oracle(T6Background(F, H, tau0))["log_gs"]
        if abs((oracle + bias) - oracle) > eps:
            p_hat_g += 1.0
    p_hat_g /= N

    delta_s = delta_e = 0.025
    print(f"candidate-vs-oracle disagreement  p_hat_g = {p_hat_g:.3f}  (N={N}, eps={eps})")

    # The exact T^6 oracle: its closed form IS ground truth, so p_hat_e = 0.
    print("oracle-vs-truth exceedance       p_hat_e = 0.000  (exact verifier)")

    print("\n--- m = 0: no validated rungs -> VACUOUS ---")
    try:
        hoeffding_radius(0, delta_e)
    except ValueError:
        print("  oracle radius = INFINITE  (certificate says nothing)")

    print("\n--- m = 4: four T^6 rungs validated -> FINITE ---")
    m = 4
    cert = two_level_certificate(p_hat_g, N, 0.0, m, delta_s, delta_e)
    print(f"  exact oracle:   bound = {cert.bound:.3f}  "
          f"(= p_hat_g {cert.p_hat_g:.3f} + 0 + radius_s {cert.radius_s:.3f} + radius_e {cert.radius_e:.3f})")

    # Contrast: an approximate oracle with 20% exceedance pays p_hat_e on top.
    approx = two_level_certificate(p_hat_g, N, 0.2, m, delta_s, delta_e)
    print(f"  approx oracle:  bound = {approx.bound:.3f}  "
          f"(same, but + p_hat_e 0.200)")

    print(f"\n  exact oracle term shrinks with m:  m=4 -> {hoeffding_radius(4, delta_e):.3f}, "
          f"m=16 -> {hoeffding_radius(16, delta_e):.3f}, m=64 -> {hoeffding_radius(64, delta_e):.3f}")
    print("  -> an exact verifier turns the deficit m into a shrinking confidence")
    print("     interval; an approximate one pays its error on top, forever.")


if __name__ == "__main__":
    main()
