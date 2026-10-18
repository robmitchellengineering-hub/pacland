# W0 is learnable through the phenotype, not the genotype

The sharpest learnability result so far, and it reframes the governing question.

## The measurement

Predict `W0` from different sets of inputs (107 real flux vacua):

| predictor → `log_W0` | R² | F | verdict |
|---|---|---|---|
| **flux (12 features)** | 0.100 | 0.81 | **not learnable** (F < 1) |
| **gauge couplings (1 scalar: mean log g²⁻¹)** | **0.144** | **16.64** | **learnable** (F >> critical ~3.94) |
| log g_s (1 scalar) | 0.045 | 4.90 | marginal |

One scalar summary of the gauge couplings predicts `W0` **better than the entire
12-dimensional flux vector**. The information about `W0` is *compressed into the
gauge couplings*, not spread across the raw flux.

## What this means for the learnability conjecture

The governing question — "is `compactification → observables` learnable?" — has
been asked the wrong way. It is **not** learnable from the *genotype* (the raw
flux, F = 0.81) but **is** learnable from the *phenotype* (the gauge couplings,
F = 16.64). The map splits:

```
flux (genotype)  --unlearnable-->  observables  --learnable-->  W0
```

The structure lives one level up: the relevant "input" for predicting `W0` is not
the flux but the *other observables*. This is a renormalization-like statement —
the predictive information flows through the intermediate observables, which is
where the learnability conjecture should actually be applied.

## Physics sense (and why it is not trivial)

`W0` and the gauge kinetic function are both determined by the *stabilized
moduli* — a shared cause driven by the flux. So they correlate through the moduli,
even though `W0` alone is statistically uniform over the raw flux. The finding
locates the moduli stabilization as the compression step: the flux's 12 degrees
of freedom collapse into the few observables that actually constrain `W0`.

## Honest caveats

- R² = 0.14 is *modest* — the relation is real (F = 16.64) but far from
  deterministic; most of `W0`'s variance remains unexplained.
- "mean gauge coupling" is a scalar proxy for a variable-length vector; the full
  coupling vector likely carries more of the signal.
- Linear only; the other session's non-linear miner is the natural complement.

## Where this lives

- `src/pacland/learnability_guards.py::guard_linear_structure` — the guard that
  certifies "learnable" (F > threshold), mutation-tested against noise.
- `docs/joint-structure.md` — the correlation this refines into a learnability statement.
- `data/flux_observables.json` — the paired data.
