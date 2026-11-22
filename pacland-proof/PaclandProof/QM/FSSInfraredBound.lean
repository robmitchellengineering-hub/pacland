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

end FSSInfraredBound
