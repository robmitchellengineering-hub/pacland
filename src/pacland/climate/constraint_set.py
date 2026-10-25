"""Climate's constraint set — the same rank question economics answers, asked here.

Economics holds **18 written-down constraints and 8 independent ones**, measured by the rank
of the constraint Jacobian at a generic point (`economics/constraint_set.py`). Climate has
never been asked that question. This module asks it.

The inventory is deliberately *everything* climate currently imposes:

- **five invariants** (energy, water, carbon, ocean mass, salinity) — the physics;
- **six guards** (`climate/guards.py`) — the same laws expressed as pass/fail checks with
  numbers on them;
- **three calibration bands** (ECS, ERF2x, drift) — the per-model assessed ranges.

That immediately looks redundant, and it is: the guards are the invariants restated with
thresholds. The Jacobian rank is what turns "looks redundant" into a number.

**Process constraints are excluded from the rank and named instead** — "fit only on data
≤ y₀", "CO₂ extrapolated", "target outside the window" constrain *how a forecast is made*,
not the state of the atmosphere. Folding them into a state-space Jacobian would be a category
error, and counting them as independent would inflate the number.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

TOL = 1e-9


@dataclass(frozen=True)
class Constraint:
    key: str
    kind: str          # invariant | guard | calibration
    statement: str
    residual: Callable[[dict], float]
    #: A differentiable stand-in, for checks with max()/abs() whose central difference
    #: vanishes at the kink or at the solution.
    smooth: Callable[[dict], float] | None = None

    def grad_residual(self, s: dict) -> float:
        return (self.smooth or self.residual)(s)


#: A state that satisfies nothing in particular — the rank is a property of the set, so it
#: is measured where no residual is accidentally zero.
def _state(**over: float) -> dict:
    base = {
        "net_toa": 0.77, "d_total_energy": 0.76,
        "precip": 1.0, "evap": 0.9, "runoff": 0.1, "d_column_water": 0.0,
        "emissions": 10.0, "d_atm": 5.0, "ocean_uptake": 2.6, "land_uptake": 2.4,
        "ocean_mass_drift": 0.05, "salt_drift": 1e-9,
        "q": 0.01, "ecs": 3.0, "erf2x": 3.7, "ledgers_failed": 0,
    }
    base.update(over)
    return base


#: Physics: the five invariants.
INVARIANTS: tuple[Constraint, ...] = (
    Constraint("energy", "invariant", "net TOA flux = d(total heat content)/dt",
               lambda s: s["net_toa"] - s["d_total_energy"]),
    Constraint("water", "invariant", "P - E - runoff = d(column water)/dt",
               lambda s: (s["precip"] - s["evap"] - s["runoff"]) - s["d_column_water"]),
    Constraint("carbon", "invariant", "emissions = Δatm + ocean + land",
               lambda s: s["emissions"] - (s["d_atm"] + s["ocean_uptake"] + s["land_uptake"])),
    Constraint("ocean_mass", "invariant", "Δ(ocean mass) = its sources",
               lambda s: s["ocean_mass_drift"]),
    Constraint("salinity", "invariant", "salt has no source or sink",
               lambda s: s["salt_drift"]),
)

#: The same laws as guards — one per invariant, plus the humidity forbidden-state check.
GUARDS: tuple[Constraint, ...] = (
    Constraint("g_energy", "guard", "guard_energy_budget", lambda s: s["net_toa"] - s["d_total_energy"]),
    Constraint("g_water", "guard", "guard_water_budget",
               lambda s: (s["precip"] - s["evap"] - s["runoff"]) - s["d_column_water"]),
    Constraint("g_carbon", "guard", "guard_carbon_budget",
               lambda s: s["emissions"] - (s["d_atm"] + s["ocean_uptake"] + s["land_uptake"])),
    Constraint("g_humidity", "guard", "specific humidity >= 0",
               lambda s: s["q"], smooth=lambda s: s["q"]),
    Constraint("g_mass", "guard", "guard_ocean_mass", lambda s: s["ocean_mass_drift"]),
    Constraint("g_salt", "guard", "guard_ocean_salt", lambda s: s["salt_drift"]),
)

#: Per-model calibration bands — the only constraints that are about a *model* rather than
#: the physics. Residual 0 inside the band, the distance outside it otherwise.
CALIBRATION: tuple[Constraint, ...] = (
    Constraint("ecs_band", "calibration", "2.5 <= ECS <= 4.0 K",
               lambda s: max(2.5 - s["ecs"], s["ecs"] - 4.0, 0.0), smooth=lambda s: s["ecs"] - 3.25),
    Constraint("erf2x_band", "calibration", "3.3 <= ERF2x <= 4.1 W/m2",
               lambda s: max(3.3 - s["erf2x"], s["erf2x"] - 4.1, 0.0),
               smooth=lambda s: s["erf2x"] - 3.7),
    Constraint("ledgers", "calibration", "no conservation ledger fails",
               lambda s: float(s["ledgers_failed"]), smooth=lambda s: float(s["ledgers_failed"])),
)

STATE_CONSTRAINTS = INVARIANTS + GUARDS + CALIBRATION

#: Constraints that are not properties of a state, so they are excluded from the rank by
#: kind rather than by convenience.
PROCESS_CONSTRAINTS = (
    "hindcast fits only on data <= y0",
    "CO2 after y0 is extrapolated, never observed",
    "the target year lies outside the forecast window",
    "units are degrees C, not kelvin",
    "the ECS emulator is not the CMIP6 model run",
)


def variables() -> list[str]:
    return sorted(_state())


def _rank(rows: list[list[float]], tol: float = 1e-8) -> int:
    m = [row[:] for row in rows]
    rank = 0
    cols = len(m[0]) if m else 0
    for col in range(cols):
        pivot = None
        for r in range(rank, len(m)):
            if abs(m[r][col]) > tol:
                pivot = r
                break
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        p = m[rank][col]
        for r in range(len(m)):
            if r != rank and m[r][col]:
                f = m[r][col] / p
                for c in range(col, cols):
                    m[r][c] -= f * m[rank][c]
        rank += 1
    return rank


def independence(step: float = 1e-6) -> dict:
    """Rank at a generic point — no residual is zero there, so nothing hides."""
    s = _state(q=0.01, ecs=3.0, erf2x=3.7, ledgers_failed=0.0)
    names = variables()
    rows, keys = [], []
    for c in STATE_CONSTRAINTS:
        grad = []
        for name in names:
            up, dn = dict(s), dict(s)
            up[name] = s[name] + step
            dn[name] = s[name] - step
            grad.append((c.grad_residual(up) - c.grad_residual(dn)) / (2 * step))
        if any(abs(v) > 1e-12 for v in grad):
            rows.append(grad)
            keys.append(c.key)
    rank = _rank(rows)
    return {"n_state": len(rows), "rank": rank, "dependent": len(rows) - rank,
            "independent": keys}


def summary() -> str:
    ind = independence()
    n_written = len(STATE_CONSTRAINTS) + len(PROCESS_CONSTRAINTS)
    lines = [
        "CLIMATE'S CONSTRAINT SET — written down versus independent",
        "=" * 68,
        f"written down            {n_written}",
        f"  state constraints     {len(STATE_CONSTRAINTS)}  "
        f"(5 invariants + 6 guards + 3 calibration bands)",
        f"  process constraints   {len(PROCESS_CONSTRAINTS)}  (excluded from the rank: they "
        f"constrain how a forecast is made, not the state)",
        "",
        f"independent state rank  {ind['rank']} of {ind['n_state']}",
        f"dependent (redundant)   {ind['dependent']}",
        "",
        "The redundancy is the guards: five of the six restate the five invariants with a",
        "threshold instead of an equality. They are not waste — a guard is what fails loudly",
        "on a model, an invariant is what the physics says — but they are not independent,",
        "and a count that treated them as eleven constraints would be inflating the number.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
