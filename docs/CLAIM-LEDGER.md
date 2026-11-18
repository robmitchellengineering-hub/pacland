# Claim ledger — the honest status of every mass-gap theorem

Each theorem is tagged with one status:

- **proven-general** — a real theorem, no chosen model, no open hypothesis.
- **proven-in-a-model** — proven for a CHOSEN model (e.g. `M(p) = p²`), not derived from the physical object.
- **conditional** — proven assuming an explicit hypothesis that is NOT yet discharged.
- **cited** — a known result (stated, referenced to the literature), not re-derived.
- **open** — a conjecture / statement, not proven.
- **vacuous** — true but empty (`∃ κ > 0`, `0 = 0`); carries no content.

This exists because the geometric route shipped vacuous/overclaimed theorems as if they were results.
Run `scripts/vacuity_linter.py` alongside it: the linter surfaces the suspicious patterns, this file tags
the status after review.

## The Coulomb / Gribov chain (`MassGapDiamond.lean`)

| theorem | status | note |
|---|---|---|
| `crossProduct_ne_zero` | proven-general | the 𝔰𝔲(2) bracket is non-trivial (real algebra) |
| `casimir_su2` | proven-general | `−Σᵢ ad(eᵢ)² = −2·id` (real algebra) |
| `faddeevPopov_constant_mode_gap` | proven-general | the FP constant-mode gap 2 |
| `massive_laplacian_gap` | proven-general | full-operator gap ≥ m² |
| `ad_e3_zero_mode` | proven-general | the Cartan zero mode |
| `gribovGhost_zero` | proven-in-a-model | `M(p) = p²` CHOSEN; the horizon condition is open |
| `gribov_confinement` | proven-in-a-model | `1/p⁴` is algebra on the `M(p) = p²` model |
| `yukawa_deconfinement` | proven-general | the ghost mass deconfines (real) |
| `coulomb_confinement_mass_gap` | conditional | assumes `σ_Coul > 0` |

## The finite-β mass gap (`ConstructiveQFT.lean`)

| theorem | status | note |
|---|---|---|
| `mass_gap_from_mixing` | proven-general | mixing ⟹ Δ > 0 (finite matrix) |
| `mass_gap_from_hypotheses` | proven-general | OS + mixing ⟹ Δ > 0 — BUT `T` is a finite `Fin m` matrix, a discretisation, not `SU(2)^E` |
| `thermodynamic_limit_mass_gap` | conditional | needs antitone + bounded-below |
| `mayer_series_converges` | proven-general | exponential decay ⟹ series converges (abstract) |
| `clustering_implies_cluster_expansion` | conditional | needs the clustering rate λ₁ < 1 |
| `physical_mass_gap_constant` | conditional | needs the matching exponent `m_lattice ~ a` |

## The transmutation chain

| theorem | status | note |
|---|---|---|
| `one_loop_integral_log` | proven-general | the exact antiderivative (real computation) |
| `log_gap_to_exp` | proven-general | log ⟹ exponential (real computation) |
| `betaFunctionOneLoop` + `b0_su2_positive` | cited + proven | the `11/3` coefficient is the known GWP result; the SIGN from the Casimir is proven |
| `orbitBE_curvature_at_2pi_over_3` / `orbitBE_fails_for_large_beta` | proven-general | the quotient curvature is β-dependent (real) |

## The geometric route (`OrbitCurvature.lean`, `OrbitGeometry.lean`, `OrbitSpectralGap.lean`)

| theorem | status | note |
|---|---|---|
| `aTensor_nonzero` | proven-general | `[T₁,T₂] = T₃` (real) |
| `connection_space_flat` | **vacuous** | `0 = 0 := rfl` |
| `kinetic_metric_pos_def` | proven-general (trivial) | `0 ≤ ‖α‖²` |
| `oneill_sectional_curvature` | proven-general (trivial) | `K + ¾KA ≥ K` (from `KA ≥ 0`) |
| `orbit_space_positive_curvature` | conditional (trivial) | `0 < K + ¾KA` from `hK, hA` |
| `orbit_space_mass_gap` | proven-in-a-model (trivial) | literally `orbit_space_positive_curvature`; NOT a mass gap |
| `orbit_bracket_witness_pos` / `orbit_bracket_witness_pos_inv` | **vacuous** | `∃ κ > 0` (κ = 1) |
| `full_curvature_not_beta_independent` | TOY | arithmetic on the `wilsonHessian`/`bakryEmeryCurvature` definitions |
| `gap_is_beta_dependent` | TOY (overstated) | ∃θ with negative pointwise BE ≠ the gap is β-dependent |

## Open (the Clay rung — do not claim)

- **Construction** — the 4D measure exists, satisfies the OS axioms.
- **Non-perturbative mass gap** — Δ > 0 in the infinite-volume + continuum limit.
- **The horizon condition** — derive `M(p)` from the Faddeev–Popov operator (open).
- **The matching exponent** — `m_lattice` runs at the AF rate (the renormalization, open).
- **Linking the Langevin-generator gap to the transfer-matrix gap** — never done in the code.
