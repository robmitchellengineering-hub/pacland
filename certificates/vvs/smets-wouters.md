# Valiant Verification certificate — Smets–Wouters (2007) linearised DSGE

**Format:** `valiant-verification/named-gate@1`  
**Issuer:** Pacland / Valiant Verification  
**Issued:** 2026-10-28  
**Grade:** **REFUSED**  
**Gates:** 1 of 5 pass  
**Verified:** no

| gate | result | evidence | falsifier | remedy |
|---|---|---|---|---|
| `conceptual_soundness_is_the_model_s_solution_correct` | **pass** | 34 equations, 34 endogenous variables; every equation vanishes at the steady state to 0.0e+00 and the solved policy satisfies the system to ~1e-13 | not stated — this finding records a measurement without naming the failure it rules out | none — the check passes; keep the evidence and re-run on change |
| `ongoing_monitoring_can_the_state_be_estimated_from_its_own_obser` | **fail** | No — observability rank 14 of 34 (41%), unchanged by adding the missing wage series | the failure is the finding | estimate the unobserved block with PRIORS rather than from the data — full-information Bayesian estimation is what the authors themselves used, and it converts the 20 unidentified directions into prior-weighted ones |
| `outcomes_analysis_does_a_filter_track_data_the_model_itself_gene` | **fail** | One-step R^2 +0.10 to +0.41 — not usable | the failure is the finding | do not run a plain filter on this model; the fix is a prior on the state, not a better filter |
| `outcomes_analysis_can_the_reduced_form_be_matched_to_the_data_wi` | **fail** | Moment fit R^2 0.999 while the shock scales are recovered to only 36% — a perfect fit with unidentified parameters | the failure is the finding | add independent series (a 7-8 observable dataset) or shrink the shock scales toward the posterior — with five series the second moments cannot separate seven shocks |
| `conceptual_soundness_is_the_model_identified_at_all` | **fail** | The shock scales are not identified from five observables and two lags; the unidentified directions are structural, not a data-quantity problem | the failure is the finding | fix the failing check before relying on this claim; the falsifier names what to repair |

**Producer:** Model: authors' Dynare file, fetched at verification time (sha256 recorded); Scripts: scripts/econ_sw_solve.py, scripts/econ_sw_filter.py, scripts/econ_sw_distance.py; Modules: src/pacland/economics/sw_solve.py, sw_filter.py, sw_distance.py

## Limitations

- No out-of-sample forecast exists, so no skill comparison against the null is possible.
- Full-information Bayesian estimation with priors — what the authors used — is untested here and would change the identification result by construction.
