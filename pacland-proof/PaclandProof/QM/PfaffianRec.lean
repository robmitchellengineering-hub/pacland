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
