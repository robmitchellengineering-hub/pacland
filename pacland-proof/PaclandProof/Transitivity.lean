import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Mitchell's Completeness Theorem — transitivity (machine-checked, n = 1)

The D3 tadpole `N = xᵀ J y` is the *unique* symplectic invariant (Mitchell's
Uniqueness, `Mitchell.lean` / `General.lean`). The completeness half is that the
symplectic group acts *transitively* on each non-zero tadpole level set. This file
machine-checks that statement for the smallest case (`2×2`, `Sp(2) = SL(2)`):

  every pair `(x, y)` with `xᵀ J y = 1` is the image of the canonical pair
  `(e₀, e₁)` under a symplectic matrix — equivalently, the level set `{xᵀ J y = 1}`
  is a single orbit.

The proof is the `2×2` determinant identity: for any `2×2` matrix `S`,
`Sᵀ J S = det S • J`, so `S` is symplectic iff `det S = 1`; the matrix with columns
`x, y` then has determinant `xᵀ J y = 1`, so it is the required symplectic map.
-/

open Matrix

noncomputable section

namespace Completeness

variable {R : Type*} [Field R]

/-- The standard `2×2` symplectic form. -/
def J₂ : Matrix (Fin 2) (Fin 2) R :=
  !![0, 1; -1, 0]

/-- A `2×2` matrix is symplectic iff it preserves `J₂`: `Sᵀ J₂ S = J₂`. -/
def Symp₂ (S : Matrix (Fin 2) (Fin 2) R) : Prop :=
  Sᵀ * J₂ * S = J₂

/-- For a `2×2` matrix, `Sᵀ J₂ S = det S • J₂`. -/
theorem transpose_mul_J_mul_self (S : Matrix (Fin 2) (Fin 2) R) :
    Sᵀ * J₂ * S = S.det • J₂ := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [J₂, Matrix.mul_apply, Matrix.transpose_apply, Matrix.det_fin_two,
      Matrix.smul_apply, Fin.sum_univ_two] <;> ring

/-- A `2×2` matrix is symplectic iff its determinant is `1`. -/
theorem symp_iff_det_eq_one (S : Matrix (Fin 2) (Fin 2) R) :
    Symp₂ S ↔ S.det = 1 := by
  rw [Symp₂]
  rw [transpose_mul_J_mul_self S]
  constructor
  · intro h
    have h' := congrArg (fun M : Matrix (Fin 2) (Fin 2) R => M 0 1) h
    simpa [J₂, Matrix.smul_apply] using h'
  · intro hdet
    rw [hdet]
    simp [J₂]

/-- **Mitchell's Completeness (transitivity, n = 1).**
Every pair `(x, y)` with `xᵀ J₂ y = 1` is the image of the canonical pair
`(e₀, e₁)` under a symplectic `2×2` matrix. -/
theorem transitivity_n1 (x y : Fin 2 → R)
    (hN : dotProduct x (J₂.mulVec y) = 1) :
    ∃ S : Matrix (Fin 2) (Fin 2) R,
      Symp₂ S ∧ S.mulVec (Pi.single 0 (1 : R)) = x ∧ S.mulVec (Pi.single 1 (1 : R)) = y := by
  let S : Matrix (Fin 2) (Fin 2) R := fun i j => if j = 0 then x i else y i
  have hdet : S.det = 1 := by
    have hdet2 : S.det = x 0 * y 1 - x 1 * y 0 := by
      rw [Matrix.det_fin_two]
      simp [S]
      ring
    have hN' : dotProduct x (J₂.mulVec y) = x 0 * y 1 - x 1 * y 0 := by
      simp [J₂, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
      ring
    rw [hdet2, ← hN']
    exact hN
  refine ⟨S, ?_, ?_, ?_⟩
  · exact (symp_iff_det_eq_one S).2 hdet
  · ext i
    fin_cases i
    · simp [S, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Pi.single]
    · simp [S, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Pi.single]
  · ext i
    fin_cases i
    · simp [S, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Pi.single]
    · simp [S, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Pi.single]

end Completeness

end
