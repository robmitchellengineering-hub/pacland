import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Gleason's theorem — step 1: the quadratic-form reconstruction

Gleason's theorem (finite-dimensional) says a frame function on dimension ≥ 3
is the Born rule. Its proof has a hard analytic step (continuity) and an
algebraic step: once the frame function is extended to a homogeneous degree-2
function `F` satisfying the parallelogram law, `F` **is** a quadratic form.

This file kernel-checks the algebraic core, rung by rung. Rung 1 (here): the
polarization `B(v,w) = (F(v+w) − F(v−w))/4` recovers `F` on the diagonal —
`B(v,v) = F(v)` — under homogeneity alone. Rung 2 (next) shows `B` is bilinear
from the parallelogram law, so `F(v) = vᵀ M v` for a symmetric `M`.
-/

noncomputable section

open BigOperators

namespace Gleason

/-- The polarization of `F`: `B(v,w) = (F(v+w) − F(v−w))/4`. -/
def polarization (F : (Fin 2 → ℝ) → ℝ) (v w : Fin 2 → ℝ) : ℝ :=
  (F (v + w) - F (v - w)) / 4

/-- Homogeneity degree 2 forces `F 0 = 0` (take `c = 0`). -/
theorem F_zero (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v) :
    F 0 = 0 := by
  have h := hhom 0 0
  norm_num at h
  exact h

/-- The polarization recovers `F` on the diagonal: `B(v,v) = F(v)`. -/
theorem polarization_recovers (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (v : Fin 2 → ℝ) :
    polarization F v v = F v := by
  unfold polarization
  have hsum : v + v = (2 : ℝ) • v := by
    ext i
    simp
    ring
  have hdiff : v - v = 0 := by
    ext i
    simp
  rw [hsum, hdiff]
  have h2 : F ((2 : ℝ) • v) = 4 * F v := by
    have h := hhom 2 v
    norm_num at h
    exact h
  have h0 : F 0 = 0 := F_zero F hhom
  rw [h2, h0]
  ring

/-- Homogeneity degree 2 forces evenness: `F(-v) = F(v)` (take `c = -1`). -/
theorem F_even (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (v : Fin 2 → ℝ) : F (-v) = F v := by
  have h := hhom (-1) v
  have hsmul : (-1 : ℝ) • v = -v := by
    ext i
    simp
  rw [hsmul] at h
  norm_num at h
  exact h

/-- The polarization is symmetric: `B(v,w) = B(w,v)`. -/
theorem polarization_symm (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (v w : Fin 2 → ℝ) : polarization F v w = polarization F w v := by
  unfold polarization
  have h1 : F (v + w) = F (w + v) := by rw [add_comm]
  have h2 : F (v - w) = F (w - v) := by
    have hnegg : v - w = -(w - v) := by
      ext i
      simp
    rw [hnegg]
    exact F_even F hhom (w - v)
  rw [h1, h2]

/-- The polarization vanishes on the zero vector: `B(0,w) = 0`. -/
theorem polarization_zero (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (w : Fin 2 → ℝ) : polarization F 0 w = 0 := by
  unfold polarization
  have h1 : F (0 + w) = F w := by rw [zero_add]
  have h2 : F (0 - w) = F w := by
    rw [zero_sub]
    exact F_even F hhom w
  rw [h1, h2]
  ring

/-- The parallelogram law descends to the polarization:
`B(x+y, z) + B(x−y, z) = 2·B(x, z)`. Proved by applying the parallelogram law
twice (with `x+z` and `x−z`) and telescoping. -/
theorem polarization_parallelogram (F : (Fin 2 → ℝ) → ℝ)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x y z : Fin 2 → ℝ) :
    polarization F (x + y) z + polarization F (x - y) z = 2 * polarization F x z := by
  unfold polarization
  have h1 : F (x + y + z) + F (x - y + z) = 2 * F (x + z) + 2 * F y := by
    have h := hpar (x + z) y
    have hA : x + z + y = x + y + z := by abel
    have hB : x + z - y = x - y + z := by abel
    rwa [hA, hB] at h
  have h2 : F (x + y - z) + F (x - y - z) = 2 * F (x - z) + 2 * F y := by
    have h := hpar (x - z) y
    have hA : x - z + y = x + y - z := by abel
    have hB : x - z - y = x - y - z := by abel
    rwa [hA, hB] at h
  nlinarith [h1, h2]

/-- The polarization doubles: `B(2x, z) = 2·B(x, z)`. -/
theorem polarization_double (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x z : Fin 2 → ℝ) :
    polarization F ((2 : ℝ) • x) z = 2 * polarization F x z := by
  have h := polarization_parallelogram F hpar x x z
  have hsum : x + x = (2 : ℝ) • x := by
    ext i
    simp
    ring
  have hdiff : x - x = 0 := by
    ext i
    simp
  have hz : polarization F 0 z = 0 := polarization_zero F hhom z
  rw [hsum, hdiff, hz] at h
  simpa using h

/-- The polarization is additive in its first argument:
`B(x+y, z) = B(x, z) + B(y, z)`. -/
theorem polarization_add (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x y z : Fin 2 → ℝ) :
    polarization F (x + y) z = polarization F x z + polarization F y z := by
  have h := polarization_parallelogram F hpar (x + y) (x - y) z
  have hA : (x + y) + (x - y) = (2 : ℝ) • x := by
    ext i
    simp
    ring
  have hB : (x + y) - (x - y) = (2 : ℝ) • y := by
    ext i
    simp
    ring
  rw [hA, hB] at h
  have hdx : polarization F ((2 : ℝ) • x) z = 2 * polarization F x z :=
    polarization_double F hhom hpar x z
  have hdy : polarization F ((2 : ℝ) • y) z = 2 * polarization F y z :=
    polarization_double F hhom hpar y z
  rw [hdx, hdy] at h
  nlinarith

/-- The diagonal is ℝ-homogeneous: `B(c·v, v) = c·B(v, v)`. This is the clean half
of the Jordan–von Neumann ℝ-linearity step, and follows from `F`'s homogeneity
alone (via `F((c±1)·v) = (c±1)² F v`). -/
theorem polarization_diag_hom (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (c : ℝ) (v : Fin 2 → ℝ) :
    polarization F (c • v) v = c * polarization F v v := by
  have hp : polarization F v v = F v := polarization_recovers F hhom v
  rw [hp]
  unfold polarization
  have hplus : c • v + v = (c + 1) • v := by
    ext i
    simp
    ring
  have hminus : c • v - v = (c - 1) • v := by
    ext i
    simp
    ring
  rw [hplus, hminus]
  have h1 : F ((c + 1) • v) = (c + 1) ^ 2 * F v := hhom (c + 1) v
  have h2 : F ((c - 1) • v) = (c - 1) ^ 2 * F v := hhom (c - 1) v
  rw [h1, h2]
  ring

/-- The polarization is `ℕ`-homogeneous in its first argument:
`B(n·v, w) = n·B(v, w)`. This is the seed of `ℚ`-linearity (then `ℝ`-linearity by
a regularity bound — the Jordan–von Neumann step). -/
theorem polarization_nsmul (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (n : ℕ) (v w : Fin 2 → ℝ) :
    polarization F (n • v) w = (n : ℝ) * polarization F v w := by
  induction n with
  | zero =>
      have hz : (0 : ℕ) • v = 0 := by rfl
      rw [hz]
      have h0 : polarization F 0 w = 0 := polarization_zero F hhom w
      rw [h0]
      norm_num
  | succ n ih =>
      have hsucc : (n + 1) • v = n • v + v := rfl
      rw [hsucc]
      rw [polarization_add F hhom hpar (n • v) v w]
      rw [ih]
      norm_num [Nat.cast_add, Nat.cast_one]
      ring

/-- The standard basis vectors. -/
def e0 : Fin 2 → ℝ := ![1, 0]
def e1 : Fin 2 → ℝ := ![0, 1]

/-- Any vector is its coordinate expansion: `v = v₀·e₀ + v₁·e₁`. -/
theorem basis_expand (v : Fin 2 → ℝ) : v = v 0 • e0 + v 1 • e1 := by
  ext i
  fin_cases i <;> simp [e0, e1]

/-- The polarization is homogeneous in its second argument (from `hlin` + symmetry). -/
theorem polarization_smul_right (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hlin : ∀ (c : ℝ) (v w : Fin 2 → ℝ), polarization F (c • v) w = c * polarization F v w)
    (c : ℝ) (v w : Fin 2 → ℝ) :
    polarization F v (c • w) = c * polarization F v w := by
  rw [polarization_symm F hhom v (c • w)]
  rw [hlin c w v]
  rw [polarization_symm F hhom w v]

/-- The bilinear expansion of the diagonal: `B(x+y, x+y) = B(x,x) + 2·B(x,y) + B(y,y)`. -/
theorem polarization_expand_diag (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (x y : Fin 2 → ℝ) :
    polarization F (x + y) (x + y) = polarization F x x + 2 * polarization F x y + polarization F y y := by
  rw [polarization_add F hhom hpar x y (x + y)]
  have hx : polarization F x (x + y) = polarization F x x + polarization F x y := by
    rw [polarization_symm F hhom x (x + y)]
    rw [polarization_add F hhom hpar x y x]
    rw [polarization_symm F hhom y x]
  have hy : polarization F y (x + y) = polarization F x y + polarization F y y := by
    rw [polarization_symm F hhom y (x + y)]
    rw [polarization_add F hhom hpar x y y]
  rw [hx, hy]
  ring

/-- **Step 1, conditionally complete.** Given the ℝ-linearity of `B` (the one
remaining Jordan–von Neumann assumption, named here as `hlin`), `F` is the
quadratic form `v ↦ v₀²F(e₀) + 2v₀v₁·B(e₀,e₁) + v₁²F(e₁)`. -/
theorem quadratic_form (F : (Fin 2 → ℝ) → ℝ)
    (hhom : ∀ (c : ℝ) (v : Fin 2 → ℝ), F (c • v) = c ^ 2 * F v)
    (hpar : ∀ v w, F (v + w) + F (v - w) = 2 * F v + 2 * F w)
    (hlin : ∀ (c : ℝ) (v w : Fin 2 → ℝ), polarization F (c • v) w = c * polarization F v w)
    (v : Fin 2 → ℝ) :
    F v = (v 0) ^ 2 * F e0 + 2 * v 0 * v 1 * polarization F e0 e1 + (v 1) ^ 2 * F e1 := by
  rw [← polarization_recovers F hhom v]
  conv_lhs => rw [basis_expand v]
  rw [polarization_expand_diag F hhom hpar (v 0 • e0) (v 1 • e1)]
  rw [hlin (v 0) e0 (v 0 • e0), hlin (v 0) e0 (v 1 • e1), hlin (v 1) e1 (v 1 • e1)]
  rw [polarization_smul_right F hhom hlin (v 0) e0 e0, polarization_smul_right F hhom hlin (v 1) e0 e1, polarization_smul_right F hhom hlin (v 1) e1 e1]
  rw [polarization_recovers F hhom e0, polarization_recovers F hhom e1]
  simp [pow_two]
  ring

end Gleason

end
