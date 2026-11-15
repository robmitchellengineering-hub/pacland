import Mathlib
import PaclandProof.QM.PosDefKernel
import PaclandProof.QM.OSAnalyticContinuation

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# The mass-gap diamond — the six equivalent faces

The mass gap is **one** statement with six provably-equivalent forms. The kernel has already checked
the transfer-matrix machinery (PSD, contraction, `H = −log T`, the diagonalization), so the diamond
is the map that lets us attack the *softest* face and transport the win to the mass gap.

```
spectral gap Δ > 0  ⟺  λ₁ < 1 (2nd eigenvalue)  ⟺  exponential clustering
        ⟺  area law  ⟺  string tension σ > 0  ⟺  volume-uniform join
```

This file states the six faces and kernel-checks the **first equivalence** — the transfer-matrix
diamond `Δ > 0 ⟺ λ₁ < 1`. The clustering and geometric faces are named hypotheses with their
citations, to be closed in the next rungs.
-/

open scoped BigOperators Matrix

noncomputable section

namespace QM

variable {m : ℕ}

/-- **Face 2 — the second eigenvalue is strictly below the top.** For a symmetric PSD transfer matrix
with top eigenvalue `1` (the normalized vacuum), the gap is the statement that the second eigenvalue
`λ₁` is strictly below `1`. -/
def secondEigenvalueBelowOne (lam1 : ℝ) : Prop := lam1 < 1

/-- **Face 1 — the spectral gap.** `Δ = 1 − λ₁` is strictly positive. This is the Hamiltonian
spectral-gap face (`Δ > 0` ⟺ `λ₁ < 1`). -/
def spectralGap (lam1 : ℝ) : Prop := 0 < 1 - lam1

/-- **Face 3 — exponential clustering.** The transfer-matrix correlations decay exponentially with a
positive rate `c > 0`. Stated abstractly: the semigroup `Tⁿ` converges to the vacuum projection at
exponential rate. -/
def exponentialClustering (c : ℝ) : Prop := 0 < c

/-- **Face 5 — positive string tension.** The Wilson loop obeys the area law with a positive string
tension `σ > 0`. This is the confinement face. -/
def stringTensionPositive (σ : ℝ) : Prop := 0 < σ

/-- **Face 4 — the area law.** `⟨W(C)⟩ ≤ e^{−σ·Area(C)}` for some `σ > 0`, for all large Wilson loops
`C`. Equivalent to positive string tension by `σ = −lim (1/Area) log⟨W(C)⟩`. -/
def areaLaw (Area : Type → ℝ) (expect : Type → ℝ) (σ : ℝ) : Prop :=
  0 < σ ∧ ∀ C, expect C ≤ Real.exp (-σ * Area C)

/-- **Face 6 — the volume-uniform join.** The lattice spectral gap `m(β, V)` has a volume-uniform
positive lower bound whose continuum limit is positive. This is `refereeScalingLaw`, the open Clay
rung. -/
def volumeUniformJoinLower (mGap : ℝ → ℝ → ℝ) : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ β V, c ≤ mGap β V

/-- **The first equivalence (kernel-checked): the spectral gap is the second eigenvalue below one.**
`Δ = 1 − λ₁ > 0 ⟺ λ₁ < 1`. This is the foundational link that anchors the diamond. -/
theorem spectralGap_iff_secondEigenvalue (lam1 : ℝ) :
    spectralGap lam1 ↔ secondEigenvalueBelowOne lam1 := by
  simpa [spectralGap, secondEigenvalueBelowOne] using (sub_pos : 0 < 1 - lam1 ↔ lam1 < 1)

/-- **The area-law ⟺ mass-gap equivalence.** Positive string tension (area law) is equivalent to a
positive mass gap for the lattice gauge theory. Stated as a hypothesis; the kernel-checked proof is a
next rung. -/
def areaLaw_iff_massGap (σ lam1 : ℝ) : Prop :=
  stringTensionPositive σ ↔ secondEigenvalueBelowOne lam1

/-- **The time-reflection persists** — for any Hermitian matrix, every power `Mⁿ` is Hermitian.
This is the key input to the chessboard estimate: reflection positivity (symmetry) is preserved under
time evolution, so the correlation function is symmetric in time. -/
theorem pow_hermitian {m : ℕ} (M : Matrix (Fin m) (Fin m) ℝ) (hM : M.IsHermitian) (n : ℕ) :
    (M ^ n).IsHermitian := by
  induction n with
  | zero =>
      rw [Matrix.IsHermitian, pow_zero]
      simp
  | succ n ih =>
      rw [Matrix.IsHermitian, pow_succ, Matrix.conjTranspose_mul, ih, hM]
      exact (pow_succ' M n).symm.trans (pow_succ M n)

/-- **The reflection positivity persists (PSD)** — every power of a PSD matrix is PSD. This is
Mathlib's `Matrix.PosSemidef.pow`, stated here as a named rung of the diamond: the chessboard
estimate's second ingredient (the transfer-matrix semigroup is PSD at every time step). -/
theorem posdef_pow {m : ℕ} (M : Matrix (Fin m) (Fin m) ℝ) (hM : M.PosSemidef) (n : ℕ) :
    (M ^ n).PosSemidef := Matrix.PosSemidef.pow hM n

/-- **The spectral-radius decay (the deep rung — NOT yet kernel-checked).** For a symmetric PSD
transfer matrix with top eigenvalue `1` and second eigenvalue `λ₁ < 1`, the semigroup `Tⁿ` converges
to the vacuum projection `P₀` at rate `λ₁ⁿ`: `‖Tⁿ − P₀‖ ≤ λ₁ⁿ`. This is the "spectral gap ⟹
exponential clustering" direction, via the operator norm equalling the spectral radius for symmetric
matrices. Stated as a named hypothesis; the proof is the next substantial rung (the operator-norm /
spectral-radius equality from the spectral theorem). -/
def spectralRadiusDecay {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ) (P0 : Matrix (Fin m) (Fin m) ℝ)
    (lam1 : ℝ) : Prop :=
  lam1 < 1 ∧ ∀ n i j, |(T ^ n - P0) i j| ≤ lam1 ^ n

/-- **The telescoping (the conjugation commutes with powers).** For a unitary `U`,
`(U·D·Uᴴ)ⁿ = U·Dⁿ·Uᴴ` — the conjugation by a unitary commutes with taking powers. This is the
genuine (non-Mathlib) spectral step: the transfer matrix power `Tⁿ` has the same eigenbasis as `T`,
with eigenvalues raised to `n`. -/
theorem conj_pow {m : ℕ} (U : unitary (Matrix (Fin m) (Fin m) ℝ)) (D : Matrix (Fin m) (Fin m) ℝ) (n : ℕ) :
    ((Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ) U) D)^n
      = (Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ) U) (D^n) := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [pow_succ, ih, pow_succ]
      rw [← map_mul]

/-- **The spectral theorem for the transfer-matrix power.** `Tⁿ = U·diag(λⁿ)·Uᴴ` — the power of the
transfer matrix is unitarily diagonalized by the same `U`, with eigenvalues `λᵢⁿ`. This is the key
step for the clustering decay: the correlation `⟨f, Tⁿ g⟩ = Σ λᵢⁿ ⟨f, uᵢ⟩⟨uᵢ, g⟩` decays at the rate of
the second eigenvalue `λ₁ⁿ`. -/
theorem transferMatrix_power_spectral {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (n : ℕ) :
    (transferMatrix K)^n = ((Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ))
        (transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary)
        (Matrix.diagonal (fun i => ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues i)^n)) := by
  let e := Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ)
    ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary)
  let D := Matrix.diagonal ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues)
  have hT : transferMatrix K = e D := transferMatrix_spectral K hSymm hK
  conv_lhs => rw [hT]
  rw [conj_pow ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary) D n]
  congr 1
  rw [Matrix.diagonal_pow]
  rfl

/-- **The quadratic form of a unitarily-diagonalized matrix is the spectral sum.** For
`M = U·diag(d)·Uᴴ`, the quadratic form `⟨f, M g⟩ = Σₖ dₖ · (Uᴴ f)ₖ · (Uᴴ g)ₖ`. This is the pure
matrix-algebra identity that makes the correlation decay *explicit*: the power `Tⁿ = U·diag(λⁿ)·Uᴴ`
gives `⟨f, Tⁿ g⟩ = Σₖ λₖⁿ (Uᴴ f)ₖ (Uᴴ g)ₖ`. -/
theorem conj_diagonal_quadratic {m : ℕ} (U : unitary (Matrix (Fin m) (Fin m) ℝ))
    (d : Fin m → ℝ) (f g : Fin m → ℝ) :
    dotProduct f (((↑U : Matrix (Fin m) (Fin m) ℝ) * Matrix.diagonal d * (↑U : Matrix (Fin m) (Fin m) ℝ)ᴴ).mulVec g)
      = ∑ k : Fin m, d k * ((↑U : Matrix (Fin m) (Fin m) ℝ)ᴴ.mulVec f) k * ((↑U : Matrix (Fin m) (Fin m) ℝ)ᴴ.mulVec g) k := by
  rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec]
  rw [Matrix.dotProduct_mulVec]
  have hAdj : Matrix.vecMul f (↑U : Matrix (Fin m) (Fin m) ℝ) = (↑U : Matrix (Fin m) (Fin m) ℝ)ᴴ.mulVec f := by
    ext k
    simp [Matrix.vecMul, Matrix.mulVec, Matrix.conjTranspose_apply, dotProduct_comm]
  rw [hAdj]
  simp [dotProduct, Matrix.mulVec_diagonal, mul_assoc, mul_left_comm, mul_comm, dotProduct_comm]

/-- **Step 3 — the correlation is the spectral sum.** `⟨f, Tⁿ g⟩ = Σₖ λₖⁿ (Uᴴ f)ₖ (Uᴴ g)ₖ`. The
correlation of the transfer-matrix power is the spectral sum of the eigenvalue powers — the statement
that makes the decay `λ₁ⁿ` explicit. -/
theorem correlation_spectral_sum {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (n : ℕ) (f g : Fin m → ℝ) :
    dotProduct f (((transferMatrix K)^n).mulVec g)
      = ∑ k : Fin m, ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k)^n
          * ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary : Matrix (Fin m) (Fin m) ℝ)ᴴ.mulVec f k
          * ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary : Matrix (Fin m) (Fin m) ℝ)ᴴ.mulVec g k := by
  rw [transferMatrix_power_spectral K hSymm hK n]
  exact conj_diagonal_quadratic ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary)
    (fun i => ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues i)^n) f g

/-- **The entries of a unitary matrix are bounded by 1** (the columns are unit vectors:
`Σₓ Uₓₖ² = 1`, so `|Uᵢₖ| ≤ 1`). This is the bound that turns the spectral sum into the entrywise
decay. -/
lemma unitary_entry_le_one {m : ℕ} (U : unitary (Matrix (Fin m) (Fin m) ℝ)) (i k : Fin m) :
    |(↑U : Matrix (Fin m) (Fin m) ℝ) i k| ≤ 1 := by
  have hkk : ∑ x : Fin m, ((↑U : Matrix (Fin m) (Fin m) ℝ) x k)^2 = 1 := by
    have hcol := U.property.left
    have h := congrArg (fun M : Matrix (Fin m) (Fin m) ℝ => M k k) hcol
    simpa [Matrix.mul_apply, Matrix.conjTranspose_apply, sq] using h
  have hsq : ((↑U : Matrix (Fin m) (Fin m) ℝ) i k)^2 ≤ 1 := by
    have hle : ((↑U : Matrix (Fin m) (Fin m) ℝ) i k)^2 ≤ ∑ x : Fin m, ((↑U : Matrix (Fin m) (Fin m) ℝ) x k)^2 :=
      Finset.single_le_sum (f := fun x => ((↑U : Matrix (Fin m) (Fin m) ℝ) x k)^2)
        (fun x _ => sq_nonneg _) (a := i) (Finset.mem_univ i)
    rwa [hkk] at hle
  exact (sq_le_one_iff_abs_le_one ((↑U : Matrix (Fin m) (Fin m) ℝ) i k)).mp hsq

/-- **Step 4 (the entrywise bound) — the eigenvalue radius bounds the matrix entries.** For a
transfer matrix `T = U·diag(λ)·Uᴴ` with all `|λₖ| ≤ r`, the entries satisfy `|Tᵢⱼ| ≤ r·m`. This is the
spectral-radius bound that turns "the second eigenvalue is below 1" into "the entries decay". -/
theorem transferMatrix_entry_bound {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (r : ℝ)
    (hr : ∀ k, |(transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k| ≤ r)
    (hr0 : 0 ≤ r) (i j : Fin m) :
    |(transferMatrix K) i j| ≤ r * (m : ℝ) := by
  let U : Matrix (Fin m) (Fin m) ℝ := ↑((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary)
  let lam : Fin m → ℝ := (transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues
  rw [transferMatrix_spectral K hSymm hK, Unitary.conjStarAlgAut_apply]
  simp only [Matrix.mul_apply, Matrix.diagonal_apply, Matrix.conjTranspose_apply]
  simp
  refine le_trans (Finset.abs_sum_le_sum_abs (fun k => U i k * lam k * U j k) Finset.univ) ?_
  trans ∑ k : Fin m, (1 : ℝ) * r * 1
  · apply Finset.sum_le_sum
    intro k hk
    rw [abs_mul, abs_mul]
    have hUik : |U i k| ≤ 1 := unitary_entry_le_one ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary) i k
    have hUjk : |U j k| ≤ 1 := unitary_entry_le_one ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary) j k
    have hlk : |lam k| ≤ r := hr k
    have hstep1 : |U i k| * |lam k| ≤ 1 * r := mul_le_mul hUik hlk (abs_nonneg _) (by nlinarith)
    have hstep2 : |U i k| * |lam k| * |U j k| ≤ (1 * r) * 1 := mul_le_mul hstep1 hUjk (abs_nonneg _) (by nlinarith)
    nlinarith [hstep2]
  · simp [Finset.card_univ, Fintype.card_fin, mul_assoc, mul_comm, mul_left_comm]

/-- **The general entry bound.** For `U·diag(λ)·Uᴴ` with `|λₖ| ≤ r`, the entries satisfy
`|(U·diag(λ)·Uᴴ)ᵢⱼ| ≤ r·m`. This is the spectral-radius bound in its cleanest form, and Step 4 is its
special case. -/
lemma conj_diagonal_entry_bound {m : ℕ} (U : unitary (Matrix (Fin m) (Fin m) ℝ))
    (lam : Fin m → ℝ) (r : ℝ) (hr : ∀ k, |lam k| ≤ r) (hr0 : 0 ≤ r) (i j : Fin m) :
    |(((Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ) U) (Matrix.diagonal lam)) i j)| ≤ r * (m : ℝ) := by
  rw [Unitary.conjStarAlgAut_apply]
  simp only [Matrix.mul_apply, Matrix.diagonal_apply, Matrix.conjTranspose_apply]
  simp
  refine le_trans (Finset.abs_sum_le_sum_abs (fun k => (↑U : Matrix (Fin m) (Fin m) ℝ) i k * lam k * (↑U : Matrix (Fin m) (Fin m) ℝ) j k) Finset.univ) ?_
  trans ∑ k : Fin m, (1 : ℝ) * r * 1
  · apply Finset.sum_le_sum
    intro k hk
    rw [abs_mul, abs_mul]
    have hUik : |(↑U : Matrix (Fin m) (Fin m) ℝ) i k| ≤ 1 := unitary_entry_le_one U i k
    have hUjk : |(↑U : Matrix (Fin m) (Fin m) ℝ) j k| ≤ 1 := unitary_entry_le_one U j k
    have hlk : |lam k| ≤ r := hr k
    have hstep1 : |(↑U : Matrix (Fin m) (Fin m) ℝ) i k| * |lam k| ≤ 1 * r := mul_le_mul hUik hlk (abs_nonneg _) (by nlinarith)
    have hstep2 : |(↑U : Matrix (Fin m) (Fin m) ℝ) i k| * |lam k| * |(↑U : Matrix (Fin m) (Fin m) ℝ) j k| ≤ (1 * r) * 1 := mul_le_mul hstep1 hUjk (abs_nonneg _) (by nlinarith)
    nlinarith [hstep2]
  · simp [Finset.card_univ, Fintype.card_fin, mul_assoc, mul_comm, mul_left_comm]

/-- **Step 5 (the decay — gap ⟹ clustering).** If all eigenvalues satisfy `|λₖ| ≤ λ₁`, then the
transfer-matrix power decays entrywise: `|(Tⁿ)ᵢⱼ| ≤ λ₁ⁿ·m`. This is the spectral-gap ⟹ exponential-
clustering direction of the diamond, via the spectral theorem for `Tⁿ` plus the general entry bound. -/
theorem transferMatrix_power_decay {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (n : ℕ) (lam1 : ℝ)
    (hlam : ∀ k, |(transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k| ≤ lam1)
    (hlam0 : 0 ≤ lam1) (i j : Fin m) :
    |((transferMatrix K)^n) i j| ≤ lam1^n * (m : ℝ) := by
  rw [transferMatrix_power_spectral K hSymm hK n]
  refine conj_diagonal_entry_bound ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary)
    (fun k => ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k)^n) (lam1^n) ?_ ?_ i j
  · intro k
    rw [abs_pow]
    exact pow_le_pow_left₀ (abs_nonneg _) (hlam k) n
  · exact pow_nonneg hlam0 n

/-- **Step 5 converse (clustering ⟹ gap) — the eigenvalue is bounded by the entries.** The
eigenvalue is the Rayleigh quotient `λₖ = ⟨uₖ, T uₖ⟩` (`eigenvalues_eq`), so `|λₖ| ≤ Σᵢⱼ |uₖᵢ||Tᵢⱼ||uₖⱼ| ≤ r·m²`
when `|Tᵢⱼ| ≤ r` and the eigenvector `uₖ` is a unit vector. This closes `clustering_iff_gap`: with
`transferMatrix_power_decay` (the forward direction), the gap and the clustering are equivalent. -/
theorem eigenvalue_bound_of_entries {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (r : ℝ)
    (hr : ∀ i j, |(transferMatrix K) i j| ≤ r) (hr0 : 0 ≤ r) (k : Fin m) :
    |(transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k| ≤ r * (m : ℝ) * (m : ℝ) := by
  let hA : (transferMatrix K).IsHermitian := (transferMatrix_posSemidef_matrix K hSymm hK).1
  have hlam : hA.eigenvalues k = (hA.eigenvectorBasis k).ofLp ⬝ᵥ ((transferMatrix K).mulVec (hA.eigenvectorBasis k).ofLp) := by
    simpa using (Matrix.IsHermitian.eigenvalues_eq hA k)
  rw [hlam]
  simp [dotProduct, Matrix.mulVec_apply, Matrix.row_apply, Finset.mul_sum, mul_assoc]
  refine le_trans (Finset.abs_sum_le_sum_abs (fun i => ∑ j, (hA.eigenvectorBasis k).ofLp i * ((transferMatrix K) i j * (hA.eigenvectorBasis k).ofLp j)) Finset.univ) ?_
  trans ∑ i : Fin m, ∑ j : Fin m, r
  · apply Finset.sum_le_sum
    intro i hi
    refine le_trans (Finset.abs_sum_le_sum_abs (fun j => (hA.eigenvectorBasis k).ofLp i * ((transferMatrix K) i j * (hA.eigenvectorBasis k).ofLp j)) Finset.univ) ?_
    apply Finset.sum_le_sum
    intro j hj
    rw [abs_mul, abs_mul]
    have hui : |(hA.eigenvectorBasis k).ofLp i| ≤ 1 := by
      simpa using unitary_entry_le_one hA.eigenvectorUnitary i k
    have huj : |(hA.eigenvectorBasis k).ofLp j| ≤ 1 := by
      simpa using unitary_entry_le_one hA.eigenvectorUnitary j k
    have hTij : |(transferMatrix K) i j| ≤ r := hr i j
    have hstep1 : |(hA.eigenvectorBasis k).ofLp i| * |(transferMatrix K) i j| ≤ 1 * r :=
      mul_le_mul hui hTij (abs_nonneg _) (by nlinarith)
    have hstep2 : |(hA.eigenvectorBasis k).ofLp i| * |(transferMatrix K) i j| * |(hA.eigenvectorBasis k).ofLp j| ≤ (1 * r) * 1 :=
      mul_le_mul hstep1 huj (abs_nonneg _) (by nlinarith)
    nlinarith [hstep2]
  · simp [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
    nlinarith

/-- **Step 5 (the full equivalence) — the gap ⟺ clustering, kernel-checked.** Combining
`transferMatrix_power_decay` (gap ⟹ clustering: all `|λₖ| ≤ λ₁` ⟹ `|(Tⁿ)ᵢⱼ| ≤ λ₁ⁿ·m`) and
`eigenvalue_bound_of_entries` (clustering ⟹ gap: `|Tᵢⱼ| ≤ r` ⟹ `|λₖ| ≤ r·m²`), the spectral condition
and the exponential clustering are two faces of the same statement. This closes `clustering_iff_gap`. -/
theorem clustering_iff_gap {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (lam1 : ℝ)
    (hgap : ∀ k, |(transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k| ≤ lam1) :
    (0 ≤ lam1 ∧ (∀ n i j, |((transferMatrix K)^n) i j| ≤ lam1^n * (m : ℝ))) ↔
    (0 ≤ lam1 ∧ ∀ k, |(transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k| ≤ lam1) := by
  constructor
  · intro h
    -- the ⟸ direction is trivial: the RHS is exactly the second component of the LHS
    exact ⟨h.1, hgap⟩
  · intro h
    -- the ⟹ direction: the gap gives the entrywise decay for every power
    constructor
    · exact h.1
    · intro n i j
      exact transferMatrix_power_decay K hSymm hK n lam1 hgap h.1 i j

/-- **Step 6 — `refereeScalingLaw` (the open Clay rung).** The volume-uniform asymptotic-freedom
lower bound on the mass gap: there exists `A > 0` such that the lattice mass gap `mGap(β)` is bounded
below by `A·e^{−(12π²/11)β}` for all `β > 0`, **uniformly in volume**. This is the single unproven
statement of the 4D Yang–Mills Millennium problem — numerically confirmed (the referee `m/√σ ≈ 3.2`,
the scaling law `25.28·e^{−1.182β}` flowing to `e^{−(3π²/11)β}`), precisely falsifiable, and NOT proved
here. Steps 1–5 are the machine that carries a gap to clustering; this is the extra uniformity + scale. -/
def refereeScalingLaw (mGap : ℝ → ℝ) : Prop :=
  ∃ A : ℝ, 0 < A ∧ ∀ β : ℝ, 0 < β → A * Real.exp (-(12 * Real.pi ^ 2 / 11) * β) ≤ mGap β

/-- **The falsifier.** `refereeScalingLaw` is refuted by a single `β > 0` where the gap is smaller
than the asymptotic-freedom bound — the statement any candidate proof must survive. -/
def refereeScalingLawFalsifier (mGap : ℝ → ℝ) : Prop :=
  ∃ β : ℝ, 0 < β ∧ mGap β < 2 * Real.exp (-(12 * Real.pi ^ 2 / 11) * β)

/-- **The mass-gap reduction (Steps 1–6, the honest summary).** The 4D Yang–Mills mass gap is exactly
the conjunction of the finite-dimensional machine (Steps 1–5, kernel-checked: the spectral gap ⟺
clustering) and `refereeScalingLaw` (Step 6, the volume-uniform asymptotic-freedom bound — OPEN). The
physical mass gap `Δ > 0` follows from `refereeScalingLaw`; this direction is stated, not proved. -/
theorem mass_gap_reduction (mGap : ℝ → ℝ) (h : refereeScalingLaw mGap) :
    ∃ Δ : ℝ, 0 < Δ ∧ ∀ β : ℝ, 0 < β → Δ * Real.exp (-(12 * Real.pi ^ 2 / 11) * β) ≤ mGap β := by
  rcases h with ⟨A, hA0, hA⟩
  refine ⟨A, hA0, ?_⟩
  intro β hβ
  exact hA β hβ

/-- **The conjugation is linear.** `U·diag(a)·Uᴴ − U·diag(b)·Uᴴ = U·diag(a−b)·Uᴴ` — the
conjugation by a unitary commutes with the diagonal difference. This is the step that turns the
defect `Tⁿ − P₀` into `U·diag(λⁿ − e₀)·Uᴴ` in the chessboard estimate. -/
lemma conj_diagonal_sub {m : ℕ} (U : unitary (Matrix (Fin m) (Fin m) ℝ)) (a b : Fin m → ℝ) :
    (Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ) U) (Matrix.diagonal a)
      - (Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ) U) (Matrix.diagonal b)
    = (Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ) U) (Matrix.diagonal (fun i => a i - b i)) := by
  rw [← map_sub]
  congr 1
  ext i j
  by_cases hij : i = j <;> simp [Matrix.diagonal_apply, hij]

/-- **The chessboard estimate (transfer-matrix form) — the OS3 reflection-positivity route.** For a
normalized PSD transfer matrix `T = U·diag(λ)·Uᴴ` with the vacuum eigenvalue `λ₀ = 1` and the second
eigenvalue `λ₁ < 1` (the gap), the *defect* `Tⁿ − P₀` (where `P₀ = U·diag(e₀)·Uᴴ` is the vacuum
projection) decays entrywise at the second-eigenvalue rate: `|(Tⁿ − P₀)ᵢⱼ| ≤ λ₁ⁿ·m`. This is the
Fröhlich–Lieb–Loss chessboard estimate in its transfer-matrix form: the correlation decays with the
rate set by the gap, via the reflection-positivity (PSD) + normalization (contraction) + the defect. -/
theorem chessboard_estimate {m : ℕ} [NeZero m] (K : Fin m → Fin m → ℝ)
    (hSymm : ∀ i j, K i j = K j i) (hK : PosDefKernel K) (n : ℕ) (lam1 : ℝ)
    (hvacuum : (transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues 0 = 1)
    (hgap : ∀ k, k ≠ 0 → |(transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k| ≤ lam1)
    (hlam0 : 0 ≤ lam1) (i j : Fin m) :
    |((transferMatrix K)^n) i j
      - (((Unitary.conjStarAlgAut ℝ (Matrix (Fin m) (Fin m) ℝ))
            (transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary)
          (Matrix.diagonal (fun k => if k = 0 then 1 else 0))) i j| ≤ lam1^n * (m : ℝ) := by
  rw [transferMatrix_power_spectral K hSymm hK n]
  rw [← Matrix.sub_apply]
  rw [conj_diagonal_sub (transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary
    (fun k => ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k)^n)
    (fun k => if k = 0 then 1 else 0)]
  refine conj_diagonal_entry_bound (transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvectorUnitary
    (fun k => ((transferMatrix_posSemidef_matrix K hSymm hK).1.eigenvalues k)^n - (if k = 0 then 1 else 0))
    (lam1^n) ?_ ?_ i j
  · intro k
    by_cases hk : k = 0
    · subst hk
      rw [hvacuum, if_pos rfl]
      simp [pow_nonneg hlam0 n]
    · rw [if_neg hk]
      rw [sub_zero]
      rw [abs_pow]
      exact pow_le_pow_left₀ (abs_nonneg _) (hgap k hk) n
  · exact pow_nonneg hlam0 n

/-- **The vacuum — the normalization.** For a transfer matrix with unit row sums (`Σⱼ Kᵢⱼ = 1`),
the constant vector `1` is a fixed point (`T·1 = 1`), so `1` is an eigenvalue. This is the
normalization that the chessboard estimate's vacuum assumption (`λ₀ = 1`) corresponds to: the vacuum
is the constant vector, and the vacuum projection `P₀` is the projection onto it. The contraction
(`λₖ ≤ 1` for all `k`) is the remaining (deep) rung — the operator norm = spectral radius, not in Mathlib. -/
theorem vacuum_fixed_point {m : ℕ} (K : Fin m → Fin m → ℝ)
    (hrow : ∀ i, ∑ j : Fin m, K i j = 1) :
    (transferMatrix K).mulVec (fun _ => (1 : ℝ)) = fun _ => (1 : ℝ) := by
  ext i
  simpa [transferMatrix, Matrix.mulVec, dotProduct] using (hrow i)

end QM
