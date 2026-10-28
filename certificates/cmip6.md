# Model risk certificate — CMIP6 model CNRM-ESM2-1 (CNRM-CERFACS)

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **REFUSED**

In a pre-industrial control, where the climate must be stationary, this model drifts +1.49 W/m2 — 1.9x the Earth's energy imbalance that its projections are meant to represent.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Conceptual soundness | Does the model conserve energy in a control climate? | Net top-of-atmosphere drift +1.485 W/m2 against a 0.1 W/m2 tolerance — fails | **failing** |
| Outcomes analysis | Is the leak large compared with the signal being measured? | Exceeds the Earth's energy imbalance of 0.77 W/m2 — the signal the model exists to project | **failing** |
| Data quality | Does the model conserve mass and salt? | Mass drift +0.44 mm/yr sea-level equivalent (fail); salt drift -1.94e-06 (pass) | **failing** |
| Ongoing monitoring | Is this model an outlier among its peers? | 12 of 19 CMIP6 models fail the energy ledger and 5 conserve all three — the model is graded against a population, not a single threshold | **satisfied** |

## Evidence

- Data: data/climate/cmip6_drift.json (Irving et al. 2021, three independent ledgers)
- Script: python3 scripts/issue_certificate.py --all
- Module: src/pacland/climate/cmip6_drift.py

## Limitations

- Conservation drift is necessary and not sufficient: a conserving model can still be wrong about feedbacks.
- Drift is measured in the control run; behaviour under forcing is a separate test.
- Grading uses the three ledgers published by Irving et al. (2021); other consistency tests exist and are not applied here.

_4 findings: 3 failing, 1 satisfied._
