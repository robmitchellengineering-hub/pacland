"""CMIP6 conservation-drift guard — per-model energy leakage (real data).

Runs ``guard_energy_budget`` on the real per-model net top-of-atmosphere drift
measured by Irving et al. 2021 (figshare doi:10.6084/m9.figshare.12143562). In a
pre-industrial control run the net TOA flux must be ~0 (energy in = energy out,
steady state); a non-zero drift is a *leak* — energy created or destroyed by
non-conserving physics. The result is a per-model PASS/FAIL table plus the
leak-vs-EEI comparison (the drift rate vs the Earth's own energy imbalance).

Pure stdlib + ``pacland.climate.guards``. Data: ``data/climate/cmip6_drift.json``.
"""
from __future__ import annotations

import json
from pathlib import Path

from .guards import guard_energy_budget

_DATA = Path(__file__).resolve().parents[3] / "data" / "climate" / "cmip6_drift.json"
_SEC_PER_YEAR = 365.25 * 86400.0
_EARTH_AREA_M2 = 5.101e14


def load() -> dict:
    return json.loads(_DATA.read_text())


def drift_wm2(nettoa_J_per_yr: float) -> float:
    """Convert a J/yr drift to a global-mean W/m2 rate."""
    return nettoa_J_per_yr / _SEC_PER_YEAR / _EARTH_AREA_M2


def verdict_table(data: dict | None = None, tol_wm2: float = 0.1) -> list[dict]:
    """Per-model verdict: does the model conserve energy (net TOA ~ 0)?"""
    d = data if data is not None else load()
    eei = d["earth_energy_imbalance_wm2"]
    rows = []
    for m in d["models"]:
        w = drift_wm2(m["netTOA_J_per_yr"])
        ok, msg = guard_energy_budget(w, 0.0, tol=tol_wm2)
        rows.append({
            "model": m["model"],
            "institution": m["institution"],
            "netTOA_drift_wm2": round(w, 3),
            "pass": ok,
            "exceeds_eei": abs(w) > eei,
            "msg": msg,
        })
    rows.sort(key=lambda r: -abs(r["netTOA_drift_wm2"]))
    return rows


def summary(data: dict | None = None, tol_wm2: float = 0.1) -> dict:
    d = data if data is not None else load()
    rows = verdict_table(d, tol_wm2)
    eei = d["earth_energy_imbalance_wm2"]
    n = len(rows)
    n_fail = sum(1 for r in rows if not r["pass"])
    n_exceed = sum(1 for r in rows if r["exceeds_eei"])
    worst = rows[0]
    return {
        "n_models": n,
        "n_failing_conservation": n_fail,
        "n_exceeding_eei": n_exceed,
        "tol_wm2": tol_wm2,
        "eei_wm2": eei,
        "worst_model": worst["model"],
        "worst_drift_wm2": worst["netTOA_drift_wm2"],
        "worst_ratio_to_eei": round(worst["netTOA_drift_wm2"] / eei, 2),
        "verdict": (
            f"{n_fail} of {n} CMIP6 models leak energy beyond {tol_wm2} W/m2; "
            f"{n_exceed} leak faster than the Earth's energy imbalance ({eei} W/m2)."
        ),
    }


__all__ = ["load", "drift_wm2", "verdict_table", "summary"]
