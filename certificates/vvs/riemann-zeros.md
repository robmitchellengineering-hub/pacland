# Valiant Verification certificate — Riemann zeros and GUE statistics

**Format:** `valiant-verification/named-gate@1`  
**Issuer:** Pacland / Valiant Verification  
**Issued:** 2026-10-28  
**Grade:** **VERIFIED**  
**Gates:** 4 of 4 pass  
**Verified:** yes

| gate | result | evidence | falsifier | remedy |
|---|---|---|---|---|
| `implementation_does_the_zeta_implementation_reproduce_known_valu` | **pass** | the first five zeros to 4.2e-11, on an engine written from scratch with no dependencies | the first five zeros are 14.134725, 21.022040, 25.010858, 30.424876, 32.935062 — an implementation that misses them is wrong and knows it | none — re-run on any change to the zeta engine; the five known zeros are the regression test |
| `data_quality_are_all_the_zeros_in_the_range_actually_found` | **pass** | 1517 zeros below t = 2000 against a smooth count of 1517.0 — no zeros missed | a count that drifts from the counting formula means missed or spurious zeros | none — the check passes; keep the evidence and re-run on change |
| `outcomes_analysis_do_the_zeros_obey_the_gue_statistics_or_poisso` | **pass** | ratio statistic 0.6176 against a synthetic GUE control 0.6140 ± 0.0068, and Poisson 0.3810 — 34.6 control standard deviations away | a ratio near the Poisson value would mean the zeros do not repel | none — the check passes; keep the evidence and re-run on change |
| `conceptual_soundness_is_the_textbook_constant_the_right_referenc` | **pass** | no — 0.5307 is the asymptotic GUE value; at 201 spacings the same estimator returns 0.6163 ± 0.0190, so the zeros are compared against a finite-sample control | comparing 201 spacings against 0.5307 would report a 4σ failure of a correct computation — which is exactly what the first run did | none — the check passes; keep the evidence and re-run on change |

**Producer:** Module: src/pacland/spectral/zeros.py (zeta by Euler–Maclaurin and Riemann–Siegel); Script: python3 scripts/spectral_zeros.py; Doctrine: docs/external-claims-padgett.md

## Limitations

- This is a numerical verification of a known result (Montgomery 1973; Odlyzko), not a new claim about the zeros.
- The range is t < 2000 (1517 zeros); the statistics tighten further up.
- Nothing here says the zeros predict anything physical — it says a number-theoretic object has a spectrum with the same statistics as a physical one.
