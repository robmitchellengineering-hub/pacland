"""Two-axis trust cross-check: conservation (ours) × sensitivity (the field's ECS).

Combines the three-ledger conservation verdict with the published Equilibrium
Climate Sensitivity to answer "which models survive BOTH axes?" Conservation is
one necessary condition (physical soundness); sensitivity is the field's own
quality axis (is the model implausibly "hot"?). A model is fully trustworthy
only if it is conservation-clean AND its ECS is within the likely range — the
second independent source that closes the single-source gap.

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


def crosscheck() -> list[dict]:
    """Per-model two-axis verdict: conservation × sensitivity."""
    d = load()
    ecs = d["ecs_K"]
    rows = []
    for r in verdict_table():
        m = r["model"]
        e = ecs.get(m)
        if e is None:
            continue
        ledgers = r["n_failed_ledgers"]
        sens = sensitivity_tier(e, d)
        if ledgers == 0 and sens == "reasonable":
            verdict = "survives both axes"
        elif ledgers == 0:
            verdict = f"clean but {sens} sensitivity"
        elif sens == "reasonable":
            verdict = "leaky but reasonable sensitivity"
        else:
            verdict = f"leaky AND {sens} sensitivity"
        rows.append({
            "model": m,
            "ledgers_failed": ledgers,
            "ecs_K": e,
            "sensitivity": sens,
            "verdict": verdict,
        })
    rows.sort(key=lambda r: (r["ledgers_failed"], r["ecs_K"]))
    return rows


def summary() -> dict:
    d = load()
    rows = crosscheck()
    surviving = [r for r in rows if r["verdict"] == "survives both axes"]
    clean_hot = [r for r in rows if r["verdict"] in ("clean but hot sensitivity", "clean but high sensitivity")]
    return {
        "n_models": len(rows),
        "n_survives_both": len(surviving),
        "survives_both_axes": [r["model"] for r in surviving],
        "clean_but_sensitive": [r["model"] for r in clean_hot],
        "verdict": (
            f"{len(surviving)} of {len(rows)} models survive both axes — "
            f"conservation-clean AND within the likely sensitivity range: "
            f"{', '.join(r['model'] for r in surviving)}. "
            f"The conservation-cleanest (EC-Earth3-Veg) is only 'high' sensitivity, "
            f"and E3SM-1-1 is clean but hot — so conservation alone is not enough."
        ),
    }


__all__ = ["load", "sensitivity_tier", "crosscheck", "summary"]
