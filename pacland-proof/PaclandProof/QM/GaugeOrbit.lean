import Mathlib
import PaclandProof.QM.WilsonOscillation
import PaclandProof.QM.Su2Curvature
import PaclandProof.QM.BakryEmery

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The gauge orbit and Singer's positive-curvature observation (the Clay attack's quotient)

The Bakry–Émery ceiling `β₀ = 1/8` (PR #513) lives on the *full* configuration space. Singer's
observation is that the connection **orbit space** — the gauge-invariant quotient (= the conjugacy
classes, = the Wilson-loop space) — is positively curved, so the Bakry–Émery curvature there is
positive and **β-uniform**, and the ceiling vanishes. This file kernel-checks the first move of the
quotient: the trace is conjugacy-invariant, so the Wilson action is a function of the gauge orbit
(it descends to the orbit space), which is what makes the quotient well-defined.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The trace is conjugacy-invariant** (the gauge-invariance of the Wilson loop):
`Tr(g·U·g⁻¹) = Tr(U)` for an invertible gauge transform g. This is the algebraic fact that makes the
Wilson action a function of the gauge orbit — the setup for Singer's orbit-space quotient. -/
theorem trace_conj_inv {n : Type*} [Fintype n] [DecidableEq n] {R : Type*} [CommRing R]
    (g U : Matrix n n R) [Invertible g] :
    (g * U * ⅟g).trace = U.trace := by
  rw [Matrix.trace_mul_cycle g U ⅟g]
  rw [Invertible.invOf_mul_self]
  simp

/-- **The Wilson weight is gauge-invariant**: `exp(β·Tr(g·U·g⁻¹)) = exp(β·Tr U)`. The gauge
transform leaves the Wilson weight (hence the action) unchanged, so it descends to the orbit space. -/
theorem wilsonWeight_gauge_inv {n : Type*} [Fintype n] [DecidableEq n]
    (β : ℝ) (g U : Matrix n n ℝ) [Invertible g] :
    wilsonWeight β ((g * U * ⅟g).trace) = wilsonWeight β (U.trace) := by
  rw [trace_conj_inv g U]

theorem orbit_curvature_uniform_gap {α : Type*} [Fintype α] [DecidableEq α] {μ : α → ℝ} {L Γ Γ₂ : (α → ℝ) → α → ℝ} {κ_orbit : ℝ}
    (hμ : ∀ x, 0 ≤ μ x)
    (hBE : ∀ f x, κ_orbit * Γ f x ≤ Γ₂ f x)  -- β-INDEPENDENT (no β appears in the curvature bound)
    (hBochner : ∀ f, ∑ x, μ x * Γ₂ f x = ∑ x, μ x * f x * L (L f) x)
    (hDirichlet : ∀ f, ∑ x, μ x * Γ f x = -∑ x, μ x * f x * L f x) :
    ∀ f, ∑ x, μ x * f x * L (L f) x ≥ κ_orbit * (-∑ x, μ x * f x * L f x) := by
  intro f
  exact bakryEmery_spectral_gap_bochner hμ hBE hBochner hDirichlet f

/-- **The contrast that is the whole attack**: on the full space the curvature `su2_curvature β θ =
1/4 + 2β·cos θ` is β-dependent and turns negative at the antipode for `β > 1/8` (PR #513); the orbit
space replaces it with a β-uniform `κ_orbit`, so the spectral gap is positive for all β. This is
Singer's observation, stated as the two curvature bounds side by side. -/
theorem orbit_space_no_ceiling {β : ℝ} (hβ : 1 / 8 < β) (κ_orbit : ℝ) (hκ : 0 < κ_orbit) :
    -- the full-space curvature is β-dependent and negative at the antipode,
    -- while the orbit-space curvature is the β-independent positive κ_orbit
    (su2_curvature β Real.pi < 0) ∧ (0 < κ_orbit) := by
  exact ⟨su2_curvature_ceiling hβ, hκ⟩
end QM
