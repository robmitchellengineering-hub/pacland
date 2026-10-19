import Mathlib

/-!
# Mitchell's Uniqueness Theorem — machine-checked core

The D3 tadpole `Fᵀ J H` is the unique symplectic invariant bilinear form in the flux
pair. Proved here in Lean 4 + Mathlib for the smallest nontrivial case (`2×2`,
`Sp(2) = SL(2)`); the argument is the same in every dimension.

Statement: for the symplectic form `J`, the only matrix `M` with `Sᵀ M S = M` for
*every* symplectic `S` is a scalar multiple of `J`.
-/

open Matrix

noncomputable section

namespace Mitchell

/-- The standard `2×2` symplectic form, over the rationals (the proof is
characteristic-zero linear algebra; the real case is identical). -/
def J₂ : Matrix (Fin 2) (Fin 2) ℚ :=
  !![0, 1; -1, 0]

/-- A matrix is symplectic iff it preserves the symplectic form: `Sᵀ J S = J`. -/
def Symp₂ (S : Matrix (Fin 2) (Fin 2) ℚ) : Prop :=
  Sᵀ * J₂ * S = J₂

/-- `J₂` is antisymmetric. -/
theorem J₂_antisymm : J₂ + J₂ᵀ = 0 := by
  native_decide

/-- The shear `[[1,1],[0,1]]` is symplectic. -/
theorem shear_symp : Symp₂ !![1, 1; 0, 1] := by
  unfold Symp₂
  native_decide

/-- The dilation `[[2,0],[0,1/2]]` is symplectic. -/
theorem dilate_symp : Symp₂ !![2, 0; 0, (1 / 2 : ℚ)] := by
  unfold Symp₂
  native_decide

/-- **Mitchell's Uniqueness Theorem (n = 1).**
The only bilinear forms invariant under the whole symplectic group are the scalar
multiples of the symplectic form itself. -/
theorem mitchell_uniqueness_n1
    (M : Matrix (Fin 2) (Fin 2) ℚ)
    (h : ∀ S, Symp₂ S → Sᵀ * M * S = M) :
    ∃ c : ℚ, M = c • J₂ := by
  have e₁ := h (!![1, 1; 0, 1] : Matrix (Fin 2) (Fin 2) ℚ) shear_symp
  have e₂ := h (!![2, 0; 0, (1 / 2 : ℚ)] : Matrix (Fin 2) (Fin 2) ℚ) dilate_symp
  -- M 0 0 = 0 (from the shear, entry (0,1))
  have h00 : M 0 0 = 0 := by
    have e := congr_fun (congr_fun e₁ 0) 1
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two] at e
    linarith
  -- M 1 0 = - M 0 1 (from the shear, entry (1,1))
  have h10 : M 1 0 = - M 0 1 := by
    have e := congr_fun (congr_fun e₁ 1) 1
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two] at e
    linarith
  -- M 1 1 = 0 (from the dilation, entry (1,1))
  have h11 : M 1 1 = 0 := by
    have e := congr_fun (congr_fun e₂ 1) 1
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two] at e
    ring_nf at e
    linarith
  refine ⟨M 0 1, ?_⟩
  ext i j <;> fin_cases i <;> fin_cases j
  · simp [h00, J₂]
  · simp [J₂]
  · simp [h10, J₂]
  · simp [h11, J₂]

end Mitchell

end
