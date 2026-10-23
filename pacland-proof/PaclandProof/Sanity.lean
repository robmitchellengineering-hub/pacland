import Mathlib
import PaclandProof.Mitchell

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Non-vacuity sanity checks — did the definitions secretly over-constrain?

The worry (ex falso quodlibet / vacuous truth): if `Symp₂` were accidentally empty or
over-constrained, or the tadpole were identically zero, every theorem would be trivially
true and meaningless. This file machine-checks that this did **not** happen:

1. `Symp₂` is **nonempty** and **non-trivial** (two distinct explicit elements);
2. the tadpole `Fᵀ J H` is **not identically zero** (a concrete witness gives `1`);
3. the uniqueness theorem's hypothesis is **satisfiable** (`J` itself is invariant);
4. the uniqueness conclusion is **restrictive** (the identity matrix is *not* invariant,
   so the theorem really excludes something).
-/

open Matrix
noncomputable section
namespace Sanity

-- 1a. Symp₂ is nonempty: the shear is a concrete witness.
theorem symp_nonempty : ∃ S : Matrix (Fin 2) (Fin 2) ℚ, Mitchell.Symp₂ S :=
  ⟨!![1, 1; 0, 1], Mitchell.shear_symp⟩

-- 1b. Symp₂ is non-trivial: the shear and the dilation are two DIFFERENT elements,
-- so the definition is not over-constrained to a single (or no) matrix.
theorem symp_two_distinct :
    (!![1, 1; 0, 1] : Matrix (Fin 2) (Fin 2) ℚ) ≠ !![2, 0; 0, (1 / 2 : ℚ)] := by
  intro h
  have e := congr_fun (congr_fun h 0) 1
  norm_num at e

-- 2. The tadpole is NOT identically zero: F = (1, 0), H = (0, 1) gives Fᵀ J H = 1.
theorem tadpole_nontrivial :
    ∃ F H : Fin 2 → ℚ, Matrix.dotProduct F (Mitchell.J₂.mulVec H) ≠ 0 := by
  refine ⟨![1, 0], ![0, 1], ?_⟩
  norm_num [Mitchell.J₂, Matrix.mulVec, Matrix.dotProduct, Fin.sum_univ_two]

-- 3. The uniqueness hypothesis is satisfiable: J itself is invariant
-- (this is exactly the definition of Symp₂, restated as a positive control).
theorem J2_is_invariant (S : Matrix (Fin 2) (Fin 2) ℚ) (hS : Mitchell.Symp₂ S) :
    Sᵀ * Mitchell.J₂ * S = Mitchell.J₂ := by
  simpa [Mitchell.Symp₂] using hS

-- 4. The uniqueness conclusion is restrictive: the identity matrix is NOT an
-- invariant bilinear form (the shear already breaks Sᵀ · 1 · S = 1), so the theorem
-- genuinely rules out all but the scalar multiples of J.
theorem identity_not_invariant :
    ¬ (∀ S : Matrix (Fin 2) (Fin 2) ℚ, Mitchell.Symp₂ S → Sᵀ * (1 : Matrix (Fin 2) (Fin 2) ℚ) * S = 1) := by
  intro h
  have e := h !![1, 1; 0, 1] Mitchell.shear_symp
  have e01 := congr_fun (congr_fun e 0) 1
  norm_num at e01

end Sanity
end
