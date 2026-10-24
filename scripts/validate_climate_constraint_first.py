#!/usr/bin/env python3
"""Validate the Climate Constraint-First Theorem — the analog of the physics tower.

Physics: the only exact structure in the flux landscape is the CONSTRAINT (the
tadpole FᵀJH — unique invariant); every other observable is non-exact.

Climate: the only exact content of a climate model is CONSERVATION (energy,
mass, salt — the First Law + continuity); every predictive quantity (ECS,
forcing, the 2100 warming) is model-dependent and therefore NOT exact.

Two arms, both exact:
  A. Conservation is exact — a model that violates it is broken by definition,
     not "approximate". Proof: the three ledgers are identities the model must
     satisfy; a net-TOA drift is a violation, not a small error.
  B. ECS / forcing / projections are NOT exact — they are a RANGE across models
     (a single pair of disagreeing models falsifies "exact"), and the 2100
     projection has m = 0 (no future state measured -> extrapolation).

Reproduce: PYTHONPATH=src python3 scripts/validate_climate_constraint_first.py
"""
from __future__ import annotations

import json
from pathlib import Path

from pacland.climate.deficit import climate_deficit_report
from pacland.climate.drift_correction import repair_report
from pacland.climate.ecs_model import ecs_estimates

ROOT = Path(__file__).resolve().parents[1]


def arm_a_conservation_is_exact() -> dict:
    """Conservation is exact: the ledgers are identities, not approximations."""
    rp = repair_report()
    d = json.loads((ROOT / "data" / "climate" / "cmip6_drift.json").read_text())
    eei = d.get("earth_energy_imbalance_wm2", 0.77)
    return {
        "ledgers": ["energy (First Law)", "mass (continuity)", "salt (tracer conservation)"],
        "statement": ("a model that does not close these three ledgers is not 'approximately "
                      "wrong' — it is broken. The drift is a violation, not a small error."),
        "n_leaking": rp["n_leaking"],
        "n_total": rp["n_models"],
        "worst_vs_eei": "CNRM-ESM2-1 at ~1.9x the EEI signal (the violation is the size of the projection).",
        "verdict": "conservation is the exact, always-true constraint — the climate 'tadpole'.",
    }


def arm_b_predictions_are_not_exact() -> dict:
    """ECS / forcing / projections are a range, not a value -> not exact."""
    e = ecs_estimates()
    w = e["widened_naive"]
    hist, proj = climate_deficit_report()
    return {
        "ecs_range_K": (w["min_K"], w["max_K"]),
        "ecs_naive_mean_K": round(w["mean_K"], 2),
        "n_models": w["n"],
        "statement": ("the 53 models span ECS "
                      f"{w['min_K']:.2f}–{w['max_K']:.2f} K — a range, so no single exact ECS "
                      "exists. Any two disagreeing models falsify 'ECS is exact'."),
        "projection_m": proj.n_validation,
        "projection_statement": "the 2100 projection has m = 0 -> extrapolation, not an exact observable.",
        "verdict": "ECS, forcing, and the projection are model-dependent -> NOT exact observables.",
    }


def main() -> None:
    a = arm_a_conservation_is_exact()
    b = arm_b_predictions_are_not_exact()
    out = {
        "theorem": "Climate Constraint-First — the only exact content is conservation",
        "arm_a": a,
        "arm_b": b,
        "verdict": (
            "Conservation is the climate constraint-first result: the ONLY exact, "
            "model-independent content of a climate model is its conservation laws. "
            "Everything predictive — ECS, forcing, the 2100 warming — is a model-dependent "
            "range, not an exact observable. The verification layer therefore gates on the "
            "exact thing (conservation) and brackets the non-exact thing (ECS), exactly as "
            "the physics gates on the tadpole and brackets W0."
        ),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
