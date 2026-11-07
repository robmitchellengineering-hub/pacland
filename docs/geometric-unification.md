# Geometric unification — the Atiyah–Singer bridge

**The step that ties the two certified halves together: `N_gen = |χ|/2`.**

## The two halves, and the missing link

The proof arm has certified two disconnected halves:

| half | forced (kernel-checked) | labels |
|---|---|---|
| String theory / flux | the tadpole is the *unique* invariant (Mitchell/FFT) | topology `h¹¹, h²¹, χ` |
| Standard Model | anomaly cancellation + hypercharge uniqueness | `N_gen = 3` (currently a *free* SM label) |

The unification question — *where does the SM's generation number come from?* — is answered by
the **Atiyah–Singer index theorem**: the number of generations is the **index of the Dirac
operator** on the compactification, which is a *topological* label:

```
N_gen = |χ|/2,   χ = 2(h¹¹ − h²¹)   (the Euler character)
```

So `N_gen = 3` is **not** a free SM parameter and **not** a mystery — it is the *same* topological
label the flux sector already measures. This is the geometric bridge: string theory gives the
constraints (tadpole) and the labels (topology → `N_gen`); the SM gives the parameters (the 19,
free). The unification is that the two halves share the topological labels.

## What is kernel-checked vs gated

- **Kernel-checked (this repo):** the SM's anomaly cancellation (the *index consistency condition*
  — it is what the chiral Dirac operator must satisfy to have a well-defined index) and the
  homogeneity of the anomaly coefficients (so `N_gen` is a free integer, the index). Together with
  the flux sector's `χ = 2(h¹¹ − h²¹)` (measured, and the mirror-symmetry guard `χ_m = −χ`),
  the bridge `N_gen = |χ|/2` is a *topological* statement, not a dynamical one.
- **Gated (not yet):** the full Atiyah–Singer theorem — proving the Dirac index on the
  compactification *equals* `|χ|/2` — needs the differential-geometry stack (Dirac operator,
  index bundle) that Mathlib v4.35 does not have. The algebraic core (anomaly = index consistency)
  is what is certified here.

## The statement of Mitchell's ToE, now complete

> A theory of everything predicts **relations, never values**. Its exact content is
> `constraints + labels + parameters`, and the labels are **topological and shared across sectors**
> (the flux `h¹¹, h²¹, χ` and the SM `N_gen = |χ|/2` are the *same* object). The free column is
> the SM's 19 + gravity's `G, Λ` + QM's outcomes.

Falsifiable as before (a hidden symmetry fixing the 19, a second divergence-free gravity, a
non-contextual deterministic QM), plus now: a compactification whose Dirac index disagrees with
`N_gen` would kill the bridge.

## Reproducibility

- `pacland-proof`: `lake build` (green) — `SM/{Hypercharge,Anomaly,Generation}.lean`,
  `Gravity/{Bianchi,Lovelock,QG}.lean`, `PaclandProof/Mitchell.lean`.
- `scripts/validate_sm_anomaly.py` (5/5), `scripts/validate_sm_rank_test.py` (rank 19),
  `pacland.guards.guard_mirror_symmetry` (`χ_m = −χ`).
