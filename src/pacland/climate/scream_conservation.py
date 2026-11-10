"""SCREAM conservation — the p̂_e (oracle-vs-truth) term behind the STRATA finding.

STRATA is verified against SCREAM (reference-fidelity). This module asks the
next level of the two-level certificate: *is the oracle itself right against
the Earth?* Three independent sources answer it:

1. **The E3SM lineage's measured conservation** (``data/climate/cmip6_drift.json``):
   E3SM-1-0 and E3SM-1-1 are the coupled models that carry SCREAM's atmosphere
   physics. Their net-TOA drift is ~-0.02 and ~-0.07 W/m2 — among the cleanest of
   the 19 CMIP6 models (30-65x smaller than the worst leaker, CNRM-ESM2-1 at
   +1.49 W/m2).

2. **SCREAM's own energy checker** (``check_energy.F90``, E3SM-Project/scream):
   it checks column total-energy conservation to 1e-14 relative error and water
   to 1e-10, AND applies a global energy *fixer* — "add a globally uniform
   heating term to account for any change of total energy" — so the global energy
   budget is forced closed every physics step.

3. **The wall**: the STRATA-published data cannot independently re-measure the
   km-scale drift — the HuggingFace Zarr is subsampled to 14 emulator variables
   (no radiation), the raw output is ~33 TB on NERSC tape, and the runs are
   17-day forced (not piControl), so the CMIP6 drift oracle does not transfer.

The definite answer, assembled from those three:

    SCREAM does NOT leak energy in the CMIP6 drift sense — it is enforced by
    design (the fixer) and verified clean in its parent lineage. Two honest
    caveats: (a) the fixer's magnitude is the raw physics energy error before
    correction, and it is not published; (b) the parent lineage DOES leak mass
    (E3SM-1-0: -0.49 mm/yr), and the nonhydrostatic km-scale core's energy
    conservation is a separate, active research question (GMD 2024).

Pure stdlib + the existing ``pacland.climate.cmip6_drift`` module.
"""
from __future__ import annotations

from .cmip6_drift import drift_wm2, mass_drift_mm_per_yr, verdict_table, load

# SCREAM/E3SM physics energy-checker tolerances (check_energy.F90, E3SM-Project/scream)
ENERGY_REL_TOL = 1e-14
WATER_REL_TOL = 1e-10

# Primary sources
CHECK_ENERGY_SRC = "E3SM-Project/scream components/eam/src/physics/cam/check_energy.F90"
CMIP6_DRIFT_SRC = "Irving et al. 2021, figshare doi:10.6084/m9.figshare.12143562"
NONHYDRO_SRC = ("GMD 17, 1429-1442, 2024: 'Energy-conserving physics for nonhydrostatic "
                "dynamics in mass coordinate models', doi:10.5194/gmd-17-1429-2024")

# The Earth's real mass accretion (cosmic dust + micrometeorites), for the
# "is the model's mass drift actually physical?" check.
EARTH_MASS_ACCRETION_KG_PER_YR = 4.0e7   # ~40,000 t/yr (Love & Brownlee 1993, Science 262:550)
ACCRETION_SRC = "Love & Brownlee 1993, Science 262, 550-553"

# The energy-budget tolerance used to call a model "clean" (matches cmip6_drift.verdict_table).
ENERGY_TOL_WM2 = 0.1
MASS_TOL_MM_PER_YR = 0.3


def parent_drift() -> dict:
    """E3SM-1-0 / E3SM-1-1 net-TOA and ocean-mass drift, recomputed from the repo data.

    The parent lineage carries the atmosphere physics SCREAM inherits; its drift
    is the closest *measured* proxy for SCREAM's own conservation that the repo
    holds. Values are computed, not typed, from ``data/climate/cmip6_drift.json``.
    """
    d = load()
    out = {}
    for m in d["models"]:
        if "E3SM" not in m["model"]:
            continue
        row = {
            "netTOA_wm2": round(drift_wm2(m["netTOA_J_per_yr"]), 4),
        }
        if "masso_kg_per_yr" in m:
            row["mass_mm_per_yr"] = round(mass_drift_mm_per_yr(m["masso_kg_per_yr"]), 4)
        out[m["model"]] = row
    return out


def mass_leak_vs_accretion_ratio() -> float:
    """E3SM-1-0's ocean-mass drift vs the Earth's real cosmic-dust accretion.

    The drift is ~1.75e14 kg/yr of WATER; the Earth accretes ~4e7 kg/yr of SOLID
    dust. A ratio ~1e6 proves the drift is a numerical water-cycle defect, not a
    real mass signal: the two differ by ~6 orders of magnitude and live in
    different reservoirs (ocean water vs lithosphere).
    """
    m = next(x for x in load()["models"] if x["model"] == "E3SM-1-0")
    return abs(m["masso_kg_per_yr"]) / EARTH_MASS_ACCRETION_KG_PER_YR


def _e3sm_rows() -> dict:
    return {r["model"]: r for r in verdict_table() if "E3SM" in r["model"]}


def verdict() -> dict:
    """The definite, evidence-backed answer to 'is SCREAM leaking'."""
    rows = _e3sm_rows()
    energy_drifts = {m: r["netTOA_drift_wm2"] for m, r in rows.items()}
    mass_drifts = {m: r["mass_drift_mm_per_yr"] for m, r in rows.items()
                   if "mass_drift_mm_per_yr" in r}
    energy_clean = all(abs(v) <= ENERGY_TOL_WM2 for v in energy_drifts.values())
    mass_leaks = {m: v for m, v in mass_drifts.items() if abs(v) > MASS_TOL_MM_PER_YR}
    return {
        "parent_energy_drift_wm2": energy_drifts,
        "parent_energy_clean": energy_clean,
        "parent_mass_leak_mm_per_yr": mass_leaks,
        "energy_enforced_by_fixer": True,
        "energy_check_rel_tol": ENERGY_REL_TOL,
        "water_check_rel_tol": WATER_REL_TOL,
        "km_scale_drift_measurable_from_published": False,
        "verdict": (
            "SCREAM does not leak energy (enforced by the fixer, parent E3SM drift "
            f"{energy_drifts.get('E3SM-1-0')} / {energy_drifts.get('E3SM-1-1')} W/m2, both "
            f"within {ENERGY_TOL_WM2} W/m2). It leaks MASS in the parent lineage "
            f"({sorted(mass_leaks.items())}). The km-scale drift and the fixer's magnitude "
            "are not published, so they are UNKNOWN, not clean."
        ),
    }


def two_level_bound() -> str:
    """The two-level certificate with the SCREAM (oracle) term filled in."""
    v = verdict()
    d = load()
    return (
        "TWO-LEVEL CERTIFICATE  p_* <= p_hat_g + p_hat_e + radius_s + radius_e\n"
        f"  p_hat_g = STRATA vs SCREAM (the emulator's reference-fidelity)\n"
        f"  p_hat_e = SCREAM vs the Earth:\n"
        f"      energy: enforced by the fixer ({CHECK_ENERGY_SRC}), parent E3SM drift "
        f"{v['parent_energy_drift_wm2']} W/m2 — clean vs EEI {d['earth_energy_imbalance_wm2']} W/m2\n"
        f"      mass:   parent E3SM leaks {v['parent_mass_leak_mm_per_yr']} mm/yr\n"
        f"      km-scale drift + fixer magnitude: not published (UNKNOWN)\n"
    )


def summary() -> str:
    """One plain-text block for the record."""
    v = verdict()
    pd = parent_drift()
    return "\n".join([
        "SCREAM (E3SM km-scale) — the oracle behind STRATA: does IT leak?",
        "=" * 66,
        "energy (net-TOA drift, parent E3SM lineage, measured):",
        f"  E3SM-1-0  {pd['E3SM-1-0']['netTOA_wm2']:+.3f} W/m2   "
        f"E3SM-1-1  {pd['E3SM-1-1']['netTOA_wm2']:+.3f} W/m2",
        "  -> among the cleanest of 19 CMIP6 models (worst: +1.49 W/m2)",
        "",
        "SCREAM's physics ENFORCES energy conservation:",
        f"  check_energy.F90: column energy to {ENERGY_REL_TOL:g}, water to {WATER_REL_TOL:g},",
        "  plus a global energy FIXER that forces the budget closed every step.",
        "",
        "mass (ocean-mass drift, parent lineage):",
        f"  E3SM-1-0 {pd['E3SM-1-0']['mass_mm_per_yr']:+.3f} mm/yr (leaks)   "
        f"E3SM-1-1 {pd['E3SM-1-1']['mass_mm_per_yr']:+.3f} mm/yr (clean)",
        "",
        "the honest gaps:",
        "  - the fixer's magnitude (the raw energy error it corrects) is not published",
        "  - the nonhydrostatic km-scale core is a separate open question (GMD 2024)",
        "  - the 17-day STRATA runs cannot measure drift; raw output is ~33 TB tape",
        "",
        "VERDICT: energy is clean (enforced + parent-verified); mass leaks in the",
        "parent lineage; the km-scale drift is UNKNOWN, not clean.",
    ])


__all__ = ["ENERGY_REL_TOL", "WATER_REL_TOL", "ENERGY_TOL_WM2", "MASS_TOL_MM_PER_YR",
           "EARTH_MASS_ACCRETION_KG_PER_YR", "ACCRETION_SRC",
           "parent_drift", "mass_leak_vs_accretion_ratio", "verdict",
           "two_level_bound", "summary"]


if __name__ == "__main__":
    print(summary())
