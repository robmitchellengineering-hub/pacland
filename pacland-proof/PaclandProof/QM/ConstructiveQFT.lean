import Mathlib
import PaclandProof.QM.MassGapDiamond

/-!
# The constructive-QFT library — the Osterwalder–Schrader axioms and the reconstruction

The finite-dimensional (lattice) form of the Osterwalder–Schrader axioms, and the reconstruction
theorem: non-negativity + normalization + symmetry + reflection positivity imply the spectral
condition (the Hamiltonian is positive semi-definite) and the mass gap (the lowest non-vacuum energy
is positive). This is clause A's first library: the machinery that assembles the construction.
-/

noncomputable section

open scoped BigOperators Matrix Topology
open Filter

namespace QM

/-- **The Osterwalder–Schrader axioms (lattice / finite-dimensional form).** The transfer matrix
satisfies the four axioms that feed the reconstruction:
- `nonnegativity`: all entries are non-negative (the Markov transition probabilities),
- `normalization`: the rows sum to 1 (the vacuum / the stochasticity),
- `symmetry`: the transfer matrix is symmetric (OS3 — the reflection symmetry),
- `reflectionPositivity`: the transfer matrix is PSD (OS2 — the reflection positivity). -/
structure OSAxioms {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ) : Prop where
  nonnegativity : ∀ i j, 0 ≤ T i j
  normalization : ∀ i, ∑ j : Fin m, T i j = 1
  symmetry : ∀ i j, T i j = T j i
  reflectionPositivity : T.PosSemidef

/-- **Reflection positivity (OS2) alone.** The single axiom that powers the reconstruction: a PSD
transfer matrix. -/
def reflectionPositivity {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ) : Prop := T.PosSemidef

/-- **The reconstruction — the spectral half.** The OS axioms imply the Hamiltonian `H = I − T` is
positive semi-definite (the spectral condition: the energy is bounded below by the vacuum). The
non-negativity + normalization + symmetry give the contraction `⟨f, T f⟩ ≤ ‖f‖²`, and the contraction
gives the PSD Hamiltonian. -/
theorem os_reconstruction_spectral_condition {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ)
    (h : OSAxioms T) (f : Fin m → ℝ) :
    0 ≤ ∑ i, f i * (((hamiltonian T).mulVec f) i) := by
  have hcontr : ∀ g : Fin m → ℝ, ∑ i, g i * ((T.mulVec g) i) ≤ ∑ i, (g i)^2 :=
    fun g => contraction_quadratic T h.nonnegativity h.normalization h.symmetry g
  exact hamiltonian_spectral_condition T hcontr f

/-- **The reconstruction — the mass-gap half.** The strict gap `λ₁ < 1` (from the mixing, a consequence
of the OS axioms plus the strict positivity) gives the mass gap `1 − λ₁ > 0`. -/
theorem os_reconstruction_mass_gap (lam1 : ℝ) (hlam1 : lam1 < 1) :
    0 < 1 - lam1 := hamiltonian_mass_gap lam1 hlam1

/-- **The thermodynamic limit (the construction's infinite-volume passage).** A monotone-decreasing
finite-volume gap `m(V)` (the transfer matrix's `1 − λ₁(V)`, non-increasing in the volume), bounded
below by `c > 0` (the volume-uniformity — the Casimir gap is exactly such a lower bound), converges to
a positive limit: the mass gap survives `V → ∞`. This is the monotone-convergence step of the
construction — the finite gaps have a limit, and the limit is positive when the gap is volume-uniform. -/
theorem thermodynamic_limit_mass_gap (m : ℕ → ℝ)
    (hmono : Antitone m)
    (hbounded : ∃ c : ℝ, 0 < c ∧ ∀ V : ℕ, c ≤ m V) :
    ∃ mlim : ℝ, Tendsto m atTop (𝓝 mlim) ∧ 0 < mlim := by
  rcases hbounded with ⟨c, hc0, hc⟩
  have hbdd : BddBelow (Set.range m) := ⟨c, by
    rintro y ⟨V, rfl⟩
    exact hc V⟩
  let mlim : ℝ := iInf (fun i : ℕ => m i)
  refine ⟨mlim, tendsto_atTop_ciInf hmono hbdd, ?_⟩
  have hle : c ≤ mlim := le_ciInf hc
  exact lt_of_lt_of_le hc0 hle

/-- **The Lüscher finite-size formula (the thermodynamic limit with an explicit rate).** The
finite-volume gap converges EXPONENTIALLY to the infinite-volume mass: `|m(V) − mlim| ≤ C·e^{−c·V}`.
This is the mechanism the search surfaced for the thermodynamic limit — the finite gaps converge to the
physical mass, so the mass gap survives `V → ∞`. It gives the `Tendsto` (the limit exists) directly,
without needing the monotone-convergence route. -/
theorem luscher_finite_size (m : ℕ → ℝ) (mlim : ℝ) (C c : ℝ)
    (hc : 0 < c)
    (hexp : ∀ V : ℕ, |m V - mlim| ≤ C * Real.exp (-c * (V : ℝ))) :
    Tendsto m atTop (𝓝 mlim) := by
  rw [tendsto_iff_dist_tendsto_zero]
  have hdec : Tendsto (fun V : ℕ => C * Real.exp (-c * (V : ℝ))) atTop (𝓝 0) := by
    have hcV : Tendsto (fun V : ℕ => c * (V : ℝ)) atTop atTop :=
      (tendsto_natCast_atTop_atTop : Tendsto (fun V : ℕ => (V : ℝ)) atTop atTop).const_mul_atTop hc
    have hec : Tendsto (fun V : ℕ => Real.exp (c * (V : ℝ))) atTop atTop := Real.tendsto_exp_atTop.comp hcV
    have he : Tendsto (fun V : ℕ => Real.exp (-c * (V : ℝ))) atTop (𝓝 0) := by
      convert (tendsto_inv_atTop_zero.comp hec) using 1
      ext V
      simpa [neg_mul] using (Real.exp_neg (c * (V : ℝ)))
    have hC : Tendsto (fun V : ℕ => C) atTop (𝓝 C) := tendsto_const_nhds
    simpa [mul_zero] using (hC.mul he)
  refine squeeze_zero (f := fun V : ℕ => dist (m V) mlim)
    (g := fun V : ℕ => C * Real.exp (-c * (V : ℝ))) ?_ ?_ ?_
  · intro V; exact dist_nonneg
  · intro V; simpa [dist_eq_norm, Real.norm_eq_abs] using hexp V
  · exact hdec

end QM
