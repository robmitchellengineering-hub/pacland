import Mathlib
import PaclandProof.Gravity.Bianchi
import PaclandProof.Gravity.Lovelock

/-!
# Quantum gravity — the forced half

Constraint-first QG: the forced content is the *union* of QM's Born rule (Gleason — the unique
non-contextual probability rule) and gravity's Einstein equation (Lovelock — the unique
divergence-free theory). The free column is `{which outcome, G, Λ, and the QM-gravity coupling}`.
Here we kernel-check the one new forced condition that joins them: the **semiclassical
consistency** — because the Einstein tensor is divergence-free, its source (classical matter or a
quantum expectation value `⟨T_ab⟩`) must be conserved, `∇^a T_ab = 0`. This is the QG analog of
the SM's anomaly cancellation: it is what the coupling must satisfy, not what the theory predicts.
-/

namespace Gravity

open scoped BigOperators

noncomputable section

variable {n : ℕ}

/-- The divergence of the Einstein tensor `G_bd = R_bd − (R/2) g_bd`:
`∇·G = ∇·Ric − (1/2) ∇·(R g)`. -/
def divEinstein (gInv g : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n) : Fin n → ℝ :=
  fun d => divRicci gInv DR d - (1 / 2 : ℝ) *
    (∑ b : Fin n, ∑ e : Fin n, gInv b e * (covScalar gInv DR e * g b d))

/-- **The Einstein tensor is divergence-free** (`∇·G = 0`): Lovelock's theorem at `α = 1,
β = −1/2` — the divergence of `R_ab − (R/2) g_ab` is `(1/2 − 1/2) ∇R = 0`. -/
theorem einstein_divergence_free (gInv g : Fin n → Fin n → ℝ) (DR : CovDerivCurvature n)
    (h_symm : ∀ a b, gInv a b = gInv b a)
    (h_asym34 : ∀ e a b c d, DR e a b c d = - DR e a b d c)
    (h_asym12 : ∀ e a b c d, DR e a b c d = - DR e b a c d)
    (h_second : SecondBianchi DR)
    (h_inv : ∀ e d, (∑ b : Fin n, gInv b e * g b d) = if e = d then (1 : ℝ) else 0) :
    ∀ d, divEinstein gInv g DR d = 0 := by
  intro d
  dsimp [divEinstein]
  -- divRicci d - (1/2) (Σ gInv covScalar g) = 0, exactly Lovelock at α=1, β=-1/2.
  have h := lovelock_divergence gInv g DR h_symm h_asym34 h_asym12 h_second h_inv 1 (-1 / 2 : ℝ) d
  nlinarith [h]

end

end Gravity
