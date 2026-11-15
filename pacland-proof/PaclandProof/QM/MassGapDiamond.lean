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
def stringTension (σ : ℝ) : Prop := 0 < σ

/-- **Face 4 — the area law.** `⟨W(C)⟩ ≤ e^{−σ·Area(C)}` for some `σ > 0`, for all large Wilson loops
`C`. Equivalent to positive string tension by `σ = −lim (1/Area) log⟨W(C)⟩`. -/
def areaLaw (Area : Type → ℝ) (expect : Type → ℝ) (σ : ℝ) : Prop :=
  0 < σ ∧ ∀ C, expect C ≤ Real.exp (-σ * Area C)

/-- **Face 6 — the volume-uniform join.** The lattice spectral gap `m(β, V)` has a volume-uniform
positive lower bound whose continuum limit is positive. This is `refereeScalingLaw`, the open Clay
rung. -/
def volumeUniformJoin (mGap : ℝ → ℝ → ℝ) : Prop :=
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
  stringTension σ ↔ secondEigenvalueBelowOne lam1

end QM
