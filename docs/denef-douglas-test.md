# Testing Denef–Douglas uniformity — first empirical pass

The negative result (W₀ uniform → not evolvable) rests on Denef–Douglas, which says
flux vacua have W₀ uniform in the complex plane, hence |W₀|² uniform, hence a *linear*
empirical CDF. This doc records the first attempt to test that directly.

## Method

Sample flux vacua three ways and measure the linearity (R²) of the |W₀|² empirical
CDF (`src/pacland/constraints.py::linearity_r2`):

| sampler | n | \|W₀\|² CDF R² (1.0 = uniform) |
|---|---|---|
| uniform flux, bounds [−5,5] | 107 | 0.30 |
| uniform flux, bounds [−20,20] | 108 | 0.24 |
| ISD (natural), all critical points | 243 | 0.14 |
| **ISD (natural), SUSY only** | **30** | **0.60** |

## Interpretation

1. **Uniform-in-a-box sampling does not reproduce uniformity** (R² ≈ 0.2–0.3), and
   widening the bounds does not help. Uniform flux is *not* the natural measure.
2. **ISD (the natural measure), full set** is strongly non-uniform (R² = 0.14) —
   but it is dominated by non-SUSY runaway points (huge τ, small g_s).
3. **ISD, SUSY subset** is substantially closer to uniform (R² = 0.60) — consistent
   with Denef–Douglas, which is a statement about *SUSY* vacua — but the sample is
   only 30 points, far too few to confirm.

## Honest conclusion

The trend points the right way (the SUSY subset, sampled by the natural measure, is
the most uniform), weakly supporting Denef–Douglas. Confirming it requires a much
larger SUSY ISD sample (`n_target ~ 1000+`), which is the natural next compute step.
Until then the honest statement is: *the negative result's uniformity basis is
theoretical; our data is consistent with it but does not yet confirm it.*

## Larger sample (380 SUSY vacua) — the precise statement

A bigger ISD run (`n_target=2000`) yielded 380 SUSY vacua. Testing *both* candidate
uniformities:

| variable | CDF linearity R² |
|---|---|
| \|W₀\|² (area-uniform) | 0.450 |
| **log\|W₀\| (log-uniform)** | **0.923** |

**Finding:** |W₀| is **log-uniform**, not area-uniform. The log\|W₀\| CDF is nearly
linear (R² = 0.92), while the |W₀|² CDF is not (R² = 0.45). This is the **standard
KKLT log-uniform prior** — the assumption that W₀ is tuned uniformly in log — now
measured directly on the SUSY subset, rather than assumed.

**Correction to the negative result's wording:** the earlier "W₀ uniform" was
imprecise. The data says "log\|W₀\| uniform," which is the physically-relevant
statement (and the one that makes the KKLT tuning probability a clean
log-range fraction).

## Where this lives

- `scripts/sample_uniformity.py` — uniform-in-a-box at two bound widths.
- `scripts/sample_isd.py` — ISD critical-point sampling + W₀ extraction.
- `scripts/sample_isd_large.py` — the n_target=2000 run; output in `data/isd_susy.json`.
- `src/pacland/constraints.py` — `elimination_curve` + `linearity_r2`.
