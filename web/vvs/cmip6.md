# Valiant Verification certificate — CMIP6 model CNRM-ESM2-1 (CNRM-CERFACS)

**Format:** `valiant-verification/named-gate@1`  
**Issuer:** Pacland / Valiant Verification  
**Issued:** 2026-10-28  
**Grade:** **REFUSED**  
**Gates:** 1 of 4 pass  
**Verified:** no

| gate | result | evidence | falsifier | remedy |
|---|---|---|---|---|
| `conceptual_soundness_does_the_model_conserve_energy_in_a_control` | **fail** | Net top-of-atmosphere drift +1.485 W/m2 against a 0.1 W/m2 tolerance — fails | the failure is the finding | apply a conservation correction to the projections, or exclude the model and use the conserving five — the drift is a constant in the control run, so it is subtractable, and CMIP6 has models that do not need the correction |
| `outcomes_analysis_is_the_leak_large_compared_with_the_signal_bei` | **fail** | Exceeds the Earth's energy imbalance of 0.77 W/m2 — the signal the model exists to project | the failure is the finding | for projections where the signal is smaller than the leak, weight the ensemble toward conserving models — a 1.9x-EEI drift is larger than the effect being attributed to it |
| `data_quality_does_the_model_conserve_mass_and_salt` | **fail** | Mass drift +0.44 mm/yr sea-level equivalent (fail); salt drift -1.94e-06 (pass) | the failure is the finding | fix the failing check before relying on this claim; the falsifier names what to repair |
| `ongoing_monitoring_is_this_model_an_outlier_among_its_peers` | **pass** | 12 of 19 CMIP6 models fail the energy ledger and 5 conserve all three — the model is graded against a population, not a single threshold | not stated — this finding records a measurement without naming the failure it rules out | none — the check passes; keep the evidence and re-run on change |

**Producer:** Data: data/climate/cmip6_drift.json (Irving et al. 2021, three independent ledgers); Script: python3 scripts/issue_certificate.py --all; Module: src/pacland/climate/cmip6_drift.py

## Limitations

- Conservation drift is necessary and not sufficient: a conserving model can still be wrong about feedbacks.
- Drift is measured in the control run; behaviour under forcing is a separate test.
- Grading uses the three ledgers published by Irving et al. (2021); other consistency tests exist and are not applied here.
