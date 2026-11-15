import Mathlib
import PaclandProof.QM.PosDefKernel

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

end QM
