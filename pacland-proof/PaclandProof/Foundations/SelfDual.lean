import Mathlib
import PaclandProof.Foundations.Gleason2D

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# QF-3 (toy) — self-duality of the qubit state space, the mechanism

The reconstruction programme's "self-duality" says the state cone and the effect
cone coincide. For a 2-level system the mechanism is two facts, kernel-checked
here over `ℝ` on `Fin 2`:

1. every rank-one `vvᵀ` is PSD — so the "effects" contain all rank-one tests;
2. pairing `A` with `vvᵀ` under the trace inner product `⟨A, B⟩ = Tr(A·B)` is
   exactly the Born value `vᵀAv`.

Together they reduce "nonnegative on the whole PSD cone" to "nonnegative on every
rank-one test", which is the self-duality core. The full `↔` (PSD iff its
quadratic form is nonnegative) is the next rung; these are its two load-bearing
facts.
-/

noncomputable section

open Matrix BigOperators

namespace SelfDual

/-- Rank-one matrix `v vᵀ`. -/
def outer (v : Fin 2 → ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => v i * v j

/-- The trace inner product `⟨A, B⟩ = Tr(A · B)` for 2×2. -/
def trProd (A B : Matrix (Fin 2) (Fin 2) ℝ) : ℝ :=
  (A * B) 0 0 + (A * B) 1 1

/-- Rank-one matrices are PSD: `v vᵀ` has principal minors `v₀²`, `v₁²`, and
det `0`. -/
theorem outer_psd (v : Fin 2 → ℝ) : Gleason2D.psd2 (outer v) := by
  constructor
  · dsimp [outer]
    simpa [sq] using sq_nonneg (v 0)
  constructor
  · dsimp [outer]
    simpa [sq] using sq_nonneg (v 1)
  · have hdet : (outer v).det = 0 := by
      rw [Matrix.det_fin_two]
      simp [outer]
      ring
    simpa [hdet]

/-- Pairing `A` with a rank-one effect `v vᵀ` is the Born value `vᵀ A v`. -/
theorem trProd_outer (A : Matrix (Fin 2) (Fin 2) ℝ) (v : Fin 2 → ℝ) :
    trProd A (outer v) = dotProduct v (A.mulVec v) := by
  simp [trProd, outer, Matrix.mul_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  ring

end SelfDual

end
