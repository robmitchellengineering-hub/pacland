import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# M3 — the axial gauge (the first piece of the weak-coupling multiscale RG scaffolding)

Balaban's multiscale RG (the weak-coupling route to the mass gap) uses the **axial gauge**: fix the
links in one lattice direction to the identity, which is a *global* gauge (no Gribov copies). This is
the gauge-fixing that makes the low-temperature cluster expansion well-defined.

On a chain, the axial gauge is a cumulative product: `g (i+1) = g i · U i`. This file kernel-checks
the two facts that make it a genuine gauge-fixing:

1. `axial_gauge_fixes` — the transform sets every link to the identity (existence);
2. `axial_gauge_unique` — any such transform equals `g 0 · axialGauge U` (uniqueness up to the global
   constant gauge `g 0`).
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {G : Type*} [Group G]

/-- The cumulative-product gauge transform on the infinite chain: `g (i+1) = g i · U i`, with
`g 0 = 1`. This is the axial-gauge construction. -/
def axialGauge (U : ℕ → G) : ℕ → G
  | 0 => 1
  | i+1 => axialGauge U i * U i

/-- **The axial-gauge-fixing theorem**: the transform `axialGauge U` sets every link to the
identity — `g i · U i · g (i+1)⁻¹ = 1`. Every connection is gauge-equivalent to the trivial one. -/
theorem axial_gauge_fixes (U : ℕ → G) (i : ℕ) :
    axialGauge U i * U i * (axialGauge U (i+1))⁻¹ = 1 := by
  simp [axialGauge]

/-- **Uniqueness up to a constant**: any gauge transform that fixes the links equals
`g 0 · axialGauge U` — the axial gauge is unique up to the global constant gauge `g 0`. -/
theorem axial_gauge_unique (U : ℕ → G) (g : ℕ → G)
    (h : ∀ i, g i * U i * (g (i+1))⁻¹ = 1) (i : ℕ) :
    g i = g 0 * axialGauge U i := by
  induction' i with i ih
  · simp [axialGauge]
  · have hgi : g (i+1) = g i * U i := (mul_inv_eq_one.mp (h i)).symm
    rw [hgi, ih]
    simp [axialGauge, mul_assoc]

end QM
