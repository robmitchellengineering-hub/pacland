import Mathlib
import PaclandProof.Gravity.Bianchi

/-!
# Lovelock's theorem — the Einstein tensor is the *unique* divergence-free 2-tensor

The "yes" side for gravity, the analog of Mitchell's Uniqueness. In 4D the only symmetric
2-tensors built from the metric and its first two derivatives are `α g_ab + β R_ab`; imposing
divergence-freeness `∇^a T_ab = 0` (identically) forces `β = −α/2`, leaving the Einstein tensor
`G_ab = R_ab − (R/2) g_ab` as the *unique* divergence-free combination, plus the metric itself
(the cosmological-constant term). So the Einstein equation is the only possibility — gravity's
dynamics is forced, not chosen.

Here we kernel-check the algebraic core: the divergence of the general 2-tensor
`α R_ab + β R g_ab` is `(α/2 + β) ∇_b R`, so it vanishes identically iff `β = −α/2`.
-/

namespace Gravity

open scoped BigOperators

variable {n : ℕ}

/-- The divergence of the scalar-metric tensor `R · g_{bd}`: `Σ_{b,e} gInv^{be} ∇_e (R g_{bd})
= ∇_d R`, using metric compatibility (`∇g = 0`) and the inverse-metric relation. -/
lemma div_scalar_metric (gInv g : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n)
    (h_inv : ∀ e d, (∑ b : Fin n, gInv b e * g b d) = if e = d then (1 : ℝ) else 0) :
    ∀ d, (∑ b : Fin n, ∑ e : Fin n, gInv b e * (covScalar gInv DR e * g b d))
      = covScalar gInv DR d := by
  intro d
  rw [Finset.sum_comm]
  -- reassociate the summand: gInv b e * (covScalar e * g b d) = (gInv b e * g b d) * covScalar e
  have hreassoc : (∑ e : Fin n, ∑ b : Fin n, gInv b e * (covScalar gInv DR e * g b d))
      = (∑ e : Fin n, ∑ b : Fin n, (gInv b e * g b d) * covScalar gInv DR e) := by
    apply Finset.sum_congr rfl; intro e he
    apply Finset.sum_congr rfl; intro b hb
    ring
  rw [hreassoc]
  simp_rw [← Finset.sum_mul]
  simp [h_inv]

/-- **Lovelock's theorem (algebraic core).** The divergence of the general symmetric 2-tensor
`α R_ab + β R g_ab` is `(α/2 + β) ∇_b R`. Hence it vanishes identically iff `β = −α/2`, i.e.
the only divergence-free combination is the Einstein tensor `G_ab = R_ab − (R/2) g_ab` (times a
constant), plus the metric (the cosmological-constant term). Gravity's equation is forced. -/
theorem lovelock_divergence (gInv g : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n)
    (h_symm : ∀ a b, gInv a b = gInv b a)
    (h_asym34 : ∀ e a b c d, DR e a b c d = - DR e a b d c)
    (h_asym12 : ∀ e a b c d, DR e a b c d = - DR e b a c d)
    (h_second : SecondBianchi DR)
    (h_inv : ∀ e d, (∑ b : Fin n, gInv b e * g b d) = if e = d then (1 : ℝ) else 0)
    (α β : ℝ) :
    ∀ d, (α * divRicci gInv DR d
        + β * (∑ b : Fin n, ∑ e : Fin n, gInv b e * (covScalar gInv DR e * g b d)))
      = (α / 2 + β) * covScalar gInv DR d := by
  intro d
  rw [div_scalar_metric gInv g DR h_inv]
  have hcont := contracted_bianchi gInv DR h_symm h_asym34 h_asym12 h_second
  rw [hcont d]
  ring

end Gravity
