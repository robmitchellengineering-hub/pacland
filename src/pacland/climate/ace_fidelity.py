"""ACE worked example — reference-fidelity is not reality-fidelity (citable report).

ACE (AI2 Climate Emulator, arXiv:2310.02074) reports that it "faithfully
reproduces the reference model's climate, outperforming a challenging baseline on
over 90% of tracked variables." This module makes the two-level certificate
explicit for that claim:

    p_*  <=  p_hat_g  +  p_hat_e  +  radius_s  +  radius_e

- ``p_hat_g`` (candidate-vs-oracle) = ACE vs its reference GCM (FV3GFS). This is
  the ONLY thing ">90% of tracked variables" measures — **model vs model**.
- ``p_hat_e`` (oracle-vs-truth) = FV3GFS vs the Earth. Never computed; for a
  100-year projection it cannot be (the future has no ground truth).
- ``radius_e`` = sqrt(ln(1/delta_e) / (2 m)) over the m outputs that are
  simultaneously measured + computable + validated against the Earth on the
  historical record.

ACE is an **atmosphere-only** emulator, so its reachable reality-fidelity is a
subset of the climate discipline's m=4 anchor set (GMST, EEI, OHC, GMSL): it
outputs GMST (T7) and EEI (the TOA radiative fluxes) plus surface pressure, but
structurally cannot output OHC or GMSL. The three honest tiers:

    strict    m = 0  — ACE's own paper validates it against FV3GFS, never Earth
    anchor    m = 2  — GMST + EEI, of the four headline climate observables
    generous  m = 3  — GMST + EEI + surface pressure (best-observed field)

radius_e(m) at delta_e = 0.025:  m=0 -> inf (vacuous),  m=2 -> ~0.960,  m=3 -> ~0.784.

Headline: climate "verification" today certifies a model against another model,
not against the Earth — and the ">90% skillful" claim is a model-vs-model number
whose reality-fidelity term is, at best, a ~78% tolerance on 3 observables.

Pure stdlib + the existing pacland modules (``..deficit``).
"""
from __future__ import annotations

from dataclasses import dataclass

from ..deficit import DeficitObservable, DeficitReport, deficit_report

# ---------------------------------------------------------------------------
# ACE's 44 output channels (arXiv:2310.02074, Table 1).
# Prognostic = input AND output (autoregressive); diagnostic = output only.
# The 3D fields (T, q, u, v) each carry 8 vertical layers -> 8 channels.
# ---------------------------------------------------------------------------
N_LAYERS_3D = 8


@dataclass(frozen=True)
class AceChannel:
    symbol: str
    description: str
    kind: str      # "prognostic" | "diagnostic"
    n_layers: int  # channels contributed (8 for 3D fields, else 1)


ACE_OUTPUT_CHANNELS: tuple[AceChannel, ...] = (
    # prognostic — 3D (8 layers each)
    AceChannel("T_k", "air temperature", "prognostic", N_LAYERS_3D),
    AceChannel("q^T_k", "specific total water (vapour + condensates)", "prognostic", N_LAYERS_3D),
    AceChannel("u_k", "eastward wind", "prognostic", N_LAYERS_3D),
    AceChannel("v_k", "northward wind", "prognostic", N_LAYERS_3D),
    # prognostic — 2D
    AceChannel("T_s", "skin temperature (land / sea-ice)", "prognostic", 1),
    AceChannel("p_s", "surface pressure", "prognostic", 1),
    # diagnostic — TOA radiation (the EEI)
    AceChannel("USWRF_toa", "upward shortwave radiative flux at TOA", "diagnostic", 1),
    AceChannel("ULWRF_toa", "upward longwave radiative flux at TOA", "diagnostic", 1),
    # diagnostic — surface radiation
    AceChannel("USWRF_sfc", "upward shortwave radiative flux at surface", "diagnostic", 1),
    AceChannel("ULWRF_sfc", "upward longwave radiative flux at surface", "diagnostic", 1),
    AceChannel("DSWRF_sfc", "downward shortwave radiative flux at surface", "diagnostic", 1),
    AceChannel("DLWRF_sfc", "downward longwave radiative flux at surface", "diagnostic", 1),
    # diagnostic — precipitation
    AceChannel("P", "surface precipitation rate", "diagnostic", 1),
    # diagnostic — derived / not directly observed
    AceChannel("dTWP/dt|_adv", "total-water-path tendency from advection", "diagnostic", 1),
    AceChannel("LHF", "surface latent heat flux", "diagnostic", 1),
    AceChannel("SHF", "surface sensible heat flux", "diagnostic", 1),
)

# "41 out of 44 output variables have a lower time-mean RMSE for ACE compared to
# the baseline" (arXiv:2310.02074, Appendix E). This is the ">90% of tracked
# variables" of the abstract, and it is candidate-vs-oracle (model-vs-model):
# the "reference" is the FV3GFS GCM and the "baseline" is a 2x-coarser FV3GFS.
N_BEATS_BASELINE = 41

# ---------------------------------------------------------------------------
# Reality-fidelity classification.
#
# Each entry maps ACE's output onto a *physical observable* and asks the pacland
# deficit's question against the EARTH (not the reference model): is there an
# independent observation c*, does ACE compute O(x), and has it been validated
# on the historical record? The standard is docs/climate-observables.md.
# ---------------------------------------------------------------------------
# name,                       measured, computable, validated
ACE_REALITY_OBSERVABLES: tuple[DeficitObservable, ...] = (
    # counted toward m — measured + computable + validated on the record
    DeficitObservable("GMST (near-surface air temperature, T7)", True, True, True),
    DeficitObservable("EEI (net top-of-atmosphere radiative flux)", True, True, True),
    DeficitObservable("surface pressure (p_s)", True, True, True),
    # measured + computable, NOT validated on the record
    DeficitObservable("upper-air temperature profile (T_k, k<7)", True, True, False),
    DeficitObservable("specific total water (q^T)", True, True, False),
    DeficitObservable("horizontal wind (u, v)", True, True, False),
    DeficitObservable("skin temperature (T_s)", True, True, False),
    DeficitObservable("surface radiative fluxes (SW/LW)", True, True, False),
    DeficitObservable("surface precipitation (P)", True, True, False),
    # computable only — no global direct observation exists
    DeficitObservable("TWP advection tendency", False, True, False),
    DeficitObservable("surface turbulent fluxes (LHF, SHF)", False, True, False),
    # measured but NOT computable by an atmosphere-only model
    DeficitObservable("OHC (ocean heat content 0-2000 m)", True, False, False),
    DeficitObservable("GMSL (global-mean sea level)", True, False, False),
)

# The climate discipline's four headline anchors, mapped onto ACE's output.
# OHC and GMSL are structurally absent from an atmosphere-only emulator.
ACE_ANCHOR_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("GMST (near-surface air temperature)", True, True, True),
    DeficitObservable("EEI (net TOA radiative flux)", True, True, True),
    DeficitObservable("OHC (ocean heat content)", True, False, False),
    DeficitObservable("GMSL (global-mean sea level)", True, False, False),
)


def channel_summary() -> dict:
    """The raw channel counts and the model-vs-model skill claim."""
    n_prog = sum(c.n_layers for c in ACE_OUTPUT_CHANNELS if c.kind == "prognostic")
    n_diag = sum(c.n_layers for c in ACE_OUTPUT_CHANNELS if c.kind == "diagnostic")
    n_total = n_prog + n_diag
    return {
        "n_outputs": n_total,
        "n_prognostic": n_prog,
        "n_diagnostic": n_diag,
        "n_beats_baseline": N_BEATS_BASELINE,
        "reference_fidelity_pct": N_BEATS_BASELINE / n_total,
    }


def reality_deficit(delta_e: float = 0.025) -> DeficitReport:
    """Generous tier: m over ACE's full reality-fidelity observable mapping."""
    return deficit_report(ACE_REALITY_OBSERVABLES, delta_e)


def anchor_deficit(delta_e: float = 0.025) -> DeficitReport:
    """Anchor tier: the climate discipline's four headline observables on ACE."""
    return deficit_report(ACE_ANCHOR_OBSERVABLES, delta_e)


def two_level_bound(delta_e: float = 0.025) -> str:
    """The two-level certificate, with the one computable term filled in."""
    r = reality_deficit(delta_e)
    a = anchor_deficit(delta_e)
    return (
        "TWO-LEVEL CERTIFICATE  p_* <= p_hat_g + p_hat_e + radius_s + radius_e\n"
        f"  p_hat_g  = ACE vs FV3GFS (reference-fidelity; the '>90%' claim) — "
        f"model vs model\n"
        f"  p_hat_e  = FV3GFS vs the Earth — never computed by ACE\n"
        f"  radius_s = finite-sample term over the {channel_summary()['n_outputs']} "
        f"scored channels (small at n={channel_summary()['n_outputs']})\n"
        f"  radius_e = sqrt(ln(1/{delta_e})/(2m)):\n"
        f"      m = {a.n_validation} (anchor, GMST+EEI)  -> {a.radius:.3f}\n"
        f"      m = {r.n_validation} (generous, +p_s)    -> {r.radius:.3f}\n"
        f"      m = 0 (strict, no Earth validation)     -> inf (vacuous)"
    )


def summary() -> str:
    """One plain-text block for the record (and the report's headline)."""
    cs = channel_summary()
    r = reality_deficit()
    a = anchor_deficit()
    return "\n".join([
        "ACE WORKED EXAMPLE — reference-fidelity is not reality-fidelity",
        "=" * 56,
        f"output channels       {cs['n_outputs']} "
        f"({cs['n_prognostic']} prognostic + {cs['n_diagnostic']} diagnostic)",
        f"'>90% of tracked'     {cs['n_beats_baseline']}/{cs['n_outputs']} = "
        f"{cs['reference_fidelity_pct']:.1%} beat a coarser FV3GFS baseline",
        "  -> that is candidate-vs-oracle (model vs model), never vs the Earth",
        "",
        "reality-fidelity (the missing p_hat_e term), radius_e = sqrt(ln(1/d)/2m):",
        f"  strict    m = 0   ACE validated against no Earth observation  -> inf",
        f"  anchor    m = {a.n_validation}   GMST + EEI (atmosphere-only, no OHC/GMSL) "
        f"-> {a.radius:.3f}",
        f"  generous  m = {r.n_validation}   GMST + EEI + surface pressure          "
        f"-> {r.radius:.3f}",
        "",
        "A climate 'verification' that certifies a model against another model,",
        "not against the Earth, is no verification of the climate.",
    ])


if __name__ == "__main__":
    print(summary())
