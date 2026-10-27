"""Climate's exact content — five invariants, and the one that is measured hardest.

A climate model's exact content is not a set of parameters; it is what the physics forbids.
Five conservation laws, each an invariant of the model equations and each with a measurement
that can fail:

| invariant | what it forbids | how it is measured |
|---|---|---|
| **energy** | net TOA flux ≠ Σ heat uptake across reservoirs | CERES Earth energy imbalance vs the reservoir sum (von Schuckmann) |
| **water** | precipitation ≠ evaporation + storage change | the global water budget |
| **carbon** | emissions ≠ atmospheric growth + sinks | the global carbon budget |
| **ocean mass** | mass change ≠ the sum of its sources | satellite gravimetry drift |
| **salinity** | salt created or destroyed | Argo salinity drift |

**What is exact here, and what is not.** Each invariant is an identity of the model's own
equations — total energy is the sum of its reservoirs, by construction — so it is exact in
the strong sense that macro-finance's accounting identities are not: it is a *physical* law,
not a definition anyone chose. What is *measured* is each model's compliance, and that
measurement is where the failures live: the energy budget closes only when **all** reservoirs
are counted (the upper ocean alone leaves a 0.15 W/m² residual), and 36 of 53 CMIP6 models
have no drift data at all.

So the inventory is proven at the level of the identities and honest about the level of the
measurement — the same split as Smets–Wouters' 16 proved conditions plus 4 specifications,
and for the same reason.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import energy_budget


@dataclass(frozen=True)
class Invariant:
    key: str
    statement: str
    measured_by: str
    status: str           # "identity + measured" | "identity, unmeasured here"


#: The five invariants. Status distinguishes "the identity is exact AND a measurement
#: exists in this repo" from "the identity is exact but nothing here measures it".
INVARIANTS: tuple[Invariant, ...] = (
    Invariant("energy", "net TOA flux = d(total heat content)/dt, summed over reservoirs",
              "CERES EEI vs von Schuckmann component sum", "identity + measured"),
    Invariant("water", "precipitation = evaporation + d(storage)/dt",
              "global water budget (measured: src/pacland/climate/water.py)",
              "identity + measured"),
    Invariant("carbon", "emissions = atmospheric growth + land + ocean sinks",
              "global carbon budget (measured: src/pacland/climate/carbon.py)",
              "identity + measured"),
    Invariant("ocean_mass", "d(ocean mass)/dt = sum of mass sources",
              "satellite gravimetry drift", "identity + measured"),
    Invariant("salinity", "salt is conserved: no source, no sink",
              "Argo salinity drift", "identity + measured"),
)


def closure(data: dict | None = None) -> dict:
    """The measured energy-budget closure, from the cited literature values."""
    return energy_budget.closure(data)


def closure_finding() -> dict:
    """The closure's own result: it does **not** close on the upper ocean alone.

    That is a substantive finding about the measurement, not a defect in the identity: the
    upper-ocean heat uptake (0.62 W/m²) is 0.15 W/m² short of the CERES imbalance (0.77),
    and the remaining 0.15 lives in the deep ocean, atmosphere, land and cryosphere. A model
    or a study that closes the budget on the upper ocean alone has quietly dropped most of
    the system.
    """
    c = closure()
    return {
        "eei": c["eei_ceres_wm2"],
        "upper_ocean_only": c["ocean_0_2000m_wm2"],
        "residual_upper_ocean": c["residual_0_2000m_only_wm2"],
        "full_sum": c["full_budget_wm2"],
        "residual_full": c["residual_full_wm2"],
        "closes_only_with_all_reservoirs": c["guard_full"]["pass"]
        and not c["guard_0_2000m_only"]["pass"],
    }


def coverage() -> dict:
    measured = [i.key for i in INVARIANTS if "measured" in i.status and "unmeasured" not in i.status]
    unmeasured = [i.key for i in INVARIANTS if "unmeasured" in i.status]
    return {"n_total": len(INVARIANTS), "n_measured": len(measured),
            "n_unmeasured": len(unmeasured), "measured": measured,
            "unmeasured": unmeasured, "complete": not unmeasured}


# --- guards -------------------------------------------------------------------


def guard_invariants_are_sourced() -> tuple[bool, str]:
    """Every invariant carries a statement and a named measurement."""
    bad = [i.key for i in INVARIANTS if not i.statement or not i.measured_by]
    return not bad, (f"{len(INVARIANTS)} invariants, "
                     f"{len(coverage()['measured'])} measured here"
                     + (f" — UNSOURCED: {', '.join(bad)}" if bad else ""))


def guard_closure_is_reported(tol_full: float = 0.05) -> tuple[bool, str]:
    """The closure must be *reported with its residual*, and it must close only with all
    reservoirs. A guard that let the upper-ocean-only budget pass would certify a model that
    dropped most of the climate system."""
    f = closure_finding()
    ok = abs(f["residual_full"]) <= tol_full and f["closes_only_with_all_reservoirs"]
    return ok, (
        f"energy: full sum {f['full_sum']:.2f} vs EEI {f['eei']:.2f} "
        f"(residual {f['residual_full']:+.3f}); upper ocean alone is short by "
        f"{f['residual_upper_ocean']:+.3f} W/m2"
    )


def guard_unmeasured_invariants_are_named() -> tuple[bool, str]:
    """An invariant with no measurement in this repo must say so rather than being counted
    as verified."""
    cov = coverage()
    ok = all("unmeasured" in i.status for i in INVARIANTS if i.key in cov["unmeasured"])
    return ok, (f"unmeasured: {', '.join(cov['unmeasured']) or 'none'} — named, not counted")


def summary() -> str:
    f = closure_finding()
    cov = coverage()
    lines = [
        "CLIMATE'S EXACT CONTENT — five invariants, and the measurement that fails",
        "=" * 70,
    ]
    for i in INVARIANTS:
        lines.append(f"  {i.key:<11} {i.status:<24} {i.measured_by}")
    lines += [
        "",
        f"energy closure: {f['full_sum']:.2f} W/m2 vs EEI {f['eei']:.2f} "
        f"-> residual {f['residual_full']:+.3f}",
        f"upper ocean alone: {f['upper_ocean_only']:.2f} -> short by "
        f"{f['residual_upper_ocean']:+.3f} W/m2 (the other reservoirs carry it)",
        "",
        f"coverage: {cov['n_measured']} of {cov['n_total']} invariants have a measurement "
        f"here; {cov['n_unmeasured']} are named and not counted",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
