# Synthesis — the landscape's learnable structure is a small, nearly-closed phenotype network

Consolidation of the verify-lead findings (2026-10-18). Each reframe is a link;
the individual docs carry the numbers.

## The claim, in one sentence

**The IIB flux-vacua landscape is not learnable through its high-dimensional
genotype (the flux), but through a small, nearly-closed network of its phenotype
(observables), centered on the D3 tadpole as the relevant coupling and the
dilaton as the residual channel.**

## The reframes, in order

1. **Joint, not marginal.** `W0` looks random against each flux coordinate, but is
   correlated with the gauge couplings (r ≈ 0.38). *Marginal independence hid
   joint structure.*
2. **Phenotype, not genotype.** `W0` is unlearnable from the 12-dim flux
   (F = 0.81) but learnable from a single gauge-coupling scalar (F = 16.64).
   *The wrong map was being learned.*
3. **Network, not map.** The observables form a structured network with the
   tadpole as its strongest node. *The relevant object is observable↔observable.*
4. **Sufficient statistic.** The flux's effect on the mass spectrum goes entirely
   through the tadpole (flux adds only +0.03 R² on top of it). *flux → tadpole →
   n(massive moduli) is a clean causal chain.*
5. **Partial Markov blanket.** The observables predict each other at 15–30% R² and
   the flux adds only 3–12% — but `log_gs` is the leak (flux adds +0.124).
   *The compression is nearly, not perfectly, complete.*
6. **Nonlinear edges.** The gauge-coupling ↔ mass-count relation is monotone
   nonlinear (Spearman −0.52 vs Pearson −0.21), and the tadpole's Pearson (0.52)
   is partly leverage (rank 0.25). *Linear analysis both over- and under-stated
   the network.*

## The honest boundaries (named, not hidden)

- `W0` is the genuinely random observable (Denef–Douglas); `g_s` and the gauge
  couplings carry the learnable structure.
- The "sufficient statistic" is clean only for the mass count; `g_s` retains a
  direct flux dependence.
- n = 107 (101 with full scalars); all results are *linear or monotone* — the
  non-linear miner (other session) and mutual-information at higher n are the
  natural extensions.
- A crude 5-bin MI estimate at n ≈ 100 was inconsistent with the Spearman and is
  **not** trusted; it is parked, not published.

## What it means for the program

The learnability conjecture should be restated: it is not "is `flux → observables`
learnable?" (answer: barely) but "is the **phenotype network** learnable?" (answer:
yes, and it is small). The search/selection problem reduces to the structured
observables — the tadpole, the gauge couplings, the dilaton — with `W0` dropping
out as random. That is the concrete, falsifiable handoff to the selection question
and to the other session's non-linear miner.

## The docs this ties together

`joint-structure`, `learnable-through-phenotype`, `phenotype-network`,
`sufficient-statistic`, `partial-markov-blanket`, `nonlinear-edges`.
