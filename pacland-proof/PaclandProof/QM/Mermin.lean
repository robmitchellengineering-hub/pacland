import Mathlib

/-!
# The Mermin–Peres magic square — a finite Kochen–Specker-type contextuality proof

A concrete finite certificate that no non-contextual ±1 assignment to quantum observables is
possible. The nine two-qubit Pauli observables

    σx⊗I   I⊗σx   σx⊗σx
    I⊗σy   σy⊗I   σy⊗σy
    σx⊗σy  σy⊗σx  σz⊗σz

are arranged so that the three observables in each row and each column commute, and their
products are `+I₄` for every row and the first two columns, but `−I₄` for the last column. A
non-contextual ±1 value assignment would then have product `+1` computed along rows and `−1`
computed along columns over the *same* nine values — impossible. Here we kernel-check the
matrix products that force the contradiction.
-/

namespace QM

noncomputable section

open scoped ComplexOrder

/-- The Pauli-σx matrix (complex). -/
def σx : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

/-- The Pauli-σy matrix (complex). -/
def σy : Matrix (Fin 2) (Fin 2) ℂ := !![0, -Complex.I; Complex.I, 0]

/-- The Pauli-σz matrix (complex). -/
def σz : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- The 2×2 identity. -/
def id2 : Matrix (Fin 2) (Fin 2) ℂ := 1

/-- The Kronecker product of two 2×2 matrices (a 4×4 matrix indexed by `Fin 2 × Fin 2`). -/
def kron (A B : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  fun x y => A x.1 y.1 * B x.2 y.2

/-- `(A⊗B)(C⊗D) = (AC)⊗(BD)`. -/
lemma kron_mul (A B C D : Matrix (Fin 2) (Fin 2) ℂ) :
    (kron A B) * (kron C D) = kron (A * C) (B * D) := by
  ext x y
  simp only [Matrix.mul_apply, kron]
  rw [← Finset.univ_product_univ, Finset.sum_product]
  simp only [Fin.sum_univ_two, mul_assoc, mul_left_comm, mul_comm]
  ring_nf

/-- Scalars factor out of the Kronecker product. -/
lemma kron_smul (c d : ℂ) (A B : Matrix (Fin 2) (Fin 2) ℂ) :
    kron (c • A) (d • B) = (c * d) • kron A B := by
  ext x y
  simp [kron, smul_apply, mul_assoc, mul_left_comm, mul_comm]

/-- `kron (i I₂) (-(i I₂)) = I₄`. -/
lemma kron_i_neg_i : kron (Complex.I • id2) (-(Complex.I • id2)) = kron id2 id2 := by
  rw [← neg_smul]
  rw [kron_smul]
  norm_num [Complex.I_mul_I]

/-- Each Pauli matrix squares to the identity. -/
lemma σx_sq : σx * σx = id2 := by ext i j; fin_cases i <;> fin_cases j <;> norm_num [σx, id2]
lemma σy_sq : σy * σy = id2 := by ext i j; fin_cases i <;> fin_cases j <;> norm_num [σy, id2]
lemma σz_sq : σz * σz = id2 := by ext i j; fin_cases i <;> fin_cases j <;> norm_num [σz, id2]

/-- `σx σy σz = i I`. -/
lemma σxσyσz : σx * σy * σz = Complex.I • id2 := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [σx, σy, σz, id2]

/-- `σy σx σz = -i I`. -/
lemma σyσxσz : σy * σx * σz = -Complex.I • id2 := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [σx, σy, σz, id2]

/-- The nine Mermin observables. -/
def mermin : Fin 3 → Fin 3 → Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ
  | 0, 0 => kron σx id2
  | 0, 1 => kron id2 σx
  | 0, 2 => kron σx σx
  | 1, 0 => kron id2 σy
  | 1, 1 => kron σy id2
  | 1, 2 => kron σy σy
  | 2, 0 => kron σx σy
  | 2, 1 => kron σy σx
  | 2, 2 => kron σz σz

/-- The identity 4×4 (as `kron id2 id2`). -/
def id4 : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ := kron id2 id2

/-- **Mermin square.** Row products are `+I₄`; the last column product is `−I₄`, the first two `+I₄`. -/
lemma mermin_row_products :
    (mermin 0 0 * mermin 0 1 * mermin 0 2 = id4) ∧
    (mermin 1 0 * mermin 1 1 * mermin 1 2 = id4) ∧
    (mermin 2 0 * mermin 2 1 * mermin 2 2 = id4) := by
  constructor
  · simp [mermin, id4, kron_mul, σx_sq, id2, mul_one, one_mul]
  constructor
  · simp [mermin, id4, kron_mul, σy_sq, id2, mul_one, one_mul]
  · calc
      mermin 2 0 * mermin 2 1 * mermin 2 2
          = kron (σx * σy * σz) (σy * σx * σz) := by simp [mermin, kron_mul]
      _ = kron (Complex.I • id2) (-(Complex.I • id2)) := by rw [σxσyσz, σyσxσz, ← neg_smul]
      _ = id4 := by rw [kron_i_neg_i, id4]

lemma mermin_col_products :
    (mermin 0 0 * mermin 1 0 * mermin 2 0 = id4) ∧
    (mermin 0 1 * mermin 1 1 * mermin 2 1 = id4) ∧
    (mermin 0 2 * mermin 1 2 * mermin 2 2 = -id4) := by
  constructor
  · simp [mermin, id4, kron_mul, σx_sq, σy_sq, id2, mul_one, one_mul]
  constructor
  · simp [mermin, id4, kron_mul, σy_sq, σx_sq, id2, mul_one, one_mul]
  · simp [mermin, id4, kron_mul, kron_smul, σxσyσz, id2, smul_smul, mul_comm,
      Complex.I_mul_I]

/-- The Mermin contradiction: no ±1 assignment `v` to the nine observables is consistent with
both the row and column products. -/
theorem mermin_no_value_assignment :
    ¬ ∃ v : Fin 3 → Fin 3 → ℂ, (∀ i j, v i j = 1 ∨ v i j = -1) ∧
      (∀ i, v i 0 * v i 1 * v i 2 = 1) ∧
      (v 0 0 * v 1 0 * v 2 0 = 1) ∧ (v 0 1 * v 1 1 * v 2 1 = 1) ∧
      (v 0 2 * v 1 2 * v 2 2 = -1) := by
  rintro ⟨v, hval, hrow, hcol1, hcol2, hcol3⟩
  -- product along rows = product along columns (the same nine values)
  have hrows : (∏ i : Fin 3, ∏ j : Fin 3, v i j) = 1 := by
    simp only [Fin.prod_univ_three]
    rw [hrow 0, hrow 1, hrow 2]
    norm_num
  have hcols : (∏ i : Fin 3, ∏ j : Fin 3, v i j) = -1 := by
    rw [Finset.prod_comm]
    simp only [Fin.prod_univ_three]
    rw [hcol1, hcol2, hcol3]
    norm_num
  rw [hrows] at hcols
  norm_num at hcols

end

end QM
