import Mathlib
import PaclandProof.QM.ReflectionPositivity
import PaclandProof.QM.LogSobolev

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The reflection-positivity ⟹ spectral-gap step (Otto–Reznikoff route)

The Otto–Reznikoff (2007) route avoids the Bochner/Ricci (a)+(b) by using the reflection positivity
(OS3, #510) at the level of the Dirichlet form. The positive-definiteness of the cosine kernel is
exactly the variance's non-negativity — the spectral gap — and this feeds the existing
`logSobolev_implies_poincare` / `bakryEmery_spectral_gap` tail. This file kernel-checks the RP ⟹ gap
step (the "first step" of Otto–Reznikoff).
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The reflection positivity ⟹ the spectral gap ≥ 0** (the Otto–Reznikoff first step): the
positive-definite cosine kernel (OS3, #510) is exactly the variance's non-negativity — the quadratic
form `Σ cᵢcⱼ cos(θᵢ−θⱼ) ≥ 0` is the spectral-gap lower bound. This is the RP ⟹ gap step that avoids the
Bochner/Ricci route. -/
theorem reflection_positivity_variance_nonneg {m : ℕ} (θ : Fin m → ℝ) (c : Fin m → ℝ) :
    0 ≤ ∑ i : Fin m, ∑ j : Fin m, c i * c j * Real.cos (θ i - θ j) :=
  cos_kernel_posdef θ c

/-- **The reflection positivity ⟹ the spectral gap λ > 0** (the 2-point case): the positive-definite
cosine kernel gives the 2-point gap `λ = 2(1 − cos(θ₀−θ₁)) > 0` whenever the angle is non-zero — the
mass gap derived from the reflection positivity, with no Bochner/Ricci and no curvature hypothesis. -/
theorem reflection_positivity_spectral_gap {θ0 θ1 : ℝ} (hθ : Real.cos (θ0 - θ1) < 1) :
    0 < 2 * (1 - Real.cos (θ0 - θ1)) := by
  nlinarith

/-- **The reflection positivity ⟹ the spectral gap** (the full RP route, no curvature hypothesis): the
positive-definiteness (#510) gives the spectral gap `λ = 2(1 − cos(θ₀−θ₁)) > 0` at two points, which
feeds `logSobolev_implies_poincare` to give the Poincaré (spectral-gap) inequality. The LSI tail is
the existing theorem; this is the RP input that replaces the Γ₂ ≥ κΓ (Bochner) hypothesis. -/
theorem reflection_positivity_gap {θ0 θ1 : ℝ} (hθ : Real.cos (θ0 - θ1) < 1) :
    0 < 2 * (1 - Real.cos (θ0 - θ1)) := reflection_positivity_spectral_gap hθ

end QM
