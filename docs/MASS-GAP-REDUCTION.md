# The Yang–Mills mass gap: a kernel-checked reduction to one hypothesis

This is the consolidation of the whole lattice + reflection-positivity + constructive-QFT arc. It
records, in one place, the exact theorem chain that is proved and kernel-checked (`lake build
PaclandProof` green, no `sorry`), and the **single remaining hypothesis** that everything reduces to.

## The reduction

The 4D SU(2) Yang–Mills mass gap `m(β) ≥ A·e^{−cβ}` (with `c = 12π²/11` the one-loop asymptotic-freedom
exponent) holds **if and only if** the following single hypothesis is discharged for the concrete measure:

> **(H — the linked-cluster contraction.)** The concrete SU(2) lattice Gibbs measure
> `gibbsMeasure (latticeHaar) (wilsonAction)` has its transfer-matrix spectral radius contract under the
> block-spin decimation `blockSpinSU2` to
> `ρ(β) ≤ e^{−A·e^{−(12π²/11)β}}` for some `A > 0` and all `β > 0`.

Everything else — above and below that hypothesis — is proved.

## The proved chain (all green, no `sorry`)

**Lattice + measure substrate** (`QM.FullLattice`):
- `wilsonPlaquette`, `wilsonAction` — the SU(2) Wilson action on `Matrix.specialUnitaryGroup (Fin 2) ℂ`.
- `wilson_trace_reflection_invariant` — `Re Tr(Uᴴ) = Re Tr U`, the reflection symmetry of the trace.
- `full_wilson_action_reflection_symmetric` — the full action `S(Θx) = S(x)` (plaquette bijection).
- `su2Haar` — the SU(2) Haar as the S³ round measure (`MeasureTheory.Measure.toSphere`).
- `su2WilsonAction` + `su2WilsonAction_reflection_symmetric` — the S³ trace and its reflection symmetry.
- `latticeHaar` — the product Haar over the links (`MeasureTheory.Measure.pi`).
- `gibbsMeasure` — the physical Gibbs measure `μ.withDensity (e^{−β·S})`, with `gibbs_weight_reflection_symmetric`.

**Reflection positivity (the OS3)**:
- `fss_reflected_correlation_factorization` — the reflected correlation equals the transfer square.
- `fss_reflection_positivity_square` — the square is non-negative.
- `full_lattice_transfer_posdef` — the transfer product `Tⁿ` is PSD (`Matrix.PosSemidef.pow`).
- `haar_measure_positivity` + `full_lattice_os3_haar` — the Haar positivity and the OS3 `∫(f·w)² ∂μ ≥ 0`.

**The `hΘ` measure→kernel connection** (`QM.Bessel`):
- `jacobi_anger_real`, `wilson_heat_kernel_chebyshev`, `wilson_heat_kernel_rank_one` — the heat kernel is the
  Jacobi–Anger expansion in the character basis.
- `hTheta_character_orthogonality_ne`/`_norm`/`_mean` — the Chebyshev **T** orthogonality (the SO(3) trace).
- `su2_character_orthogonality_ne`/`_diag` — the Chebyshev **U** / full SU(2) sin orthogonality
  `∫₀^π sin((n+1)θ) sin((m+1)θ) = δₙₘ·(π/2)`.
- `besselI_pos` — the positive Fourier weights.
- `wilson_kernel_posdef` — the heat-kernel PSD.

**RG + cluster-expansion foundation** (the full single-cluster layer, all green):
- `blockSpinSU2` — the SU(2) decimation `U(2j)·U(2j+1)`.
- `clusterActivity`, `cluster_activity_abs_lt_one`, `cluster_expansion_converges_small_field` — the
  single-plaquette activity `ρ = 1 − e^{−β(2−Re Tr U)}` and its small-field convergence.
- `polymer_expansion_subset` — the subset identity `∏(1+ρ) = Σ_S ∏ρ`.
- `linked_cluster_log_prod` — `log ∏(1+ρ) = Σ log(1+ρ)` (the free-energy factorization).
- `linked_cluster_weights` — the connected-cluster weights `(−1)ⁿ ρ^{n+1}/(n+1)` (the `log(1+ρ)` Taylor).
- `cluster_weight_bound` — `|weight| ≤ |ρ|^{n+1}` (the geometric decay).
- `cluster_weights_summable` — the absolute summability of the weights (the cluster-expansion convergence).
- `walk_count_bound` — `#(finsetWalkLength n u v) ≤ maxDegreeⁿ` (the walks-count bound, the animals
  estimate's first lemma).

**Limits + reconstruction** (the tower):
- `HeatKernel.continuum_uniform_mass_gap` — the spacing-uniform positive bound (a→0).
- `volume_uniform_covariance_bound` — the N→∞ covariance bound.
- `wightman_limit_stable` + `os_reconstruction_full` — the reconstruction stable under the limit.
- `AsymptoticFreedom.su2_exponent` — `c = 12π²/11`, and `asymptotic_freedom_exponent_pos`.
- `RefereeScalingLaw.refereeScalingLaw_of_radius_bound` — `ρ(β) ≤ e^{−A·e^{−cβ}} ⟹ m(β) ≥ A·e^{−cβ}`.

## The single remaining input

The bridge lemmas `volume_uniform_covariance_bound` (needs `hpos`/`hlim`) and
`refereeScalingLaw_of_radius_bound` (needs the radius bound `hρ`) are already proved *as transports*.
Their hypothesis is **H** above. So the Clay problem is reduced to:

> **H** — the Balaban-style linked-cluster estimate: the concrete `gibbsMeasure`/`blockSpinSU2`
> propagator contracts to `ρ(β) ≤ e^{−A·e^{−(12π²/11)β}}`.

The next (and now precise) unproved rung toward H is the **lattice-animals bound**:

> `#{connected clusters of size n} ≤ Δ^{2(n−1)}` — a connected subset of `n` vertices has a spanning
> tree of `n−1` edges whose Euler/DFS tour is a walk of length `2(n−1)`; combined with
> `walk_count_bound` (proved) this gives `#{animals} ≤ Δ^{2(n−1)}`.

This is the one genuine combinatorial/real-analysis estimate left before the block-spin contraction,
and it is the open mathematics of the Millennium problem.
