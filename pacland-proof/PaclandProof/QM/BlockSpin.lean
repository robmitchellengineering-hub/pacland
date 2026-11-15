import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# M3 — the block-spin (coarse-graining) map

The second piece of the weak-coupling multiscale RG scaffolding. The block-spin map groups pairs of
fine links into a coarse link, and the key property is that it **preserves the total holonomy** — the
coarse field carries the same topological information as the fine field. This is the "decimation" step
that lets the multiscale RG integrate out the small-cell fluctuations while keeping the Wilson loop.
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {G : Type*} [CommGroup G]

/-- The block-spin (decimation) map: the coarse link `j` is the product of the two fine links
`U (2j)` and `U (2j+1)`. This is the coarse-graining step of the multiscale RG. -/
def blockSpin (U : ℕ → G) (j : ℕ) : G := U (2 * j) * U (2 * j + 1)

/-- **The block-spin preserves the total holonomy**: the product of `2n` fine links equals the
product of `n` coarse links. The coarse field carries the same topological (holonomy) information. -/
theorem blockSpin_preserves_holonomy (U : ℕ → G) (n : ℕ) :
    (∏ i ∈ Finset.range (2 * n), U i) = (∏ j ∈ Finset.range n, blockSpin U j) := by
  induction' n with n ih
  · simp [blockSpin]
  · rw [Finset.prod_range_succ]
    rw [show 2 * (n + 1) = 2 * n + 2 by ring]
    rw [Finset.prod_range_succ, Finset.prod_range_succ]
    rw [ih]
    dsimp [blockSpin]
    group

end QM
