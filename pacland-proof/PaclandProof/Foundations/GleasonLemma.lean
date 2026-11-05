import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Gleason step 2 — the dim-≥-3 geometry (cross product)

Gleason's lemma needs, for two unit vectors `u ⊥ v`, a **third** unit vector
orthogonal to both — possible only in dimension ≥ 3 (and impossible in dimension
2, which is exactly where Gleason fails). In `ℝ³` that vector is the cross
product `u × v`. This file kernel-checks its two load-bearing facts:
`u × v` is orthogonal to `u` and `v`, and is a unit vector when `u, v` are
orthonormal. They are the foundation for the 2D additivity rung.
-/

noncomputable section

open Matrix BigOperators

namespace GleasonLemma

/-- A unit vector in `ℝ³`. -/
def unitVec3 (v : Fin 3 → ℝ) : Prop :=
  dotProduct v v = 1

/-- Orthogonality in `ℝ³`. -/
def orthVec3 (u v : Fin 3 → ℝ) : Prop :=
  dotProduct u v = 0

/-- The cross product `u × v`. -/
def cross (u v : Fin 3 → ℝ) : Fin 3 → ℝ :=
  ![u 1 * v 2 - u 2 * v 1, u 2 * v 0 - u 0 * v 2, u 0 * v 1 - u 1 * v 0]

/-- The cross product is orthogonal to its first argument. -/
theorem cross_orth_left (u v : Fin 3 → ℝ) : orthVec3 u (cross u v) := by
  simp [orthVec3, cross, dotProduct, Fin.sum_univ_three]
  ring

/-- The cross product is orthogonal to its second argument. -/
theorem cross_orth_right (u v : Fin 3 → ℝ) : orthVec3 v (cross u v) := by
  simp [orthVec3, cross, dotProduct, Fin.sum_univ_three]
  ring

/-- Lagrange's identity `|u × v|² = |u|²|v|² − (u·v)²`, so the cross product of
orthonormal vectors is a unit vector. -/
theorem cross_unit (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v)
    (horth : orthVec3 u v) : unitVec3 (cross u v) := by
  simp [unitVec3, cross, dotProduct, Fin.sum_univ_three]
  have hu' : u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2 = 1 := by
    simpa [unitVec3, dotProduct, Fin.sum_univ_three, sq] using hu
  have hv' : v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2 = 1 := by
    simpa [unitVec3, dotProduct, Fin.sum_univ_three, sq] using hv
  have horth' : u 0 * v 0 + u 1 * v 1 + u 2 * v 2 = 0 := by
    simpa [orthVec3, dotProduct, Fin.sum_univ_three] using horth
  nlinarith [hu', hv', horth']

end GleasonLemma

end
