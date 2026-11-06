import Mathlib
import PaclandProof.Foundations.Cauchy

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

/-- **Parseval** (Binet–Cauchy): for orthonormal `u ⊥ v`, the triple `{u, v, u×v}` is
orthonormal, so `(u·p)² + (v·p)² + ((u×v)·p)² = p·p`. -/
theorem parseval (u v p : Fin 3 → ℝ)
    (hu : unitVec3 u) (hv : unitVec3 v) (horth : orthVec3 u v) :
    (dotProduct u p) ^ 2 + (dotProduct v p) ^ 2 + (dotProduct (cross u v) p) ^ 2 = dotProduct p p := by
  have hu' : u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2 = 1 := by
    simpa [unitVec3, dotProduct, Fin.sum_univ_three, sq] using hu
  have hv' : v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2 = 1 := by
    simpa [unitVec3, dotProduct, Fin.sum_univ_three, sq] using hv
  have horth' : u 0 * v 0 + u 1 * v 1 + u 2 * v 2 = 0 := by
    simpa [orthVec3, dotProduct, Fin.sum_univ_three] using horth
  -- diagonal "row" facts (Lagrange identity)
  have hr0 : u 0 ^ 2 + v 0 ^ 2 + (u 1 * v 2 - u 2 * v 1) ^ 2 = 1 := by
    have hu0 : u 1 ^ 2 + u 2 ^ 2 = 1 - u 0 ^ 2 := by linarith [hu']
    have hv0 : v 1 ^ 2 + v 2 ^ 2 = 1 - v 0 ^ 2 := by linarith [hv']
    have horth0 : u 1 * v 1 + u 2 * v 2 = -(u 0 * v 0) := by linarith [horth']
    calc
      u 0 ^ 2 + v 0 ^ 2 + (u 1 * v 2 - u 2 * v 1) ^ 2
          = u 0 ^ 2 + v 0 ^ 2 + (u 1 ^ 2 + u 2 ^ 2) * (v 1 ^ 2 + v 2 ^ 2) - (u 1 * v 1 + u 2 * v 2) ^ 2 := by ring
      _ = u 0 ^ 2 + v 0 ^ 2 + (1 - u 0 ^ 2) * (1 - v 0 ^ 2) - (u 0 * v 0) ^ 2 := by
          rw [hu0, hv0, horth0]
          ring
      _ = 1 := by ring
  have hr1 : u 1 ^ 2 + v 1 ^ 2 + (u 2 * v 0 - u 0 * v 2) ^ 2 = 1 := by
    have hu1 : u 2 ^ 2 + u 0 ^ 2 = 1 - u 1 ^ 2 := by linarith [hu']
    have hv1 : v 2 ^ 2 + v 0 ^ 2 = 1 - v 1 ^ 2 := by linarith [hv']
    have horth1 : u 2 * v 2 + u 0 * v 0 = -(u 1 * v 1) := by linarith [horth']
    calc
      u 1 ^ 2 + v 1 ^ 2 + (u 2 * v 0 - u 0 * v 2) ^ 2
          = u 1 ^ 2 + v 1 ^ 2 + (u 2 ^ 2 + u 0 ^ 2) * (v 2 ^ 2 + v 0 ^ 2) - (u 2 * v 2 + u 0 * v 0) ^ 2 := by ring
      _ = u 1 ^ 2 + v 1 ^ 2 + (1 - u 1 ^ 2) * (1 - v 1 ^ 2) - (u 1 * v 1) ^ 2 := by
          rw [hu1, hv1, horth1]
          ring
      _ = 1 := by ring
  have hr2 : u 2 ^ 2 + v 2 ^ 2 + (u 0 * v 1 - u 1 * v 0) ^ 2 = 1 := by
    have hu2 : u 0 ^ 2 + u 1 ^ 2 = 1 - u 2 ^ 2 := by linarith [hu']
    have hv2 : v 0 ^ 2 + v 1 ^ 2 = 1 - v 2 ^ 2 := by linarith [hv']
    have horth2 : u 0 * v 0 + u 1 * v 1 = -(u 2 * v 2) := by linarith [horth']
    calc
      u 2 ^ 2 + v 2 ^ 2 + (u 0 * v 1 - u 1 * v 0) ^ 2
          = u 2 ^ 2 + v 2 ^ 2 + (u 0 ^ 2 + u 1 ^ 2) * (v 0 ^ 2 + v 1 ^ 2) - (u 0 * v 0 + u 1 * v 1) ^ 2 := by ring
      _ = u 2 ^ 2 + v 2 ^ 2 + (1 - u 2 ^ 2) * (1 - v 2 ^ 2) - (u 2 * v 2) ^ 2 := by
          rw [hu2, hv2, horth2]
          ring
      _ = 1 := by ring
  -- off-diagonal "row" facts
  have hc01 : u 0 * u 1 + v 0 * v 1 + (u 1 * v 2 - u 2 * v 1) * (u 2 * v 0 - u 0 * v 2) = 0 := by
    have h1 : 1 - (v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2) = 0 := by linarith [hv']
    have h2 : 1 - (u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2) = 0 := by linarith [hu']
    have h : u 0 * u 1 + v 0 * v 1 + (u 1 * v 2 - u 2 * v 1) * (u 2 * v 0 - u 0 * v 2)
        = (u 0 * v 0 + u 1 * v 1 + u 2 * v 2) * (u 0 * v 1 + u 1 * v 0)
          + u 0 * u 1 * (1 - (v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2))
          + v 0 * v 1 * (1 - (u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2)) := by ring
    rw [h1, h2] at h
    have h' : u 0 * u 1 + v 0 * v 1 + (u 1 * v 2 - u 2 * v 1) * (u 2 * v 0 - u 0 * v 2)
        = (u 0 * v 0 + u 1 * v 1 + u 2 * v 2) * (u 0 * v 1 + u 1 * v 0) := by simpa using h
    rw [h', horth']
    ring
  have hc02 : u 0 * u 2 + v 0 * v 2 + (u 1 * v 2 - u 2 * v 1) * (u 0 * v 1 - u 1 * v 0) = 0 := by
    have h1 : 1 - (v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2) = 0 := by linarith [hv']
    have h2 : 1 - (u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2) = 0 := by linarith [hu']
    have h : u 0 * u 2 + v 0 * v 2 + (u 1 * v 2 - u 2 * v 1) * (u 0 * v 1 - u 1 * v 0)
        = (u 0 * v 0 + u 1 * v 1 + u 2 * v 2) * (u 0 * v 2 + u 2 * v 0)
          + u 0 * u 2 * (1 - (v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2))
          + v 0 * v 2 * (1 - (u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2)) := by ring
    rw [h1, h2] at h
    have h' : u 0 * u 2 + v 0 * v 2 + (u 1 * v 2 - u 2 * v 1) * (u 0 * v 1 - u 1 * v 0)
        = (u 0 * v 0 + u 1 * v 1 + u 2 * v 2) * (u 0 * v 2 + u 2 * v 0) := by simpa using h
    rw [h', horth']
    ring
  have hc12 : u 1 * u 2 + v 1 * v 2 + (u 2 * v 0 - u 0 * v 2) * (u 0 * v 1 - u 1 * v 0) = 0 := by
    have h1 : 1 - (v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2) = 0 := by linarith [hv']
    have h2 : 1 - (u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2) = 0 := by linarith [hu']
    have h : u 1 * u 2 + v 1 * v 2 + (u 2 * v 0 - u 0 * v 2) * (u 0 * v 1 - u 1 * v 0)
        = (u 0 * v 0 + u 1 * v 1 + u 2 * v 2) * (u 1 * v 2 + u 2 * v 1)
          + u 1 * u 2 * (1 - (v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2))
          + v 1 * v 2 * (1 - (u 0 ^ 2 + u 1 ^ 2 + u 2 ^ 2)) := by ring
    rw [h1, h2] at h
    have h' : u 1 * u 2 + v 1 * v 2 + (u 2 * v 0 - u 0 * v 2) * (u 0 * v 1 - u 1 * v 0)
        = (u 0 * v 0 + u 1 * v 1 + u 2 * v 2) * (u 1 * v 2 + u 2 * v 1) := by simpa using h
    rw [h', horth']
    ring
  have hr0' : u 0 ^ 2 + v 0 ^ 2 + (u 1 * v 2 - u 2 * v 1) ^ 2 - 1 = 0 := by linarith [hr0]
  have hr1' : u 1 ^ 2 + v 1 ^ 2 + (u 2 * v 0 - u 0 * v 2) ^ 2 - 1 = 0 := by linarith [hr1]
  have hr2' : u 2 ^ 2 + v 2 ^ 2 + (u 0 * v 1 - u 1 * v 0) ^ 2 - 1 = 0 := by linarith [hr2]
  have hfinal : (dotProduct u p) ^ 2 + (dotProduct v p) ^ 2 + (dotProduct (cross u v) p) ^ 2 - dotProduct p p
      = (u 0 ^ 2 + v 0 ^ 2 + (u 1 * v 2 - u 2 * v 1) ^ 2 - 1) * p 0 ^ 2
        + (u 1 ^ 2 + v 1 ^ 2 + (u 2 * v 0 - u 0 * v 2) ^ 2 - 1) * p 1 ^ 2
        + (u 2 ^ 2 + v 2 ^ 2 + (u 0 * v 1 - u 1 * v 0) ^ 2 - 1) * p 2 ^ 2
        + 2 * (u 0 * u 1 + v 0 * v 1 + (u 1 * v 2 - u 2 * v 1) * (u 2 * v 0 - u 0 * v 2)) * p 0 * p 1
        + 2 * (u 0 * u 2 + v 0 * v 2 + (u 1 * v 2 - u 2 * v 1) * (u 0 * v 1 - u 1 * v 0)) * p 0 * p 2
        + 2 * (u 1 * u 2 + v 1 * v 2 + (u 2 * v 0 - u 0 * v 2) * (u 0 * v 1 - u 1 * v 0)) * p 1 * p 2 := by
    simp [cross, dotProduct, Fin.sum_univ_three]
    ring
  rw [hr0', hr1', hr2', hc01, hc02, hc12] at hfinal
  linarith [hfinal]

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

/-- Linearity of `(u − v) · z`. -/
theorem dotProduct_sub_left (u v z : Fin 3 → ℝ) :
    dotProduct (u - v) z = dotProduct u z - dotProduct v z := by
  simp [dotProduct, Fin.sum_univ_three, sub_eq_add_neg, Pi.neg_apply]
  ring

/-- Linearity of `z · (αu + βv)` in the second argument. -/
theorem dotProduct_add_smul_right (z u v : Fin 3 → ℝ) (α β : ℝ) :
    dotProduct z (α • u + β • v) = α * dotProduct z u + β * dotProduct z v := by
  simp [dotProduct, Fin.sum_univ_three, Pi.smul_apply]
  ring

/-- Linearity of `z · (u − v)`. -/
theorem dotProduct_sub_right (z u v : Fin 3 → ℝ) :
    dotProduct z (u - v) = dotProduct z u - dotProduct z v := by
  simp [dotProduct, Fin.sum_univ_three, sub_eq_add_neg, Pi.neg_apply]
  ring

/-- The dot product is symmetric. -/
theorem dotProduct_symm (u v : Fin 3 → ℝ) : dotProduct u v = dotProduct v u := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- The "latitude `a`" unit vector `√a·p + √(1−a)·q` (for `p ⊥ q`): it is unit and
its squared projection onto `p` is exactly `a`. Building block for realizability. -/
theorem unit_smul_of_latitude (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q)
    (hpq : orthVec3 p q) (a : ℝ) (ha : 0 ≤ a) (ha1 : a ≤ 1) :
    unitVec3 (Real.sqrt a • p + Real.sqrt (1 - a) • q) ∧
    (dotProduct (Real.sqrt a • p + Real.sqrt (1 - a) • q) p) ^ 2 = a := by
  have hsqrt_a : (Real.sqrt a) ^ 2 = a := Real.sq_sqrt ha
  have hsqrt_1a : (Real.sqrt (1 - a)) ^ 2 = 1 - a := Real.sq_sqrt (by linarith)
  constructor
  · rw [unitVec3, dotProduct_expand p q (Real.sqrt a) (Real.sqrt (1 - a))]
    have hp' : dotProduct p p = 1 := by simpa [unitVec3] using hp
    have hq' : dotProduct q q = 1 := by simpa [unitVec3] using hq
    have hpq' : dotProduct p q = 0 := by simpa [orthVec3] using hpq
    rw [hp', hq', hpq', hsqrt_a, hsqrt_1a]
    ring
  · have hdot : dotProduct (Real.sqrt a • p + Real.sqrt (1 - a) • q) p = Real.sqrt a := by
      rw [dotProduct_add_smul p q p (Real.sqrt a) (Real.sqrt (1 - a))]
      have hp' : dotProduct p p = 1 := by simpa [unitVec3] using hp
      have hqp : dotProduct q p = 0 := by
        rw [dotProduct_symm]
        simpa [orthVec3] using hpq
      rw [hp', hqp]
      ring
    rw [hdot, hsqrt_a]

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

/-- **Evenness** — a frame function is even: `f(-x) = f x` for unit `x`, once we
have a perpendicular unit `v ⊥ x` (the `α = 0, β = 1` case of the 2D additivity).
This is what the homogeneous extension needs for `c < 0`. -/
theorem even_of_frame (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (x v : Fin 3 → ℝ) (hx : unitVec3 x) (hv : unitVec3 v) (horth : orthVec3 x v) :
    f (-x) = f x := by
  have h := two_dim_additivity f hf x v hx hv horth 0 1 (by norm_num)
  have h' : f v + f (-x) = f x + f v := by simpa using h
  linarith

/-- **A perpendicular unit vector always exists** — the dim-3 completion that
unblocks evenness, boundedness and the extension. For unit `x`, the quarter-turn
`![0, -x₂, x₁]` is `⊥ x` (nonzero unless `x = ±e₁`, handled separately). -/
theorem exists_perp (x : Fin 3 → ℝ) (hx : unitVec3 x) :
    ∃ y : Fin 3 → ℝ, unitVec3 y ∧ orthVec3 x y := by
  by_cases h : x 1 = 0 ∧ x 2 = 0
  · refine ⟨![0, 1, 0], ?_, ?_⟩
    · norm_num [unitVec3, dotProduct, Fin.sum_univ_three]
    · simp [orthVec3, dotProduct, Fin.sum_univ_three, h.1, h.2]
  · let y₀ : Fin 3 → ℝ := ![0, -x 2, x 1]
    have hy₀_orth : orthVec3 x y₀ := by
      simp [orthVec3, y₀, dotProduct, Fin.sum_univ_three]
      ring
    have hn_pos : 0 < dotProduct y₀ y₀ := by
      simp [y₀, dotProduct, Fin.sum_univ_three]
      by_cases hx1 : x 1 = 0
      · have hx2 : x 2 ≠ 0 := by
          intro h2; exact h ⟨hx1, h2⟩
        have h2sq : 0 < x 2 ^ 2 := sq_pos_of_ne_zero hx2
        nlinarith [h2sq, sq_nonneg (x 1)]
      · have h1sq : 0 < x 1 ^ 2 := sq_pos_of_ne_zero hx1
        nlinarith [h1sq, sq_nonneg (x 2)]
    let n : ℝ := Real.sqrt (dotProduct y₀ y₀)
    let y : Fin 3 → ℝ := (1 / n) • y₀
    refine ⟨y, ?_, ?_⟩
    · simp [unitVec3, y, y₀, dotProduct, Fin.sum_univ_three]
      have hn2 : n ^ 2 = dotProduct y₀ y₀ := Real.sq_sqrt (le_of_lt hn_pos)
      have hn_ne : n ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hn_pos)
      field_simp [hn_ne]
      ring_nf
      rw [hn2]
      simp [y₀, dotProduct, Fin.sum_univ_three]
      ring
    · simp [orthVec3, y, y₀, dotProduct, Fin.sum_univ_three]
      have hn_ne : n ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hn_pos)
      field_simp [hn_ne]
      ring

/-- **Boundedness** — a nonnegative frame function is `≤ 1` on every unit vector:
complete `x` to the frame `{x, y, x×y}` and use `f x + f y + f z = 1`. -/
theorem frameFunction3_bounded (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x)
    (x : Fin 3 → ℝ) (hx : unitVec3 x) :
    f x ≤ 1 := by
  rcases exists_perp x hx with ⟨y, hy, horth⟩
  let z : Fin 3 → ℝ := cross x y
  have hz : unitVec3 z := cross_unit x y hx hy horth
  have hframe : f x + f y + f z = 1 :=
    hf x y z hx hy hz horth (cross_orth_left x y) (cross_orth_right x y)
  have hnonneg_y : 0 ≤ f y := hpos y hy
  have hnonneg_z : 0 ≤ f z := hpos z hz
  linarith

/-- **Two-frame relation** — the functional equation behind Gleason's continuity.
For two orthonormal frames `{t,w,z}` and `{t',w',z'}` (the latitude-`a` setup: `t,t'`
at the same latitude with a 90° longitude shift, `w,w'` their polar partners, `z,z'`
the plane normals), the frame property forces
`f t − f t' = (f w' − f w) + (f z' − f z)`. -/
theorem two_frame_diff (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (t w z t' w' z' : Fin 3 → ℝ)
    (ht : unitVec3 t) (hw : unitVec3 w) (hz : unitVec3 z)
    (ht' : unitVec3 t') (hw' : unitVec3 w') (hz' : unitVec3 z')
    (h12 : orthVec3 t w) (h13 : orthVec3 t z) (h23 : orthVec3 w z)
    (h12' : orthVec3 t' w') (h13' : orthVec3 t' z') (h23' : orthVec3 w' z') :
    f t - f t' = (f w' - f w) + (f z' - f z) := by
  have h1 : f t + f w + f z = 1 := hf t w z ht hw hz h12 h13 h23
  have h2 : f t' + f w' + f z' = 1 := hf t' w' z' ht' hw' hz' h12' h13' h23'
  linarith

/-- **The cross-plane consistency** — for unit `x ⊥ y`, the 2D sum is
`f x + f y = 1 − f(x×y)`, i.e. depends only on the plane's normal `x×y`. This is
the fact (absent in the 2D-additivity-only picture) that forces continuity. -/
theorem two_dim_sum_eq_one_minus_z (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (x y : Fin 3 → ℝ) (hx : unitVec3 x) (hy : unitVec3 y) (hxy : orthVec3 x y) :
    f x + f y = 1 - f (cross x y) := by
  have hz : unitVec3 (cross x y) := cross_unit x y hx hy hxy
  have h := hf x y (cross x y) hx hy hz hxy (cross_orth_left x y) (cross_orth_right x y)
  linarith

/-- **The 90°-rotation about `p`.** `ρ x = (x·p)·p + p×x` fixes `p` and rotates the
plane `p⊥` by 90°. On the equator (`x ⊥ p`) it is just `p×x`. -/
def rot90p (p x : Fin 3 → ℝ) : Fin 3 → ℝ :=
  (dotProduct x p) • p + cross p x

/-- **Symmetrization is constant on the equator** (the first step of Gleason's
continuity). For `e ⊥ p`, the frame `{e, ρe, p}` is orthonormal (with `ρe = p×e`),
so `f e + f(ρe) + f p = 1`, i.e. the symmetrized value `f e + f(p×e)` is the
constant `1 − f p`. This is what the 2D step function lacks (no 3D equator circle). -/
theorem symmetrization_equator_constant (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (e : Fin 3 → ℝ) (he : unitVec3 e) (hep : orthVec3 e p) :
    f e + f (cross p e) = 1 - f p := by
  have hpe : orthVec3 p e := by simpa [orthVec3, dotProduct_symm] using hep
  have hz : unitVec3 (cross p e) := cross_unit p e hp he hpe
  have hez : orthVec3 e (cross p e) := cross_orth_right p e
  have hzp : orthVec3 (cross p e) p := by simpa [orthVec3, dotProduct_symm] using cross_orth_left p e
  have hframe : f e + f (cross p e) + f p = 1 := hf e (cross p e) p he hz hp hez hep hzp
  linarith

/-- **Binet–Cauchy**: `(a×b)·(c×d) = (a·c)(b·d) − (a·d)(b·c)`. -/
theorem cross_dot_cross (a b c d : Fin 3 → ℝ) :
    dotProduct (cross a b) (cross c d) = dotProduct a c * dotProduct b d - dotProduct a d * dotProduct b c := by
  simp [cross, dotProduct, Fin.sum_univ_three]
  ring

/-- **Cauchy–Schwarz**: `|x·y| ≤ ‖x‖·‖y‖`. -/
theorem dotProduct_abs_le_norm (x y : Fin 3 → ℝ) :
    |dotProduct x y| ≤ Real.sqrt (dotProduct x x) * Real.sqrt (dotProduct y y) := by
  have hxy : dotProduct (cross x y) (cross x y) = dotProduct x x * dotProduct y y - (dotProduct x y) ^ 2 := by
    rw [cross_dot_cross x y x y]
    simp [dotProduct_symm]
    ring
  have hnonneg : 0 ≤ dotProduct (cross x y) (cross x y) := by
    simp [dotProduct, Fin.sum_univ_three]
    nlinarith [sq_nonneg ((cross x y) 0), sq_nonneg ((cross x y) 1), sq_nonneg ((cross x y) 2)]
  have hsq_le : (dotProduct x y) ^ 2 ≤ dotProduct x x * dotProduct y y := by nlinarith [hxy, hnonneg]
  have hxx : 0 ≤ dotProduct x x := by
    simp [dotProduct, Fin.sum_univ_three]
    nlinarith [sq_nonneg (x 0), sq_nonneg (x 1), sq_nonneg (x 2)]
  have hyy : 0 ≤ dotProduct y y := by
    simp [dotProduct, Fin.sum_univ_three]
    nlinarith [sq_nonneg (y 0), sq_nonneg (y 1), sq_nonneg (y 2)]
  have hprod : (Real.sqrt (dotProduct x x) * Real.sqrt (dotProduct y y)) ^ 2 = dotProduct x x * dotProduct y y := by
    rw [mul_pow]
    rw [Real.sq_sqrt hxx, Real.sq_sqrt hyy]
  have hfinal : (dotProduct x y) ^ 2 ≤ (Real.sqrt (dotProduct x x) * Real.sqrt (dotProduct y y)) ^ 2 := by
    rw [hprod]
    exact hsq_le
  have hnonneg_prod : 0 ≤ Real.sqrt (dotProduct x x) * Real.sqrt (dotProduct y y) :=
    mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
  simpa [abs_of_nonneg hnonneg_prod] using (sq_le_sq.mp hfinal)

/-- **BAC–CAB**: `a × (b × c) = (a·c)·b − (a·b)·c`. -/
theorem cross_triple (a b c : Fin 3 → ℝ) :
    cross a (cross b c) = dotProduct a c • b - dotProduct a b • c := by
  ext i
  fin_cases i <;> simp [cross, dotProduct, Fin.sum_univ_three] <;> ring

/-- `a × a = 0`. -/
theorem cross_self (a : Fin 3 → ℝ) : cross a a = 0 := by
  ext i
  fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring

/-- **`ρ` preserves the projection onto `p`**: `(ρx)·p = x·p` (for unit `p`). -/
theorem rot90p_preserves_proj (p x : Fin 3 → ℝ) (hp : unitVec3 p) :
    dotProduct (rot90p p x) p = dotProduct x p := by
  dsimp [rot90p]
  have h1 : dotProduct ((dotProduct x p) • p + cross p x) p
      = (dotProduct x p) * dotProduct p p + dotProduct (cross p x) p := by
    simpa only [one_smul, one_mul] using (dotProduct_add_smul p (cross p x) p (dotProduct x p) 1)
  have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
  have hcp : dotProduct (cross p x) p = 0 := by rw [dotProduct_symm]; simpa [orthVec3] using cross_orth_left p x
  rw [h1, hpp, hcp]
  ring

/-- `ρ` rotates the plane `p⊥`: for `q ⊥ p` and `r = p×q`, `(ρt)·q = −t·r` and
`(ρt)·r = t·q` — the 90° rotation sends `(t·q, t·r) ↦ (−t·r, t·q)`. -/
theorem rot90p_rotates_plane (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (t : Fin 3 → ℝ) :
    dotProduct (rot90p p t) q = - dotProduct t (cross p q) ∧
    dotProduct (rot90p p t) (cross p q) = dotProduct t q := by
  constructor
  · dsimp [rot90p]
    have h1 : dotProduct ((dotProduct t p) • p + cross p t) q
        = (dotProduct t p) * dotProduct p q + dotProduct (cross p t) q := by
      simpa only [one_smul, one_mul] using (dotProduct_add_smul p (cross p t) q (dotProduct t p) 1)
    have hpq0 : dotProduct p q = 0 := by simpa [orthVec3] using hpq
    have hptq : dotProduct (cross p t) q = - dotProduct t (cross p q) := by
      simp [cross, dotProduct, Fin.sum_univ_three]
      ring
    rw [h1, hpq0, hptq]
    ring
  · dsimp [rot90p]
    have h1 : dotProduct ((dotProduct t p) • p + cross p t) (cross p q)
        = (dotProduct t p) * dotProduct p (cross p q) + dotProduct (cross p t) (cross p q) := by
      simpa only [one_smul, one_mul] using (dotProduct_add_smul p (cross p t) (cross p q) (dotProduct t p) 1)
    have hpr0 : dotProduct p (cross p q) = 0 := by simpa [orthVec3] using cross_orth_left p q
    have hptpq : dotProduct (cross p t) (cross p q) = dotProduct t q := by
      rw [cross_dot_cross p t p q]
      have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
      have hpq0 : dotProduct p q = 0 := by simpa [orthVec3] using hpq
      rw [hpp, hpq0]
      ring
    rw [h1, hpr0, hptpq]
    ring

/-- `ρ²` fixes `p` and negates the plane `p⊥`: `(ρ²t)·p = t·p`, `(ρ²t)·q = −t·q`,
`(ρ²t)·(p×q) = −t·(p×q)`. -/
theorem rot90p_sq_proj (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (t : Fin 3 → ℝ) :
    dotProduct (rot90p p (rot90p p t)) p = dotProduct t p ∧
    dotProduct (rot90p p (rot90p p t)) q = - dotProduct t q ∧
    dotProduct (rot90p p (rot90p p t)) (cross p q) = - dotProduct t (cross p q) := by
  constructor
  · rw [rot90p_preserves_proj p (rot90p p t) hp, rot90p_preserves_proj p t hp]
  constructor
  · have h1 := (rot90p_rotates_plane p q hp hq hpq (rot90p p t)).1
    have h2 := (rot90p_rotates_plane p q hp hq hpq t).2
    rw [h1, h2]
  · have h1 := (rot90p_rotates_plane p q hp hq hpq (rot90p p t)).2
    have h2 := (rot90p_rotates_plane p q hp hq hpq t).1
    rw [h1, h2]

/-- **The quadratic's symmetrization matches `g`'s latitude dependence.** For
`Q(x) = f p·(x·p)² + f q·(x·q)² + f r·(x·r)²` (`r = p×q`), Parseval and the frame sum give
`Q t + Q(ρt) = (3·f p − 1)·(t·p)² + (1 − f p)` — the exact relation the recover-`f` step
uses (RB Theorem 23) to force `f = Q`. -/
theorem quadratic_symm (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (t : Fin 3 → ℝ) (ht : unitVec3 t) :
    (f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2)
      + (f p * (dotProduct (rot90p p t) p) ^ 2 + f q * (dotProduct (rot90p p t) q) ^ 2 + f (cross p q) * (dotProduct (rot90p p t) (cross p q)) ^ 2)
      = (3 * f p - 1) * (dotProduct t p) ^ 2 + (1 - f p) := by
  have hsqsum : (dotProduct t q) ^ 2 + (dotProduct t (cross p q)) ^ 2 = 1 - (dotProduct t p) ^ 2 := by
    have hpv := parseval p q t hp hq hpq
    rw [dotProduct_symm p t, dotProduct_symm q t, dotProduct_symm (cross p q) t] at hpv
    have htt : dotProduct t t = 1 := by simpa [unitVec3] using ht
    rw [htt] at hpv
    linarith
  have hfsum : f q + f (cross p q) = 1 - f p := by
    have hfr : unitVec3 (cross p q) := cross_unit p q hp hq hpq
    have hframe : f p + f q + f (cross p q) = 1 := hf p q (cross p q) hp hq hfr hpq (cross_orth_left p q) (cross_orth_right p q)
    linarith
  have hproj : (dotProduct (rot90p p t) p) ^ 2 = (dotProduct t p) ^ 2 := by
    rw [rot90p_preserves_proj p t hp]
  have hρq : (dotProduct (rot90p p t) q) ^ 2 = (dotProduct t (cross p q)) ^ 2 := by
    have h := (rot90p_rotates_plane p q hp hq hpq t).1
    rw [h]
    ring
  have hρr : (dotProduct (rot90p p t) (cross p q)) ^ 2 = (dotProduct t q) ^ 2 := by
    have h := (rot90p_rotates_plane p q hp hq hpq t).2
    rw [h]
  calc
    (f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2)
      + (f p * (dotProduct (rot90p p t) p) ^ 2 + f q * (dotProduct (rot90p p t) q) ^ 2 + f (cross p q) * (dotProduct (rot90p p t) (cross p q)) ^ 2)
        = f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2
          + f p * (dotProduct t p) ^ 2 + f q * (dotProduct t (cross p q)) ^ 2 + f (cross p q) * (dotProduct t q) ^ 2 := by
            rw [hproj, hρq, hρr]
            ring
    _ = 2 * f p * (dotProduct t p) ^ 2 + (f q + f (cross p q)) * ((dotProduct t q) ^ 2 + (dotProduct t (cross p q)) ^ 2) := by ring
    _ = 2 * f p * (dotProduct t p) ^ 2 + (1 - f p) * (1 - (dotProduct t p) ^ 2) := by
            rw [hfsum, hsqsum]
    _ = (3 * f p - 1) * (dotProduct t p) ^ 2 + (1 - f p) := by ring

/-- `ρ` is linear: `ρ(x − y) = ρx − ρy`. -/
theorem rot90p_sub (p x y : Fin 3 → ℝ) :
    rot90p p (x - y) = rot90p p x - rot90p p y := by
  dsimp [rot90p]
  have hdot : dotProduct (x - y) p = dotProduct x p - dotProduct y p := by
    simp [dotProduct, Fin.sum_univ_three]
    ring
  have hcross : cross p (x - y) = cross p x - cross p y := by
    ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring
  rw [hdot, hcross]
  ext i
  fin_cases i <;> simp [Pi.smul_apply, sub_eq_add_neg] <;> ring

/-- **`ρ²` is the 180°-rotation about `p`**: `ρ(ρ x) = 2(x·p)·p − x`. -/
theorem rot90p_sq (p x : Fin 3 → ℝ) (hp : unitVec3 p) :
    rot90p p (rot90p p x) = 2 * dotProduct x p • p - x := by
  have hdot : dotProduct ((dotProduct x p) • p + cross p x) p = dotProduct x p := by
    exact rot90p_preserves_proj p x hp
  have hcross : cross p ((dotProduct x p) • p + cross p x) = dotProduct x p • p - x := by
    have hb : cross p ((dotProduct x p) • p + cross p x)
        = (dotProduct x p) • cross p p + cross p (cross p x) := by
      ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring
    have h0 : (dotProduct x p) • cross p p = 0 := by
      have hself : cross p p = 0 := by ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring
      rw [hself]
      simp
    rw [hb, h0, cross_triple p p x]
    have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
    have hxp : dotProduct p x = dotProduct x p := dotProduct_symm p x
    rw [hpp, hxp]
    simp [one_smul]
  calc
    rot90p p (rot90p p x)
        = dotProduct x p • p + cross p ((dotProduct x p) • p + cross p x) := by
            dsimp [rot90p]
            rw [hdot]
    _ = dotProduct x p • p + (dotProduct x p • p - x) := by rw [hcross]
    _ = 2 * dotProduct x p • p - x := by ring

/-- **`rot90p` is orthogonal** (for unit `p`): it preserves the dot product. -/
theorem rot90p_orthogonal (p x y : Fin 3 → ℝ) (hp : unitVec3 p) :
    dotProduct (rot90p p x) (rot90p p y) = dotProduct x y := by
  dsimp [rot90p]
  calc
    dotProduct ((dotProduct x p) • p + cross p x) ((dotProduct y p) • p + cross p y)
        = dotProduct p p * dotProduct x y + (dotProduct x p) * (dotProduct y p) * (dotProduct p p - 1) := by
            simp [dotProduct, cross, Fin.sum_univ_three]
            ring
    _ = dotProduct x y := by
            have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
            rw [hpp]
            ring

/-- `ρ` is an isometry: `‖ρx − ρy‖² = ‖x − y‖²` (for unit `p`). -/
theorem rot90p_isometry (p x y : Fin 3 → ℝ) (hp : unitVec3 p) :
    dotProduct (rot90p p x - rot90p p y) (rot90p p x - rot90p p y) = dotProduct (x - y) (x - y) := by
  rw [← rot90p_sub p x y]
  exact rot90p_orthogonal p (x - y) (x - y) hp

/-- `ρ` preserves unit vectors: `ρx` is unit when `x` is. -/
theorem rot90p_unit (p x : Fin 3 → ℝ) (hp : unitVec3 p) (hx : unitVec3 x) :
    unitVec3 (rot90p p x) := by
  simpa [unitVec3, rot90p_orthogonal p x x hp] using hx

/-- **The φ-map** (Richman–Bridges' oscillation transfer): `u` rotated 90° in the plane
`span(v,u)` in the `v → u` direction — a rational function of dot products:
`λ(u) = ((u·v)·u − v)/√(1 − (u·v)²)`. -/
def phi_map (u v : Fin 3 → ℝ) : Fin 3 → ℝ :=
  (1 / Real.sqrt (1 - (dotProduct u v) ^ 2)) • ((dotProduct u v) • u - v)

/-- **`λ(e) = p`** when `v = a·e + b·p` lies "south" of the equator point `e` (`b < 0`,
`v` unit, `e ⊥ p`). -/
theorem phi_map_eq_pole (e p v : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (a b : ℝ) (hv : v = a • e + b • p) (hb : b < 0) (hunit : unitVec3 v) :
    phi_map e v = p := by
  dsimp [phi_map]
  have hev : dotProduct e v = a := by
    rw [hv]
    rw [dotProduct_symm e (a • e + b • p)]
    rw [dotProduct_add_smul e p e a b]
    have hee : dotProduct e e = 1 := by simpa [unitVec3] using he
    have hep0 : dotProduct p e = 0 := by simpa [orthVec3, dotProduct_symm] using hep
    rw [hee, hep0]
    ring
  have hdiff : (dotProduct e v) • e - v = (-b) • p := by
    rw [hev, hv]
    ext i; fin_cases i <;> simp [Pi.smul_apply, sub_eq_add_neg] <;> ring
  have hab : a ^ 2 + b ^ 2 = 1 := by
    have hvu : dotProduct v v = 1 := by simpa [unitVec3] using hunit
    rw [hv] at hvu
    rw [dotProduct_expand e p a b] at hvu
    rw [he, hp, hep] at hvu
    nlinarith
  have hsq : 1 - (dotProduct e v) ^ 2 = b ^ 2 := by
    rw [hev]
    nlinarith [hab]
  have hsqrt : Real.sqrt (1 - (dotProduct e v) ^ 2) = -b := by
    rw [hsq]
    have hbabs : |b| = -b := abs_of_neg hb
    rw [← hbabs]
    exact Real.sqrt_sq_eq_abs b
  rw [hsqrt, hdiff]
  have hb_ne : -b ≠ 0 := by linarith [hb]
  rw [smul_smul]
  have hmul : (1 / (-b)) * (-b) = 1 := by
    rw [one_div]
    exact inv_mul_cancel₀ hb_ne
  rw [hmul]
  rw [one_smul]

/-- **`λ(u)` is a unit vector** (for unit `u,v` with `u ≠ ±v`). -/
theorem phi_map_unit (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v)
    (hne : dotProduct u v ^ 2 ≠ 1) :
    unitVec3 (phi_map u v) := by
  have hcs : (dotProduct u v) ^ 2 ≤ 1 := by
    have h := cross_dot_cross u v u v
    rw [dotProduct_symm v u] at h
    have huu : dotProduct u u = 1 := by simpa [unitVec3] using hu
    have hvv : dotProduct v v = 1 := by simpa [unitVec3] using hv
    have hnonneg : 0 ≤ dotProduct (cross u v) (cross u v) := by
      simp [dotProduct, Fin.sum_univ_three]
      nlinarith [sq_nonneg ((cross u v) 0), sq_nonneg ((cross u v) 1), sq_nonneg ((cross u v) 2)]
    nlinarith [h, huu, hvv, hnonneg]
  have ha_le : 0 ≤ 1 - (dotProduct u v) ^ 2 := by linarith
  have hw : dotProduct ((dotProduct u v) • u - v) ((dotProduct u v) • u - v) = 1 - (dotProduct u v) ^ 2 := by
    calc
      dotProduct ((dotProduct u v) • u - v) ((dotProduct u v) • u - v)
          = (dotProduct u v) ^ 2 * dotProduct u u - 2 * dotProduct u v * dotProduct u v + dotProduct v v := by
            simp [dotProduct, Fin.sum_univ_three, sub_eq_add_neg, Pi.smul_apply, Pi.neg_apply]
            ring
      _ = 1 - (dotProduct u v) ^ 2 := by
            rw [hu, hv]
            ring
  have hcsq : (1 / Real.sqrt (1 - (dotProduct u v) ^ 2)) ^ 2 = 1 / (1 - (dotProduct u v) ^ 2) := by
    have hsqrt_sq : (Real.sqrt (1 - (dotProduct u v) ^ 2)) ^ 2 = 1 - (dotProduct u v) ^ 2 := Real.sq_sqrt ha_le
    rw [← hsqrt_sq]
    simp
  calc
    dotProduct (phi_map u v) (phi_map u v)
        = (1 / Real.sqrt (1 - (dotProduct u v) ^ 2)) ^ 2 * dotProduct ((dotProduct u v) • u - v) ((dotProduct u v) • u - v) := by
            dsimp [phi_map]
            simp [dotProduct, Fin.sum_univ_three, Pi.smul_apply]
            ring_nf
    _ = (1 / (1 - (dotProduct u v) ^ 2)) * (1 - (dotProduct u v) ^ 2) := by
            rw [hcsq, hw]
    _ = 1 := by
            have hne' : 1 - (dotProduct u v) ^ 2 ≠ 0 := by
              intro h
              have : (dotProduct u v) ^ 2 = 1 := by linarith
              exact hne this
            field_simp [hne']

/-- **L5 scalar setup.** For `0 < r < 1`, with `γ := √(1−r²/16)`, `a := 1−r²/8`,
`s₀ := (r/2)γ`: `1/2 < γ < 1`, `7/8 < a < 1`, `r/4 < s₀ < r/2`, and `a² + s₀² = 1`. -/
theorem l5_scalars (r : ℝ) (hr : 0 < r) (hr1 : r < 1) :
    let γ := Real.sqrt (1 - r ^ 2 / 16)
    let a := 1 - r ^ 2 / 8
    let s₀ := (r / 2) * γ
    (1 / 2 < γ ∧ γ < 1) ∧ (7 / 8 < a ∧ a < 1) ∧ (r / 4 < s₀ ∧ s₀ < r / 2) ∧ (a ^ 2 + s₀ ^ 2 = 1) := by
  intro γ a s₀
  have hr2 : r ^ 2 < 1 := by nlinarith [hr, hr1]
  have hγsq : γ ^ 2 = 1 - r ^ 2 / 16 := by
    dsimp [γ]
    exact Real.sq_sqrt (by nlinarith [sq_nonneg r] : 0 ≤ 1 - r ^ 2 / 16)
  have hγ_nonneg : 0 ≤ γ := by dsimp [γ]; exact Real.sqrt_nonneg _
  have hγ_gt : 1 / 2 < γ := by
    have hγsq_gt : γ ^ 2 > (1 / 2 : ℝ) ^ 2 := by
      rw [hγsq]
      nlinarith [hr2]
    nlinarith [hγsq_gt, hγ_nonneg, sq_nonneg (1 / 2 : ℝ)]
  have hγ_lt : γ < 1 := by
    have hγsq_lt : γ ^ 2 < 1 := by rw [hγsq]; nlinarith [sq_nonneg r]
    nlinarith [hγsq_lt, hγ_nonneg]
  have ha_gt : 7 / 8 < a := by
    dsimp [a]
    nlinarith [hr2]
  have ha_lt : a < 1 := by
    dsimp [a]
    nlinarith [sq_nonneg r]
  have hs₀_gt : r / 4 < s₀ := by
    dsimp [s₀]
    nlinarith [hγ_gt, hr]
  have hs₀_lt : s₀ < r / 2 := by
    dsimp [s₀]
    nlinarith [hγ_lt, hr]
  have hs₀sq : s₀ ^ 2 = r ^ 2 / 4 * γ ^ 2 := by
    dsimp [s₀]
    ring
  have hsum : a ^ 2 + s₀ ^ 2 = 1 := by
    dsimp [a]
    rw [hs₀sq, hγsq]
    ring
  exact ⟨⟨hγ_gt, hγ_lt⟩, ⟨ha_gt, ha_lt⟩, ⟨hs₀_gt, hs₀_lt⟩, hsum⟩

/-- **L5 F0**: for unit `u,e`, `(u−e)·e = −‖u−e‖²/2`. -/
theorem l5_f0 (u e : Fin 3 → ℝ) (hu : unitVec3 u) (he : unitVec3 e) :
    dotProduct (u - e) e = - dotProduct (u - e) (u - e) / 2 := by
  have hwe : dotProduct (u - e) e = dotProduct u e - 1 := by
    rw [dotProduct_sub_left u e e]
    have hee : dotProduct e e = 1 := by simpa [unitVec3] using he
    rw [hee]
  have hww : dotProduct (u - e) (u - e) = 2 - 2 * dotProduct u e := by
    rw [dotProduct_sub_left u e (u - e)]
    rw [dotProduct_sub_right u u e, dotProduct_sub_right e u e]
    have huu : dotProduct u u = 1 := by simpa [unitVec3] using hu
    have hee : dotProduct e e = 1 := by simpa [unitVec3] using he
    rw [huu, hee]
    rw [dotProduct_symm e u]
    ring
  rw [hwe]
  nlinarith [hww]

/-- The `v`-vector of L5: `v = a·e + b·p` (unit, due south of `e` at distance `r/2`). -/
def l5_v (e p : Fin 3 → ℝ) (r : ℝ) : Fin 3 → ℝ :=
  (1 - r ^ 2 / 8) • e + (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16)) • p

/-- `v·e = a` and `v·p = b` for the L5 `v` (unit `e ⊥ p`). -/
theorem l5_v_dots (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) :
    dotProduct (l5_v e p r) e = 1 - r ^ 2 / 8 ∧ dotProduct (l5_v e p r) p = -(r / 2) * Real.sqrt (1 - r ^ 2 / 16) := by
  constructor
  · dsimp [l5_v]
    rw [dotProduct_add_smul e p e (1 - r ^ 2 / 8) (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16))]
    have hee : dotProduct e e = 1 := by simpa [unitVec3] using he
    have hep0 : dotProduct p e = 0 := by simpa [orthVec3, dotProduct_symm] using hep
    rw [hee, hep0]
    ring
  · dsimp [l5_v]
    rw [dotProduct_add_smul e p p (1 - r ^ 2 / 8) (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16))]
    have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
    have hep0 : dotProduct e p = 0 := by simpa [orthVec3] using hep
    rw [hpp, hep0]
    ring

/-- The L5 `v` is a unit vector (for `0 < r < 1`, unit `e ⊥ p`). -/
theorem l5_v_unit (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) :
    unitVec3 (l5_v e p r) := by
  have hγsq : (Real.sqrt (1 - r ^ 2 / 16)) ^ 2 = 1 - r ^ 2 / 16 :=
    Real.sq_sqrt (by nlinarith [sq_nonneg r] : 0 ≤ 1 - r ^ 2 / 16)
  change dotProduct ((1 - r ^ 2 / 8) • e + (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16)) • p) ((1 - r ^ 2 / 8) • e + (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16)) • p) = 1
  rw [dotProduct_expand e p (1 - r ^ 2 / 8) (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16))]
  have hee : dotProduct e e = 1 := by simpa [unitVec3] using he
  have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
  have hep0 : dotProduct e p = 0 := by simpa [orthVec3] using hep
  rw [hee, hpp, hep0]
  rw [mul_pow, hγsq]
  ring

/-- **L5 F1**: `|(u−e)·v| ≤ a·δ²/2 + s₀·δ` — the sharp bound using `w·e = −δ²/2`. -/
theorem l5_f1 (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) (u : Fin 3 → ℝ) (hu : unitVec3 u)
    (δ : ℝ) (hδpos : 0 ≤ δ) (hδsq : δ ^ 2 = dotProduct (u - e) (u - e)) :
    |dotProduct (u - e) (l5_v e p r)| ≤ (1 - r ^ 2 / 8) * δ ^ 2 / 2 + (r / 2) * Real.sqrt (1 - r ^ 2 / 16) * δ := by
  let w : Fin 3 → ℝ := u - e
  let γ : ℝ := Real.sqrt (1 - r ^ 2 / 16)
  let a : ℝ := 1 - r ^ 2 / 8
  let s₀ : ℝ := (r / 2) * γ
  have hsc := l5_scalars r hr hr1
  dsimp [γ, a, s₀] at hsc
  have ha_gt : 7 / 8 < a := hsc.2.1.1
  have hs₀_gt : r / 4 < s₀ := hsc.2.2.1.1
  have hε : dotProduct w (l5_v e p r) = a * dotProduct w e + (-s₀) * dotProduct w p := by
    dsimp [l5_v]
    rw [dotProduct_add_smul_right w e p (1 - r ^ 2 / 8) (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16))]
    dsimp [a, s₀, γ]
    ring
  have hwe : dotProduct w e = - δ ^ 2 / 2 := by
    dsimp [w]
    rw [l5_f0 u e hu he]
    rw [hδsq]
  have hwp : |dotProduct w p| ≤ δ := by
    have hcs := dotProduct_abs_le_norm (u - e) p
    have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
    rw [hpp] at hcs
    have hsqrt : Real.sqrt (dotProduct (u - e) (u - e)) = δ := by
      rw [← hδsq]
      rw [Real.sqrt_sq_eq_abs δ]
      exact abs_of_nonneg hδpos
    dsimp [w]
    rw [hsqrt] at hcs
    rw [Real.sqrt_one] at hcs
    simpa using hcs
  calc
    |dotProduct w (l5_v e p r)|
        ≤ a * |dotProduct w e| + s₀ * |dotProduct w p| := by
          rw [hε]
          have ha_nonneg : 0 ≤ a := by nlinarith [ha_gt]
          have hs₀_nonneg : 0 ≤ s₀ := by nlinarith [hs₀_gt, hr]
          calc
            |a * dotProduct w e + (-s₀) * dotProduct w p|
                ≤ |a * dotProduct w e| + |(-s₀) * dotProduct w p| := abs_add_le _ _
            _ = a * |dotProduct w e| + s₀ * |dotProduct w p| := by
                  rw [abs_mul, abs_mul, abs_of_nonneg ha_nonneg, abs_neg, abs_of_nonneg hs₀_nonneg]
    _ ≤ a * (δ ^ 2 / 2) + s₀ * δ := by
          have hwe_abs : |dotProduct w e| = δ ^ 2 / 2 := by
            rw [hwe]
            rw [abs_of_nonpos (by nlinarith [sq_nonneg δ] : -δ ^ 2 / 2 ≤ 0)]
            ring
          rw [hwe_abs]
          nlinarith [hwp]
    _ = (1 - r ^ 2 / 8) * δ ^ 2 / 2 + (r / 2) * Real.sqrt (1 - r ^ 2 / 16) * δ := by
          dsimp [a, s₀, γ]
          ring

/-- **L5 F7 (algebraic part)**: the vector identity
`c·u − v − s·p = a·(u−e) + ε·u + (s₀−s)·p`. -/
theorem l5_f7_algebra (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p) (r : ℝ) (u : Fin 3 → ℝ) :
    (dotProduct u (l5_v e p r)) • u - l5_v e p r - (Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) • p
      = (1 - r ^ 2 / 8) • (u - e) + (dotProduct (u - e) (l5_v e p r)) • u
        + ((r / 2) * Real.sqrt (1 - r ^ 2 / 16) - Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) • p := by
  let a : ℝ := 1 - r ^ 2 / 8
  let s₀ : ℝ := (r / 2) * Real.sqrt (1 - r ^ 2 / 16)
  let ε : ℝ := dotProduct (u - e) (l5_v e p r)
  let c : ℝ := dotProduct u (l5_v e p r)
  have hc : c = ε + a := by
    have hve0 : dotProduct (l5_v e p r) e = 1 - r ^ 2 / 8 := (l5_v_dots e p he hp hep r).1
    have hve : dotProduct e (l5_v e p r) = a := by
      rw [dotProduct_symm e (l5_v e p r)]
      dsimp [a]
      exact hve0
    dsimp [c, ε]
    nlinarith [dotProduct_sub_left u e (l5_v e p r), hve]
  have hv : l5_v e p r = a • e + (-s₀) • p := by
    ext i; fin_cases i <;> simp [l5_v, a, s₀, Pi.smul_apply]
  calc
    (dotProduct u (l5_v e p r)) • u - l5_v e p r - (Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) • p
        = c • u - (a • e + (-s₀) • p) - (Real.sqrt (1 - c ^ 2)) • p := by
            dsimp [c]
            rw [hv]
    _ = c • u - a • e + s₀ • p - (Real.sqrt (1 - c ^ 2)) • p := by
            ext i; fin_cases i <;> simp [Pi.smul_apply, sub_eq_add_neg] <;> ring
    _ = (a + ε) • u - a • e + (s₀ - Real.sqrt (1 - c ^ 2)) • p := by
            rw [hc]
            ext i; fin_cases i <;> simp [Pi.smul_apply, sub_eq_add_neg] <;> ring
    _ = a • (u - e) + ε • u + (s₀ - Real.sqrt (1 - c ^ 2)) • p := by
            ext i; fin_cases i <;> simp [Pi.smul_apply, sub_eq_add_neg] <;> ring
    _ = (1 - r ^ 2 / 8) • (u - e) + (dotProduct (u - e) (l5_v e p r)) • u
          + ((r / 2) * Real.sqrt (1 - r ^ 2 / 16) - Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) • p := by
            dsimp [a, ε, c, s₀]

/-- **L5 F7 (smul part)**: `(1/s)·x − p = (1/s)·(x − s·p)` for `s ≠ 0`. -/
theorem l5_f7_smul (s : ℝ) (x p : Fin 3 → ℝ) (hs : s ≠ 0) :
    (1 / s) • x - p = (1 / s) • (x - s • p) := by
  ext i
  fin_cases i <;> simp [Pi.smul_apply, sub_eq_add_neg] <;> field_simp [hs] <;> ring

/-- **L5 F7**: `λ(u) − p = (a·w + ε·u + (s₀−s)·p)/s`. -/
theorem l5_f7 (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p) (r : ℝ) (u : Fin 3 → ℝ)
    (hs : Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2) ≠ 0) :
    phi_map u (l5_v e p r) - p
      = (1 / Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2))
        • ((1 - r ^ 2 / 8) • (u - e) + (dotProduct (u - e) (l5_v e p r)) • u
          + ((r / 2) * Real.sqrt (1 - r ^ 2 / 16) - Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) • p) := by
  dsimp [phi_map]
  rw [l5_f7_smul (Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) ((dotProduct u (l5_v e p r)) • u - l5_v e p r) p hs]
  rw [l5_f7_algebra e p he hp hep r u]


/-- **L5 F2**: from `|(u−e)·v| ≤ a·δ²/2 + s₀·δ` bound `|u·v| < 1 − 23r²/288`. -/
theorem l5_f2 (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) (u : Fin 3 → ℝ) (hu : unitVec3 u)
    (δ : ℝ) (hδpos : 0 ≤ δ) (hδlt : δ < r ^ 2 / 12)
    (hF1 : |dotProduct (u - e) (l5_v e p r)| ≤ (1 - r ^ 2 / 8) * δ ^ 2 / 2 + (r / 2) * Real.sqrt (1 - r ^ 2 / 16) * δ) :
    |dotProduct u (l5_v e p r)| < 1 - 23 * r ^ 2 / 288 := by
  let γ : ℝ := Real.sqrt (1 - r ^ 2 / 16)
  let a : ℝ := 1 - r ^ 2 / 8
  let s₀ : ℝ := (r / 2) * γ
  have hsc := l5_scalars r hr hr1
  dsimp [γ, a, s₀] at hsc
  have ha_lt : a < 1 := hsc.2.1.2
  have ha_gt0 : 0 < a := by
    have h : 7 / 8 < a := hsc.2.1.1
    linarith
  have hs₀_lt : s₀ < r / 2 := hsc.2.2.1.2
  have hs₀_gt0 : 0 < s₀ := by
    have h : r / 4 < s₀ := hsc.2.2.1.1
    linarith [h, hr]
  have hdots := l5_v_dots e p he hp hep r
  have hve : dotProduct (l5_v e p r) e = a := by
    dsimp [a]
    exact hdots.1
  have hsub := dotProduct_sub_left u e (l5_v e p r)
  have hsymm : dotProduct e (l5_v e p r) = dotProduct (l5_v e p r) e :=
    dotProduct_symm e (l5_v e p r)
  have hev : dotProduct e (l5_v e p r) = a := by
    rw [hsymm, hve]
  have hF1' : |dotProduct (u - e) (l5_v e p r)| ≤ a * δ ^ 2 / 2 + s₀ * δ := by
    dsimp [a, s₀, γ]
    exact hF1
  have hc_eq : dotProduct u (l5_v e p r) = dotProduct (u - e) (l5_v e p r) + a := by
    linarith [hsub, hev]
  have htri : |dotProduct u (l5_v e p r)| ≤ |dotProduct (u - e) (l5_v e p r)| + a := by
    calc
      |dotProduct u (l5_v e p r)| = |dotProduct (u - e) (l5_v e p r) + a| := by rw [hc_eq]
      _ ≤ |dotProduct (u - e) (l5_v e p r)| + |a| := abs_add_le _ _
      _ = |dotProduct (u - e) (l5_v e p r)| + a := by rw [abs_of_pos ha_gt0]
  have hM_nonneg : 0 ≤ r ^ 2 / 12 := by linarith [sq_nonneg r]
  have hδsq_lt : δ ^ 2 < (r ^ 2 / 12) ^ 2 := by
    rw [sq_lt_sq]
    rw [abs_of_nonneg hδpos, abs_of_nonneg hM_nonneg]
    exact hδlt
  have hδsq_bound : δ ^ 2 < r ^ 4 / 144 := by
    have h : (r ^ 2 / 12) ^ 2 = r ^ 4 / 144 := by ring
    rwa [← h]
  have hr4_pos : 0 < r ^ 4 := by nlinarith [hr]
  have hadsq_lt : a * δ ^ 2 / 2 < r ^ 4 / 288 := by
    have hstep : a * δ ^ 2 < a * (r ^ 4 / 144) :=
      mul_lt_mul_of_pos_left hδsq_bound ha_gt0
    have hdiv : a * (r ^ 4 / 144) < r ^ 4 / 144 := by
      have hr4over144_pos : 0 < r ^ 4 / 144 := by nlinarith [hr4_pos]
      have h : a * (r ^ 4 / 144) < 1 * (r ^ 4 / 144) :=
        mul_lt_mul_of_pos_right ha_lt hr4over144_pos
      simpa using h
    have hstep2 : a * δ ^ 2 < r ^ 4 / 144 := lt_trans hstep hdiv
    linarith [hstep2]
  have hr2over12_pos : 0 < r ^ 2 / 12 := by nlinarith [hr]
  have hs₀δ_lt : s₀ * δ < (r / 2) * (r ^ 2 / 12) := by
    have h1 : s₀ * δ < s₀ * (r ^ 2 / 12) := mul_lt_mul_of_pos_left hδlt hs₀_gt0
    have h2 : s₀ * (r ^ 2 / 12) < (r / 2) * (r ^ 2 / 12) :=
      mul_lt_mul_of_pos_right hs₀_lt hr2over12_pos
    exact lt_trans h1 h2
  have hs₀δ_bound : s₀ * δ < r ^ 3 / 24 := by
    have h : (r / 2) * (r ^ 2 / 12) = r ^ 3 / 24 := by ring
    rw [← h]
    exact hs₀δ_lt
  have hsum : |dotProduct u (l5_v e p r)| < a + r ^ 4 / 288 + r ^ 3 / 24 := by
    have hmid1 : |dotProduct u (l5_v e p r)| ≤ a * δ ^ 2 / 2 + s₀ * δ + a := by
      calc
        |dotProduct u (l5_v e p r)| ≤ |dotProduct (u - e) (l5_v e p r)| + a := htri
        _ ≤ a * δ ^ 2 / 2 + s₀ * δ + a := by linarith [hF1']
    have hmid2 : a * δ ^ 2 / 2 + s₀ * δ + a < a + r ^ 4 / 288 + r ^ 3 / 24 := by
      linarith [hadsq_lt, hs₀δ_bound]
    exact lt_of_le_of_lt hmid1 hmid2
  have hr2_pos : 0 < r ^ 2 := by nlinarith [hr]
  have hr2_lt1 : r ^ 2 < 1 := by nlinarith [hr, hr1]
  have hr3_lt : r ^ 3 < r ^ 2 := by
    have hfac : r ^ 3 - r ^ 2 = r ^ 2 * (r - 1) := by ring
    have hneg : r - 1 < 0 := by linarith [hr1]
    have hprod : r ^ 2 * (r - 1) < 0 := mul_neg_of_pos_of_neg hr2_pos hneg
    linarith [hfac, hprod]
  have hr4_lt : r ^ 4 < r ^ 2 := by
    have hfac : r ^ 4 - r ^ 2 = r ^ 2 * (r ^ 2 - 1) := by ring
    have hneg : r ^ 2 - 1 < 0 := by linarith [hr2_lt1]
    have hprod : r ^ 2 * (r ^ 2 - 1) < 0 := mul_neg_of_pos_of_neg hr2_pos hneg
    linarith [hfac, hprod]
  have hfinal_arith : a + r ^ 4 / 288 + r ^ 3 / 24 < 1 - 23 * r ^ 2 / 288 := by
    dsimp [a]
    have h1 : r ^ 4 / 288 < r ^ 2 / 288 := by linarith [hr4_lt]
    have h2 : r ^ 3 / 24 < r ^ 2 / 24 := by linarith [hr3_lt]
    linarith [h1, h2]
  exact lt_trans hsum hfinal_arith

/-- **L5 F3**: `|c| < 1 − 23r²/288` gives `√(1−c²) > r/3`. -/
theorem l5_f3 (r : ℝ) (hr : 0 < r) (hr1 : r < 1)
    (c : ℝ) (hF2 : |c| < 1 - 23 * r ^ 2 / 288) :
    Real.sqrt (1 - c ^ 2) > r / 3 := by
  have hr2_lt1 : r ^ 2 < 1 := by nlinarith [hr, hr1]
  have hb_pos : 0 < 1 - 23 * r ^ 2 / 288 := by
    have h : 23 * r ^ 2 / 288 < 1 := by linarith [hr2_lt1]
    linarith
  have hb_nonneg : 0 ≤ 1 - 23 * r ^ 2 / 288 := by linarith [hb_pos]
  have hc_sq : c ^ 2 < (1 - 23 * r ^ 2 / 288) ^ 2 := by
    have h : |c| < |1 - 23 * r ^ 2 / 288| := by
      rwa [abs_of_nonneg hb_nonneg]
    exact sq_lt_sq.mpr h
  have hsq : (r / 3) ^ 2 < 1 - c ^ 2 := by
    have hchain : 1 - c ^ 2 > 1 - (1 - 23 * r ^ 2 / 288) ^ 2 := by
      linarith [hc_sq]
    have hr2_pos : 0 < r ^ 2 := by nlinarith [hr]
    have hr4_lt2 : r ^ 4 < r ^ 2 := by
      have hfac : r ^ 4 - r ^ 2 = r ^ 2 * (r ^ 2 - 1) := by ring
      have hneg : r ^ 2 - 1 < 0 := by linarith [hr2_lt1]
      have hprod : r ^ 2 * (r ^ 2 - 1) < 0 := mul_neg_of_pos_of_neg hr2_pos hneg
      linarith [hfac, hprod]
    have hmid : 1 - (1 - 23 * r ^ 2 / 288) ^ 2 > r ^ 2 * 12719 / 82944 := by
      have h : 1 - (1 - 23 * r ^ 2 / 288) ^ 2 = r ^ 2 * 12719 / 82944 + 529 * (r ^ 2 - r ^ 4) / 82944 := by
        ring
      rw [h]
      have hdiff : 0 < 529 * (r ^ 2 - r ^ 4) / 82944 := by
        have h1 : 0 < r ^ 2 - r ^ 4 := by linarith [hr4_lt2]
        have hcoef : 0 < (529 : ℝ) := by norm_num
        have hden : 0 < (82944 : ℝ) := by norm_num
        have h2 : 0 < 529 * (r ^ 2 - r ^ 4) := mul_pos hcoef h1
        exact div_pos h2 hden
      linarith [hdiff]
    have hcoef : (1 : ℝ) / 9 < 12719 / 82944 := by norm_num
    have hlast : (r / 3) ^ 2 < r ^ 2 * 12719 / 82944 := by
      have h : r ^ 2 * (1 / 9) < r ^ 2 * (12719 / 82944) :=
        mul_lt_mul_of_pos_left hcoef hr2_pos
      calc
        (r / 3) ^ 2 = r ^ 2 * (1 / 9) := by ring
        _ < r ^ 2 * (12719 / 82944) := h
        _ = r ^ 2 * 12719 / 82944 := by ring
    linarith [hchain, hmid, hlast]
  have hr3_nonneg : 0 ≤ r / 3 := by linarith [hr]
  have hsqrt_nonneg : 0 ≤ Real.sqrt (1 - c ^ 2) := Real.sqrt_nonneg _
  have hnonneg_1c : 0 ≤ 1 - c ^ 2 := by linarith [hsq, sq_nonneg (r / 3)]
  have hsq_sqrt : (Real.sqrt (1 - c ^ 2)) ^ 2 = 1 - c ^ 2 := Real.sq_sqrt hnonneg_1c
  have h : (r / 3) ^ 2 < (Real.sqrt (1 - c ^ 2)) ^ 2 := by
    rw [hsq_sqrt]
    exact hsq
  have h' : |r / 3| < |Real.sqrt (1 - c ^ 2)| := sq_lt_sq.mp h
  rwa [abs_of_nonneg hr3_nonneg, abs_of_nonneg hsqrt_nonneg] at h'

-- The nlinarith bounds in l5_f4/f5/f6 exceed the default heartbeat budget.
set_option maxHeartbeats 4000000 in
/-- **L5 F4**: `‖a·w + ε·u‖ < (11/10)δ` with `a = 1−r²/8`, `w = u−e`, `ε = (u−e)·v`.
Needs `0 < δ` (the `δ = 0` case makes the conclusion `0 < 0`, which is false). -/
theorem l5_f4 (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) (u : Fin 3 → ℝ) (hu : unitVec3 u)
    (δ : ℝ) (hδpos : 0 < δ) (hδlt : δ < r ^ 2 / 12)
    (hδsq : δ ^ 2 = dotProduct (u - e) (u - e))
    (hF1 : |dotProduct (u - e) (l5_v e p r)| ≤ (1 - r ^ 2 / 8) * δ ^ 2 / 2 + (r / 2) * Real.sqrt (1 - r ^ 2 / 16) * δ) :
    dotProduct ((1 - r ^ 2 / 8) • (u - e) + (dotProduct (u - e) (l5_v e p r)) • u)
      ((1 - r ^ 2 / 8) • (u - e) + (dotProduct (u - e) (l5_v e p r)) • u) < ((11 / 10) * δ) ^ 2 := by
  let γ : ℝ := Real.sqrt (1 - r ^ 2 / 16)
  let a : ℝ := 1 - r ^ 2 / 8
  let s₀ : ℝ := (r / 2) * γ
  let w : Fin 3 → ℝ := u - e
  let ε : ℝ := dotProduct w (l5_v e p r)
  change dotProduct (a • w + ε • u) (a • w + ε • u) < ((11 / 10) * δ) ^ 2
  have hsc := l5_scalars r hr hr1
  dsimp [γ, a, s₀] at hsc
  have ha_gt : 7 / 8 < a := hsc.2.1.1
  have ha_lt : a < 1 := hsc.2.1.2
  have hs₀_gt : r / 4 < s₀ := hsc.2.2.1.1
  have hs₀_lt : s₀ < r / 2 := hsc.2.2.1.2
  have hab : a ^ 2 + s₀ ^ 2 = 1 := hsc.2.2.2
  have ha_pos : 0 < a := by nlinarith [ha_gt]
  have ha_nonneg : 0 ≤ a := le_of_lt ha_pos
  have hs₀_pos : 0 < s₀ := by nlinarith [hs₀_gt, hr]
  have hF1ε : |ε| ≤ a * δ ^ 2 / 2 + s₀ * δ := by
    dsimp [ε, w, a, s₀, γ]
    exact hF1
  have hww : dotProduct w w = δ ^ 2 := by
    dsimp [w]
    rw [hδsq]
  have huu : dotProduct u u = 1 := by simpa [unitVec3] using hu
  have hwu : dotProduct w u = δ ^ 2 / 2 := by
    dsimp [w]
    rw [dotProduct_sub_left u e u]
    rw [huu]
    have heu : dotProduct e u = 1 - δ ^ 2 / 2 := by
      rw [dotProduct_symm e u]
      have hue : dotProduct u e = 1 - δ ^ 2 / 2 := by
        have hdecomp : dotProduct (u - e) e = dotProduct u e - 1 := by
          rw [dotProduct_sub_left u e e]
          have hee : dotProduct e e = 1 := by simpa [unitVec3] using he
          rw [hee]
        have hwe' : dotProduct (u - e) e = - δ ^ 2 / 2 := by
          rw [l5_f0 u e hu he]
          rw [hδsq]
        nlinarith
      exact hue
    rw [heu]
    ring
  have hnorm : dotProduct (a • w + ε • u) (a • w + ε • u) = a ^ 2 * δ ^ 2 + a * ε * δ ^ 2 + ε ^ 2 := by
    rw [dotProduct_expand w u a ε]
    rw [hww, hwu, huu]
    ring
  have hε_le_abs : ε ≤ |ε| := le_abs_self ε
  have habs_nonneg : 0 ≤ |ε| := abs_nonneg ε
  have hεsq : ε ^ 2 = |ε| ^ 2 := (sq_abs ε).symm
  have hδ2_nonneg : 0 ≤ δ ^ 2 := sq_nonneg δ
  let B : ℝ := a * δ ^ 2 / 2 + s₀ * δ
  have hε_le_B : |ε| ≤ B := by
    dsimp [B]
    exact hF1ε
  have hb1 : a * ε * δ ^ 2 + ε ^ 2 ≤ a * |ε| * δ ^ 2 + |ε| ^ 2 := by
    have haε : a * ε ≤ a * |ε| := mul_le_mul_of_nonneg_left hε_le_abs ha_nonneg
    have haεδ2 : a * ε * δ ^ 2 ≤ a * |ε| * δ ^ 2 := mul_le_mul_of_nonneg_right haε hδ2_nonneg
    linarith [haεδ2, hεsq]
  have hb2 : a * |ε| * δ ^ 2 + |ε| ^ 2 ≤ a * B * δ ^ 2 + B ^ 2 := by
    have hB_nonneg : 0 ≤ B := by
      dsimp [B]
      linarith [hF1ε, habs_nonneg]
    have hdiff1 : 0 ≤ B - |ε| := sub_nonneg.mpr hε_le_B
    have haδ2 : 0 ≤ a * δ ^ 2 := mul_nonneg ha_nonneg hδ2_nonneg
    have hsecond : 0 ≤ a * δ ^ 2 + B + |ε| := by
      linarith [haδ2, hB_nonneg, habs_nonneg]
    have hprod : 0 ≤ (B - |ε|) * (a * δ ^ 2 + B + |ε|) := mul_nonneg hdiff1 hsecond
    have hdiff_eq : (B - |ε|) * (a * δ ^ 2 + B + |ε|)
        = a * B * δ ^ 2 + B ^ 2 - (a * |ε| * δ ^ 2 + |ε| ^ 2) := by
      ring
    have hprod' : 0 ≤ a * B * δ ^ 2 + B ^ 2 - (a * |ε| * δ ^ 2 + |ε| ^ 2) := by
      rw [← hdiff_eq]
      exact hprod
    linarith [hprod']
  have hb : a ^ 2 * δ ^ 2 + a * ε * δ ^ 2 + ε ^ 2 ≤ a ^ 2 * δ ^ 2 + a * B * δ ^ 2 + B ^ 2 := by
    linarith [hb1, hb2]
  have hRHS' : a ^ 2 * δ ^ 2 + a * B * δ ^ 2 + B ^ 2
      = δ ^ 2 * (1 + (3 / 4) * a ^ 2 * δ ^ 2 + 2 * a * s₀ * δ) + (a ^ 2 + s₀ ^ 2 - 1) * δ ^ 2 := by
    dsimp [B]
    ring
  have hRHS : a ^ 2 * δ ^ 2 + a * B * δ ^ 2 + B ^ 2 = δ ^ 2 * (1 + (3 / 4) * a ^ 2 * δ ^ 2 + 2 * a * s₀ * δ) := by
    rw [hRHS']
    have hab0 : a ^ 2 + s₀ ^ 2 - 1 = 0 := by linarith [hab]
    rw [hab0]
    ring
  have hle : a ^ 2 * δ ^ 2 + a * ε * δ ^ 2 + ε ^ 2 ≤ δ ^ 2 * (1 + (3 / 4) * a ^ 2 * δ ^ 2 + 2 * a * s₀ * δ) := by
    rw [hRHS] at hb
    exact hb
  have hr2 : r ^ 2 < 1 := by nlinarith [hr, hr1]
  have hδ12 : δ < 1 / 12 := by nlinarith [hδlt, hr2]
  have hs₀_half : s₀ < 1 / 2 := by nlinarith [hs₀_lt, hr1]
  have hlt : δ ^ 2 * (1 + (3 / 4) * a ^ 2 * δ ^ 2 + 2 * a * s₀ * δ) < ((11 / 10) * δ) ^ 2 := by
    have hδ2_pos : 0 < δ ^ 2 := sq_pos_of_pos hδpos
    have ha2_lt1 : a ^ 2 < 1 := by nlinarith [ha_lt, ha_pos]
    have hδ2_lt : δ ^ 2 < (1 / 12) ^ 2 := by nlinarith [hδpos, hδ12]
    have ha2δ2_lt : a ^ 2 * δ ^ 2 < (1 / 12) ^ 2 := by
      have hstep : a ^ 2 * δ ^ 2 < 1 * δ ^ 2 := mul_lt_mul_of_pos_right ha2_lt1 hδ2_pos
      have hstep2 : 1 * δ ^ 2 < 1 * ((1 / 12) ^ 2) :=
        mul_lt_mul_of_pos_left hδ2_lt (by norm_num : (0 : ℝ) < 1)
      linarith [hstep, hstep2]
    have has₀ : a * s₀ < 1 / 2 := by
      have h1 : a * s₀ < 1 * s₀ := mul_lt_mul_of_pos_right ha_lt hs₀_pos
      have h2 : 1 * s₀ < 1 * (1 / 2) := mul_lt_mul_of_pos_left hs₀_half (by norm_num : (0 : ℝ) < 1)
      linarith [h1, h2]
    have has₀δ : a * s₀ * δ < (1 / 2) * (1 / 12) := by
      have h1 : a * s₀ * δ < (1 / 2) * δ := mul_lt_mul_of_pos_right has₀ hδpos
      have h2 : (1 / 2) * δ < (1 / 2) * (1 / 12) :=
        mul_lt_mul_of_pos_left hδ12 (by norm_num : (0 : ℝ) < 1 / 2)
      linarith [h1, h2]
    have hbracket : 1 + (3 / 4) * a ^ 2 * δ ^ 2 + 2 * a * s₀ * δ < (11 / 10) ^ 2 := by
      have h1' : (3 / 4) * (a ^ 2 * δ ^ 2) < (3 / 4) * (1 / 12) ^ 2 :=
        mul_lt_mul_of_pos_left ha2δ2_lt (by norm_num : (0 : ℝ) < 3 / 4)
      have h2' : 2 * (a * s₀ * δ) < 2 * ((1 / 2) * (1 / 12)) :=
        mul_lt_mul_of_pos_left has₀δ (by norm_num : (0 : ℝ) < 2)
      have hsum : 1 + (3 / 4) * (a ^ 2 * δ ^ 2) + 2 * (a * s₀ * δ)
          < 1 + (3 / 4) * (1 / 12) ^ 2 + 2 * ((1 / 2) * (1 / 12)) := by
        linarith [h1', h2']
      have hconst : (1 + (3 / 4 : ℝ) * (1 / 12 : ℝ) ^ 2 + 2 * ((1 / 2 : ℝ) * (1 / 12 : ℝ)) < (11 / 10 : ℝ) ^ 2) := by norm_num
      have hsum' : 1 + (3 / 4) * (a ^ 2 * δ ^ 2) + 2 * (a * s₀ * δ) < (11 / 10) ^ 2 := by
        linarith [hsum, hconst]
      ring_nf at hsum' ⊢
      exact hsum'
    have hstep : δ ^ 2 * (1 + (3 / 4) * a ^ 2 * δ ^ 2 + 2 * a * s₀ * δ) < δ ^ 2 * (11 / 10) ^ 2 :=
      mul_lt_mul_of_pos_left hbracket hδ2_pos
    ring_nf at hstep ⊢
    exact hstep
  have hfinal : a ^ 2 * δ ^ 2 + a * ε * δ ^ 2 + ε ^ 2 < ((11 / 10) * δ) ^ 2 :=
    lt_of_le_of_lt hle hlt
  rw [hnorm]
  exact hfinal
-- The nlinarith bounds in l5_f4/f5/f6 exceed the default heartbeat budget.
set_option maxHeartbeats 4000000 in
/-- **L5 F5**: `s₀ + s > r/2` from `s₀ > r/4` (i.e. `γ > 1/2`) and `s > r/3`. -/
theorem l5_f5 (r : ℝ) (hr : 0 < r) (hr1 : r < 1) (s : ℝ) (hs : r / 3 < s) :
    (r / 2) * Real.sqrt (1 - r ^ 2 / 16) + s > r / 2 := by
  let γ : ℝ := Real.sqrt (1 - r ^ 2 / 16)
  let a : ℝ := 1 - r ^ 2 / 8
  let s₀ : ℝ := (r / 2) * γ
  have hsc := l5_scalars r hr hr1
  dsimp [γ, a, s₀] at hsc
  have hs₀_gt : r / 4 < s₀ := hsc.2.2.1.1
  change s₀ + s > r / 2
  nlinarith [hs₀_gt, hs, hr]
-- The nlinarith bounds in l5_f4/f5/f6 exceed the default heartbeat budget.
set_option maxHeartbeats 4000000 in
/-- **L5 F6**: `|s₀ − s| < (7/3)δ` for `s` the sine of `u` (i.e. `s² = 1 − (u·v)²`)
and `s > r/3` (so `s₀ + s > r/2` via F5). This is the Richman–Bridges oscillation
estimate: `s₀ − s = (2aε + ε²)/(s₀ + s)` with `ε = (u−e)·v` bounded by F1. -/
theorem l5_f6 (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) (u : Fin 3 → ℝ) (hu : unitVec3 u)
    (δ : ℝ) (hδpos : 0 < δ) (hδlt : δ < r ^ 2 / 12)
    (s : ℝ) (hs : s ^ 2 = 1 - (dotProduct u (l5_v e p r)) ^ 2) (hs_gt : r / 3 < s)
    (hF1 : |dotProduct (u - e) (l5_v e p r)| ≤ (1 - r ^ 2 / 8) * δ ^ 2 / 2 + (r / 2) * Real.sqrt (1 - r ^ 2 / 16) * δ) :
    |(r / 2) * Real.sqrt (1 - r ^ 2 / 16) - s| < (7 / 3) * δ := by
  let γ : ℝ := Real.sqrt (1 - r ^ 2 / 16)
  let a : ℝ := 1 - r ^ 2 / 8
  let s₀ : ℝ := (r / 2) * γ
  let c : ℝ := dotProduct u (l5_v e p r)
  let ε : ℝ := dotProduct (u - e) (l5_v e p r)
  have hsc := l5_scalars r hr hr1
  dsimp [γ, a, s₀] at hsc
  have ha_lt : a < 1 := hsc.2.1.2
  have ha_gt : 7 / 8 < a := hsc.2.1.1
  have hs₀_lt : s₀ < r / 2 := hsc.2.2.1.2
  have hs₀_gt : r / 4 < s₀ := hsc.2.2.1.1
  have hab : a ^ 2 + s₀ ^ 2 = 1 := hsc.2.2.2
  have ha_pos : 0 ≤ a := by nlinarith [ha_gt]
  have hs₀_pos : 0 ≤ s₀ := by nlinarith [hs₀_gt, hr]
  have hs₀sq : s₀ ^ 2 = 1 - a ^ 2 := by nlinarith [hab]
  have hF5 : s₀ + s > r / 2 := by
    have h := l5_f5 r hr hr1 s hs_gt
    simpa [s₀, γ] using h
  have hvd := l5_v_dots e p he hp hep r
  have hε : ε = c - a := by
    dsimp [ε, c]
    rw [dotProduct_sub_left u e (l5_v e p r)]
    have h2 : dotProduct e (l5_v e p r) = a := by
      rw [dotProduct_symm e (l5_v e p r)]
      exact hvd.1
    rw [h2]
  have hc : c = a + ε := by nlinarith [hε]
  have hs' : s ^ 2 = 1 - c ^ 2 := by
    dsimp [c]
    exact hs
  have hdiff : s₀ ^ 2 - s ^ 2 = 2 * a * ε + ε ^ 2 := by
    rw [hs₀sq, hs', hc]
    ring
  have hF1' : |ε| ≤ a * δ ^ 2 / 2 + s₀ * δ := by
    dsimp [ε, a, s₀, γ]
    exact hF1
  have habs_nonneg : 0 ≤ |ε| := abs_nonneg ε
  have h_abs_mul : |2 * a * ε| = 2 * a * |ε| := by
    rw [abs_mul, abs_mul, abs_of_nonneg ha_pos]
    norm_num
  have h_abs_sq : |ε ^ 2| = |ε| ^ 2 := by
    rw [abs_sq, sq_abs]
  have hnum : |2 * a * ε + ε ^ 2| ≤ 2 * a * |ε| + |ε| ^ 2 := by
    calc
      |2 * a * ε + ε ^ 2| ≤ |2 * a * ε| + |ε ^ 2| := abs_add_le _ _
      _ = 2 * a * |ε| + |ε| ^ 2 := by rw [h_abs_mul, h_abs_sq]
  -- 2a|ε| + |ε|² ≤ 2aE + E²  (E := a·δ²/2 + s₀·δ)
  have hsum_le : 2 * a * |ε| + |ε| ^ 2 ≤ 2 * a * (a * δ ^ 2 / 2 + s₀ * δ) + (a * δ ^ 2 / 2 + s₀ * δ) ^ 2 := by
    have hε_le_E : |ε| ≤ a * δ ^ 2 / 2 + s₀ * δ := hF1'
    have hE_nonneg : 0 ≤ a * δ ^ 2 / 2 + s₀ * δ := by nlinarith [hF1', habs_nonneg]
    have hdiff1 : 0 ≤ (a * δ ^ 2 / 2 + s₀ * δ) - |ε| := sub_nonneg.mpr hε_le_E
    have ha2 : 0 ≤ 2 * a := by nlinarith [ha_pos]
    have hsecond : 0 ≤ 2 * a + (a * δ ^ 2 / 2 + s₀ * δ) + |ε| := by
      nlinarith [ha2, hE_nonneg, habs_nonneg]
    have hprod : 0 ≤ ((a * δ ^ 2 / 2 + s₀ * δ) - |ε|) * (2 * a + (a * δ ^ 2 / 2 + s₀ * δ) + |ε|) :=
      mul_nonneg hdiff1 hsecond
    nlinarith [hprod]
  -- 2aE + E² < (7r/6)·δ
  have hE_lt_M : a * δ ^ 2 / 2 + s₀ * δ < δ ^ 2 / 2 + (r / 2) * δ := by
    nlinarith [ha_lt, hs₀_lt, hδpos]
  have hE_nonneg : 0 ≤ a * δ ^ 2 / 2 + s₀ * δ := by nlinarith [ha_pos, hs₀_pos, hδpos]
  have hM_nonneg : 0 ≤ δ ^ 2 / 2 + (r / 2) * δ := by nlinarith [hδpos, hr]
  have hEsq_lt_Msq : (a * δ ^ 2 / 2 + s₀ * δ) ^ 2 < (δ ^ 2 / 2 + (r / 2) * δ) ^ 2 := by
    rw [sq_lt_sq, abs_of_nonneg hE_nonneg, abs_of_nonneg hM_nonneg]
    exact hE_lt_M
  have h2E_lt : 2 * (a * δ ^ 2 / 2 + s₀ * δ) + (a * δ ^ 2 / 2 + s₀ * δ) ^ 2
      < 2 * (δ ^ 2 / 2 + (r / 2) * δ) + (δ ^ 2 / 2 + (r / 2) * δ) ^ 2 := by
    nlinarith [hE_lt_M, hEsq_lt_Msq, hE_nonneg, hM_nonneg]
  have hM_lt : 2 * (δ ^ 2 / 2 + (r / 2) * δ) + (δ ^ 2 / 2 + (r / 2) * δ) ^ 2 < (7 * r / 6) * δ := by
    have hT1 : δ ^ 2 < (r / 12) * δ := by
      nlinarith [hδlt, hδpos, hr, hr1]
    have hT2 : δ ^ 4 / 4 < (r / 576) * δ := by
      nlinarith [hδlt, hδpos, hr, hr1]
    have hT3 : r * δ ^ 3 / 2 < (r / 24) * δ := by
      nlinarith [hδlt, hδpos, hr, hr1]
    have hT4 : r ^ 2 * δ ^ 2 / 4 < (r / 48) * δ := by
      nlinarith [hδlt, hδpos, hr, hr1]
    have h_expand : 2 * (δ ^ 2 / 2 + (r / 2) * δ) + (δ ^ 2 / 2 + (r / 2) * δ) ^ 2
        = δ ^ 2 + r * δ + δ ^ 4 / 4 + r * δ ^ 3 / 2 + r ^ 2 * δ ^ 2 / 4 := by
      ring
    rw [h_expand]
    nlinarith [hT1, hT2, hT3, hT4]
  have hpoly_lt : 2 * a * (a * δ ^ 2 / 2 + s₀ * δ) + (a * δ ^ 2 / 2 + s₀ * δ) ^ 2 < (7 * r / 6) * δ := by
    have h2aE_le : 2 * a * (a * δ ^ 2 / 2 + s₀ * δ) ≤ 2 * (a * δ ^ 2 / 2 + s₀ * δ) := by
      nlinarith [ha_lt, hE_nonneg]
    have hstep1 : 2 * a * (a * δ ^ 2 / 2 + s₀ * δ) + (a * δ ^ 2 / 2 + s₀ * δ) ^ 2
        ≤ 2 * (a * δ ^ 2 / 2 + s₀ * δ) + (a * δ ^ 2 / 2 + s₀ * δ) ^ 2 :=
      add_le_add h2aE_le le_rfl
    exact lt_of_le_of_lt hstep1 (lt_trans h2E_lt hM_lt)
  have hcleared : 2 * a * |ε| + |ε| ^ 2 < (7 * r / 6) * δ := by
    nlinarith [hsum_le, hpoly_lt]
  -- (s₀ + s)·|s₀ − s| = |2aε + ε²|
  have hpos : 0 < s₀ + s := by nlinarith [hF5, hr]
  have hprod : (s₀ - s) * (s₀ + s) = s₀ ^ 2 - s ^ 2 := by ring
  have heq : (s₀ + s) * |s₀ - s| = |2 * a * ε + ε ^ 2| := by
    calc
      (s₀ + s) * |s₀ - s| = |(s₀ - s) * (s₀ + s)| := by
        rw [abs_mul, abs_of_pos hpos, mul_comm]
      _ = |s₀ ^ 2 - s ^ 2| := by rw [hprod]
      _ = |2 * a * ε + ε ^ 2| := by rw [hdiff]
  have hmid : (s₀ + s) * |s₀ - s| < (7 * r / 6) * δ := by
    nlinarith [heq, hnum, hcleared]
  have hscale : (7 * r / 6) * δ < (s₀ + s) * ((7 / 3) * δ) := by
    nlinarith [hF5, hδpos, hr]
  have hprod_lt : (s₀ + s) * |s₀ - s| < (s₀ + s) * ((7 / 3) * δ) := by
    nlinarith [hmid, hscale]
  change |s₀ - s| < (7 / 3) * δ
  exact lt_of_mul_lt_mul_left hprod_lt (le_of_lt hpos)
/-- `0 ≤ x·x` (sum of squares). -/
theorem dotProduct_self_nonneg (x : Fin 3 → ℝ) : 0 ≤ dotProduct x x := by
  have h : dotProduct x x = x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2 := by
    simp [dotProduct, Fin.sum_univ_three]
    ring
  rw [h]
  nlinarith [sq_nonneg (x 0), sq_nonneg (x 1), sq_nonneg (x 2)]

-- The nlinarith bounds in the L5 F-chain exceed the default heartbeat budget.
set_option maxHeartbeats 4000000 in
/-- **L5 (the oscillation-transfer norm estimate, Richman–Bridges Lemma 14).** For the equator
point `e`, the pole `p`, and `v = a·e + b·p` due south of `e` at distance `r/2`, if `‖u−e‖ < r²/12`
then `‖λ(u) − p‖ < r` (in fact `< (103/120)r`). This is the single geometric step of the
continuity proof. -/
theorem oscillation_transfer_norm (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) (u : Fin 3 → ℝ) (hu : unitVec3 u)
    (hδ : dotProduct (u - e) (u - e) < (r ^ 2 / 12) ^ 2) :
    dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p) < r ^ 2 := by
  let w : Fin 3 → ℝ := u - e
  let δ : ℝ := Real.sqrt (dotProduct w w)
  have hδsq : δ ^ 2 = dotProduct w w := by
    dsimp [δ]
    exact Real.sq_sqrt (by dsimp [w]; exact dotProduct_self_nonneg (u - e))
  have hδnonneg : 0 ≤ δ := by dsimp [δ]; exact Real.sqrt_nonneg _
  have hδ_small : δ < r ^ 2 / 12 := by
    have hlt : δ ^ 2 < (r ^ 2 / 12) ^ 2 := by rw [hδsq]; dsimp [w]; exact hδ
    have hnonneg : 0 ≤ r ^ 2 / 12 := by nlinarith [sq_nonneg r]
    simpa [abs_of_nonneg hδnonneg, abs_of_nonneg hnonneg] using (sq_lt_sq.mp hlt)
  by_cases hδzero : δ = 0
  · -- u = e, so λ(u) = p
    have hw0 : dotProduct (u - e) (u - e) = 0 := by
      have hδsq0 : δ ^ 2 = 0 := by rw [hδzero]; norm_num
      rw [hδsq] at hδsq0
      dsimp [w] at hδsq0
      exact hδsq0
    have hsub0 : u - e = 0 := by
      ext i
      fin_cases i
      · have hsum : ((u - e) 0) ^ 2 + ((u - e) 1) ^ 2 + ((u - e) 2) ^ 2 = 0 := by
          simpa [dotProduct, Fin.sum_univ_three, sq] using hw0
        have hsq : ((u - e) 0) ^ 2 = 0 := by nlinarith [hsum, sq_nonneg ((u - e) 0), sq_nonneg ((u - e) 1), sq_nonneg ((u - e) 2)]
        exact sq_eq_zero_iff.mp hsq
      · have hsum : ((u - e) 0) ^ 2 + ((u - e) 1) ^ 2 + ((u - e) 2) ^ 2 = 0 := by
          simpa [dotProduct, Fin.sum_univ_three, sq] using hw0
        have hsq : ((u - e) 1) ^ 2 = 0 := by nlinarith [hsum, sq_nonneg ((u - e) 0), sq_nonneg ((u - e) 1), sq_nonneg ((u - e) 2)]
        exact sq_eq_zero_iff.mp hsq
      · have hsum : ((u - e) 0) ^ 2 + ((u - e) 1) ^ 2 + ((u - e) 2) ^ 2 = 0 := by
          simpa [dotProduct, Fin.sum_univ_three, sq] using hw0
        have hsq : ((u - e) 2) ^ 2 = 0 := by nlinarith [hsum, sq_nonneg ((u - e) 0), sq_nonneg ((u - e) 1), sq_nonneg ((u - e) 2)]
        exact sq_eq_zero_iff.mp hsq
    have hue : u = e := sub_eq_zero.mp hsub0
    have hphi : phi_map u (l5_v e p r) = p := by
      rw [hue]
      refine phi_map_eq_pole e p (l5_v e p r) he hp hep (1 - r ^ 2 / 8) (-(r / 2) * Real.sqrt (1 - r ^ 2 / 16)) rfl ?_ (l5_v_unit e p he hp hep r hr hr1)
      have hsqrt_pos : 0 < Real.sqrt (1 - r ^ 2 / 16) :=
        Real.sqrt_pos.2 (by nlinarith [sq_nonneg r] : 0 < 1 - r ^ 2 / 16)
      nlinarith [hr, hsqrt_pos]
    rw [hphi]
    simp
    nlinarith [hr]
  · -- δ > 0: the F-chain
    have hδpos : 0 < δ := lt_of_le_of_ne hδnonneg (by intro h; exact hδzero (Eq.symm h))
    have hF1 := l5_f1 e p he hp hep r hr hr1 u hu δ hδnonneg hδsq
    have hF2 := l5_f2 e p he hp hep r hr hr1 u hu δ hδnonneg hδ_small hF1
    have hF3 := l5_f3 r hr hr1 (dotProduct u (l5_v e p r)) hF2
    have hF4 := l5_f4 e p he hp hep r hr hr1 u hu δ hδpos hδ_small hδsq hF1
    have hF5 := l5_f5 r hr hr1 (Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) hF3
    have hs : (Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) ^ 2 = 1 - (dotProduct u (l5_v e p r)) ^ 2 := by
      exact Real.sq_sqrt (by
        have hcs := dotProduct_abs_le_norm u (l5_v e p r)
        have huu : dotProduct u u = 1 := by simpa [unitVec3] using hu
        have hvv : dotProduct (l5_v e p r) (l5_v e p r) = 1 := by simpa [unitVec3] using l5_v_unit e p he hp hep r hr hr1
        rw [huu, hvv] at hcs
        have h1 : |dotProduct u (l5_v e p r)| ≤ 1 := by simpa [Real.sqrt_one] using hcs
        have hsq : (dotProduct u (l5_v e p r)) ^ 2 ≤ 1 := by
          have hsqabs : (dotProduct u (l5_v e p r)) ^ 2 = |dotProduct u (l5_v e p r)| ^ 2 := (sq_abs (dotProduct u (l5_v e p r))).symm
          rw [hsqabs]
          nlinarith [h1, abs_nonneg (dotProduct u (l5_v e p r))]
        nlinarith)
    have hF6 := l5_f6 e p he hp hep r hr hr1 u hu δ hδpos hδ_small (Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)) hs hF3 hF1
    have hs_ne : Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2) ≠ 0 := by
      have hpos : 0 < Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2) := by linarith [hF3, hr]
      exact ne_of_gt hpos
    have hF7 := l5_f7 e p he hp hep r u hs_ne
    -- combine F4, F6, F3, F7
    let s : ℝ := Real.sqrt (1 - (dotProduct u (l5_v e p r)) ^ 2)
    let Y : Fin 3 → ℝ := (1 - r ^ 2 / 8) • (u - e) + (dotProduct (u - e) (l5_v e p r)) • u
    let c : ℝ := (r / 2) * Real.sqrt (1 - r ^ 2 / 16) - s
    let X : Fin 3 → ℝ := Y + c • p
    have hs_pos : 0 < s := by dsimp [s]; linarith [hF3, hr]
    have hs2_ne : s ^ 2 ≠ 0 := by nlinarith [hs_pos]
    have hYp_le : |dotProduct Y p| ≤ (11 / 10) * δ := by
      have hcs := dotProduct_abs_le_norm Y p
      have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
      rw [hpp] at hcs
      have hcs' : |dotProduct Y p| ≤ Real.sqrt (dotProduct Y Y) := by simpa using hcs
      have hY_sqrt_lt : Real.sqrt (dotProduct Y Y) < (11 / 10) * δ := by
        have hYpos : 0 ≤ dotProduct Y Y := dotProduct_self_nonneg Y
        have hnonneg : 0 ≤ (11 / 10) * δ := by nlinarith [hδpos]
        have hsq : (Real.sqrt (dotProduct Y Y)) ^ 2 < ((11 / 10) * δ) ^ 2 := by
          rw [Real.sq_sqrt hYpos]
          dsimp [Y]
          exact hF4
        have h := sq_lt_sq.mp hsq
        simpa [abs_of_nonneg (Real.sqrt_nonneg _), abs_of_nonneg hnonneg] using h
      nlinarith [hcs', hY_sqrt_lt]
    have hX_sq : dotProduct X X = dotProduct Y Y + 2 * c * dotProduct Y p + c ^ 2 := by
      dsimp [X]
      change dotProduct (Y + c • p) (Y + c • p) = dotProduct Y Y + 2 * c * dotProduct Y p + c ^ 2
      rw [show Y + c • p = (1 : ℝ) • Y + c • p by simp]
      rw [dotProduct_expand Y p (1 : ℝ) c]
      have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
      rw [hpp]
      ring
    have hX_sq_lt : dotProduct X X < ((103 / 30) * δ) ^ 2 := by
      have hcyp_le : c * dotProduct Y p ≤ (7 / 3) * δ * ((11 / 10) * δ) := by
        have h1 : c * dotProduct Y p ≤ |c| * |dotProduct Y p| := by
          have h : c * dotProduct Y p ≤ |c * dotProduct Y p| := le_abs_self _
          rwa [abs_mul] at h
        have h2 : |c| * |dotProduct Y p| ≤ (7 / 3) * δ * ((11 / 10) * δ) := by
          have hpos : 0 ≤ (7 / 3) * δ := by nlinarith [hδpos]
          have hA : |c| * |dotProduct Y p| ≤ (7 / 3) * δ * |dotProduct Y p| :=
            mul_le_mul_of_nonneg_right (le_of_lt (by dsimp [c]; exact hF6)) (abs_nonneg _)
          have hB : (7 / 3) * δ * |dotProduct Y p| ≤ (7 / 3) * δ * ((11 / 10) * δ) :=
            mul_le_mul_of_nonneg_left hYp_le hpos
          exact le_trans hA hB
        exact le_trans h1 h2
      have hc_sq_lt : c ^ 2 < ((7 / 3) * δ) ^ 2 := by
        have hnonneg : 0 ≤ (7 / 3) * δ := by nlinarith [hδpos]
        have h : |c| < |(7 / 3) * δ| := by
          dsimp [c]
          simpa [abs_of_nonneg hnonneg] using hF6
        exact sq_lt_sq.mpr h
      rw [hX_sq]
      nlinarith [hF4, hcyp_le, hc_sq_lt]
    have hmain_eq : dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p) = (1 / s) ^ 2 * dotProduct X X := by
      rw [hF7]
      dsimp [s]
      change dotProduct ((1 / s) • X) ((1 / s) • X) = (1 / s) ^ 2 * dotProduct X X
      simp [dotProduct, Fin.sum_univ_three, Pi.smul_apply]
      ring
    have hX_r4 : dotProduct X X < r ^ 4 / 9 := by
      have hδ_bound : ((103 / 30) * δ) ^ 2 < ((103 / 30) * (r ^ 2 / 12)) ^ 2 := by
        have hnonneg1 : 0 ≤ (103 / 30) * δ := by nlinarith [hδpos]
        have hnonneg2 : 0 ≤ (103 / 30) * (r ^ 2 / 12) := by nlinarith [hr]
        have hlt : (103 / 30) * δ < (103 / 30) * (r ^ 2 / 12) :=
          mul_lt_mul_of_pos_left hδ_small (by norm_num : 0 < (103 / 30 : ℝ))
        exact sq_lt_sq.mpr (by simpa [abs_of_nonneg hnonneg1, abs_of_nonneg hnonneg2] using hlt)
      have hconst : ((103 / 30) * (r ^ 2 / 12)) ^ 2 < r ^ 4 / 9 := by
        ring_nf
        nlinarith [sq_nonneg r]
      nlinarith [hX_sq_lt, hδ_bound, hconst]
    have hs2_gt : r ^ 2 * s ^ 2 > r ^ 4 / 9 := by
      have hs2 : s ^ 2 > (r / 3) ^ 2 := by
        have hnonneg : 0 ≤ r / 3 := by linarith [hr]
        exact sq_lt_sq.mpr (by simpa [abs_of_nonneg hnonneg, abs_of_nonneg (le_of_lt hs_pos)] using (by dsimp [s]; exact hF3))
      have hr2_pos : 0 < r ^ 2 := sq_pos_of_pos hr
      have h : r ^ 2 * s ^ 2 > r ^ 2 * (r / 3) ^ 2 := mul_lt_mul_of_pos_left hs2 hr2_pos
      have h' : r ^ 2 * (r / 3) ^ 2 = r ^ 4 / 9 := by ring
      nlinarith [h, h']
    have hX_r2s2 : dotProduct X X < r ^ 2 * s ^ 2 := by nlinarith [hX_r4, hs2_gt]
    have hfin : (1 / s) ^ 2 * dotProduct X X < r ^ 2 := by
      have hs2_pos : 0 < s ^ 2 := sq_pos_of_pos hs_pos
      have hpos : 0 < (1 / s) ^ 2 := sq_pos_of_pos (one_div_pos.mpr hs_pos)
      have h := mul_lt_mul_of_pos_left hX_r2s2 hpos
      have h1 : (1 / s) ^ 2 * (r ^ 2 * s ^ 2) = r ^ 2 := by
        have hcomm : (1 / s) ^ 2 * (r ^ 2 * s ^ 2) = ((1 / s) ^ 2 * s ^ 2) * r ^ 2 := by ring
        have hunit : (1 / s) ^ 2 * s ^ 2 = 1 := by
          rw [← mul_pow]
          rw [one_div, inv_mul_cancel₀ hs_ne]
          norm_num
        rw [hcomm, hunit]
        ring
      nlinarith [h, h1]
    rw [hmain_eq]
    exact hfin

/-- The symmetrization `g(x) = f x + f(ρ x)` about `p` (`ρ = rot90p p`). -/
def symm (p : Fin 3 → ℝ) (f : (Fin 3 → ℝ) → ℝ) (x : Fin 3 → ℝ) : ℝ :=
  f x + f (rot90p p x)

/-- `ρ` fixes the pole: `ρ p = p`. -/
theorem rot90p_pole (p : Fin 3 → ℝ) (hp : unitVec3 p) : rot90p p p = p := by
  dsimp [rot90p]
  have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
  have hself : cross p p = 0 := by ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring
  rw [hpp, hself]
  simp

/-- The symmetrization at the pole: `g p = 2·f p`. -/
theorem symm_eq_pole (p : Fin 3 → ℝ) (hp : unitVec3 p) (f : (Fin 3 → ℝ) → ℝ) :
    symm p f p = 2 * f p := by
  dsimp [symm]
  rw [rot90p_pole p hp]
  ring

/-- **The symmetrization difference** `g x − g(ρx) = f x − f(ρ²x)` — the relation
the recover-`f` step uses (a 180° rotation as `ρ²`). -/
theorem symm_sub_rot90 (p : Fin 3 → ℝ) (f : (Fin 3 → ℝ) → ℝ) (x : Fin 3 → ℝ) :
    symm p f x - symm p f (rot90p p x) = f x - f (rot90p p (rot90p p x)) := by
  dsimp [symm]
  ring

/-- **From `g` latitude-invariant, `f` is 180°-longitude invariant**: if the
symmetrization depends only on `(t·p)²`, then `f x = f(ρ²x)` (since `ρ` preserves
the projection and `g x − g(ρx) = f x − f(ρ²x)`). The key recover-`f` step. -/
theorem f_rho2_inv_of_g_lat_inv (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ)
    (hg_lat : ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p) ^ 2 = (dotProduct t' p) ^ 2 →
      symm p f t = symm p f t')
    (x : Fin 3 → ℝ) (hx : unitVec3 x) :
    f x = f (rot90p p (rot90p p x)) := by
  have hρx : unitVec3 (rot90p p x) := by simpa [unitVec3, rot90p_orthogonal p x x hp] using hx
  have hproj : (dotProduct x p) ^ 2 = (dotProduct (rot90p p x) p) ^ 2 := by
    rw [rot90p_preserves_proj p x hp]
  have hg : symm p f x = symm p f (rot90p p x) := hg_lat x (rot90p p x) hx hρx hproj
  have hdiff := symm_sub_rot90 p f x
  have hzero : symm p f x - symm p f (rot90p p x) = 0 := by linarith [hg]
  rw [hzero] at hdiff
  linarith

/-- **The symmetrization is a weight-2 frame function**: `Σ g(eᵢ) = 2` over every
orthonormal basis (since `ρ` is orthogonal, `{ρeᵢ}` is again a frame). -/
theorem symm_is_frame (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f) :
    ∀ e1 e2 e3, unitVec3 e1 → unitVec3 e2 → unitVec3 e3 →
      orthVec3 e1 e2 → orthVec3 e1 e3 → orthVec3 e2 e3 →
      symm p f e1 + symm p f e2 + symm p f e3 = 2 := by
  intro e1 e2 e3 h1 h2 h3 h12 h13 h23
  have hρ1 : unitVec3 (rot90p p e1) := by
    simpa [unitVec3, rot90p_orthogonal p e1 e1 hp] using h1
  have hρ2 : unitVec3 (rot90p p e2) := by
    simpa [unitVec3, rot90p_orthogonal p e2 e2 hp] using h2
  have hρ3 : unitVec3 (rot90p p e3) := by
    simpa [unitVec3, rot90p_orthogonal p e3 e3 hp] using h3
  have hρ12 : orthVec3 (rot90p p e1) (rot90p p e2) := by
    simpa [orthVec3, rot90p_orthogonal p e1 e2 hp] using h12
  have hρ13 : orthVec3 (rot90p p e1) (rot90p p e3) := by
    simpa [orthVec3, rot90p_orthogonal p e1 e3 hp] using h13
  have hρ23 : orthVec3 (rot90p p e2) (rot90p p e3) := by
    simpa [orthVec3, rot90p_orthogonal p e2 e3 hp] using h23
  have hf0 : f e1 + f e2 + f e3 = 1 := hf e1 e2 e3 h1 h2 h3 h12 h13 h23
  have hfρ : f (rot90p p e1) + f (rot90p p e2) + f (rot90p p e3) = 1 :=
    hf (rot90p p e1) (rot90p p e2) (rot90p p e3) hρ1 hρ2 hρ3 hρ12 hρ13 hρ23
  dsimp [symm]
  linarith

/-- **The 2D additivity for the symmetrization** `g = f + f∘ρ`: for unit `u ⊥ v`
and `α² + β² = 1`, `g(αu + βv) + g(−βu + αv) = g u + g v`. (The weight-2 version
of `two_dim_additivity`, the prerequisite for the transport/great-circle argument.) -/
theorem symm_two_dim_additivity (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v) (horth : orthVec3 u v)
    (α β : ℝ) (hαβ : α ^ 2 + β ^ 2 = 1) :
    symm p f (α • u + β • v) + symm p f ((-β) • u + α • v) = symm p f u + symm p f v := by
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
  have hframe1 : symm p f w + symm p f w' + symm p f z = 2 :=
    symm_is_frame p hp f hf w w' z hw_unit hw'_unit hz_unit hw_orth hz_orth_w hz_orth_w'
  have hframe2 : symm p f u + symm p f v + symm p f z = 2 :=
    symm_is_frame p hp f hf u v z hu hv hz_unit horth (cross_orth_left u v) (cross_orth_right u v)
  linarith

/-- **The transport for `g`** — the increment is invariant under the 90° rotation
of its straddle axis: `g(a·u+b·v) − g(a·u−b·v) = g(b·u+a·v) − g(−b·u+a·v)`. The
key observation behind Richman–Bridges' oscillation transfer. -/
theorem symm_transport (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v) (horth : orthVec3 u v)
    (a b : ℝ) (hαβ : a ^ 2 + b ^ 2 = 1) :
    symm p f (a • u + b • v) - symm p f (a • u + (-b) • v)
      = symm p f (b • u + a • v) - symm p f ((-b) • u + a • v) := by
  have h1 := symm_two_dim_additivity p hp f hf u v hu hv horth a b hαβ
  have h2 := symm_two_dim_additivity p hp f hf u v hu hv horth a (-b) (by simpa [sq] using hαβ)
  rw [show -(-b) = b by ring] at h2
  nlinarith [h1, h2]

/-- The symmetrization is nonnegative when `f` is (on unit vectors). -/
theorem symm_nonneg (p x : Fin 3 → ℝ) (hp : unitVec3 p) (hx : unitVec3 x)
    (f : (Fin 3 → ℝ) → ℝ) (hpos : ∀ y, unitVec3 y → 0 ≤ f y) :
    0 ≤ symm p f x := by
  dsimp [symm]
  have hρx : unitVec3 (rot90p p x) := by simpa [unitVec3, rot90p_orthogonal p x x hp] using hx
  nlinarith [hpos x hx, hpos (rot90p p x) hρx]

/-- The symmetrization is bounded: `0 ≤ g x ≤ 2` (for a nonnegative frame function). -/
theorem symm_bounded (p x : Fin 3 → ℝ) (hp : unitVec3 p) (hx : unitVec3 x)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ y, unitVec3 y → 0 ≤ f y) :
    0 ≤ symm p f x ∧ symm p f x ≤ 2 := by
  constructor
  · exact symm_nonneg p x hp hx f hpos
  · have hρx : unitVec3 (rot90p p x) := by simpa [unitVec3, rot90p_orthogonal p x x hp] using hx
    have hfx : f x ≤ 1 := frameFunction3_bounded f hf hpos x hx
    have hfρx : f (rot90p p x) ≤ 1 := frameFunction3_bounded f hf hpos (rot90p p x) hρx
    dsimp [symm]
    linarith

/-- The symmetrization's value on the equator (`e ⊥ p`) is `1 − f p`. -/
theorem symm_eq_equator (p : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (e : Fin 3 → ℝ) (he : unitVec3 e) (hep : orthVec3 e p) :
    symm p f e = 1 - f p := by
  dsimp [symm]
  have hep' : dotProduct e p = 0 := by simpa [orthVec3] using hep
  have hρe : rot90p p e = cross p e := by
    dsimp [rot90p]
    rw [hep']
    simp
  rw [hρe]
  exact symmetrization_equator_constant p hp f hf e he hep

/-- **The upper bound `g t ≤ 1 + f p`** — from the weight-2 frame property
(`g t + g q + g n = 2`), nonnegativity (`g n ≥ 0`), and the equator value
(`g q = 1 − f p`). This supplies the monotonicity_bound hypothesis. -/
theorem symm_le_bound (p q n t : Fin 3 → ℝ) (hp : unitVec3 p)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ y, unitVec3 y → 0 ≤ f y)
    (hq : unitVec3 q) (hn : unitVec3 n) (ht : unitVec3 t)
    (htq : orthVec3 t q) (htn : orthVec3 t n) (hqn : orthVec3 q n)
    (hqp : orthVec3 q p) :
    symm p f t ≤ 1 + f p := by
  have hframe : symm p f t + symm p f q + symm p f n = 2 :=
    symm_is_frame p hp f hf t q n ht hq hn htq htn hqn
  have heq : symm p f q = 1 - f p := symm_eq_equator p hp f hf q hq hqp
  have hnn : 0 ≤ symm p f n := symm_nonneg p n hp hn f hpos
  linarith

/-- **The great-circle identity (★)** — for a weight-2 frame function `g`, if
`{r,q,n}` and `{s,t,n}` are orthonormal triples sharing the normal `n`, then
`g r + g q = g s + g t`. This is the identity behind Richman–Bridges' monotonicity
lemma (their Lemma 16). -/
theorem weight2_frame_relation (g : (Fin 3 → ℝ) → ℝ)
    (hg : ∀ e1 e2 e3, unitVec3 e1 → unitVec3 e2 → unitVec3 e3 →
      orthVec3 e1 e2 → orthVec3 e1 e3 → orthVec3 e2 e3 → g e1 + g e2 + g e3 = 2)
    (r q n s t : Fin 3 → ℝ)
    (hr : unitVec3 r) (hq : unitVec3 q) (hn : unitVec3 n)
    (hs : unitVec3 s) (ht : unitVec3 t)
    (h12 : orthVec3 r q) (h13 : orthVec3 r n) (h23 : orthVec3 q n)
    (h12' : orthVec3 s t) (h13' : orthVec3 s n) (h23' : orthVec3 t n) :
    g r + g q = g s + g t := by
  have h1 : g r + g q + g n = 2 := hg r q n hr hq hn h12 h13 h23
  have h2 : g s + g t + g n = 2 := hg s t n hs ht hn h12' h13' h23'
  linarith

/-- **The monotonicity bound** (abstract form of Richman–Bridges' Lemma 16). From
the identity `g r + g q = g s + g t`, the equator value `g q = 1 − f p`, and the
upper bound `g t ≤ 1 + f p` (from `g ≥ 0` and `g t + g q + g n = 2`), we get
`g r ≤ g s + 2·f p`. -/
theorem monotonicity_bound (g : (Fin 3 → ℝ) → ℝ) (f : (Fin 3 → ℝ) → ℝ)
    (r q s t : Fin 3 → ℝ) (p : Fin 3 → ℝ)
    (h_identity : g r + g q = g s + g t)
    (h_eq : g q = 1 - f p) (h_bound : g t ≤ 1 + f p) :
    g r ≤ g s + 2 * f p := by
  linarith [h_identity, h_eq, h_bound]

/-- **The great-circle frames.** For the great circle with normal `n` and a point `q` on it
(`q ⊥ n`), let `r = n×q`. For any `φ`, the points `s = cos φ·q + sin φ·r` and
`t = −sin φ·q + cos φ·r` give two orthonormal triples `{r,q,n}` and `{s,t,n}` (all eight
unit/orthogonality facts at once). -/
theorem great_circle_frames (q n : Fin 3 → ℝ) (hq : unitVec3 q) (hn : unitVec3 n) (hqn : orthVec3 q n)
    (φ : ℝ) :
    let r := cross n q
    let s := Real.cos φ • q + Real.sin φ • r
    let t := -Real.sin φ • q + Real.cos φ • r
    unitVec3 r ∧ orthVec3 r q ∧ orthVec3 r n ∧
    unitVec3 s ∧ unitVec3 t ∧ orthVec3 s t ∧ orthVec3 s n ∧ orthVec3 t n := by
  intro r s t
  have hnr : orthVec3 n q := by simpa [orthVec3, dotProduct_symm] using hqn
  have hr_unit : unitVec3 r := cross_unit n q hn hq hnr
  have hrq : orthVec3 r q := by simpa [orthVec3, dotProduct_symm] using cross_orth_right n q
  have hrn : orthVec3 r n := by simpa [orthVec3, dotProduct_symm] using cross_orth_left n q
  have hqr : dotProduct q r = 0 := by
    rw [dotProduct_symm q r]
    exact hrq
  have hs_unit : unitVec3 s := by
    change dotProduct (Real.cos φ • q + Real.sin φ • r) (Real.cos φ • q + Real.sin φ • r) = 1
    rw [dotProduct_expand q r (Real.cos φ) (Real.sin φ)]
    rw [hq, hr_unit, hqr]
    nlinarith [Real.sin_sq_add_cos_sq φ]
  have ht_unit : unitVec3 t := by
    change dotProduct (-Real.sin φ • q + Real.cos φ • r) (-Real.sin φ • q + Real.cos φ • r) = 1
    rw [dotProduct_expand q r (-Real.sin φ) (Real.cos φ)]
    rw [hq, hr_unit, hqr]
    nlinarith [Real.sin_sq_add_cos_sq φ]
  have hst : orthVec3 s t := by
    change dotProduct (Real.cos φ • q + Real.sin φ • r) (-Real.sin φ • q + Real.cos φ • r) = 0
    rw [dotProduct_expand_mixed q r (Real.cos φ) (Real.sin φ)]
    rw [hq, hr_unit, hqr]
    ring
  have hsn : orthVec3 s n := by
    change dotProduct (Real.cos φ • q + Real.sin φ • r) n = 0
    rw [dotProduct_add_smul q r n (Real.cos φ) (Real.sin φ)]
    rw [hqn, hrn]
    ring
  have htn : orthVec3 t n := by
    change dotProduct (-Real.sin φ • q + Real.cos φ • r) n = 0
    rw [dotProduct_add_smul q r n (-Real.sin φ) (Real.cos φ)]
    rw [hqn, hrn]
    ring
  exact ⟨hr_unit, hrq, hrn, hs_unit, ht_unit, hst, hsn, htn⟩

/-- **The transport** — an increment is invariant under the 90° rotation of its
straddle axis: for unit `u ⊥ v`, `a² + b² = 1`,
`f(a·u + b·v) − f(a·u − b·v) = f(b·u + a·v) − f(−b·u + a·v)`. The continuity
estimate iterates this. -/
theorem transport (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v) (horth : orthVec3 u v)
    (a b : ℝ) (hαβ : a ^ 2 + b ^ 2 = 1) :
    f (a • u + b • v) - f (a • u + (-b) • v) = f (b • u + a • v) - f ((-b) • u + a • v) := by
  have h1 := two_dim_additivity f hf u v hu hv horth a b hαβ
  have h2 := two_dim_additivity f hf u v hu hv horth a (-b) (by simpa [sq] using hαβ)
  rw [show -(-b) = b by ring] at h2
  nlinarith [h1, h2]

/-- The squared norm. -/
def normSq (v : Fin 3 → ℝ) : ℝ := dotProduct v v

/-- `normSq (c • v) = c² · normSq v`. -/
theorem normSq_smul (c : ℝ) (v : Fin 3 → ℝ) : normSq (c • v) = c ^ 2 * normSq v := by
  dsimp [normSq]
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- The homogeneous extension `F(v) = ‖v‖²·f(v/‖v‖)` (defined for all `v`, since
`F 0 = 0`). -/
noncomputable def extend (f : (Fin 3 → ℝ) → ℝ) : (Fin 3 → ℝ) → ℝ :=
  fun v => normSq v * f ((Real.sqrt (normSq v))⁻¹ • v)

/-- `√(c²·a) = |c|·√a` for `a ≥ 0` — the scalar fact the extension's homogeneity
turns on. -/
theorem sqrt_smul (c : ℝ) (a : ℝ) (ha : 0 ≤ a) :
    Real.sqrt (c ^ 2 * a) = |c| * Real.sqrt a := by
  rw [Real.sqrt_eq_iff_eq_sq (mul_nonneg (sq_nonneg c) ha) (mul_nonneg (abs_nonneg c) (Real.sqrt_nonneg a))]
  conv_lhs => rw [← sq_abs, ← Real.sq_sqrt ha, ← mul_pow]

/-- `normSq v = 0 ↔ v = 0` (the squared norm is nondegenerate). -/
theorem normSq_eq_zero_iff (v : Fin 3 → ℝ) : normSq v = 0 ↔ v = 0 := by
  constructor
  · intro h
    ext i
    have hsum : v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2 = 0 := by
      simpa [normSq, dotProduct, Fin.sum_univ_three, sq] using h
    fin_cases i
    · have hle : v 0 ^ 2 ≤ 0 := by nlinarith [hsum, sq_nonneg (v 1), sq_nonneg (v 2)]
      exact sq_eq_zero_iff.mp (le_antisymm hle (sq_nonneg (v 0)))
    · have hle : v 1 ^ 2 ≤ 0 := by nlinarith [hsum, sq_nonneg (v 0), sq_nonneg (v 2)]
      exact sq_eq_zero_iff.mp (le_antisymm hle (sq_nonneg (v 1)))
    · have hle : v 2 ^ 2 ≤ 0 := by nlinarith [hsum, sq_nonneg (v 0), sq_nonneg (v 1)]
      exact sq_eq_zero_iff.mp (le_antisymm hle (sq_nonneg (v 2)))
  · intro h
    subst h
    simp [normSq, dotProduct, Fin.sum_univ_three]

/-- `√(normSq v) ≠ 0` for `v ≠ 0`. -/
theorem sqrt_normSq_ne_zero (v : Fin 3 → ℝ) (hv : v ≠ 0) :
    Real.sqrt (normSq v) ≠ 0 := by
  intro hz
  have hnonneg : 0 ≤ normSq v := by
    dsimp [normSq]; simp [dotProduct, Fin.sum_univ_three]
    nlinarith [sq_nonneg (v 0), sq_nonneg (v 1), sq_nonneg (v 2)]
  have hz' : normSq v = 0 := by
    rw [← Real.sq_sqrt hnonneg]
    rw [hz]
    norm_num
  exact hv ((normSq_eq_zero_iff v).1 hz')

/-- `(√(normSq v))⁻¹ • v` is a unit vector (for `v ≠ 0`). -/
theorem unit_smul_inv_sqrt (v : Fin 3 → ℝ) (hv : v ≠ 0) :
    unitVec3 ((Real.sqrt (normSq v))⁻¹ • v) := by
  have hnonneg : 0 ≤ normSq v := by
    dsimp [normSq]; simp [dotProduct, Fin.sum_univ_three]
    nlinarith [sq_nonneg (v 0), sq_nonneg (v 1), sq_nonneg (v 2)]
  have hne : Real.sqrt (normSq v) ≠ 0 := sqrt_normSq_ne_zero v hv
  dsimp [unitVec3]
  change normSq ((Real.sqrt (normSq v))⁻¹ • v) = 1
  rw [normSq_smul]
  field_simp [hne]
  rw [Real.sq_sqrt hnonneg]

/-- `(c·a)⁻¹·c = a⁻¹` for nonzero `c`, `a`. -/
theorem inv_mul_self_eq (c a : ℝ) (hc : c ≠ 0) (ha : a ≠ 0) :
    (c * a)⁻¹ * c = a⁻¹ := by
  field_simp [hc, ha]

/-- The extension is even: `F(−v) = F v` (from the frame function's evenness). -/
theorem extend_even (f : (Fin 3 → ℝ) → ℝ)
    (hf_even : ∀ v, unitVec3 v → f (-v) = f v) :
    ∀ v, extend f (-v) = extend f v := by
  intro v
  dsimp [extend]
  have hsq : normSq (-v) = normSq v := by
    dsimp [normSq]
    simp [dotProduct, Fin.sum_univ_three]
  rw [hsq]
  by_cases hv : v = 0
  · subst hv
    simp [normSq, dotProduct, Fin.sum_univ_three]
  · have hunit : unitVec3 ((Real.sqrt (normSq v))⁻¹ • v) := unit_smul_inv_sqrt v hv
    have hneg : (Real.sqrt (normSq v))⁻¹ • (-v) = -((Real.sqrt (normSq v))⁻¹ • v) := by
      ext i
      simp [neg_smul, mul_neg]
    rw [hneg, hf_even ((Real.sqrt (normSq v))⁻¹ • v) hunit]

/-- **The extension is homogeneous** — `F(c·v) = c²·F(v)` (the `H` that step 1
consumes), using the evenness for the `c < 0` case. -/
theorem extend_homogeneous (f : (Fin 3 → ℝ) → ℝ)
    (hf_even : ∀ v, unitVec3 v → f (-v) = f v) :
    ∀ (c : ℝ) (v : Fin 3 → ℝ), extend f (c • v) = c ^ 2 * extend f v := by
  intro c v
  have h_nonneg : ∀ (d : ℝ), 0 ≤ d → extend f (d • v) = d ^ 2 * extend f v := by
    intro d hd
    by_cases hv : v = 0
    · subst hv
      simp [extend, normSq, dotProduct, Fin.sum_univ_three]
    · dsimp [extend]
      rw [normSq_smul d v]
      have hsq_nonneg : 0 ≤ normSq v := by
        dsimp [normSq]; simp [dotProduct, Fin.sum_univ_three]
        nlinarith [sq_nonneg (v 0), sq_nonneg (v 1), sq_nonneg (v 2)]
      have hsqrt : Real.sqrt (d ^ 2 * normSq v) = d * Real.sqrt (normSq v) := by
        simpa [abs_of_nonneg hd] using sqrt_smul d (normSq v) hsq_nonneg
      rw [hsqrt]
      by_cases hd0 : d = 0
      · subst hd0
        simp [normSq, dotProduct, Fin.sum_univ_three]
      · have hscal : (d * Real.sqrt (normSq v))⁻¹ • (d • v) = (Real.sqrt (normSq v))⁻¹ • v := by
          ext i
          have hsc : (d * Real.sqrt (normSq v))⁻¹ * d = (Real.sqrt (normSq v))⁻¹ :=
            inv_mul_self_eq d (Real.sqrt (normSq v)) hd0 (sqrt_normSq_ne_zero v hv)
          calc
            ((d * Real.sqrt (normSq v))⁻¹ • (d • v)) i
                = (d * Real.sqrt (normSq v))⁻¹ * (d * v i) := by simp
            _ = ((d * Real.sqrt (normSq v))⁻¹ * d) * v i := by ring
            _ = (Real.sqrt (normSq v))⁻¹ * v i := by rw [hsc]
            _ = ((Real.sqrt (normSq v))⁻¹ • v) i := by simp
        rw [hscal]
        ring
  by_cases hcpos : 0 ≤ c
  · exact h_nonneg c hcpos
  · have hcneg : c = -|c| := by rw [abs_of_neg (lt_of_not_ge hcpos)]; ring
    rw [hcneg, neg_smul, extend_even f hf_even]
    rw [neg_sq]
    exact h_nonneg |c| (abs_nonneg c)

/-- Bilinear expansion of `(αu + βv + γw) · (αu + βv + γw)`. -/
theorem dotProduct_expand_three (u v w : Fin 3 → ℝ) (α β γ : ℝ) :
    dotProduct (α • u + β • v + γ • w) (α • u + β • v + γ • w)
    = α ^ 2 * dotProduct u u + β ^ 2 * dotProduct v v + γ ^ 2 * dotProduct w w
      + 2 * α * β * dotProduct u v + 2 * α * γ * dotProduct u w + 2 * β * γ * dotProduct v w := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- Linearity of `(αu + βv + γw) · z` in `(α, β, γ)`. -/
theorem dotProduct_add_smul_three (u v w z : Fin 3 → ℝ) (α β γ : ℝ) :
    dotProduct (α • u + β • v + γ • w) z = α * dotProduct u z + β * dotProduct v z + γ * dotProduct w z := by
  simp [dotProduct, Fin.sum_univ_three]
  ring

/-- **Realizability** (the dim-≥-3 step): for unit `p` and `a + b + c = 1`
(nonnegative), there is an orthonormal triple whose squared projections onto `p`
are exactly `a, b, c`. -/
theorem realize (p : Fin 3 → ℝ) (hp : unitVec3 p) (a b c : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (habc : a + b + c = 1) :
    ∃ t1 t2 t3, unitVec3 t1 ∧ unitVec3 t2 ∧ unitVec3 t3 ∧
      orthVec3 t1 t2 ∧ orthVec3 t1 t3 ∧ orthVec3 t2 t3 ∧
      (dotProduct t1 p) ^ 2 = a ∧ (dotProduct t2 p) ^ 2 = b ∧ (dotProduct t3 p) ^ 2 = c := by
  rcases exists_perp p hp with ⟨q, hq, hpq⟩
  by_cases ha1 : a = 1
  · refine ⟨p, q, cross p q, hp, hq, cross_unit p q hp hq hpq, hpq, cross_orth_left p q, cross_orth_right p q, ?_, ?_, ?_⟩
    · have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
      simp [hpp, ha1]
    · have hqp : dotProduct q p = 0 := by rw [dotProduct_symm]; simpa [orthVec3] using hpq
      have hb0 : b = 0 := by nlinarith [habc, ha1, hb]
      simp [hqp, hb0]
    · have hcp : dotProduct (cross p q) p = 0 := by
        rw [dotProduct_symm]
        simpa [orthVec3] using cross_orth_left p q
      have hc0 : c = 0 := by nlinarith [habc, ha1, hc]
      simp [hcp, hc0]
  · have ha_lt1 : a < 1 := lt_of_le_of_ne (by linarith [ha, habc, hb, hc]) ha1
    let t1 := Real.sqrt a • p + Real.sqrt (1 - a) • q
    let t2 := Real.sqrt b • p + (-(Real.sqrt a * Real.sqrt b / Real.sqrt (1 - a))) • q + (Real.sqrt c / Real.sqrt (1 - a)) • (cross p q)
    let t3 := cross t1 t2
    have ht1 : unitVec3 t1 ∧ (dotProduct t1 p) ^ 2 = a := unit_smul_of_latitude p q hp hq hpq a ha (by linarith)
    have ht2_unit : unitVec3 t2 := by
      rw [unitVec3]
      dsimp [t2]
      rw [dotProduct_expand_three p q (cross p q) (Real.sqrt b) (-(Real.sqrt a * Real.sqrt b / Real.sqrt (1 - a))) (Real.sqrt c / Real.sqrt (1 - a))]
      have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
      have hqq : dotProduct q q = 1 := by simpa [unitVec3] using hq
      have hrr : dotProduct (cross p q) (cross p q) = 1 := by simpa [unitVec3] using cross_unit p q hp hq hpq
      have hpq' : dotProduct p q = 0 := by simpa [orthVec3] using hpq
      have hpr : dotProduct p (cross p q) = 0 := by simpa [orthVec3] using cross_orth_left p q
      have hqr : dotProduct q (cross p q) = 0 := by simpa [orthVec3] using cross_orth_right p q
      rw [hpp, hqq, hrr, hpq', hpr, hqr]
      have ha_sq : (Real.sqrt a) ^ 2 = a := Real.sq_sqrt ha
      have hb_sq : (Real.sqrt b) ^ 2 = b := Real.sq_sqrt hb
      have hc_sq : (Real.sqrt c) ^ 2 = c := Real.sq_sqrt hc
      have h1a_sq : (Real.sqrt (1 - a)) ^ 2 = 1 - a := Real.sq_sqrt (by linarith)
      have hab_c : a * b + c = (1 - a) * (1 - b) := by nlinarith [habc]
      ring_nf
      field_simp [show (1 - a) ≠ 0 by linarith]
      nlinarith [ha_sq, hb_sq, hc_sq, h1a_sq, hab_c]
    have ht2_p : (dotProduct t2 p) ^ 2 = b := by
      dsimp [t2]
      have h : dotProduct t2 p = Real.sqrt b := by
        rw [dotProduct_add_smul_three p q (cross p q) p (Real.sqrt b) (-(Real.sqrt a * Real.sqrt b / Real.sqrt (1 - a))) (Real.sqrt c / Real.sqrt (1 - a))]
        have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
        have hqp : dotProduct q p = 0 := by rw [dotProduct_symm]; simpa [orthVec3] using hpq
        have hrp : dotProduct (cross p q) p = 0 := by rw [dotProduct_symm]; simpa [orthVec3] using cross_orth_left p q
        rw [hpp, hqp, hrp]
        ring
      rw [h]
      exact Real.sq_sqrt hb
    have ht2_orth : orthVec3 t2 t1 := by
      rw [orthVec3]
      dsimp [t2]
      rw [dotProduct_add_smul_three p q (cross p q) t1 (Real.sqrt b) (-(Real.sqrt a * Real.sqrt b / Real.sqrt (1 - a))) (Real.sqrt c / Real.sqrt (1 - a))]
      have hpt1 : dotProduct p t1 = Real.sqrt a := by
        rw [dotProduct_symm]
        dsimp [t1]
        rw [dotProduct_add_smul p q p (Real.sqrt a) (Real.sqrt (1 - a))]
        have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
        have hqp : dotProduct q p = 0 := by rw [dotProduct_symm]; simpa [orthVec3] using hpq
        rw [hpp, hqp]
        ring
      have hqt1 : dotProduct q t1 = Real.sqrt (1 - a) := by
        rw [dotProduct_symm]
        dsimp [t1]
        rw [dotProduct_add_smul p q q (Real.sqrt a) (Real.sqrt (1 - a))]
        have hpq' : dotProduct p q = 0 := by simpa [orthVec3] using hpq
        have hqq : dotProduct q q = 1 := by simpa [unitVec3] using hq
        rw [hpq', hqq]
        ring
      have hrt1 : dotProduct (cross p q) t1 = 0 := by
        rw [dotProduct_symm]
        dsimp [t1]
        rw [dotProduct_add_smul p q (cross p q) (Real.sqrt a) (Real.sqrt (1 - a))]
        have hpr : dotProduct p (cross p q) = 0 := by simpa [orthVec3] using cross_orth_left p q
        have hqr : dotProduct q (cross p q) = 0 := by simpa [orthVec3] using cross_orth_right p q
        rw [hpr, hqr]
        ring
      rw [hpt1, hqt1, hrt1]
      field_simp [show Real.sqrt (1 - a) ≠ 0 by positivity]
      ring
    have ht2_orth' : orthVec3 t1 t2 := by
      simpa [orthVec3, dotProduct_symm] using ht2_orth
    have ht3_unit : unitVec3 t3 := cross_unit t1 t2 ht1.1 ht2_unit ht2_orth'
    have ht3_orth1 : orthVec3 t1 t3 := by dsimp [t3]; exact cross_orth_left t1 t2
    have ht3_orth2 : orthVec3 t2 t3 := by dsimp [t3]; exact cross_orth_right t1 t2
    have ht3_p : (dotProduct t3 p) ^ 2 = c := by
      dsimp [t3]
      have hparseval := parseval t1 t2 p ht1.1 ht2_unit ht2_orth'
      -- (t1·p)² + (t2·p)² + (t3·p)² = p·p = 1, and (t1·p)² = a, (t2·p)² = b
      have hpp : dotProduct p p = 1 := by simpa [unitVec3] using hp
      rw [hpp] at hparseval
      rw [ht1.2, ht2_p] at hparseval
      nlinarith [hparseval, habc]
    refine ⟨t1, t2, t3, ht1.1, ht2_unit, ht3_unit, ht2_orth', ht3_orth1, ht3_orth2, ht1.2, ht2_p, ht3_p⟩

/-- Cauchy–Schwarz for unit vectors: `(u·v)² ≤ 1`. -/
theorem sq_dot_le_one_of_unit (u v : Fin 3 → ℝ) (hu : unitVec3 u) (hv : unitVec3 v) :
    (dotProduct u v) ^ 2 ≤ 1 := by
  have hcs : (dotProduct u u) * (dotProduct v v) - (dotProduct u v) ^ 2
      = (u 0 * v 1 - u 1 * v 0) ^ 2 + (u 0 * v 2 - u 2 * v 0) ^ 2 + (u 1 * v 2 - u 2 * v 1) ^ 2 := by
    simp [dotProduct, Fin.sum_univ_three]
    ring
  have hnonneg : 0 ≤ (dotProduct u u) * (dotProduct v v) - (dotProduct u v) ^ 2 := by
    rw [hcs]
    nlinarith [sq_nonneg (u 0 * v 1 - u 1 * v 0), sq_nonneg (u 0 * v 2 - u 2 * v 0), sq_nonneg (u 1 * v 2 - u 2 * v 1)]
  have hu' : dotProduct u u = 1 := by simpa [unitVec3] using hu
  have hv' : dotProduct v v = 1 := by simpa [unitVec3] using hv
  nlinarith [hnonneg, hu', hv']

/-- **Constant-on-latitudes for `g`** (conditional on its latitude invariance): if
the symmetrization depends only on `(t·p)²`, then it is affine in it,
`g t = (3·f p − 1)·(t·p)² + (1 − f p)`. The recursion (`affine_of_triple_sum`)
applied to `F(a) = g(√a·p + √(1−a)·q)` via the realizability. -/
theorem symm_latitude_affine (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x)
    (hg_lat : ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p) ^ 2 = (dotProduct t' p) ^ 2 → symm p f t = symm p f t') :
    ∀ t, unitVec3 t → symm p f t = (3 * f p - 1) * (dotProduct t p) ^ 2 + (1 - f p) := by
  let F : ℝ → ℝ := fun a => symm p f (Real.sqrt a • p + Real.sqrt (1 - a) • q)
  have hF_bounded : ∃ M : ℝ, ∀ a, 0 ≤ a → a ≤ 1 → |F a| ≤ M := by
    refine ⟨2, ?_⟩
    intro a ha ha1
    have hta : unitVec3 (Real.sqrt a • p + Real.sqrt (1 - a) • q) :=
      (unit_smul_of_latitude p q hp hq hpq a ha ha1).1
    have hb := symm_bounded p (Real.sqrt a • p + Real.sqrt (1 - a) • q) hp hta f hf hpos
    dsimp [F]
    rw [abs_of_nonneg hb.1]
    exact hb.2
  have hF : ∀ a b c, 0 ≤ a → 0 ≤ b → 0 ≤ c → a + b + c = 1 → F a + F b + F c = F 1 + 2 * F 0 := by
    intro a b c ha hb hc habc
    rcases realize p hp a b c ha hb hc habc with ⟨t1, t2, t3, ht1, ht2, ht3, h12, h13, h23, hp1, hp2, hp3⟩
    have hFa : F a = symm p f t1 := by
      dsimp [F]
      exact hg_lat _ t1 (unit_smul_of_latitude p q hp hq hpq a ha (by linarith)).1 ht1
        (by rw [(unit_smul_of_latitude p q hp hq hpq a ha (by linarith)).2, hp1])
    have hFb : F b = symm p f t2 := by
      dsimp [F]
      exact hg_lat _ t2 (unit_smul_of_latitude p q hp hq hpq b hb (by linarith)).1 ht2
        (by rw [(unit_smul_of_latitude p q hp hq hpq b hb (by linarith)).2, hp2])
    have hFc : F c = symm p f t3 := by
      dsimp [F]
      exact hg_lat _ t3 (unit_smul_of_latitude p q hp hq hpq c hc (by linarith)).1 ht3
        (by rw [(unit_smul_of_latitude p q hp hq hpq c hc (by linarith)).2, hp3])
    have hframe : symm p f t1 + symm p f t2 + symm p f t3 = 2 :=
      symm_is_frame p hp f hf t1 t2 t3 ht1 ht2 ht3 h12 h13 h23
    have hF1 : F 1 = 2 * f p := by dsimp [F]; simpa [Real.sqrt_one, Real.sqrt_zero] using (symm_eq_pole p hp f)
    have hF0 : F 0 = 1 - f p := by dsimp [F]; simpa [Real.sqrt_one, Real.sqrt_zero] using (symm_eq_equator p hp f hf q hq (by simpa [orthVec3, dotProduct_symm] using hpq))
    rw [hFa, hFb, hFc, hF1, hF0]
    linarith [hframe]
  have hFlin := Cauchy.affine_of_triple_sum F hF hF_bounded
  have hF1 : F 1 = 2 * f p := by dsimp [F]; simpa [Real.sqrt_one, Real.sqrt_zero] using (symm_eq_pole p hp f)
  have hF0 : F 0 = 1 - f p := by dsimp [F]; simpa [Real.sqrt_one, Real.sqrt_zero] using (symm_eq_equator p hp f hf q hq (by simpa [orthVec3, dotProduct_symm] using hpq))
  intro t ht
  have hproj_nonneg : 0 ≤ (dotProduct t p) ^ 2 := sq_nonneg _
  have hproj_le : (dotProduct t p) ^ 2 ≤ 1 := sq_dot_le_one_of_unit t p ht hp
  have hFt := hFlin ((dotProduct t p) ^ 2) hproj_nonneg hproj_le
  have hF_eq : F ((dotProduct t p) ^ 2) = symm p f t := by
    dsimp [F]
    apply hg_lat
    · exact (unit_smul_of_latitude p q hp hq hpq ((dotProduct t p) ^ 2) hproj_nonneg hproj_le).1
    · exact ht
    · rw [(unit_smul_of_latitude p q hp hq hpq ((dotProduct t p) ^ 2) hproj_nonneg hproj_le).2]
  rw [← hF_eq, hFt, hF1, hF0]
  ring

/-- **The recover-`f` key relation.** For `Q` the quadratic matching `f` at `p, q, p×q`
and `f' = f − Q`, if `g = f + f∘ρ` is latitude-invariant then `f'(t) + f'(ρt) = 0`
(since `g = f + f∘ρ = Q + Q∘ρ`). -/
theorem f_minus_Q_antisymm (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x)
    (hg_lat : ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p) ^ 2 = (dotProduct t' p) ^ 2 → symm p f t = symm p f t')
    (t : Fin 3 → ℝ) (ht : unitVec3 t) :
    (f t - (f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2))
      + (f (rot90p p t) - (f p * (dotProduct (rot90p p t) p) ^ 2 + f q * (dotProduct (rot90p p t) q) ^ 2 + f (cross p q) * (dotProduct (rot90p p t) (cross p q)) ^ 2)) = 0 := by
  let Q : (Fin 3 → ℝ) → ℝ := fun x => f p * (dotProduct x p) ^ 2 + f q * (dotProduct x q) ^ 2 + f (cross p q) * (dotProduct x (cross p q)) ^ 2
  change (f t - Q t) + (f (rot90p p t) - Q (rot90p p t)) = 0
  have hg : symm p f t = (3 * f p - 1) * (dotProduct t p) ^ 2 + (1 - f p) :=
    symm_latitude_affine p q hp hq hpq f hf hpos hg_lat t ht
  have hQ : Q t + Q (rot90p p t) = (3 * f p - 1) * (dotProduct t p) ^ 2 + (1 - f p) := by
    simpa [Q] using (quadratic_symm p q hp hq hpq f hf t ht)
  dsimp [symm] at hg
  rw [← hQ] at hg
  nlinarith [hg]

/-- **`f' = f − Q` is 180°-invariant** (`f'(t) = f'(ρ²t)`), since both `f` (via
`f_rho2_inv_of_g_lat_inv`) and `Q` (via `rot90p_sq_proj`) are. -/
theorem f_prime_rho2_inv (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x)
    (hg_lat : ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p) ^ 2 = (dotProduct t' p) ^ 2 → symm p f t = symm p f t')
    (t : Fin 3 → ℝ) (ht : unitVec3 t) :
    (f t - (f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2))
      = (f (rot90p p (rot90p p t)) - (f p * (dotProduct (rot90p p (rot90p p t)) p) ^ 2 + f q * (dotProduct (rot90p p (rot90p p t)) q) ^ 2 + f (cross p q) * (dotProduct (rot90p p (rot90p p t)) (cross p q)) ^ 2)) := by
  have hf_inv : f t = f (rot90p p (rot90p p t)) := f_rho2_inv_of_g_lat_inv p hp f hg_lat t ht
  have hQ_inv : (f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2)
      = (f p * (dotProduct (rot90p p (rot90p p t)) p) ^ 2 + f q * (dotProduct (rot90p p (rot90p p t)) q) ^ 2 + f (cross p q) * (dotProduct (rot90p p (rot90p p t)) (cross p q)) ^ 2) := by
    have hproj := rot90p_sq_proj p q hp hq hpq t
    rw [hproj.1, hproj.2.1, hproj.2.2]
    ring
  rw [hf_inv, hQ_inv]

/-- **`f' = f − Q` is bounded by 1** (both `f` and the quadratic `Q` lie in `[0,1]`). -/
theorem f_prime_bounded (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x)
    (t : Fin 3 → ℝ) (ht : unitVec3 t) :
    |f t - (f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2)| ≤ 1 := by
  have hft : 0 ≤ f t ∧ f t ≤ 1 := ⟨hpos t ht, frameFunction3_bounded f hf hpos t ht⟩
  have hfr : unitVec3 (cross p q) := cross_unit p q hp hq hpq
  have hfq : 0 ≤ f q ∧ f q ≤ 1 := ⟨hpos q hq, frameFunction3_bounded f hf hpos q hq⟩
  have hfp : 0 ≤ f p ∧ f p ≤ 1 := ⟨hpos p hp, frameFunction3_bounded f hf hpos p hp⟩
  have hfrb : 0 ≤ f (cross p q) ∧ f (cross p q) ≤ 1 := ⟨hpos (cross p q) hfr, frameFunction3_bounded f hf hpos (cross p q) hfr⟩
  have hQ_nonneg : 0 ≤ f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2 := by
    nlinarith [sq_nonneg (dotProduct t p), sq_nonneg (dotProduct t q), sq_nonneg (dotProduct t (cross p q)), hfp.1, hfq.1, hfrb.1]
  have hQ_le : f p * (dotProduct t p) ^ 2 + f q * (dotProduct t q) ^ 2 + f (cross p q) * (dotProduct t (cross p q)) ^ 2 ≤ 1 := by
    have hparseval := parseval p q t hp hq hpq
    rw [dotProduct_symm p t, dotProduct_symm q t, dotProduct_symm (cross p q) t] at hparseval
    have htt : dotProduct t t = 1 := by simpa [unitVec3] using ht
    rw [htt] at hparseval
    have h1 : f p * (dotProduct t p) ^ 2 ≤ 1 * (dotProduct t p) ^ 2 := mul_le_mul_of_nonneg_right hfp.2 (sq_nonneg _)
    have h2 : f q * (dotProduct t q) ^ 2 ≤ 1 * (dotProduct t q) ^ 2 := mul_le_mul_of_nonneg_right hfq.2 (sq_nonneg _)
    have h3 : f (cross p q) * (dotProduct t (cross p q)) ^ 2 ≤ 1 * (dotProduct t (cross p q)) ^ 2 := mul_le_mul_of_nonneg_right hfrb.2 (sq_nonneg _)
    nlinarith [h1, h2, h3, hparseval]
  rw [abs_le]
  constructor <;> nlinarith [hft.1, hft.2, hQ_nonneg, hQ_le]

/-- **The assembly** (Gleason's theorem, dim 3, conditional on latitude
invariance). A nonnegative frame function `f` that depends only on the squared
projection `(t·p)²` is affine in it: `f t = (f p − f q)·(t·p)² + f q`, i.e.
`f t = Tr(ρ·ttᵀ)` for the mixed state `ρ = (f p − f q)·ppᵀ + f q·I`. -/
theorem gleason_assembly (p q : Fin 3 → ℝ) (hp : unitVec3 p) (hq : unitVec3 q) (hpq : orthVec3 p q)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f)
    (hpos : ∀ x, unitVec3 x → 0 ≤ f x)
    (hlat : ∀ t t', unitVec3 t → unitVec3 t' → (dotProduct t p) ^ 2 = (dotProduct t' p) ^ 2 → f t = f t') :
    ∀ t, unitVec3 t → f t = (f p - f q) * (dotProduct t p) ^ 2 + f q := by
  let F : ℝ → ℝ := fun a => f (Real.sqrt a • p + Real.sqrt (1 - a) • q)
  have hF_bounded : ∃ M : ℝ, ∀ a, 0 ≤ a → a ≤ 1 → |F a| ≤ M := by
    refine ⟨1, ?_⟩
    intro a ha ha1
    have hta : unitVec3 (Real.sqrt a • p + Real.sqrt (1 - a) • q) :=
      (unit_smul_of_latitude p q hp hq hpq a ha ha1).1
    have hnonneg : 0 ≤ F a := by dsimp [F]; exact hpos _ hta
    have hle : F a ≤ 1 := by dsimp [F]; exact frameFunction3_bounded f hf hpos _ hta
    dsimp [F]
    rw [abs_of_nonneg hnonneg]
    exact hle
  have hF : ∀ a b c, 0 ≤ a → 0 ≤ b → 0 ≤ c → a + b + c = 1 → F a + F b + F c = F 1 + 2 * F 0 := by
    intro a b c ha hb hc habc
    rcases realize p hp a b c ha hb hc habc with ⟨t1, t2, t3, ht1, ht2, ht3, h12, h13, h23, hp1, hp2, hp3⟩
    have hFa : F a = f t1 := by
      dsimp [F]
      exact hlat _ t1 (unit_smul_of_latitude p q hp hq hpq a ha (by linarith)).1 ht1
        (by rw [(unit_smul_of_latitude p q hp hq hpq a ha (by linarith)).2, hp1])
    have hFb : F b = f t2 := by
      dsimp [F]
      exact hlat _ t2 (unit_smul_of_latitude p q hp hq hpq b hb (by linarith)).1 ht2
        (by rw [(unit_smul_of_latitude p q hp hq hpq b hb (by linarith)).2, hp2])
    have hFc : F c = f t3 := by
      dsimp [F]
      exact hlat _ t3 (unit_smul_of_latitude p q hp hq hpq c hc (by linarith)).1 ht3
        (by rw [(unit_smul_of_latitude p q hp hq hpq c hc (by linarith)).2, hp3])
    have hframe : f t1 + f t2 + f t3 = 1 := hf t1 t2 t3 ht1 ht2 ht3 h12 h13 h23
    have hF1 : F 1 = f p := by dsimp [F]; simp [Real.sqrt_one, Real.sqrt_zero]
    have hF0 : F 0 = f q := by dsimp [F]; simp [Real.sqrt_one, Real.sqrt_zero]
    have hpq_cross : f (cross p q) = f q := by
      apply hlat
      · exact cross_unit p q hp hq hpq
      · exact hq
      · have h1 : dotProduct (cross p q) p = 0 := by
          rw [dotProduct_symm]
          simpa [orthVec3] using cross_orth_left p q
        have h2 : dotProduct q p = 0 := by rw [dotProduct_symm]; simpa [orthVec3] using hpq
        simp [h1, h2]
    have hsum1 : f p + f q + f (cross p q) = 1 :=
      hf p q (cross p q) hp hq (cross_unit p q hp hq hpq) hpq (cross_orth_left p q) (cross_orth_right p q)
    rw [hFa, hFb, hFc, hF1, hF0]
    rw [hpq_cross] at hsum1
    linarith [hframe, hsum1]
  have hFlin := Cauchy.affine_of_triple_sum F hF hF_bounded
  have hF1 : F 1 = f p := by dsimp [F]; simp [Real.sqrt_one, Real.sqrt_zero]
  have hF0 : F 0 = f q := by dsimp [F]; simp [Real.sqrt_one, Real.sqrt_zero]
  intro t ht
  have hproj_nonneg : 0 ≤ (dotProduct t p) ^ 2 := sq_nonneg _
  have hproj_le : (dotProduct t p) ^ 2 ≤ 1 := sq_dot_le_one_of_unit t p ht hp
  have hFt := hFlin ((dotProduct t p) ^ 2) hproj_nonneg hproj_le
  have hF_eq_ft : F ((dotProduct t p) ^ 2) = f t := by
    dsimp [F]
    apply hlat
    · exact (unit_smul_of_latitude p q hp hq hpq ((dotProduct t p) ^ 2) hproj_nonneg hproj_le).1
    · exact ht
    · rw [(unit_smul_of_latitude p q hp hq hpq ((dotProduct t p) ^ 2) hproj_nonneg hproj_le).2]
  rw [← hF_eq_ft, hFt, hF1, hF0]

/-- `u · (c • x) = c · (u · x)` — scalar moves out of the second argument. -/
theorem dotProduct_smul_right (u x : Fin 3 → ℝ) (c : ℝ) :
    dotProduct u (c • x) = c * dotProduct u x := by
  simp [dotProduct, Fin.sum_univ_three, Pi.smul_apply]
  ring

/-- The φ-map is perpendicular to its argument: `λ(u) ⊥ u`. -/
theorem phi_map_orth (u v : Fin 3 → ℝ) (hu : unitVec3 u) : orthVec3 u (phi_map u v) := by
  dsimp [phi_map, orthVec3]
  rw [dotProduct_smul_right u ((dotProduct u v) • u - v) (1 / Real.sqrt (1 - (dotProduct u v) ^ 2))]
  rw [dotProduct_sub_right u ((dotProduct u v) • u) v]
  rw [dotProduct_smul_right u u (dotProduct u v)]
  have huu : dotProduct u u = 1 := by simpa [unitVec3] using hu
  rw [huu]
  ring

/-- **L6 (the oscillation relation)** — the frame identity that the continuity proof iterates.
For the frames `{u, λ(u), u×λ(u)}` and `{e, p, e×p}` (with `λ(e) = p`), the frame property gives
`f u − f e = (f p − f(λ u)) + (f(e×p) − f(u×λ u))`. -/
theorem oscillation_relation (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (v : Fin 3 → ℝ) (hv : unitVec3 v)
    (u : Fin 3 → ℝ) (hu : unitVec3 u) (hne : dotProduct u v ^ 2 ≠ 1)
    (f : (Fin 3 → ℝ) → ℝ) (hf : FrameFunction3 f) :
    f u - f e = (f p - f (phi_map u v)) + (f (cross e p) - f (cross u (phi_map u v))) := by
  let lu : Fin 3 → ℝ := phi_map u v
  have hlu : unitVec3 lu := by dsimp [lu]; exact phi_map_unit u v hu hv hne
  have hul : orthVec3 u lu := by dsimp [lu]; exact phi_map_orth u v hu
  have hz : unitVec3 (cross u lu) := cross_unit u lu hu hlu hul
  have hez : unitVec3 (cross e p) := cross_unit e p he hp hep
  have huz : orthVec3 u (cross u lu) := cross_orth_left u lu
  have hlz : orthVec3 lu (cross u lu) := cross_orth_right u lu
  have hel : orthVec3 e p := hep
  have hez_orth : orthVec3 e (cross e p) := cross_orth_left e p
  have hpz : orthVec3 p (cross e p) := cross_orth_right e p
  have h := two_frame_diff f hf u lu (cross u lu) e p (cross e p) hu hlu hz he hp hez hul huz hlz hel hez_orth hpz
  dsimp [lu] at h
  exact h

/-- The cross product is bounded by the product of norms: `‖a×b‖² ≤ ‖a‖²·‖b‖²`
(Binet–Cauchy). -/
theorem cross_norm_le (a b : Fin 3 → ℝ) :
    dotProduct (cross a b) (cross a b) ≤ dotProduct a a * dotProduct b b := by
  have h := cross_dot_cross a b a b
  have hab : dotProduct a b * dotProduct b a ≥ 0 := by
    rw [dotProduct_symm b a]
    exact mul_self_nonneg (dotProduct a b)
  rw [h]
  nlinarith

/-- `cross` is linear in the first argument. -/
theorem cross_add_left (u w z : Fin 3 → ℝ) : cross (u + w) z = cross u z + cross w z := by
  ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring

/-- `cross` is linear in the second argument. -/
theorem cross_add_right (u w z : Fin 3 → ℝ) : cross u (w + z) = cross u w + cross u z := by
  ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three] <;> ring

/-- `cross` is homogeneous in the first argument: `(c•a) × b = c • (a × b)`. -/
theorem cross_smul_left (c : ℝ) (a b : Fin 3 → ℝ) : cross (c • a) b = c • cross a b := by
  ext i; fin_cases i <;> simp [cross, Fin.sum_univ_three, Pi.smul_apply] <;> ring

/-- The triangle inequality in squared-norm form: `‖X+Y‖² ≤ (‖X‖+‖Y‖)²`. -/
theorem norm_sq_triangle (X Y : Fin 3 → ℝ) :
    dotProduct (X + Y) (X + Y) ≤ (Real.sqrt (dotProduct X X) + Real.sqrt (dotProduct Y Y)) ^ 2 := by
  have hcs := dotProduct_abs_le_norm X Y
  have hle : dotProduct X Y ≤ Real.sqrt (dotProduct X X) * Real.sqrt (dotProduct Y Y) :=
    le_trans (le_abs_self (dotProduct X Y)) hcs
  calc
    dotProduct (X + Y) (X + Y) = dotProduct X X + 2 * dotProduct X Y + dotProduct Y Y := by
      simp [dotProduct, Fin.sum_univ_three]
      ring
    _ ≤ dotProduct X X + 2 * (Real.sqrt (dotProduct X X) * Real.sqrt (dotProduct Y Y)) + dotProduct Y Y := by
      nlinarith [hle]
    _ = (Real.sqrt (dotProduct X X) + Real.sqrt (dotProduct Y Y)) ^ 2 := by
      rw [add_sq]
      have hX : (Real.sqrt (dotProduct X X)) ^ 2 = dotProduct X X := Real.sq_sqrt (dotProduct_self_nonneg X)
      have hY : (Real.sqrt (dotProduct Y Y)) ^ 2 = dotProduct Y Y := Real.sq_sqrt (dotProduct_self_nonneg Y)
      rw [hX, hY]
      ring

/-- **Cross-product continuity bound** — the geometric bridge from `‖λu − p‖` and `‖u − e‖`
to the second oscillation term: `‖u×λu − e×p‖ ≤ ‖u−e‖·‖λu‖ + ‖e‖·‖λu − p‖` (squared). -/
theorem cross_sub_norm_le (u w e z : Fin 3 → ℝ) :
    dotProduct (cross u w - cross e z) (cross u w - cross e z)
      ≤ (Real.sqrt (dotProduct (u - e) (u - e)) * Real.sqrt (dotProduct w w)
          + Real.sqrt (dotProduct e e) * Real.sqrt (dotProduct (w - z) (w - z))) ^ 2 := by
  have hdecomp : cross u w - cross e z = cross (u - e) w + cross e (w - z) := by
    ext i; fin_cases i <;> simp [cross, sub_eq_add_neg] <;> ring
  rw [hdecomp]
  have htri := norm_sq_triangle (cross (u - e) w) (cross e (w - z))
  have h1 : Real.sqrt (dotProduct (cross (u - e) w) (cross (u - e) w)) ≤ Real.sqrt (dotProduct (u - e) (u - e)) * Real.sqrt (dotProduct w w) := by
    have h := cross_norm_le (u - e) w
    have hsqrt := Real.sqrt_le_sqrt h
    rw [Real.sqrt_mul (dotProduct_self_nonneg (u - e)) (dotProduct w w)] at hsqrt
    exact hsqrt
  have h2 : Real.sqrt (dotProduct (cross e (w - z)) (cross e (w - z))) ≤ Real.sqrt (dotProduct e e) * Real.sqrt (dotProduct (w - z) (w - z)) := by
    have h := cross_norm_le e (w - z)
    have hsqrt := Real.sqrt_le_sqrt h
    rw [Real.sqrt_mul (dotProduct_self_nonneg e) (dotProduct (w - z) (w - z))] at hsqrt
    exact hsqrt
  have hsum : Real.sqrt (dotProduct (cross (u - e) w) (cross (u - e) w)) + Real.sqrt (dotProduct (cross e (w - z)) (cross e (w - z)))
      ≤ Real.sqrt (dotProduct (u - e) (u - e)) * Real.sqrt (dotProduct w w) + Real.sqrt (dotProduct e e) * Real.sqrt (dotProduct (w - z) (w - z)) :=
    add_le_add h1 h2
  have hnonneg : 0 ≤ Real.sqrt (dotProduct (cross (u - e) w) (cross (u - e) w)) + Real.sqrt (dotProduct (cross e (w - z)) (cross e (w - z))) :=
    add_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
  have hb : 0 ≤ Real.sqrt (dotProduct (u - e) (u - e)) * Real.sqrt (dotProduct w w) + Real.sqrt (dotProduct e e) * Real.sqrt (dotProduct (w - z) (w - z)) :=
    add_nonneg (mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)) (mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
  have hsumbound : (Real.sqrt (dotProduct (cross (u - e) w) (cross (u - e) w)) + Real.sqrt (dotProduct (cross e (w - z)) (cross e (w - z)))) ^ 2
      ≤ (Real.sqrt (dotProduct (u - e) (u - e)) * Real.sqrt (dotProduct w w) + Real.sqrt (dotProduct e e) * Real.sqrt (dotProduct (w - z) (w - z))) ^ 2 := by
    exact sq_le_sq.mpr (by
      show |Real.sqrt (dotProduct (cross (u - e) w) (cross (u - e) w)) + Real.sqrt (dotProduct (cross e (w - z)) (cross e (w - z)))| ≤
           |Real.sqrt (dotProduct (u - e) (u - e)) * Real.sqrt (dotProduct w w) + Real.sqrt (dotProduct e e) * Real.sqrt (dotProduct (w - z) (w - z))|
      rwa [abs_of_nonneg hnonneg, abs_of_nonneg hb])
  exact le_trans htri hsumbound

/-- **L6 (the contraction)** — the φ-map's second leg: for `u` near `e` (`‖u−e‖ < r²/12`),
`u×λu` is within `r²/12 + r` of `e×p` (combining L5 `‖λu − p‖ < r` with the cross-product
bound). This is the geometric contraction the continuity iteration runs on. -/
theorem l6_contraction (e p : Fin 3 → ℝ) (he : unitVec3 e) (hp : unitVec3 p) (hep : orthVec3 e p)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1)
    (u : Fin 3 → ℝ) (hu : unitVec3 u) (hne : dotProduct u (l5_v e p r) ^ 2 ≠ 1)
    (hδ : dotProduct (u - e) (u - e) < (r ^ 2 / 12) ^ 2) :
    dotProduct (cross u (phi_map u (l5_v e p r)) - cross e p) (cross u (phi_map u (l5_v e p r)) - cross e p) < (r ^ 2 / 12 + r) ^ 2 := by
  have hphi := oscillation_transfer_norm e p he hp hep r hr hr1 u hu hδ
  have hphi_unit : unitVec3 (phi_map u (l5_v e p r)) :=
    phi_map_unit u (l5_v e p r) hu (l5_v_unit e p he hp hep r hr hr1) hne
  have hcross := cross_sub_norm_le u (phi_map u (l5_v e p r)) e p
  have hδ' : Real.sqrt (dotProduct (u - e) (u - e)) < r ^ 2 / 12 := by
    have hlt := sq_lt_sq.mp (show (Real.sqrt (dotProduct (u - e) (u - e))) ^ 2 < (r ^ 2 / 12) ^ 2 by
      rw [Real.sq_sqrt (dotProduct_self_nonneg (u - e))]
      exact hδ)
    have h1 : |Real.sqrt (dotProduct (u - e) (u - e))| = Real.sqrt (dotProduct (u - e) (u - e)) := abs_of_nonneg (Real.sqrt_nonneg _)
    have h2 : |r ^ 2 / 12| = r ^ 2 / 12 := abs_of_nonneg (by nlinarith [sq_nonneg r])
    rwa [h1, h2] at hlt
  have hphip : Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p)) < r := by
    have hlt := sq_lt_sq.mp (show (Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p))) ^ 2 < r ^ 2 by
      rw [Real.sq_sqrt (dotProduct_self_nonneg (phi_map u (l5_v e p r) - p))]
      exact hphi)
    have h1 : |Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p))| = Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p)) := abs_of_nonneg (Real.sqrt_nonneg _)
    have h2 : |r| = r := abs_of_nonneg (le_of_lt hr)
    rwa [h1, h2] at hlt
  have hphi_norm : Real.sqrt (dotProduct (phi_map u (l5_v e p r)) (phi_map u (l5_v e p r))) = 1 := by
    have h : dotProduct (phi_map u (l5_v e p r)) (phi_map u (l5_v e p r)) = 1 := by simpa [unitVec3] using hphi_unit
    rw [h, Real.sqrt_one]
  have he_norm : Real.sqrt (dotProduct e e) = 1 := by
    have h : dotProduct e e = 1 := by simpa [unitVec3] using he
    rw [h, Real.sqrt_one]
  rw [hphi_norm, he_norm] at hcross
  have hsum_lt : Real.sqrt (dotProduct (u - e) (u - e)) + Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p)) < r ^ 2 / 12 + r := by
    nlinarith [hδ', hphip]
  have hsq : (Real.sqrt (dotProduct (u - e) (u - e)) + Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p))) ^ 2 < (r ^ 2 / 12 + r) ^ 2 := by
    exact sq_lt_sq.mpr (by
      have h1 : |Real.sqrt (dotProduct (u - e) (u - e)) + Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p))| = Real.sqrt (dotProduct (u - e) (u - e)) + Real.sqrt (dotProduct (phi_map u (l5_v e p r) - p) (phi_map u (l5_v e p r) - p)) :=
        abs_of_nonneg (add_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
      have h2 : |r ^ 2 / 12 + r| = r ^ 2 / 12 + r := abs_of_nonneg (by nlinarith [hr])
      rwa [h1, h2])
  nlinarith [hcross, hsq]

end GleasonLemma

