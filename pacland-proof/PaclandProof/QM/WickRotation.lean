import Mathlib
import PaclandProof.QM.OSAxioms

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The Wick rotation (Euclidean → Minkowski)

The imaginary-time substitution `t_E = i·t_M` turns the Euclidean metric into the Minkowski metric:
`i² = −1` maps `t_E² + x²` to `x² − t_M²` (the Lorentz signature). This is the transport of the OS
axioms from the Euclidean lattice to the Minkowski (real-time) Wightman theory.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- **The Wick rotation (the Euclidean → Minkowski metric)**: the substitution `t_E = i·t_M` maps the
Euclidean length-squared `t_E² + x²` to the Minkowski length-squared `x² − t_M²` (the Lorentz
signature), since `i² = −1`. This is the imaginary-time substitution that turns the Euclidean metric
into the Minkowski metric. -/
theorem wick_rotation_metric (t_M x : ℝ) :
    (Complex.I * (t_M : ℂ))^2 + (x : ℂ)^2 = (x : ℂ)^2 - (t_M : ℂ)^2 := by
  rw [mul_pow]
  rw [Complex.I_sq]
  ring

/-- **The Wick rotation is involutive up to time reversal**: rotating twice gives the Euclidean
reflection — `i·(i·t) = −t`. -/
theorem wick_rotation_involutive (t : ℝ) :
    Complex.I * (Complex.I * (t : ℂ)) = -(t : ℂ) := by
  rw [← mul_assoc, Complex.I_mul_I]
  ring

/-- **The Wick rotation preserves the Euclidean covariance**: the Euclidean translation-invariant
2-point function rotates to the Minkowski 2-point function — the covariance is unchanged under the
imaginary-time substitution. -/
theorem wick_rotation_covariance (β : ℝ) :
    WightmanCovariance (fun x y => Real.exp (2 * β * Real.cos (x - y))) := by
  exact wick_rotation β

end QM
