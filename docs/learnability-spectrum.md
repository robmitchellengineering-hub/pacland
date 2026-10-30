# The learnability boundary — linear fails, quadratic carries structure, W0 is random

Refined result from the paired flux↔observable data (107 real SUSY flux vacua,
`data/flux_observables.json`). This is the *verification* angle: not mining for
structure, but certifying **where** structure exists and where it does not.

## What was measured

For each observable, linear regression R² (flux → observable) plus, for the
deterministic case, the quadratic cross-term correlation.

| observable | linear R² | linear F | verdict |
|---|---|---|---|
| `log_W0` | 0.105 | 0.92 | random — no linear structure |
| `log_gs` | 0.119 | 1.06 | weak / marginal |
| `tadpole` | 0.067 | 0.56 | **nonlinear — see below** |
| n(gauge couplings) | 0.061 | 0.50 | random |
| n(masses) | 0.028 | 0.23 | random |

## The telling case: tadpole

`tadpole` is a *deterministic* function of the flux — the D3 tadpole, a bilinear
form ∫H₃∧F₃ — yet its **linear R² is 0.067** (F = 0.56, "random"). The reason:

| probe of tadpole vs | max \|r\| |
|---|---|
| linear fᵢ | 0.132 |
| diagonal fᵢ² | 0.155 |
| **cross-terms fᵢfⱼ** | **0.453** (f0·f9, f2·f11, f3·f6, f4·f7, f5·f8) |

The cross-terms that carry the tadpole are precisely **F₃–H₃ pairings** (first six
coordinates are F₃, last six are H₃) — the bilinear structure linear regression is
blind to.

## What this says about the learnability conjecture

1. **The map is not linearly learnable.** Every observable has linear R² ≤ 0.12.
   A linear/statistical-query learner restricted to coordinate queries sees
   nothing — which is exactly why my earlier "linear correlation ≈ 0" reading was
   correct but *incomplete*.
2. **The map is nonlinearly structured, not random.** The tadpole is recovered by
   quadratic cross-terms (|r| ≈ 0.45). Its complexity is *quadratic* — O(p²)
   features — which is **polynomial**, consistent with the learnability
   conjecture's positive branch (`SQdim = O(poly(p))`), *not* the negative one.
3. **`W0` is the genuine exception** — statistically uniform (Denef–Douglas),
   random, unlearnable. `log_gs` is marginal (linear) but the other session's
   non-linear miner found structure there (z = 3.56).

## The refined picture (supersedes the earlier flat "not evolvable")

The flux→observable map is **not** uniformly random and **not** linear: it is
**nonlinearly structured at polynomial complexity** for the deterministic parts
(tadpole), with `W0` the one truly random observable. That means:

- linear learnability: fails (certified here);
- polynomial (quadratic) learnability: holds for the deterministic part;
- the evolvability gate is therefore **not** trivially closed — the search is
  blocked by the *random* observables (W0), not by exponential complexity.

This is the boundary the "compare notes" step should test: the other session's
non-linear miner recovers the structure; this side certifies *linear* absence and
*poly* presence, and pins `W0` as the unlearnable part.

## Where this lives

- `scripts/measure_learnability_spectrum.py` — linear R²/F per observable.
- `data/flux_observables.json` — the paired flux + richer observables (107 vacua).
