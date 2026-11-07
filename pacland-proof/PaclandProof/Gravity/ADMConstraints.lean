import Mathlib
import PaclandProof.Gravity.ADM

/-!
# The ADM constraint system — momentum, momentum constraint, and the full pair

Rung 2 of the QG library build. The ADM momentum is the trace-reversed extrinsic curvature,
`π_ab = K_ab − (tr K) q_ab` (its trace is `tr_q(π) = (1 − tr_q(q)) tr_q(K)`, i.e. reversed by the
factor `−(n−1)` for the metric); the **momentum constraint** is its divergence-freeness
`∇_b π^b_a = 0` — the companion to the Hamiltonian constraint, and the other half of the forced QG
constraint system `{Ĥ = 0, Ĥ_a = 0}` (which encodes diffeomorphism invariance).
-/

namespace Gravity

open scoped BigOperators

noncomputable section

variable {n : ℕ}

/-- The trace of a 2-tensor `X` with the 3-metric: `tr_q(X) = q^ab X_ab`. -/
def traceK (q X : Fin n → Fin n → ℝ) : ℝ :=
  ∑ a : Fin n, ∑ b : Fin n, q a b * X a b

/-- The **ADM momentum**: `π_ab = K_ab − (tr K) q_ab` — the trace-reversed extrinsic curvature. -/
def momentum (q K : Fin n → Fin n → ℝ) (a b : Fin n) : ℝ :=
  K a b - traceK q K * q a b

/-- **The momentum constraint**: `∇_b π^b_a = 0` — the momentum is divergence-free. This is the
companion to the Hamiltonian constraint (as the Einstein tensor's divergence-freeness `∇·G = 0` is
to the Hamiltonian constraint, so `∇·π = 0` is to the momentum constraint). -/
def momentumConstraint (gInv : Fin n → Fin n → ℝ) (Dπ : Fin n → Fin n → Fin n → ℝ) (a : Fin n) : ℝ :=
  ∑ b : Fin n, ∑ e : Fin n, gInv b e * Dπ e b a

/-- **The full ADM constraint system** — the forced content of QG: the Hamiltonian constraint
`Ĥ = G^abcd π_ab π_cd − R = 0` and the momentum constraint `Ĥ_a = ∇_b π^b_a = 0`. A physical
3-geometry `(q, π)` is one on which both vanish. -/
def admConstraints (q : Fin n → Fin n → ℝ) (π : Fin n → Fin n → ℝ) (R : ℝ)
    (gInv : Fin n → Fin n → ℝ) (Dπ : Fin n → Fin n → Fin n → ℝ) : Prop :=
  hamiltonianConstraint q π R = 0 ∧ (∀ a : Fin n, momentumConstraint gInv Dπ a = 0)

end

end Gravity
