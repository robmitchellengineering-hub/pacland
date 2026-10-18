# The Verification Deficit Report — approach #6

**Status: 2026-10-18. The product is a number, not a vacuum.**

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

| | count |
|---|---|
| measured (`c*` known) | 10 |
| computable (oracle) | 7 |
| **validated (the real `m`)** | **0** |
| unverifiable (measured, not computable) | 3 |

With `m = 0`, the Hoeffding radius `sqrt(ln(1/δ_e)/(2m))` is **infinite**: the
certificate is **vacuous**. The deficit is **total**, not ~31%.

## The correction this report makes over v1

v1 quoted "~19 measured Standard-Model parameters → ~31% radius." That conflates
*measured targets* with *validation points*. A validation point needs both `O(x)`
and an independent `c*(x)` on the *same* `x`:

- for our universe, `c*` is known but `O` is not (the compactification is unknown);
- for exact/tractable backgrounds, `O` is computable but they are not our universe.

So the true `m` is the number of exact/tractable cases with both — today **zero**,
because no flux-vacua oracle emits a calibrated error model (`docs/oracle.md` §7:
only `validated: true` models may be used).

## What closes the deficit

The binding constraint is not compute; it is **validated oracle outputs**. Each
observable that gains a calibrated error model in the verification zone moves `m`
from 0 toward the ~10–19 targets and shrinks the radius from ∞ toward ~31%.
That is exactly what stage 2 (#1, the Verification Vault) builds.

## Where this lives

- `src/pacland/deficit.py` — the computation.
- `src/pacland/observables.py` — the canonical classified set.
- `tests/test_deficit.py` — the guards (positive assertions).
- `tests/test_deficit_mutations.py` — the required-to-fail mutation tests.
- `scripts/verify_deficit_numbers.py` — pins the radii.
