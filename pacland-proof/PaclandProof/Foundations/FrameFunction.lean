import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Gleason step 2 — the frame function, first consequences

A **frame function** assigns a weight to every unit vector so that the weights sum
to `1` over every orthonormal frame (basis). Gleason's lemma says such a function
is continuous (for dimension ≥ 3); this file kernel-checks the two clean first
consequences every proof of that lemma uses — **evenness** (`f(-u) = f u`) and
**boundedness** (`f u ≤ 1`, for a nonnegative frame function). Toy case `Fin 2`.
-/

noncomputable section

open Matrix BigOperators

namespace FrameFunction

/-- A unit vector (`v · v = 1`, the squared norm to avoid `sqrt`). -/
def unitVec (v : Fin 2 → ℝ) : Prop :=
  dotProduct v v = 1

/-- Orthogonality (`u · v = 0`). -/
def orthVec (u v : Fin 2 → ℝ) : Prop :=
  dotProduct u v = 0

/-- A frame function: weights on unit vectors summing to `1` over every
orthonormal pair (frame in dimension 2). -/
def FrameFunction (f : (Fin 2 → ℝ) → ℝ) : Prop :=
  ∀ u v, unitVec u → unitVec v → orthVec u v → f u + f v = 1

/-- The quarter-turn `v ↦ ![-u₁, u₀]` is the perpendicular unit vector. -/
def rot90 (u : Fin 2 → ℝ) : Fin 2 → ℝ :=
  ![-u 1, u 0]

/-- `dotProduct (-u) (-u) = dotProduct u u` (the norm is even). -/
theorem dotProduct_neg_neg (u : Fin 2 → ℝ) :
    dotProduct (-u) (-u) = dotProduct u u := by
  simp [dotProduct, Fin.sum_univ_two]

/-- The quarter-turn is orthogonal and unit. -/
theorem rot90_orth_unit (u : Fin 2 → ℝ) (hu : unitVec u) :
    orthVec u (rot90 u) ∧ unitVec (rot90 u) := by
  constructor
  · simp [orthVec, rot90, dotProduct, Fin.sum_univ_two]
    ring
  · simp [unitVec, rot90, dotProduct, Fin.sum_univ_two]
    have hu' : u 0 * u 0 + u 1 * u 1 = 1 := by
      simpa [unitVec, dotProduct, Fin.sum_univ_two] using hu
    ring_nf at hu' ⊢
    exact hu'

/-- `unitVec` is even: `-u` is a unit vector iff `u` is. -/
theorem unitVec_neg (u : Fin 2 → ℝ) : unitVec (-u) ↔ unitVec u := by
  simp [unitVec, dotProduct_neg_neg]

/-- **Evenness** — the first clean consequence of the frame property:
`f(-u) = f u`. -/
theorem frameFunction_even (f : (Fin 2 → ℝ) → ℝ) (hf : FrameFunction f)
    (u : Fin 2 → ℝ) (hu : unitVec u) :
    f (-u) = f u := by
  have hv := rot90_orth_unit u hu
  have horth_neg : orthVec (-u) (rot90 u) := by
    simp [orthVec, rot90, dotProduct, Fin.sum_univ_two]
    ring
  have h1 : f u + f (rot90 u) = 1 := hf u (rot90 u) hu hv.2 hv.1
  have h2 : f (-u) + f (rot90 u) = 1 := hf (-u) (rot90 u) ((unitVec_neg u).mpr hu) hv.2 horth_neg
  linarith

/-- **Boundedness** — a nonnegative frame function is `≤ 1` on every unit vector. -/
theorem frameFunction_bounded (f : (Fin 2 → ℝ) → ℝ) (hf : FrameFunction f)
    (hpos : ∀ u, unitVec u → 0 ≤ f u)
    (u : Fin 2 → ℝ) (hu : unitVec u) :
    f u ≤ 1 := by
  have hv := rot90_orth_unit u hu
  have hsum : f u + f (rot90 u) = 1 := hf u (rot90 u) hu hv.2 hv.1
  have hnonneg : 0 ≤ f (rot90 u) := hpos (rot90 u) hv.2
  linarith

end FrameFunction

end
