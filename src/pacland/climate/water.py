"""Water — the fifth conservation invariant, measured with free data.

`structure.py` named five conservation laws; four were measured (energy, ocean mass, salinity,
carbon) and water was the last one outstanding. It was held up by a dependency: the obvious
products are netCDF behind OPeNDAP, or reanalysis behind an API key.

Neither is needed. NOAA/PSL serves both fields through **OPeNDAP's ASCII interface**, which is
plain text over HTTPS: GPCP v2.3 for precipitation, NCEP/NCAR latent heat flux for evaporation.
No credential, no library, no netCDF. `scripts/fetch_water_budget.py` samples five Januarys
across four decades, area-weights by cos(latitude), and stores the result.

The invariant: over a long enough period the global hydrological cycle balances —

    precipitation = evaporation + d(storage)/dt

and the storage term is negligible at annual scale, so **P must equal E**. Measured:

    P  2.84 - 3.10 mm/day      (GPCP, five Januarys)
    E  2.67 - 2.94 mm/day      (NCEP latent heat flux, same months)

The two agree to within a few percent, which is what the published global water budget gives.

Two guards, both about the *measurement* rather than the physics:

  weighting   an unweighted grid mean is 2.46-2.60 mm/day against 2.84-3.10 weighted: the poles
              are over-counted, and the "disagreement" would be an artefact of the averaging
  units       leave evaporation in W/m2 and the balance breaks by a factor of ~85 — the trap
              that a units-guard exists to catch before it reaches a report

Run:        python3 scripts/climate_water.py
Guarded by: tests/test_climate_water.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "climate" / "water.json"

#: How far P and E may diverge before the balance is declared broken. One observation product
#: against one reanalysis: the published disagreement is a few percent, so 10% is generous
#: enough to be a real test and tight enough to catch a unit or weighting error (which are
#: 15-30% and 85x respectively).
TOLERANCE = 0.10


def load() -> dict:
    return json.loads(DATA.read_text())


def balance() -> dict:
    samples = load()["samples"]
    ratios = {k: v["precip_mm_day"] / v["evap_mm_day"] for k, v in samples.items()}
    worst = max(abs(r - 1.0) for r in ratios.values())
    mean_p = sum(v["precip_mm_day"] for v in samples.values()) / len(samples)
    mean_e = sum(v["evap_mm_day"] for v in samples.values()) / len(samples)
    return {"n": len(samples), "mean_precip_mm_day": mean_p, "mean_evap_mm_day": mean_e,
            "ratios": ratios, "worst_imbalance": worst,
            "closes": worst < TOLERANCE,
            "verdict": (f"water closes: P/E within {worst:.1%} in every sampled month"
                        if worst < TOLERANCE else
                        f"water does NOT close: worst P/E imbalance {worst:.1%}")}


def guard_weighting() -> tuple[bool, str]:
    """MUTATION: drop the area weighting and the global mean must move by a visible margin —
    otherwise the weighting guard is not measuring anything and a weighting bug would pass."""
    samples = load()["samples"]
    weighted = [v["precip_mm_day"] for v in samples.values()]
    unweighted = [v["precip_unweighted_mm_day"] for v in samples.values()]
    drift = min(abs(u - w) / w for u, w in zip(unweighted, weighted))
    r = balance()
    ok = r["closes"] and drift > 0.05
    return ok, (f"weighting: unweighted means sit {drift:.1%}-"
                f"{max(abs(u - w) / w for u, w in zip(unweighted, weighted)):.1%} below the "
                f"area-weighted ones (detected = {drift > 0.05})")


def guard_units() -> tuple[bool, str]:
    """MUTATION: treat the latent flux as if it were already in mm/day and the ratio collapses
    by a factor of ~85. The guard exists to catch exactly that before it is reported."""
    samples = load()["samples"]
    # forgetting W/m2 -> mm/day leaves the flux ~29x too large, so the balance reads ~0.04
    wrong = {k: v["precip_mm_day"] / v["latent_flux_wm2"] for k, v in samples.items()}
    factor = list(samples.values())[0]["latent_flux_wm2"] / list(samples.values())[0]["evap_mm_day"]
    absurd = max(abs(w) for w in wrong.values()) < 0.5 and factor > 5.0
    r = balance()
    ok = r["closes"] and absurd
    return ok, (f"units: precip over raw flux reads {list(wrong.values())[0]:.3f} instead of "
                f"~1.0 — off by {factor:.0f}x from the missing conversion (detected = {absurd})")


def invariant() -> dict:
    r = balance()
    return {"name": "water", "measured": True, "closes": bool(r["closes"]),
            "value": r["mean_precip_mm_day"] / r["mean_evap_mm_day"],
            "tolerance": TOLERANCE,
            "detail": (f"P {r['mean_precip_mm_day']:.2f} vs E {r['mean_evap_mm_day']:.2f} "
                       f"mm/day over {r['n']} sampled months")}


def audit() -> dict:
    checks = []
    for name, run in (("closure", lambda: (balance()["closes"], balance()["verdict"])),
                      ("weighting", guard_weighting),
                      ("units", guard_units)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["load", "balance", "invariant", "guard_weighting", "guard_units", "audit",
           "TOLERANCE"]
