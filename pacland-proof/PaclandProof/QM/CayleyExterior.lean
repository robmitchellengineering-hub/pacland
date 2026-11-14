import Mathlib
import PaclandProof.QM.Matchgate
import PaclandProof.QM.PfaffianRec

open BigOperators
open QM

noncomputable section

/-- The standard basis vector `eᵢ` of `Fin n → ℂ`. -/
def stdBasis (n : ℕ) (i : Fin n) : Fin n → ℂ := fun j => if i = j then 1 else 0

/-- The m=1 exterior-algebra identity: the 2-form `ω = A₀₁ e₀ ∧ e₁` equals `Pf(A)·vol` where
`vol = e₀ ∧ e₁`. This is the base of the exterior-algebra route to the general Cayley `det = Pf²`
(issue #431). -/
theorem omega_eq_pf_mul_vol_1 (A : Matrix (Fin 2) (Fin 2) ℂ) :
    (A 0 1 • (ExteriorAlgebra.ι ℂ (stdBasis 2 0) * ExteriorAlgebra.ι ℂ (stdBasis 2 1)))
      = pfaffian 1 A • (ExteriorAlgebra.ιMulti ℂ 2 (stdBasis 2)) := by
  rw [pfaffian_rec_2]
  simp [pfaffian2]
  rw [ExteriorAlgebra.ιMulti_apply]
  simp [List.ofFn, List.prod, stdBasis]

end
