#!/usr/bin/env python3
"""Verify SW's linearised model against the authors' own Dynare file.

Fetches the GPL Dynare implementation (never committed), parses the linearised system,
and checks that every equilibrium condition vanishes at the steady state while every
measurement equation carries its constant. Then compares the implied steady-state rates
with the paper's own prose ("about 3%" real, "about 6%" nominal) and with this repo's
independent derivation.

Run:  PYTHONPATH=src python3 scripts/verify_sw_mod.py
Out:  data/economics/sw_mod.json  (fixture for the offline tests)
Exit: 0 when the checks pass.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import urllib.request

from pacland.economics import sw2007, sw_linear

URL = ("https://raw.githubusercontent.com/rui-q/DSGE_mod/master/"
       "Smets_Wouters_2007/Smets_Wouters_2007.mod")
OUT = pathlib.Path("data/economics/sw_mod.json")
FAIL = 0


def check(name: str, detail: str, ok: bool) -> None:
    global FAIL
    FAIL += 0 if ok else 1
    print(f"{name:<56} {'PASS' if ok else 'FAIL'}  {detail}")


def main() -> int:
    global FAIL
    with urllib.request.urlopen(URL, timeout=40) as r:
        text = r.read().decode()
    digest = hashlib.sha256(text.encode()).hexdigest()
    p = sw_linear.parse(text)
    res = sw_linear.check(p)
    rates = sw_linear.steady_state_rates(p)

    print("SW LINEARISED MODEL — the authors' own Dynare file, machine-checked")
    print("=" * 72)
    print(f"source  {URL}")
    print(f"sha256  {digest}")
    print()
    check("L1  the model block parses into statements",
          f"{res['n_equations']} equations = {res['n_equilibrium']} equilibrium "
          f"+ {res['n_measurement']} measurement", res["n_equations"] >= 30)
    check("L2  every equilibrium condition vanishes at the steady state",
          f"{res['n_equilibrium'] - len(res['equilibrium_bad'])}/{res['n_equilibrium']}",
          not res["equilibrium_bad"])
    check("L3  every measurement equation carries its constant",
          f"{res['n_measurement']} of {res['n_measurement']}",
          not res["measurement_without_constant"])
    check("L4  the implied real rate matches the paper's 'about 3%'",
          f"{rates['real_annual_pct']:.2f}%/yr vs 3.0",
          abs(rates["real_annual_pct"] - 3.0) <= 0.6)
    check("L5  the implied nominal rate matches the paper's 'about 6%'",
          f"{rates['nominal_annual_pct']:.2f}%/yr vs 6.0",
          abs(rates["nominal_annual_pct"] - 6.0) <= 0.6)
    check("L6  it agrees with this repo's independent derivation",
          f"model {rates['nominal_annual_pct']:.2f} vs sw2007 "
          f"{sw2007.nominal_rate_annual_pct():.2f} %/yr",
          abs(rates["nominal_annual_pct"] - sw2007.nominal_rate_annual_pct()) < 0.05)
    check("L7  the expenditure shares sum to one",
          f"c/y {rates['consumption_share']:.4f} + i/y {rates['investment_share']:.4f} "
          f"+ g/y 0.18 = {rates['shares_sum']:.4f}",
          abs(rates["shares_sum"] - 1.0) < 1e-9)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "source": URL, "sha256": digest,
        "n_equations": res["n_equations"], "n_equilibrium": res["n_equilibrium"],
        "n_measurement": res["n_measurement"],
        "equilibrium_bad": [e for e, _ in res["equilibrium_bad"]],
        "rates": rates, "fetched": "2026-10-26",
    }, indent=1, sort_keys=True))
    print()
    total = 7
    print(f"sw linear: {total - FAIL}/{total} — "
          f"{'the linearised system checks out' if FAIL == 0 else 'FAILURES ABOVE'}")
    print(f"fixture written to {OUT}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
