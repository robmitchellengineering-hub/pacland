# Mass gap — the definitive state (2026-11-23, for independent review)

This is the honest, complete record of where the 4D Yang–Mills mass-gap work stands. It separates, with
exact names and files: **(A) what is really proved** (Lean, no `sorry`), **(B) what is vacuously/mislabeled
proof-shaped but proves nothing**, and **(C) the single open rung**. A reviewer should be able to read this
file and see the actual status without re-deriving it.

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

## The honest bottom line

Everything finite-dimensional, linear/Abelian, and transport-side is kernel-checked and real. The **single
open rung** is the volume-uniform FSS infrared bound for the SU(2) character — the non-Abelian reflection
positivity that survives the thermodynamic + continuum limit. It is the Clay rung, and this file records
that precisely, together with the vacuous traps so a reviewer is not misled by proof-shaped non-results.
