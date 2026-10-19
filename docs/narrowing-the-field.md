# Narrowing the field — using the structure map to collapse the search

The constraint-first program says the only navigable move is *elimination by
verified constraint*. This doc records the out-of-the-box reading of the structure
map that makes that concrete: **the structure map narrows the *search*, not just
the landscape.** The uniform observables it found are not "uninteresting" — they
are *useless for narrowing*, and dropping them collapses the search space.

## The classification (narrowing power, not just learnability)

Every flux-determined observable falls in one of three tiers, and each tier has a
*different narrowing power*:

| tier | r | observables | narrowing power |
|---|---|---|---|
| **exact** | 1.0 | D3 tadpole FᵀJH | **full** — rules out vacua precisely |
| **weak** | ~0.6 | W₀, saxions | **partial** — eliminates tails, not the target |
| **uniform** | <0.25 | g_s, gauge, mass-shape, axions, dilaton, V | **zero** — cannot distinguish any two vacua |

The uniform tier is the point. An observable that is statistically identical across
the landscape carries **no information to narrow with** — it can be *removed from
the search* without losing anything.

## Result: the effective search dimension collapses ~10 → 3

Of the ten flux-determined observables measured, **seven are uniform** (g_s, gauge
couplings, mass-spectrum shape, axions, dilaton, AdS V, and — measured earlier — the
string-scale observables). They have r < 0.25, i.e. zero narrowing power. Only three
carry any structure:

- **tadpole** (r = 1.0) — the constraint, full narrowing power;
- **W₀** (r = 0.62) — weak, partial narrowing (its own flux dependence, see
  `docs/w0-refinement.md`);
- **saxions** (r = 0.30–0.42) — weak, partial.

So the search for our vacuum is **not** a ~10-dimensional scan; it is a
**3-dimensional** one — and one of those three (the tadpole) is the constraint that
*eliminates*, not selects.

## The measured narrowing curve (degree-0, h¹²=2)

| step | survives | eliminated |
|---|---|---|
| critical points (start) | 100% | — |
| after SUSY (DW = 0) | 13.2% | **86.8%** |
| after degree-0 stability (min eig ≥ 0) | 13.2% | ~0% (no-scale: all SUSY are degree-0 stable) |
| uniform observables (g_s, gauge, shape, axions, dilaton, V) | 13.2% | **0% each** (they cannot discriminate) |
| after \|W₀\| < 1 | ~1.9% | ~85% of the SUSY slice |

The honest headline: **two facts do almost all the narrowing** — SUSY (×0.13) and
the small-W₀ prior (×0.14). The seven uniform observables do *nothing*. That is the
structure map telling us where the narrowing power lives (the constraints and the
measure), and where it does not (the smooth observables everyone has been scanning).

## The no-fingerprint no-go (a bound on narrowing itself)

Because **no** observable carries strong structure (r > 0.9), no learning algorithm
can narrow the field below what the constraints + the measure already determine.
Narrowing the field is therefore *bounded by the constraints*, which is exactly the
constraint-first program restated as a limit:

> **You can only narrow the landscape by what it forbids, not by what it produces.**

## The five ways to use the system to narrow further

1. **Search-dimension collapse** (measured here) — drop the uniform observables;
   scan only the 3 structured ones.
2. **Constraint completeness** — verify FᵀJH is the *only* exact (r = 1.0) flux
   invariant; if others exist, they are new elimination tools.
3. **The narrowing curve** — rank constraints by elimination fraction and stack
   them (SUSY → tadpole → W₀ prior → …); each rung is a multiplicative cut.
4. **Weak-structure tails** — W₀'s r = 0.62 cannot hit the KKLT target (20 σ away),
   but it *can* rule out the wrong-W₀ vacua; narrow by the tail, not the target.
5. **SM prioritisation** — rank the ten SM observables by elimination power and
   build the oracles (close the deficit m = 5) in that order, highest cut first.

All five are testable with the existing system. Items 1–4 run now on the data we
have; item 5 is the roadmap for turning m = 5 into m = 6, 7, ….
