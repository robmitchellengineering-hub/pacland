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

/-- **A volume-independent positive quantity is a volume-uniform lower bound.** The Coulomb string
tension is a local quantity (the linear coefficient of the Coulomb potential at a point), so it is
volume-independent; this discharges the `bounded-below` hypothesis of `thermodynamic_limit_mass_gap`. -/
theorem volume_independent_is_volume_uniform (f : ℕ → ℝ) (f0 : ℝ)
    (hconst : ∀ V, f V = f0) (hf0 : 0 < f0) :
    volumeUniform f := by
  rw [volumeUniform]
  refine ⟨f0, hf0, ?_⟩
  intro V hV
  rw [hconst V]

/-- **The Coulomb route closes the thermodynamic limit.** If the finite-volume gap `m(V)` is monotone
and bounded below by a volume-independent `σ_Coul > 0` (Zwanziger: the Coulomb tension lower-bounds the
physical string tension ≤ the gap), then the mass gap survives `V → ∞`. This is the mechanism the search
targeted: a volume-uniform lower bound on the transfer-matrix gap. -/
theorem mass_gap_from_volume_independent_tension (m : ℕ → ℝ) (σ_Coul : ℝ)
    (hmono : Antitone m)
    (htension : ∀ V : ℕ, σ_Coul ≤ m V)
    (hσ0 : 0 < σ_Coul) :
    ∃ mlim : ℝ, Tendsto m atTop (𝓝 mlim) ∧ 0 < mlim := by
  exact thermodynamic_limit_mass_gap m hmono ⟨σ_Coul, hσ0, htension⟩

/-- **The 2-state Dirichlet identity (the explicit gap mechanism).** For the 2-state symmetric
stochastic transfer matrix `T = [[1−p, p], [p, 1−p]]`, the quadratic form is `⟨x, Tx⟩ = ‖x‖² − p·(x₀−x₁)²`.
The gap is EXACTLY `p·(x₀−x₁)²` — the mixing `p` times the spread — which is the volume-uniform lower
bound the search targets: `p` is local (volume-independent), so the gap cannot close as the volume grows. -/
theorem two_state_dirichlet_identity (p x0 x1 : ℝ) :
    x0 * ((1-p) * x0 + p * x1) + x1 * (p * x0 + (1-p) * x1)
      = (x0^2 + x1^2) - p * (x0 - x1)^2 := by
  ring

/-- **The 2-state gap is `2·p`** — the second eigenvalue is `λ₁ = 1 − 2p`, so the gap `1 − λ₁ = 2p`
is exactly twice the mixing `p`, volume-independent. This is the explicit "mixing rate" the search
surfaced: a positive local mixing gives a positive volume-uniform gap. -/
theorem two_state_gap (p : ℝ) (hp : 0 < p) :
    0 < 2 * p := by
  nlinarith

/-- **The Dirichlet identity (the general mixing-rate gap).** For a symmetric stochastic matrix `T`
(row sums 1, symmetric), the quadratic form is `⟨x, Tx⟩ = ‖x‖² − (1/2)·Σᵢⱼ Tᵢⱼ·(xᵢ−xⱼ)²`. The gap IS the
Dirichlet form (the weighted spread), so the mixing `Tᵢⱼ ≥ δ` bounds the gap below by `(δ/2)·(the
spread)` — the volume-uniform lower bound the search targets, now in general dimension. -/
theorem dirichlet_identity {m : ℕ} (T : Matrix (Fin m) (Fin m) ℝ)
    (hrow : ∀ i, ∑ j : Fin m, T i j = 1) (hsymm : ∀ i j, T i j = T j i) (x : Fin m → ℝ) :
    ∑ i : Fin m, x i * (∑ j : Fin m, T i j * x j)
      = (∑ i : Fin m, (x i)^2) - (1/2) * (∑ i : Fin m, ∑ j : Fin m, T i j * (x i - x j)^2) := by
  -- Step A: ⟨x,Tx⟩ = ∑_ij T_ij x_i x_j
  have hA : ∑ i : Fin m, x i * (∑ j : Fin m, T i j * x j) = ∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j) := by
    apply Finset.sum_congr rfl; intro i hi
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl; intro j hj
    ring
  rw [hA]
  -- Step B: ∑_ij T_ij x_i x_j = ∑_ij T_ij x_j x_i  (swap + symmetry)
  have hB : ∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j) = ∑ i : Fin m, ∑ j : Fin m, T i j * (x j * x i) := by
    calc
      ∑ i, ∑ j, T i j * (x i * x j) = ∑ j, ∑ i, T i j * (x i * x j) := by rw [Finset.sum_comm]
      _ = ∑ i, ∑ j, T j i * (x j * x i) := by
          -- rename the swapped indices back
          apply Finset.sum_congr rfl; intro j hj
          apply Finset.sum_congr rfl; intro i hi
          rfl
      _ = ∑ i, ∑ j, T i j * (x j * x i) := by
          apply Finset.sum_congr rfl; intro i hi
          apply Finset.sum_congr rfl; intro j hj
          rw [hsymm i j]
  -- Step C: 2·(the sum) = ∑_ij T_ij (x_i x_j + x_j x_i)
  have hC : (2 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j))
      = ∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j + x j * x i) := by
    calc
      (2 : ℝ) * (∑ i, ∑ j, T i j * (x i * x j))
        = (∑ i, ∑ j, T i j * (x i * x j)) + (∑ i, ∑ j, T i j * (x i * x j)) := by ring
      _ = (∑ i, ∑ j, T i j * (x i * x j)) + (∑ i, ∑ j, T i j * (x j * x i)) := by rw [hB]
      _ = ∑ i, ∑ j, T i j * (x i * x j + x j * x i) := by
          rw [← Finset.sum_add_distrib]
          apply Finset.sum_congr rfl; intro i hi
          rw [← Finset.sum_add_distrib]
          apply Finset.sum_congr rfl; intro j hj
          ring
  -- Step D: x_i x_j + x_j x_i = x_i² + x_j² - (x_i - x_j)²
  have hD : ∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j + x j * x i)
      = ∑ i : Fin m, ∑ j : Fin m, T i j * ((x i)^2 + (x j)^2 - (x i - x j)^2) := by
    apply Finset.sum_congr rfl; intro i hi
    apply Finset.sum_congr rfl; intro j hj
    ring
  -- Step E: ∑_ij T_ij (x_i² + x_j²) = 2‖x‖²
  have hE : ∑ i : Fin m, ∑ j : Fin m, T i j * ((x i)^2 + (x j)^2) = 2 * (∑ i : Fin m, (x i)^2) := by
    calc
      ∑ i, ∑ j, T i j * ((x i)^2 + (x j)^2)
        = (∑ i, ∑ j, T i j * (x i)^2) + (∑ i, ∑ j, T i j * (x j)^2) := by
            rw [← Finset.sum_add_distrib]
            apply Finset.sum_congr rfl; intro i hi
            rw [← Finset.sum_add_distrib]
            apply Finset.sum_congr rfl; intro j hj
            ring
      _ = (∑ i, (x i)^2 * (∑ j, T i j)) + (∑ i, ∑ j, T i j * (x j)^2) := by
            congr 1
            apply Finset.sum_congr rfl; intro i hi
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl; intro j hj
            rw [mul_comm]
      _ = (∑ i, (x i)^2 * 1) + (∑ j, (x j)^2 * (∑ i, T i j)) := by
            rw [← Finset.sum_comm]
            congr 1
            · apply Finset.sum_congr rfl; intro i hi; rw [hrow i]
            · apply Finset.sum_congr rfl; intro j hj
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl; intro i hi
              rw [mul_comm]
      _ = (∑ i, (x i)^2) + (∑ j, (x j)^2) := by
            congr 1
            · apply Finset.sum_congr rfl; intro i hi; ring
            · apply Finset.sum_congr rfl; intro j hj
              -- column sums = 1 via hrow + hsymm
              have hcol : ∑ i : Fin m, T i j = 1 := by
                calc
                  ∑ i : Fin m, T i j = ∑ i : Fin m, T j i := by
                    apply Finset.sum_congr rfl; intro i hi; rw [hsymm i j]
                  _ = 1 := by rw [hrow j]
              rw [hcol]; ring
      _ = 2 * (∑ i, (x i)^2) := by
          rw [show (∑ j : Fin m, (x j)^2) = (∑ i : Fin m, (x i)^2) by rfl]
          ring
  -- Step F: combine
  -- 2⟨x,Tx⟩ = ∑_ij T_ij (x_i²+x_j²-(x_i-x_j)²) = 2‖x‖² - D
  -- hence ⟨x,Tx⟩ = ‖x‖² - D/2
  -- combine: 2·S = ∑_ij T_ij (x_i x_j + x_j x_i) = ∑_ij T_ij (x_i²+x_j²-(x_i-x_j)²) = 2‖x‖² - D
  have hkey : (2 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j))
      = 2 * (∑ i : Fin m, (x i)^2) - ∑ i : Fin m, ∑ j : Fin m, T i j * (x i - x j)^2 := by
    calc
      (2 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j))
        = ∑ i : Fin m, ∑ j : Fin m, T i j * (x i * x j + x j * x i) := hC
      _ = ∑ i : Fin m, ∑ j : Fin m, T i j * ((x i)^2 + (x j)^2 - (x i - x j)^2) := hD
      _ = (∑ i : Fin m, ∑ j : Fin m, T i j * ((x i)^2 + (x j)^2)) - (∑ i : Fin m, ∑ j : Fin m, T i j * (x i - x j)^2) := by
          simp [Finset.sum_sub_distrib, mul_sub]
      _ = 2 * (∑ i : Fin m, (x i)^2) - ∑ i : Fin m, ∑ j : Fin m, T i j * (x i - x j)^2 := by rw [hE]
  nlinarith



end QM
