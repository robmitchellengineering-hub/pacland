import Mathlib
import PaclandProof.QM.ReflectionPositivity

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Positive-definite kernels and their closure

The reflection positivity (OS3) of the Wilson heat kernel `exp(2β·cos θ)` is the statement that it is
a positive-definite kernel. The closure facts here — PSD is closed under addition and non-negative
scaling — are the machinery that lifts the cosine-kernel positive-definiteness (#500) to the
truncated heat kernel `Σ (2β)^n/n!·cos^n`.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- A positive-definite kernel on a finite type: `Σ c_i c_j K(i,j) ≥ 0` for all coefficients. -/
def PosDefKernel {α : Type*} [Fintype α] (K : α → α → ℝ) : Prop :=
  ∀ c : α → ℝ, 0 ≤ ∑ i, ∑ j, c i * c j * K i j

/-- **PSD is closed under addition**: the pointwise sum of two positive-definite kernels is PSD. -/
theorem posdef_add {α : Type*} [Fintype α] (K L : α → α → ℝ)
    (hK : PosDefKernel K) (hL : PosDefKernel L) : PosDefKernel (fun a b => K a b + L a b) := by
  intro c
  have h : (∑ a, ∑ b, c a * c b * (K a b + L a b)) = (∑ a, ∑ b, c a * c b * K a b) + (∑ a, ∑ b, c a * c b * L a b) := by
    simp_rw [mul_add, Finset.sum_add_distrib]
  rw [h]
  exact add_nonneg (hK c) (hL c)

/-- **PSD is closed under non-negative scaling**: `w·K` is PSD for `w ≥ 0`. -/
theorem posdef_smul {α : Type*} [Fintype α] (K : α → α → ℝ) (w : ℝ) (hw : 0 ≤ w)
    (hK : PosDefKernel K) : PosDefKernel (fun a b => w * K a b) := by
  intro c
  have h : (∑ a, ∑ b, c a * c b * (w * K a b)) = w * (∑ a, ∑ b, c a * c b * K a b) := by
    simp_rw [mul_assoc, mul_left_comm, mul_comm, Finset.mul_sum]
  rw [h]
  exact mul_nonneg hw (hK c)

/-- **PSD is closed under finite sums**: the pointwise sum of a finite family of PSD kernels is PSD. -/
theorem posdef_sum {α ι : Type*} [Fintype α] [Fintype ι] (K : ι → α → α → ℝ)
    (hK : ∀ n, PosDefKernel (K n)) : PosDefKernel (fun i j => ∑ n, K n i j) := by
  intro c
  have h : 0 ≤ ∑ n, ∑ i, ∑ j, c i * c j * K n i j :=
    Finset.sum_nonneg (fun n _ => (hK n) c)
  have hsum : (∑ i, ∑ j, c i * c j * (∑ n, K n i j)) = ∑ n, ∑ i, ∑ j, c i * c j * K n i j := by
    calc
      (∑ i, ∑ j, c i * c j * (∑ n, K n i j))
        = ∑ i, ∑ j, ∑ n, c i * c j * K n i j := by simp_rw [Finset.mul_sum]
      _ = ∑ i, ∑ n, ∑ j, c i * c j * K n i j := by
          congr 1; ext i; rw [Finset.sum_comm]
      _ = ∑ n, ∑ i, ∑ j, c i * c j * K n i j := by rw [Finset.sum_comm]
  rw [hsum]
  exact h

/-- **PSD is closed under pointwise limits**: the pointwise limit of PSD kernels is PSD. -/
theorem posdef_of_tendsto {α : Type*} [Fintype α] (K : ℕ → α → α → ℝ) (Klim : α → α → ℝ)
    (h : ∀ i j, Filter.Tendsto (fun n => K n i j) Filter.atTop (nhds (Klim i j)))
    (hK : ∀ n, PosDefKernel (K n)) : PosDefKernel Klim := by
  intro c
  have hsum : Filter.Tendsto (fun n => ∑ i : α, ∑ j : α, c i * c j * K n i j) Filter.atTop (nhds (∑ i : α, ∑ j : α, c i * c j * Klim i j)) := by
    apply tendsto_finsetSum
    intro i _
    apply tendsto_finsetSum
    intro j _
    exact (h i j).const_mul (c i * c j)
  exact ge_of_tendsto hsum (Filter.Eventually.of_forall (fun n => hK n c))

/-- **The rank-one kernel as a `PosDefKernel`** (from the direct `rank_one_posdef`). -/
theorem rank_one_posdef_kernel {α : Type*} [Fintype α] (f : α → ℝ) :
    PosDefKernel (fun i j => f i * f j) := fun c => rank_one_posdef f c

/-- **cos(θᵢ−θⱼ)ⁿ is positive-definite** — the binomial rank-one expansion (cos_pow_rankone), each term
`(n choose k)·|Σ cᵢ fₖ(θᵢ)|² ≥ 0`, so the finite positive sum is PSD (posdef_sum/posdef_smul over the
`Fin (n+1)`). The finite Fubini replaces the Chebyshev reindexing. -/
theorem cos_pow_posdef {m : ℕ} (θ : Fin m → ℝ) (n : ℕ) :
    PosDefKernel (fun i j => (Real.cos (θ i - θ j)) ^ n) := by
  have hid : (fun i j => (Real.cos (θ i - θ j)) ^ n)
      = (fun i j => ∑ k : Fin (n + 1), (n.choose k.1 : ℝ) * ((Real.cos (θ i) ^ k.1 * Real.sin (θ i) ^ (n - k.1)) * (Real.cos (θ j) ^ k.1 * Real.sin (θ j) ^ (n - k.1)))) := by
    funext i j
    rw [cos_pow_rankone n (θ i) (θ j)]
    rw [← Fin.sum_univ_eq_sum_range]
    apply Finset.sum_congr rfl
    intro k hk
    ring_nf
  rw [hid]
  exact posdef_sum (fun k : Fin (n + 1) => fun i j => (n.choose k.1 : ℝ) * ((Real.cos (θ i) ^ k.1 * Real.sin (θ i) ^ (n - k.1)) * (Real.cos (θ j) ^ k.1 * Real.sin (θ j) ^ (n - k.1))))
    (fun k => posdef_smul (fun i j => (Real.cos (θ i) ^ k.1 * Real.sin (θ i) ^ (n - k.1)) * (Real.cos (θ j) ^ k.1 * Real.sin (θ j) ^ (n - k.1))) (n.choose k.1 : ℝ) (by positivity) (rank_one_posdef_kernel (fun i => Real.cos (θ i) ^ k.1 * Real.sin (θ i) ^ (n - k.1))))

set_option maxHeartbeats 800000 in
/-- **The Wilson heat kernel is positive-definite** (the OS reflection positivity of the SU(2) Wilson
measure): `exp(2β·cos(θᵢ−θⱼ))` is the pointwise limit of the exponential partial sums
`Σ_{n<N} (2β)ⁿ/n!·cosⁿ(θᵢ−θⱼ)`, each PSD by `cos_pow_posdef` + `posdef_smul`, and the pointwise limit
of PSD kernels is PSD (`posdef_of_tendsto`). The infinite sum is handled by the finite partial-sum
limit, not a `tsum` reindexing. -/
theorem wilson_kernel_posdef {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) :
    PosDefKernel (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) := by
  intro c
  let xij : Fin m → Fin m → ℝ := fun i j => 2 * β * Real.cos (θ i - θ j)
  have hlim : ∀ i j, Filter.Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (xij i j)^n / (n.factorial : ℝ)) Filter.atTop (nhds (Real.exp (xij i j))) := by
    intro i j
    have hsum : Summable (fun n : ℕ => (xij i j)^n / (n.factorial : ℝ)) := Real.summable_pow_div_factorial (xij i j)
    have hhas : HasSum (fun n : ℕ => (xij i j)^n / (n.factorial : ℝ)) (Real.exp (xij i j)) := by
      have htsum : Real.exp (xij i j) = ∑' n : ℕ, (xij i j)^n / (n.factorial : ℝ) := by
        have h1 : NormedSpace.exp (𝔸 := ℝ) (xij i j) = ∑' n : ℕ, (n.factorial : ℝ)⁻¹ • (xij i j)^n := by
          rw [NormedSpace.exp_eq_tsum ℝ]
        have h2 : NormedSpace.exp (𝔸 := ℝ) (xij i j) = Real.exp (xij i j) := congr_fun Real.exp_eq_exp_ℝ.symm (xij i j)
        rw [← h2, h1]
        apply tsum_congr
        intro n
        simp [div_eq_mul_inv, mul_comm]
      rw [htsum]
      exact hsum.hasSum
    exact hhas.tendsto_sum_nat
  have hK : ∀ N : ℕ, PosDefKernel (fun i j => ∑ n ∈ Finset.range N, (xij i j)^n / (n.factorial : ℝ)) := by
    intro N
    have hrewrite : (fun i j => ∑ n ∈ Finset.range N, (xij i j)^n / (n.factorial : ℝ)) = fun i j => ∑ n ∈ Finset.range N, ((2 * β)^n / (n.factorial : ℝ)) * (Real.cos (θ i - θ j))^n := by
      funext i j
      dsimp [xij]
      apply Finset.sum_congr rfl
      intro n hn
      rw [mul_pow]
      ring
    rw [hrewrite]
    have hfin : (fun i j => ∑ n ∈ Finset.range N, ((2 * β)^n / (n.factorial : ℝ)) * (Real.cos (θ i - θ j))^n) = fun i j => ∑ n : Fin N, ((2 * β)^(n.1) / (n.1.factorial : ℝ)) * (Real.cos (θ i - θ j))^(n.1) := by
      funext i j
      rw [← Fin.sum_univ_eq_sum_range]
    rw [hfin]
    exact posdef_sum (fun n : Fin N => fun i j => ((2 * β)^(n.1) / (n.1.factorial : ℝ)) * (Real.cos (θ i - θ j))^(n.1))
      (fun n => posdef_smul (fun i j => (Real.cos (θ i - θ j))^(n.1)) ((2 * β)^(n.1) / (n.1.factorial : ℝ))
        (by exact div_nonneg (pow_nonneg (mul_nonneg (by norm_num : 0 ≤ (2 : ℝ)) hβ) _) (Nat.cast_nonneg _)) (cos_pow_posdef θ n.1))
  simpa [xij] using ((posdef_of_tendsto (fun N => fun i j => ∑ n ∈ Finset.range N, (xij i j)^n / (n.factorial : ℝ)) (fun i j => Real.exp (xij i j)) hlim hK) c)

end QM
