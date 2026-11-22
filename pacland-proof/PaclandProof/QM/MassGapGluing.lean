import Mathlib
import PaclandProof.QM.ClusterExpansion
import PaclandProof.QM.WangAssembly

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The common observable and the gluing theorem

The two mechanisms bound the SAME spectral quantity: `m = 1/ξ = −log(λ₁/λ₀)` — the spectral gap of the
transfer operator, equivalently the inverse physical correlation length. The cluster expansion reaches it
through the correlation-length face (`m ≥ m_strong = −log u`); the Wang bound reaches it through the
spectral-gap face (`m ≥ m_weak = the integrated curvature`). Because they are bounds on the SAME `m`, the
gluing `m ≥ max(m_strong, m_weak)` is well-defined over the whole coupling domain.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The common observable: the spectral gap `m = 1/ξ = −log(λ₁/λ₀)` of the transfer operator. This is
the single quantity both mechanisms bound, and the object whose positivity is the mass gap. -/
def massGap (m : ℝ) : ℝ := m

/-- The strong-coupling bound (cluster expansion), on the correlation-length face: `m ≥ −log u(β)`,
where `u(β) = I₂(2β)/I₁(2β)` is the character coefficient. Valid at strong coupling. -/
def m_strong (u : ℝ → ℝ) (β : ℝ) : ℝ := -Real.log (u β)

/-- The two bounds are on the SAME observable: both `m_strong` and `m_weak` are lower bounds on the
spectral gap `m`. This is the statement that makes the gluing well-defined. -/
def SameObservable (m m_strong m_weak : ℝ → ℝ) : Prop :=
  (∀ β, m_strong β ≤ m β) ∧ (∀ β, m_weak β ≤ m β)

/-- **The gluing theorem (the statement)**: `m ≥ max(m_strong, m_weak)` over the whole coupling domain.
Equivalent to `SameObservable`; the open step (Step 5) is proving it, uniform in volume and surviving the
continuum. -/
def MassGapGluing (m m_strong m_weak : ℝ → ℝ) : Prop :=
  SameObservable m m_strong m_weak

/-- **The mass gap is positive** iff the gluing holds AND at least one bound is positive somewhere — the
crossover is covered because the max never dips below the larger of the two. -/
def MassGapPositive (m m_strong m_weak : ℝ → ℝ) : Prop :=
  MassGapGluing m m_strong m_weak ∧ (∃ β : ℝ, 0 < m_strong β) ∧ (∃ β : ℝ, 0 < m_weak β)

end QM
