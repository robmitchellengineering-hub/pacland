import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Cayley cubic is SL(2)-invariant

The k=3 flux-pair joint invariant ring has a degree-6 generator: the *Cayley cubic*

    det [[P₁₂, P₁₃, P₂₃], [A₁₂, A₁₃, A₂₃], [Q₁₂, Q₁₃, Q₂₃]]

the `3×3` determinant of the three mixed `Sym²(C²)` triples `(P, A, Q)`.  This file
machine-checks the reason it is `SL(2)`-invariant: the Sym² representation
`SL(2) → GL(3)` has determinant `(ad - bc)³`, hence is `1` on `SL(2)`.

Statement: for `g = [[a, b], [c, d]]` acting on the coefficient vector `(P, A, Q)ᵀ` of a
binary quadratic `P x² + A x y + Q y²` by `(g·q)(x, y) = q(a x + b y, c x + d y)`, the
induced matrix is `ρ(a,b,c,d)`, and `det ρ(a,b,c,d) = (a d - b c)³`.
-/

noncomputable section

open Matrix

namespace Cayley

/-- The Sym² action: `[[a, b], [c, d]]` acts on the column `(P, A, Q)ᵀ` by this `3×3`
matrix.  (Explicitly: `P ↦ a²P + ac A + c²Q`, `A ↦ 2ab P + (ad+bc) A + 2cd Q`,
`Q ↦ b²P + bd A + d²Q`.) -/
def sym2Mat (a b c d : ℚ) : Matrix (Fin 3) (Fin 3) ℚ :=
  !![a*a, a*c, c*c;
     2*a*b, a*d + b*c, 2*c*d;
     b*b, b*d, d*d]

/-- The Sym² representation has determinant `(a d - b c)³`.  This is the whole reason the
Cayley cubic (a `3×3` determinant of three Sym² vectors) is `SL(2)`-invariant. -/
theorem det_sym2 (a b c d : ℚ) : (sym2Mat a b c d).det = (a * d - b * c)^3 := by
  rw [Matrix.det_fin_three]
  simp [sym2Mat]
  ring

/-- On `SL(2)` (where `a d - b c = 1`) the Sym² matrix has determinant `1`. -/
theorem det_sym2_eq_one (a b c d : ℚ) (h : a * d - b * c = 1) :
    (sym2Mat a b c d).det = 1 := by
  rw [det_sym2, h]
  norm_num

/-- The Cayley cubic is the determinant of a `3×3` matrix whose three columns are Sym²
vectors.  Under the Sym² action every column is left-multiplied by `sym2Mat a b c d`, so
the determinant is multiplied by `det (sym2Mat a b c d) = 1` on `SL(2)`.  This is the
machine-checked reason the Cayley cubic is `SL(2)`-invariant. -/
theorem cayleyCubic_invariant (a b c d : ℚ) (h : a * d - b * c = 1)
    (M : Matrix (Fin 3) (Fin 3) ℚ) :
    (sym2Mat a b c d * M).det = M.det := by
  rw [Matrix.det_mul, det_sym2_eq_one a b c d h, one_mul]

end Cayley
