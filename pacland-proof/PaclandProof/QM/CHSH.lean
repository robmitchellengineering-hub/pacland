import Mathlib

/-!
# Bell's theorem — the CHSH inequality (the locality no-go)

The falsification rung that excludes *local* hidden variables. Alice has two measurement
settings `a0, a1`, Bob two `b0, b1`, each with outcome ±1. A local hidden-variable theory
assigns a definite value to each, so the CHSH correlation

    S = a0·b0 + a0·b1 + a1·b0 − a1·b1

must satisfy `S ≤ 2`. Quantum mechanics saturates `S = 2√2` (the Tsirelson bound), so
locality is falsified. Here we kernel-check the forced half: **no deterministic local
assignment can exceed 2**. (The quantum-violation half `2√2` is a separate, tensor-level
computation.)

The proof is a pure case analysis: `S = (a0+a1)b0 + (a0−a1)b1`, and for `a0, a1 ∈ {±1}`
exactly one of `a0+a1, a0−a1` is nonzero (equal to ±2), so `S = ±2`.
-/

namespace QM

/-- The CHSH correlation value. -/
def chsh (a0 a1 b0 b1 : ℝ) : ℝ := a0*b0 + a0*b1 + a1*b0 - a1*b1

/-- **CHSH inequality (local bound).** For deterministic ±1 local hidden variables, `S ≤ 2`. -/
theorem chsh_local_bound (a0 a1 b0 b1 : ℝ)
    (ha0 : a0 = 1 ∨ a0 = -1) (ha1 : a1 = 1 ∨ a1 = -1)
    (hb0 : b0 = 1 ∨ b0 = -1) (hb1 : b1 = 1 ∨ b1 = -1) :
    chsh a0 a1 b0 b1 ≤ 2 := by
  dsimp [chsh]
  rcases ha0 with ha0 | ha0 <;> rcases ha1 with ha1 | ha1 <;>
    rcases hb0 with hb0 | hb0 <;> rcases hb1 with hb1 | hb1 <;>
    subst a0 <;> subst a1 <;> subst b0 <;> subst b1 <;> norm_num

end QM
