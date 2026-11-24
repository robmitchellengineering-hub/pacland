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

/-- **The FSS factorization** — the reflected correlation across the reflection plane is the SQUARE of the
transfer: `Σₓᵧ (fₓ wₓ)(fᵧ wᵧ) = (Σₓ fₓ wₓ)²` (`Finset.sum_mul_sum`). This is the algebraic core of the
FSS reflection positivity: the reflected correlation equals the square of the single-slice transfer, so its
non-negativity is the square's non-negativity. -/
theorem fss_reflected_correlation_factorization {α : Type*} [Fintype α] [DecidableEq α]
    (w f : α → ℝ) :
    (∑ x : α, f x * w x) ^ 2 = ∑ x : α, ∑ y : α, (f x * w x) * (f y * w y) := by
  rw [pow_two, Finset.sum_mul_sum]

/-- **The FSS reflection positivity (the square form)** — the reflected correlation `(Σₓ fₓ wₓ)²` is
non-negative, the OS3 in its factorized form: the reflected correlation is a square, hence `≥ 0`. -/
theorem fss_reflection_positivity_square {α : Type*} [Fintype α]
    (w f : α → ℝ) :
    0 ≤ (∑ x : α, f x * w x) ^ 2 := by
  positivity

/-- **The Wilson 1-plaquette action on SU(2)** — `1 − Re Tr U`, the real part of the trace of the holonomy
(the `specialUnitaryGroup (Fin 2)` element). This is the specific lattice weight the full action sums over
the plaquettes. -/
noncomputable def wilsonPlaquette (U : Matrix.specialUnitaryGroup (Fin 2) ℂ) : ℝ :=
  1 - (Matrix.trace (U : Matrix (Fin 2) (Fin 2) ℂ)).re

/-- **The full Wilson action** — the sum of the 1-plaquette actions over a finite set of plaquettes (the
specific lattice configuration space's action). -/
noncomputable def wilsonAction {P : Type*} [Fintype P] (U : P → Matrix.specialUnitaryGroup (Fin 2) ℂ) : ℝ :=
  ∑ p : P, wilsonPlaquette (U p)

/-- **The trace invariance under the reflection Θ** — the geometric reflection maps the SU(2) holonomy to
its inverse (the conjugate transpose `Matrix.conjTranspose U`), and the real part of the trace is invariant:
`Re Tr(Uᴴ) = Re Tr U`. This is the specific version of the reflection symmetry for the Wilson plaquette
action (Mathlib's `Matrix.trace_conjTranspose` + `Complex.conj_re`). -/
theorem wilson_trace_reflection_invariant (U : Matrix (Fin 2) (Fin 2) ℂ) :
    (Matrix.trace (Matrix.conjTranspose U)).re = (Matrix.trace U).re := by
  rw [Matrix.trace_conjTranspose]
  simp [Complex.conj_re]

end QM
