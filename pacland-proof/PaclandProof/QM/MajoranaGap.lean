import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Majorana mass gap — a zero mode exists iff the mass matrix is singular

A system of Majorana fermions has an antisymmetric mass matrix `M`. Its "mass gap" is the
smallest mass in the spectrum; the system has a **zero mode** (a massless Majorana, the
topological edge of the spectrum) exactly when `M` has a nonzero null vector.

This is the linear-algebra core of the mass gap:

1. `gapped_iff_det_ne_zero` — the system is gapped (the mass map is injective) iff `det M ≠ 0`;
2. `hasZeroMode_iff_not_injective` — a zero mode exists iff the mass map is not injective;
3. `hasZeroMode_iff_det_eq_zero` — the Majorana zero-mode criterion: a zero mode exists iff
   `det M = 0`.

Together with the Cayley identity `det M = (Pf M)²` (the `QM` matching route), criterion 3 is
the standard fact that a Majorana zero mode exists iff the Pfaffian vanishes — the reason the
Pfaffian detects topological superconductivity. The `Pf` connection is stated here once
`det = Pf²` is closed.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- A Majorana zero mode: a nonzero vector annihilated by the mass matrix. -/
def hasZeroMode {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) : Prop :=
  ∃ v : Fin n → ℂ, v ≠ 0 ∧ M.mulVec v = 0

/-- The system is gapped (the mass map is injective) iff `det M ≠ 0`. -/
theorem gapped_iff_det_ne_zero {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) :
    Function.Injective M.mulVec ↔ M.det ≠ 0 := by
  rw [Matrix.mulVec_injective_iff_isUnit, Matrix.isUnit_iff_isUnit_det, isUnit_iff_ne_zero]

/-- A zero mode exists iff the mass map is not injective. -/
theorem hasZeroMode_iff_not_injective {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) :
    hasZeroMode M ↔ ¬ Function.Injective M.mulVec := by
  constructor
  · rintro ⟨v, hv, hMv⟩ hinj
    exact hv (hinj (by simpa using hMv))
  · intro hninj
    rw [Function.Injective] at hninj
    push_neg at hninj
    rcases hninj with ⟨a, b, hf, hab⟩
    refine ⟨a - b, ?_, ?_⟩
    · intro h; exact hab (sub_eq_zero.mp h)
    · ext i
      calc
        (M.mulVec (a - b)) i = (M.mulVec a) i - (M.mulVec b) i := by
          simp [Matrix.mulVec, sub_eq_add_neg]
        _ = 0 := by rw [hf]; simp

/-- The Majorana zero-mode criterion: a zero mode exists iff `det M = 0`. -/
theorem hasZeroMode_iff_det_eq_zero {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) :
    hasZeroMode M ↔ M.det = 0 := by
  rw [hasZeroMode_iff_not_injective, gapped_iff_det_ne_zero]
  constructor
  · intro h; exact of_not_not h
  · intro h; exact not_not.mpr h

end QM
