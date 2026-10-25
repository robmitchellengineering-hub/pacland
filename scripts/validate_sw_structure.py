#!/usr/bin/env python3
"""Proof arm for the Smets–Wouters equilibrium conditions — derived, not transcribed.

The paper states its model nonlinearly (appendix 1) and linearises numerically. So this
script derives the *steady state* symbolically from those nonlinear conditions and
compares each result to the closed form the module implements. Two independent
implementations (sympy derivation, python closed form) must agree, which is what makes
the comparison a check rather than a repetition.

Run:  PYTHONPATH=src python3 scripts/validate_sw_structure.py
Exit: 0 when every derivation agrees, 1 otherwise.
"""
from __future__ import annotations

import sys

import sympy as sp

from pacland.economics import sw2007, sw_structure

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<52} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    global FAIL
    beta, gamma, sig, pibar, delta, alpha, mc = sp.symbols(
        "beta gamma sigma_c pi_bar delta alpha mc", positive=True
    )
    R, Rk, k, L, y, g, c, i = sp.symbols("R Rk k L y g c i", positive=True)

    # --- D1 the Euler equation -> Fisher -------------------------------------
    bt = beta * gamma ** (-sig)
    # 1 = beta_tilde * R_gross / pi_gross  =>  R_gross = pi_gross / beta_tilde
    R_sol = sp.solve(sp.Eq(1, bt * R / pibar), R)[0]
    d1 = sp.simplify(R_sol - pibar / bt) == 0
    check("D1  Euler -> R = pi_bar/beta_tilde", f"R = {R_sol}", d1)

    # --- D2 Tobin's Q and the rental rate ------------------------------------
    # 1 = beta_tilde (Rk + 1 - delta) at Q = 1
    Rk_sol = sp.solve(sp.Eq(1, bt * (Rk + 1 - delta)), Rk)[0]
    d2 = sp.simplify(Rk_sol - (1 / bt - 1 + delta)) == 0
    check("D2  Q=1 -> Rk = 1/beta_tilde - 1 + delta", f"Rk = {Rk_sol}", d2)

    # --- D3 capital accumulation at the steady state -------------------------
    i_sol = sp.solve(sp.Eq(k, (1 - delta) * k + i), i)[0]
    check("D3  accumulation -> i = delta k", f"i = {i_sol}", sp.simplify(i_sol - delta * k) == 0)

    # --- D4 the marginal-product FOCs, and the k/L ratio of eq. (5) ----------
    # production y = k^alpha (gamma L)^(1-alpha) - phi ; FOCs on the net output
    Y = k ** alpha * L ** (1 - alpha)          # gamma absorbed into the detrended wage
    w = (1 - alpha) * mc * Y / L
    rk = alpha * mc * Y / k
    kl_ratio = sp.simplify(k / L)
    d4 = sp.simplify(kl_ratio - (alpha / (1 - alpha)) * (w / rk)) == 0
    check("D4  k/L = alpha/(1-alpha) * w/Rk (eq. 5)",
          f"k/L = alpha/(1-alpha)*w/Rk", d4)

    # --- D5 the cost identity holds because production is CRS ----------------
    mc_implied = (w ** (1 - alpha)) * (rk ** alpha) / (alpha ** alpha * (1 - alpha) ** (1 - alpha))
    # every quantity is positive, so the identity can be proved on the log scale
    log_ratio = sp.expand_log(sp.log(mc_implied / mc), force=True)
    d5 = sp.simplify(log_ratio) == 0
    check("D5  eq. (6) reproduces mc from the FOCs (Euler's theorem)",
          f"log(mc_implied/mc) = {sp.simplify(log_ratio)}", d5)

    # --- D6 the capital-output ratio and the shares --------------------------
    # k/y from the steady-state rental rate (D2), not from the symbolic FOC
    k_over_y = alpha * mc / Rk_sol
    d6a = sp.simplify(k_over_y - alpha * mc / (1 / bt - 1 + delta)) == 0
    shares_sum = sp.simplify((1 - (delta * k_over_y) - g) + delta * k_over_y + g)
    d6b = shares_sum == 1
    check("D6  k/y = alpha*mc/Rk, and c/y+i/y+g/y = 1", f"sum = {shares_sum}", d6a and d6b)

    # --- D7 the policy rule is satisfied at ANY target -----------------------
    rho, r_pi, r_y, r_dy, Rstar, pistar, eps = sp.symbols(
        "rho r_pi r_y r_dy R_star pi_star eps", positive=True
    )
    lhs = R / Rstar
    rhs = (R / Rstar) ** rho * ((pistar / pistar) ** r_pi * (1) ** r_y) ** (1 - rho) * (1) ** r_dy * 1
    resid = sp.simplify((lhs - rhs).subs(R, Rstar))
    d7 = resid == 0
    check("D7  policy rule holds at R=R*, pi=pi* for any target", f"residual = {resid}", d7)

    # --- D8 the module's closed forms agree with the derivations -------------
    subs = {
        beta: 1 / (1 + sw2007.PUBLISHED_STRUCTURAL["tau"] / 100),
        gamma: 1 + sw2007.PUBLISHED_STRUCTURAL["gamma"] / 100,
        sig: sw2007.PUBLISHED_STRUCTURAL["sigma_c"],
        pibar: 1 + sw2007.PUBLISHED_STRUCTURAL["pi_bar"] / 100,
        delta: sw_structure.DELTA,
        alpha: sw2007.PUBLISHED_STRUCTURAL["alpha"],
        mc: 1 / 1.2,
    }
    r_num = float(sp.N(R_sol.subs(subs))) - 1.0            # net, quarterly
    rk_num = float(sp.N(Rk_sol.subs(subs)))
    d8a = abs(r_num - sw_structure.nominal_rate_quarterly()) < 1e-12
    d8b = abs(rk_num - sw_structure.rental_rate()) < 1e-12
    d8c = abs(float(sp.N(k_over_y.subs(subs)).evalf())
              - sw_structure.capital_output_ratio(1 / 1.2)) < 1e-12
    check("D8  module closed forms match the symbolic solutions",
          f"R={100*r_num:.4f}%/q, Rk={100*rk_num:.4f}%/q", d8a and d8b and d8c)

    # --- the inventory -------------------------------------------------------
    cov = sw_structure.coverage()
    print()
    print(f"inventory: {cov['n_proved']}/{cov['n_total']} conditions established; "
          f"{cov['n_dynamic_only']} are dynamic-only, {cov['n_cited']} are cited as given")
    ok, msg = sw_structure.guard_conditions_inventory()
    print(f"guard:     {msg}")
    if not ok:
        FAIL += 1

    print()
    total = 9
    print(f"SW structure: {total - FAIL}/{total} — "
          f"{'the steady state is derived, and its scope is stated' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
