import Mathlib
import PaclandProof.Mitchell

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Degree-1 slice of the FFT (n = 1) — no linear invariant

No non-zero vector is fixed by every symplectic transformation, so the invariant
ring `ℂ[N]` has no degree-1 piece. The dilation `[[2,0],[0,1/2]]` forces both
entries to vanish. (Proved in its own namespace to keep the Mitchell core minimal.)
-/

open Matrix
noncomputable section
namespace DegreeOne

/-- **Degree-1 slice of the FFT (n = 1)**: the only vector fixed by every symplectic
transformation is zero. -/
theorem no_linear_invariant_n1 (v : Fin 2 → ℚ)
    (h : ∀ S, Mitchell.Symp₂ S → Sᵀ.mulVec v = v) :
    v = 0 := by
  have e := h (!![2, 0; 0, (1 / 2 : ℚ)] : Matrix (Fin 2) (Fin 2) ℚ) Mitchell.dilate_symp
  have mulVec0 : ((!![2, 0; 0, (1 / 2 : ℚ)] : Matrix (Fin 2) (Fin 2) ℚ)ᵀ.mulVec v) 0 = 2 * v 0 := by
    norm_num [Matrix.mulVec, Matrix.transpose_apply, Fin.sum_univ_two]
  have mulVec1 : ((!![2, 0; 0, (1 / 2 : ℚ)] : Matrix (Fin 2) (Fin 2) ℚ)ᵀ.mulVec v) 1 = (1 / 2 : ℚ) * v 1 := by
    norm_num [Matrix.mulVec, Matrix.transpose_apply, Fin.sum_univ_two]
  have h0 : v 0 = 0 := by
    have e0 := congr_fun e 0
    rw [mulVec0] at e0
    linarith
  have h1 : v 1 = 0 := by
    have e1 := congr_fun e 1
    rw [mulVec1] at e1
    linarith
  ext i <;> fin_cases i <;> simp [h0, h1]

end DegreeOne
end
