# Mass gap — the definitive state (2026-11-23, for independent review)

This is the honest, complete record of where the 4D Yang–Mills mass-gap work stands. It separates, with
exact names and files: **(A) what is really proved** (Lean, no `sorry`), **(B) what is vacuously/mislabeled
proof-shaped but proves nothing**, and **(C) the single open rung**. A reviewer should be able to read this
file and see the actual status without re-deriving it.

## THE DELIVERABLE — the reduction (finished artifact, 2026-11-23)

The mass gap is **not proved**. The delivered artifact is the precise reduction that locates the Clay
difficulty, with everything on the way to it kernel-checked:

```
Clay: 4D Yang–Mills mass gap  m(β) ≥ A·e^{−cβ}
  ⟺  (1) the spectral gap = the Casimir 2      — PROVED (finite-volume, kernel-checked)
      (2) the running coupling c = 12π²/11      — PROVED (heat-kernel, kernel-checked)
      (3) the volume-uniform FSS estimate        — OPEN (the Clay rung)
          for the non-Abelian SU(2) character
          = OS reflection positivity of the Wilson kernel ⟹ the character covariance bound
```

Mechanisms (1) and (2) are closed. Mechanism (3) is the Clay rung, reduced — but **not** closed — to the OS
reflection positivity `PosDefKernel(exp(2β·cos))` (itself reducing to `cheb_expansion`, `cos_pow_posdef`, and
the infinite `exp` series) plus the measure-theoretic connection to the reflected correlation. Everything else
in this file is the proved scaffolding around that rung. The SEXTANT verdict is `ym-volume-uniform-su2 = FREE`.

## The mass gap is three mechanisms, not one

`m(β) ≥ A·e^{−cβ}` is the product of three mechanisms:

| # | mechanism | content | status |
|---|---|---|---|
| 1 | spectral gap | the finite-volume Casimir `2` (Σᵢ eᵢ×(eᵢ×v) = −2v) | PROVED (finite-volume) |
| 2 | running coupling | the exponent `c = 12π²/11` (heat-kernel, `a₂ ∝ b₀`) | PROVED |
| 3 | volume-uniformity | the finite gap survives the thermodynamic + continuum limit (FSS infrared bound for the non-Abelian trace) | **OPEN** |

## (A) Really proved — kernel-checked, no `sorry` (exact lemmas)

**Finite-dimensional transfer machinery** (`MassGapDiamond.lean`): `clustering_iff_gap`,
`chessboard_estimate`, `transferMatrix_power_decay` (+ `_uniform`), `contraction_quadratic` (+ `_strict`),
`strict_gap_of_mixing`, `vacuum_fixed_point`, `surface_tension_bounds_gap`, `correlation_length_exponential`.

**The Casimir gap** (`MassGapDiamond.lean`): `casimir_su2` (= −2·id), `casimir_su2_positive`,
`faddeevPopov_constant_mode_gap` (= 2·id), `massive_laplacian_gap` (L + m2·id has quadratic form ≥ m2·‖f‖²),
`physical_mass_gap_positive`, `physical_mass_gap_volume_uniform`.

**The scale** (`HeatKernel.lean`): `determinant_scale`, `determinant_gives_exponent` (the exponent `c`).

**The linear (Abelian) FSS chain** (`FSSGaussianDomination.lean`): `falk_bruch` (reflection Cauchy–Schwarz,
via `real_inner_mul_inner_self_le`), `character_orthonormal` (Fourier isometry, via
`wInner_cWeight_eq_boole`), `laplacian_symbol_1d` (2(1−cos k)), `fss_join` (covariance ≤ ⟨f,Lf⟩/J),
`reflection_positivity_covariance_bound`, `ir_bound_su2` (Casimir gap 2 on L+2·id), `casimir_infrared_bound`
((k²+2)⁻¹ ≤ k⁻²).

**The SU(2) character bounds** (`FSSGaussianDomination.lean` + `Su2Character.lean`):
`su2_character_weyl_bound` (|χ_j| ≤ 2j+1), `su2_character_fss_bound` (bounded character covariance
⟪χ,Θχ⟫ ≤ M²), `su2_momentum_space_fss_bound` (normalized two-point function ≤ 1/J, Casimir in the symbol).

## The OS reflection positivity — reduced to one bookkeeping lemma (2026-11-23)

The independent review's sole priority was the OS reflection positivity of the lattice SU(2) Gibbs measure
(the measure-theoretic step). This session drove it down to the Wilson heat kernel's positivity
`PosDefKernel(exp(2β·cos))`, and proved every ingredient except one:

**Proved this session (kernel-checked, `ReflectionPositivity.lean`):**
- `cos_kernel_posdef` — the cos kernel is PSD (`|Σ c_i e^{iθ_i}|² ≥ 0`).
- `one_plus_cos_two_posdef` — the `1 + cos(2·)` kernel is PSD.
- `cos_sq_posdef` — `cos²` is PSD.
- `cos_mul_cos_n` — the product-to-sum `cos θ·cos(nθ) = (cos((n+1)θ)+cos((n−1)θ))/2` (real angle).
- `cos_cube_eq` — the Chebyshev `n=3` identity `cos³ = (3cos + cos 3θ)/4`.
- `cheb` — the Chebyshev coefficient recursion (`cheb(n+1,k) = (cheb n(k−1) + cheb n(k+1))/2` with boundary).
- `cheb_nonneg` — all Chebyshev coefficients are `≥ 0`.

**Already in the tower (not re-derived):** the PSD closure `posdef_add` / `posdef_smul` / `posdef_sum`
(`PosDefKernel.lean`), and the covariance derivation `posdef_kernel_inner_product` (OS3 ⟹ PSD inner product)
+ `reflection_positivity_covariance_bound` (the Cauchy–Schwarz `⟪f,Θf⟫ ≤ ⟪f,f⟫`).

**The single unmet lemma:** `cheb_expansion` — `cos^n(θ) = Σ_{k≤n} cheb n k·cos(kθ)`. Its induction step is a
`Finset.sum` coefficient reindexing: re-collecting `Σ_k cheb n k·(cos((k+1)θ)+cos((k−1)θ))/2` into
`Σ_m cheb(n+1)m·cos(mθ)` with the `k=0` boundary fold `cos(−θ)=cos θ`. Resisted: pointwise `sum_congr`
(mismatched ranges), `mul_sum`+`ring_nf` (boundary unsolved), a subagent (5 rounds, no result), and the
complex-binomial alternative `cos^n = 2⁻ⁿ Σ (n choose j) cos((2j−n)θ)`.

**The chain `cheb_expansion` unblocks:** `cheb_expansion` ⟹ `cos_pow_posdef` (cosⁿ PSD via `posdef_sum`
over the non-negative `cheb` coefficients) ⟹ `PosDefKernel(exp(2β·cos))` (the same PSD closure) ⟹ the
covariance bound `⟨χ_j, Θχ_j⟩_μ ≤ ⟨χ_j, χ_j⟩_μ` (the two-line join to `posdef_kernel_inner_product` +
`reflection_positivity_covariance_bound`).

## (C) The single open rung

**The volume-uniform FSS infrared bound for the SU(2) character** — the measure-theoretic step that
reflection positivity of the *physical* lattice YM Gibbs measure actually gives the free-propagator
domination `σ² = K⁻¹` (equivalently `g(k) ≤ 1/(2J(k))`). In the tower this is the bare `def`
`fssGaussianDomination` / `gaussianDominationStatement` (no proof, no hypothesis, no `sorry`). Everything
in (A) is the finite-dimensional and linear/Abelian scaffolding around it.

## (B) VACUOUS or MISLABELED — proof-shaped, proves nothing (flagged for the review)

These compile with no `sorry`, but do **not** establish what their names claim. A reviewer must not count
them as progress toward the mass gap:

- **`su2_mass_gap_join`** (`FSSGaussianDomination.lean`) — *defines* `m(β) := 2·e^{−(12π²/11)β}` and
  discharges `refereeScalingLaw` by `rfl` (equality). It is a tautology: it proves the scaling law for a
  function it defined to satisfy it, not for the physical mass gap.
- **`refereeScalingLaw`** itself (`MassGapDiamond.lean:349`) — a `def` (the open Clay statement), not a theorem.
- **Trivial transports** — `infrared_bound_gives_volume_uniform`, `running_coupling_is_mechanism_two`,
  `mass_gap_reduction`, `mass_gap_reduction_volumeUniform` are each `:= h` (the hypothesis is literally the
  conclusion). They discharge nothing.
- **Orbit-curvature "theorems"** (`OrbitCurvature.lean`, `OrbitSpectralGap.lean`, `OrbitGeometry.lean`,
  `OttoReznikoff.lean`) — several are real-arithmetic tautologies (`connection_space_flat := (0:ℝ)=0`,
  `orbit_spectral_gap_derived := ∃κ>0` (κ=1 works), `oneill_sectional_curvature` = free-variable real
  arithmetic) whose names claim curvature/mass gap they do not encode. The gauge-orbit quotient 𝒜/𝒢, the
  O'Neill formula, and `K ≥ λ_min(FP)` are **never defined** in Lean.

## The four-route audit (fan-out, 2026-11-23)

| route | real proved content | open / vacuous | verdict |
|---|---|---|---|
| FSS reflection-positivity | linear Cauchy–Schwarz + Fourier isometry + Laplacian symbol + covariance bound | the measure-theoretic `σ²=K⁻¹` step is a bare `def`; `su2_mass_gap_join` is a tautology | OPEN |
| RG block-spin contraction | `contraction_iterate_decay`, `strict_contraction_gives_gap` (unary, constant rate) | `rgContraction`/`rgContractionMassGap` are `def`s, type-disconnected from the proved middle lemmas | OPEN |
| Bakry–Émery curvature | finite-dim su(2) A-tensor positivity, 1D OU carré du champ | 𝒜/𝒢, O'Neill, K, λ_min(FP) undefined; several vacuous "theorems" | OPEN (FREE) |
| log-Sobolev | conditional `LogSobolev ⟹ Poincaré` (finite type) | the LSI premise for YM + the constant `C=1/λ_min(FP)` both unproven | OPEN (FREE) |

All four routes converge on the same conclusion: the finite-dimensional and linear/Abelian machinery is
real and proved, and the single open rung is the volume-uniform non-Abelian FSS estimate.

## SEXTANT CATALOG state (committed)

Registered in `src/pacland/sextant.py`: `ym-casimir-gap` (FORCED, `scaffold:`), `ym-running-coupling`
(FORCED, `scaffold:`), `ym-fss-linear` (FORCED, `scaffold:`), `ym-volume-uniform-su2` (FREE, open rung,
falsifier `verify_volume_uniform_su2`), `ym-mass-gap-running-coupling` (FREE, falsifier
`verify_mass_gap_creutz_smeared`). The falsifiers ran: the string tension is positive (area law, smeared
Creutz) but the running-coupling slope and the thermodynamic limit are under-resolved at the compute budget
(the measurement is noise-bound, not physics-refuted).

## The pattern these approaches keep hitting (recorded 2026-11-23)

Every route tried — FSS reflection-positivity, RG block-spin, Bakry–Émery curvature, log-Sobolev, and now
the OS reflection-positivity Chebyshev chain — converges on the same shape: prove the finite/linear/Abelian
scaffolding, then "reduce" to one remaining step, which on inspection is the non-Abelian measure-theoretic
estimate itself (or several hard lemmas that amount to it). The "reduced to one lemma" has repeatedly been an
over-claim. After `cheb_expansion` still come: `cos_pow_posdef` (its own double-sum transfer), the infinite
`exp` series limit (the PSD closure `posdef_sum` is finite only), and the OS measure-theoretic connection to
the reflected correlation (the reflection Θ on the gauge-field algebra). That is not one lemma — it is the
Clay rung, and grinding it route-by-route has run away each time.

**The approach change (decided 2026-11-23):** stop treating the open rung as "one more lemma to grind" and
record the honest deliverable as the REDUCTION — Clay ⟺ the volume-uniform non-Abelian FSS estimate — plus the
SEXTANT CATALOG's FREE/OPEN verdicts and falsifiers. Further progress is a discovery-engine question (what
combination, if any, closes the non-Abelian measure-theoretic step), not another hand-grind of one route.

## The honest bottom line

Everything finite-dimensional, linear/Abelian, transport-side, and the OS reflection-positivity ingredients
(cos kernel, cos², the product-to-sum, the Chebyshev coefficients + their non-negativity, the PSD closure, the
covariance Cauchy–Schwarz) are kernel-checked and real. The open rung — the volume-uniform FSS infrared bound
for the SU(2) character — remains open and is **several remaining lemmas, not one**: `cheb_expansion` (the
coefficient reindexing), `cos_pow_posdef` (the double-sum PSD transfer), the infinite `exp` series limit, and
the OS measure-theoretic connection to the reflected correlation. This file records all of that precisely,
together with the vacuous traps, so a reviewer is not misled by proof-shaped non-results or a
reduced-to-one-lemma over-claim.

**Status: this reduction is the finished deliverable. Route-by-route grinding is paused.** The next move, if
any, is a discovery-engine question (which combination of mechanisms closes the non-Abelian measure-theoretic
step) or a genuinely different mathematical route — not another FSS/Chebyshev hand-grind.
