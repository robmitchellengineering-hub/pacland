#!/usr/bin/env python3
"""Reproduce the estimation result.

Run:  PYTHONPATH=src python3 scripts/economics_estimate.py
Exit: 0 when the rule is identified, the slope is shown not to be, and the
      constraint set refuses the fitted rule.
"""
from __future__ import annotations

import sys

from pacland.economics import estimate as E

FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<58} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    print(E.summary())
    print("-" * 62)

    fit = E.fit_rule()
    check("E1  the rule is identified from real data",
          f"phi_pi={fit['phi_pi']:.3f} (SE {fit['se']['phi_pi']:.3f}), n={fit['n']}",
          fit["n"] > 200 and fit["se"]["phi_pi"] > 0)

    check("E2  ...and it is passive (phi_pi < 1)",
          f"phi_pi={fit['phi_pi']:.3f} < 1", fit["phi_pi"] < 1.0)

    rec = E.kappa_recovery()
    check("E3  kappa is NOT recoverable from clean synthetic data",
          f"truth {rec['truth']} -> {rec['recovered']:.3f}", not rec["recovered_ok"])

    full = next(p for p in E.probe() if len(p["free"]) == 4)
    check("E4  the four-parameter fit is rank-deficient",
          f"rank {full['rank']}/4", not full["identified"])

    cal = {"beta": E.FIXED["beta"], "kappa": E.sw2007.calvo_kappa(),
           "sigma": E.FIXED["sigma"], "phi_pi": fit["phi_pi"], "phi_y": fit["phi_y"]}
    check("E5  the constraint set refuses the fitted rule",
          ", ".join(E.admissibility(cal)), "taylor_principle" in E.admissibility(cal))

    refused = False
    try:
        E.estimated_calibration()
    except E.InadmissibleFit:
        refused = True
    check("E6  so no forecast calibration is handed out", "InadmissibleFit", refused)

    print()
    total = 6
    print(f"estimation: {total - FAIL}/{total} — "
          f"{'the data identifies the rule and refuses the model' if FAIL == 0 else 'FAILURES ABOVE'}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
