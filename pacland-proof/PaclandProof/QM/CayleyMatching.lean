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

/-- The 4-cycle `(0 1 2 3)` and its even/odd-edge split: even edges `(0 1)(2 3)`, odd edges
`(1 2)(3 0)`. -/
def sigma4 : Equiv.Perm (Fin 4) := Equiv.swap (0 : Fin 4) 3 * Equiv.swap 0 2 * Equiv.swap 0 1
def evenEdges4 : Equiv.Perm (Fin 4) := Equiv.swap (0 : Fin 4) 1 * Equiv.swap 2 3
def oddEdges4 : Equiv.Perm (Fin 4) := Equiv.swap (1 : Fin 4) 2 * Equiv.swap 3 0

/-- **Atomic unit of the bijection (4-cycle):** the determinant term of an even cycle equals the
product of the two matching terms — the sign and the antisymmetric weight balance exactly. This is
the local identity the full even-cycle ↔ pair-of-matchings bijection glues together. -/
theorem atomic4_weight (A : Matrix (Fin 4) (Fin 4) ℂ) (hA : A.transpose = -A) :
    ((Equiv.Perm.sign sigma4 : ℤ) : ℂ) * (A 1 0 * A 2 1 * A 3 2 * A 0 3)
    = ((Equiv.Perm.sign evenEdges4 : ℤ) : ℂ) * (A 0 1 * A 2 3)
      * ((Equiv.Perm.sign oddEdges4 : ℤ) : ℂ) * (A 0 3 * A 1 2) := by
  have hs4 : (Equiv.Perm.sign sigma4 : ℤ) = -1 := by native_decide
  have hs1 : (Equiv.Perm.sign evenEdges4 : ℤ) = 1 := by native_decide
  have hs2 : (Equiv.Perm.sign oddEdges4 : ℤ) = 1 := by native_decide
  rw [hs4, hs1, hs2]
  norm_num
  have h10 : A 1 0 = -A 0 1 := congr_fun (congr_fun hA 0) 1
  have h21 : A 2 1 = -A 1 2 := congr_fun (congr_fun hA 1) 2
  have h32 : A 3 2 = -A 2 3 := congr_fun (congr_fun hA 2) 3
  rw [h10, h21, h32]
  ring
