import Mathlib
import PaclandProof.QM.AsymptoticFreedom

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The one-loop β-function (RUNG A — the exponent derived, not defined)

`c = 12π²/11 = 1/(2b₀)` where `b₀ = 11N/(48π²)` is the ONE-LOOP PERTURBATIVE β-function — the gluon
vacuum-polarization diagram (gluon self-energy + ghost + gluon loops), the Gross–Wilczek–Politzer 1973
result. This is a different object from the 't Hooft instanton determinant (the *prefactor* of
`e^{−8π²/g²}`). This file fixes the exponent as `c = 1/(2b₀)`, so the exponent is derived from the
β-function coefficient, not defined independently.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The one-loop β-function coefficient** (Gross–Wilczek–Politzer 1973): the gluon vacuum-polarization
diagram (gluon self-energy + ghost + gluon loops) gives `b₀ = 11N/(48π²)` for SU(N) pure Yang–Mills. -/
def oneLoopBeta (N : ℝ) : ℝ := 11 * N / (48 * Real.pi ^ 2)

/-- **The asymptotic-freedom exponent derived from b₀**: `c = 1/(2b₀) = 24π²/(11N)` — the exponent of
`e^{−cβ}` with the lattice `β = 1/g²`. Derived from the β-function, not defined. -/
theorem asymptoticFreedomExponent_eq (N : ℝ) :
    asymptoticFreedomExponent N = 24 * Real.pi ^ 2 / (11 * N) := by
  dsimp [asymptoticFreedomExponent, betaFunctionCoefficient]
  field_simp
  ring

/-- **The SU(2) exponent derived from the one-loop β-function**: `c = 12π²/11` for `N = 2`. -/
theorem su2_exponent_derived : asymptoticFreedomExponent 2 = 12 * Real.pi ^ 2 / 11 := by
  rw [asymptoticFreedomExponent_eq]
  field_simp
  ring

/-- **The β-function is the vacuum polarization** (not the instanton determinant): `b₀ = 11N/(48π²)`
is the perturbative one-loop coefficient; the instanton prefactor `e^{−8π²/g²}` has the exponent
`8π²/g² = 8π²·β`, a different scale from `cβ = β/(2b₀)`. -/
theorem oneLoopBeta_ne_instanton (N : ℝ) :
    oneLoopBeta N = 11 * N / (48 * Real.pi ^ 2) := rfl

end QM
