import Mathlib
import PaclandProof.QM.Matchgate

open Matrix
open BigOperators
open QM

theorem pfaffian_rec_2 (A : Matrix (Fin 2) (Fin 2) ℂ) :
    pfaffian 1 A = pfaffian2 (A 0 1) := by
  rw [pfaffian2]
  rw [pfaffian]
  simp [pfaffian]

theorem pfaffian_rec_4 (A : Matrix (Fin 4) (Fin 4) ℂ) :
    pfaffian 2 A = pfaffian4 (A 0 1) (A 0 2) (A 0 3) (A 1 2) (A 1 3) (A 2 3) := by
  rw [pfaffian4]
  rw [pfaffian]
  simp [Fin.sum_univ_three, pfaffian, Fin.succAbove]
  norm_num
  ring


/-- The m=1 base of the general induction: for an antisymmetric 2×2 matrix, the square of the
recursive Pfaffian equals the determinant — `pfaffian 1 A ^ 2 = A.det`, using the recursion (not
the explicit `pfaffian2` form). -/
theorem pfaffian_sq_eq_det_2 (A : Matrix (Fin 2) (Fin 2) ℂ)
    (h00 : A 0 0 = 0) (h11 : A 1 1 = 0) (h10 : A 1 0 = -A 0 1) :
    pfaffian 1 A ^ 2 = A.det := by
  rw [pfaffian_rec_2, pfaffian2_sq_eq_det]
  congr 1
  ext i j
  fin_cases i <;> fin_cases j <;> simp [h00, h11, h10]
