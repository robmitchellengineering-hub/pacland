import Mathlib
import PaclandProof.QM.Matchgate

open BigOperators

noncomputable section

namespace QM

/-- The diagonal of an antisymmetric matrix vanishes: `Aᵀ = -A` implies `A i i = 0`.
This is step 1 of the general Cayley identity `det A = (Pf A)²` (issue #431) — the ingredient that
makes every fixed-point term in the Leibniz sum vanish. -/
theorem antisymm_diagonal_eq_zero {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (hA : A.transpose = -A) (i : Fin n) :
    A i i = 0 := by
  have h : A i i = -A i i := by
    calc
      A i i = (A.transpose) i i := by rw [Matrix.transpose_apply]
      _ = (-A) i i := by rw [hA]
      _ = -A i i := rfl
  have h2 : A i i + A i i = 0 := by
    nth_rewrite 1 [h]
    ring
  have h3 : (2 : ℂ) * A i i = 0 := by
    simpa [two_mul] using h2
  exact (mul_eq_zero.mp h3).resolve_left (by norm_num : (2 : ℂ) ≠ 0)

end QM
