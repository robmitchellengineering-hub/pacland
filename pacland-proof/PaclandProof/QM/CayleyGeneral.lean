import Mathlib
import PaclandProof.QM.Matchgate

open scoped BigOperators

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

/-- Step 2 (ingredient 1): reversing all cycles of a permutation negates the antisymmetric product
over its support by `(-1)^(#σ.support)`.

Reindex `∏ i, A (σ⁻¹ i) i` by the bijection `σ⁻¹` (which permutes `σ.support`), turning the
`A (σ⁻¹ i) i` factor into `A j (σ j)`; then antisymmetry `A j i = -A i j` negates each factor.
This is the algebra behind "reversing an odd cycle negates the product": when `σ` is a single cycle
its support *is* the cycle, so the exponent `#σ.support` is exactly the cycle length. -/
theorem prod_support_apply_inv_eq_neg_pow {m : ℕ} (σ : Equiv.Perm (Fin m))
    (A : Matrix (Fin m) (Fin m) ℂ) (hA : A.transpose = -A) :
    (∏ i ∈ σ.support, A (σ⁻¹ i) i) = ((-1 : ℂ) ^ σ.support.card) * ∏ i ∈ σ.support, A (σ i) i := by
  have hantisymm : ∀ i j, A i j = - A j i := by
    intro i j
    have h := congr_fun (congr_fun hA j) i
    simpa [Matrix.transpose_apply] using h
  calc
    (∏ i ∈ σ.support, A (σ⁻¹ i) i)
        = ∏ j ∈ σ.support, A j (σ j) := by
          refine Finset.prod_equiv σ.symm ?_ ?_
          · intro i
            simpa using (Equiv.Perm.apply_mem_support (f := σ⁻¹) (x := i)).symm
          · intro i _
            rw [Equiv.apply_symm_apply]
            rfl
    _ = ∏ j ∈ σ.support, - A (σ j) j := by
          refine Finset.prod_congr rfl ?_
          intro j _
          exact hantisymm j (σ j)
    _ = ((-1 : ℂ) ^ σ.support.card) * ∏ j ∈ σ.support, A (σ j) j := by
          simpa using (Finset.prod_neg (s := σ.support) (f := fun j => A (σ j) j))

/-- Step 2 (ingredient 1, odd case): when the support (equivalently, for a cycle, the cycle length)
has odd cardinality, `(-1)^(#σ.support) = -1`, so reversing the cycles negates the product. -/
theorem prod_support_apply_eq_neg_inv_of_odd {m : ℕ} (σ : Equiv.Perm (Fin m))
    (A : Matrix (Fin m) (Fin m) ℂ) (hA : A.transpose = -A) (hodd : Odd σ.support.card) :
    (∏ i ∈ σ.support, A (σ i) i) = - (∏ i ∈ σ.support, A (σ⁻¹ i) i) := by
  simpa [hodd.neg_one_pow] using (prod_support_apply_inv_eq_neg_pow σ⁻¹ A hA)

/-- Step 2 (single-cycle form): for a single odd-length cycle `c`, reversing the cycle negates the
antisymmetric product over its support. The `IsCycle` hypothesis is carried to match the intended
pairing (its twin is `c⁻¹`); the identity itself holds for any permutation. -/
theorem prod_support_apply_eq_neg_inv_of_odd_cycle {m : ℕ} (c : Equiv.Perm (Fin m)) (hc : c.IsCycle)
    (A : Matrix (Fin m) (Fin m) ℂ) (hA : A.transpose = -A) (hodd : Odd c.support.card) :
    (∏ i ∈ c.support, A (c i) i) = - (∏ i ∈ c.support, A (c⁻¹ i) i) :=
  prod_support_apply_eq_neg_inv_of_odd c A hA hodd

/-- Step 2 (ingredient 2): reversing a permutation does not change its sign, so the
"reverse-one-odd-cycle" twin keeps the same sign while negating the product — the two Leibniz terms
cancel. For a single cycle the twin is `σ⁻¹`; in general the twin reverses exactly one odd cycle and
has the same cycle type, hence the same sign via `Equiv.Perm.sign_of_cycleType`. -/
theorem sign_inv_eq_sign {m : ℕ} (σ : Equiv.Perm (Fin m)) :
    (Equiv.Perm.sign σ⁻¹ : ℤ) = Equiv.Perm.sign σ := by
  rw [Equiv.Perm.sign_inv]

/-- Step 3 (ingredient): the sign of a fixed-point-free involution on `Fin (2m)` — a perfect
matching, i.e. a product of `m` disjoint transpositions — is `(-1)^m`. This is the sign carried by
each matching in the signed matching sum that defines the Pfaffian. -/
theorem sign_fixedPointFree_involution {m : ℕ} (σ : Equiv.Perm (Fin (2 * m)))
    (hinv : σ ^ 2 = 1) (hfree : ∀ i, σ i ≠ i) :
    (Equiv.Perm.sign σ : ℤ) = (-1 : ℤ) ^ m := by
  rw [Equiv.Perm.sign_of_pow_two_eq_one hinv]
  have hfixed : Function.fixedPoints σ = ∅ := by
    ext i
    simp [Function.mem_fixedPoints, Function.IsFixedPt, hfree i]
  simp [hfixed, Fintype.card_fin]

/-- Step 2 final (ingredient): for a disjoint product `σ * τ`, the permutation `τ` fixes
`σ.support`, so the product over `σ.support` is unaffected by `τ`. This is the factorization that
lets the odd-cycle reversal (which only touches one cycle) act independently on one factor. -/
theorem prod_mul_disjoint_support (σ τ : Equiv.Perm (Fin n)) (h : σ.Disjoint τ)
    (A : Matrix (Fin n) (Fin n) ℂ) :
    (∏ i ∈ σ.support, A ((σ * τ) i) i) = ∏ i ∈ σ.support, A (σ i) i := by
  refine Finset.prod_congr rfl ?_
  intro i hi
  have hτ : τ i = i := by
    rcases h i with hσ | hτ
    · exact False.elim ((Equiv.Perm.mem_support.mp hi) hσ)
    · exact hτ
  simp [mul_apply, hτ]

/-- Step 2 final: the Leibniz product over the support of a disjoint product factors as the
product over the two cycle supports. This is the factorization behind "reversing one odd cycle
negates only that cycle's factor". -/
theorem prod_mul_disjoint_support_full (σ τ : Equiv.Perm (Fin n)) (h : σ.Disjoint τ)
    (A : Matrix (Fin n) (Fin n) ℂ) :
    (∏ i ∈ (σ * τ).support, A ((σ * τ) i) i)
      = (∏ i ∈ σ.support, A (σ i) i) * (∏ i ∈ τ.support, A (τ i) i) := by
  rw [h.support_mul]
  rw [Finset.prod_union h.disjoint_support]
  congr 1
  · exact prod_mul_disjoint_support σ τ h A
  · calc
      (∏ i ∈ τ.support, A ((σ * τ) i) i) = ∏ i ∈ τ.support, A ((τ * σ) i) i := by
        refine Finset.prod_congr rfl ?_
        intro i _
        rw [h.commute]
      _ = ∏ i ∈ τ.support, A (τ i) i := prod_mul_disjoint_support τ σ h.symm A

/-- Step 2 final (the pairing): reversing one odd cycle `c` inside a disjoint product `c * τ`
keeps the sign but negates the Leibniz product over the support, so the two terms cancel in the
determinant sum. This is the odd-cycle cancellation. -/
theorem twin_sign_eq_product_neg (c τ : Equiv.Perm (Fin n)) (hdisj : c.Disjoint τ)
    (A : Matrix (Fin n) (Fin n) ℂ) (hA : A.transpose = -A) (hodd : Odd c.support.card) :
    ((Equiv.Perm.sign (c⁻¹ * τ) : ℤ) : ℂ) * (∏ i ∈ (c⁻¹ * τ).support, A ((c⁻¹ * τ) i) i)
      = - (((Equiv.Perm.sign (c * τ) : ℤ) : ℂ) * (∏ i ∈ (c * τ).support, A ((c * τ) i) i)) := by
  have hsign : (Equiv.Perm.sign (c⁻¹ * τ) : ℤ) = Equiv.Perm.sign (c * τ) := by
    rw [Equiv.Perm.sign_mul, Equiv.Perm.sign_mul, Equiv.Perm.sign_inv c]
  have hdisj_inv : c⁻¹.Disjoint τ := by
    intro x
    rcases hdisj x with hc | hτ
    · left
      exact ((Equiv.apply_eq_iff_eq_symm_apply (f := c)).mp hc).symm
    · right
      exact hτ
  have hprod : (∏ i ∈ (c⁻¹ * τ).support, A ((c⁻¹ * τ) i) i)
      = - (∏ i ∈ (c * τ).support, A ((c * τ) i) i) := by
    rw [prod_mul_disjoint_support_full c⁻¹ τ hdisj_inv A, prod_mul_disjoint_support_full c τ hdisj A]
    rw [Equiv.Perm.support_inv c]
    have hneg : (∏ i ∈ c.support, A (c⁻¹ i) i) = - (∏ i ∈ c.support, A (c i) i) := by
      rw [← neg_neg (∏ i ∈ c.support, A (c⁻¹ i) i)]
      congr 1
      exact (prod_support_apply_eq_neg_inv_of_odd c A hA hodd).symm
    rw [hneg]
    ring
  rw [hsign, hprod]
  ring

/-- Step 2 final (ingredient): an odd-length cycle has sign +1 — `IsCycle.sign` gives
`-(-1)^#support`, and for odd support that is `-(-1) = 1`. Combined with `sign_inv_eq_sign`, this is
why the reverse-twin keeps the same sign. -/
theorem sign_odd_cycle_eq_one {m : ℕ} (c : Equiv.Perm (Fin m)) (hc : c.IsCycle)
    (hodd : Odd c.support.card) :
    (Equiv.Perm.sign c : ℤ) = 1 := by
  rw [hc.sign]
  rw [hodd.neg_one_pow]
  norm_num

/-- Step 2 final: reverse the cycle of `σ` containing `0` — the odd-cycle-cancellation involution.
`φ σ = c⁻¹ * σ * c⁻¹`? No: if `σ = c * τ` with `c = σ.cycleOf 0` and `τ` disjoint, the twin that
reverses `c` is `c⁻¹ * τ = c⁻² * σ` (since `τ = c⁻¹ * σ`). This is the pairing used to cancel the
odd-cycle terms. -/
def reverseZeroCycle {n : ℕ} (σ : Equiv.Perm (Fin (n + 1))) : Equiv.Perm (Fin (n + 1)) :=
  (Equiv.Perm.cycleOf σ 0)⁻¹ * (Equiv.Perm.cycleOf σ 0)⁻¹ * σ

/-- The cycle of `0` in `reverseZeroCycle σ` is the inverse of the cycle of `0` in `σ`. -/
theorem reverseZeroCycle_cycleOf_zero {n : ℕ} (σ : Equiv.Perm (Fin (n + 1))) (h0 : σ 0 ≠ 0) :
    (reverseZeroCycle σ).cycleOf 0 = (σ.cycleOf 0)⁻¹ := by
  let c := σ.cycleOf 0
  let τ := c⁻¹ * σ
  have hcm : c ∈ σ.cycleFactorsFinset := by
    rw [Equiv.Perm.cycleOf_mem_cycleFactorsFinset_iff]
    exact (Equiv.Perm.mem_support.mpr h0)
  have hcIsCycle : c.IsCycle := (Equiv.Perm.mem_cycleFactorsFinset_iff.mp hcm).1
  have hcx : ∀ x, x ∈ c.support → σ x = c x := by
    intro x hx
    exact ((Equiv.Perm.mem_cycleFactorsFinset_iff.mp hcm).2 x hx).symm
  have hdisj : c.Disjoint τ := by
    intro x
    by_cases hx : x ∈ c.support
    · right
      dsimp [τ]
      simp [hcx x hx]
    · left
      by_contra h
      exact hx (Equiv.Perm.mem_support.mpr h)
  have hdisj_inv : c⁻¹.Disjoint τ := by
    intro x
    rcases hdisj x with hc | hτ
    · left
      exact (Equiv.eq_symm_apply (e := c)).mpr hc |>.symm
    · right
      exact hτ
  have hcomm : Commute c⁻¹ τ := Equiv.Perm.Disjoint.commute hdisj_inv
  have h0c : 0 ∈ c.support := by
    rw [Equiv.Perm.mem_support, Equiv.Perm.cycleOf_apply_self]
    exact h0
  have hτ0 : τ 0 = 0 := by
    rcases hdisj 0 with hc0 | hτ0
    · exfalso
      exact (Equiv.Perm.mem_support.mp h0c) hc0
    · exact hτ0
  have hmul : (c⁻¹ * τ).cycleOf 0 = (c⁻¹).cycleOf 0 :=
    Equiv.Perm.cycleOf_mul_of_apply_right_eq_self (f := c⁻¹) (g := τ) hcomm 0 hτ0
  have hc0_ne : c 0 ≠ 0 := Equiv.Perm.mem_support.mp h0c
  have hc_inv_0 : c⁻¹ 0 ≠ 0 := by
    intro h
    exact hc0_ne (by simpa using (congr_arg c h).symm)
  have hc_inv_IsCycle : c⁻¹.IsCycle := hcIsCycle.inv
  have hc_inv_cycle : (c⁻¹).cycleOf 0 = c⁻¹ := by
    rw [Equiv.Perm.IsCycle.cycleOf hc_inv_IsCycle]
    split_ifs with h
    · exfalso
      exact hc_inv_0 h
    · rfl
  have hre : reverseZeroCycle σ = c⁻¹ * τ := by
    dsimp [reverseZeroCycle, τ]
    rw [mul_assoc]
  calc
    (reverseZeroCycle σ).cycleOf 0 = (c⁻¹ * τ).cycleOf 0 := by rw [hre]
    _ = (c⁻¹).cycleOf 0 := hmul
    _ = c⁻¹ := hc_inv_cycle
    _ = (σ.cycleOf 0)⁻¹ := by simp [c]

/-- `reverseZeroCycle` is an involution (on permutations that move `0`). -/
theorem reverseZeroCycle_involution {n : ℕ} (σ : Equiv.Perm (Fin (n + 1))) (h0 : σ 0 ≠ 0) :
    reverseZeroCycle (reverseZeroCycle σ) = σ := by
  let c := σ.cycleOf 0
  have h : (reverseZeroCycle σ).cycleOf 0 = c⁻¹ := reverseZeroCycle_cycleOf_zero σ h0
  calc
    reverseZeroCycle (reverseZeroCycle σ)
        = ((reverseZeroCycle σ).cycleOf 0)⁻¹ * ((reverseZeroCycle σ).cycleOf 0)⁻¹ *
            (reverseZeroCycle σ) := rfl
    _ = (c⁻¹)⁻¹ * (c⁻¹)⁻¹ * (reverseZeroCycle σ) := by rw [h]
    _ = c * c * (reverseZeroCycle σ) := by simp [inv_inv]
    _ = c * c * (c⁻¹ * c⁻¹ * σ) := rfl
    _ = σ := by group

/-- Reversing the cycle of `0` negates the Leibniz term (over the support), so the two terms
cancel in the determinant sum. This wires the involution into the odd-cycle cancellation. -/
theorem reverseZeroCycle_term_neg {n : ℕ} (σ : Equiv.Perm (Fin (n + 1)))
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℂ) (hA : A.transpose = -A)
    (h0 : σ 0 ≠ 0) (hodd : Odd (σ.cycleOf 0).support.card) :
    ((Equiv.Perm.sign (reverseZeroCycle σ) : ℤ) : ℂ) * (∏ i ∈ (reverseZeroCycle σ).support, A ((reverseZeroCycle σ) i) i)
      = - (((Equiv.Perm.sign σ : ℤ) : ℂ) * (∏ i ∈ σ.support, A (σ i) i)) := by
  let c := σ.cycleOf 0
  let τ := c⁻¹ * σ
  have hcm : c ∈ σ.cycleFactorsFinset := by
    rw [Equiv.Perm.cycleOf_mem_cycleFactorsFinset_iff]
    exact (Equiv.Perm.mem_support.mpr h0)
  have hcx : ∀ x, x ∈ c.support → σ x = c x := by
    intro x hx
    exact ((Equiv.Perm.mem_cycleFactorsFinset_iff.mp hcm).2 x hx).symm
  have hdisj : c.Disjoint τ := by
    intro x
    by_cases hx : x ∈ c.support
    · right
      dsimp [τ]
      simp [hcx x hx]
    · left
      by_contra h
      exact hx (Equiv.Perm.mem_support.mpr h)
  have hσ : c * τ = σ := by
    dsimp [τ]
    group
  have hr : reverseZeroCycle σ = c⁻¹ * τ := by
    dsimp [reverseZeroCycle, τ]
    rw [mul_assoc]
  have hneg := twin_sign_eq_product_neg c τ hdisj A hA hodd
  simpa [hσ, ← hr] using hneg

/-- For a fixed-point-free permutation, the Leibniz product over all of `Fin n` equals the
product over the support — the bridge from the determinant's `∏ i` to the support-based
odd-cycle lemmas. -/
theorem prod_univ_eq_prod_support {n : ℕ} (σ : Equiv.Perm (Fin n))
    (A : Matrix (Fin n) (Fin n) ℂ) (hfree : ∀ i, σ i ≠ i) :
    (∏ i : Fin n, A (σ i) i) = ∏ i ∈ σ.support, A (σ i) i := by
  have hs : σ.support = Finset.univ := by
    ext i
    simp [Equiv.Perm.mem_support, hfree i]
  rw [hs]

/-- `reverseZeroCycle` preserves the support (reversing a cycle keeps the same moved points). -/
theorem reverseZeroCycle_support {n : ℕ} (σ : Equiv.Perm (Fin (n + 1))) (h0 : σ 0 ≠ 0) :
    (reverseZeroCycle σ).support = σ.support := by
  let c := σ.cycleOf 0
  let τ := c⁻¹ * σ
  have hcm : c ∈ σ.cycleFactorsFinset := by
    rw [Equiv.Perm.cycleOf_mem_cycleFactorsFinset_iff]
    exact (Equiv.Perm.mem_support.mpr h0)
  have hcx : ∀ x, x ∈ c.support → σ x = c x := by
    intro x hx
    exact ((Equiv.Perm.mem_cycleFactorsFinset_iff.mp hcm).2 x hx).symm
  have hdisj : c.Disjoint τ := by
    intro x
    by_cases hx : x ∈ c.support
    · right
      dsimp [τ]
      simp [hcx x hx]
    · left
      by_contra h
      exact hx (Equiv.Perm.mem_support.mpr h)
  have hdisj_inv : c⁻¹.Disjoint τ := by
    intro x
    rcases hdisj x with hc | hτ
    · left
      exact (Equiv.eq_symm_apply (e := c)).mpr hc |>.symm
    · right
      exact hτ
  have hσ : c * τ = σ := by
    dsimp [τ]
    group
  have hr : reverseZeroCycle σ = c⁻¹ * τ := by
    dsimp [reverseZeroCycle, τ]
    rw [mul_assoc]
  rw [hr, hσ]
  rw [hdisj_inv.support_mul, hdisj.support_mul, Equiv.Perm.support_inv c]

/-- The full (univ) term-negation: the determinant term of `reverseZeroCycle σ` is the negative of
`σ`'s, for fixed-point-free `σ` with an odd cycle of `0`. -/
theorem reverseZeroCycle_term_neg_univ {n : ℕ} (σ : Equiv.Perm (Fin (n + 1)))
    (A : Matrix (Fin (n + 1)) (Fin (n + 1)) ℂ) (hA : A.transpose = -A)
    (h0 : σ 0 ≠ 0) (hfree : ∀ i, σ i ≠ i) (hodd : Odd (σ.cycleOf 0).support.card) :
    ((Equiv.Perm.sign (reverseZeroCycle σ) : ℤ) : ℂ) * (∏ i : Fin (n + 1), A ((reverseZeroCycle σ) i) i)
      = - (((Equiv.Perm.sign σ : ℤ) : ℂ) * (∏ i : Fin (n + 1), A (σ i) i)) := by
  have hfree' : ∀ i, (reverseZeroCycle σ) i ≠ i := by
    intro i
    have hs := reverseZeroCycle_support σ h0
    rw [hs]
    exact hfree i
  rw [prod_univ_eq_prod_support (reverseZeroCycle σ) A hfree',
      prod_univ_eq_prod_support σ A hfree]
  exact reverseZeroCycle_term_neg σ A hA h0 hodd

end QM
