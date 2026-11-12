import Mathlib
import PaclandProof.QM.PosDefKernel
import PaclandProof.QM.ReflectionPositivity

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Powers of the cosine kernel are positive-definite (the multi-angle input)

The Wilson heat kernel `exp(2β·cos θ)` is a power series in the cosine kernel. This file proves the
building blocks: the constant kernel, the doubled-angle cosine kernel, the square, and the product of
two cosine kernels are all positive-definite. Together with the closure facts (#501), this lifts the
cosine-kernel positivity (#500) toward the full heat kernel.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The product-to-sum identity: `cos a · cos b = (cos(a+b) + cos(a−b))/2`. -/
theorem cos_mul_cos (a b : ℝ) : Real.cos a * Real.cos b = (Real.cos (a + b) + Real.cos (a - b)) / 2 := by
  have h1 := Real.cos_add a b
  have h2 := Real.cos_sub a b
  linarith

/-- The constant kernel is positive-definite: `Σ c_i c_j = (Σ c_i)² ≥ 0`. -/
theorem const_kernel_posdef {α : Type*} [Fintype α] : PosDefKernel (fun _ _ : α => (1 : ℝ)) := by
  intro c
  have h : (∑ i : α, ∑ j : α, c i * c j * (1 : ℝ)) = (∑ i : α, c i)^2 := by
    rw [pow_two]
    rw [Finset.sum_mul_sum]
    simp
  rw [h]
  exact sq_nonneg _

/-- The cosine kernel with a doubled angle is positive-definite (via #500). -/
theorem cos_double_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => Real.cos (2 * (θ i - θ j))) := by
  intro c
  have h : (∑ i, ∑ j, c i * c j * Real.cos (2 * (θ i - θ j))) = ∑ i, ∑ j, c i * c j * Real.cos ((2 * θ i) - (2 * θ j)) := by
    simp_rw [mul_sub]
  rw [h]
  exact cos_kernel_posdef (fun i => 2 * θ i) c

/-- **The square of the cosine kernel is positive-definite** — the double-angle turns `cos²` into
the positive combination `(1 + cos(2θ))/2`. -/
theorem cos_sq_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => (Real.cos (θ i - θ j))^2) := by
  have heq : (fun i j => (Real.cos (θ i - θ j))^2) = fun i j => (1 / 2) * ((1 : ℝ) + Real.cos (2 * (θ i - θ j))) := by
    funext i j
    rw [Real.cos_sq]
    ring
  rw [heq]
  exact posdef_smul (fun i j => (1 : ℝ) + Real.cos (2 * (θ i - θ j))) (1 / 2) (by norm_num)
    (posdef_add (fun _ _ : Fin m => (1 : ℝ)) (fun i j => Real.cos (2 * (θ i - θ j))) const_kernel_posdef (cos_double_posdef θ))

/-- **The pointwise product of two cosine kernels is positive-definite**: the product-to-sum turns
`cos(θ_i−θ_j)·cos(φ_i−φ_j)` into the positive combination of two cosine kernels. -/
theorem cos_product_posdef {m : ℕ} (θ φ : Fin m → ℝ) :
    PosDefKernel (fun i j => Real.cos (θ i - θ j) * Real.cos (φ i - φ j)) := by
  have hsum : PosDefKernel (fun i j => Real.cos ((θ i + φ i) - (θ j + φ j)) + Real.cos ((θ i - φ i) - (θ j - φ j))) := by
    exact posdef_add (fun i j => Real.cos ((θ i + φ i) - (θ j + φ j))) (fun i j => Real.cos ((θ i - φ i) - (θ j - φ j)))
      (cos_kernel_posdef (fun i => θ i + φ i))
      (cos_kernel_posdef (fun i => θ i - φ i))
  have heq : (fun i j => Real.cos (θ i - θ j) * Real.cos (φ i - φ j)) = fun i j => (1 / 2) * (Real.cos ((θ i + φ i) - (θ j + φ j)) + Real.cos ((θ i - φ i) - (θ j - φ j))) := by
    funext i j
    rw [cos_mul_cos]
    ring
  rw [heq]
  exact posdef_smul (fun i j => Real.cos ((θ i + φ i) - (θ j + φ j)) + Real.cos ((θ i - φ i) - (θ j - φ j))) (1 / 2) (by norm_num) hsum

/-- **The truncated Wilson heat kernel is positive-definite** (the OS3 reflection positivity, first
three terms): `1 + 2β·cos + 2β²·cos²` is PSD for `β ≥ 0`, as a non-negative combination of the
positive-definite constant, cosine, and cosine-squared kernels. -/
theorem heat_kernel_truncated_posdef {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) :
    PosDefKernel (fun i j => (1 : ℝ) + (2 * β) * Real.cos (θ i - θ j) + ((2 * β)^2 / 2) * (Real.cos (θ i - θ j))^2) := by
  let K₁ : Fin m → Fin m → ℝ := fun _ _ => (1 : ℝ)
  let K₂ : Fin m → Fin m → ℝ := fun i j => Real.cos (θ i - θ j)
  let K₃ : Fin m → Fin m → ℝ := fun i j => (Real.cos (θ i - θ j))^2
  have hK₁ : PosDefKernel K₁ := by dsimp [K₁]; exact const_kernel_posdef
  have hK₂ : PosDefKernel K₂ := by dsimp [K₂]; exact cos_kernel_posdef θ
  have hK₃ : PosDefKernel K₃ := by dsimp [K₃]; exact cos_sq_posdef θ
  have h1 : PosDefKernel (fun i j => (1 : ℝ) + (2 * β) * K₂ i j) := by
    exact posdef_add K₁ (fun i j => (2 * β) * K₂ i j) hK₁ (posdef_smul K₂ (2 * β) (by nlinarith [hβ]) hK₂)
  have h2 : PosDefKernel (fun i j => (1 : ℝ) + (2 * β) * K₂ i j + ((2 * β)^2 / 2) * K₃ i j) := by
    exact posdef_add (fun i j => (1 : ℝ) + (2 * β) * K₂ i j) (fun i j => ((2 * β)^2 / 2) * K₃ i j) h1
      (posdef_smul K₃ ((2 * β)^2 / 2) (by positivity) hK₃)
  simpa [K₁, K₂, K₃] using h2
/-- The scaled cosine kernel `cos(k·(θ_i−θ_j))` is positive-definite (via #500). -/
theorem cos_scaled_posdef {m : ℕ} (θ : Fin m → ℝ) (k : ℕ) :
    PosDefKernel (fun i j => Real.cos ((k : ℝ) * (θ i - θ j))) := by
  intro c
  have h : (∑ i, ∑ j, c i * c j * Real.cos ((k : ℝ) * (θ i - θ j))) = ∑ i, ∑ j, c i * c j * Real.cos (((k : ℝ) * θ i) - ((k : ℝ) * θ j)) := by
    simp_rw [mul_sub]
  rw [h]
  exact cos_kernel_posdef (fun i => (k : ℝ) * θ i) c

/-- The triple-angle expansion: `cos³(θ) = (3cos θ + cos 3θ)/4`. -/
theorem cos_cube_expansion (θ : ℝ) : (Real.cos θ)^3 = (3 * Real.cos θ + Real.cos (3 * θ)) / 4 := by
  have h := Real.cos_three_mul θ
  linarith

/-- **The cube of the cosine kernel is positive-definite** — the triple-angle turns `cos³` into
the positive combination `(3cos θ + cos 3θ)/4`. -/
theorem cos_cube_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => (Real.cos (θ i - θ j))^3) := by
  have heq : (fun i j => (Real.cos (θ i - θ j))^3) = fun i j => (3 / 4) * Real.cos (θ i - θ j) + (1 / 4) * Real.cos (3 * (θ i - θ j)) := by
    funext i j
    rw [cos_cube_expansion]
    ring
  rw [heq]
  exact posdef_add (fun i j => (3 / 4) * Real.cos (θ i - θ j)) (fun i j => (1 / 4) * Real.cos (3 * (θ i - θ j)))
    (posdef_smul (fun i j => Real.cos (θ i - θ j)) (3 / 4) (by norm_num) (cos_kernel_posdef θ))
    (posdef_smul (fun i j => Real.cos (3 * (θ i - θ j))) (1 / 4) (by norm_num) (cos_scaled_posdef θ 3))
/-- The quadruple-angle expansion: `cos⁴(θ) = (3 + 4cos 2θ + cos 4θ)/8`. -/
theorem cos_four_expansion (θ : ℝ) : (Real.cos θ)^4 = (3 + 4 * Real.cos (2 * θ) + Real.cos (4 * θ)) / 8 := by
  have h1 : (Real.cos θ)^4 = ((Real.cos θ)^2)^2 := by ring
  rw [h1, Real.cos_sq]
  -- ((1 + cos 2θ)/2)² = (1 + 2cos 2θ + cos² 2θ)/4
  have h2 : (1 / 2 + Real.cos (2 * θ) / 2)^2 = (1 + 2 * Real.cos (2 * θ) + (Real.cos (2 * θ))^2) / 4 := by
    ring_nf
  rw [h2]
  have h3 : (Real.cos (2 * θ))^2 = 1 / 2 + Real.cos (4 * θ) / 2 := by
    have h := Real.cos_sq (2 * θ)
    rw [show 2 * (2 * θ) = 4 * θ by ring] at h
    exact h
  rw [h3]
  ring_nf

/-- **The fourth power of the cosine kernel is positive-definite** — the quadruple-angle turns
`cos⁴` into the positive combination `(3 + 4cos 2θ + cos 4θ)/8`. -/
theorem cos_four_posdef {m : ℕ} (θ : Fin m → ℝ) : PosDefKernel (fun i j => (Real.cos (θ i - θ j))^4) := by
  have heq : (fun i j => (Real.cos (θ i - θ j))^4) = fun i j => (3 / 8) * (1 : ℝ) + (4 / 8) * Real.cos (2 * (θ i - θ j)) + (1 / 8) * Real.cos (4 * (θ i - θ j)) := by
    funext i j
    rw [cos_four_expansion]
    ring
  rw [heq]
  exact posdef_add (fun i j => (3 / 8) * (1 : ℝ) + (4 / 8) * Real.cos (2 * (θ i - θ j)))
      (fun i j => (1 / 8) * Real.cos (4 * (θ i - θ j)))
    (posdef_add (fun _ _ : Fin m => (3 / 8) * (1 : ℝ)) (fun i j => (4 / 8) * Real.cos (2 * (θ i - θ j)))
      (posdef_smul (fun _ _ : Fin m => (1 : ℝ)) (3 / 8) (by norm_num) const_kernel_posdef)
      (posdef_smul (fun i j => Real.cos (2 * (θ i - θ j))) (4 / 8) (by norm_num) (cos_double_posdef θ)))
    (posdef_smul (fun i j => Real.cos (4 * (θ i - θ j))) (1 / 8) (by norm_num) (cos_scaled_posdef θ 4))
set_option maxHeartbeats 400000 in
/-- **The general truncated Wilson heat kernel is positive-definite** (first N+1 terms):
`Σ_{n=0}^{N} (2β)^n/n!·cos^n` is PSD for `β ≥ 0`, a non-negative combination of the PSD `cos^n`. -/
theorem heat_kernel_truncated_posdef_gen {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) (N : ℕ)
    (hcos : ∀ n, PosDefKernel (fun i j => (Real.cos (θ i - θ j))^n)) :
    PosDefKernel (fun i j => ∑ n : Fin (N+1), ((2 * β)^(n.1) / (n.1.factorial : ℝ)) * (Real.cos (θ i - θ j))^(n.1)) := by
  let Kcos : ℕ → Fin m → Fin m → ℝ := fun n i j => (Real.cos (θ i - θ j))^n
  let w : Fin (N+1) → ℝ := fun n => (2 * β)^(n.1) / (n.1.factorial : ℝ)
  have hw : ∀ n : Fin (N+1), 0 ≤ w n := fun n => div_nonneg (pow_nonneg (mul_nonneg (by norm_num : 0 ≤ (2 : ℝ)) hβ) (n.1)) (Nat.cast_nonneg (n.1.factorial))
  have hK : ∀ n : Fin (N+1), PosDefKernel (fun i j => w n * Kcos n.1 i j) := fun n =>
    posdef_smul (Kcos n.1) (w n) (hw n) (hcos n.1)
  simpa [Kcos, w] using (posdef_sum (fun n => fun i j => w n * Kcos n.1 i j) hK)
/-- `Real.exp x = ∑' n, x^n/n!` (the Taylor series, via `NormedSpace.exp_eq_tsum`). -/
theorem real_exp_eq_tsum (x : ℝ) : Real.exp x = ∑' n : ℕ, x^n / (n.factorial : ℝ) := by
  have h : NormedSpace.exp (𝔸 := ℝ) x = ∑' n : ℕ, (n.factorial : ℝ)⁻¹ • x^n := by
    rw [NormedSpace.exp_eq_tsum ℝ]
  have h' : NormedSpace.exp (𝔸 := ℝ) x = Real.exp x := congr_fun Real.exp_eq_exp_ℝ.symm x
  rw [← h', h]
  apply tsum_congr
  intro n
  simp [div_eq_mul_inv, mul_comm]

set_option maxHeartbeats 800000 in
/-- **The full Wilson heat kernel is positive-definite** (OS3), parametric in the `cos^n` PSD. -/
theorem heat_kernel_posdef_of_cos_pow {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β)
    (hcos : ∀ n, PosDefKernel (fun i j => (Real.cos (θ i - θ j))^n)) :
    PosDefKernel (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) := by
  intro c
  let xij : Fin m → Fin m → ℝ := fun i j => 2 * β * Real.cos (θ i - θ j)
  have hlim : ∀ i j, Filter.Tendsto (fun N : ℕ => ∑ n ∈ Finset.range N, (xij i j)^n / (n.factorial : ℝ)) Filter.atTop (nhds (Real.exp (xij i j))) := by
    intro i j
    have hsum : Summable (fun n : ℕ => (xij i j)^n / (n.factorial : ℝ)) := Real.summable_pow_div_factorial (xij i j)
    have hhas : HasSum (fun n : ℕ => (xij i j)^n / (n.factorial : ℝ)) (Real.exp (xij i j)) := by
      rw [real_exp_eq_tsum (xij i j)]
      exact hsum.hasSum
    exact (hsum.hasSum_iff_tendsto_nat).mp hhas
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
    -- range N ↔ Fin N
    have hfin : (fun i j => ∑ n ∈ Finset.range N, ((2 * β)^n / (n.factorial : ℝ)) * (Real.cos (θ i - θ j))^n) = fun i j => ∑ n : Fin N, ((2 * β)^(n.1) / (n.1.factorial : ℝ)) * (Real.cos (θ i - θ j))^(n.1) := by
      funext i j
      rw [← Fin.sum_univ_eq_sum_range]
    rw [hfin]
    exact posdef_sum (fun n : Fin N => fun i j => ((2 * β)^(n.1) / (n.1.factorial : ℝ)) * (Real.cos (θ i - θ j))^(n.1))
      (fun n => posdef_smul (fun i j => (Real.cos (θ i - θ j))^(n.1)) ((2 * β)^(n.1) / (n.1.factorial : ℝ))
        (by exact div_nonneg (pow_nonneg (mul_nonneg (by norm_num : 0 ≤ (2 : ℝ)) hβ) _) (Nat.cast_nonneg _)) (hcos n.1))
  simpa [xij] using ((posdef_of_tendsto (fun N => fun i j => ∑ n ∈ Finset.range N, (xij i j)^n / (n.factorial : ℝ)) (fun i j => Real.exp (xij i j)) hlim hK) c)

/-- The recurrence `cos((m+1)θ)·cos θ = (cos((m+2)θ) + cos(mθ))/2` for `m : ℕ`. -/
theorem cos_mul_cos_nat (m : ℕ) (θ : ℝ) :
    Real.cos (((m + 1 : ℕ) : ℝ) * θ) * Real.cos θ =
      (Real.cos (((m + 2 : ℕ) : ℝ) * θ) + Real.cos ((m : ℝ) * θ)) / 2 := by
  rw [cos_mul_cos]
  have h1 : ((m + 1 : ℕ) : ℝ) * θ + θ = ((m + 2 : ℕ) : ℝ) * θ := by
    norm_num [Nat.cast_add]
    ring
  have h2 : ((m + 1 : ℕ) : ℝ) * θ - θ = (m : ℝ) * θ := by
    norm_num [Nat.cast_add]
    ring
  rw [h1, h2]

/-- A function is a non-negative combination of the cosines `cos(m·θ)` for `m ≤ n`. -/
def IsPosCosComb (n : ℕ) (f : ℝ → ℝ) : Prop :=
  ∃ a : ℕ → ℝ,
    (∀ m, 0 ≤ a m) ∧
    (∀ θ, f θ = ∑ m ∈ Finset.range (n + 1), a m * Real.cos ((m : ℝ) * θ))

/-- The base case: `cos θ` is itself a positive cosine combination (`n = 1`). -/
theorem isPosCosComb_one : IsPosCosComb 1 (fun θ => Real.cos θ) := by
  refine ⟨fun m => if m = 1 then 1 else 0, ?_, ?_⟩
  · intro m
    by_cases h : m = 1 <;> simp [h]
  · intro θ
    simp

/-- PSD is closed under finite non-negative combinations. -/
theorem posdef_finset_sum {α : Type*} [Fintype α] {ι : Type*} (s : Finset ι)
    (K : ι → α → α → ℝ) (w : ι → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hK : ∀ i, PosDefKernel (K i)) :
    PosDefKernel (fun a b => ∑ i ∈ s, w i * K i a b) := by
  classical
  refine Finset.induction_on s ?empty ?insert
  · intro c
    simp
  · intro i s his ih
    have hmain : (fun a b => ∑ j ∈ insert i s, w j * K j a b) = fun a b => w i * K i a b + ∑ j ∈ s, w j * K j a b := by
      funext a b
      rw [Finset.sum_insert his]
    rw [hmain]
    exact posdef_add (fun a b => w i * K i a b) (fun a b => ∑ j ∈ s, w j * K j a b)
      (posdef_smul (K i) (w i) (hw i) (hK i)) ih

-- reindexing lemmas for the induction step

lemma sum_cos_one_indicator (a : ℕ → ℝ) (θ : ℝ) (n : ℕ) :
    (∑ k ∈ Finset.range (n + 2), (if k = 1 then a 0 else 0) * Real.cos ((k : ℝ) * θ))
      = a 0 * Real.cos θ := by
  rw [Finset.sum_eq_single 1]
  · simp
  · intro b hb hb1
    simp [hb1]
  · intro hnotin
    exfalso
    exact hnotin (by simp)

lemma sum_cos_shift_down (a : ℕ → ℝ) (θ : ℝ) (n : ℕ) :
    (∑ k ∈ Finset.range (n + 2), (if k < n then a (k + 1) else 0) * Real.cos ((k : ℝ) * θ))
      = ∑ m ∈ Finset.range n, a (m + 1) * Real.cos ((m : ℝ) * θ) := by
  calc
    (∑ k ∈ Finset.range (n + 2), (if k < n then a (k + 1) else 0) * Real.cos ((k : ℝ) * θ))
      = ∑ k ∈ Finset.range (n + 2), (if k < n then a (k + 1) * Real.cos ((k : ℝ) * θ) else 0) := by
          apply Finset.sum_congr rfl
          intro k hk
          by_cases hklt : k < n <;> simp [hklt]
    _ = ∑ k ∈ Finset.range n, a (k + 1) * Real.cos ((k : ℝ) * θ) := by
          rw [← Finset.sum_filter]
          have hf : (Finset.range (n + 2)).filter (fun k => k < n) = Finset.range n := by
            ext k
            simp
            omega
          rw [hf]

lemma sum_cos_shift_up (a : ℕ → ℝ) (θ : ℝ) (n : ℕ) :
    (∑ k ∈ Finset.range (n + 2), (if 2 ≤ k ∧ k ≤ n + 1 then a (k - 1) else 0) * Real.cos ((k : ℝ) * θ))
      = ∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ) := by
  calc
    (∑ k ∈ Finset.range (n + 2), (if 2 ≤ k ∧ k ≤ n + 1 then a (k - 1) else 0) * Real.cos ((k : ℝ) * θ))
      = ∑ k ∈ Finset.range (n + 2), (if 2 ≤ k ∧ k ≤ n + 1 then a (k - 1) * Real.cos ((k : ℝ) * θ) else 0) := by
          apply Finset.sum_congr rfl
          intro k hk
          by_cases hc : 2 ≤ k ∧ k ≤ n + 1 <;> simp [hc]
    _ = ∑ k ∈ Finset.Ico 2 (n + 2), a (k - 1) * Real.cos ((k : ℝ) * θ) := by
          rw [← Finset.sum_filter]
          have hf : (Finset.range (n + 2)).filter (fun k => 2 ≤ k ∧ k ≤ n + 1) = Finset.Ico 2 (n + 2) := by
            ext k
            simp [Finset.mem_Ico]
            omega
          rw [hf]
    _ = ∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ) := by
          rw [Finset.sum_Ico_eq_sum_range]
          simp only [Nat.add_sub_cancel]
          apply Finset.sum_congr rfl
          intro m hm
          congr 1
          · congr 1
            omega
          · congr 1
            rw [show (2 + m : ℕ) = m + 2 by omega]

/-- Splitting a scaled sum of cosines: `a·((cos X + cos Y)/2) = (1/2)·a·cos X + (1/2)·a·cos Y`. -/
lemma cos_summand_split (a : ℕ → ℝ) (θ : ℝ) (m : ℕ) :
    a (m + 1) * ((Real.cos (((m + 2 : ℕ) : ℝ) * θ) + Real.cos ((m : ℝ) * θ)) / 2)
      = (1 / 2) * (a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ)) + (1 / 2) * (a (m + 1) * Real.cos ((m : ℝ) * θ)) := by
  ring_nf

/-- The induction step: if `f` is a positive cosine combination, so is `f · cos`. -/
theorem isPosCosComb_step {n : ℕ} {f : ℝ → ℝ} (h : IsPosCosComb n f) :
    IsPosCosComb (n + 1) (fun θ => f θ * Real.cos θ) := by
  rcases h with ⟨a, ha_nonneg, ha⟩
  let b : ℕ → ℝ := fun k =>
    (1 / 2) * (if 2 ≤ k ∧ k ≤ n + 1 then a (k - 1) else 0)
    + (1 / 2) * (if k < n then a (k + 1) else 0)
    + (if k = 1 then a 0 else 0)
  refine ⟨b, ?_, ?_⟩
  · intro k
    dsimp [b]
    have h1 : 0 ≤ (1 / 2) * (if 2 ≤ k ∧ k ≤ n + 1 then a (k - 1) else 0) := by
      by_cases hc : 2 ≤ k ∧ k ≤ n + 1
      · have : 0 ≤ (1 / 2) * a (k - 1) := mul_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) (ha_nonneg (k - 1))
        simpa [hc] using this
      · simp [hc]
    have h2 : 0 ≤ (1 / 2) * (if k < n then a (k + 1) else 0) := by
      by_cases hc : k < n
      · have : 0 ≤ (1 / 2) * a (k + 1) := mul_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) (ha_nonneg (k + 1))
        simpa [hc] using this
      · simp [hc]
    have h3 : 0 ≤ (if k = 1 then a 0 else 0) := by
      by_cases hc : k = 1 <;> simp [hc, ha_nonneg 0]
    linarith
  · intro θ
    have hmiddle :
        f θ * Real.cos θ
          = a 0 * Real.cos θ
              + (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ))
              + (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos ((m : ℝ) * θ)) := by
      calc
        f θ * Real.cos θ
          = (∑ m ∈ Finset.range (n + 1), a m * Real.cos ((m : ℝ) * θ)) * Real.cos θ := by rw [ha]
        _ = (∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 1 : ℕ) : ℝ) * θ)) * Real.cos θ + a 0 * Real.cos θ := by
              rw [Finset.sum_range_succ', add_mul]
              simp
        _ = (∑ m ∈ Finset.range n, a (m + 1) * (Real.cos (((m + 1 : ℕ) : ℝ) * θ) * Real.cos θ)) + a 0 * Real.cos θ := by
              rw [Finset.sum_mul]
              simp_rw [mul_assoc]
        _ = (∑ m ∈ Finset.range n, a (m + 1) * ((Real.cos (((m + 2 : ℕ) : ℝ) * θ) + Real.cos ((m : ℝ) * θ)) / 2)) + a 0 * Real.cos θ := by
              simp_rw [cos_mul_cos_nat]
        _ = (∑ m ∈ Finset.range n, ((1 / 2) * (a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ)) + (1 / 2) * (a (m + 1) * Real.cos ((m : ℝ) * θ)))) + a 0 * Real.cos θ := by
              rw [Finset.sum_congr rfl (fun m _ => cos_summand_split a θ m)]
        _ = a 0 * Real.cos θ + (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ)) + (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos ((m : ℝ) * θ)) := by
              rw [Finset.sum_add_distrib]
              simp_rw [← Finset.mul_sum]
              ring
    have hs1 : (∑ k ∈ Finset.range (n + 2), ((1 / 2) * (if 2 ≤ k ∧ k ≤ n + 1 then a (k - 1) else 0)) * Real.cos ((k : ℝ) * θ))
        = (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ)) := by
      simp_rw [mul_assoc]
      rw [← Finset.mul_sum]
      rw [sum_cos_shift_up a θ n]
    have hs2 : (∑ k ∈ Finset.range (n + 2), ((1 / 2) * (if k < n then a (k + 1) else 0)) * Real.cos ((k : ℝ) * θ))
        = (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos ((m : ℝ) * θ)) := by
      simp_rw [mul_assoc]
      rw [← Finset.mul_sum]
      rw [sum_cos_shift_down a θ n]
    have hs3 : (∑ k ∈ Finset.range (n + 2), (if k = 1 then a 0 else 0) * Real.cos ((k : ℝ) * θ))
        = a 0 * Real.cos θ := by
      exact sum_cos_one_indicator a θ n
    calc
      f θ * Real.cos θ
        = a 0 * Real.cos θ + (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos (((m + 2 : ℕ) : ℝ) * θ)) + (1 / 2) * (∑ m ∈ Finset.range n, a (m + 1) * Real.cos ((m : ℝ) * θ)) := hmiddle
      _ = ∑ k ∈ Finset.range (n + 2), b k * Real.cos ((k : ℝ) * θ) := by
          dsimp [b]
          simp_rw [add_mul]
          rw [Finset.sum_add_distrib]
          rw [Finset.sum_add_distrib]
          rw [hs1, hs2, hs3]
          ring

/-- Every power of the cosine is a positive cosine combination. -/
theorem isPosCosComb_all (n : ℕ) : IsPosCosComb n (fun θ => (Real.cos θ) ^ n) := by
  induction n with
  | zero =>
      refine ⟨fun m => if m = 0 then 1 else 0, ?_, ?_⟩
      · intro m
        by_cases h : m = 0 <;> simp [h]
      · intro θ
        simp
  | succ n ih =>
      have hstep := isPosCosComb_step ih
      simpa [pow_succ] using hstep

/-- **Every power of the cosine kernel is positive-definite.** -/
theorem cos_pow_posdef {m : ℕ} (θ : Fin m → ℝ) (n : ℕ) :
    PosDefKernel (fun i j => (Real.cos (θ i - θ j)) ^ n) := by
  rcases isPosCosComb_all n with ⟨a, ha_nonneg, ha⟩
  have hmain : (fun i j => (Real.cos (θ i - θ j)) ^ n) = fun i j => ∑ k ∈ Finset.range (n + 1), a k * Real.cos ((k : ℝ) * (θ i - θ j)) := by
    funext i j
    simpa using ha (θ i - θ j)
  rw [hmain]
  exact posdef_finset_sum (Finset.range (n + 1))
    (fun k => fun i j => Real.cos ((k : ℝ) * (θ i - θ j))) a ha_nonneg
    (fun k => cos_scaled_posdef θ k)


/-- **The full Wilson heat kernel is positive-definite** (the OS3 reflection positivity of the
SU(2) Wilson measure): `exp(2β·cos(θ_i−θ_j))` is PSD for `β ≥ 0`. This is the complete theorem — the
general `cos^n` PSD feeds the assembly `heat_kernel_posdef_of_cos_pow`, with no hypotheses left. -/
theorem heat_kernel_posdef {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β) :
    PosDefKernel (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) := by
  exact heat_kernel_posdef_of_cos_pow θ β hβ (fun n => cos_pow_posdef θ n)

end QM
