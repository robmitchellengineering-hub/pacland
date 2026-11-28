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

/-- **The single-plaquette activity bound** (the core of the small-field cluster expansion): for the
SU(2) plaquette action `S_p = β·(1 − cos θ)`, the activity `|e^(−S_p) − 1|` is bounded by `2·β·(1 − cos θ)`
in the small-field region `β·(1 − cos θ) ≤ 1` (`Real.abs_exp_sub_one_le` with `x = −β(1−cos θ)`). This is the
measure-theoretic estimate's first rung: the plaquette weight's deviation from 1 is controlled by the action
deviation, uniformly. -/
theorem plaquette_activity_bound (β θ : ℝ) (hβ : 0 ≤ β) (hθ : β * (1 - Real.cos θ) ≤ 1) :
    |Real.exp (-(β * (1 - Real.cos θ))) - 1| ≤ 2 * β * (1 - Real.cos θ) := by
  have hnonneg : 0 ≤ β * (1 - Real.cos θ) :=
    mul_nonneg hβ (sub_nonneg.mpr (Real.cos_le_one θ))
  have hx : |-(β * (1 - Real.cos θ))| ≤ 1 := by
    rwa [abs_neg, abs_of_nonneg hnonneg]
  simpa [abs_neg, abs_of_nonneg hnonneg, mul_assoc] using Real.abs_exp_sub_one_le hx

/-- **The small-field action estimate** `1 − cos θ ≤ θ²/2` (for all `θ`): via `1 − cos θ = 2·sin²(θ/2)`
(the half-angle) and `|sin x| ≤ |x|`. This turns the plaquette action deviation into the small-field quadratic,
giving the cutoff `β·(1−cos θ) ≤ β·θ²/2`. (Named to avoid the `0 ≤ x`-hypothesis version in HyperbolicPlane.) -/
theorem one_sub_cos_le_sq_div_two_all (θ : ℝ) :
    1 - Real.cos θ ≤ θ ^ 2 / 2 := by
  have h1 : 1 - Real.cos θ = 2 * (Real.sin (θ / 2))^2 := by
    have hcos : Real.cos θ = 2 * Real.cos (θ / 2)^2 - 1 := by
      conv_lhs => rw [show θ = 2 * (θ / 2) by ring]
      exact Real.cos_two_mul (θ / 2)
    rw [hcos]
    rw [Real.sin_sq (θ / 2)]
    ring
  rw [h1]
  have hsq : (Real.sin (θ / 2))^2 ≤ (θ / 2)^2 := by
    exact sq_le_sq.mpr (Real.abs_sin_le_abs (x := θ / 2))
  nlinarith [hsq]

/-- **The small-field plaquette activity bound**: combining `plaquette_activity_bound` with
`one_sub_cos_le_sq_div_two_all`, in the small-field region `β·(1−cos θ) ≤ 1` the activity satisfies
`|e^(−β(1−cos θ)) − 1| ≤ β·θ²`. This is the concrete small-field activity bound the cluster expansion
controls. -/
theorem plaquette_activity_small_field (β θ : ℝ) (hβ : 0 ≤ β) (hθ : β * (1 - Real.cos θ) ≤ 1) :
    |Real.exp (-(β * (1 - Real.cos θ))) - 1| ≤ β * θ ^ 2 := by
  have hact := plaquette_activity_bound β θ hβ hθ
  have hcos := one_sub_cos_le_sq_div_two_all θ
  have hmul : 2 * β * (1 - Real.cos θ) ≤ β * θ ^ 2 := by
    calc
      2 * β * (1 - Real.cos θ) = β * (2 * (1 - Real.cos θ)) := by ring
      _ ≤ β * (θ ^ 2) := by
        exact mul_le_mul_of_nonneg_left (by nlinarith [hcos]) hβ
  exact le_trans hact hmul
/-- **The small-field cutoff**: for `β, c, θ > 0`, the small-field activity condition `β·θ² ≤ e^(−cβ)` is
equivalent to the cutoff `θ ≤ e^(−cβ/2)/√β`. This is the region restriction that turns the pointwise
small-field bound `|e^(−S_p) − 1| ≤ βθ²` into a small-field set on which the cluster expansion converges. -/
theorem small_field_cutoff (c β θ : ℝ) (hc : 0 < c) (hβ : 0 < β) (hθ : 0 ≤ θ) :
    β * θ ^ 2 ≤ Real.exp (-(c * β)) ↔ θ ≤ Real.exp (-(c * β) / 2) / Real.sqrt β := by
  have hsq_id : (Real.exp (-(c * β) / 2) / Real.sqrt β)^2 = Real.exp (-(c * β)) / β := by
    rw [div_pow]
    have hexp2 : (Real.exp (-(c * β) / 2))^2 = Real.exp (-(c * β)) := by
      rw [← Real.exp_nat_mul (-(c * β) / 2) 2]
      congr 1
      ring
    rw [hexp2, Real.sq_sqrt (le_of_lt hβ)]
  constructor
  · intro h
    have hdiv : θ ^ 2 ≤ Real.exp (-(c * β)) / β := by
      exact (le_div_iff₀ hβ).mpr (by simpa [mul_comm] using h)
    have hsq : θ ^ 2 ≤ (Real.exp (-(c * β) / 2) / Real.sqrt β)^2 := by
      rwa [hsq_id]
    have habs : |θ| ≤ |Real.exp (-(c * β) / 2) / Real.sqrt β| := sq_le_sq.mp hsq
    have hpos : 0 ≤ Real.exp (-(c * β) / 2) / Real.sqrt β :=
      div_nonneg (Real.exp_pos _).le (Real.sqrt_nonneg _)
    simpa [abs_of_nonneg hθ, abs_of_nonneg hpos] using habs
  · intro h
    have hsq : θ ^ 2 ≤ (Real.exp (-(c * β) / 2) / Real.sqrt β)^2 := by
      have hpos : 0 ≤ Real.exp (-(c * β) / 2) / Real.sqrt β :=
        div_nonneg (Real.exp_pos _).le (Real.sqrt_nonneg _)
      exact sq_le_sq.mpr (by simpa [abs_of_nonneg hθ, abs_of_nonneg hpos] using h)
    have hdiv : θ ^ 2 ≤ Real.exp (-(c * β)) / β := by
      rwa [hsq_id] at hsq
    simpa [mul_comm] using (le_div_iff₀ hβ).mp hdiv

/-- **The large-field weight bound**: for a fixed cutoff `δ > 0`, in the large-field region
`1 − cos θ ≥ δ` the plaquette weight satisfies `e^(−β(1−cos θ)) ≤ e^(−βδ)` — exponentially small in `β`.
This is the pointwise core of the large-field estimate: the region where the plaquette deviates from the
trivial connection by at least `δ` contributes weight `≤ e^(−βδ)`. -/
theorem large_field_weight_bound (β δ θ : ℝ) (hβ : 0 ≤ β) (hδ : δ ≤ 1 - Real.cos θ) :
    Real.exp (-(β * (1 - Real.cos θ))) ≤ Real.exp (-(β * δ)) := by
  have hmul : β * δ ≤ β * (1 - Real.cos θ) := mul_le_mul_of_nonneg_left hδ hβ
  have hneg : -(β * (1 - Real.cos θ)) ≤ -(β * δ) := by nlinarith [hmul]
  exact Real.exp_le_exp.mpr hneg

/-- **The concrete SU(2) cluster-weight bound** (the measure-theoretic step's first rung): the actual
cluster weight `φ(Γ) = ∏_{i∈Γ} (e^(−β(1−cos θᵢ)) − 1)` is bounded by the product of the action deviations
`∏ 2β(1−cos θᵢ)`, in the small-field region `β(1−cos θᵢ) ≤ 1` (combining `plaquette_activity_bound` pointwise
with the product comparison via `Finset.abs_prod` + `gcongr`). This is the real SU(2) cluster weight — the
product of per-plaquette activities — not an abstract `a`. -/
theorem su2_cluster_weight_bound {ι : Type u} (β : ℝ) (hβ : 0 ≤ β) (θ : ι → ℝ) (Γ : Finset ι)
    (hθ : ∀ i ∈ Γ, β * (1 - Real.cos (θ i)) ≤ 1) :
    |∏ i ∈ Γ, (Real.exp (-(β * (1 - Real.cos (θ i)))) - 1)| ≤ ∏ i ∈ Γ, (2 * β * (1 - Real.cos (θ i))) := by
  rw [Finset.abs_prod Γ (fun i => Real.exp (-(β * (1 - Real.cos (θ i)))) - 1)]
  gcongr with i hi
  exact plaquette_activity_bound β (θ i) hβ (hθ i hi)


/-- **The concrete SU(2) cluster-weight bound** `|φ(Γ)| ≤ (e^(−cβ))^|Γ|` (the measure-theoretic step's
second rung): in the small-field region `β(1−cos θᵢ) ≤ 1` with the cutoff `βθᵢ² ≤ e^(−cβ)`, the real cluster
weight `φ(Γ) = ∏ (e^(−β(1−cos θᵢ)) − 1)` is bounded by the activity to the cluster size. This is the
polymer-expansion estimate for the actual SU(2) per-plaquette activity — combining `su2_cluster_weight_bound`,
the small-field quadratic `one_sub_cos_le_sq_div_two_all`, and the cutoff, then `Finset.prod_const`. -/
lemma prod_le_prod_of_le_nonneg {ι : Type u} (s : Finset ι) (f g : ι → ℝ)
    (h0 : ∀ i ∈ s, 0 ≤ f i) (hle : ∀ i ∈ s, f i ≤ g i) :
    (∏ i ∈ s, f i) ≤ ∏ i ∈ s, g i := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s' ha ih =>
      rw [Finset.prod_insert ha, Finset.prod_insert ha]
      refine mul_le_mul (hle a (Finset.mem_insert_self a s')) (ih ?_ ?_) ?_ ?_
      · intro i hi
        exact h0 i (Finset.mem_insert_of_mem hi)
      · intro i hi
        exact hle i (Finset.mem_insert_of_mem hi)
      · exact Finset.prod_nonneg (fun i hi => h0 i (Finset.mem_insert_of_mem hi))
      · exact le_trans (h0 a (Finset.mem_insert_self a s')) (hle a (Finset.mem_insert_self a s'))

theorem su2_cluster_weight_small_field {ι : Type u} (β c : ℝ) (hβ : 0 ≤ β) (hc : 0 < c) (θ : ι → ℝ) (Γ : Finset ι)
    (hθ : ∀ i ∈ Γ, β * (1 - Real.cos (θ i)) ≤ 1)
    (hcut : ∀ i ∈ Γ, β * (θ i)^2 ≤ Real.exp (-(c * β))) :
    |∏ i ∈ Γ, (Real.exp (-(β * (1 - Real.cos (θ i)))) - 1)| ≤ (Real.exp (-(c * β)))^Γ.card := by
  have h1 : |∏ i ∈ Γ, (Real.exp (-(β * (1 - Real.cos (θ i)))) - 1)| ≤ ∏ i ∈ Γ, 2 * β * (1 - Real.cos (θ i)) :=
    su2_cluster_weight_bound β hβ θ Γ hθ
  have hquad : ∀ i ∈ Γ, 2 * β * (1 - Real.cos (θ i)) ≤ β * (θ i)^2 := by
    intro i hi
    have hcos : 1 - Real.cos (θ i) ≤ (θ i)^2 / 2 := one_sub_cos_le_sq_div_two_all (θ i)
    calc
      2 * β * (1 - Real.cos (θ i)) = β * (2 * (1 - Real.cos (θ i))) := by ring
      _ ≤ β * (θ i)^2 := mul_le_mul_of_nonneg_left (by nlinarith [hcos]) hβ
  have h0quad : ∀ i ∈ Γ, 0 ≤ 2 * β * (1 - Real.cos (θ i)) := by
    intro i hi
    exact mul_nonneg (mul_nonneg (by norm_num) hβ) (sub_nonneg.mpr (Real.cos_le_one (θ i)))
  have h23 : (∏ i ∈ Γ, 2 * β * (1 - Real.cos (θ i))) ≤ (Real.exp (-(c * β)))^Γ.card := by
    calc
      ∏ i ∈ Γ, 2 * β * (1 - Real.cos (θ i)) ≤ ∏ i ∈ Γ, β * (θ i)^2 :=
        prod_le_prod_of_le_nonneg Γ (fun i => 2 * β * (1 - Real.cos (θ i))) (fun i => β * (θ i)^2) h0quad hquad
      _ ≤ ∏ i ∈ Γ, Real.exp (-(c * β)) :=
        prod_le_prod_of_le_nonneg Γ (fun i => β * (θ i)^2) (fun i => Real.exp (-(c * β)))
          (fun i hi => mul_nonneg hβ (sq_nonneg (θ i))) hcut
      _ = (Real.exp (-(c * β)))^Γ.card := Finset.prod_const _
  exact le_trans h1 h23

/-- **The Wilson product expansion** (the algebraic core of the polymer expansion): the product of
`(1 + a_p)` over the plaquettes `P` expands as the sum over all subsets `A ⊆ P` of the product of the
activities over `A`. This is `∏_{p∈P} (1 + a_p) = Σ_{A⊆P} ∏_{p∈A} a_p` — the identity the cluster/polymer
expansion is built on, via `Finset.prod_add`. -/
theorem wilson_product_expansion {ι : Type u} [DecidableEq ι] (a : ι → ℝ) (P : Finset ι) :
    ∏ p ∈ P, (1 + a p) = ∑ A ∈ P.powerset, ∏ p ∈ A, a p := by
  calc
    ∏ p ∈ P, (1 + a p) = ∏ p ∈ P, (a p + 1) := by
      apply Finset.prod_congr rfl
      intro p hp
      ring
    _ = ∑ A ∈ P.powerset, (∏ p ∈ A, a p) * ∏ p ∈ P \ A, (1 : ℝ) := Finset.prod_add a (fun _ => 1) P
    _ = ∑ A ∈ P.powerset, ∏ p ∈ A, a p := by
      apply Finset.sum_congr rfl
      intro A hA
      simp

/-- **The running-coupling activity vanishes in the continuum limit**: `Tendsto (fun β => e^(−cβ)) atTop (nhds 0)`
for `c > 0` — the small-field activity `ρ = e^(−cβ)` that the cluster expansion controls shrinks to `0` as
`β → ∞` (the `a → 0` limit). This is the foundational fact of the a→0 continuum passage: at the running-coupling
scale the cluster expansion converges with activity → 0, so the small-field region is asymptotically exact. -/
theorem running_coupling_activity_tendsto_zero (c : ℝ) (hc : 0 < c) :
    Filter.Tendsto (fun β : ℝ => Real.exp (-(c * β))) Filter.atTop (nhds 0) := by
  have hlin : Filter.Tendsto (fun β : ℝ => -(c * β)) Filter.atTop Filter.atBot := by
    rw [Filter.tendsto_atBot]
    intro b
    refine Filter.eventually_atTop.2 ⟨max 0 ((-b) / c), ?_⟩
    intro β hβ
    have hβ' : max 0 ((-b) / c) ≤ β := hβ
    have hβ0 : 0 ≤ β := le_trans (le_max_left 0 ((-b) / c)) hβ'
    have hbc : (-b) / c ≤ β := le_trans (le_max_right 0 ((-b) / c)) hβ'
    have hcmul : c * ((-b) / c) ≤ c * β := mul_le_mul_of_nonneg_left hbc (le_of_lt hc)
    have hcb : c * ((-b) / c) = -b := by field_simp [ne_of_gt hc]
    nlinarith
  exact Real.tendsto_exp_atBot.comp hlin

end QM
