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

/-- The symmetrization is nonnegative when `f` is (on unit vectors). -/
theorem symm_nonneg (p x : Fin 3 → ℝ) (hp : unitVec3 p) (hx : unitVec3 x)
    (f : (Fin 3 → ℝ) → ℝ) (hpos : ∀ y, unitVec3 y → 0 ≤ f y) :
    0 ≤ symm p f x := by
  dsimp [symm]
  have hρx : unitVec3 (rot90p p x) := by simpa [unitVec3, rot90p_orthogonal p x x hp] using hx
  nlinarith [hpos x hx, hpos (rot90p p x) hρx]

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

end GleasonLemma

end
