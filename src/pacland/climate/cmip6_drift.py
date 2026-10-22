"""CMIP6 conservation-drift guard — per-model energy AND mass leakage (real data).

Runs the conservation guards on the real per-model drift measured by Irving et
al. 2021 (figshare doi:10.6084/m9.figshare.12143562):

  - energy: net top-of-atmosphere drift (netTOA), plus the ocean-vs-atmosphere split;
  - mass:   ocean-mass drift (masso), converted to a sea-level-equivalent rate.

Pure stdlib + ``pacland.climate.guards``. Data: ``data/climate/cmip6_drift.json``.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from .guards import guard_energy_budget, guard_ocean_mass

_DATA = Path(__file__).resolve().parents[3] / "data" / "climate" / "cmip6_drift.json"
_SEC_PER_YEAR = 365.25 * 86400.0
_EARTH_AREA_M2 = 5.101e14


def load() -> dict:
    return json.loads(_DATA.read_text())


def drift_wm2(j_per_yr: float) -> float:
    """Convert a J/yr drift to a global-mean W/m2 rate."""
    return j_per_yr / _SEC_PER_YEAR / _EARTH_AREA_M2


def mass_drift_mm_per_yr(kg_per_yr: float, kg_per_mm: float = 3.6e14) -> float:
    """Convert a kg/yr ocean-mass drift to a sea-level-equivalent mm/yr rate."""
    return kg_per_yr / kg_per_mm


def verdict_table(data: dict | None = None, tol_wm2: float = 0.1,
                  tol_mm_per_yr: float = 0.3) -> list[dict]:
    """Per-model verdict: does the model conserve energy AND mass?

    Reports the energy drift (net TOA), the ocean-vs-atmosphere split, and the
    ocean-mass drift as a sea-level-equivalent rate.
    """
    d = data if data is not None else load()
    eei = d["earth_energy_imbalance_wm2"]
    kg_per_mm = d.get("kg_per_mm_sl", 3.6e14)
    rows = []
    for m in d["models"]:
        nettoa = drift_wm2(m["netTOA_J_per_yr"])
        ok, msg = guard_energy_budget(nettoa, 0.0, tol=tol_wm2)
        row = {
            "model": m["model"],
            "institution": m["institution"],
            "netTOA_drift_wm2": round(nettoa, 3),
            "pass": ok,
            "exceeds_eei": abs(nettoa) > eei,
            "msg": msg,
        }
        if "OHC_J_per_yr" in m:
            ohc = drift_wm2(m["OHC_J_per_yr"])
            row["ocean_drift_wm2"] = round(ohc, 3)
            row["non_ocean_leak_wm2"] = round(nettoa - ohc, 3)
        if "masso_kg_per_yr" in m:
            mm = mass_drift_mm_per_yr(m["masso_kg_per_yr"], kg_per_mm)
            mok, mmsg = guard_ocean_mass(mm, tol_mm_per_yr)
            row["mass_drift_mm_per_yr"] = round(mm, 3)
            row["mass_pass"] = mok
            row["mass_msg"] = mmsg
        rows.append(row)
    rows.sort(key=lambda r: -abs(r["netTOA_drift_wm2"]))
    return rows


def trust_ranking(data: dict | None = None, tol_wm2: float = 0.1) -> dict:
    """Tier the models by energy conservation: broken (leak > EEI), leaking, clean."""
    d = data if data is not None else load()
    eei = d["earth_energy_imbalance_wm2"]
    tiers: dict[str, list[str]] = {"broken": [], "leaking": [], "clean": []}
    for r in verdict_table(d, tol_wm2):
        a = abs(r["netTOA_drift_wm2"])
        if a > eei:
            tiers["broken"].append(r["model"])
        elif a > tol_wm2:
            tiers["leaking"].append(r["model"])
        else:
            tiers["clean"].append(r["model"])
    return tiers


def summary(data: dict | None = None, tol_wm2: float = 0.1,
            tol_mm_per_yr: float = 0.3) -> dict:
    d = data if data is not None else load()
    rows = verdict_table(d, tol_wm2, tol_mm_per_yr)
    eei = d["earth_energy_imbalance_wm2"]
    slr = d.get("sea_level_rise_reference_mm_per_yr", 3.4)
    n = len(rows)
    n_fail = sum(1 for r in rows if not r["pass"])
    n_exceed = sum(1 for r in rows if r["exceeds_eei"])
    worst = rows[0]
    with_ohc = [r for r in rows if "ocean_drift_wm2" in r]
    med_toa = statistics.median(abs(r["netTOA_drift_wm2"]) for r in rows)
    med_ohc = statistics.median(abs(r["ocean_drift_wm2"]) for r in with_ohc)
    with_mass = [r for r in rows if "mass_drift_mm_per_yr" in r]
    n_mass_fail = sum(1 for r in with_mass if not r["mass_pass"])
    worst_mass = max(with_mass, key=lambda r: abs(r["mass_drift_mm_per_yr"]))
    tiers = trust_ranking(d, tol_wm2)
    return {
        "n_models": n,
        "n_failing_conservation": n_fail,
        "n_exceeding_eei": n_exceed,
        "tol_wm2": tol_wm2,
        "eei_wm2": eei,
        "worst_model": worst["model"],
        "worst_drift_wm2": worst["netTOA_drift_wm2"],
        "worst_ratio_to_eei": round(worst["netTOA_drift_wm2"] / eei, 2),
        "median_abs_nettoa_wm2": round(med_toa, 3),
        "median_abs_ocean_wm2": round(med_ohc, 3),
        "n_failing_mass": n_mass_fail,
        "tol_mm_per_yr": tol_mm_per_yr,
        "worst_mass_model": worst_mass["model"],
        "worst_mass_mm_per_yr": worst_mass["mass_drift_mm_per_yr"],
        "worst_mass_ratio_to_slr": round(abs(worst_mass["mass_drift_mm_per_yr"]) / slr, 2),
        "slr_reference_mm_per_yr": slr,
        "trust_ranking": tiers,
        "verdict": (
            f"{n_fail} of {n} CMIP6 models leak energy beyond {tol_wm2} W/m2; "
            f"{n_exceed} leak faster than the EEI ({eei} W/m2). "
            f"The leak lives in the atmosphere: median total TOA drift {med_toa:.3f} W/m2 "
            f"vs {med_ohc:.3f} W/m2 in the ocean. "
            f"{n_mass_fail} also leak ocean mass beyond {tol_mm_per_yr} mm/yr "
            f"(worst {worst_mass['model']} at {worst_mass['mass_drift_mm_per_yr']:+.2f} mm/yr "
            f"= {abs(worst_mass['mass_drift_mm_per_yr'])/slr:.0%} of observed sea-level rise)."
        ),
    }


def trust_entries() -> list:
    """Emit the CMIP6 models as trust-board entries (broken/weak/clean)."""
    from ..trust import TrustEntry

    d = load()
    eei = d["earth_energy_imbalance_wm2"]
    out = []
    for r in verdict_table():
        a = abs(r["netTOA_drift_wm2"])
        if a > eei:
            tier = "broken"
        elif a > 0.1:
            tier = "weak"
        else:
            tier = "clean"
        detail = f"net-TOA energy leak {r['netTOA_drift_wm2']:+.3f} W/m2 ({a / eei:.2f}x EEI)"
        if "mass_drift_mm_per_yr" in r:
            detail += f"; ocean-mass leak {r['mass_drift_mm_per_yr']:+.2f} mm/yr"
        out.append(TrustEntry(
            discipline="climate",
            artifact=f"CMIP6 {r['model']}",
            tier=tier,
            detail=detail,
            evidence="Irving et al. 2021, figshare doi:10.6084/m9.figshare.12143562",
        ))
    return out


__all__ = ["load", "drift_wm2", "mass_drift_mm_per_yr", "verdict_table",
           "trust_ranking", "summary", "trust_entries"]
