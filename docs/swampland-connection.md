# The swampland connection — the constraint-first conjecture as a swampland test

This doc records the bridge between the measured structure map and the swampland
program, and the runnable system that tests it: `pacland.swampland` +
`scripts/test_swampland.py` (pure stdlib + numpy; `python -m unittest` green).

## The claim being tested

`docs/constraint-first-conjecture.md` says: *the landscape's only structure is what
it forbids; everything it produces is noise plus a weak scale.* The swampland
program is the same sentence as theory — every swampland conjecture is a "consistency
forbids X" statement. So the conjecture makes a **per-conjecture prediction**: any
swampland quantity we can actually compute will be

- **exactly determined by flux (r ≈ 1.0)** when it is a pure charge/consistency
  condition (the tadpole class), or
- **statistically uniform in flux (r < 0.25)** when it depends on moduli
  stabilization (the W₀/g_s/mass class).

A swampland quantity that falls in neither bucket would be a *new kind of structure*
— and would refute the conjecture. That is what the system is for.

## The results (Rule of Three, 101 vacua + 174-SUSY slice)

| conjecture | quantity | ridge r | ridge z | MI z | verdict |
|---|---|---|---|---|---|
| Weak Gravity (electric) | g_min = lightest coupling | −0.13 | −1.29 | 0.55 | **random** |
| Weak Gravity (electric) | g_mean | −0.16 | −1.46 | 0.84 | **random** |
| No global symmetries | charge gcd | — | — | — | **consistent (gcd = 1)** |
| Distance (proxy) | log m_light vs distance | −0.68 | −9.21 | (Spearman −0.46, z −6.33) | **real signal** |
| Gravity/tadpole (anchor) | N_flux | +0.98 | +9.12 | +1.18 | **structured** |

### What each line means

- **Weak Gravity.** The magnetic scale Λ = g·M_pl depends on g_s through the
  stabilized moduli, so the constraint-first conjecture predicts it is uniform in
  flux — and it is (r < 0.25, MI z < 1). The *scale* half of the WGC is testable
  now and consistent. The *existence* half (a super-extremal state in the spectrum)
  needs the full charged spectrum → **NEEDS-BIGGER-MACHINE**.

- **No global symmetries.** The necessary condition — the flux charges must not all
  share a divisor d, or the theory carries a forced Z_d global symmetry — is
  satisfied (gcd = 1). The *stronger* statement splits honestly in two: (i) the
  flux lattice is Z^{2b3} by the flux-quantization theorem, so it is unimodular
  *tautologically* — an SNF over the flux sample would measure the sample, not the
  theory; (ii) the object that actually carries a global-symmetry statement is the
  *gauge* charge lattice of the low-energy U(1)s, and its unimodularity is fixed by
  the intersection-form charge matrix inside the model. That is a model-internal
  quantity not yet exposed → **NEEDS-MODEL-INTERNALS** (a sibling of
  NEEDS-BIGGER-MACHINE), not a small follow-up.

- **Distance.** The proxy turns out to be a **real signal, not an artifact** — but
  it is *directionally* consistent with the distance conjecture, not a test of it.
  The lightest mass falls with the (CS) moduli distance from the sample centroid:
  Pearson r = −0.68 (z = −9.2) and rank-Spearman r = −0.46 (z = −6.3) — both far past
  the permutation null. The trend **survives flux control** (residual r = −0.63 after
  removing the ridge-quadratic flux prediction of the mass), so it is not just the
  already-known flux→mass-scale structure. The two honest bounds: it runs on the CS
  moduli, where the conjecture does *not* live (it lives on the Kähler moduli, flat at
  degree-0), and the distance is centroid-Euclidean, not a field-space geodesic.
  → **NEEDS-BIGGER-MACHINE** for the clean test; the proxy itself is real and
  reproducible (`pacland.swampland.distance_conjecture_test`).

- **Tadpole anchor.** r = 0.98 with ridge z = 9.1 — the exact constraint is
  recovered by the joint quadratic fit. Note **MI z = 1.18**: single-coordinate MI is
  blind to a bilinear form, which is exactly the lesson the Rule of Three exists to
  keep. This is the positive control that the system is measuring what it claims.

## What this adds to the falsifiable surface

1. **New prediction (confirmed once):** the WGC scale Λ = g·M_pl is statistically
   uniform in flux. Refutation = a future sample where g carries flux structure at
   cross-validated r > 0.5.
2. **New prediction (to run on the bigger machine):** the lightest tower mass already
   falls with field distance on the CS slice (Pearson −0.68, z −9.2, flux-controlled
   residual −0.63) — directionally what the distance conjecture predicts. The clean
   test needs the full Kähler sector and a geodesic distance; the h12=25/272 chase is
   exactly where this becomes testable.

## The Mitchell deficit does not change here — and that is the honest point

The swampland bounds are *predictions*, not *measurements*: there is no experimental
target value for "the WGC scale" the way there is for α_s(M_Z). So this system
extends PACLAND's **prediction** surface (`docs/falsifiable-predictions.md`), not its
verification deficit. m stays **9** (topology 4 + flux tadpole 1 + SM 4); the swampland
work is the benchmark that future structure-mining claims must beat, not a new
validated oracle rung.

## Reproduce it

```
python3 scripts/test_swampland.py
python3 -m unittest discover -s tests -q   # 475 tests
```

The module cross-checks its numpy ridge against the canonical stdlib
`structure.ridge_cv_predictability` (identical to 5 decimals on the tadpole and W₀),
so the swampland numbers live in the same reference frame as the published
structure map.
