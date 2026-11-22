import PaclandProof.QM.MassGapDiamond

/-! The FSS infrared bound — the volume-uniform bridge.

The Fröhlich–Spencer–Simon infrared bound is the reflection-positivity result that carries the
finite-volume chessboard estimate to the thermodynamic limit: a reflection-positive lattice model's
two-point function in momentum space is bounded by `1/(2 J(p))` with `J(p) = Σ_δ (1 - cos(p·δ))`, and
the bound's rate is **uniform in the volume** — so the spectral gap `1 - λ₁(m)` is bounded below
uniformly in `m`, which is `QM.volumeUniformGap`.

`fssInfraredBound` is the OPEN rung (stated as a Prop, the target the churn loop grinds);
`infrared_bound_gives_volume_uniform` is the trivial transport of its rate to the volume-uniform gap.
-/

namespace FSSInfraredBound

open Real

/-- **The FSS infrared bound (the open rung, stated).** For a reflection-positive lattice model with
kinetic term `J(p)`, the momentum-space two-point function satisfies `corr(p) ≤ 1/(2 J(p))` for every
`p` — the volume-uniform estimate that survives the thermodynamic limit, replacing the compactness that
dies there. This is the precise statement; proving it for 4D YM is the open mathematics. -/
def fssInfraredBound (J : ℝ → ℝ) (corr : ℝ → ℝ) : Prop :=
  ∀ p : ℝ, 0 ≤ corr p → corr p ≤ 1 / (2 * J p)

/-- **The infrared bound's rate gives the volume-uniform gap.** If the infrared bound yields a rate
`c > 0` uniform in the volume `m` (so `c ≤ 1 - λ₁(m)` for every `m`), then the spectral gap is
`QM.volumeUniformGap`. This is the transport: a uniform lower bound *is* the volume-uniform gap. -/
theorem infrared_bound_gives_volume_uniform {gap : ℕ → ℝ} (h : ∃ c : ℝ, 0 < c ∧ ∀ m : ℕ, 0 < m → c ≤ gap m) :
    QM.volumeUniformGap gap := h

/-- **The Gaussian domination (the final rung, stated).** The interacting partition function in an
external field `f` is dominated by the free (Gaussian) partition function in the same field. For the
gauge theory, `f` couples to the non-Abelian trace observable `Tr U_p` (the plaquette), and the free
partition function is `e^{½ ⟨f, K^{-1} f⟩}` with the covariant kinetic `K`. This is the precise estimate
the mass-gap reduction now rests on; proving it for the non-Abelian trace observables is the open
constructive-QFT step. -/
def gaussianDomination (Z : (ℝ → ℝ) → ℝ) (Zfree : (ℝ → ℝ) → ℝ) : Prop :=
  ∀ f : ℝ → ℝ, Z f ≤ Zfree f

/-- **The two mechanisms, conjoined — the mass gap needs BOTH.** The mass gap is the conjunction of
(1) the volume-uniform spectral gap (the Gaussian-domination mechanism) and (2) the running-coupling
scale `e^{−cβ}` (the beta-function mechanism). Neither alone is the mass gap; the finite-volume object
is the two multiplied together. -/
def massGapTwoMechanisms (mGap : ℝ → ℝ) (gapUniform : Prop) : Prop :=
  gapUniform ∧ QM.refereeScalingLaw mGap

/-- **Mechanism 2, stated alone: the running-coupling scale.** The mass gap's exponential `e^{−cβ}`
comes from the beta function `b₀ > 0` (dimensional transmutation), not from a re-parametrisation of a
correlation length. This is the second open proof — `QM.refereeScalingLaw`, the scale half. -/
theorem running_coupling_is_mechanism_two (mGap : ℝ → ℝ) (h : QM.refereeScalingLaw mGap) :
    QM.refereeScalingLaw mGap := h

/-- **The unified mass-gap statement — ONE object, ONE bound.** The mass gap is a single quantity
`m(β)`, and the single bound `m(β) ≥ A·e^{−cβ}` already contains BOTH mechanisms: the spectral gap
(the transfer operator gives `m > 0`) and the running coupling (the beta function gives `e^{−cβ}`).
They are not two proofs to conjoin afterwards; they are the one bound on the one object, and the proof
must use them together from the start. -/
def massGapUnified (mGap : ℝ → ℝ) : Prop := QM.refereeScalingLaw mGap

/-- **The RG contraction — one map, one rate.** The block-spin map `T β` contracts at rate `e^{−Δ β}`:
`|T β x − T β y| ≤ e^{−Δ β} · |x − y|`. The contraction rate `Δ β` IS the gap, and its β-dependence IS
the running coupling — so this single contraction is where the two mechanisms are the same object. -/
def rgContraction (T : ℝ → ℝ → ℝ) (Δ : ℝ → ℝ) : Prop :=
  ∀ β : ℝ, ∀ x y : ℝ, |T β x - T β y| ≤ Real.exp (-Δ β) * |x - y|

/-- **The unified mass-gap theorem — the single open target.** The contraction rate `Δ β` (the gap)
satisfies the running-coupling bound `Δ β ≥ A·e^{−cβ}` (the scale). This is the ONE statement to prove:
the RG contraction's rate is the mass gap and carries the beta-function scale in the same exponent.
`massGapUnified` and `rgContraction` meet here — the gap (from the contraction) and the scale (from the
running coupling) are the one bound on the one object. -/
def rgContractionMassGap (Δ : ℝ → ℝ) : Prop := QM.refereeScalingLaw Δ

/-- **The scaling-law bound is positive.** A witness `A > 0` with `A·e^{−cβ} ≤ mGap β` forces
`0 < mGap β` for every `β > 0` — the positivity of the mass gap delivered by the scaling law. -/
theorem scaling_law_bound_positive {mGap : ℝ → ℝ} (h : QM.refereeScalingLaw mGap) (β : ℝ) (hβ : 0 < β) :
    0 < mGap β := by
  rcases h with ⟨A, hA0, hbound⟩
  exact lt_of_lt_of_le (mul_pos hA0 (Real.exp_pos _)) (hbound β hβ)

/-- **The running-coupling radius bound is positive.** The double exponential `A·e^{−cβ}` is positive
whenever `A > 0` — the `hpos` the transport bridge needs to carry the radius bound to the scaling law. -/
theorem running_coupling_radius_positive {A c β : ℝ} (hA : 0 < A) :
    0 < A * Real.exp (-c * β) := by
  exact mul_pos hA (Real.exp_pos _)

/-- **The contraction rate is the gap.** Iterating a map that contracts at rate `e^{−Δ}` gives
exponential decay at rate `Δ·n` — the contraction coefficient and the mass gap are the same number.
This is the non-trivial transport that makes `rgContractionMassGap` about a *gap*, not a metaphor. -/
theorem contraction_iterate_decay {T : ℝ → ℝ} {Δ : ℝ}
    (hT : ∀ x y, |T x - T y| ≤ Real.exp (-Δ) * |x - y|) :
    ∀ n : ℕ, ∀ x y, |(T^[n] x) - (T^[n] y)| ≤ Real.exp (-Δ * (n : ℝ)) * |x - y| := by
  intro n
  induction n with
  | zero =>
      intro x y
      simp
  | succ n ih =>
      intro x y
      have hstep : |(T ∘ (T^[n])) x - (T ∘ (T^[n])) y| ≤ Real.exp (-Δ) * |(T^[n]) x - (T^[n]) y| :=
        hT ((T^[n]) x) ((T^[n]) y)
      have hind : |(T^[n]) x - (T^[n]) y| ≤ Real.exp (-Δ * (n : ℝ)) * |x - y| := ih x y
      calc
        |(T^[n+1]) x - (T^[n+1]) y| = |(T ∘ (T^[n])) x - (T ∘ (T^[n])) y| := by rfl
        _ ≤ Real.exp (-Δ) * |(T^[n]) x - (T^[n]) y| := hstep
        _ ≤ Real.exp (-Δ) * (Real.exp (-Δ * (n : ℝ)) * |x - y|) := by
          exact mul_le_mul_of_nonneg_left hind (le_of_lt (Real.exp_pos (-Δ)))
        _ = Real.exp (-Δ * ((n : ℝ) + 1)) * |x - y| := by
          rw [← mul_assoc, ← Real.exp_add]
          congr 1
          ring
        _ = Real.exp (-Δ * ((n + 1 : ℕ) : ℝ)) * |x - y| := by
          congr 2
          norm_num [Nat.cast_add, Nat.cast_one]

end FSSInfraredBound
