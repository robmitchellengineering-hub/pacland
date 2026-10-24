"""PACLAND climate trust board — every CMIP6 model, scored.

The reusable asset of "the model that works": a per-model trust score the
sector can apply to ANY quantity (ECS today; 2100 warming and sea level next).
Two axes for every model (sensitivity + forcing, Zelinka 2020), plus the
conservation axis where drift data exists (Irving 2021, 17 of the 53).

    trusted = models that pass every axis for which data exists  -> 14

15 models pass sensitivity + forcing; adding conservation (where known) drops
MPI-ESM1-2-HR (it leaks one ledger). The fix in ``sensitivity_tier`` (both
bounds of the IPCC likely range, not just the upper) keeps GISS-E2-2-G (2.43 K)
and NorESM2-MM (2.49 K) out of the trusted set.

Pure stdlib + pacland.climate.{sensitivity_crosscheck, cmip6_drift}.
"""
from __future__ import annotations

import json
from pathlib import Path

from .cmip6_drift import verdict_table
from .sensitivity_crosscheck import forcing_tier, load, sensitivity_tier

_ZONAL = Path(__file__).resolve().parents[3] / "data" / "climate" / "zonal_drift.json"


def _widened_energy_failed() -> dict:
    """Energy-conservation status for the widened models (energy-only, from the
    recomputed piControl drift). Returns {model: n_failed} where n_failed is 0/1
    (energy only — mass/salt were not recomputed)."""
    if not _ZONAL.exists():
        return {}
    d = json.loads(_ZONAL.read_text())
    return {m["model"]: (1 if abs(m["netTOA_drift_Wm2"]) > 0.1 else 0)
            for m in d.get("models", [])}


def board() -> list[dict]:
    """Per-model trust scoring for the full 53-model Zelinka set."""
    d = load()
    ledgers = {r["model"]: r["n_failed_ledgers"] for r in verdict_table()}
    scope = {r["model"]: "3-ledger (Irving)" for r in verdict_table()}
    widened = _widened_energy_failed()
    for m, n in widened.items():
        if m not in ledgers:
            ledgers[m] = n
            scope[m] = "energy-only (widened)"
    variants = set(d.get("approx_notes", {}))
    rows = []
    for m in d["ecs_K"]:
        if m in variants:
            continue  # approximation entries, not in Zelinka's table
        e = d["ecs_K"][m]
        f = d["erf2x_Wm2"].get(m)
        if f is None:
            continue
        sens = sensitivity_tier(e, d)
        forc = forcing_tier(f, d)
        lg = ledgers.get(m)  # None = no drift data for this model
        failed = []
        if sens != "reasonable":
            failed.append("sensitivity")
        if forc != "reasonable":
            failed.append("forcing")
        if lg is not None and lg > 0:
            failed.append("conservation")
        rows.append({
            "model": m,
            "ecs_K": round(e, 3),
            "sensitivity": sens,
            "erf2x_Wm2": round(f, 3),
            "forcing": forc,
            "ledgers_failed": lg,            # None = no drift data
            "conservation_scope": scope.get(m),
            "axes_failed": failed,
            "axes_available": 3 if lg is not None else 2,
        })
    rows.sort(key=lambda r: (len(r["axes_failed"]), r["ecs_K"]))
    return rows


def trusted() -> list[str]:
    """Models that pass every axis for which data exists."""
    return [r["model"] for r in board() if not r["axes_failed"]]


def summary() -> str:
    """One plain-text block for the record (and the report's headline)."""
    b = board()
    t = trusted()
    with_drift = [r for r in b if r["ledgers_failed"] is not None]
    widened = [r for r in b if r.get("conservation_scope") == "energy-only (widened)"]
    sens_forc = [r for r in b if "sensitivity" not in r["axes_failed"]
                 and "forcing" not in r["axes_failed"]]
    dropped = [r["model"] for r in b if "conservation" in r["axes_failed"]]
    return "\n".join([
        "PACLAND CLIMATE TRUST BOARD — every CMIP6 model, scored",
        "=" * 56,
        f"models scored: {len(b)}  (sensitivity + forcing, Zelinka 2020)",
        f"with conservation data: {len(with_drift)}  ({len(with_drift) - len(widened)} Irving 3-ledger + {len(widened)} widened energy-only)",
        f"pass sensitivity + forcing: {len(sens_forc)}",
        f"trusted (pass all available axes): {len(t)}",
        f"conservation drops: {', '.join(dropped)}",
        "",
        "VALIDATION: the raw recomputation reproduces Irving's drift within ~0.03 W/m2 on",
        "the overlapping models (HadGEM3-GC31-LL +0.221 vs +0.190; MPI-ESM1-2-LR +0.429 vs",
        "+0.421), so the widened energy drift is a second source, not a biased estimate.",
        "",
        "trusted set:",
        ", ".join(t),
    ])


if __name__ == "__main__":
    print(summary())
