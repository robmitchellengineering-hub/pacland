# The Verification Deficit Report — approach #6

**Status: 2026-10-18. The product is a number, not a vacuum.**

> **Correction (2026-10-22).** This report was written on 2026-10-18, when nothing was
> validated. The deficit has since been climbed — topology 4 + flux tadpole 1 + SM 4 —
> so the combined `m = 9` (`0c6bfe0`), and the certificate is no longer vacuous overall:
> its radius at `δ_e = 0.025` is 0.45 (0.68 for topology alone, 1.36 for the flux
> tadpole alone). What is *still* total is the **values** sector measured below: the SM's
> 19 free parameters are measured, but not validated as *predictions*, because `m`
> counts exact structure, not values.

## The claim, quantified

"How far is string theory from being verifiable?" is today answerable as a number —
and the number is worse than the earlier ~31% estimate suggested.

The certificate's oracle-validation term is bounded by `m`, the number of
observables that are simultaneously:

- **measured** — an independent target `c*` exists;
- **computable** — the oracle can evaluate `O(x)`;
- **validated** — the oracle's error model is calibrated against `c*`.

Only observables with all three contribute to the certificate
(`docs/observable-measure.md` §6, top-left cell).

## The result

For the ten standard-model **values** (`STANDARD_OBSERVABLES` — the sector this report
measured), the count is unchanged:

| | count |
|---|---|
| measured (`c*` known) | 10 |
| computable (oracle) | 7 |
| **validated (the real `m`)** | **0** |
| unverifiable (measured, not computable) | 3 |

For that sector nothing clears the third condition, so the Hoeffding radius
`sqrt(ln(1/δ_e)/(2m))` is **infinite**: a certificate for a *value prediction* is
**vacuous**. The *values* deficit is **total**, not ~31% — and it is not what the
combined `m = 9` above measures (that counts exact structure: the topology, the
tadpole, and the SM's constraints and labels).

## The correction this report makes over v1

v1 quoted "~19 measured Standard-Model parameters → ~31% radius." That conflates
*measured targets* with *validation points*. A validation point needs both `O(x)`
and an independent `c*(x)` on the *same* `x`:

- for our universe, `c*` is known but `O` is not (the compactification is unknown);
- for exact/tractable backgrounds, `O` is computable but they are not our universe.

So the true `m` is the number of exact/tractable cases with both — today `pacland
deficit` counts 9 for exact structure (topology 4 + flux tadpole 1 + SM 4), while the
**values** count is still zero, because no *value* oracle emits a calibrated error
model (`docs/oracle.md` §7: only `validated: true` models may be used).

## What closes the deficit

The binding constraint is not compute; it is **validated oracle outputs**. Each
observable that gains a calibrated error model in the verification zone moves `m`
from 9 toward the ~10–19 targets and shrinks the radius from ~45% toward ~31%.
That is exactly what stage 2 (#1, the Verification Vault) builds.

## Where this lives

- `src/pacland/deficit.py` — the computation.
- `src/pacland/observables.py` — the canonical classified set.
- `tests/test_deficit.py` — the guards (positive assertions).
- `tests/test_deficit_mutations.py` — the required-to-fail mutation tests.
- `scripts/verify_deficit_numbers.py` — pins the radii.
