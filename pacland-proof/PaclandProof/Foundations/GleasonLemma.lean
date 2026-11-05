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

/-- A frame function in `ℝ³`: weights sum to `1` over every orthonormal triple. -/
def FrameFunction3 (f : (Fin 3 → ℝ) → ℝ) : Prop :=
  ∀ e1 e2 e3, unitVec3 e1 → unitVec3 e2 → unitVec3 e3 →
    orthVec3 e1 e2 → orthVec3 e1 e3 → orthVec3 e2 e3 →
    f e1 + f e2 + f e3 = 1

/-- Bilinear expansion of `(αu + βv) · (αu + βv)`. -/
theorem dotProduct_expand (u v : Fin 3 → ℝ) (α β : ℝ) :
    dotProduct (α • u + β • v) (α • u + β • v)
    = α ^ 2 * dotProduct u u + 2 * α * β * dotProduct u v + β ^ 2 * dotProduct v v := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- Bilinear expansion of `(αu + βv) · (−βu + αv)`. -/
theorem dotProduct_expand_mixed (u v : Fin 3 → ℝ) (α β : ℝ) :
    dotProduct (α • u + β • v) ((-β) • u + α • v)
    = -α * β * dotProduct u u + (α ^ 2 - β ^ 2) * dotProduct u v + α * β * dotProduct v v := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- Linearity of `(αu + βv) · z` in `(α, β)`. -/
theorem dotProduct_add_smul (u v z : Fin 3 → ℝ) (α β : ℝ) :
    dotProduct (α • u + β • v) z = α * dotProduct u z + β * dotProduct v z := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- The dot product is symmetric. -/
theorem dotProduct_symm (u v : Fin 3 → ℝ) : dotProduct u v = dotProduct v u := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- **The 2D additivity** (the algebraic heart of Gleason's lemma). For unit
`u ⊥ v` and `w = αu + βv` (with `α² + β² = 1`), the frames `{w, w', u×v}` and
`{u, v, u×v}` force `f w + f w' = f u + f v`, where `w' = −βu + αv`. -/
theorem two_dim_additivity (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v) (horth : orthVec3 u v)
    (α β : ℝ) (hαβ : α ^ 2 + β ^ 2 = 1) :
    f (α • u + β • v) + f ((-β) • u + α • v) = f u + f v := by
  let w : Fin 3 → ℝ := α • u + β • v
  let w' : Fin 3 → ℝ := (-β) • u + α • v
  let z : Fin 3 → ℝ := cross u v
  have hw_unit : unitVec3 w := by
    change dotProduct (α • u + β • v) (α • u + β • v) = 1
    rw [dotProduct_expand u v α β]
    rw [hu, hv, horth]
    nlinarith [hαβ]
  have hw'_unit : unitVec3 w' := by
    change dotProduct ((-β) • u + α • v) ((-β) • u + α • v) = 1
    rw [dotProduct_expand u v (-β) α]
    rw [hu, hv, horth]
    nlinarith [hαβ]
  have hw_orth : orthVec3 w w' := by
    change dotProduct (α • u + β • v) ((-β) • u + α • v) = 0
    rw [dotProduct_expand_mixed u v α β]
    rw [hu, hv, horth]
    ring
  have hz_unit : unitVec3 z := cross_unit u v hu hv horth
  have huz : dotProduct u z = 0 := by simpa [orthVec3] using cross_orth_left u v
  have hvz : dotProduct v z = 0 := by simpa [orthVec3] using cross_orth_right u v
  have hz_orth_w : orthVec3 w z := by
    change dotProduct (α • u + β • v) z = 0
    rw [dotProduct_add_smul u v z α β]
    rw [huz, hvz]
    ring
  have hz_orth_w' : orthVec3 w' z := by
    change dotProduct ((-β) • u + α • v) z = 0
    rw [dotProduct_add_smul u v z (-β) α]
    rw [huz, hvz]
    ring
  have hframe1 : f w + f w' + f z = 1 := hf w w' z hw_unit hw'_unit hz_unit hw_orth hz_orth_w hz_orth_w'
  have hframe2 : f u + f v + f z = 1 :=
    hf u v z hu hv hz_unit horth (cross_orth_left u v) (cross_orth_right u v)
  linarith

/-- **The 45° additivity** — the concrete form the continuity estimate feeds on:
for unit `u ⊥ v`, `f((u+v)/√2) + f((u-v)/√2) = f u + f v`, written here in the
equivalent smul form `(1/√2)•u + (1/√2)•v = (u+v)/√2`. -/
theorem forty_five_additivity (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v) (horth : orthVec3 u v) :
    f ((1 / √2) • u + (1 / √2) • v) + f ((1 / √2) • u + (-1 / √2) • v) = f u + f v := by
  have hαβ : (1 / √2) ^ 2 + (-1 / √2) ^ 2 = 1 := by
    rw [div_pow, div_pow]
    rw [show (√2 : ℝ) ^ 2 = 2 by exact Real.sq_sqrt (by norm_num)]
    norm_num
  have h := two_dim_additivity f hf u v hu hv horth (1 / √2) (-1 / √2) hαβ
  have hneg : -(-1 / √2 : ℝ) = 1 / √2 := by ring_nf
  rw [hneg] at h
  rw [add_comm] at h
  exact h

end GleasonLemma

end
