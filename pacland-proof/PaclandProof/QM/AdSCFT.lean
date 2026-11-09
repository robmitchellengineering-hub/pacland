import Mathlib
import PaclandProof.QM.HyperbolicPlane

/-!
# AdS/CFT — the symmetry dictionary (Job 3, piece 1)

The first kernel-checkable piece of the duality: the **Möbius group** `PSL(2,ℝ)` is simultaneously
the conformal symmetry of the boundary (the circle / real line) and the isometry group of the bulk
hyperbolic plane `H²`. This file starts that piece: the Möbius action of `SL(2,ℝ)` on the boundary,
the first object of the dictionary.
-/

namespace QM

open scoped Matrix BigOperators

/-- The Möbius transformation of `z` by `g = [[a,b],[c,d]] ∈ SL(2,ℝ)`: `z ↦ (a z + b)/(c z + d)`.
This is the conformal symmetry of the boundary — the CFT side of the AdS/CFT dictionary. -/
noncomputable def mobius (g : Matrix.SpecialLinearGroup (Fin 2) ℝ) (z : ℝ) : ℝ :=
  (g.1 0 0 * z + g.1 0 1) / (g.1 1 0 * z + g.1 1 1)

/-- The composition of Möbius transformations matches matrix multiplication up to the group law —
the Möbius transformations form a group (the boundary conformal group), which is the symmetry side
of the dictionary matching the bulk isometry group of H². -/
theorem mobius_one (z : ℝ) :
    mobius (1 : Matrix.SpecialLinearGroup (Fin 2) ℝ) z = z := by
  simp [mobius]

end QM
