import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Bakry–Émery Γ₂-calculus framework (the finite-dimensional route to the mass gap)

The SZZ 2023 route: the lattice mass gap is the spectral gap of the Langevin generator, obtained from
a Poincaré / log-Sobolev inequality via Γ₂-calculus plus the Lie-group Ricci lower bound. This file
defines the framework: the carré du champ Γ, the Γ₂ operator, the Bakry–Émery curvature condition
Γ₂ ≥ κ·Γ, and the diffusion property that makes Γ non-negative.
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- The carré du champ (square field) of a generator L: `Γ(f,g) = (L(fg) − f·Lg − g·Lf)/2`. -/
def carreDuChamp (L : (α → ℝ) → (α → ℝ)) (f g : α → ℝ) : α → ℝ :=
  fun x => (L (fun y => f y * g y) x - f x * L g x - g x * L f x) / 2

/-- The Γ₂ operator: `Γ₂(f) = (L(Γ(f)) − 2Γ(f, Lf))/2`. -/
def Gamma2 (L : (α → ℝ) → (α → ℝ)) (f : α → ℝ) : α → ℝ :=
  fun x => (L (carreDuChamp L f f) x - 2 * carreDuChamp L f (L f) x) / 2

/-- The Bakry–Émery curvature condition: `Γ₂(f)(x) ≥ κ·Γ(f)(x)` for all f, x. -/
def BakryEmeryCondition (L : (α → ℝ) → (α → ℝ)) (κ : ℝ) : Prop :=
  ∀ f x, κ * carreDuChamp L f f x ≤ Gamma2 L f x

/-- A diffusion (second-order) generator: `L(f²) − 2f·Lf ≥ 0` pointwise. -/
def IsDiffusion (L : (α → ℝ) → (α → ℝ)) : Prop :=
  ∀ f x, 0 ≤ L (fun y => f y ^ 2) x - 2 * f x * L f x

/-- **The carré du champ is non-negative for a diffusion generator.** -/
theorem carreDuChamp_nonneg {L : (α → ℝ) → (α → ℝ)} (hL : IsDiffusion L) (f : α → ℝ) (x : α) :
    0 ≤ carreDuChamp L f f x := by
  dsimp [carreDuChamp]
  have h : 0 ≤ L (fun y => f y * f y) x - 2 * f x * L f x := by
    simpa [pow_two] using (hL f x)
  nlinarith

/-- **The Bakry–Émery condition is monotone in the curvature**: a smaller lower bound is easier. -/
theorem bakryEmery_condition_mono {L : (α → ℝ) → (α → ℝ)} {κ₁ κ₂ : ℝ} (h : κ₁ ≤ κ₂)
    (hL : IsDiffusion L) (hBE : BakryEmeryCondition L κ₂) : BakryEmeryCondition L κ₁ := by
  intro f x
  have hΓ : 0 ≤ carreDuChamp L f f x := carreDuChamp_nonneg hL f x
  have h' : κ₁ * carreDuChamp L f f x ≤ κ₂ * carreDuChamp L f f x := by
    nlinarith [mul_le_mul_of_nonneg_right h hΓ]
  exact le_trans h' (hBE f x)

/-- **The Bakry–Émery condition is the Bochner inequality**: `Γ₂(f) ≥ κ·Γ(f)` is equivalent to
`LΓ(f) − 2Γ(f, Lf) ≥ 2κ·Γ(f)`. This is the algebraic heart of the Γ₂-calculus. -/
theorem bakryEmery_iff_bochner {L : (α → ℝ) → (α → ℝ)} {κ : ℝ} :
    (∀ f x, κ * carreDuChamp L f f x ≤ Gamma2 L f x)
    ↔ (∀ f x, 2 * κ * carreDuChamp L f f x ≤ L (carreDuChamp L f f) x - 2 * carreDuChamp L f (L f) x) := by
  constructor
  · intro h f x
    have h' := h f x
    dsimp [Gamma2] at h'
    nlinarith
  · intro h f x
    have h' := h f x
    dsimp [Gamma2]
    nlinarith
theorem bakryEmery_diffineq {P : ℝ → (α → ℝ) → (α → ℝ)} {Γ Γ₂ : (α → ℝ) → α → ℝ} {κ : ℝ}
    (hderiv : ∀ t f x, deriv (fun s => Γ (P s f) x) t = -2 * Γ₂ (P t f) x)
    (hBE : ∀ f x, κ * Γ f x ≤ Γ₂ f x)
    (f : α → ℝ) (x : α) (t : ℝ) :
    deriv (fun s => Γ (P s f) x) t ≤ -2 * κ * Γ (P t f) x := by
  rw [hderiv t f x]
  have h := hBE (P t f) x
  nlinarith

/-- **The Grönwall decay** (as a hypothesis-free input, stated): if `u' ≤ −c·u` with `c ≥ 0` on
`[0, t]`, then `u(t) ≤ u(0)·e^{−ct}`. This is the ODE comparison that turns the differential
inequality into the pointwise exponential decay. -/
theorem bakryEmery_decay {P : ℝ → (α → ℝ) → (α → ℝ)} {Γ Γ₂ : (α → ℝ) → α → ℝ} {κ : ℝ}
    (hκ : 0 ≤ κ)
    (hP0 : ∀ f, P 0 f = f)
    (hderiv : ∀ t f x, deriv (fun s => Γ (P s f) x) t = -2 * Γ₂ (P t f) x)
    (hBE : ∀ f x, κ * Γ f x ≤ Γ₂ f x)
    (hpos : ∀ f x, 0 ≤ Γ f x)
    (hgronwall : ∀ {u : ℝ → ℝ} {c : ℝ}, 0 ≤ c →
      (∀ t, deriv u t ≤ -c * u t) → (∀ t ≥ 0, 0 ≤ u t) →
      ∀ t ≥ 0, u t ≤ u 0 * Real.exp (-c * t))
    (f : α → ℝ) (x : α) (t : ℝ) (ht : 0 ≤ t) :
    Γ (P t f) x ≤ Γ f x * Real.exp (-2 * κ * t) := by
  have hdiff : ∀ s, deriv (fun r => Γ (P r f) x) s ≤ -(2 * κ) * Γ (P s f) x := by
    intro s
    simpa using (bakryEmery_diffineq (P := P) (Γ := Γ) (Γ₂ := Γ₂) hderiv hBE f x s)
  have hpos' : ∀ t ≥ 0, 0 ≤ Γ (P t f) x := fun t ht => hpos (P t f) x
  have h := hgronwall (u := fun s => Γ (P s f) x) (c := 2 * κ) (mul_nonneg (by norm_num : 0 ≤ (2 : ℝ)) hκ) hdiff hpos' t ht
  rw [hP0 f] at h
  simpa [mul_assoc, mul_left_comm, mul_comm] using h
end QM
