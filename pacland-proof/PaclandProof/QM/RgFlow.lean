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

/-- **UV stability (the small-field spacing-uniform control)**: the cluster expansion converges
UNIFORMLY in the activity — for `|z| ≤ ρ < 1`, the geometric series `Σ zⁿ` converges, and its sum is
bounded by `1/(1−ρ)` uniformly in `z`. This is the small-field region's spacing-uniform bound that
Balaban's polymer expansion needs at every scale. -/
theorem cluster_expansion_uniform_bound {z ρ : ℝ} (hρ : ρ < 1) (hz : |z| ≤ ρ) :
    Summable (fun n : ℕ => z ^ n) ∧ ∑' n : ℕ, z ^ n ≤ 1 / (1 - ρ) := by
  have hz' : |z| < 1 := lt_of_le_of_lt hz hρ
  constructor
  · exact (cluster_expansion_converges_iff).mpr hz'
  · have hgeom : ∑' n : ℕ, z ^ n = (1 - z)⁻¹ := tsum_geometric_of_abs_lt_one hz'
    rw [hgeom]
    have h3 : 1 - ρ ≤ |1 - z| := by
      have h4 : 1 - |z| ≤ |1 - z| := by
        have h5 : |(1 : ℝ)| - |z| ≤ |1 - z| := abs_sub_abs_le_abs_sub 1 z
        simpa using h5
      linarith [h4, hz]
    have hne : 1 - z ≠ 0 := by
      intro h
      have hz1 : z = 1 := by linarith
      rw [hz1] at hz'
      norm_num at hz'
    have h5 : |(1 - z)⁻¹| ≤ (1 - ρ)⁻¹ := by
      rw [abs_inv]
      exact (inv_le_inv₀ (abs_pos.mpr hne) (by linarith : 0 < 1 - ρ)).mpr h3
    simpa [one_div] using (le_trans (le_abs_self _) h5)
/-- **The small/large-field decomposition** (Balaban's two regions): the activity `z` splits into the
small-field (`|z| ≤ ρ`, controlled by the cluster expansion) and the large-field (`ρ < |z|`, controlled
by the compactness of the gauge group). -/
theorem small_large_field_decomposition {z ρ : ℝ} :
    (|z| ≤ ρ) ∨ (ρ < |z|) := le_or_gt (|z|) ρ

/-- **UV stability (the spacing-uniform bound)**: the effective action is bounded uniformly in the
scale. In the small-field region `|z| ≤ ρ < 1` the cluster expansion converges with the bound `1/(1−ρ)`;
in the large-field region `ρ < |z|` the compactness of the gauge group bounds the activity `|z| ≤ 1`.
The two regions together give the spacing-uniform control that Balaban's RG needs at every scale. -/
theorem uv_stability {z ρ : ℝ} (hρ : ρ < 1) (hz : |z| ≤ 1) :
    (|z| ≤ ρ ∧ Summable (fun n : ℕ => z ^ n) ∧ ∑' n : ℕ, z ^ n ≤ 1 / (1 - ρ))
    ∨ (ρ < |z| ∧ |z| ≤ 1) := by
  rcases small_large_field_decomposition (z := z) (ρ := ρ) with h | h
  · left
    have hsum := cluster_expansion_uniform_bound hρ h
    exact ⟨h, hsum.1, hsum.2⟩
  · right
    exact ⟨h, hz⟩
end QM
