# Model risk certificate — Smets–Wouters (2007) linearised DSGE

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **REFUSED**

The model solves and its units reconcile to the data, but its state is only 41% observable from its own series and its shock scales are unidentified. It cannot currently be scored out of sample, and that is the finding.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Conceptual soundness | Is the model's solution correct? | 34 equations, 34 endogenous variables; every equation vanishes at the steady state to 0.0e+00 and the solved policy satisfies the system to ~1e-13 | **satisfied** |
| Ongoing monitoring | Can the state be estimated from its own observables? | No — observability rank 14 of 34 (41%), unchanged by adding the missing wage series | **failing** |
| Outcomes analysis | Does a filter track data the model itself generated? | One-step R^2 +0.10 to +0.41 — not usable | **failing** |
| Outcomes analysis | Can the reduced form be matched to the data without a state? | Moment fit R^2 0.999 while the shock scales are recovered to only 36% — a perfect fit with unidentified parameters | **failing** |
| Conceptual soundness | Is the model identified at all? | The shock scales are not identified from five observables and two lags; the unidentified directions are structural, not a data-quantity problem | **not demonstrated** |

## Evidence

- Model: authors' Dynare file, fetched at verification time (sha256 recorded)
- Scripts: scripts/econ_sw_solve.py, scripts/econ_sw_filter.py, scripts/econ_sw_distance.py
- Modules: src/pacland/economics/sw_solve.py, sw_filter.py, sw_distance.py

## Limitations

- No out-of-sample forecast exists, so no skill comparison against the null is possible.
- Full-information Bayesian estimation with priors — what the authors used — is untested here and would change the identification result by construction.

_5 findings: 3 failing, 1 not demonstrated, 1 satisfied._
