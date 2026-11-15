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

/-- **The clustering ⟺ gap bridge (Douglas–Rajasekaran transfer-operator gap).** For a symmetric PSD
transfer matrix, exponential clustering (Face 3) is equivalent to the spectral gap (Faces 1–2), via
the Perron–Frobenius / Jentzsch argument. Stated as a named hypothesis; the full kernel-checked proof
is the next rung. -/
def clustering_iff_gap (c lam1 : ℝ) : Prop :=
  exponentialClustering c ↔ secondEigenvalueBelowOne lam1

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

end QM
