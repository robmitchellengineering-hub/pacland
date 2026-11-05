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

end Gleason

end
