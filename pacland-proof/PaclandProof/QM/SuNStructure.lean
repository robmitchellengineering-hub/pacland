import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The SU(N) adjoint Casimir = N (kernel-checked, explicit su(2))

The one-loop Yang–Mills β-function needs one group-theoretic factor: the quadratic Casimir of the
adjoint representation, `C₂(G) = N`, i.e. `f^{abc} f^{dbc} = N · δ^{ad}`. This file proves it for the
explicit case **N = 2** (`su(2)`, the structure constants being the Levi-Civita symbol `ε^{abc}`), so
that the `N` on the right-hand side is the **evaluated trace of the adjoint representation**, not a
constant that is typed in.

Two conventions are both present, and are both kernel-checked:

* **The structure-constant contraction** (the literal statement): `∑_{b,c} f^{abc} f^{dbc} = N·δ^{ad}`.
  Over `ℤ` this is positive: the sum evaluates to `2·δ^{ad}` (theorem `su2_structure_constant_identity`).

* **The trace form** (the physics convention `(ad Tᵃ)_{bc} = -i f^{abc}`, so that the generators are
  anti-Hermitian and `tr(ad Tᵃ · ad Tᵇ) = N·δ^{ab}` is positive): the trace is computed over the
  3×3 adjoint matrices and evaluates to `N = 2` (theorem `su2_adjoint_trace_identity`).

The Casimir itself (`∑_a (ad Tᵃ)²`, normalized by `dim su(2) = 3`) is *defined as a trace* and proved
equal to `2` — the `2` is the **output** of that trace (theorem `su2_adjoint_casimir`). There is no
`def ... := 2` anywhere: the value `N = 2` is always computed.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The Levi-Civita symbol on three indices: `ε i j k` is `+1` for the even permutations of
`(0,1,2)`, `-1` for the odd ones, and `0` otherwise. These are the **structure constants of su(2)**:
`f^{abc} = ε^{abc}`. -/
def su2LeviCivita (i j k : Fin 3) : ℤ :=
  if i.val = 0 ∧ j.val = 1 ∧ k.val = 2 then 1
  else if i.val = 1 ∧ j.val = 2 ∧ k.val = 0 then 1
  else if i.val = 2 ∧ j.val = 0 ∧ k.val = 1 then 1
  else if i.val = 0 ∧ j.val = 2 ∧ k.val = 1 then -1
  else if i.val = 2 ∧ j.val = 1 ∧ k.val = 0 then -1
  else if i.val = 1 ∧ j.val = 0 ∧ k.val = 2 then -1
  else 0

/-- The structure constants of su(2): `f^{abc} = ε^{abc}` (the totally antisymmetric symbol). -/
def su2StructureConstant (a b c : Fin 3) : ℤ := su2LeviCivita a b c

/-- **The literal one-loop group factor, kernel-checked**: `f^{abc} f^{dbc} = N · δ^{ad}` with
`N = 2`. The sum over the two repeated indices evaluates to `2 · δ^{ad}` — this `2` is the *output*
of the sum (= the adjoint index `T(G) = C₂(G) = N`), not a constant typed on the right. -/
theorem su2_structure_constant_identity (a d : Fin 3) :
    (∑ b : Fin 3, ∑ c : Fin 3, su2StructureConstant a b c * su2StructureConstant d b c)
      = 2 * (if a = d then 1 else 0) := by
  fin_cases a <;> fin_cases d <;>
    norm_num [su2StructureConstant, su2LeviCivita, Fin.sum_univ_three]

/-- The adjoint representation matrices of su(2), physics convention: `(ad Tᵃ)_{bc} = -i · f^{abc}`.
These are `-i` times the three so(3) generators (angular-momentum matrices `Jᵃ`), and they satisfy
`tr(ad Tᵃ · ad Tᵇ) = N · δ^{ab}`. -/
def su2AdjointMatrix (a : Fin 3) : Matrix (Fin 3) (Fin 3) ℂ :=
  fun b c => -Complex.I * (su2LeviCivita a b c : ℂ)

/-- **The adjoint Killing form is the trace, and the trace evaluates to `N`**:
`tr(ad Tᵃ · ad Tᵇ) = N · δ^{ab}` with `N = 2`. The `2` on the right is what the trace over the
3×3 adjoint matrices computes to (for `a = b` the trace of `(ad Tᵃ)²` is exactly `N`); it is the
evaluated trace of the adjoint representation, not a constant typed in. -/
theorem su2_adjoint_trace_identity (a b : Fin 3) :
    Matrix.trace (su2AdjointMatrix a * su2AdjointMatrix b)
      = (2 : ℂ) * (if a = b then 1 else 0) := by
  fin_cases a <;> fin_cases b <;>
    norm_num [su2AdjointMatrix, su2LeviCivita, Matrix.trace, Matrix.mul_apply, Fin.sum_univ_three]

/-- The quadratic Casimir of the adjoint representation of su(2), **defined as a trace**: the trace
of `∑_a (ad Tᵃ)²`, normalized by the dimension `dim su(2) = 3`. No value is typed in — the theorem
below computes it. -/
def su2AdjointCasimir : ℂ :=
  (∑ a : Fin 3, Matrix.trace (su2AdjointMatrix a * su2AdjointMatrix a)) / 3

/-- **`C₂(G) = N`, kernel-checked**: the adjoint Casimir, computed as the trace of `∑_a (ad Tᵃ)²`
divided by `dim = 3`, evaluates to `2`. This `2` is the **output** of the trace — the quadratic
Casimir of the adjoint representation of su(2) is `N = 2`. -/
theorem su2_adjoint_casimir : su2AdjointCasimir = 2 := by
  norm_num [su2AdjointCasimir, su2AdjointMatrix, su2LeviCivita,
    Matrix.trace, Matrix.mul_apply, Fin.sum_univ_three]

/-- The diagonal (`a = b`) reading of the trace identity: `tr((ad Tᵃ)²) = N` for every generator —
the trace of the square of each adjoint matrix is exactly the Casimir `N = 2`. -/
theorem su2_adjoint_square_trace (a : Fin 3) :
    Matrix.trace (su2AdjointMatrix a * su2AdjointMatrix a) = (2 : ℂ) := by
  simpa using su2_adjoint_trace_identity a a

end QM
