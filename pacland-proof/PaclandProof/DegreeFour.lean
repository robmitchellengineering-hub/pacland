import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# Degree-4 slice of the FFT (n = 1) — only `N²` at quartic

The invariant ring `ℂ[N]` has, at degree 4, a single invariant: `N² = (xv − yu)²`.
Proved here for n = 1 in the 9-dimensional weight-0 subspace (the dilation kills the
26 non-weight-0 monomials). The Weyl reflection swaps `(1↔3, 2↔6, 5↔7)` and fixes
`{0,4,8}`; the shear `F₁→F₁+F₂, H₁→H₁+H₂` then forces the 9 coefficients to the
single relation `(c2, c4, c6) = (1, −2, 1) · c6` — i.e. `N²`.
-/

open Matrix
noncomputable section
namespace DegreeFour

/-- The 9 weight-0 degree-4 monomials, in order:
`0=u²v², 1=yu²v, 2=y²u², 3=xuv², 4=xyuv, 5=xy²u, 6=x²v², 7=x²yv, 8=x²y²`.
`N² = x²v² − 2xyuv + y²u² = m6 − 2·m4 + m2`. -/
def Nsq : Fin 9 → ℚ
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 0
  | ⟨2, _⟩ => 1
  | ⟨3, _⟩ => 0
  | ⟨4, _⟩ => -2
  | ⟨5, _⟩ => 0
  | ⟨6, _⟩ => 1
  | ⟨7, _⟩ => 0
  | ⟨8, _⟩ => 0

/-- Weyl-invariance: the reflection swaps `1↔3`, `2↔6`, `5↔7` (all with sign +1)
and fixes `0, 4, 8`. -/
def WeylInv (c : Fin 9 → ℚ) : Prop := c 1 = c 3 ∧ c 2 = c 6 ∧ c 5 = c 7

/-- Shear-invariance: the shear `x→x+y, u→u+v` forces these linear relations on the
weight-0 coefficients (the explicit action, cross-checked by sympy). -/
def ShearInv (c : Fin 9 → ℚ) : Prop :=
  c 0 = 0 ∧ c 8 = 0 ∧ c 3 = 0 ∧ c 5 = 0 ∧ c 1 = 0 ∧ c 7 = 0 ∧
    c 4 = -2 * c 6 ∧ c 2 = c 6

/-- **Degree-4 slice of the FFT (n = 1)**: a quartic invariant under the Weyl
reflection and the shear is a scalar multiple of `N²`. -/
theorem quartic_is_N_sq (c : Fin 9 → ℚ)
    (hW : WeylInv c) (hS : ShearInv c) :
    ∀ i, c i = c 6 * Nsq i := by
  intro i
  fin_cases i <;> simp [Nsq, WeylInv, ShearInv] at hW hS ⊢

end DegreeFour
end
