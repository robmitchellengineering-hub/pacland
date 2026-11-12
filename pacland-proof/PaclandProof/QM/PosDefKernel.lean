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
/-- **PSD is closed under finite sums**: the pointwise sum of finitely many PSD kernels is PSD. -/
theorem posdef_sum {α : Type*} [Fintype α] {ι : Type*} [Fintype ι]
    (K : ι → α → α → ℝ) (hK : ∀ i, PosDefKernel (K i)) :
    PosDefKernel (fun a b => ∑ i, K i a b) := by
  classical
  have h : ∀ s : Finset ι, PosDefKernel (fun a b => ∑ i ∈ s, K i a b) := by
    intro s
    refine Finset.induction_on s ?_ ?_
    · intro c
      simp
    · intro x s hx ih
      intro c
      simp_rw [Finset.sum_insert hx]
      simp_rw [mul_add, Finset.sum_add_distrib]
      exact add_nonneg (hK x c) (ih c)
  simpa using (h Finset.univ)
end QM
