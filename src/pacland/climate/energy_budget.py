"""Earth's energy-budget closure — the first real-data guard run.

Runs ``guard_energy_budget`` on published, cited component heat-uptake values
(CERES EEI; von Schuckmann et al. 2023) to demonstrate the two honest cases:

  - a single reservoir (0-2000 m ocean) UNDER-closes the budget -> guard FAILS,
    leaving a ~0.15 W/m2 residual that is the deep ocean + atmosphere + land +
    cryosphere;
  - the full budget (all reservoirs) CLOSES -> guard PASSES.

The lesson is the constraint-first one: the energy budget is only an invariant
when *all* its terms are accounted for; a partial ledger is not a closed ledger.

Pure stdlib + ``pacland.climate.guards``. Data: ``data/climate/energy_budget.json``.
"""
from __future__ import annotations

import json
from pathlib import Path

from .guards import guard_energy_budget

_DATA = Path(__file__).resolve().parents[3] / "data" / "climate" / "energy_budget.json"


def load() -> dict:
    return json.loads(_DATA.read_text())


def closure(data: dict | None = None) -> dict:
    d = data if data is not None else load()
    eei = d["eei_ceres_wm2"]
    comp = d["components_wm2"]
    full = sum(comp.values())
    ok_2000, msg_2000 = guard_energy_budget(eei, comp["ocean_0_2000m"], tol=0.02)
    ok_full, msg_full = guard_energy_budget(eei, full, tol=0.05)
    return {
        "eei_ceres_wm2": eei,
        "ocean_0_2000m_wm2": comp["ocean_0_2000m"],
        "full_budget_wm2": round(full, 3),
        "residual_0_2000m_only_wm2": round(eei - comp["ocean_0_2000m"], 3),
        "residual_full_wm2": round(eei - full, 3),
        "guard_0_2000m_only": {"pass": ok_2000, "msg": msg_2000},
        "guard_full": {"pass": ok_full, "msg": msg_full},
        "verdict": ("budget closes only with all reservoirs"
                    if (ok_full and not ok_2000) else "unexpected — check the inputs"),
    }


__all__ = ["load", "closure"]
