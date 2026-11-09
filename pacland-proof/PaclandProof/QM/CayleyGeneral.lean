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

/-- Step 1 (continued): when a permutation `σ` has a fixed point `i`, the Leibniz product
`∏ j, A (σ j) j` vanishes, because its factor `A (σ i) i = A i i = 0`. This is what lets us
restrict the determinant sum to fixed-point-free permutations. -/
theorem prod_eq_zero_of_fixedPoint (A : Matrix (Fin n) (Fin n) ℂ) (hA : A.transpose = -A)
    (σ : Equiv.Perm (Fin n)) {i : Fin n} (hi : σ i = i) :
    (∏ j, A (σ j) j) = 0 := by
  have hzero : A (σ i) i = 0 := by
    rw [hi]
    exact antisymm_diagonal_eq_zero A hA i
  exact (Finset.prod_eq_zero_iff.mpr ⟨i, Finset.mem_univ i, hzero⟩)

end QM
