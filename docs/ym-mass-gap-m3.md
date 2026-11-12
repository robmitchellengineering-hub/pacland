# M3 — the weak-coupling multiscale RG scaffolding (the Balaban program)

The open endgame of the mass-gap plan. M1 (the exact 2D mass gap) and M2 (the clustering ⟺ gap
bridge) are done and kernel-checked. M3 is the machinery for the weak-coupling regime — β → ∞ in
d ≥ 3 — where the Dobrushin method dies (our `YMMassGap.lean`: `m → 0` at the ceiling, `m < 0` past
it).

## The precise obstruction (why this is the Clay problem)

From the research fan-out, the weak-coupling cluster expansion fails because:

1. **The flat directions are non-compact.** The trivial connection's gauge orbit `G^{|V|−1}` diverges
   in infinite volume, so the low-temperature expansion has no compact "soft-mode" target (unlike
   O(N) spin models, whose vacuum manifold is the compact sphere).
2. **Gribov–Singer.** No global, single-valued gauge fixing exists for non-Abelian G — so the
   gauge-fixed action has copies / non-analytic boundaries, and is not a small perturbation of one
   Gaussian reference.

## Balaban's answer (the scaffolding to formalize)

Balaban (CMP 1984–1989, reconstructed by Dimock 2013–14) bypassed both by a **multiscale RG in
axial gauge**, which proved **UV stability** — spacing-uniform bounds on the effective action — but
*not* the mass gap. The scaffolding is:

1. **Axial gauge.** Fix the links in one lattice direction to the identity. This is a *global*
   gauge (no Gribov copies), at the cost of breaking Euclidean covariance. The first formalization
   target: the axial-gauge-fixing theorem — every connection is gauge-equivalent to a unique axial one.
2. **Block-spin (coarse-graining) map.** Integrate out the high-momentum (small-cell) fields to get an
   effective action on a coarser lattice. The "small-field" assumption (the connection stays near the
   trivial one) is what makes the low-temperature expansion converge — this is Balaban's *small-field
   region*.
3. **Convergent cluster/polymer expansion** of the effective action, uniform in the lattice spacing.

## What this needs

These three pieces live on top of the `lgt` lattice gauge theory (connections, gauge transformations,
the Wilson action) — v4.30.0, a different codebase from pacland's mathlib v4.35. So M3 is a separate
formalization effort in the `lgt` ecosystem, not a continuation of the pacland `QM` files.

## Status

- The **obstruction is kernel-checked** (pacland `YMMassGap.lean`): the Dobrushin rate is positive
  below the ceiling but vanishes at it (`massRate_pos`, `massRate_tendsto_zero`), and negative past it
  (`massRate_neg_of_one_lt`).
- The **axial gauge + block-spin RG** are the open Balaban-program formalization targets — a
  multi-session effort in the `lgt` codebase, not a session task.
