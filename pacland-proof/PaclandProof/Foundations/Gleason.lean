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

end Gleason

end
