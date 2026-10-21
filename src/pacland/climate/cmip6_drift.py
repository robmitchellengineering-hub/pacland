"""CMIP6 conservation-drift guard — per-model energy leakage (real data).

Runs ``guard_energy_budget`` on the real per-model net-TOA drift measured by
Irving et al. 2021 (figshare doi:10.6084/m9.figshare.12143562). Adds the sharp
split: the total TOA leak vs the ocean's own drift — which shows the leak lives
in the atmosphere, not the ocean. Also emits a conservation "trust ranking".

Pure stdlib + ``pacland.climate.guards``. Data: ``data/climate/cmip6_drift.json``.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from .guards import guard_energy_budget

_DATA = Path(__file__).resolve().parents[3] / "data" / "climate" / "cmip6_drift.json"
_SEC_PER_YEAR = 365.25 * 86400.0
_EARTH_AREA_M2 = 5.101e14


def load() -> dict:
    return json.loads(_DATA.read_text())


def drift_wm2(j_per_yr: float) -> float:
    """Convert a J/yr drift to a global-mean W/m2 rate."""
    return j_per_yr / _SEC_PER_YEAR / _EARTH_AREA_M2


def verdict_table(data: dict | None = None, tol_wm2: float = 0.1) -> list[dict]:
    """Per-model verdict: does the model conserve energy (net TOA ~ 0)?

    Also reports the ocean's own drift and the *non-ocean* leak
    (net TOA minus ocean) — the atmosphere/land/cryosphere part.
    """
    d = data if data is not None else load()
    eei = d["earth_energy_imbalance_wm2"]
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
        rows.append(row)
    rows.sort(key=lambda r: -abs(r["netTOA_drift_wm2"]))
    return rows


def trust_ranking(data: dict | None = None, tol_wm2: float = 0.1) -> dict:
    """Tier the models by conservation: broken (leak > EEI), leaking, clean."""
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


def summary(data: dict | None = None, tol_wm2: float = 0.1) -> dict:
    d = data if data is not None else load()
    rows = verdict_table(d, tol_wm2)
    eei = d["earth_energy_imbalance_wm2"]
    n = len(rows)
    n_fail = sum(1 for r in rows if not r["pass"])
    n_exceed = sum(1 for r in rows if r["exceeds_eei"])
    worst = rows[0]
    with_ohc = [r for r in rows if "ocean_drift_wm2" in r]
    med_toa = statistics.median(abs(r["netTOA_drift_wm2"]) for r in rows)
    med_ohc = statistics.median(abs(r["ocean_drift_wm2"]) for r in with_ohc)
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
        "trust_ranking": tiers,
        "verdict": (
            f"{n_fail} of {n} CMIP6 models leak energy beyond {tol_wm2} W/m2; "
            f"{n_exceed} leak faster than the EEI ({eei} W/m2). "
            f"The leak lives in the atmosphere: median total TOA drift is {med_toa:.3f} W/m2 "
            f"vs {med_ohc:.3f} W/m2 in the ocean."
        ),
    }


__all__ = ["load", "drift_wm2", "verdict_table", "trust_ranking", "summary"]
