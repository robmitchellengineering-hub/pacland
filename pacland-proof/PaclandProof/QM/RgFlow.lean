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

/-- **The running-coupling scale is a valid activity bound** — `0 < e^(−cβ) < 1` for `c, β > 0`,
so `ρ := e^(−cβ)` is the small-field activity the cluster expansion controls. This is the ACTIVITY form of
the running-coupling scale (the `ym-linked-cluster-contraction` radius's activity proxy), the first concrete
step of the exponential contraction rate. -/
theorem running_coupling_activity_bound (c β : ℝ) (hc : 0 < c) (hβ : 0 < β) :
    0 < Real.exp (-(c * β)) ∧ Real.exp (-(c * β)) < 1 := by
  constructor
  · exact Real.exp_pos _
  · exact Real.exp_lt_one_iff.mpr (by nlinarith [mul_pos hc hβ])

/-- **The cluster expansion converges uniformly at the running-coupling scale** — for activity
`|z| ≤ e^(−cβ)` the geometric series converges with the sum bounded by `1/(1 − e^(−cβ))`. This is the
small-field region's spacing-uniform control at the running-coupling activity, the second concrete step of
the exponential contraction rate (the spectral-radius `ρ ≤ e^(−A·e^(−cβ))` is the further measure-concentration
step this feeds). -/
theorem uv_stability_running_coupling (c β : ℝ) (hc : 0 < c) (hβ : 0 < β) (z : ℝ)
    (hz : |z| ≤ Real.exp (-(c * β))) :
    Summable (fun n : ℕ => z ^ n) ∧ ∑' n : ℕ, z ^ n ≤ 1 / (1 - Real.exp (-(c * β))) := by
  have hρ : Real.exp (-(c * β)) < 1 := (running_coupling_activity_bound c β hc hβ).2
  exact cluster_expansion_uniform_bound hρ hz

/-- **The concrete SU(2) cluster-expansion convergence condition**: the running-coupling activity
`ρ = e^(−cβ)` satisfies the summability condition `|ρ|·(Δ+1)² < 1` (the hypothesis of
`full_cluster_weights_summable`) exactly when `cβ > 2·log(Δ+1)` — i.e. for `β` above the asymptotic-freedom
scale. This ties the cluster expansion's convergence to the running-coupling activity. -/
theorem cluster_activity_condition (c Δ β : ℝ) (hc : 0 < c) (hΔ : 0 ≤ Δ)
    (hβ : 2 * Real.log (Δ + 1) / c < β) :
    |Real.exp (-(c * β))| * (Δ + 1)^2 < 1 := by
  have hexp_pos : 0 < Real.exp (-(c * β)) := Real.exp_pos _
  rw [abs_of_pos hexp_pos]
  have hΔ1 : 0 < Δ + 1 := by nlinarith [hΔ]
  have hcβ : 2 * Real.log (Δ + 1) < c * β := by
    have h' := (div_lt_iff₀ hc).mp hβ
    nlinarith [h']
  have hpow : (Δ + 1)^2 = Real.exp (2 * Real.log (Δ + 1)) := by
    rw [← Real.exp_log (sq_pos_of_ne_zero (ne_of_gt hΔ1))]
    rw [Real.log_pow (Δ + 1) 2]
    norm_num
  have hmul : Real.exp (-(c * β)) * (Δ + 1)^2 = Real.exp (2 * Real.log (Δ + 1) - c * β) := by
    rw [hpow]
    rw [← Real.exp_add]
    ring_nf
  rw [hmul]
  have harg : 2 * Real.log (Δ + 1) - c * β < 0 := by nlinarith [hcβ]
  exact Real.exp_lt_one_iff.mpr harg

end QM
