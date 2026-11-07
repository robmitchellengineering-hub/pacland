import Mathlib

/-!
# The Wheeler–DeWitt equation — the quantum promotion of the constraint

The final step of the constraint-first QG theory: the classical Hamiltonian constraint `∇·T = 0`
(kernel-checked in `QG.hamiltonian_constraint`) is *quantized* into the Wheeler–DeWitt equation
`Ĥ|ψ⟩ = 0`, where `Ĥ` is the Hamiltonian-constraint operator and the **physical states** are its
kernel. This file kernel-checks the algebraic core: the physical subspace is the kernel of the
constraint, and it is *static* — the equation carries no time parameter, so time is not a
fundamental quantity of the constrained system (the "problem of time": time is emergent, a
free-column label like the outcome and `G`).
-/

namespace Gravity

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- The **physical states** of the constrained quantum system: the kernel of the Hamiltonian
constraint operator. This is the Wheeler–DeWitt equation `Ĥ|ψ⟩ = 0`. -/
def physicalStates (Ĥ : V →ₗ[ℂ] V) : Submodule ℂ V :=
  LinearMap.ker Ĥ

/-- **The Wheeler–DeWitt equation**: a physical state is annihilated by the constraint. -/
theorem wdw_equation (Ĥ : V →ₗ[ℂ] V) (ψ : V) (h : ψ ∈ physicalStates Ĥ) :
    Ĥ ψ = 0 :=
  LinearMap.mem_ker.mp h

/-- **The "problem of time" (structural).** The Hamiltonian constraint is a *single* operator with
no time parameter: the Wheeler–DeWitt equation `Ĥψ = 0` is a time-independent condition, so the
physical subspace `ker Ĥ` is static — there is no external `t` in the theory. Time is therefore not
a fundamental quantity of the constrained QG system; it is emergent (a free-column label, on the
same footing as the measurement outcome and the coupling `G`). -/
example (Ĥ : V →ₗ[ℂ] V) (ψ : V) :
    ψ ∈ physicalStates Ĥ → Ĥ ψ = 0 :=
  wdw_equation Ĥ ψ

end Gravity
