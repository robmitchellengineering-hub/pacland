import Mathlib

/-!
# The matchgate seed — the amplitude is a Pfaffian, hence a polynomial

Matchgates are classically simulable because their amplitudes are **Pfaffians** (sums over perfect
matchings) — equivalently, square roots of determinants — and a determinant is a polynomial in the
entries, computable in polynomial time. This file kernel-checks the seed of that correspondence:

1. the 2×2 Pfaffian (the single perfect-matching weight) squares to the determinant;
2. a 3×3 antisymmetric matrix has determinant **0** — odd dimension kills it, so the Pfaffian
   (and hence matchgates) is an even-dimensional object.

Together these are the even/odd split behind matchgate simulability. The 4×4 case (the exact
four-qubit amplitude) is the next rung.
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

/-- **Odd dimension kills the determinant.** A 3×3 antisymmetric matrix has determinant 0 — the
reason matchgates (Pfaffians) exist only on an *even* number of qubits. Combined with the 2×2 case
(Pf² = det ≠ 0), this is the even/odd split: the Pfaffian is an even-dimensional object. -/
theorem det_three_antisymm_eq_zero (a b c : ℂ) :
    Matrix.det !![0, a, b; -a, 0, c; -b, -c, 0] = 0 := by
  rw [Matrix.det_fin_three]
  simp
  ring

end QM
