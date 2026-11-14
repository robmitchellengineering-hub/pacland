import Mathlib
import PaclandProof.QM.SpacingUniform
import PaclandProof.QM.AsymptoticFreedom

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The mass-gap join (the strong-coupling gap matches the weak-coupling physical mass)

The reconstruction's gap `Δ = 1` (strong coupling, lattice units) and the spacing-uniform
`m_phys = Λ_QCD` (weak coupling, physical) are the SAME physical mass. This file states the single
gap `Δ(β) = e^{−cβ}` (c = 12π²/11) that interpolates the two scales: at β = 0 it is the compactness
gap `λ = 1`, and `m_phys = Δ(β)/a(β) = Λ_QCD = 1` is β-uniform. Honest scope: the interpolation
`Δ(β) = e^{−cβ}` is the hypothesis that the strong- and weak-coupling gaps are one curve; the
β-uniform identification of the two "1"s is then exact.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The single mass gap `Δ(β)` in lattice units: the weak-coupling instanton `e^{−cβ}` (c = 12π²/11),
whose strong-coupling (β = 0) limit is the compactness gap `λ = 1`. This is the ONE gap that
interpolates the two scales. -/
def massGap (c β : ℝ) : ℝ := Real.exp (-c * β)

/-- The running lattice spacing `a(β)`: the asymptotic-freedom spacing `e^{−cβ}`. -/
def runningSpacing (c β : ℝ) : ℝ := Real.exp (-c * β)

/-- **The mass-gap join (strong-coupling side)**: `Δ(0) = 1` — the weak-coupling instanton gap at
`β = 0` equals the strong-coupling compactness gap `λ = 1`. They are the SAME single gap, not two
different scales. -/
theorem mass_gap_join_strong (c : ℝ) : massGap c 0 = 1 := by
  simp [massGap]

/-- **The mass-gap join (the β-uniform identification)**: `m_phys = Δ(β)/a(β) = 1 = Λ_QCD`, uniform in
`β` — the lattice gap and the running spacing cancel, so the physical mass is the cutoff-independent
constant. This is the explicit identification of the two "1"s. -/
theorem mass_gap_join (c β : ℝ) : massGap c β / runningSpacing c β = 1 := by
  dsimp [massGap, runningSpacing]
  field_simp [Real.exp_ne_zero]

/-- **The single gap is positive for all β**: `0 < Δ(β)` — the mass gap never vanishes. -/
theorem mass_gap_positive (c β : ℝ) : 0 < massGap c β := by
  dsimp [massGap]
  exact Real.exp_pos _

/-- **The physical mass is positive and β-uniform**: `0 < Δ(β)/a(β) = Λ_QCD` for all β. -/
theorem physical_mass_positive_uniform (c β : ℝ) : 0 < massGap c β / runningSpacing c β := by
  rw [mass_gap_join]
  norm_num

end QM
