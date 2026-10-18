# The structure is joint, not marginal — W0 is random alone but correlated with the gauge couplings

The swing that landed, after the first test missed.

## The finding

Across the 107 real flux vacua (both models, consistent):

| correlation | r | n |
|---|---|---|
| `log_W0` ↔ mean gauge coupling (log g²⁻¹) | **0.378** (z ≈ 3.8σ) | 101 |
| — model 1 | 0.414 | 44 |
| — model 2 | 0.331 | 57 |
| `log_W0` ↔ number of gauge couplings | −0.074 | 107 |
| `log_W0` ↔ individual flux coordinate (max) | 0.17 (2.2σ) | 107 |

So `W0` is **marginally random** — independent of every flux coordinate — yet
**jointly structured** with the gauge-coupling *values* (not their count).

## What it means

1. **"W0 is random" was only half the story.** It is random *conditioned on the
   raw flux*, but not random *jointly with the other observables*. The information
   about `W0` lives in the gauge couplings, not in the flux coordinates alone.
2. **The selection signal is conditional/joint, not marginal.** My earlier
   marginal-uniformity test (KS) failed to find it because distribution *shape*
   is the wrong probe — the signal is the *correlation between observables*.
3. **Physics sense:** the superpotential `W0` and the gauge kinetic function are
   both set by the *stabilized moduli* (a shared cause driven by the flux). They
   correlate through that common cause even though neither is a simple function of
   the raw flux quanta.

## The refined learnability/selection picture

- marginal (flux → any single observable): near-zero structure (certified earlier);
- joint (observable ↔ observable): **real structure** — `W0` ↔ gauge couplings at
  0.38, robust across models.

The hypothesis class for "which vacuum is ours" must model the **joint**
distribution, not the marginals. That is where selection — if it exists — lives,
and it is now located to a concrete, testable relationship.

## Honest caveats

- n = 101; the correlation is a *linear* joint statistic. A non-linear miner may
  find more; this is a lower bound on the joint structure.
- "mean gauge coupling" is a crude summary of a variable-length vector; the full
  coupling-vector structure is the natural next test.

## Where this lives

- `data/flux_observables.json` — the paired data.
- `docs/selection-uniformity.md` — the claim this refines (marginal test missed,
  joint test found it).
- `src/pacland/learnability_guards.py` — the marginal guards; a joint-structure
  guard is the next build.
