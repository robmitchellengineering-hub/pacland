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

/-- **The general 4×4 determinant** (the missing Mathlib lemma). The determinant of a general 4×4
matrix, by cofactor expansion along row 0. This is the reusable rung for the 6×6 (and the general
even-n Pfaffian): with `Fin.succAbove` unfolded, the cofactor minors reduce to 3×3 determinants. -/
theorem det_fin_four (a b c d e f g h i j k l m n o p : ℂ) :
    Matrix.det !![a, b, c, d; e, f, g, h; i, j, k, l; m, n, o, p] =
      a * (f * (k * p - l * o) - g * (j * p - l * n) + h * (j * o - k * n))
      - b * (e * (k * p - l * o) - g * (i * p - l * m) + h * (i * o - k * m))
      + c * (e * (j * p - l * n) - f * (i * p - l * m) + h * (i * n - j * m))
      - d * (e * (j * o - k * n) - f * (i * o - k * m) + g * (i * n - j * m)) := by
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_four, Matrix.det_fin_three, Fin.succAbove]
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
