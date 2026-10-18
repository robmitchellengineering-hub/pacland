# The phenotype network — the landscape's learnable structure is observable↔observable, with the tadpole as hub

The reframe that fell out of going multipath: stop asking about the
genotype→phenotype map (unlearnable) and map the **phenotype network** instead.

## The network (107 real flux vacua)

Pairwise correlations among the observables:

| edge | r |
|---|---|
| **tadpole ↔ n(massive moduli)** | **+0.519** (z ≈ 5σ) |
| `log_W0` ↔ mean gauge coupling | +0.379 (z ≈ 3.8σ) |
| `log_W0` ↔ `log_gs` | −0.211 |
| tadpole ↔ mean gauge coupling | −0.213 |
| mean gauge coupling ↔ n(massive moduli) | −0.212 |
| `log_gs` ↔ (anything) | ≤ 0.11 |

The **tadpole is the hub**: it correlates with the mass count (0.52), the gauge
couplings (−0.21), and weakly with `W0`. It is the one observable everything else
routes through.

## The headline, robust across models

`tadpole ↔ n(massive moduli)`:

| model | n | r |
|---|---|---|
| h12_2_model1 | 47 | 0.486 |
| h12_2_model2 | 60 | 0.551 |

The flux tadpole (∫H₃∧F₃, range ~[−58, 72]) strongly predicts **how many moduli
are stabilized/massive** (0–6). Physics sense: the tadpole sets the scale of the
flux-induced potential, which determines the moduli mass spectrum — more flux
charge, more stabilized moduli.

## The reframe

The learnability question has been aimed at the wrong object. The
genotype→phenotype map (`flux → observables`) is unlearnable (F ≈ 0.8), but the
**phenotype→phenotype network** is richly structured and learnable:

```
flux (12 redundant dims)  --lossy-->  observables  --structured-->  each other
                                       └ tadpole (hub)
```

The landscape's relevant, learnable description is a **small network of
observable–observable relations** with the tadpole at its center — not the
high-dimensional flux. This is a compression statement (the 12 flux dims collapse
to a handful of structured observables) and a causal statement (the tadpole is
the common driver).

## Caveats

- n = 107; correlations are linear; the network is a lower bound on the structure.
- `n(massive moduli)` is a count (0–6), so the tadpole→count relation is the
  coarse-grained shadow of the full mass spectrum; the actual masses are the
  finer target.

## Where this lives

- `data/flux_observables.json` — the paired data.
- `docs/learnable-through-phenotype.md` — the single-observable precursor.
- `docs/joint-structure.md` — the W0↔gauge-coupling edge.
