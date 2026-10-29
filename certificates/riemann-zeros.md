# Model risk certificate — Riemann zeros and GUE statistics

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **VERIFIED**

The zeros repel exactly as a Gaussian unitary ensemble does — ratio statistic 0.6155 against a finite-sample GUE control of 0.6163, and 12 control standard deviations from Poisson. Computed from scratch, no dependencies.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Implementation | Does the zeta implementation reproduce known values? | the first five zeros to 4.2e-11, on an engine written from scratch with no dependencies | **satisfied** |
| Data quality | Are all the zeros in the range actually found? | 202 zeros below t = 400 against a smooth count of 201.6 — no zeros missed | **satisfied** |
| Outcomes analysis | Do the zeros obey the GUE statistics, or Poisson? | ratio statistic 0.6155 against a synthetic GUE control 0.6163 ± 0.0190, and Poisson 0.3810 — 12.3 control standard deviations away | **satisfied** |
| Conceptual soundness | Is the textbook constant the right reference? | no — 0.5307 is the asymptotic GUE value; at 201 spacings the same estimator returns 0.6163 ± 0.0190, so the zeros are compared against a finite-sample control | **satisfied** |

## Evidence

- Module: src/pacland/spectral/zeros.py (zeta by Euler–Maclaurin and Riemann–Siegel)
- Script: python3 scripts/spectral_zeros.py
- Doctrine: docs/external-claims-padgett.md

## Limitations

- This is a numerical verification of a known result (Montgomery 1973; Odlyzko), not a new claim about the zeros.
- The range is t < 400 (202 zeros); the statistics converge further up.
- Nothing here says the zeros predict anything physical — it says a number-theoretic object has a spectrum with the same statistics as a physical one.

_4 findings: 4 satisfied._
