import Mathlib
import PaclandProof.QM.CayleyGeneral

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Cayley step 3 — the matching side

A perfect matching on `Fin (2m)` is a fixed-point-free involution (already in
`CayleyGeneral` as `IsMatching`). Here we build the signed matching sum that the
Pfaffian is: the canonical matching sign ε (the crossing number) and the signed
matching term. The 2×2 base pins the convention: the single edge has sign `+1`.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The crossing number of a matching: pairs of upper representatives `i < j` with `j < τ i`. -/
def matchingCrossings {m : ℕ} (τ : Equiv.Perm (Fin (2*m))) : ℕ :=
  ((matchingUpperSupport τ).product (matchingUpperSupport τ)).filter
    (fun p => p.1 < p.2 ∧ p.2 < τ p.1) |>.card

/-- The canonical matching sign: `(-1)^crossings`. -/
def matchingSign {m : ℕ} (τ : Equiv.Perm (Fin (2*m))) (_hm : IsMatching τ) : ℤ :=
  (-1 : ℤ) ^ matchingCrossings τ

/-- The signed matching term: `ε(τ) · ∏_{i < τ i} A(i, τ i)`. -/
def matchingTerm {m : ℕ} (A : Matrix (Fin (2*m)) (Fin (2*m)) ℂ) (τ : Equiv.Perm (Fin (2*m)))
    (hm : IsMatching τ) : ℂ :=
  ((matchingSign τ hm : ℤ) : ℂ) * (∏ i ∈ matchingUpperSupport τ, A i (τ i))

/-- **2×2 base**: the single matching `{0, 1}` has canonical sign `+1`, pinning the
convention (the Pfaffian of `[[0,a],[-a,0]]` is `+a`). -/
theorem matchingSign_eq_one_of_two :
    matchingSign (m := 1) (Equiv.swap (0 : Fin (2*1)) 1)
      (by constructor
          · ext i; fin_cases i <;> rfl
          · intro i; fin_cases i <;> norm_num) = 1 := by
  native_decide

end QM
