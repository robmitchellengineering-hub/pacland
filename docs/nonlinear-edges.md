# Nonlinear edges — the phenotype network is more structured than linear correlation showed, and the tadpole hub is partly leverage

Spearman (rank) vs Pearson (linear) on the phenotype network, n ≈ 101.

## The nonlinear edge the linear test missed

| edge | Pearson | Spearman |
|---|---|---|
| **mean gauge coupling ↔ n(massive moduli)** | −0.21 | **−0.52** |

A **monotone nonlinear** relation: the gauge couplings and the mass count are
strongly rank-correlated (−0.52) while the linear Pearson is weak (−0.21) because
the relation is curved, not straight. This is exactly the class of structure a
linear R²/F analysis is blind to — and it is the concrete bridge to the other
session's non-linear miner (which found `g_s` structure this side's linear tests
also missed).

## The caveat that tempers the earlier headline

| edge | Pearson | Spearman |
|---|---|---|
| tadpole ↔ n(massive moduli) | +0.52 | +0.25 |

The tadpole's headline correlation (0.52) is **partly leverage**: a few
large-|tadpole| vacua dominate the linear fit, while the robust rank relation is
half as strong. The true relation is threshold-like (large tadpole → more
stabilized moduli, noisy in between), not a clean line. The "tadpole is the hub"
claim stands, but its strength is ~0.25–0.5, not 0.5 flat.

## The refined picture

The phenotype network has **two kinds of edges**:

- **linear** (tadpole → mass count via the high-leverage tail),
- **nonlinear** (gauge couplings ↔ mass count, rank −0.52).

A linear-only analysis both *over*-states the tadpole and *under*-states the
gauge-coupling edge. The correct object is the **rank/information structure** of
the network, not the correlation matrix. That is the handoff point to mutual
information and to the non-linear miner.

## Caveats

- Spearman captures *monotone* nonlinearity only; non-monotone structure (the
  other session's `g_s` signal) needs mutual information or a miner.
- n = 101; the rank signal is robust but the exact functional form is unmodeled.

## Where this lives

- `docs/phenotype-network.md` — the linear network this corrects.
- `data/flux_observables.json` — the paired data.
