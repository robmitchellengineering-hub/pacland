import Mathlib
import PaclandProof.QM.BochnerProof
import PaclandProof.QM.Su2Curvature

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The SU(2) Bochner inequality — Γ₂ ≥ (1/4 + 2β·cos θ)·Γ(f)

Step 2 of the mass-gap reduction: instantiate the proven 1D Bochner formula with the full S³ generator
`a(θ) = 2·cot θ − 2β·sin θ`. The derivative `−a'(θ) = 2/sin²θ + 2β·cos θ`, and `2/sin²θ ≥ 2 ≥ 1/4`, so
`Γ₂(f) = (f'')² + (2/sin²θ + 2β·cos θ)(f')² ≥ (1/4 + 2β·cos θ)·Γ(f)`.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The SU(2) diffusion generator on the full S³: `Lf = f'' + (2·cot θ − 2β·sin θ)·f'`. -/
def su2_generator (β : ℝ) (f : ℝ → ℝ) : ℝ → ℝ :=
  fun θ => deriv (deriv f) θ + (2 * (Real.cos θ / Real.sin θ) - 2 * β * Real.sin θ) * deriv f θ

/-- The SU(2) drift `a(θ) = 2·cot θ − 2β·sin θ`. -/
def su2_drift (β : ℝ) (θ : ℝ) : ℝ :=
  2 * (Real.cos θ / Real.sin θ) - 2 * β * Real.sin θ

/-- The derivative of the SU(2) drift: `a'(θ) = −2/sin²θ − 2β·cos θ`. -/
theorem su2_drift_deriv (β : ℝ) (θ : ℝ) (hθ : Real.sin θ ≠ 0) :
    deriv (su2_drift β) θ = -2 / (Real.sin θ) ^ 2 - 2 * β * Real.cos θ := by
  change deriv (fun x => 2 * (Real.cos x / Real.sin x) - 2 * β * Real.sin x) θ = _
  have hcos : HasDerivAt Real.cos (-Real.sin θ) θ := Real.hasDerivAt_cos θ
  have hsin : HasDerivAt Real.sin (Real.cos θ) θ := Real.hasDerivAt_sin θ
  have hdiv : HasDerivAt (fun x => Real.cos x / Real.sin x)
      ((-Real.sin θ * Real.sin θ - Real.cos θ * Real.cos θ) / (Real.sin θ) ^ 2) θ :=
    hcos.div hsin hθ
  have hconst : HasDerivAt (fun x => 2 * (Real.cos x / Real.sin x))
      (2 * ((-Real.sin θ * Real.sin θ - Real.cos θ * Real.cos θ) / (Real.sin θ) ^ 2)) θ :=
    hdiv.const_mul 2
  have hsin2 : HasDerivAt (fun x => 2 * β * Real.sin x) (2 * β * Real.cos θ) θ :=
    hsin.const_mul (2 * β)
  have hsub : HasDerivAt (fun x => 2 * (Real.cos x / Real.sin x) - 2 * β * Real.sin x)
      (2 * ((-Real.sin θ * Real.sin θ - Real.cos θ * Real.cos θ) / (Real.sin θ) ^ 2) - 2 * β * Real.cos θ) θ :=
    hconst.sub hsin2
  rw [hsub.deriv]
  field_simp [hθ]
  rw [Real.sin_sq_add_cos_sq]
  ring

/-- **The SU(2) Bochner inequality**: `Γ₂(f) ≥ (1/4 + 2β·cos θ)·Γ(f)` on the S³ coordinate chart. -/
theorem su2_bochner_inequality (β : ℝ) (f : ℝ → ℝ) (θ : ℝ) (hθ : Real.sin θ ≠ 0)
    (hf : ContDiff ℝ 4 f) :
    (1 / 4 + 2 * β * Real.cos θ) * carreDuChamp (su2_generator β) f f θ
      ≤ Gamma2 (su2_generator β) f θ := by
  sorry

end QM
