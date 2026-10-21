"""Climate falsification guards — the first guard-suite (playbook item #1).

Mirrors ``pacland.guards``: each guard asserts one physical invariant a climate
model's output must satisfy, under the Valiant Verification discipline —

  - a violation fails LOUDLY (a silent pass is a fail),
  - each guard has a seeded-fault mutation test in
    ``tests/test_climate_guards.py`` proving it goes red on the fault it exists
    to catch.

These are the *constraint-first* half of the method: conservation laws are what
a model FORBIDS being violated — the reliable content — as opposed to the free
values it projects. Real CMIP6 outputs plug into these guards later; for now
they are exercised on exact/toy data, same contract, no model needed.
"""
from __future__ import annotations


def guard_energy_budget(net_toa_flux: float, d_energy_dt: float, tol: float = 1e-6) -> tuple[bool, str]:
    """Earth's energy budget: net TOA flux equals the rate of change of total
    heat content (ocean + atmosphere + cryosphere + land).

    Fails on a model whose radiative imbalance is not matched by the change in
    stored energy — the drift class quantified for CMIP6 by Irving et al. 2021.
    """
    resid = net_toa_flux - d_energy_dt
    ok = abs(resid) <= tol
    return ok, f"energy budget residual={resid:+.3e} (tol {tol})"


def guard_water_budget(
    precip: float, evap: float, runoff: float, d_column_water: float, tol: float = 1e-6
) -> tuple[bool, str]:
    """Global water budget: precipitation - evaporation - runoff = d(column water)/dt.

    Fails on a model that does not conserve water mass — the constraint-first
    "forbidden" check for the hydrological cycle.
    """
    resid = (precip - evap - runoff) - d_column_water
    ok = abs(resid) <= tol
    return ok, f"water budget residual={resid:+.3e} (tol {tol})"


def guard_carbon_budget(
    emissions: float, d_atm: float, ocean_uptake: float, land_uptake: float, tol: float = 1e-6
) -> tuple[bool, str]:
    """Carbon budget: cumulative emissions = atmospheric growth + ocean + land sinks.

    Fails on a model whose carbon ledger does not close — the accounting closure
    the Global Carbon Budget already imposes informally, here as a hard guard.
    """
    resid = emissions - (d_atm + ocean_uptake + land_uptake)
    ok = abs(resid) <= tol
    return ok, f"carbon budget residual={resid:+.3e} (tol {tol})"


def guard_nonnegative_specific_humidity(q, tol: float = 0.0) -> tuple[bool, str]:
    """Forbidden-state guard: specific humidity cannot be negative.

    The "what the model forbids" check — a negative water-vapour mass fraction is
    unphysical in every state, so a violation is a hard falsification, not a
    tuning issue. The constraint-first analogue of ``guard_integer_flux``.
    """
    bad = [v for v in q if v < -tol]
    return not bad, f"negative specific humidity at {len(bad)} point(s): {bad[:5]}"


__all__ = [
    "guard_energy_budget",
    "guard_water_budget",
    "guard_carbon_budget",
    "guard_nonnegative_specific_humidity",
]
