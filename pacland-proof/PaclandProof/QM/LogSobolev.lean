import Mathlib
import PaclandProof.QM.BakryEmery

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The log-Sobolev ⟹ spectral-gap bridge (Bakry–Émery, finite form)

A log-Sobolev inequality `Ent(f²) ≤ C·Γ(f)` implies the Poincaré inequality `Var(f) ≤ (C/2)·Γ(f)`,
by linearizing around the constant `1 + εg` and taking `ε → 0`. This is the abstract bridge that
turns a Γ₂ ≥ κ·Γ curvature bound (whose Γ₂-calculus gives the log-Sobolev with `C = 2/κ`) into the
spectral gap `λ ≥ κ` of the Langevin generator.
-/

open scoped BigOperators
open Filter

noncomputable section

namespace QM

variable {α : Type*} [Fintype α]

/-- The entropy of f with respect to the measure μ (μ ≥ 0, total 1):
`Ent(f) = Σ μ f log f − (Σ μ f) log (Σ μ f)`. -/
def entropy (μ : α → ℝ) (f : α → ℝ) : ℝ :=
  (∑ x, μ x * f x * Real.log (f x)) - (∑ x, μ x * f x) * Real.log (∑ x, μ x * f x)

/-- The variance of f with respect to the measure μ: `Var(f) = Σ μ f² − (Σ μ f)²`. -/
def variance (μ : α → ℝ) (f : α → ℝ) : ℝ :=
  (∑ x, μ x * f x ^ 2) - (∑ x, μ x * f x) ^ 2

/-- The log-Sobolev inequality: `Ent(f²) ≤ C·Σ μ Γ(f)` for all f. -/
def LogSobolev (μ : α → ℝ) (Γ : (α → ℝ) → α → ℝ) (C : ℝ) : Prop :=
  ∀ f, entropy μ (fun x => f x ^ 2) ≤ C * ∑ x, μ x * Γ f x

/-- The Poincaré inequality (the spectral gap): `Var(f) ≤ C'·Σ μ Γ(f)` for all f. -/
def Poincare (μ : α → ℝ) (Γ : (α → ℝ) → α → ℝ) (C' : ℝ) : Prop :=
  ∀ f, variance μ f ≤ C' * ∑ x, μ x * Γ f x

/-- The entropy's quadratic part at 1: `Ent((1+εg)²)/ε² → 2·Var(g)` as `ε → 0`. -/
def EntropyQuadraticAtOne (μ : α → ℝ) : Prop :=
  ∀ g, Tendsto (fun ε : ℝ => entropy μ (fun x => (1 + ε * g x) ^ 2) / ε ^ 2)
    (nhdsWithin 0 {0}ᶜ) (nhds (2 * variance μ g))

/-- **The log-Sobolev ⟹ the Poincaré (the spectral gap)**: `Ent(f²) ≤ C·Γ(f)` gives
`Var(g) ≤ (C/2)·Γ(g)` by the linearization `f = 1 + εg` and `ε → 0`. -/
theorem logSobolev_implies_poincare {μ : α → ℝ} {Γ : (α → ℝ) → α → ℝ} {C : ℝ}
    (hΓlin : ∀ g ε, Γ (fun x => 1 + ε * g x) = fun x => ε ^ 2 * Γ g x)
    (hEnt : EntropyQuadraticAtOne μ) (hLS : LogSobolev μ Γ C) :
    Poincare μ Γ (C / 2) := by
  intro g
  have hls : ∀ ε, entropy μ (fun x => (1 + ε * g x) ^ 2) ≤ C * ∑ x, μ x * Γ (fun y => 1 + ε * g y) x := by
    intro ε
    exact hLS (fun x => 1 + ε * g x)
  have hΓ : ∀ ε, ∑ x, μ x * Γ (fun y => 1 + ε * g y) x = ε ^ 2 * ∑ x, μ x * Γ g x := by
    intro ε
    rw [hΓlin g ε]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro x hx
    ring
  have hineq : ∀ ε, ε ≠ 0 → entropy μ (fun x => (1 + ε * g x) ^ 2) / ε ^ 2 ≤ C * ∑ x, μ x * Γ g x := by
    intro ε hε
    have h' := hls ε
    have hΓε : ∑ x, μ x * Γ (fun y => 1 + ε * g y) x = ε ^ 2 * ∑ x, μ x * Γ g x := hΓ ε
    rw [hΓε] at h'
    have hε2 : 0 < ε ^ 2 := sq_pos_of_ne_zero hε
    exact (div_le_iff₀ hε2).mpr (by nlinarith [h'])
  have hlim : Tendsto (fun ε : ℝ => entropy μ (fun x => (1 + ε * g x) ^ 2) / ε ^ 2)
      (nhdsWithin 0 {0}ᶜ) (nhds (2 * variance μ g)) := hEnt g
  have hle : 2 * variance μ g ≤ C * ∑ x, μ x * Γ g x := by
    refine le_of_tendsto hlim ?_
    refine Filter.Eventually.mono self_mem_nhdsWithin ?_
    intro ε hε
    exact hineq ε hε
  nlinarith

/-- **The Bakry–Émery theorem (abstract form)**: a Γ₂ ≥ κ·Γ curvature bound gives the log-Sobolev
inequality with constant `2/κ` (the Γ₂-calculus semigroup interpolation), which gives the Poincaré
inequality (the spectral gap) with constant `1/κ`. Assembling the two bridges names the spectral gap
`λ ≥ κ` of the Langevin generator. -/
theorem bakryEmery_spectral_gap {μ : α → ℝ} {Γ : (α → ℝ) → α → ℝ} {κ : ℝ}
    (hκ : κ ≠ 0)
    (hBEtoLS : LogSobolev μ Γ (2 / κ))  -- the Γ₂-calculus output: Γ₂ ≥ κ·Γ ⟹ Ent(f²) ≤ (2/κ)·Γ(f)
    (hΓlin : ∀ g ε, Γ (fun x => 1 + ε * g x) = fun x => ε ^ 2 * Γ g x)
    (hEnt : EntropyQuadraticAtOne μ) :
    Poincare μ Γ (1 / κ) := by
  have h := logSobolev_implies_poincare hΓlin hEnt hBEtoLS
  have h' : (2 / κ) / 2 = 1 / κ := by field
  simpa [h'] using h
end QM
