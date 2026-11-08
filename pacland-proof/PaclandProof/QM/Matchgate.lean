import Mathlib

/-!
# The matchgate seed — the amplitude is a Pfaffian, hence a polynomial

Matchgates are classically simulable because their amplitudes are **Pfaffians** (sums over perfect
matchings) — equivalently, square roots of determinants — and a determinant is a polynomial in the
entries, computable in polynomial time. This file kernel-checks the seed of that correspondence:
for the 2×2 antisymmetric matrix, the Pfaffian (the single perfect-matching weight) squares to the
determinant. The 4×4 case (the exact four-qubit matchgate amplitude) is the next rung.
-/

namespace QM

open Matrix

/-- The 2×2 Pfaffian of `[[0, a], [-a, 0]]` — the single perfect-matching weight. -/
def pfaffian2 (a : ℂ) : ℂ := a

/-- The 2×2 perfect-matching sum is the single weight `a`. -/
theorem pfaffian2_is_perfect_matching (a : ℂ) :
    pfaffian2 a = a := rfl

/-- **Matchgate core (2×2).** The square of the Pfaffian equals the determinant — the seed that a
matchgate amplitude is a Pfaffian, hence a polynomial, hence classically simulable. -/
theorem pfaffian2_sq_eq_det (a : ℂ) :
    pfaffian2 a ^ 2 = Matrix.det !![0, a; -a, 0] := by
  rw [pfaffian2]
  rw [Matrix.det_fin_two_of]
  ring

/-- The 4×4 Pfaffian — the signed sum over the three perfect matchings (the exact four-qubit
matchgate amplitude; its square-equals-determinant is the next rung). -/
def pfaffian4 (a b c d e f : ℂ) : ℂ :=
  a * f - b * e + c * d

end QM
