#!/usr/bin/env python3
"""Climate: does conservation drift transfer linearly into ECS?

    python3 scripts/energy_drift_ecs.py [--ecs PATH]

REGISTERED, PARTLY PREPARED. Claim (docs/energy-conjectures.md): a model's conservation residual eps in
piControl transfers linearly to its ECS — slope of log|dECS| on log|eps| is 1.0 +/- 0.2, with
|dECS|/|eps| ~ 0.76 K per W/m2 — so a one-line correction to abrupt-4xCO2 ECS suffices.

What this repository already has: data/climate/cmip6_drift.json, the three conservation ledgers for 19
models (Irving et al. 2021). What it does not have: the per-model ECS column (Zelinka et al. 2020).
So this script computes the drift it can, prints it, and REFUSES to state the transfer until the ECS
column is supplied. No verdict without the join.

Falsifier: slope > 1.3 or < 0.7, or |dECS|/|eps| outside [0.4, 1.2].
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DRIFT = ROOT / "data" / "climate" / "cmip6_drift.json"
#: Earth surface area, m2 — the conversion from J/yr to W/m2.
AREA_M2 = 5.1e14
SECONDS_PER_YEAR = 3.15e7


def net_toa_wm2(row: dict) -> float:
    """The model's net top-of-atmosphere imbalance in W/m2 from its J/yr ledger."""
    return row["netTOA_J_per_yr"] / (AREA_M2 * SECONDS_PER_YEAR)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Drift -> ECS transfer test (registered).")
    ap.add_argument("--ecs", default=str(ROOT / "data" / "climate" / "cmip6_ecs_models.json"))
    args = ap.parse_args(argv[1:])

    if not DRIFT.is_file():
        print(f"REFUSED: no drift ledger at {DRIFT}")
        return 2
    drift = json.loads(DRIFT.read_text())
    rows = drift.get("models") or drift.get("rows") or []
    if not rows:
        print("REFUSED: the drift ledger has no model rows")
        return 2

    print(f"Drift ledger: {len(rows)} models (Irving et al. 2021)\n")
    print(f"  {'model':28} {'netTOA W/m2':>12}")
    for row in sorted(rows, key=lambda r: abs(net_toa_wm2(r)), reverse=True)[:8]:
        print(f"  {row['model'][:28]:28} {net_toa_wm2(row):>+12.3f}")
    print(f"  ... {max(0, len(rows) - 8)} more")

    ecs_path = pathlib.Path(args.ecs)
    if not ecs_path.is_file():
        print()
        print("REFUSED: the per-model ECS column is not present, so the transfer cannot be tested.")
        print(f"  looked for: {ecs_path}")
        print()
        print("What is needed: Zelinka et al. (2020) ECS for these 19 models, as")
        print('  {"models": [{"model": "...", "ecs_K": 3.2}, ...]}')
        print()
        print("  prediction : slope of log|dECS| on log|eps| = 1.0 +/- 0.2; ratio 0.76 K per W/m2")
        print("  falsifier  : slope > 1.3 or < 0.7, or ratio outside [0.4, 1.2]")
        return 2

    ecs = json.loads(ecs_path.read_text()).get("models", [])
    by_model = {m["model"]: m["ecs_K"] for m in ecs}
    joined = [(r["model"], net_toa_wm2(r), by_model[r["model"]]) for r in rows if r["model"] in by_model]
    print(f"\nJoined {len(joined)} of {len(rows)} models with an ECS value.")
    if len(joined) < 10:
        print("REFUSED: fewer than 10 joined models cannot test a slope.")
        return 2
    print("REFUSED: the join exists but the regression is not implemented in this change —")
    print("registering a falsifier is not the same as running the test.")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
