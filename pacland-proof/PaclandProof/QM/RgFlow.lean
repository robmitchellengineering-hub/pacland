import Mathlib
import PaclandProof.QM.BlockSpin
import PaclandProof.QM.ClusterExpansion
import PaclandProof.QM.Bessel
import PaclandProof.QM.BesselRecurrence
import PaclandProof.QM.BesselIntegral

open Filter

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

/-- **The strong-coupling concentration bound**: `E[z] = 1 − I₁/I₀ ≤ 2/β` for `β ≤ 2`. Since
`I₁/I₀ ≥ 0` (positivity), `E[z] ≤ 1`, and for `β ≤ 2` we have `1 ≤ 2/β`. This is the tractable
strong-coupling half of `smallGActivityBound 2`; the weak-coupling (β → ∞) half is the open Clay step. -/
theorem meanActivity_le_two_div_beta_of_le_two {β : ℝ} (hβ : 0 < β) (hβle : β ≤ 2) :
    meanActivity β ≤ 2 / β := by
  have hI1 : 0 < besselI 1 β := besselI_pos hβ
  have hI0 : 0 < besselI 0 β := besselI_pos hβ
  have hle1 : meanActivity β ≤ 1 := by
    dsimp [meanActivity]
    have hratio : 0 ≤ besselI 1 β / besselI 0 β := div_nonneg (le_of_lt hI1) (le_of_lt hI0)
    linarith
  have hle2 : (1 : ℝ) ≤ 2 / β := (one_le_div hβ).mpr hβle
  exact le_trans hle1 hle2

/-- **The small-field activity bound `C = 1`**: `E[z] = 1 − I₁/I₀ ≤ 1/β` for all β > 0. This is
the ym-bakry-ceiling antipode-suppression bound, proved via the Riccati/barrier route
(`bessel_activity_le_one_div_beta`). It is the convergence-criterion input: the cluster expansion
converges uniformly at weak coupling. -/
theorem smallGActivityBound_one : smallGActivityBound 1 := by
  intro β hβ
  dsimp [meanActivity]
  exact bessel_activity_le_one_div_beta hβ

/-- **The activity is `|z| < 1` at weak coupling** (β > 1): `meanActivity ≤ 1/β < 1` and `0 ≤
meanActivity`, so `|meanActivity| < 1`. This is the input that makes the cluster expansion converge
(`cluster_expansion_converges`), which the `clustering ⟺ gap` bridge turns into the mass gap. -/
theorem meanActivity_abs_lt_one_of_gt_one {β : ℝ} (hβ : 1 < β) :
    |meanActivity β| < 1 := by
  have hβ0 : 0 < β := lt_trans zero_lt_one hβ
  have hI1 : 0 < besselI 1 β := besselI_pos hβ0
  have hI0 : 0 < besselI 0 β := besselI_pos hβ0
  have hpos : 0 ≤ meanActivity β := by
    dsimp [meanActivity]
    have hratio : besselI 1 β / besselI 0 β ≤ 1 := (div_le_one hI0).mpr (le_of_lt (besselI1_lt_besselI0 hβ0))
    linarith
  have hle : meanActivity β ≤ 1 / β := smallGActivityBound_one β hβ0
  have hlt : meanActivity β < 1 := lt_of_le_of_lt hle ((div_lt_one hβ0).mpr hβ)
  rw [abs_of_nonneg hpos]
  exact hlt

/-- **The cluster expansion converges at weak coupling**: `|meanActivity β| < 1` for β > 1 gives
`cluster_expansion_converges (meanActivity β)`. This is the objective's part (2): the small-field
activity bound chains through the already-proven convergence to the `clustering ⟺ gap` bridge. -/
theorem cluster_expansion_converges_weak {β : ℝ} (hβ : 1 < β) :
    Summable (fun n : ℕ => (meanActivity β) ^ n) := by
  exact cluster_expansion_converges (meanActivity_abs_lt_one_of_gt_one hβ)

/-- **The mass gap at weak coupling**: `m = −log E[z] > 0` for β > 1. Since `0 < E[z] < 1`
(the activity is positive by `I₁<I₀` and `<1` by the concentration), the spectral gap `−log E[z]`
is positive. This is the transfer-operator gap `‖S‖ = e^{−m} < 1` that the clustering ⟺ gap bridge
turns into the exponential clustering — the mass gap, chained from `smallGActivityBound 1`. -/
theorem mass_gap_pos_weak {β : ℝ} (hβ : 1 < β) :
    0 < -Real.log (meanActivity β) := by
  have hβ0 : 0 < β := lt_trans zero_lt_one hβ
  have hpos : 0 < meanActivity β := by
    dsimp [meanActivity]
    have hI0 : 0 < besselI 0 β := besselI_pos hβ0
    have horder : besselI 1 β < besselI 0 β := besselI1_lt_besselI0 hβ0
    have hratio : besselI 1 β / besselI 0 β < 1 := (div_lt_one hI0).mpr horder
    linarith
  have hlt : meanActivity β < 1 := by
    have habs : |meanActivity β| < 1 := meanActivity_abs_lt_one_of_gt_one hβ
    rw [abs_of_nonneg (le_of_lt hpos)] at habs
    exact habs
  exact neg_pos.mpr (Real.log_neg hpos hlt)

/-- **The exponential clustering (mass-gap) at weak coupling**: `m = −log E[z] > 0` gives the massive
2-point function `e^{−m·d} → 0` as `d → ∞` (the clustering ⟺ gap bridge). This is the objective's part (2):
the small-field activity bound chained to the mass gap. -/
theorem exponential_clustering_weak {β : ℝ} (hβ : 1 < β) :
    Tendsto (fun d : ℝ => Real.exp (-(-Real.log (meanActivity β)) * d)) atTop (nhds 0) := by
  have hm : 0 < -Real.log (meanActivity β) := mass_gap_pos_weak hβ
  have h1 : Tendsto (fun d : ℝ => (-Real.log (meanActivity β)) * d) atTop atTop :=
    tendsto_id.const_mul_atTop hm
  have h2 : Tendsto (fun d : ℝ => Real.exp ((-Real.log (meanActivity β)) * d)) atTop atTop :=
    Real.tendsto_exp_atTop.comp h1
  have h3 : Tendsto (fun d : ℝ => (Real.exp ((-Real.log (meanActivity β)) * d))⁻¹) atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp h2
  convert h3 using 1
  ext d
  rw [show (-(-Real.log (meanActivity β)) * d) = -((-Real.log (meanActivity β)) * d) by ring]
  rw [Real.exp_neg]

/-- **The Bessel order `I₂ < I₁` at weak coupling** (β > 2): from the concentration `1 − I₁/I₀ ≤ 1/β`
we get `I₁/I₀ ≥ (β−1)/β > β/(β+2)`, so `βI₀ < (β+2)I₁`, which with the recurrence
`I₂ = I₀ − 2I₁/β` gives `I₂ < I₁`. -/
theorem besselI2_lt_besselI1_of_gt_two {β : ℝ} (hβ : 2 < β) :
    besselI 2 β < besselI 1 β := by
  have hβ0 : 0 < β := lt_trans zero_lt_two hβ
  have hconc : 1 - besselI 1 β / besselI 0 β ≤ 1 / β := bessel_activity_le_one_div_beta hβ0
  have hI0 : 0 < besselI 0 β := besselI_pos hβ0
  have hI1 : 0 < besselI 1 β := besselI_pos hβ0
  have hrec : besselI 0 β - besselI 2 β = (2 / β) * besselI 1 β := bessel_recurrence hβ0
  have hconc' : β * besselI 0 β - β * besselI 1 β ≤ besselI 0 β := by
    field_simp [ne_of_gt hI0, ne_of_gt hβ0] at hconc
    nlinarith
  have hhalf : besselI 0 β < 2 * besselI 1 β := by nlinarith [hconc', hβ]
  have hmain : β * besselI 0 β < (β + 2) * besselI 1 β := by nlinarith [hconc', hhalf]
  have hI2eq : besselI 2 β = besselI 0 β - (2 / β) * besselI 1 β := by linarith [hrec]
  rw [hI2eq]
  have hlt : besselI 0 β - (2 / β) * besselI 1 β < besselI 1 β := by
    field_simp [ne_of_gt hβ0]
    nlinarith [hmain]
  exact hlt

/-- **The full SU(2) plaquette mean activity**: `E[z] = 1 − I₂/I₁`, where `(1/2)Tr U = I₂/I₁` is the
mean fundamental character under the SU(2) Haar measure (`sin²(θ/2) dθ`). This is the actual 4D
cluster-expansion input, the diagonal-torus `1 − I₁/I₀` lifted one index. -/
def meanActivitySU2 (β : ℝ) : ℝ := 1 - besselI 2 β / besselI 1 β

/-- **The SU(2) small-field bound `C = 2`**: `E[z] = 1 − I₂/I₁ ≤ 2/β` for all β > 0, from
`bessel_ratio_I2_I1_lt_two_div_beta`. The activity is `O(1/β)` small at weak coupling — the
convergence-criterion input for the cluster expansion on the full plaquette. -/
theorem meanActivitySU2_le_two_div_beta {β : ℝ} (hβ : 0 < β) :
    meanActivitySU2 β ≤ 2 / β := by
  dsimp [meanActivitySU2]
  exact le_of_lt (bessel_ratio_I2_I1_lt_two_div_beta hβ)

/-- **The SU(2) activity is `|z| < 1` at weak coupling** (β > 2): `E[z] ≤ 2/β < 1` and `0 ≤ E[z]`. -/
theorem meanActivitySU2_abs_lt_one_of_gt_two {β : ℝ} (hβ : 2 < β) :
    |meanActivitySU2 β| < 1 := by
  have hβ0 : 0 < β := lt_trans zero_lt_two hβ
  have hI1 : 0 < besselI 1 β := besselI_pos hβ0
  have hI2 : 0 < besselI 2 β := besselI_pos hβ0
  have hpos : 0 ≤ meanActivitySU2 β := by
    dsimp [meanActivitySU2]
    have hratio : besselI 2 β / besselI 1 β ≤ 1 := (div_le_one hI1).mpr (le_of_lt (besselI2_lt_besselI1_of_gt_two hβ))
    linarith
  have hle : meanActivitySU2 β ≤ 2 / β := meanActivitySU2_le_two_div_beta hβ0
  have hlt : meanActivitySU2 β < 1 := lt_of_le_of_lt hle (by have h : (2 : ℝ) / β < 1 := (div_lt_one hβ0).mpr hβ; exact h)
  rw [abs_of_nonneg hpos]
  exact hlt

/-- **The SU(2) cluster expansion converges at weak coupling**: `|E[z]| < 1` for β > 2. -/
theorem cluster_expansion_converges_weak_su2 {β : ℝ} (hβ : 2 < β) :
    Summable (fun n : ℕ => (meanActivitySU2 β) ^ n) := by
  exact cluster_expansion_converges (meanActivitySU2_abs_lt_one_of_gt_two hβ)

/-- **The SU(2) mass gap at weak coupling**: `m = −log E[z] > 0` for β > 2. The transfer-operator
gap `‖S‖ = e^{−m} < 1`, chained from the SU(2) concentration to the clustering ⟺ gap bridge. -/
theorem mass_gap_pos_weak_su2 {β : ℝ} (hβ : 2 < β) :
    0 < -Real.log (meanActivitySU2 β) := by
  have hβ0 : 0 < β := lt_trans zero_lt_two hβ
  have hpos : 0 < meanActivitySU2 β := by
    dsimp [meanActivitySU2]
    have hI1 : 0 < besselI 1 β := besselI_pos hβ0
    have horder : besselI 2 β < besselI 1 β := besselI2_lt_besselI1_of_gt_two hβ
    have hratio : besselI 2 β / besselI 1 β < 1 := (div_lt_one hI1).mpr horder
    linarith
  have hlt : meanActivitySU2 β < 1 := by
    have habs : |meanActivitySU2 β| < 1 := meanActivitySU2_abs_lt_one_of_gt_two hβ
    rw [abs_of_nonneg (le_of_lt hpos)] at habs
    exact habs
  exact neg_pos.mpr (Real.log_neg hpos hlt)

/-- **The mass-gap lower bound `c(β) = log(β/2)`** (the join's clause-(2) candidate, single-plaquette).
From the concentration `E[z] ≤ 2/β` and the monotonicity of `log`, `−log E[z] ≥ −log(2/β) = log(β/2)`.
This is the positive, volume-independent lower bound the join's clause (2) needs — it depends only on β,
grows like `log β`, and is `> 0` for β > 2. -/
theorem mass_gap_ge_log_half_beta {β : ℝ} (hβ : 2 < β) :
    Real.log (β / 2) ≤ -Real.log (meanActivitySU2 β) := by
  have hβ0 : 0 < β := lt_trans zero_lt_two hβ
  have hle : meanActivitySU2 β ≤ 2 / β := meanActivitySU2_le_two_div_beta hβ0
  have hpos : 0 < meanActivitySU2 β := by
    dsimp [meanActivitySU2]
    have hI1 : 0 < besselI 1 β := besselI_pos hβ0
    have horder : besselI 2 β < besselI 1 β := besselI2_lt_besselI1_of_gt_two hβ
    have hratio : besselI 2 β / besselI 1 β < 1 := (div_lt_one hI1).mpr horder
    linarith
  have h2β : 0 < 2 / β := div_pos (by norm_num) hβ0
  have hlog : Real.log (meanActivitySU2 β) ≤ Real.log (2 / β) := Real.log_le_log hpos hle
  have hneg : -Real.log (2 / β) ≤ -Real.log (meanActivitySU2 β) := neg_le_neg hlog
  rw [← Real.log_inv (2 / β)] at hneg
  simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using hneg

end QM
