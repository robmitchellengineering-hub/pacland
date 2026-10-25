#!/usr/bin/env python3
"""Proof arm for the New Keynesian 3-equation model — exact, zero tolerance.

Mirrors ``scripts/validate_constraint_first.py`` / ``validate_t6_sympy.py``: the claims
in ``src/pacland/economics/nk3.py`` are not cited, they are *derived* here in sympy and
the residuals are asserted to be exactly zero. The determinacy boundary is then checked
against the module's own eigenvalue search, so the analytic and numeric arms have to
agree — the Rule of Three, applied to a stability condition.

Run:  PYTHONPATH=src python3 scripts/validate_economics_nk3.py
Exit: 0 when every proof passes, 1 otherwise.
"""
from __future__ import annotations

import sys

import sympy as sp

from pacland.economics import nk3

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<58} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    b, k, s, r_star, pi_s, phi_pi, phi_y = sp.symbols(
        "beta kappa sigma r_star pi_star phi_pi phi_y", positive=True
    )
    x, pi, i = sp.symbols("x pi i", real=True)

    # --- P1: the steady-state family of the NKPC --------------------------------
    # pi = beta*pi + kappa*x   =>   x = (1-beta)/kappa * pi
    x_of_pi = sp.solve(sp.Eq(pi, b * pi + k * x), x)[0]
    p1 = sp.simplify(x_of_pi - (1 - b) / k * pi) == 0
    check("P1  NKPC steady state: x = (1-beta)/kappa*pi", "exact", p1)

    # --- P2: the model has no consistent steady state at pi* != 0 ---------------
    # IS at the steady state: x = x - sigma*(i - pi - r*)  =>  i = r* + pi  (Fisher)
    i_fisher = sp.solve(sp.Eq(x, x - s * (i - pi - r_star)), i)[0]
    # Taylor at the same point, with the gap the NKPC implies:
    i_taylor = r_star + pi_s + phi_pi * (pi - pi_s) + phi_y * x_of_pi
    # Consistency requires the two nominal rates to agree; evaluate at pi = pi*
    resid = sp.simplify((i_taylor - i_fisher).subs(pi, pi_s))
    p2 = sp.simplify(resid - phi_y * (1 - b) / k * pi_s) == 0
    check(
        "P2  Taylor-vs-NKPC inconsistency at pi* != 0",
        f"residual = +phi_y*(1-beta)/kappa*pi* = {resid}",
        p2,
    )
    # ...and it vanishes exactly at pi* = 0, which is the model's only admissible point
    p2b = sp.simplify(resid.subs(pi_s, 0)) == 0
    check("P2b that residual vanishes exactly at pi* = 0", "0 at the origin", p2b)

    # --- P3: Fisher is exact ----------------------------------------------------
    p3 = sp.simplify((i_fisher - (r_star + pi))) == 0
    check("P3  Fisher at the steady state: i = r* + pi", "exact", p3)

    # --- P4: superneutrality (a nominal shift cannot move the real rate) -------
    real_rate = i_fisher - pi
    p4 = sp.simplify(sp.diff(real_rate, pi)) == 0
    check("P4  superneutrality: d(i-pi)/dpi = 0", "exact", p4)

    # --- P5: the long-run Phillips slope ---------------------------------------
    slope = sp.simplify(sp.diff(x_of_pi, pi))
    p5 = sp.simplify(slope - (1 - b) / k) == 0
    check("P5  long-run Phillips: dx/dpi = (1-beta)/kappa", f"slope = {slope}", p5)
    # vertical only at beta = 1 — the claim that is refused at beta < 1
    p5b = sp.simplify(slope.subs(b, 1)) == 0
    check("P5b the LRPC is vertical only at beta = 1", "0 at beta=1", p5b)

    # --- P6: the determinacy boundary, analytic vs measured --------------------
    # Analytic: phi_pi > 1 - (1-beta)/kappa*phi_y. Measured: locate the boundary with
    # the module's eigen-search and require agreement, for several calibrations,
    # including sigma changes (the boundary must be sigma-free).
    cases = [
        (0.99, 0.10, 1.0, 0.0),
        (0.99, 0.10, 1.0, 0.5),
        (0.99, 0.10, 4.0, 0.5),   # sigma change must not move the boundary
        (0.99, 0.05, 1.0, 0.5),
        (0.90, 0.30, 2.0, 0.5),
        (0.50, 0.20, 1.0, 0.25),
    ]
    worst = 0.0
    for beta, kappa, sigma, phi_y in cases:
        lo, hi = 0.0, 6.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if nk3.determinacy_margin(mid, phi_y, beta, sigma, kappa) > 0.0:
                hi = mid
            else:
                lo = mid
        analytic = float(sp.N(1 - (1 - beta) / kappa * phi_y))
        worst = max(worst, abs(hi - analytic))
    p6 = worst < 1e-9
    check(
        "P6  determinacy boundary = 1-(1-beta)/kappa*phi_y",
        f"6 calibrations, worst |measured-analytic| = {worst:.2e}",
        p6,
    )

    print()
    total = 8
    passed = total - FAIL
    print(f"NK3 exact structure: {passed}/{total} exact — "
          f"{'all proofs hold' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
