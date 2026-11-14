import Mathlib
import PaclandProof.QM.PosDefKernel

/-!
# B1 — reflection positivity ⟹ the correlation contraction (the analytic continuation's core)

The Osterwalder–Schrader reconstruction's B1 rung (reflection positivity ⟹ analytic continuation)
rests on one algebraic fact: **positivity bounds the correlations**. For a positive-definite (OS3)
kernel, the diagonal is non-negative — the first rung of the Cauchy–Schwarz contraction that makes
the transfer matrix's time evolution well-defined.

This file proves the **first rung** (`posdef_diag_nonneg`, the diagonal of the reflection form is
non-negative) and the reusable delta-sum helpers (`sum_single`, `sum_delta_delta`) that the full
Cauchy–Schwarz contraction `K(i,j)² ≤ K(i,i)·K(j,j)` is built from. The full contraction is the
next step. Neither rung claims the mass gap — that is the volume-uniform join
(`VolumeUniformJoin.lean`), a separate open rung.
-/

noncomputable section

namespace QM

open scoped BigOperators

/-- The single delta sum: `∑ l, (if l = j then 1 else 0) * f l = f j`. -/
lemma sum_single {m : ℕ} (j : Fin m) (f : Fin m → ℝ) :
    (∑ l : Fin m, (if l = j then 1 else 0) * f l) = f j := by
  rw [Finset.sum_eq_single j]
  · simp
  · intro l _ hlj
    simp [hlj]
  · intro hj
    simp at hj

/-- The delta pair: `∑ k, ∑ l, δ_i(k) δ_j(l) K(k,l) = K(i,j)`. -/
lemma sum_delta_delta {m : ℕ} (i j : Fin m) (K : Fin m → Fin m → ℝ) :
    (∑ k : Fin m, ∑ l : Fin m, (if k = i then 1 else 0) * (if l = j then 1 else 0) * K k l) = K i j := by
  have h : (∑ k : Fin m, ∑ l : Fin m, (if k = i then 1 else 0) * (if l = j then 1 else 0) * K k l)
         = ∑ k : Fin m, (if k = i then 1 else 0) * K k j := by
    congr 1
    ext k
    simp_rw [mul_assoc]
    rw [← Finset.mul_sum]
    rw [sum_single j (fun l => K k l)]
  rw [h]
  rw [sum_single i (fun k => K k j)]

/-- **B1 (first rung) — the diagonal of a reflection-positive kernel is non-negative.** The single
delta test function applied to the positive form gives `0 ≤ K(i,i)` — the "energy" at a single site
is non-negative. This is the first rung of the Cauchy–Schwarz contraction
(`K(i,j)² ≤ K(i,i)·K(j,j)`) that the OS analytic continuation is built on. -/
theorem posdef_diag_nonneg {m : ℕ} (K : Fin m → Fin m → ℝ) (hK : PosDefKernel K) (i : Fin m) :
    0 ≤ K i i := by
  have h := hK (fun k => if k = i then 1 else 0)
  simpa [PosDefKernel, sum_delta_delta] using h

end QM
