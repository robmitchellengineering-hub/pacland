"""CMIP6 conservation drift — the climate discipline's Rule of Three (real data).

A conserving model must close THREE independent ledgers in its pre-industrial
control (the climate-specific oracle: no forcing => zero drift):

  energy  — net top-of-atmosphere drift (netTOA) ~ 0
  mass    — ocean-mass drift (masso) ~ 0
  salt    — salinity drift (soga) ~ 0  (salt has no sources or sinks)

The three ledgers are the climate Rule of Three: independent physics, and a
model must pass all three. The drift data (Irving et al. 2021,
figshare doi:10.6084/m9.figshare.12143562) measures the violation of the oracle.

Pure stdlib + ``pacland.climate.guards``.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from .guards import guard_energy_budget, guard_ocean_mass, guard_ocean_salt

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
                  tol_mm_per_yr: float = 0.3,
                  tol_salt_g_per_kg_per_yr: float = 1e-5) -> list[dict]:
    """Per-model three-ledger verdict (energy + mass + salt).

    ``n_failed_ledgers`` is the number of the three ledgers the model violates;
    0 means the model conserves all three.
    """
    d = data if data is not None else load()
    eei = d["earth_energy_imbalance_wm2"]
    kg_per_mm = d.get("kg_per_mm_sl", 3.6e14)
    rows = []
    for m in d["models"]:
        nettoa = drift_wm2(m["netTOA_J_per_yr"])
        eok, _ = guard_energy_budget(nettoa, 0.0, tol=tol_wm2)
        row = {
            "model": m["model"],
            "institution": m["institution"],
            "netTOA_drift_wm2": round(nettoa, 3),
            "energy_pass": eok,
            "exceeds_eei": abs(nettoa) > eei,
        }
        if "OHC_J_per_yr" in m:
            ohc = drift_wm2(m["OHC_J_per_yr"])
            row["ocean_drift_wm2"] = round(ohc, 3)
            row["non_ocean_leak_wm2"] = round(nettoa - ohc, 3)
        mok = True
        if "masso_kg_per_yr" in m:
            mm = mass_drift_mm_per_yr(m["masso_kg_per_yr"], kg_per_mm)
            mok, _ = guard_ocean_mass(mm, tol_mm_per_yr)
            row["mass_drift_mm_per_yr"] = round(mm, 3)
            row["mass_pass"] = mok
        sok = True
        if "soga_g_per_kg_per_yr" in m:
            sg = m["soga_g_per_kg_per_yr"]
            sok, _ = guard_ocean_salt(sg, tol_salt_g_per_kg_per_yr)
            row["salt_drift_g_per_kg_per_yr"] = sg
            row["salt_pass"] = sok
        row["n_failed_ledgers"] = (0 if eok else 1) + (0 if mok else 1) + (0 if sok else 1)
        rows.append(row)
    rows.sort(key=lambda r: (-r["n_failed_ledgers"], -abs(r["netTOA_drift_wm2"])))
    return rows


def trust_ranking(data: dict | None = None, tol_wm2: float = 0.1) -> dict:
    """Tier the models by how many of the three ledgers they violate."""
    tiers: dict[str, list[str]] = {"broken": [], "leaking": [], "clean": []}
    for r in verdict_table(data, tol_wm2):
        if r["n_failed_ledgers"] >= 2:
            tiers["broken"].append(r["model"])
        elif r["n_failed_ledgers"] == 1:
            tiers["leaking"].append(r["model"])
        else:
            tiers["clean"].append(r["model"])
    return tiers


def summary(data: dict | None = None, tol_wm2: float = 0.1,
            tol_mm_per_yr: float = 0.3,
            tol_salt_g_per_kg_per_yr: float = 1e-5) -> dict:
    d = data if data is not None else load()
    rows = verdict_table(d, tol_wm2, tol_mm_per_yr, tol_salt_g_per_kg_per_yr)
    eei = d["earth_energy_imbalance_wm2"]
    slr = d.get("sea_level_rise_reference_mm_per_yr", 3.4)
    n = len(rows)
    n_energy = sum(1 for r in rows if not r["energy_pass"])
    n_mass = sum(1 for r in rows if "mass_pass" in r and not r["mass_pass"])
    n_salt = sum(1 for r in rows if "salt_pass" in r and not r["salt_pass"])
    n_exceed = sum(1 for r in rows if r["exceeds_eei"])
    n_clean = sum(1 for r in rows if r["n_failed_ledgers"] == 0)
    worst_overall = rows[0]
    worst_energy = max(rows, key=lambda r: abs(r["netTOA_drift_wm2"]))
    with_ohc = [r for r in rows if "ocean_drift_wm2" in r]
    med_toa = statistics.median(abs(r["netTOA_drift_wm2"]) for r in rows)
    med_ohc = statistics.median(abs(r["ocean_drift_wm2"]) for r in with_ohc)
    with_mass = [r for r in rows if "mass_drift_mm_per_yr" in r]
    worst_mass = max(with_mass, key=lambda r: abs(r["mass_drift_mm_per_yr"]))
    with_salt = [r for r in rows if "salt_drift_g_per_kg_per_yr" in r]
    worst_salt = max(with_salt, key=lambda r: abs(r["salt_drift_g_per_kg_per_yr"]))
    tiers = trust_ranking(d, tol_wm2)
    return {
        "n_models": n,
        "n_failing_energy": n_energy,
        "n_failing_mass": n_mass,
        "n_failing_salt": n_salt,
        "n_exceeding_eei": n_exceed,
        "n_conserving_all": n_clean,
        "tol_wm2": tol_wm2,
        "tol_mm_per_yr": tol_mm_per_yr,
        "tol_salt_g_per_kg_per_yr": tol_salt_g_per_kg_per_yr,
        "eei_wm2": eei,
        "slr_reference_mm_per_yr": slr,
        "worst_overall_model": worst_overall["model"],
        "worst_overall_ledgers_failed": worst_overall["n_failed_ledgers"],
        "worst_energy_model": worst_energy["model"],
        "worst_drift_wm2": worst_energy["netTOA_drift_wm2"],
        "worst_ratio_to_eei": round(worst_energy["netTOA_drift_wm2"] / eei, 2),
        "worst_mass_model": worst_mass["model"],
        "worst_mass_mm_per_yr": worst_mass["mass_drift_mm_per_yr"],
        "worst_salt_model": worst_salt["model"],
        "worst_salt_g_per_kg_per_yr": worst_salt["salt_drift_g_per_kg_per_yr"],
        "median_abs_nettoa_wm2": round(med_toa, 3),
        "median_abs_ocean_wm2": round(med_ohc, 3),
        "trust_ranking": tiers,
        "verdict": (
            f"{n_energy}/{n} leak energy, {n_mass}/{n} leak mass, {n_salt}/{n} leak salt. "
            f"Salt — the purely-ocean ledger — is conserved orders of magnitude better "
            f"than energy and mass, which cross the air-sea boundary. So the leak is in "
            f"the atmosphere-ocean coupling, not the ocean model: {n_clean} of {n} models "
            f"conserve all three ledgers."
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
        tier = "broken" if r["n_failed_ledgers"] >= 2 else ("weak" if r["n_failed_ledgers"] == 1 else "clean")
        detail = (f"{r['n_failed_ledgers']} of 3 ledgers fail — "
                  f"energy leak {r['netTOA_drift_wm2']:+.3f} W/m2 ({a / eei:.2f}x EEI)")
        if "mass_drift_mm_per_yr" in r:
            detail += f", mass {r['mass_drift_mm_per_yr']:+.2f} mm/yr"
        if "salt_drift_g_per_kg_per_yr" in r:
            detail += f", salt {r['salt_drift_g_per_kg_per_yr']:+.1e} g/kg/yr"
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
