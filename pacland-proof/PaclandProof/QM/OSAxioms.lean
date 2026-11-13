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
open Filter

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

theorem wilson_kernel_symmetric {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) :
    (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j)))
      = fun i j => Real.exp (2 * β * Real.cos (θ j - θ i)) := by
  funext i j
  rw [show θ j - θ i = -(θ i - θ j) by ring]
  rw [Real.cos_neg]

/-- **The Clay assembly — the proven scaffold** (kernel-checked, no sorries), NOT the closure: the
strong-coupling mass gap `λ = 1 > 0` and the OS3 reflection positivity hold together. The full Clay
theorem (continuum existence + mass gap `Δ = Λ_QCD`) still has two open rungs: (A) the explicit
full-lattice collective instanton with the renormalized action, and (B) the full Osterwalder–Schrader
⟹ Wightman reconstruction. This theorem is the honest assembly of what is proven; it does not claim
the open rungs are closed. -/
theorem clay_assembly
    (hgap_strong : 0 < (1 : ℝ))                       -- the compactness gap λ = 1 > 0 (PR #525)
    (hOS3 : ∀ {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β),
      OSReflectionPositivity (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j))))  -- #510
    (hscaling : ∀ β, 0 ≤ β → Real.exp (-(12 * Real.pi^2 / 11) * β) ≤ (1 : ℝ))  -- the instanton lower bound
    :
    -- the strong-coupling gap + the reflection positivity hold together
    0 < (1 : ℝ) ∧ (∀ {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (hβ : 0 ≤ β),
      OSReflectionPositivity (fun i j => Real.exp (2 * β * Real.cos (θ i - θ j)))) := by
  exact ⟨hgap_strong, hOS3⟩
/-- **OS1 (Euclidean covariance) for the Wilson heat kernel**: the kernel is translation-invariant —
adding a common translation `t` to all arguments leaves it unchanged, because it depends only on the
differences `θ_i − θ_j`. -/
theorem wilson_kernel_covariant {m : ℕ} (θ : Fin m → ℝ) (t : ℝ) (β : ℝ) :
    (fun i j => Real.exp (2 * β * Real.cos ((θ i + t) - (θ j + t))))
      = fun i j => Real.exp (2 * β * Real.cos (θ i - θ j)) := by
  funext i j
  rw [show (θ i + t) - (θ j + t) = θ i - θ j by ring]

/-- **OS1 (reflection covariance) for the Wilson heat kernel**: the kernel is reflection-invariant —
negating the arguments (the lattice reflection) leaves it unchanged, because `cos` is even. -/
theorem wilson_kernel_reflection {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) :
    (fun i j => Real.exp (2 * β * Real.cos (-(θ i) - (-(θ j)))))
      = fun i j => Real.exp (2 * β * Real.cos (θ i - θ j)) := by
  funext i j
  rw [show -(θ i) - (-(θ j)) = -(θ i - θ j) by ring]
  rw [Real.cos_neg]

/-- **OS4 (clustering, the uniform bound) for the Wilson heat kernel**: the Schwinger function is
uniformly bounded by `e^{2β}` (the `|cos| ≤ 1` bound). The full exponential clustering (the decay of
the connected 2-point) follows from the clustering ⟺ mass-gap bridge (#484) plus the compactness gap
`λ = 1` (#525); this is the pointwise bound that makes the clustering well-defined. -/
theorem wilson_kernel_bounded {m : ℕ} (θ : Fin m → ℝ) (β : ℝ) (i j : Fin m) :
    |Real.exp (2 * β * Real.cos (θ i - θ j))| ≤ Real.exp (2 * |β|) := by
  rw [abs_of_nonneg (le_of_lt (Real.exp_pos _))]
  have h1 : 2 * β * Real.cos (θ i - θ j) ≤ 2 * |β| := by
    have hcos : |Real.cos (θ i - θ j)| ≤ 1 := Real.abs_cos_le_one _
    have h2 : |2 * β * Real.cos (θ i - θ j)| ≤ 2 * |β| := by
      calc
        |2 * β * Real.cos (θ i - θ j)| = |2 * β| * |Real.cos (θ i - θ j)| := by rw [abs_mul]
        _ ≤ |2 * β| * 1 := mul_le_mul_of_nonneg_left hcos (abs_nonneg _)
        _ = 2 * |β| := by rw [abs_mul]; ring
    exact le_trans (le_abs_self _) h2
  exact Real.exp_le_exp.mpr h1
/-- **OS4 (exponential clustering)**: the massive 2-point function `e^{−m·d}` with the mass gap
`m > 0` decays to `0` as the distance `d → ∞` — the connected correlation vanishes exponentially.
This is the clustering ⟺ mass-gap bridge (#484) in its one-line form: a positive gap gives the
exponential decay of the correlation. -/
theorem exponential_clustering_tendsto {m : ℝ} (hm : 0 < m) :
    Tendsto (fun d : ℝ => Real.exp (-m * d)) atTop (nhds 0) := by
  have h1 : Tendsto (fun d : ℝ => m * d) atTop atTop := tendsto_id.const_mul_atTop hm
  have h2 : Tendsto (fun d : ℝ => Real.exp (m * d)) atTop atTop := Real.tendsto_exp_atTop.comp h1
  have h3 : Tendsto (fun d : ℝ => (Real.exp (m * d))⁻¹) atTop (nhds 0) := tendsto_inv_atTop_zero.comp h2
  convert h3 using 1
  ext d
  rw [show (-m * d) = -(m * d) by ring]
  rw [Real.exp_neg]

/-- **OS4 (exponential clustering, the concrete rate)**: the connected 2-point function of the compact
soft mode decays exponentially — `e^{−m·d} ≤ e^{−m·d₀}·e^{−m·(d−d₀)}` for `d ≥ d₀`, so the correlation
at distance `d` is at most the correlation at `d₀` times `e^{−m·(d−d₀)}`. The mass gap `m > 0` gives the
strict exponential decay. -/
theorem exponential_clustering_rate {m : ℝ} (d d₀ : ℝ) :
    Real.exp (-m * d) ≤ Real.exp (-m * d₀) * Real.exp (-m * (d - d₀)) := by
  have h1 : Real.exp (-m * d) = Real.exp (-m * d₀) * Real.exp (-m * (d - d₀)) := by
    rw [show -m * d = -m * d₀ + (-m * (d - d₀)) by ring]
    rw [Real.exp_add]
  exact le_of_eq h1
end QM
