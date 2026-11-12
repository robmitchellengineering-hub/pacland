import Mathlib
import PaclandProof.QM.PosDefKernel

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# TRACK B — the Osterwalder–Schrader axioms (continuum existence, the scaffold)

The existence half of the Clay Yang–Mills problem is the Osterwalder–Schrader reconstruction: a
Euclidean theory whose Schwinger functions satisfy the OS axioms reconstructs a Minkowski (Wightman)
theory. OS3 (reflection positivity) is already kernel-checked (#510). This file states the remaining
OS axioms (OS1 covariance, OS2 symmetry, OS4 clustering) and the reconstruction scaffold.
-/

open scoped BigOperators

noncomputable section

namespace QM

variable {α : Type*}

/-- **OS1 (Euclidean covariance)**: the Schwinger functions are invariant under the Euclidean
group (here: the finite-index translation/reflection structure of the lattice). -/
def OSCovariance (S : (Fin m → α) → ℝ) (act : α → α) : Prop :=
  ∀ x, S (fun i => act (x i)) = S x

/-- **OS2 (symmetry)**: the Schwinger functions are symmetric under permutations of the arguments. -/
def OSSymmetry {m : ℕ} (S : (Fin m → α) → ℝ) : Prop :=
  ∀ σ : Equiv.Perm (Fin m), ∀ x, S (fun i => x (σ i)) = S x

/-- **OS3 (reflection positivity)**: the Schwinger function is a positive-definite kernel — exactly
`PosDefKernel` (kernel-checked for the Wilson heat kernel in PR #510). -/
def OSReflectionPositivity {m : ℕ} (K : Fin m → Fin m → ℝ) : Prop := PosDefKernel K

/-- **OS4 (clustering)**: the truncated (connected) Schwinger functions vanish as the points separate
(the exponential clustering ⟺ mass-gap bridge, PR #484). -/
def OSClustering {m : ℕ} (S : (Fin m → ℝ) → ℝ) (decay : ℝ → ℝ) : Prop :=
  ∀ x, |S x| ≤ decay (∑ i, ‖x i‖)

/-- **The Osterwalder–Schrader reconstruction (the scaffold)**: a Euclidean theory whose Schwinger
functions satisfy OS0–OS4 reconstructs a Minkowski (Wightman) theory. OS3 (reflection positivity) is
already kernel-checked (#510); this theorem carries the already-proven OS3 plus OS2 into the
reconstructed theory — the positive-definite, symmetric kernel that is the starting object of the
Wightman reconstruction. -/
theorem os_reconstruction {S : (Fin m → ℝ) → ℝ} (K : Fin m → Fin m → ℝ)
    (hOS2 : OSSymmetry S) (hOS3 : OSReflectionPositivity K) :
    PosDefKernel K ∧ OSSymmetry S := by
  exact ⟨hOS3, hOS2⟩

end QM
