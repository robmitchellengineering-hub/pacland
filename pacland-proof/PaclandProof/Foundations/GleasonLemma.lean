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

end GleasonLemma

end
