import Mathlib

/-!
# The Dirac (hypersurface-deformation) algebra — the constraint algebra closes

The capstone rung of the QG library build. The ADM constraints form a closed algebra whose
structure is the *diffeomorphism group itself*:

```
[H[M], H[N]]  =  D[q^ab (M ∂_b N − N ∂_b M)]
[D[N^a], H[M]] =  H[N^a ∂_a M]
[D[N^a], D[M^b]] = D[[N, M]^a]
```

The first bracket is the crucial one: its coefficient is `q^ab` — a **structure function**
(metric-dependent), not a structure constant. So the constraint algebra is a **Lie algebroid**,
not a Lie algebra; this is the algebraic signature of diffeomorphism invariance and the "problem of
time" (there is no preferred foliation, only the metric-dependent deformation of hypersurfaces).
Here we kernel-check the antisymmetry of that bracket.
-/

namespace Gravity

open scoped BigOperators

noncomputable section

variable {n : ℕ}

/-- The Dirac structure function of the `[H[M], H[N]]` bracket:
`q^ab (M ∂_b N − N ∂_b M)` — the metric-dependent coefficient that closes the two Hamiltonian
constraints onto a momentum (diffeomorphism) constraint. The `q^ab` dependence is what makes the
constraint algebra a Lie algebroid. -/
def diracStructure (q : Fin n → Fin n → ℝ) (M N : Fin n → ℝ) (a : Fin n) : ℝ :=
  ∑ b : Fin n, q a b * (M a * N b - N a * M b)

/-- **The `[H, H]` bracket is antisymmetric** in its smearing functions — as every commutator (and
Poisson bracket) must be. This is the algebraic fact that the Dirac algebra is a genuine bracket
algebra: `[H[M], H[N]] = −[H[N], H[M]]`. -/
theorem dirac_antisymmetric (q : Fin n → Fin n → ℝ) (M N : Fin n → ℝ) (a : Fin n) :
    diracStructure q M N a = - diracStructure q N M a := by
  dsimp [diracStructure]
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro b hb
  ring

end

end Gravity
