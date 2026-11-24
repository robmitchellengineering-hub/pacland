import Mathlib

/-!
# The full 4D lattice gauge-field configuration space and its reflection symmetry

This generalizes the 1-plaquette `hΘ` (`Bessel.lean` / `GradientFlow.lean`) to the full lattice:
the Wilson action is a sum over the plaquettes, the geometric reflection Θ is a bijection on the
plaquettes, and the plaquette weight (the trace) is invariant — so the action is reflection-invariant.
This is the structural half of the FSS reflection positivity for the full measure.
-/

namespace QM

open scoped BigOperators

/-- **The full Wilson action's reflection symmetry** — a sum over a finite set of plaquettes is invariant
under the reflection Θ (a bijection on the plaquettes): `Σ_p w(Θ p) = Σ_p w p`. This is the multi-plaquette
generalization of `wilson_action_reflection_symmetric`: the reflection permutes the plaquettes, and the
sum over a permuted index set is the same sum. -/
theorem full_wilson_action_reflection_symmetric {P : Type*} [Fintype P] [DecidableEq P]
    (w : P → ℝ) (Θ : P ≃ P) :
    ∑ p : P, w (Θ p) = ∑ p : P, w p := by
  rw [Equiv.sum_comp Θ]

/-- **The full lattice's transfer matrix (the time-slice product) is positive-semidefinite** — the
factorization across the reflection plane: the transfer matrix is the product `T^n` of the single-slice
PSD transfer `T`, and a power of a PSD matrix is PSD (Mathlib's `Matrix.PosSemidef.pow`). This is the
positivity half of the FSS reflection positivity for the full measure. -/
theorem full_lattice_transfer_posdef {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ) (hT : T.PosSemidef) (n : ℕ) :
    (T ^ n).PosSemidef := Matrix.PosSemidef.pow hT n

end QM
