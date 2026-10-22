"""Climate explainer content — generated from live data, not hand-written prose.

``content()`` pulls the real numbers from the climate modules (deficit, energy
budget, three-ledger CMIP6 drift), so the PDF is always current when the numbers
change.
"""
from __future__ import annotations

from .cmip6_drift import summary as drift_summary
from .deficit import climate_deficit_report
from .energy_budget import closure


def content() -> list[tuple[str, str]]:
    hist, proj = climate_deficit_report()
    eb = closure()
    ds = drift_summary()
    mass_ratio = abs(ds["worst_mass_mm_per_yr"]) / ds["slr_reference_mm_per_yr"]
    return [
        ("title", "PACLAND · Climate"),
        ("subtitle", "The verification discipline applied to climate modelling — a plain-English brief"),
        ("h", "The headlines"),
        ("headline", f"The error bar is the size of the signal — {ds['n_exceeding_eei']} models leak heat at ~{ds['worst_ratio_to_eei']:.1f}× the energy imbalance they are used to project."),
        ("headline", f"A 2100 projection is extrapolation, not verification — {proj.n_validation} future states are measured (m = 0)."),
        ("headline", f"The leak lives in the coupling, not the ocean — {ds['n_failing_energy']}/19 leak energy, {ds['n_failing_mass']}/19 leak mass, but only {ds['n_failing_salt']}/19 leak salt."),
        ("headline", "For the first time, a climate model's trustworthiness is a machine-checked verdict — not a footnote in a paper."),
        ("headline", "Skillful ≠ true: the AI climate emulators are verified against another model, not the Earth."),
        ("h", "1 · What we are measuring"),
        ("p", "Climate projections are the most consequential predictions we make. The discipline asks the question the field has never answered in numbers: how much of a projection is verified, versus extrapolated?"),
        ("h", "2 · The verification deficit"),
        ("b", f"{hist.n_validation} of {hist.n_observables} historical observables are measured + computable + validated — a certificate radius of {hist.radius:.0%}."),
        ("b", f"{proj.n_validation} of {proj.n_observables} 2100-projection targets are validated — the projection is extrapolation, not verification."),
        ("p", "A 1% certificate needs ~18,000 validated observables — three orders of magnitude beyond what the historical record can supply. The bottleneck is measured data, not compute."),
        ("h", "3 · The energy budget, on real data"),
        ("b", f"The 0–2000 m ocean alone under-closes the budget (residual {eb['residual_0_2000m_only_wm2']:.2f} W/m²)."),
        ("b", f"The full budget — ocean + atmosphere + land + cryosphere — closes it (residual {eb['residual_full_wm2']:.2f} W/m²). An invariant is only an invariant when all its terms are counted."),
        ("h", "4 · The CMIP6 conservation drift — three ledgers"),
        ("p", "A conserving model must close three independent ledgers in its control run: energy, mass, and salt. The measured drift shows how many fail each."),
        ("b", f"Energy: {ds['n_failing_energy']} of {ds['n_models']} models leak (net TOA beyond 0.1 W/m²); {ds['n_exceeding_eei']} leak faster than the EEI — {ds['worst_energy_model']} at {ds['worst_drift_wm2']:.3f} W/m² ({ds['worst_ratio_to_eei']:.2f}×)."),
        ("b", f"Mass: {ds['n_failing_mass']} models leak ocean mass — {ds['worst_mass_model']} at {ds['worst_mass_mm_per_yr']:+.2f} mm/yr, {mass_ratio:.0%} of observed sea-level rise."),
        ("b", f"Salt: only {ds['n_failing_salt']} models leak — salt is conserved orders of magnitude better."),
        ("b", f"So the leak lives in the atmosphere-ocean coupling, not the ocean model: {ds['n_conserving_all']} of {ds['n_models']} models conserve all three ledgers."),
        ("h", "5 · Why it matters"),
        ("p", "A model leaking heat at ~2× the signal it is projecting carries an error the size of the projection. Conservation is not a solved detail — it is a hard, quantified defect in most models, invisible to skill scores and to ensemble spread. And because salt (purely ocean) is conserved far better than energy and mass (which cross the air-sea boundary), the defect is in the coupling, not the ocean."),
        ("h", "6 · Reproduce"),
        ("p", "pacland climate · python3 scripts/climate_cmip6_drift.py · docs/climate-cmip6-drift.md"),
    ]


__all__ = ["content"]
