# Model risk certificate — Riemann zeros and GUE statistics

**Issued:** 2026-10-28  
**Issuer:** Pacland / Valiant Verification  
**Grade:** **VERIFIED**

1517 zeros computed from scratch: they repel exactly as a Gaussian unitary ensemble does — ratio statistic 0.6176 against a finite-sample GUE control of 0.6140 +- 0.0068, and 35 control standard deviations from Poisson.

| clause | question | what the evidence says | status |
|---|---|---|---|
| Implementation | Does the zeta implementation reproduce known values? | the first five zeros to 4.2e-11, on an engine written from scratch with no dependencies | **satisfied** |
| Data quality | Are all the zeros in the range actually found? | 1517 zeros below t = 2000 against a smooth count of 1517.0 — no zeros missed | **satisfied** |
| Outcomes analysis | Do the zeros obey the GUE statistics, or Poisson? | ratio statistic 0.6176 against a synthetic GUE control 0.6140 ± 0.0068, and Poisson 0.3810 — 34.6 control standard deviations away | **satisfied** |
| Conceptual soundness | Is the textbook constant the right reference? | no — 0.5307 is the asymptotic GUE value; at 201 spacings the same estimator returns 0.6163 ± 0.0190, so the zeros are compared against a finite-sample control | **satisfied** |

## Evidence

- Module: src/pacland/spectral/zeros.py (zeta by Euler–Maclaurin and Riemann–Siegel)
- Script: python3 scripts/spectral_zeros.py
- Doctrine: docs/external-claims-padgett.md

## Limitations

- This is a numerical verification of a known result (Montgomery 1973; Odlyzko), not a new claim about the zeros.
- The range is t < 2000 (1517 zeros); the statistics tighten further up.
- Nothing here says the zeros predict anything physical — it says a number-theoretic object has a spectrum with the same statistics as a physical one.

_4 findings: 4 satisfied._
