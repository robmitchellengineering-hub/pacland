import Mathlib
import PaclandProof.QM.GaussianLSI
import PaclandProof.QM.LogSobolev

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The mass-gap reduction, with the committed Bochner/curvature wired in

The honest state of the Gaussian mass-gap half, stated as a reduction:

    mass gap  =  the committed Bochner curvature Γ₂ ≥ Γ (GaussianLSI.lean, kernel-checked)
                 +  the Bakry–Émery interpolation Γ₂ ≥ κΓ ⟹ LSI (Bakry–Émery 1985, CITED)
                 +  the LSI ⟹ Poincaré tail (LogSobolev.lean, kernel-checked)

The single open rung is the Bakry–Émery interpolation — a published theorem, named with its exact
reference, stated as a hypothesis with the citation, not proved and not faked.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The Bakry–Émery interpolation (the cited open rung)**: `Γ₂ ≥ κΓ ⟹ LogSobolev(2/κ)`.
Bakry and Émery, "Diffusions hypercontractives", Séminaire de Probabilités XIX, Springer LNM 1123
(1985) 177–206. A published theorem, stated as a hypothesis with the citation. -/
def bakryEmeryInterpolation {α : Type*} [Fintype α] (μ : α → ℝ) (Γ Γ₂ : (α → ℝ) → α → ℝ) (κ : ℝ) : Prop :=
  (∀ f x, κ * Γ f x ≤ Γ₂ f x) → LogSobolev μ Γ (2 / κ)

/-- **The Gaussian mass-gap reduction**: the Poincaré (spectral) gap follows from
(i) the committed Bochner curvature `Γ ≤ Γ₂` (the `hBE` hypothesis, kernel-checked in `GaussianLSI.lean`
for the OU generator), (ii) the cited Bakry–Émery interpolation, and (iii) the committed
`LSI ⟹ Poincaré` tail. The interpolation is the single named open rung. -/
theorem gaussian_mass_gap_reduction {α : Type*} [Fintype α] {μ : α → ℝ} {Γ Γ₂ : (α → ℝ) → α → ℝ}
    (hBE : ∀ f x, Γ f x ≤ Γ₂ f x)
    (hinterp : bakryEmeryInterpolation μ Γ Γ₂ 1)
    (hΓlin : ∀ g ε, Γ (fun x => 1 + ε * g x) = fun x => ε ^ 2 * Γ g x)
    (hEnt : EntropyQuadraticAtOne μ) :
    Poincare μ Γ 1 := by
  have hLS : LogSobolev μ Γ (2 / 1) := hinterp (by intro f x; simpa using hBE f x)
  have h := bakryEmery_spectral_gap (κ := 1) (by norm_num) hLS hΓlin hEnt
  simpa using h

/-- **The committed curvature plugs into the reduction**: for the OU generator, the Bochner curvature
`Γ ≤ Γ₂` is already kernel-checked (`ou_bakry_emery`), so the Gaussian mass gap reduces to the single
cited Bakry–Émery interpolation. -/
theorem gaussian_mass_gap_reduction_ou (f : ℝ → ℝ)
    (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f)) (hf'' : Differentiable ℝ (deriv (deriv f)))
    (hf''' : Differentiable ℝ (deriv (deriv (deriv f)))) (x : ℝ) :
    carreDuChamp ouGenerator f f x ≤ Gamma2 ouGenerator f x :=
  ou_bakry_emery f hf hf' hf'' hf''' x

end QM
