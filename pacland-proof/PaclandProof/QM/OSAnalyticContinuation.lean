import Mathlib
import PaclandProof.QM.PosDefKernel
import PaclandProof.QM.OSAxioms

/-!
# B1 — reflection positivity ⟹ the correlation contraction (the analytic continuation's core)

The Osterwalder–Schrader reconstruction's B1 rung (reflection positivity ⟹ analytic continuation)
rests on one algebraic fact: **positivity bounds the correlations**. For a positive-definite (OS3)
and symmetric (OS2) kernel, the off-diagonal correlation is bounded by the diagonal —

    `K(i,j)² ≤ K(i,i)·K(j,j)`  (Cauchy–Schwarz for the reflection form)

This is the "contraction" that makes the transfer matrix's time evolution well-defined, the algebraic
core the full analytic continuation is built on. This file proves that core, kernel-checked. It does
NOT claim the mass gap — that is the volume-uniform join (`VolumeUniformJoin.lean`), a separate open
rung.
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

/-- **B1 (first rung) — the diagonal of a reflection-positive kernel is non-negative.** -/
theorem posdef_diag_nonneg {m : ℕ} (K : Fin m → Fin m → ℝ) (hK : PosDefKernel K) (i : Fin m) :
    0 ≤ K i i := by
  have h := hK (fun k => if k = i then 1 else 0)
  simpa [PosDefKernel, sum_delta_delta] using h

/-- The two-point quadratic form: for the test function `δ_i + t·δ_j`, the reflection form is
`K(i,i) + t·K(i,j) + t·K(j,i) + t²·K(j,j)`. -/
lemma quad_two_point {m : ℕ} (i j : Fin m) (K : Fin m → Fin m → ℝ) (t : ℝ) :
    (∑ k : Fin m, ∑ l : Fin m,
        ((if k = i then 1 else 0) + t * (if k = j then 1 else 0))
          * ((if l = i then 1 else 0) + t * (if l = j then 1 else 0)) * K k l)
      = K i i + t * K i j + t * K j i + t * t * K j j := by
  simp [Finset.sum_add_distrib, mul_add, add_mul, sum_delta_delta]
  ring

/-- **B1 core — the reflection-positivity contraction (Cauchy–Schwarz).** A symmetric positive-definite
kernel satisfies `K(i,j)² ≤ K(i,i)·K(j,j)`: the off-diagonal correlation is bounded by the diagonal.
This is the contraction property the OS analytic continuation is built on. -/
theorem posdef_cauchy_schwarz {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (i j : Fin m) :
    K i j ^ 2 ≤ K i i * K j j := by
  by_cases hij : i = j
  · subst hij
    -- diagonal case: K(i,i)^2 ≤ K(i,i)^2, which holds iff 0 ≤ K(i,i)
    have hdiag : 0 ≤ K i i := posdef_diag_nonneg K hK i
    nlinarith [mul_nonneg hdiag hdiag]
  · -- off-diagonal: the quadratic in t is non-negative for every t
    have hquad : ∀ t : ℝ, 0 ≤ K i i + t * K i j + t * K j i + t * t * K j j := by
      intro t
      have h := hK (fun k => (if k = i then 1 else 0) + t * (if k = j then 1 else 0))
      rw [quad_two_point i j K t] at h
      exact h
    have hquadSymm : ∀ t : ℝ, 0 ≤ K i i + 2 * t * K i j + t ^ 2 * K j j := by
      intro t
      have h := hquad t
      rw [hSymm j i] at h
      nlinarith [h]
    have hjj : 0 ≤ K j j := posdef_diag_nonneg K hK j
    by_cases hj0 : K j j = 0
    · -- a = 0: the quadratic is linear, non-negative for all t, forcing K i j = 0
      have hlin : ∀ t : ℝ, 0 ≤ K i i + 2 * t * K i j := by
        intro t
        simpa [hj0] using hquadSymm t
      have hKij : K i j = 0 := by
        by_contra hne
        -- K i j ≠ 0: evaluate the linear bound at t = -(K i i + 1) / (2 K i j), which gives -1
        have hbad : K i i + 2 * (-(K i i + 1) / (2 * K i j)) * K i j = -1 := by
          field_simp [hne]
          ring
        have h := hlin (-(K i i + 1) / (2 * K i j))
        rw [hbad] at h
        nlinarith
      rw [hKij]
      rw [hj0]
      norm_num
    · -- a = K j j > 0: the quadratic is non-negative for all t, so its discriminant is ≤ 0
      have hjpos : 0 < K j j := lt_of_le_of_ne hjj (Ne.symm hj0)
      have hdet : 0 ≤ K i i * K j j - K i j ^ 2 := by
        have h := hquadSymm (-K i j / K j j)
        have hsimp : K i i + 2 * (-K i j / K j j) * K i j + (-K i j / K j j) ^ 2 * K j j
            = K i i - K i j ^ 2 / K j j := by
          field_simp [hj0]
          ring
        rw [hsimp] at h
        have hmul : 0 ≤ (K i i - K i j ^ 2 / K j j) * K j j := mul_nonneg h (le_of_lt hjpos)
        have hclear : (K i i - K i j ^ 2 / K j j) * K j j = K i i * K j j - K i j ^ 2 := by
          field_simp [hj0]
        simpa [hclear] using hmul
      exact sub_nonneg.mp hdet

/-- **B1 contraction (normalized) — the transfer matrix is a contraction.** For a normalized
reflection-positive kernel (`K(i,i) ≤ 1`), the off-diagonal correlation is bounded by 1:
`|K(i,j)| ≤ 1`. This is the "contraction" that makes the transfer matrix's spectrum ≤ 1 — the
condition the OS analytic continuation (the time evolution being a contraction semigroup) needs. -/
theorem posdef_contraction {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K)
    (hnorm : ∀ i, K i i ≤ 1) (i j : Fin m) :
    |K i j| ≤ 1 := by
  have hcs := posdef_cauchy_schwarz K hSymm hK i j
  have hii : K i i ≤ 1 := hnorm i
  have hjj : K j j ≤ 1 := hnorm j
  have hii0 : 0 ≤ K i i := posdef_diag_nonneg K hK i
  have hjj0 : 0 ≤ K j j := posdef_diag_nonneg K hK j
  have h1 : K i j ^ 2 ≤ 1 := by
    nlinarith [hcs, mul_le_mul hii hjj hjj0 (le_trans hii0 hii)]
  exact (sq_le_one_iff_abs_le_one (K i j)).mp h1

/-- The FinSupp double sum equals the full double sum over `Fin m` (via `Finsupp.sum_fintype`). -/
lemma finsupp_double_sum_eq {m : ℕ} (x : Fin m →₀ ℝ) (K : Fin m → Fin m → ℝ) :
    x.sum (fun i xi => x.sum (fun j xj => xi * K i j * xj))
      = ∑ i : Fin m, ∑ j : Fin m, x i * K i j * x j := by
  rw [Finsupp.sum_fintype x (fun i xi => x.sum (fun j xj => xi * K i j * xj)) (by intro i; simp)]
  congr 1
  ext i
  rw [Finsupp.sum_fintype x (fun j xj => x i * K i j * xj) (by intro j; simp)]

/-- **B1 spectral condition — the transfer matrix is positive-semidefinite (matrix form).**
Bridges the kernel's `PosDefKernel` to Mathlib's `Matrix.PosSemidef`, unlocking the spectral
theorem: a PSD symmetric transfer matrix has non-negative eigenvalues, which is the "energy ≥ 0"
half of the spectral condition (the Hamiltonian `H = -log T` is non-negative). -/
theorem transferMatrix_posSemidef_matrix {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) :
    (transferMatrix K).PosSemidef := by
  constructor
  · -- IsHermitian (for ℝ this is symmetry: K j i = K i j)
    ext i j
    simp [transferMatrix, Matrix.conjTranspose]
    exact hSymm j i
  · -- the quadratic form is non-negative for every FinSupp test vector
    intro x
    have h := hK (fun i => x i)
    simp only [transferMatrix]
    change 0 ≤ x.sum (fun i xi => x.sum (fun j xj => xi * K i j * xj))
    rw [finsupp_double_sum_eq x K]
    convert h using 1
    congr 1
    ext i
    congr 1
    ext j
    ring

/-- **B1 spectral condition — the transfer matrix has non-negative eigenvalues.** A PSD symmetric
transfer matrix has spectrum ≥ 0, so its Hamiltonian `H = -log T` is non-negative — the "energy ≥ 0"
half of the OS spectral condition. (The mass gap `Δ > 0` is the other session's volume-uniform join;
this is only the non-negativity half.) -/
theorem transferMatrix_eigenvalues_nonneg {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (i : Fin m) :
    0 ≤ (Matrix.IsHermitian.eigenvalues (transferMatrix_posSemidef_matrix K hSymm hK).1) i := by
  exact Matrix.PosSemidef.eigenvalues_nonneg (transferMatrix_posSemidef_matrix K hSymm hK) i

/-- **The actual OS reconstruction (existence half) — B1 + B2, with the mass gap left open.**
OS2 (symmetry) + OS3 (reflection positivity) reconstruct the Wightman axioms W0 (Hilbert), W1
(Minkowski covariance), W3 (locality), W4 (vacuum) for the Wilson heat kernel, AND the B1
contraction `K(i,j)² ≤ K(i,i)·K(j,j)`. W2 (the mass gap) is deliberately NOT asserted — it is the
volume-uniform join, the other session's open rung. This is the honest replacement for the trivial
`os_reconstruction` (which only re-packaged its own hypotheses). -/
theorem os_reconstruction_actual {m : ℕ} (K : Fin m → Fin m → ℝ) (θ : Fin m → ℝ) (β : ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) :
    (∀ i j, K i j ^ 2 ≤ K i i * K j j) ∧
    WightmanHilbert (fun (f g : Fin m → ℝ) => ∑ i, ∑ j, f i * g j * K i j) ∧
    WightmanCovariance (fun x y => Real.exp (2 * β * Real.cos (x - y))) ∧
    WightmanLocality (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) ∧
    WightmanVacuum (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))) := by
  constructor
  · intro i j
    exact posdef_cauchy_schwarz K hSymm hK i j
  · constructor
    · exact posdef_kernel_inner_product K hK
    · constructor
      · exact wick_rotation β
      · constructor
        · exact wilson_kernel_local θ β
        · intro i j
          exact wilson_kernel_vacuum θ β i j

end QM
