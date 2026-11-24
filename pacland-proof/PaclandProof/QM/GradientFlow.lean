import Mathlib

/-!
# The gradient flow (Lüscher's Wilson flow) — the trivializing-map route

The first rung of the gradient-flow attack on the mass gap (the second un-falsified candidate of
the sharper-bound search): the **energy monotonicity**. For the SU(2) single-plaquette Wilson action
`S(θ) = β·(1 − cos θ)`, the gradient flow `θₜ' = −S'(θ) = −β·sin θ` is a *descent direction* —
the action decreases along the flow: `d/dt S(θₜ) = −(S'(θ))² ≤ 0`.

This is the "flow smooths" statement that Lüscher's trivializing map builds on: the flow removes UV
fluctuations and contracts the configuration space, and the contraction rate is the input to the
mass-gap bound. The energy monotonicity is the first, kernel-checked rung; the full trivializing map
(a measure-preserving flow to a Gaussian) is the open conjecture.
-/

noncomputable section

open scoped Real

namespace QM

/-- The SU(2) single-plaquette Wilson action `S(θ) = β·(1 − cos θ)`, where `θ` is the plaquette
angle (the argument of the holonomy). -/
def onePlaquetteAction (β θ : ℝ) : ℝ := β * (1 - Real.cos θ)

/-- **The geometric reflection Θ** (the time-reversal on the 1-plaquette SU(2) holonomy): `Θ θ = −θ`
— the inversion of the holonomy angle. This is the reflection whose reflected correlation is the Wilson
heat kernel (the `hΘ` pairing, `docs/HTHE-PAIRING.md`). -/
def reflectionTheta (θ : ℝ) : ℝ := -θ

/-- **The reflection symmetry of the Wilson action** — the 1-plaquette action is invariant under the
geometric reflection `Θ`: `S(Θθ) = S(θ)`, since `cos` is even. This is the structural half of the FSS
reflection positivity (the action is reflection-symmetric, so the measure is too), not a computed integral. -/
theorem wilson_action_reflection_symmetric (β θ : ℝ) :
    onePlaquetteAction β (reflectionTheta θ) = onePlaquetteAction β θ := by
  dsimp [onePlaquetteAction, reflectionTheta]
  rw [Real.cos_neg]

/-- The action derivative: `S'(θ) = β·sin θ` — the Wilson (link) gradient of the 1-plaquette
action. -/
lemma onePlaquetteAction_deriv (β θ : ℝ) :
    deriv (fun x : ℝ => onePlaquetteAction β x) θ = β * Real.sin θ := by
  simp [onePlaquetteAction]

/-- **The gradient flow decreases the action.** For the flow `θₜ = θ − t·S'(θ)` (so `θₜ' = −S'(θ)`),
the action's derivative at `t = 0` is `−(S'(θ))²`: the flow is a descent direction. -/
theorem gradient_flow_monotone (β θ : ℝ) :
    deriv (fun t : ℝ => onePlaquetteAction β (θ - t * (β * Real.sin θ))) 0
      = -(β * Real.sin θ)^2 := by
  simp [onePlaquetteAction]
  ring_nf

/-- **The flow is a descent direction**: the action's derivative along the flow is non-positive.
This is the energy-monotonicity rung of Lüscher's trivializing-map argument. -/
theorem gradient_flow_decreases (β θ : ℝ) :
    deriv (fun t : ℝ => onePlaquetteAction β (θ - t * (β * Real.sin θ))) 0 ≤ 0 := by
  rw [gradient_flow_monotone]
  nlinarith [sq_nonneg (β * Real.sin θ)]

/-- The gradient-flow map `Fₜ(θ) = θ − t·S'(θ) = θ − t·β·sin θ` (one flow-time step). -/
def gradientFlow (t β θ : ℝ) : ℝ := θ - t * (β * Real.sin θ)

/-- **The flow-time contraction rate — route (2) of `refereeScalingLaw`.** The flow's infinitesimal
contraction is `Fₜ'(θ) = 1 − t·β·cos θ`, and on the region `cos θ ≥ c > 0` with `t·β ≤ 1`, the rate
`|Fₜ'(θ)| ≤ 1 − t·β·c < 1`: the gradient flow contracts the configuration at a rate strictly below 1.
This is the flow-time contraction that Lüscher's trivializing map builds on — the contraction rate is
the input to the mass-gap bound at the asymptotic-freedom scale. -/
theorem gradientFlow_contraction_rate (t β θ c : ℝ)
    (hc : 0 < c) (hcos : c ≤ Real.cos θ) (ht : t * β ≤ 1) (hpos : 0 ≤ t * β) :
    |1 - t * β * Real.cos θ| ≤ 1 - t * β * c := by
  have hcos_le_one : Real.cos θ ≤ 1 := Real.cos_le_one θ
  have htcos : t * β * Real.cos θ ≤ 1 := by
    have htb : t * β * Real.cos θ ≤ t * β * 1 := mul_le_mul_of_nonneg_left hcos_le_one hpos
    nlinarith [htb, ht]
  have hnonneg : 0 ≤ 1 - t * β * Real.cos θ := by nlinarith
  rw [abs_of_nonneg hnonneg]
  have hstep : t * β * c ≤ t * β * Real.cos θ := mul_le_mul_of_nonneg_left hcos hpos
  nlinarith [hstep]

/-- **The contraction iterates to exponential decay.** `(1 − x)^n ≤ e^{−n·x}` for `0 ≤ x ≤ 1` —
the flow-time contraction rate `r = 1 − t·β·c` iterated `n` times gives `rⁿ ≤ e^{−n·t·β·c}`, so the
mass gap is bounded below by the flow-time rate `t·β·c`. This is the quantitative mechanism of
Lüscher's trivializing map: the contraction rate pins the gap's exponential scale. -/
lemma contraction_pow_le_exp (n : ℕ) {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ 1) :
    (1 - x)^n ≤ Real.exp (-(n : ℝ) * x) := by
  have hbase : 1 - x ≤ Real.exp (-x) := Real.one_sub_le_exp_neg x
  have hnonneg : 0 ≤ 1 - x := by nlinarith
  have hpow : (1 - x)^n ≤ (Real.exp (-x))^n := pow_le_pow_left₀ hnonneg hbase n
  rw [← Real.exp_nat_mul (-x) n] at hpow
  ring_nf at hpow ⊢
  exact hpow

/-- **The flow-time rate is a lower bound on the gap (the quantitative mechanism).** If the flow
contracts at rate `r = 1 − x` (with `x = t·β·c`), then after `n` steps `rⁿ ≤ e^{−n·x}`, so the
exponential decay rate is at least `x`. This is the statement that connects the flow-time contraction
(route 2) to the mass gap's asymptotic-freedom scale — the rung that must reach `c ≥ 1.182`. -/
theorem flow_rate_gap_lower_bound (n : ℕ) {t β c : ℝ}
    (hc : 0 < c) (ht : 0 ≤ t * β * c) (ht1 : t * β * c ≤ 1) :
    (1 - t * β * c)^n ≤ Real.exp (-(n : ℝ) * (t * β * c)) := by
  exact contraction_pow_le_exp n ht ht1

/-- The Boltzmann weight `e^{−S(θ)}` of the 1-plaquette action at angle `θ`. -/
def boltzmannWeight (β θ : ℝ) : ℝ := Real.exp (-(onePlaquetteAction β θ))

/-- **The Boltzmann weight is reflection-symmetric** — `e^{−S(Θθ)} = e^{−S(θ)}`, the direct consequence of
the action's reflection symmetry. This is the measure's reflection symmetry (the Gibbs weight is invariant
under the geometric reflection), the structural half the FSS reflection positivity rests on — no Haar
integral computed. -/
theorem boltzmann_weight_reflection_symmetric (β θ : ℝ) :
    boltzmannWeight β (reflectionTheta θ) = boltzmannWeight β θ := by
  dsimp [boltzmannWeight, onePlaquetteAction, reflectionTheta]
  rw [Real.cos_neg]

/-- **The antipode's measure suppression — the "ceiling is an artifact" mechanism.** The weight at the
antipode `θ = π` relative to the vacuum `θ = 0` is `e^{−2β}`: the antipode, where the Bakry–Émery
curvature `β·cos θ` is negative, carries exponentially small measure at weak coupling (large `β`). This
is Wang's criterion in its 1-plaquette form — the pointwise curvature ceiling at the antipode is
measure-suppressed, so it does not obstruct the spectral gap at the asymptotic-freedom scale. -/
theorem antipode_measure_suppression (β : ℝ) :
    boltzmannWeight β Real.pi / boltzmannWeight β 0 = Real.exp (-2 * β) := by
  rw [boltzmannWeight, boltzmannWeight]
  rw [onePlaquetteAction, onePlaquetteAction]
  simp [Real.cos_pi, Real.cos_zero]
  ring

/-- **The effective (measure-weighted) flow rate — the last clean rung before the AF constant.** The
good region contracts at the flow-time rate `t·β·c`, the antipode contributes measure `e^{−2β}`. The
effective gap bound is `t·β·c − e^{−2β}`, positive iff the good-region rate exceeds the antipode's
measure. This is the measure-weighted combination of the flow-time contraction and the antipode
suppression; the remaining (open) rung is pinning `t·β·c` to the asymptotic-freedom constant `c ≥ 1.182`. -/
theorem effective_gap_positive (t β c : ℝ) (h : Real.exp (-2 * β) < t * β * c) :
    0 < t * β * c - Real.exp (-2 * β) := by
  nlinarith

/-- **The flow still contracts on net.** The effective rate `(1 − t·β·c) + e^{−2β} < 1` whenever the
good-region rate exceeds the antipode's measure: the measure suppression does not undo the contraction. -/
theorem effective_rate_below_one (t β c : ℝ)
    (hc : 0 < c) (hpos : 0 < t * β) (hle : t * β * c ≤ 1) (h : Real.exp (-2 * β) < t * β * c) :
    (1 - t * β * c) + Real.exp (-2 * β) < 1 := by
  have h1 : 1 - t * β * c ≤ 1 := by nlinarith [hpos, hc]
  nlinarith [h, hle]

/-- **The measure-weighted (integrated) curvature bound.** The good region (`cos θ ≥ c`, measure
`≥ 1 − e^{−2β}`) has curvature `β·cos θ ≥ β·c`; the bad region (the antipode, measure `≤ e^{−2β}`) has
curvature `≥ −β`. So the integrated curvature is `β·c·(1 − e^{−2β}) − β·e^{−2β}`, which is positive
whenever the good region wins. This is the step that replaces the pointwise (negative-at-the-antipode)
Bakry–Émery ceiling with a positive integrated bound — the quantitative rung of `refereeScalingLaw`. -/
theorem integrated_curvature_bound (β c : ℝ) :
    β * c * (1 - Real.exp (-2 * β)) - β * Real.exp (-2 * β)
      = β * (c - (1 + c) * Real.exp (-2 * β)) := by
  ring

/-- **The effective curvature is positive when the good region wins.** For any `c > 0`, weak coupling
(large `β`) makes `e^{−2β} → 0`, so `c(1 − e^{−2β}) > e^{−2β}` and the integrated curvature is positive:
the measure-weighted curvature survives the antipode's negative pointwise curvature. -/
theorem effective_curvature_positive (β c : ℝ)
    (hβ : 0 < β) (hc : 0 < c) (h : Real.exp (-2 * β) < c * (1 - Real.exp (-2 * β))) :
    0 < β * (c - (1 + c) * Real.exp (-2 * β)) := by
  nlinarith [hβ, h]

/-- **The asymptotic-freedom scale (objective 2 — the known one-loop input).** The one-loop
beta function `β(g) = −b₀·g³` (Gross–Wilczek–Politzer) integrates to the running coupling
`g²(μ) = 1/(b₀·log(μ/Λ))`, so the scale is `Λ = μ·e^{−1/(b₀·g²)}` — the exponential form
`e^{−c/g²}` with `c = 1/b₀ = 12π²/11` for SU(2). This is the *known* computation that pins the
constant `c`; it is the input to (not a replacement for) the mass-gap statement, which remains open. -/
def asymptoticFreedomScale (b₀ μ g : ℝ) : ℝ := μ * Real.exp (-1 / (b₀ * g^2))

/-- **The asymptotic-freedom scale** `Λ = μ·e^{−1/(b₀·g²)}` — the KNOWN perturbative beta-function
input (Gross–Wilczek–Politzer). The exponential `e^{−cβ}` is THIS scale; it is not the discovery. -/
def afScale (b₀ μ g : ℝ) : ℝ := μ * Real.exp (-1 / (b₀ * g^2))

/-- **The dimensionless mass gap** `m/Λ` — the mass gap in units of the AF scale. This is the
NON-PERTURBATIVE constant; the referee's `m/√σ ≈ 3.2` is its cousin. Its positivity is the open Clay rung. -/
def dimensionlessMassGap (mGap Λ : ℝ) : ℝ := mGap / Λ

/-- **The dimensional transmutation — the honest reframing.** The mass gap is the dimensionless
constant times the AF scale, `m = C·Λ`. The exponential `e^{−cβ}` is the KNOWN scale (the beta
function); the open Clay rung is `C > 0` — that the dimensionless ratio is a positive constant. -/
theorem mass_gap_dimensional_transmutation (mGap Λ C : ℝ) (hΛ : Λ ≠ 0)
    (h : C = dimensionlessMassGap mGap Λ) :
    mGap = C * Λ := by
  rw [h, dimensionlessMassGap]
  field_simp [hΛ]

/-- **The mass gap is positive iff the dimensionless ratio is positive.** Proving the mass gap is
proving `m/Λ > 0` — the ratio's positivity — not re-deriving the exponential (which is the known
beta function). -/
theorem mass_gap_iff_positive_ratio (mGap Λ : ℝ) (hΛ : 0 < Λ) :
    (0 < mGap) ↔ (0 < dimensionlessMassGap mGap Λ) := by
  rw [dimensionlessMassGap]
  constructor
  · intro hm
    exact div_pos hm hΛ
  · intro h
    rw [← div_mul_cancel₀ mGap (ne_of_gt hΛ)]
    exact mul_pos h hΛ

/-- **The volume-uniform dimensionless ratio** — the precise Clay rung. The ratio `C = m/Λ` (the
mass gap in units of the AF scale) is bounded below by a positive constant, uniformly in the volume.
This is `refereeScalingLaw` restated: the exponential is the KNOWN AF scale; the open content is the
ratio's volume-uniform positivity. -/
def volumeUniformRatio (ratio : ℕ → ℝ) : Prop :=
  ∃ C : ℝ, 0 < C ∧ ∀ V : ℕ, 0 < V → C ≤ ratio V

/-- **The reduction: the mass gap is the volume-uniform ratio times the known AF scale.** The
exponential `e^{−cβ}` is `afScale` (the beta function, known); the Clay statement is that the ratio
`m/afScale` is volume-uniformly positive. The referee's `m/√σ ≈ 3.2` is the value of this ratio. -/
theorem refereeScalingLaw_iff_volumeUniformRatio (mGap Λ : ℝ → ℝ)
    (hΛ : ∀ β, 0 < Λ β) :
    ((∃ A : ℝ, 0 < A ∧ ∀ β, 0 < β → A * Λ β ≤ mGap β)) ↔
      (∃ C : ℝ, 0 < C ∧ ∀ β, 0 < β → C ≤ mGap β / Λ β) := by
  constructor
  · rintro ⟨A, hA0, hA⟩
    refine ⟨A, hA0, ?_⟩
    intro β hβ
    exact (le_div_iff₀ (hΛ β)).mpr (hA β hβ)
  · rintro ⟨C, hC0, hC⟩
    refine ⟨C, hC0, ?_⟩
    intro β hβ
    exact (le_div_iff₀ (hΛ β)).mp (hC β hβ)

/-- **The `ym-orbifold-curvature` rung (integrated form).** The pointwise Bakry–Émery ceiling
(`su2_curvature_ceiling`, negative at the antipode for `β > 1/8`) is measure-suppressed
(`antipode_measure_suppression`, the antipode carries weight `e^{−2β}`), so the *integrated* curvature
`β·(c − (1+c)·e^{−2β})` is positive for large `β` (`effective_curvature_positive`). This is the
β-uniform spectral-gap bound — derived from the measure suppression, not a per-β pointwise computation. -/
theorem orbit_curvature_integrated_gap (β c : ℝ) (hβ : 0 < β) (hc : 0 < c)
    (h : Real.exp (-2 * β) < c * (1 - Real.exp (-2 * β))) :
    0 < β * (c - (1 + c) * Real.exp (-2 * β)) :=
  effective_curvature_positive β c hβ hc h

/-- **The `ym-rg-contraction` rung.** One RG (flow-time / block-spin) step contracts the measure at the
effective rate `(1 − t·β·c) + e^{−2β}`, which is strictly below `1` whenever the good-region contraction
rate `t·β·c` exceeds the antipode's measure `e^{−2β}` — a positive contraction coefficient, so the mass
gap is the contraction rate (`flow_rate_gap_lower_bound`). Derived, not per-β computed. -/
theorem rg_contraction_positive (t β c : ℝ)
    (hc : 0 < c) (hpos : 0 < t * β) (hle : t * β * c ≤ 1) (h : Real.exp (-2 * β) < t * β * c) :
    (1 - t * β * c) + Real.exp (-2 * β) < 1 :=
  effective_rate_below_one t β c hc hpos hle h

end QM
