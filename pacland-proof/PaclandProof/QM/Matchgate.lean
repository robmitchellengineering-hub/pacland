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

/-- The `Fin.succ` numeral lemmas missing from Mathlib (only 0→1 and 1→2 exist). -/
@[simp] lemma fin_succ_two_eq_three : Fin.succ (2 : Fin 3) = 3 := rfl
@[simp] lemma fin_succ_three_eq_four : Fin.succ (3 : Fin 4) = 4 := rfl

/-- **The general 4×4 determinant** (in the general `Matrix (Fin 4)` form, so it applies to submatrix
minors — the form Mathlib's `det_fin_three` has but `det_fin_four` was missing). -/
theorem det_fin_four (A : Matrix (Fin 4) (Fin 4) ℂ) :
    A.det = A 0 0 * A 1 1 * A 2 2 * A 3 3 - A 0 0 * A 1 1 * A 2 3 * A 3 2 - A 0 0 * A 1 2 * A 2 1 * A 3 3  +  A 0 0 * A 1 2 * A 2 3 * A 3 1  +  A 0 0 * A 1 3 * A 2 1 * A 3 2 - A 0 0 * A 1 3 * A 2 2 * A 3 1 - A 0 1 * A 1 0 * A 2 2 * A 3 3  +  A 0 1 * A 1 0 * A 2 3 * A 3 2  +  A 0 1 * A 1 2 * A 2 0 * A 3 3 - A 0 1 * A 1 2 * A 2 3 * A 3 0 - A 0 1 * A 1 3 * A 2 0 * A 3 2  +  A 0 1 * A 1 3 * A 2 2 * A 3 0  +  A 0 2 * A 1 0 * A 2 1 * A 3 3 - A 0 2 * A 1 0 * A 2 3 * A 3 1 - A 0 2 * A 1 1 * A 2 0 * A 3 3  +  A 0 2 * A 1 1 * A 2 3 * A 3 0  +  A 0 2 * A 1 3 * A 2 0 * A 3 1 - A 0 2 * A 1 3 * A 2 1 * A 3 0 - A 0 3 * A 1 0 * A 2 1 * A 3 2  +  A 0 3 * A 1 0 * A 2 2 * A 3 1  +  A 0 3 * A 1 1 * A 2 0 * A 3 2 - A 0 3 * A 1 1 * A 2 2 * A 3 0 - A 0 3 * A 1 2 * A 2 0 * A 3 1  +  A 0 3 * A 1 2 * A 2 1 * A 3 0 := by
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_four, Matrix.det_fin_three, Fin.succAbove,
    fin_succ_two_eq_three, fin_succ_three_eq_four]
  norm_num
  ring

/-- The `Fin.succ` numeral lemmas missing from Mathlib, for the 5×5/6×6 rung. -/
@[simp] lemma fin_succ_four_eq_five : Fin.succ (4 : Fin 5) = 5 := rfl

/-- **The general 5×5 determinant** (in the general `Matrix (Fin 5)` form, so it applies to the 6×6
cofactor's 5×5 minors). -/
theorem det_fin_five (A : Matrix (Fin 5) (Fin 5) ℂ) :
    A.det = A 0 0 * A 1 1 * A 2 2 * A 3 3 * A 4 4 - A 0 0 * A 1 1 * A 2 2 * A 3 4 * A 4 3 - A 0 0 * A 1 1 * A 2 3 * A 3 2 * A 4 4  +  A 0 0 * A 1 1 * A 2 3 * A 3 4 * A 4 2  +  A 0 0 * A 1 1 * A 2 4 * A 3 2 * A 4 3 - A 0 0 * A 1 1 * A 2 4 * A 3 3 * A 4 2 - A 0 0 * A 1 2 * A 2 1 * A 3 3 * A 4 4  +  A 0 0 * A 1 2 * A 2 1 * A 3 4 * A 4 3  +  A 0 0 * A 1 2 * A 2 3 * A 3 1 * A 4 4 - A 0 0 * A 1 2 * A 2 3 * A 3 4 * A 4 1 - A 0 0 * A 1 2 * A 2 4 * A 3 1 * A 4 3  +  A 0 0 * A 1 2 * A 2 4 * A 3 3 * A 4 1  +  A 0 0 * A 1 3 * A 2 1 * A 3 2 * A 4 4 - A 0 0 * A 1 3 * A 2 1 * A 3 4 * A 4 2 - A 0 0 * A 1 3 * A 2 2 * A 3 1 * A 4 4  +  A 0 0 * A 1 3 * A 2 2 * A 3 4 * A 4 1  +  A 0 0 * A 1 3 * A 2 4 * A 3 1 * A 4 2 - A 0 0 * A 1 3 * A 2 4 * A 3 2 * A 4 1 - A 0 0 * A 1 4 * A 2 1 * A 3 2 * A 4 3  +  A 0 0 * A 1 4 * A 2 1 * A 3 3 * A 4 2  +  A 0 0 * A 1 4 * A 2 2 * A 3 1 * A 4 3 - A 0 0 * A 1 4 * A 2 2 * A 3 3 * A 4 1 - A 0 0 * A 1 4 * A 2 3 * A 3 1 * A 4 2  +  A 0 0 * A 1 4 * A 2 3 * A 3 2 * A 4 1 - A 0 1 * A 1 0 * A 2 2 * A 3 3 * A 4 4  +  A 0 1 * A 1 0 * A 2 2 * A 3 4 * A 4 3  +  A 0 1 * A 1 0 * A 2 3 * A 3 2 * A 4 4 - A 0 1 * A 1 0 * A 2 3 * A 3 4 * A 4 2 - A 0 1 * A 1 0 * A 2 4 * A 3 2 * A 4 3  +  A 0 1 * A 1 0 * A 2 4 * A 3 3 * A 4 2  +  A 0 1 * A 1 2 * A 2 0 * A 3 3 * A 4 4 - A 0 1 * A 1 2 * A 2 0 * A 3 4 * A 4 3 - A 0 1 * A 1 2 * A 2 3 * A 3 0 * A 4 4  +  A 0 1 * A 1 2 * A 2 3 * A 3 4 * A 4 0  +  A 0 1 * A 1 2 * A 2 4 * A 3 0 * A 4 3 - A 0 1 * A 1 2 * A 2 4 * A 3 3 * A 4 0 - A 0 1 * A 1 3 * A 2 0 * A 3 2 * A 4 4  +  A 0 1 * A 1 3 * A 2 0 * A 3 4 * A 4 2  +  A 0 1 * A 1 3 * A 2 2 * A 3 0 * A 4 4 - A 0 1 * A 1 3 * A 2 2 * A 3 4 * A 4 0 - A 0 1 * A 1 3 * A 2 4 * A 3 0 * A 4 2  +  A 0 1 * A 1 3 * A 2 4 * A 3 2 * A 4 0  +  A 0 1 * A 1 4 * A 2 0 * A 3 2 * A 4 3 - A 0 1 * A 1 4 * A 2 0 * A 3 3 * A 4 2 - A 0 1 * A 1 4 * A 2 2 * A 3 0 * A 4 3  +  A 0 1 * A 1 4 * A 2 2 * A 3 3 * A 4 0  +  A 0 1 * A 1 4 * A 2 3 * A 3 0 * A 4 2 - A 0 1 * A 1 4 * A 2 3 * A 3 2 * A 4 0  +  A 0 2 * A 1 0 * A 2 1 * A 3 3 * A 4 4 - A 0 2 * A 1 0 * A 2 1 * A 3 4 * A 4 3 - A 0 2 * A 1 0 * A 2 3 * A 3 1 * A 4 4  +  A 0 2 * A 1 0 * A 2 3 * A 3 4 * A 4 1  +  A 0 2 * A 1 0 * A 2 4 * A 3 1 * A 4 3 - A 0 2 * A 1 0 * A 2 4 * A 3 3 * A 4 1 - A 0 2 * A 1 1 * A 2 0 * A 3 3 * A 4 4  +  A 0 2 * A 1 1 * A 2 0 * A 3 4 * A 4 3  +  A 0 2 * A 1 1 * A 2 3 * A 3 0 * A 4 4 - A 0 2 * A 1 1 * A 2 3 * A 3 4 * A 4 0 - A 0 2 * A 1 1 * A 2 4 * A 3 0 * A 4 3  +  A 0 2 * A 1 1 * A 2 4 * A 3 3 * A 4 0  +  A 0 2 * A 1 3 * A 2 0 * A 3 1 * A 4 4 - A 0 2 * A 1 3 * A 2 0 * A 3 4 * A 4 1 - A 0 2 * A 1 3 * A 2 1 * A 3 0 * A 4 4  +  A 0 2 * A 1 3 * A 2 1 * A 3 4 * A 4 0  +  A 0 2 * A 1 3 * A 2 4 * A 3 0 * A 4 1 - A 0 2 * A 1 3 * A 2 4 * A 3 1 * A 4 0 - A 0 2 * A 1 4 * A 2 0 * A 3 1 * A 4 3  +  A 0 2 * A 1 4 * A 2 0 * A 3 3 * A 4 1  +  A 0 2 * A 1 4 * A 2 1 * A 3 0 * A 4 3 - A 0 2 * A 1 4 * A 2 1 * A 3 3 * A 4 0 - A 0 2 * A 1 4 * A 2 3 * A 3 0 * A 4 1  +  A 0 2 * A 1 4 * A 2 3 * A 3 1 * A 4 0 - A 0 3 * A 1 0 * A 2 1 * A 3 2 * A 4 4  +  A 0 3 * A 1 0 * A 2 1 * A 3 4 * A 4 2  +  A 0 3 * A 1 0 * A 2 2 * A 3 1 * A 4 4 - A 0 3 * A 1 0 * A 2 2 * A 3 4 * A 4 1 - A 0 3 * A 1 0 * A 2 4 * A 3 1 * A 4 2  +  A 0 3 * A 1 0 * A 2 4 * A 3 2 * A 4 1  +  A 0 3 * A 1 1 * A 2 0 * A 3 2 * A 4 4 - A 0 3 * A 1 1 * A 2 0 * A 3 4 * A 4 2 - A 0 3 * A 1 1 * A 2 2 * A 3 0 * A 4 4  +  A 0 3 * A 1 1 * A 2 2 * A 3 4 * A 4 0  +  A 0 3 * A 1 1 * A 2 4 * A 3 0 * A 4 2 - A 0 3 * A 1 1 * A 2 4 * A 3 2 * A 4 0 - A 0 3 * A 1 2 * A 2 0 * A 3 1 * A 4 4  +  A 0 3 * A 1 2 * A 2 0 * A 3 4 * A 4 1  +  A 0 3 * A 1 2 * A 2 1 * A 3 0 * A 4 4 - A 0 3 * A 1 2 * A 2 1 * A 3 4 * A 4 0 - A 0 3 * A 1 2 * A 2 4 * A 3 0 * A 4 1  +  A 0 3 * A 1 2 * A 2 4 * A 3 1 * A 4 0  +  A 0 3 * A 1 4 * A 2 0 * A 3 1 * A 4 2 - A 0 3 * A 1 4 * A 2 0 * A 3 2 * A 4 1 - A 0 3 * A 1 4 * A 2 1 * A 3 0 * A 4 2  +  A 0 3 * A 1 4 * A 2 1 * A 3 2 * A 4 0  +  A 0 3 * A 1 4 * A 2 2 * A 3 0 * A 4 1 - A 0 3 * A 1 4 * A 2 2 * A 3 1 * A 4 0  +  A 0 4 * A 1 0 * A 2 1 * A 3 2 * A 4 3 - A 0 4 * A 1 0 * A 2 1 * A 3 3 * A 4 2 - A 0 4 * A 1 0 * A 2 2 * A 3 1 * A 4 3  +  A 0 4 * A 1 0 * A 2 2 * A 3 3 * A 4 1  +  A 0 4 * A 1 0 * A 2 3 * A 3 1 * A 4 2 - A 0 4 * A 1 0 * A 2 3 * A 3 2 * A 4 1 - A 0 4 * A 1 1 * A 2 0 * A 3 2 * A 4 3  +  A 0 4 * A 1 1 * A 2 0 * A 3 3 * A 4 2  +  A 0 4 * A 1 1 * A 2 2 * A 3 0 * A 4 3 - A 0 4 * A 1 1 * A 2 2 * A 3 3 * A 4 0 - A 0 4 * A 1 1 * A 2 3 * A 3 0 * A 4 2  +  A 0 4 * A 1 1 * A 2 3 * A 3 2 * A 4 0  +  A 0 4 * A 1 2 * A 2 0 * A 3 1 * A 4 3 - A 0 4 * A 1 2 * A 2 0 * A 3 3 * A 4 1 - A 0 4 * A 1 2 * A 2 1 * A 3 0 * A 4 3  +  A 0 4 * A 1 2 * A 2 1 * A 3 3 * A 4 0  +  A 0 4 * A 1 2 * A 2 3 * A 3 0 * A 4 1 - A 0 4 * A 1 2 * A 2 3 * A 3 1 * A 4 0 - A 0 4 * A 1 3 * A 2 0 * A 3 1 * A 4 2  +  A 0 4 * A 1 3 * A 2 0 * A 3 2 * A 4 1  +  A 0 4 * A 1 3 * A 2 1 * A 3 0 * A 4 2 - A 0 4 * A 1 3 * A 2 1 * A 3 2 * A 4 0 - A 0 4 * A 1 3 * A 2 2 * A 3 0 * A 4 1  +  A 0 4 * A 1 3 * A 2 2 * A 3 1 * A 4 0 := by
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_five, det_fin_four, Fin.succAbove, fin_succ_three_eq_four, fin_succ_four_eq_five]
  norm_num
  ring

/-- The 6×6 Pfaffian — the signed sum over the fifteen perfect matchings (the exact six-qubit
matchgate amplitude). -/
def pfaffian6 (a b c d e f g h i j k l m n o : ℂ) : ℂ :=
  a * j * o - a * k * n + a * l * m - b * g * o + b * h * n - b * i * m
  + c * f * o - c * h * l + c * i * k - d * f * n + d * g * l - d * i * j
  + e * f * m - e * g * k + e * h * j

/-- **Matchgate core (6×6).** The square of the 6×6 Pfaffian equals the determinant of the 6×6
antisymmetric matrix — the exact six-qubit matchgate amplitude, the next even rung after the 4×4. -/
theorem pfaffian6_sq_eq_det (a b c d e f g h i j k l m n o : ℂ) :
    pfaffian6 a b c d e f g h i j k l m n o ^ 2 =
      Matrix.det !![0, a, b, c, d, e; -a, 0, f, g, h, i; -b, -f, 0, j, k, l; -c, -g, -j, 0, m, n; -d, -h, -k, -m, 0, o; -e, -i, -l, -n, -o, 0] := by
  rw [pfaffian6]
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_six, det_fin_five, Fin.succAbove, fin_succ_four_eq_five]
  norm_num
  ring

/-- The 4×4 Pfaffian — the signed sum over the three perfect matchings (the exact four-qubit
matchgate amplitude). -/
def pfaffian4 (a b c d e f : ℂ) : ℂ :=
  a * f - b * e + c * d

/-- **Matchgate core (4×4, the even companion).** The square of the Pfaffian equals the determinant
of the 4×4 antisymmetric matrix — the exact four-qubit matchgate amplitude. -/
theorem pfaffian4_sq_eq_det (a b c d e f : ℂ) :
    pfaffian4 a b c d e f ^ 2 =
      Matrix.det !![0, a, b, c; -a, 0, d, e; -b, -d, 0, f; -c, -e, -f, 0] := by
  rw [pfaffian4]
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_four, Matrix.det_fin_three, Fin.succAbove]
  norm_num
  ring

/-- **The general sign theorem.** For any antisymmetric matrix over ℂ, `det A = (−1)ⁿ det A` —
the single structural fact that unifies the whole even/odd split. Odd `n` forces `det = 0` (the
corollary below); even `n` leaves `det` unchanged (and it is in fact a perfect square, Cayley). -/
theorem det_antisymm_sign {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℂ) (hA : Aᵀ = -A) :
    A.det = (-1 : ℂ) ^ Fintype.card n * A.det := by
  calc
    A.det = Aᵀ.det := (Matrix.det_transpose A).symm
    _ = (-A).det := by rw [hA]
    _ = (-1 : ℂ) ^ Fintype.card n * A.det := by simpa using (Matrix.det_smul A (-1 : ℂ))

/-- **The structural wall-move.** Any odd-dimensional antisymmetric matrix has determinant 0,
proved *structurally* (no cofactor computation): `det A = det Aᵀ = det (−A) = (−1)ⁿ det A`, and for
odd `n` this forces `det A = −det A`, hence `det A = 0`. This is the general theorem the 3×3 case
instantiates, and it is *why* the Pfaffian (and matchgates) is an even-dimensional object. -/
theorem det_antisymm_odd_eq_zero {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℂ) (hA : Aᵀ = -A) (hodd : Odd (Fintype.card n)) :
    A.det = 0 := by
  have h1 : A.det = Aᵀ.det := (Matrix.det_transpose A).symm
  have h2 : Aᵀ.det = (-A).det := by rw [hA]
  have h3 : (-A).det = (-1 : ℂ) ^ Fintype.card n * A.det := by
    simpa using (Matrix.det_smul A (-1 : ℂ))
  have h4 : (-1 : ℂ) ^ Fintype.card n = -1 := by
    rcases hodd with ⟨k, hk⟩
    rw [hk, pow_add, pow_mul]
    norm_num
  have hdet : A.det = -A.det := by
    calc
      A.det = Aᵀ.det := h1
      _ = (-A).det := h2
      _ = (-1 : ℂ) ^ Fintype.card n * A.det := h3
      _ = -1 * A.det := by rw [h4]
      _ = -A.det := by ring
  -- A.det = -A.det forces A.det = 0 (ℂ has characteristic 0)
  rw [eq_neg_iff_add_eq_zero] at hdet
  have htwo : (2 : ℂ) * A.det = 0 := by
    rw [show (2 : ℂ) * A.det = A.det + A.det by ring]
    exact hdet
  exact (eq_zero_or_eq_zero_of_mul_eq_zero htwo).resolve_left (by norm_num : (2 : ℂ) ≠ 0)

/-- **Odd dimension kills the determinant.** A 3×3 antisymmetric matrix has determinant 0 — the
reason matchgates (Pfaffians) exist only on an *even* number of qubits. Combined with the 2×2 case
(Pf² = det ≠ 0), this is the even/odd split: the Pfaffian is an even-dimensional object. -/
theorem det_three_antisymm_eq_zero (a b c : ℂ) :
    Matrix.det !![0, a, b; -a, 0, c; -b, -c, 0] = 0 := by
  rw [Matrix.det_fin_three]
  simp
  ring

end QM
