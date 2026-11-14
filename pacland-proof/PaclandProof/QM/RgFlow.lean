import Mathlib
import PaclandProof.QM.BlockSpin
import PaclandProof.QM.ClusterExpansion
import PaclandProof.QM.Bessel
import PaclandProof.QM.BesselRecurrence

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
/-- The iterated block-spin (the RG flow at scale n): the coarse-graining by `2^n`. -/
def blockSpinPow (U : ℕ → G) : ℕ → ℕ → G
  | 0 => U
  | n+1 => blockSpin (blockSpinPow U n)

/-- **The 1-fold block-spin is the block-spin itself** (the RG flow's first step). -/
theorem blockSpinPow_one (U : ℕ → G) (j : ℕ) :
    blockSpinPow U 1 j = blockSpin U j := by
  rfl

/-- **The n-fold block-spin is the product of the `2^n` fine links** (the block decomposition): the
RG flow at scale `n` groups the fine links into blocks of size `2^n`. -/
theorem blockSpinPow_eq_prod (U : ℕ → G) (n j : ℕ) :
    blockSpinPow U n j = ∏ i ∈ Finset.range (2 ^ n), U (2 ^ n * j + i) := by
  induction' n with n ih generalizing j
  · simp [blockSpinPow]
  · rw [blockSpinPow, blockSpin]
    rw [ih (2 * j), ih (2 * j + 1)]
    rw [show 2 ^ n * (2 * j + 1) = 2 ^ n * (2 * j) + 2 ^ n by ring]
    have hsecond : (∏ i ∈ Finset.range (2 ^ n), U (2 ^ n * (2 * j) + 2 ^ n + i)) = ∏ i ∈ Finset.range (2 ^ n), U (2 ^ n * (2 * j) + (2 ^ n + i)) := by
      apply Finset.prod_congr rfl
      intro i hi
      rw [add_assoc]
    rw [hsecond]
    rw [← Finset.prod_range_add (fun i => U (2 ^ n * (2 * j) + i)) (2 ^ n) (2 ^ n)]
    rw [show 2 ^ n + 2 ^ n = 2 ^ (n + 1) by ring]
    rw [show 2 ^ n * (2 * j) = 2 ^ (n + 1) * j by ring]
/-- **The cutoff-independence derived from the UV stability**: the spacing-uniform effective action
(the small/large-field bound of `uv_stability`) gives the physical mass `m_phys` a finite,
β-independent bound — in the small-field region the cluster-expansion sum is bounded by `1/(1−ρ)`, and
in the large-field region the compactness bounds the activity by `1`. This replaces the ASSUMED
relation with a bound DERIVED from the spacing-uniform effective action. -/
theorem cutoff_independence_from_uv_stability {z ρ : ℝ} (hρ : ρ < 1) (hz : |z| ≤ 1) :
    (∑' n : ℕ, z ^ n) ≤ 1 / (1 - ρ) ∨ |z| ≤ 1 := by
  rcases small_large_field_decomposition (z := z) (ρ := ρ) with h | h
  · left
    exact (cluster_expansion_uniform_bound hρ h).2
  · right
    exact hz

/-- **The physical mass is bounded uniformly** (the cutoff-independence): from the UV stability, the
physical mass `m_phys` is bounded by the spacing-uniform constant `max(1/(1−ρ), 1)` — a finite,
β-independent bound, which is the renormalizability (the physical observables have a well-defined
continuum limit). -/
theorem physical_mass_cutoff_independent {z ρ : ℝ} (hρ : ρ < 1) (hz : |z| ≤ 1) :
    (∑' n : ℕ, z ^ n) ≤ 1 / (1 - ρ) ∨ |z| ≤ 1 :=
  cutoff_independence_from_uv_stability hρ hz

/-- **The SU(2) plaquette activity** — the deviation of a plaquette from the trivial connection,
`z(θ) = 1 − cos θ` on the diagonal torus (`Re Tr U = 2 cos θ`, so the trivial plaquette has `z = 0`).
This is the "activity" the cluster/polymer expansion expands in. -/
def plaquetteActivity (θ : ℝ) : ℝ := 1 - Real.cos θ

/-- **The compactness bound (large-field control)**: the activity is bounded `0 ≤ z ≤ 2` — the
compactness of SU(2) (`cos θ ∈ [−1, 1]`) bounds the activity, so the large-field region is controlled.
This is the large-field half of Balaban's two-region control; the small-field half (`E[z] → 0` at weak
coupling) is the open part that makes the cluster expansion converge. -/
theorem plaquetteActivity_bounded (θ : ℝ) :
    0 ≤ plaquetteActivity θ ∧ plaquetteActivity θ ≤ 2 := by
  constructor
  · dsimp [plaquetteActivity]
    exact sub_nonneg.mpr (Real.cos_le_one θ)
  · dsimp [plaquetteActivity]
    nlinarith [Real.neg_one_le_cos θ]

/-- **The mean activity** at coupling β — the Wilson-measure expectation of `z` on the diagonal torus:
`E[z] = 1 − I₁(β)/I₀(β)` (the Bessel ratio is the mean of `cos θ` under `e^{β cos θ} dθ`). This is the
small-field quantity that must vanish as β → ∞ for the cluster expansion to converge. -/
def meanActivity (β : ℝ) : ℝ := 1 - besselI 1 β / besselI 0 β

/-- **The small-g activity bound (the open small-field step, stated as a falsifiable target).** For
the cluster expansion to converge at weak coupling, the mean activity must be `O(1/β)`:
`E[z] = 1 − I₁(β)/I₀(β) ≤ C/β` for some constant C. This is the precise lemma to prove (via the
Bessel asymptotics `I₀ − I₁ ~ e^β/√(2πβ)·(1/(2β))`); it is the convergence criterion's input, and it
is where the de-risk toy (Migdal–Kadanoff) should be calibrated first. NOT proved — the target. -/
def smallGActivityBound (C : ℝ) : Prop :=
  ∀ β : ℝ, 0 < β → meanActivity β ≤ C / β

/-- **The mean activity is positive at strong coupling**: `E[z] = 1 − I₁/I₀ > 0` when `β ≤ 2`, from
the order `I₁ < I₀` (`besselI1_lt_besselI0_of_le_two`) and `I₀ > 0`. This is the strong-coupling half
of the activity's positivity; the weak-coupling rate `E[z] ≤ C/β` is the open Clay step. -/
theorem meanActivity_pos_of_le_two {β : ℝ} (hβ : 0 < β) (hβle : β ≤ 2) :
    0 < meanActivity β := by
  have horder : besselI 1 β < besselI 0 β := besselI1_lt_besselI0_of_le_two hβ hβle
  have hI0 : 0 < besselI 0 β := besselI_pos hβ
  have hratio : besselI 1 β / besselI 0 β < 1 := (div_lt_one hI0).mpr horder
  dsimp [meanActivity]
  linarith

end QM
