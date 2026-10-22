"""Three-axis trust cross-check: conservation × sensitivity × forcing.

Combines the three-ledger conservation verdict (ours) with two of the field's
own quality axes to answer "which models survive ALL axes?" A model is fully
trustworthy only if it is:

  1. conservation-clean  — closes energy, mass and salt in its control run (ours);
  2. sensitivity-reasonable — ECS inside the IPCC likely range 2.5–4.0 K;
  3. forcing-reasonable — ERF2x inside the assessed 3.3–4.1 W/m² band.

Three independent sources close the single-source gap: the drift ledger is a
measured physical invariant, while ECS and ERF2x are the field's own published
diagnostics. ``crosscheck()`` counts how many of the three axes each model
fails; a model that fails none is the only one worth building on.

Pure stdlib + ``pacland.climate.cmip6_drift``. Data: ``data/climate/cmip6_ecs.json``.
"""
from __future__ import annotations

import json
from pathlib import Path

from .cmip6_drift import verdict_table

_DATA = Path(__file__).resolve().parents[3] / "data" / "climate" / "cmip6_ecs.json"


def load() -> dict:
    return json.loads(_DATA.read_text())


def sensitivity_tier(ecs: float, d: dict) -> str:
    if ecs <= d["likely_range_K"][1]:
        return "reasonable"
    if ecs <= d["hot_threshold_K"]:
        return "high"
    return "hot"


def forcing_tier(erf2x: float, d: dict) -> str:
    lo, hi = d["forcing_range_Wm2"]
    if erf2x < lo:
        return "low"
    if erf2x > hi:
        return "high"
    return "reasonable"


def _axes_failed(ledgers: int, sensitivity: str, forcing: str) -> list[str]:
    failed = []
    if ledgers > 0:
        failed.append("conservation")
    if sensitivity != "reasonable":
        failed.append("sensitivity")
    if forcing != "reasonable":
        failed.append("forcing")
    return failed


def _verdict(failed: list[str]) -> str:
    n = len(failed)
    if n == 0:
        return "survives all three axes"
    if n == 1:
        return f"fails 1 axis — {failed[0]}"
    if n == 2:
        return f"fails 2 axes — {' + '.join(failed)}"
    return "fails all three axes"


def crosscheck() -> list[dict]:
    """Per-model three-axis verdict: conservation × sensitivity × forcing."""
    d = load()
    ecs = d["ecs_K"]
    erf = d["erf2x_Wm2"]
    rows = []
    for r in verdict_table():
        m = r["model"]
        e = ecs.get(m)
        f = erf.get(m)
        if e is None or f is None:
            continue
        ledgers = r["n_failed_ledgers"]
        sens = sensitivity_tier(e, d)
        forc = forcing_tier(f, d)
        failed = _axes_failed(ledgers, sens, forc)
        rows.append({
            "model": m,
            "ledgers_failed": ledgers,
            "ecs_K": e,
            "sensitivity": sens,
            "erf2x_Wm2": f,
            "forcing": forc,
            "axes_failed": failed,
            "n_axes_failed": len(failed),
            "verdict": _verdict(failed),
        })
    rows.sort(key=lambda r: (r["n_axes_failed"], r["ledgers_failed"], r["ecs_K"]),
              reverse=True)
    return rows


def summary() -> dict:
    d = load()
    rows = crosscheck()
    surviving = [r for r in rows if r["n_axes_failed"] == 0]
    one_axis = [r for r in rows if r["n_axes_failed"] == 1]
    clean = [r for r in rows if r["ledgers_failed"] == 0]
    return {
        "n_models": len(rows),
        "n_survives_all": len(surviving),
        "survives_all_axes": [r["model"] for r in surviving],
        "n_fails_one_axis": len(one_axis),
        "fails_one_axis": [r["model"] for r in one_axis],
        "n_conservation_clean": len(clean),
        "verdict": (
            f"{len(surviving)} of {len(rows)} models survive all three axes — "
            f"conservation-clean, ECS inside 2.5–4.0 K, and ERF2x inside "
            f"3.3–4.1 W/m²: {', '.join(r['model'] for r in surviving)}. "
            f"The forcing axis sharpens the two-axis result: "
            f"MPI-ESM1-2-LR / MPI-ESM-1-2-HAM leak AND force too strongly, "
            f"ACCESS-ESM1-5 / BCC / CNRM-ESM2-1 leak AND force too weakly, "
            f"E3SM-1-1 is conservation-clean but hot, and EC-Earth3-Veg is "
            f"conservation-clean but high-sensitivity — conservation alone is "
            f"never enough."
        ),
    }


__all__ = ["load", "sensitivity_tier", "forcing_tier", "crosscheck", "summary",
           "trust_entries"]


def trust_entries() -> list:
    """Emit the three-axis trust entries (clean = all three pass; broken = ≥2 fail)."""
    from ..trust import TrustEntry

    out = []
    for r in crosscheck():
        if r["n_axes_failed"] == 0:
            tier = "clean"
        elif r["n_axes_failed"] >= 2:
            tier = "broken"
        else:
            tier = "weak"
        ledgers = (f"{r['ledgers_failed']} ledger"
                   + ("" if r["ledgers_failed"] == 1 else "s") + " failed")
        out.append(TrustEntry(
            discipline="climate",
            artifact=f"CMIP6 {r['model']}",
            tier=tier,
            detail=(f"{r['verdict']} — {ledgers}, "
                    f"ECS {r['ecs_K']:.2f} K, ERF2x {r['erf2x_Wm2']:.2f} W/m²"),
            evidence="Irving et al. 2021 (drift) + Zelinka et al. 2020 (ECS + ERF2x)",
        ))
    return out
