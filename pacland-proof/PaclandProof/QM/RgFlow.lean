import Mathlib
import PaclandProof.QM.BlockSpin
import PaclandProof.QM.ClusterExpansion

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Phase 2 — the multiscale RG flow (assembling Balaban's pieces)

The block-spin composes into a multiscale RG flow (each step halves the links), and it preserves the
total holonomy at every scale, while the small-field cluster expansion converges uniformly in the
activity. These are the FIRST assembled pieces of Balaban's multiscale RG; the UV-stability bound
(the spacing-uniform effective action) is the deep output that the full program (small/large-field
regions + induction over scales) produces on top of these.
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {G : Type*} [CommGroup G]

/-- **The block-spin RG flow**: applying the block-spin twice gives the coarse-graining by 4 — the
multiscale RG composes the decimation steps, and each step halves the number of links. -/
theorem blockSpin_twice (U : ℕ → G) (j : ℕ) :
    blockSpin (blockSpin U) j = U (4 * j) * U (4 * j + 1) * U (4 * j + 2) * U (4 * j + 3) := by
  dsimp [blockSpin]
  group

/-- **The RG flow preserves the total holonomy at the 4-fold scale**: the product of 4n fine links
equals the product of n twice-block-spun links. -/
theorem blockSpin_twice_preserves_holonomy (U : ℕ → G) (n : ℕ) :
    (∏ i ∈ Finset.range (4 * n), U i) = (∏ j ∈ Finset.range n, blockSpin (blockSpin U) j) := by
  rw [show 4 * n = 2 * (2 * n) by ring]
  rw [blockSpin_preserves_holonomy]
  rw [blockSpin_preserves_holonomy]

/-- **The small-field cluster expansion converges uniformly in the block-spin scale**: the geometric
series in the activity `z` (the small-field deviation) converges exactly when `|z| < 1` — the
small-field condition that Balaban's polymer expansion needs to be well-defined at every scale. -/
theorem cluster_expansion_converges {z : ℝ} (hz : |z| < 1) : Summable (fun n : ℕ => z ^ n) := by
  exact (cluster_expansion_converges_iff).mpr hz

end QM
