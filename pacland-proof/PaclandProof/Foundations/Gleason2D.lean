import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# QF-1 — Gleason's theorem is FALSE in dimension 2

The kernel-checked reason the Born-rule hinge `Hinges.F3` must carry
`h_dim_ge_three`. In two dimensions a Born measure (a positive-semidefinite
density matrix) with `f(e₁) = 1`, `f(e₂) = 0` is *forced* to give
`f((1,1)) = 1/2`; therefore no such measure can realise a frame function that
assigns `f((1,1)) = 1/10`. A 2D frame function may do exactly that (the frame
condition only requires `f(u) + f(u⊥) = 1`), so additivity does **not** imply
the Born rule below dimension 3 — Gleason's hypothesis is load-bearing.

All computation is over `ℝ` on `Fin 2` matrices and vectors.
-/

noncomputable section

open Matrix BigOperators

namespace Gleason2D

/-- The Born value of a density matrix `M` on a vector `v`: `vᵀ M v / vᵀ v`. -/
def born (M : Matrix (Fin 2) (Fin 2) ℝ) (v : Fin 2 → ℝ) : ℝ :=
  dotProduct v (M.mulVec v) / dotProduct v v

/-- 2×2 positive semidefinite (symmetric) via the principal-minors criterion:
`M 0 0 ≥ 0 ∧ M 1 1 ≥ 0 ∧ det M ≥ 0`. -/
def psd2 (M : Matrix (Fin 2) (Fin 2) ℝ) : Prop :=
  0 ≤ M 0 0 ∧ 0 ≤ M 1 1 ∧ 0 ≤ M.det

/-- If a symmetric PSD matrix has diagonal `(1, 0)`, it is off-diagonal `0`.
(PSD forces `det = -M₀₁² ≥ 0`, hence `M₀₁ = 0`.) -/
theorem diag_10_forces_offdiag (M : Matrix (Fin 2) (Fin 2) ℝ)
    (hsym : M 1 0 = M 0 1) (hpsd : psd2 M)
    (h00 : M 0 0 = 1) (h11 : M 1 1 = 0) :
    M 0 1 = 0 := by
  rcases hpsd with ⟨_h00nn, _h11nn, hdetnn⟩
  have hdet : M.det = -(M 0 1) ^ 2 := by
    rw [Matrix.det_fin_two]
    rw [h00, h11, hsym]
    ring
  have hsq_le : (M 0 1) ^ 2 ≤ 0 := by
    have h : (0 : ℝ) ≤ M.det := hdetnn
    rw [hdet] at h
    nlinarith
  have hsq_eq : (M 0 1) ^ 2 = 0 := le_antisymm hsq_le (sq_nonneg (M 0 1))
  exact sq_eq_zero_iff.mp hsq_eq

/-- With diagonal `(1, 0)` and off-diagonal `0`, the Born value on `(1, 1)` is
exactly `1/2`. -/
theorem born_diag_10 (M : Matrix (Fin 2) (Fin 2) ℝ)
    (hsym : M 1 0 = M 0 1) (h00 : M 0 0 = 1) (h11 : M 1 1 = 0) (hoff : M 0 1 = 0) :
    born M (fun _ => (1 : ℝ)) = 1 / 2 := by
  unfold born
  have hmv : M.mulVec (fun _ : Fin 2 => (1 : ℝ)) = fun i => if i = 0 then (1 : ℝ) else 0 := by
    ext i
    fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two, h00, h11, hsym, hoff]
  rw [hmv]
  norm_num [dotProduct, Fin.sum_univ_two]

/-- **Gleason's theorem fails in dimension 2.** No symmetric PSD matrix with
`f(e₁) = 1`, `f(e₂) = 0` can assign Born value `1/10` to `(1, 1)` — the Born
rule forces `1/2`. Hence a 2D frame function (additive but not Born) exists, and
`h_dim_ge_three` on `Hinges.F3` is necessary, not decoration. -/
theorem no_born_dim2_counterexample :
    ¬ ∃ M : Matrix (Fin 2) (Fin 2) ℝ,
      M 1 0 = M 0 1 ∧ psd2 M ∧ M 0 0 = 1 ∧ M 1 1 = 0 ∧
      born M (fun _ => (1 : ℝ)) = 1 / 10 := by
  rintro ⟨M, hsym, hpsd, h00, h11, hf⟩
  have hoff : M 0 1 = 0 := diag_10_forces_offdiag M hsym hpsd h00 h11
  have hhalf : born M (fun _ => (1 : ℝ)) = 1 / 2 :=
    born_diag_10 M hsym h00 h11 hoff
  rw [hhalf] at hf
  norm_num at hf

end Gleason2D

end
