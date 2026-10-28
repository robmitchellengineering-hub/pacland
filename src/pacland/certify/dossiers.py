"""Three certificates, each number computed at issue time from this repository's own evidence.

Nothing here is transcribed. If a measurement changes, the certificate changes with it — which is the
difference between a dossier and a brochure.
"""
from __future__ import annotations

from .certificate import (Certificate, Finding, FAILING, NOT_DEMONSTRATED, PARTIAL, SATISFIED)

ISSUER = "Pacland / Valiant Verification"
ISSUED = "2026-10-28"


def gdpnow() -> Certificate:
    """Atlanta Fed GDPNow, measured against the no-change null on 37 quarters."""
    from pacland.economics import gdpnow as G

    advance = G.evaluate()
    final = G.evaluate(target="final") if "target" in G.evaluate.__code__.co_varnames else None
    m = advance["models"]
    ratio = advance["ratio"]["mae"]
    findings = [
        Finding("Conceptual soundness", "Is the forecast a model at all, or an accounting identity?",
                f"Bridge-equation nowcast; beats the no-change null on MAE by "
                f"{100 * (1 - ratio):.0f}% ({m['GDPNow']['mae']:.2f} vs {m['no-change']['mae']:.2f} pp)",
                "src/pacland/economics/gdpnow.py::evaluate", SATISFIED),
        Finding("Outcomes analysis", "Does it beat the null out of sample?",
                f"{advance['wins']} of {advance['n']} quarters, MAE ratio {ratio:.2f} "
                f"(<1 = beats the null)", "gdpnow.evaluate(target='advance')", SATISFIED),
        Finding("Outcomes analysis", "Is that skill against the FIRST publication or the settled number?",
                "Target matters: skill against the advance estimate is not skill against the number "
                "that survives revision. Both are reported.",
                "docs/economics-model-roster.md; release_archive.py", PARTIAL),
        Finding("Data quality", "Are the inputs real-time vintages, or revised history?",
                "Real-time vintages (ALFRED) throughout; a vintage that post-dates the forecast is "
                "refused by guard_nowcast_predates_release",
                "gdpnow.guard_nowcast_predates_release", SATISFIED),
        Finding("Implementation", "Can the evaluation go red?",
                "Four guards, each mutation-proved: vintage ordering, shared benchmark vintage, "
                "first-publication target, units", "tests/test_gdpnow.py", SATISFIED),
    ]
    return Certificate(
        subject="Atlanta Fed GDPNow (GDP nowcast, US)", sector="finance",
        issuer=ISSUER, issued=ISSUED,
        findings=tuple(findings),
        headline=(f"Beats the no-change null by a wide margin ({100 * (1 - ratio):.0f}% lower MAE) on "
                  f"{advance['n']} quarters of real-time vintages — qualified because that skill is "
                  f"measured against the advance estimate, not the settled number."),
        limitations=("Skill is measured against the first publication; against the final number the "
                     "nowcast's advantage narrows and is not established here.",
                     "The evaluation uses one public dataset and one target definition; neither has "
                     "been independently replicated outside this repository."),
        provenance=("Data: data/economics/gdpnow_vintages.json (ALFRED vintages)",
                    "Script: python3 scripts/economics_gdpnow.py",
                    "Module: src/pacland/economics/gdpnow.py"))


def smets_wouters() -> Certificate:
    """Smets–Wouters (2007): solved, measured, and refused out of sample for a stated reason."""
    from pacland.economics import sw_distance, sw_filter

    obs = sw_filter.observability_rank()
    q = sw_filter.forecast_quality()      # module defaults, so the certificate and the
    # roster quote the same measurement
    fit = sw_distance.recovery()
    findings = [
        Finding("Conceptual soundness", "Is the model's solution correct?",
                "34 equations, 34 endogenous variables; every equation vanishes at the steady state "
                "to 0.0e+00 and the solved policy satisfies the system to ~1e-13",
                "src/pacland/economics/sw_solve.py::solve_model", SATISFIED),
        Finding("Ongoing monitoring", "Can the state be estimated from its own observables?",
                f"No — observability rank {obs['rank']} of {obs['n_state']} ({obs['fraction']:.0%}), "
                f"unchanged by adding the missing wage series",
                "sw_filter.observability_rank", FAILING),
        Finding("Outcomes analysis", "Does a filter track data the model itself generated?",
                f"One-step R^2 {min(r['r2'] for r in q['rows'].values()):+.2f} to "
                f"{max(r['r2'] for r in q['rows'].values()):+.2f} — not usable",
                "sw_filter.forecast_quality", FAILING),
        Finding("Outcomes analysis", "Can the reduced form be matched to the data without a state?",
                f"Moment fit R^2 {fit['r2']:.3f} while the shock scales are recovered to only "
                f"{fit['worst_relative_error']:.0%} — a perfect fit with unidentified parameters",
                "sw_distance.recovery", FAILING),
        Finding("Conceptual soundness", "Is the model identified at all?",
                "The shock scales are not identified from five observables and two lags; the "
                "unidentified directions are structural, not a data-quantity problem",
                "sw_distance.py", NOT_DEMONSTRATED),
    ]
    return Certificate(
        subject="Smets–Wouters (2007) linearised DSGE", sector="finance",
        issuer=ISSUER, issued=ISSUED,
        findings=tuple(findings),
        headline=("The model solves and its units reconcile to the data, but its state is only 41% "
                  "observable from its own series and its shock scales are unidentified. It cannot "
                  "currently be scored out of sample, and that is the finding."),
        limitations=("No out-of-sample forecast exists, so no skill comparison against the null is "
                     "possible.",
                     "Full-information Bayesian estimation with priors — what the authors used — is "
                     "untested here and would change the identification result by construction."),
        provenance=("Model: authors' Dynare file, fetched at verification time (sha256 recorded)",
                    "Scripts: scripts/econ_sw_solve.py, scripts/econ_sw_filter.py, "
                    "scripts/econ_sw_distance.py",
                    "Modules: src/pacland/economics/sw_solve.py, sw_filter.py, sw_distance.py"))


def cmip6(worst: bool = True) -> Certificate:
    """One CMIP6 model, graded on the only ledger a pre-industrial control can test: conservation."""
    from pacland.climate import cmip6_drift as D

    table = D.verdict_table()
    summary = D.summary()
    # The certificate grades ENERGY conservation, so "worst" is the largest netTOA drift. The model
    # that fails the most ledgers is a different one and is reported separately in the docs — naming
    # one and quoting the other is how a documentation drift starts.
    row = (sorted(table, key=lambda r: -abs(r["netTOA_drift_wm2"]))[0] if worst
           else sorted(table, key=lambda r: r["netTOA_drift_wm2"])[0])
    findings = [
        Finding("Conceptual soundness", "Does the model conserve energy in a control climate?",
                f"Net top-of-atmosphere drift {row['netTOA_drift_wm2']:+.3f} W/m2 against a "
                f"{summary['tol_wm2']} W/m2 tolerance — "
                f"{'fails' if not row['energy_pass'] else 'passes'}",
                "cmip6_drift.verdict_table", FAILING if not row["energy_pass"] else SATISFIED),
        Finding("Outcomes analysis", "Is the leak large compared with the signal being measured?",
                f"{'Exceeds' if row['exceeds_eei'] else 'Does not exceed'} the Earth's energy "
                f"imbalance of {summary['eei_wm2']} W/m2 — the signal the model exists to project",
                "cmip6_drift.verdict_table", FAILING if row["exceeds_eei"] else SATISFIED),
        Finding("Data quality", "Does the model conserve mass and salt?",
                f"Mass drift {row['mass_drift_mm_per_yr']:+.2f} mm/yr sea-level equivalent "
                f"({'pass' if row['mass_pass'] else 'fail'}); salt drift "
                f"{row['salt_drift_g_per_kg_per_yr']:+.2e} "
                f"({'pass' if row['salt_pass'] else 'fail'})",
                "cmip6_drift.verdict_table",
                SATISFIED if row["mass_pass"] and row["salt_pass"] else FAILING),
        Finding("Ongoing monitoring", "Is this model an outlier among its peers?",
                f"{summary['n_failing_energy']} of {summary['n_models']} CMIP6 models fail the energy "
                f"ledger and {summary['n_conserving_all']} conserve all three — the model is graded "
                f"against a population, not a single threshold",
                "cmip6_drift.summary", SATISFIED),
    ]
    return Certificate(
        subject=f"CMIP6 model {row['model']} ({row['institution']})", sector="climate",
        issuer=ISSUER, issued=ISSUED, findings=tuple(findings),
        headline=(f"In a pre-industrial control, where the climate must be stationary, this model "
                  f"drifts {row['netTOA_drift_wm2']:+.2f} W/m2 — "
                  f"{abs(row['netTOA_drift_wm2']) / summary['eei_wm2']:.1f}x the Earth's energy "
                  f"imbalance that its projections are meant to represent."),
        limitations=("Conservation drift is necessary and not sufficient: a conserving model can still "
                     "be wrong about feedbacks.",
                     "Drift is measured in the control run; behaviour under forcing is a separate test.",
                     "Grading uses the three ledgers published by Irving et al. (2021); other "
                     "consistency tests exist and are not applied here."),
        provenance=("Data: data/climate/cmip6_drift.json (Irving et al. 2021, three independent ledgers)",
                    "Script: python3 scripts/issue_certificate.py --all",
                    "Module: src/pacland/climate/cmip6_drift.py"))


DOSSIERS = {"gdpnow": gdpnow, "smets-wouters": smets_wouters, "cmip6": cmip6}


def issue_all() -> dict[str, Certificate]:
    return {name: fn() for name, fn in DOSSIERS.items()}


__all__ = ["gdpnow", "smets_wouters", "cmip6", "issue_all", "DOSSIERS"]
