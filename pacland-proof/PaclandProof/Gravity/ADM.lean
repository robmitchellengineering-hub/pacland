import Mathlib

/-!
# The ADM constraint — the DeWitt supermetric and the Hamiltonian constraint (algebraic core)

The first seed of the QG library build (see `docs/qg-library-build.md`): the **DeWitt supermetric**
`G^abcd = (1/2)(q^ac q^bd + q^ad q^bc) − q^ab q^cd` — the metric on superspace (the space of
3-geometries) that defines the kinetic term of the Hamiltonian constraint. It is pure finite-index
algebra (no manifold machinery), so its symmetries and its role in `Ĥ` are kernel-checkable now.

The Hamiltonian constraint (the Wheeler–DeWitt operator's classical core) is then
`Ĥ = G^abcd π_ab π_cd − R(³) = 0` — kinetic term (supermetric-contracted momenta) minus the
potential term (the 3-scalar curvature).
-/

namespace Gravity

open scoped BigOperators

noncomputable section

variable {n : ℕ}

/-- The **DeWitt supermetric** on superspace. -/
def supermetric (q : Fin n → Fin n → ℝ) (a b c d : Fin n) : ℝ :=
  (1 / 2 : ℝ) * (q a c * q b d + q a d * q b c) - q a b * q c d

/-- The supermetric is symmetric under `(ab) ↔ (cd)` (for a symmetric 3-metric `q`). -/
theorem supermetric_sym_pairs (q : Fin n → Fin n → ℝ) (hq : ∀ a b, q a b = q b a)
    (a b c d : Fin n) :
    supermetric q a b c d = supermetric q c d a b := by
  dsimp [supermetric]
  rw [hq c a, hq d b, hq c b, hq d a]
  ring

/-- The supermetric is symmetric under `a ↔ b` (for a symmetric 3-metric `q`). -/
theorem supermetric_sym_indices (q : Fin n → Fin n → ℝ) (hq : ∀ a b, q a b = q b a)
    (a b c d : Fin n) :
    supermetric q a b c d = supermetric q b a c d := by
  dsimp [supermetric]
  rw [hq a b]
  ring

/-- The **Hamiltonian constraint** (algebraic core): `Ĥ = G^abcd π_ab π_cd − R = 0` — the kinetic
term (the momenta contracted with the supermetric) minus the potential term (the densitized
3-scalar curvature). This is the classical shadow of the Wheeler–DeWitt operator. -/
def hamiltonianConstraint (q : Fin n → Fin n → ℝ) (π : Fin n → Fin n → ℝ) (R : ℝ) : ℝ :=
  (∑ a : Fin n, ∑ b : Fin n, ∑ c : Fin n, ∑ d : Fin n,
    supermetric q a b c d * π a b * π c d) - R

end

end Gravity
