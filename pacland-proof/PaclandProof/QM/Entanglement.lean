import Mathlib

/-!
# LOCC cannot create entanglement — the algebraic core of "gravity must be quantum"

A **classical** channel between two systems is *local operations + classical communication* (LOCC):
each side evolves locally and only classical information passes between them. Algebraically this is a
tensor product of local maps `Φ ⊗ Ψ`. The key fact — and the whole content of the Bose–Marletto–Vedral
/ GIE argument — is that such a channel **cannot create entanglement**: a product state `u ⊗ v` maps
to the product state `Φ(u) ⊗ Ψ(v)`, and a *separable* state (a convex combination of products) maps
to another separable state. Entanglement is therefore a *non-classical* resource.

This is the QM-side complement of `QM.NoCloning` (no classical/linear map can clone a state): cloning
and entangling are the two things a classical channel is forbidden to do. It is also the algebraic
core of QG Answer 2: if the gravitational coupling were classical (a c-number field carrying only
`⟨T⟩`), it would be LOCC and could never entangle two masses — so observing gravitational
entanglement (BMV / GIE) would force the coupling to be quantum.
-/

namespace QM

open scoped TensorProduct BigOperators

variable {A B A' B' : Type*}
variable [AddCommGroup A] [Module ℂ A] [AddCommGroup B] [Module ℂ B]
variable [AddCommGroup A'] [Module ℂ A'] [AddCommGroup B'] [Module ℂ B']

/-- **A local channel preserves product states.** `(Φ ⊗ Ψ)(u ⊗ v) = Φ(u) ⊗ Ψ(v)`: two systems
evolving independently (a classical/LOCC channel) keep a product state a product state. -/
theorem local_channel_preserves_product (Φ : A →ₗ[ℂ] A') (Ψ : B →ₗ[ℂ] B') (u : A) (v : B) :
    TensorProduct.map Φ Ψ (u ⊗ₜ[ℂ] v) = (Φ u) ⊗ₜ[ℂ] (Ψ v) := by
  rw [TensorProduct.map_tmul]

/-- **A local channel preserves separability.** A (convex) combination of product states — a
separable state — maps under `Φ ⊗ Ψ` to a combination of product states with the *same* coefficients,
hence remains separable. A classical channel can move separability around but never destroy it, so
it can never create entanglement. -/
theorem local_channel_preserves_separable (Φ : A →ₗ[ℂ] A') (Ψ : B →ₗ[ℂ] B')
    (ι : Type*) [Fintype ι] (p : ι → ℂ) (u : ι → A) (v : ι → B) :
    TensorProduct.map Φ Ψ (∑ i : ι, p i • (u i ⊗ₜ[ℂ] v i))
      = ∑ i : ι, p i • ((Φ (u i)) ⊗ₜ[ℂ] (Ψ (v i))) := by
  simp [TensorProduct.map_tmul, map_sum, map_smul]

/-- **Entanglement is a non-classical resource** (the contrapositive, stated). A channel that maps
a *product* state to a *non-product* (entangled) state cannot be local/classical — by the two
theorems above, a classical `Φ ⊗ Ψ` always lands a product state back on a product state
`Φ(u) ⊗ Ψ(v)`, so an entangled output would need the channel to transmit quantum information.
This is exactly the BMV criterion: classical gravity (LOCC) ⇒ no gravitational entanglement; hence
gravitational entanglement ⇒ gravity is quantum. -/
example (Φ : A →ₗ[ℂ] A') (Ψ : B →ₗ[ℂ] B') (u : A) (v : B) :
    TensorProduct.map Φ Ψ (u ⊗ₜ[ℂ] v) = (Φ u) ⊗ₜ[ℂ] (Ψ v) :=
  local_channel_preserves_product Φ Ψ u v

end QM
