# Valiant Verification certificate — CMIP6 model CNRM-ESM2-1 (CNRM-CERFACS)

**Format:** `valiant-verification/named-gate@1`  
**Issuer:** Pacland / Valiant Verification  
**Issued:** 2026-10-28  
**Grade:** **REFUSED**  
**Gates:** 1 of 4 pass  
**Verified:** no

| gate | result | evidence | falsifier |
|---|---|---|---|
| `conceptual_soundness_does_the_model_conserve_energy_in_a_control` | **fail** | Net top-of-atmosphere drift +1.485 W/m2 against a 0.1 W/m2 tolerance — fails | the failure is the finding |
| `outcomes_analysis_is_the_leak_large_compared_with_the_signal_bei` | **fail** | Exceeds the Earth's energy imbalance of 0.77 W/m2 — the signal the model exists to project | the failure is the finding |
| `data_quality_does_the_model_conserve_mass_and_salt` | **fail** | Mass drift +0.44 mm/yr sea-level equivalent (fail); salt drift -1.94e-06 (pass) | the failure is the finding |
| `ongoing_monitoring_is_this_model_an_outlier_among_its_peers` | **pass** | 12 of 19 CMIP6 models fail the energy ledger and 5 conserve all three — the model is graded against a population, not a single threshold | not stated — this finding records a measurement without naming the failure it rules out |

**Producer:** Data: data/climate/cmip6_drift.json (Irving et al. 2021, three independent ledgers); Script: python3 scripts/issue_certificate.py --all; Module: src/pacland/climate/cmip6_drift.py

## Limitations

- Conservation drift is necessary and not sufficient: a conserving model can still be wrong about feedbacks.
- Drift is measured in the control run; behaviour under forcing is a separate test.
- Grading uses the three ledgers published by Irving et al. (2021); other consistency tests exist and are not applied here.
