/-
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
import Mathlib
import PaclandProof.QM.AxialGauge
import PaclandProof.QM.AsymptoticFreedom

/-!
# The one-loop Yang–Mills β-function from the heat kernel (Seeley–DeWitt)

The one-loop β-function coefficient of pure SU(N) Yang–Mills in d = 4 is

  `b₀ = 11N/(48π²) = (11/3)·N · (1/(16π²))`.

This file kernel-checks the LOOP FACTOR: it shows that the `1/(16π²)` (the *universal*
heat-kernel constant) is the **evaluated output** of the heat trace of the free Laplacian on
flat ℝ⁴ — one Gaussian integral per dimension — rather than a typed constant. The full
coefficient is then assembled as

  `b₀ = (spin-1 F²-coefficient) · (adjoint Casimir) · (universal heat-kernel constant)`

and the number `11N/(48π²)` falls out of `field_simp`/`ring` on those pieces.

## What is derived here vs. what is a stated count

* **DERIVED (the universal constant).** `universalHeatKernelCoeff` is *defined* as the heat
  trace of the free scalar Laplacian on flat ℝ⁴ (the Gaussian integral `∫ e^{-‖p‖²} dp` divided
  by the phase-space volume `(2π)⁴`). `universalHeatKernelCoeff_eq` proves it *evaluates* to
  `1/(16π²)`. This is the "1/16π² falls out" step — it is the *conclusion*, not an input.
* **STATED (the group/tensor count).** `spinOneF2Coeff = 11/3` is the spin-1 heat-kernel
  `F²`-coefficient — the standard Gross–Wilczek–Politzer 1973 number, equivalently the
  `b₄`-coefficient of the gauge-field fluctuation operator. It is a *coefficient* (a
  group/tensor count), not derived from the Gaussian integral; deriving it from scratch needs
  the full spin-structure trace of the fluctuation operator, which is the literature result we
  cite. The `N` is the SU(N) adjoint Casimir `C₂(G) = N`.
* **The axial gauge** (already fixed in this repo — `QM.AxialGauge.axialGauge`, PR #489) is
  *ghost-free*: the two unphysical polarizations are removed by the gauge condition `n·A = 0`
  and the residual Gauss-law constraint, leaving the `d - 2 = 2` physical transverse
  polarizations (`physicalPolarizations_four` below).

## The two routes

The `1/(16π²)` is read off the *flat-space* heat trace (the Gaussian integral). The *flat
torus* route — `tr(e^{-tΔ}) = Σ_modes e^{-tλ}` — is the same universal constant, and its engine
is Jacobi's theta identity (`torus_heat_trace_theta` below), which mathlib already has as
`Real.tsum_exp_neg_mul_int_sq`. Both routes are recorded; the flat-space one is what we close.
-/

open scoped BigOperators

noncomputable section

namespace QM

namespace SeeleyDeWitt

open Real

/-- The symbol of (minus) the flat Laplacian `Δ = -∑ᵢ ∂ᵢ²` on ℝ⁴: `p ↦ ‖p‖²`. The gauge-field
fluctuation operator in the axial gauge is a matrix of such Laplacians on the transverse
polarizations (plus a constant gauge-coupling term); its heat kernel is governed by this symbol. -/
def laplacianSymbol (p : EuclideanSpace ℝ (Fin 4)) : ℝ := ‖p‖ ^ 2

/-- The heat trace of the free scalar Laplacian on flat ℝ⁴ (the momentum-space heat-kernel
trace, un-normalized): `∫ e^{-t·‖p‖²} d⁴p`. This is one Gaussian integral per spacetime
dimension, i.e. `(√(π/t))⁴ = π²/t²`. -/
def scalarHeatTrace (t : ℝ) : ℝ :=
  ∫ p : EuclideanSpace ℝ (Fin 4), Real.exp (-t * laplacianSymbol p)

/-- **The 4-dimensional Gaussian integral.** The heat trace of the free Laplacian on flat ℝ⁴ is
`π²/t²`: the four one-dimensional Gaussian integrals `∫ e^{-t x²} dx = √(π/t)` multiply to give
`(√(π/t))⁴ = π²/t²`. This is the heat-kernel `a₀` coefficient (the volume term) evaluated. -/
theorem scalarHeatTrace_eq {t : ℝ} (ht : 0 < t) :
    scalarHeatTrace t = Real.pi ^ 2 / t ^ 2 := by
  dsimp [scalarHeatTrace, laplacianSymbol]
  rw [GaussianFourier.integral_rexp_neg_mul_sq_norm ht]
  rw [finrank_euclideanSpace_fin]
  norm_num
  ring

/-- The universal heat-kernel constant: the heat trace of the free scalar Laplacian on flat ℝ⁴
at `t = 1`, normalized by the phase-space volume `(2π)⁴`. **Defined** as the Gaussian integral,
and **proven** below to evaluate to `1/(16π²)`. -/
def universalHeatKernelCoeff : ℝ :=
  scalarHeatTrace 1 / (2 * Real.pi) ^ 4

/-- **The universal constant `1/(16π²)` falls OUT of the heat kernel.** The heat trace of the
free Laplacian on flat ℝ⁴ evaluates to `π²`, and dividing by the phase-space volume `(2π)⁴`
gives exactly `1/(16π²)`. This is the Seeley–DeWitt universal coefficient as an *output* of the
Gaussian integral — not a typed constant. -/
theorem universalHeatKernelCoeff_eq :
    universalHeatKernelCoeff = 1 / (16 * Real.pi ^ 2) := by
  dsimp [universalHeatKernelCoeff]
  rw [scalarHeatTrace_eq (t := 1) (by norm_num : 0 < (1 : ℝ))]
  norm_num
  field_simp [Real.pi_ne_zero]
  ring

/-- **The flat-torus heat trace is self-dual (Jacobi's theta identity).** The mode-sum heat
trace of the scalar Laplacian on the flat circle is `Σₙ e^{-π a n²}`; Poisson summation gives
`Σₙ e^{-π a n²} = a^{-1/2} · Σₙ e^{-π n² / a}`. This is the engine of the `t → 0` heat-kernel
expansion on the torus, whose leading term is the same universal constant `1/(16π²)`.
(This is mathlib's `Real.tsum_exp_neg_mul_int_sq`, restated with its heat-trace meaning.) -/
theorem torus_heat_trace_theta {a : ℝ} (ha : 0 < a) :
    (∑' n : ℤ, Real.exp (-Real.pi * a * (n : ℝ) ^ 2)) =
      (1 : ℝ) / a ^ (1 / 2 : ℝ) * (∑' n : ℤ, Real.exp (-Real.pi / a * (n : ℝ) ^ 2)) := by
  simpa using Real.tsum_exp_neg_mul_int_sq ha

/-- A massless spin-1 field in `d` spacetime dimensions has `d - 2` physical (transverse)
polarizations. In the axial gauge (see `QM.AxialGauge`) the temporal polarization is removed by
the gauge condition `n·A = 0` and one further longitudinal polarization is removed by the
residual Gauss-law constraint, leaving exactly `d - 2`. -/
def physicalPolarizations (d : ℕ) : ℕ := d - 2

/-- **In d = 4 the massless gauge field has exactly 2 physical polarizations.** This is the
degree-of-freedom count of the axial gauge: `4 - 2 = 2`. -/
theorem physicalPolarizations_four : physicalPolarizations 4 = 2 := by
  norm_num [physicalPolarizations]

/-- The spin-1 Seeley–DeWitt `F²`-coefficient: for the gauge-field fluctuation operator in d = 4
the heat-kernel coefficient of `∫ F²` is `11/3` per unit of the adjoint Casimir (Gross–Wilczek–
Politzer 1973; the transverse-gluon loop's anti-screening coefficient). This is the group/tensor
*count* — the one deep constant, stated from the literature, not re-derived here. -/
def spinOneF2Coeff : ℝ := 11 / 3

/-- **The one-loop β-function coefficient equals the assembled Seeley–DeWitt coefficient.** For
SU(N), `b₀ = (11/3) · N · (1/16π²)`: the spin-1 `F²`-coefficient times the adjoint Casimir `N`
times the universal heat-kernel constant (derived in `universalHeatKernelCoeff_eq`). -/
theorem oneLoopBeta_eq_heatKernel (N : ℝ) :
    QM.betaFunctionCoefficient N = spinOneF2Coeff * N * universalHeatKernelCoeff := by
  rw [universalHeatKernelCoeff_eq]
  dsimp [QM.betaFunctionCoefficient, spinOneF2Coeff]
  field_simp [Real.pi_ne_zero]
  ring

/-- **The Seeley–DeWitt coefficient evaluates to `11N/(48π²)`.** The `11/(48π²)` is the *output*
of `field_simp`/`ring` on the derived pieces `(11/3) · N · (1/16π²)` — the universal constant
`1/(16π²)` came out of the heat kernel above, and the `11/3` is the spin-1 group/tensor count. -/
theorem seeleyDeWittCoeff_evaluates (N : ℝ) :
    spinOneF2Coeff * N * universalHeatKernelCoeff = 11 * N / (48 * Real.pi ^ 2) := by
  rw [universalHeatKernelCoeff_eq]
  dsimp [spinOneF2Coeff]
  field_simp [Real.pi_ne_zero]
  ring

/-- **The full chain**: the one-loop β-function coefficient is the evaluated Seeley–DeWitt
coefficient, and it equals `11N/(48π²)`. -/
theorem oneLoopBeta_from_heatKernel (N : ℝ) :
    QM.betaFunctionCoefficient N = 11 * N / (48 * Real.pi ^ 2) := by
  rw [oneLoopBeta_eq_heatKernel]
  exact seeleyDeWittCoeff_evaluates N

end SeeleyDeWitt

end QM
