#!/usr/bin/env python3
"""Proof arm for the Smets–Wouters (2007) record — provenance, not recollection.

The workhorse's parameters are *published*; the risk here is not algebra, it is
transcription. So this script re-derives, from the recorded posterior means, the three
quantities the paper reports only in prose (about 3% real, about 6% nominal, about 3%
inflation, annualised), and the quantities it reports as formulas. If a digit were
copied wrong, a check here breaks.

Run:  PYTHONPATH=src python3 scripts/validate_economics_sw.py
Exit: 0 when every check passes, 1 otherwise.
"""
from __future__ import annotations

import sys

import sympy as sp

from pacland.economics import nk3, sw2007

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    tau, sig_c, xi_p = sp.symbols("tau sigma_c xi_p", positive=True)
    g = sp.symbols("gamma", positive=True)

    # --- S1: beta from the reported 100(1/beta-1) -----------------------------
    beta_sym = 1 / (1 + tau / 100)
    s1 = sp.simplify(beta_sym.subs(tau, 0.16) - sw2007.beta()) == 0
    check("S1  beta = 1/(1 + tau/100), tau = 0.16 %/q",
          f"beta = {sw2007.beta():.8f}", s1)

    # --- S2: the detrending relation ------------------------------------------
    bt_sym = beta_sym * g ** (-sig_c)
    s2 = sp.simplify(bt_sym.subs({tau: 0.16, g: 1.0043, sig_c: 1.38}) - sw2007.beta_tilde()) == 0
    check("S2  beta_tilde = beta * gamma**(-sigma_c)", f"{sw2007.beta_tilde():.8f}", s2)

    # --- S3..S5: the three prose statements the paper makes -------------------
    real = sw2007.real_rate_annual_pct()
    nom = sw2007.nominal_rate_annual_pct()
    infl = sw2007.inflation_annual_pct()
    ok3, msg3 = sw2007.guard_provenance_consistency()
    check("S3  implied real rate matches 'about 3%'", f"{real:.2f}% vs 3%", abs(real - 3.0) <= 0.5)
    check("S4  implied nominal rate matches 'about 6%'", f"{nom:.2f}% vs 6%", abs(nom - 6.0) <= 0.5)
    check("S5  steady-state inflation matches 'about 3%'", f"{infl:.2f}% vs 3%", abs(infl - 3.0) <= 0.5)
    check("S5b the provenance guard agrees", msg3, ok3)

    # Fisher must hold as an identity, not approximately: nominal = real + inflation
    fisher_ok = abs(nom - (real + infl)) <= 1e-9
    check("S6  Fisher as an identity: nominal = real + inflation",
          f"{nom:.6f} = {real:.6f} + {infl:.6f}", fisher_ok)

    # --- S7: the Calvo slope, its limits, and the published value -------------
    kappa_sym = (1 - xi_p) * (1 - bt_sym * xi_p) / xi_p
    s7a = bool(sp.simplify(sp.limit(kappa_sym, xi_p, 1)) == 0)   # no rigidity -> no slope
    s7b = abs(float(kappa_sym.subs({tau: 0.16, g: 1.0043, sig_c: 1.38, xi_p: 0.66}))
              - sw2007.calvo_kappa()) < 1e-12
    check("S7  Calvo kappa = (1-xi)(1-beta_tilde*xi)/xi, -> 0 as xi -> 1",
          f"kappa(xi=0.66) = {sw2007.calvo_kappa():.6f} (limit={s7a}, value={s7b})",
          bool(s7a) and bool(s7b))

    # --- S8: the Taylor boundary, analytic vs the module's eigen-search -------
    worst = 0.0
    for r_y in (0.0, 0.08, 0.22):
        lo, hi = 0.0, 6.0
        for _ in range(160):
            mid = 0.5 * (lo + hi)
            if nk3.determinacy_margin(mid, r_y, sw2007.beta_tilde(), nk3.SIGMA,
                                      sw2007.calvo_kappa()) > 0:
                hi = mid
            else:
                lo = mid
        worst = max(worst, abs(hi - nk3.taylor_boundary(r_y, sw2007.beta_tilde(),
                                                        sw2007.calvo_kappa())))
    check("S8  Taylor boundary reproduced by eigen-search (r_y = 0, .08, .22)",
          f"worst |measured-analytic| = {worst:.2e}", worst < 1e-9)

    # --- S9: the published rule is determinate --------------------------------
    d = sw2007.determinacy()
    ok9, msg9 = sw2007.guard_determinacy()
    check("S9  published rule r_pi=2.04 lies above the boundary",
          f"boundary {d['boundary']:.4f}, margin {d['margin']:+.4f}", ok9)

    # --- S10: the record of Table 3 ------------------------------------------
    rec = sw2007.out_of_sample_vs_random_walk()
    check("S10 Table 3 benchmarks a VAR(1), with NO no-change null",
          f"benchmark={rec['benchmark']}, dsge ahead at every horizon="
          f"{rec['dsge_beats_var1_at_every_horizon']}",
          rec["benchmark"] == "VAR(1)" and rec["random_walk_present"] is False)

    print()
    total = 11
    print(f"SW record: {total - FAIL}/{total} checks — "
          f"{'the record is faithful to the source' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
