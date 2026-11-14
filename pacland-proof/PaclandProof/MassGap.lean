import Mathlib
import PaclandProof.Mitchell

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The mass scale is a value, not a relation

The constraint-first claim for the mass scale (a proxy for the mass gap): it is **not**
one of the exact symplectic invariants of the flux — of which the D3 tadpole `Fᵀ J H` is
the unique bilinear one (Mitchell's Uniqueness). Two ways this is made precise:

1. `massScale_not_invariant` — a symplectic transformation (the dilation) changes the
   mass scale, so the mass scale is not an invariant at all.
2. `massScale_not_determined_by_tadpole` — two flux pairs with the same tadpole have
   different mass scale, so the tadpole (the unique invariant) does not fix the mass
   scale.

Together: the mass gap is a *value* (a free parameter in the deficit), not a *relation*
(the exact structure is exhausted by the constraint). This is the "relations, never
values" boundary, machine-checked.
-/

open Matrix
open scoped BigOperators

noncomputable section

namespace Mitchell

/-- The D3 tadpole: the symplectic pairing `Fᵀ J₂ H` of the flux pair. -/
def tadpole (F H : Fin 2 → ℚ) : ℚ :=
  F ⬝ᵥ (J₂.mulVec H)

/-- A proxy for the overall mass scale: the squared norm `‖F‖² + ‖H‖²`. -/
def massScale (F H : Fin 2 → ℚ) : ℚ :=
  (F ⬝ᵥ F) + (H ⬝ᵥ H)

/-- **The mass scale is not a symplectic invariant.** The dilation is symplectic but
rescales the flux, so the mass scale changes under it. -/
theorem massScale_not_invariant :
    ∃ S : Matrix (Fin 2) (Fin 2) ℚ, Symp₂ S ∧
      ∃ F H : Fin 2 → ℚ, massScale (S.mulVec F) (S.mulVec H) ≠ massScale F H := by
  refine ⟨!![2, 0; 0, (1 / 2 : ℚ)], dilate_symp, ![1, 0], ![0, 1], ?_⟩
  norm_num [massScale, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- **The mass scale is not determined by the tadpole.** Two flux pairs share the same
tadpole but have different mass scale, so the unique invariant does not fix the mass scale. -/
theorem massScale_not_determined_by_tadpole :
    ∃ F1 H1 F2 H2 : Fin 2 → ℚ,
      tadpole F1 H1 = tadpole F2 H2 ∧ massScale F1 H1 ≠ massScale F2 H2 := by
  refine ⟨![1, 0], ![1, 0], ![2, 0], ![1, 0], ?_, ?_⟩
  · norm_num [tadpole, J₂, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  · norm_num [massScale, dotProduct, Fin.sum_univ_two]

end Mitchell
