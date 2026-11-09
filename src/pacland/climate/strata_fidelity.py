"""STRATA (NVIDIA) — a km-scale emulator, run through the two-level certificate.

STRATA (Storm-resolving Tile-based autoRegressive Atmosphere Transformer,
arXiv:2606.31248, NeurIPS 2026) is NVIDIA's first autoregressive AI emulator of
global *storm-resolving* atmosphere: trained on 17 days of SCREAM physics-model
output at 4.9 km (~25M grid cells, sampled every 10 minutes), it produces stable
24-hour global rollouts. Its headline claims are about **energy efficiency** —
48 simulation-days per megawatt-hour (~50x the SCREAM physics model) and 741
simulated days per wall-clock day on 512 H100 GPUs.

This module runs STRATA through the same two-level certificate as ACE
(``ace_fidelity.py``):

    p_*  <=  p_hat_g  +  p_hat_e  +  radius_s  +  radius_e

- ``p_hat_g`` (candidate-vs-oracle) = STRATA vs SCREAM. This is ALL the paper's
  "realistic km-scale dynamics" measures — **model vs model**.
- ``p_hat_e`` (oracle-vs-truth) = SCREAM vs the Earth. Never computed by STRATA.
- ``radius_e`` = sqrt(ln(1/delta_e) / (2m)) over the m outputs that are
  simultaneously measured + computable + validated against the Earth.

Three findings, each guarded by a test:

1. **Reference-fidelity, admitted.** STRATA validates against SCREAM, not the
   Earth, and its own abstract concedes *"large-scale biases develop with lead
   time."* That is the ACE point, at 20x finer resolution.

2. **The headline is throughput, not fidelity.** 48 sim-days/MWh and "50x
   SCREAM" measure how *cheaply* STRATA reproduces its reference — not how close
   either model is to the Earth. Efficiency of an emulator is efficiency at
   reproducing a model, not at knowing the climate.

3. **The EEI hook is missing.** STRATA's released checkpoint (``channels.json``)
   emits no top-of-atmosphere radiative flux — its diagnostics are
   ``precip_ice_surf_mass_flux``, ``precip_liq_surf_mass_flux`` and ``ps`` only.
   So the Earth energy imbalance (EEI, rsdt-rsut-rlut) — the exact quantity the
   CMIP6-drift finding shows 12/19 reference models get wrong — is **not
   computable** from the emulator's output. The anchor reality-fidelity count
   drops to **m = 1** (GMST only), *below* ACE's m = 2: the km-scale emulator
   traded the observability of the energy imbalance for resolution.

radius_e(m) at delta_e = 0.025:  m=0 -> inf (vacuous),  m=1 -> ~1.358,  m=2 -> ~0.960.

Pure stdlib + the existing pacland modules (``..deficit``). Every constant below
is from a primary source — the arXiv abstract or the released
``huggingface.co/nvidia/strata`` ``config.json`` / ``channels.json`` /
``train_config.json`` — not from memory.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..deficit import DeficitObservable, DeficitReport, deficit_report

# ---------------------------------------------------------------------------
# The released model — huggingface.co/nvidia/strata config.json / channels.json
# / train_config.json. These are the numbers the tests pin.
# ---------------------------------------------------------------------------
N_PARAMETERS = 331_664_906            # config.json "parameters"
GRID = "cubesphere ne1024pg2"
NSIDE = 2048                          # six 2048 x 2048 cube faces
N_LEVELS = 24                         # train_config level_start=8, level_end=32
TILE_SIZE = 128
TIME_STEP_MINUTES = 10

# --- the paper's own stated facts (arXiv:2606.31248 abstract) ---
TRAINING_DAYS = 17
RESOLUTION_KM = 4.9
N_GRID_CELLS = 25_000_000             # ~25 million grid cells
SAMPLING_MINUTES = 10

# --- the energy-efficiency headline (abstract) ---
SIM_DAYS_PER_MWH = 48                 # 48 simulation days per megawatt-hour
ENERGY_FACTOR_VS_SCREAM = 50          # ~50x the SCREAM physics model
SIM_DAYS_PER_WALLCLOCK_DAY = 741      # 741 simulated days per wall-clock day
H100_COUNT = 512                      # ... on 512 H100 GPUs
FLOP_FACTOR_PER_GRIDPOINT = 10        # ~10x FLOPs per grid point vs coarse AI weather models


@dataclass(frozen=True)
class StrataChannel:
    symbol: str
    description: str
    kind: str       # "prognostic" | "diagnostic"
    n_levels: int   # 24 for 3D fields (SCREAM model levels 8..31), 1 for 2D


# channels.json variables_prognostic + variables_diagnostic. The 3D fields each
# carry the full 24 model levels; T_2m and the three diagnostics are 2D.
STRATA_OUTPUT_CHANNELS: tuple[StrataChannel, ...] = (
    # prognostic — 3D (24 levels each)
    StrataChannel("PotentialTemperature", "potential temperature", "prognostic", N_LEVELS),
    StrataChannel("U", "eastward wind", "prognostic", N_LEVELS),
    StrataChannel("V", "northward wind", "prognostic", N_LEVELS),
    StrataChannel("z_mid", "geometric height at layer midpoints", "prognostic", N_LEVELS),
    StrataChannel("omega", "pressure vertical velocity", "prognostic", N_LEVELS),
    StrataChannel("qv", "specific humidity", "prognostic", N_LEVELS),
    # prognostic — 2D
    StrataChannel("T_2m", "near-surface (2 m) air temperature", "prognostic", 1),
    # diagnostic — 2D (note: NO top-of-atmosphere radiative flux)
    StrataChannel("precip_ice_surf_mass_flux", "surface ice precipitation flux", "diagnostic", 1),
    StrataChannel("precip_liq_surf_mass_flux", "surface liquid precipitation flux", "diagnostic", 1),
    StrataChannel("ps", "surface pressure", "diagnostic", 1),
)

# channels.json variables_forcing — inputs, not emulated outputs.
STRATA_FORCING: tuple[str, ...] = ("coszr", "phis", "sgh30", "landfrac")


def channel_summary() -> dict:
    """The raw variable counts, the layer-expanded channel count, and model size."""
    n_prog_vars = sum(1 for c in STRATA_OUTPUT_CHANNELS if c.kind == "prognostic")
    n_diag_vars = sum(1 for c in STRATA_OUTPUT_CHANNELS if c.kind == "diagnostic")
    n_prog_channels = sum(c.n_levels for c in STRATA_OUTPUT_CHANNELS if c.kind == "prognostic")
    n_diag_channels = sum(c.n_levels for c in STRATA_OUTPUT_CHANNELS if c.kind == "diagnostic")
    return {
        "n_prognostic_vars": n_prog_vars,
        "n_diagnostic_vars": n_diag_vars,
        "n_forcing_vars": len(STRATA_FORCING),
        "n_levels": N_LEVELS,
        # the ACE convention: a 3D field contributes one channel per level
        "n_prognostic_channels": n_prog_channels,
        "n_diagnostic_channels": n_diag_channels,
        "n_outputs": n_prog_channels + n_diag_channels,
        "n_parameters": N_PARAMETERS,
        "resolution_km": RESOLUTION_KM,
        "n_grid_cells": N_GRID_CELLS,
    }


def eei_computable() -> bool:
    """Whether the Earth energy imbalance can be computed from STRATA's output.

    The released checkpoint's diagnostics are precipitation (ice + liquid) and
    surface pressure only — no upward/downward shortwave or longwave flux — so
    EEI (rsdt - rsut - rlut) is not computable from it.
    """
    for c in STRATA_OUTPUT_CHANNELS:
        s = c.symbol.lower()
        if "toa" in s or "radiative" in s or s.startswith(("uswrf", "ulwrf", "dswrf", "dlwrf")):
            return True
    return False


# ---------------------------------------------------------------------------
# Reality-fidelity classification (generous tier: grant the reference model's
# Earth-validation, as ACE does). The standard is docs/climate-observables.md.
# ---------------------------------------------------------------------------
# name,                       measured, computable, validated
STRATA_REALITY_OBSERVABLES: tuple[DeficitObservable, ...] = (
    # counted toward m — measured + computable + validated on the record
    DeficitObservable("GMST (near-surface air temperature, T_2m)", True, True, True),
    DeficitObservable("surface pressure (ps)", True, True, True),
    # measured + computable, NOT validated on the record
    DeficitObservable("upper-air temperature profile (PotentialTemperature)", True, True, False),
    DeficitObservable("specific humidity (qv)", True, True, False),
    DeficitObservable("horizontal wind (U, V)", True, True, False),
    DeficitObservable("geopotential height (z_mid)", True, True, False),
    DeficitObservable("surface precipitation (liquid + ice)", True, True, False),
    # computable only — no global direct observation
    DeficitObservable("pressure vertical velocity (omega)", False, True, False),
    # measured but NOT computable — the sharp findings
    DeficitObservable("EEI (net top-of-atmosphere radiative flux)", True, False, False),
    DeficitObservable("OHC (ocean heat content 0-2000 m)", True, False, False),
    DeficitObservable("GMSL (global-mean sea level)", True, False, False),
)

# The climate discipline's four headline anchors, mapped onto STRATA's output.
# EEI, OHC and GMSL are not computable from an atmosphere-only emulator that
# also emits no TOA flux — so only GMST survives.
STRATA_ANCHOR_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("GMST (near-surface air temperature)", True, True, True),
    DeficitObservable("EEI (net TOA radiative flux)", True, False, False),
    DeficitObservable("OHC (ocean heat content)", True, False, False),
    DeficitObservable("GMSL (global-mean sea level)", True, False, False),
)


def reality_deficit(delta_e: float = 0.025) -> DeficitReport:
    """Generous tier: m over STRATA's full reality-fidelity observable mapping."""
    return deficit_report(STRATA_REALITY_OBSERVABLES, delta_e)


def anchor_deficit(delta_e: float = 0.025) -> DeficitReport:
    """Anchor tier: the climate discipline's four headline observables on STRATA."""
    return deficit_report(STRATA_ANCHOR_OBSERVABLES, delta_e)


def efficiency_summary() -> dict:
    """The energy-efficiency headline, and the point that it is not fidelity."""
    return {
        "sim_days_per_mwh": SIM_DAYS_PER_MWH,
        "energy_factor_vs_scream": ENERGY_FACTOR_VS_SCREAM,
        "sim_days_per_wallclock_day": SIM_DAYS_PER_WALLCLOCK_DAY,
        "h100_count": H100_COUNT,
        "flop_factor_per_gridpoint": FLOP_FACTOR_PER_GRIDPOINT,
        "verdict": (
            "throughput is not fidelity: 48 sim-days/MWh measures how cheaply STRATA "
            "reproduces SCREAM, not how close either model is to the Earth"
        ),
    }


def two_level_bound(delta_e: float = 0.025) -> str:
    """The two-level certificate, with the one computable term filled in."""
    r = reality_deficit(delta_e)
    a = anchor_deficit(delta_e)
    ee = "computable" if eei_computable() else "NOT computable (no TOA flux output)"
    return (
        "TWO-LEVEL CERTIFICATE  p_* <= p_hat_g + p_hat_e + radius_s + radius_e\n"
        f"  p_hat_g  = STRATA vs SCREAM (reference-fidelity; the 'realistic km-scale "
        f"dynamics' claim) — model vs model\n"
        f"  p_hat_e  = SCREAM vs the Earth — never computed by STRATA\n"
        f"  EEI      = {ee}\n"
        f"  radius_s = finite-sample term over the {channel_summary()['n_outputs']} "
        f"scalar channels (small at n={channel_summary()['n_outputs']})\n"
        f"  radius_e = sqrt(ln(1/{delta_e})/(2m)):\n"
        f"      m = {a.n_validation} (anchor, GMST only)     -> {a.radius:.3f}\n"
        f"      m = {r.n_validation} (generous, +p_s)         -> {r.radius:.3f}\n"
        f"      m = 0 (strict, no Earth validation)      -> inf (vacuous)"
    )


def summary() -> str:
    """One plain-text block for the record (and the report's headline)."""
    cs = channel_summary()
    r = reality_deficit()
    a = anchor_deficit()
    e = efficiency_summary()
    return "\n".join([
        "STRATA (NVIDIA) — km-scale emulator, reference-fidelity is not reality-fidelity",
        "=" * 72,
        f"model                 pixeldit, {cs['n_parameters']:,} parameters, {cs['resolution_km']} km",
        f"output channels       {cs['n_outputs']} "
        f"({cs['n_prognostic_channels']} prognostic + {cs['n_diagnostic_channels']} diagnostic, "
        f"{cs['n_levels']} levels)",
        f"                      = {cs['n_prognostic_vars']} prognostic + "
        f"{cs['n_diagnostic_vars']} diagnostic variables (forcings: {cs['n_forcing_vars']})",
        "  -> validated against SCREAM (model vs model), never against the Earth",
        "",
        "energy headline       " + f"{e['sim_days_per_mwh']} sim-days/MWh "
        f"({e['energy_factor_vs_scream']}x SCREAM), "
        f"{e['sim_days_per_wallclock_day']} sim-days/day @ {e['h100_count']} H100",
        "  -> throughput, not fidelity: cheaply reproducing a model is not knowing the climate",
        "",
        "EEI                   not computable — the released checkpoint emits no TOA flux",
        "  -> the one diagnostic that would catch the CMIP6-drift leak is absent",
        "",
        "reality-fidelity (the missing p_hat_e term), radius_e = sqrt(ln(1/d)/2m):",
        f"  strict    m = 0   STRATA validated against no Earth observation  -> inf",
        f"  anchor    m = {a.n_validation}   GMST only (EEI/OGC/GMSL not computable)   "
        f"-> {a.radius:.3f}",
        f"  generous  m = {r.n_validation}   GMST + surface pressure                        "
        f"-> {r.radius:.3f}",
        "",
        "A km-scale emulator that cannot even be checked against the energy imbalance",
        "is finer, not truer — reference-fidelity to a leaky reference is fidelity to a defect.",
    ])


if __name__ == "__main__":
    print(summary())
