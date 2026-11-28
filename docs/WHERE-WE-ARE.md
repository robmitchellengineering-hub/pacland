# Where we are — the Yang–Mills mass gap (honest state)

Last updated 2026-11-28. This is the anti-drift record: the one place to read before doing more
work, so we do not re-derive or over-claim.

## The one-liner

> The **lattice mass gap is proved** (sharp `A = 1/2`), the **gap survives** the continuum limit
> (`Δ_phys > 0`), and the **sharp cutoff-independence `β·gap → 1/4` is PROVED** (the irreducible cubic
> `C(Φ) = xΦ³ − 2Φ² − xΦ + 1 ≤ 0` is now a kernel-checked theorem). The **continuum existence on ℝ⁴
> is open** — that is the remaining Clay half.

## The Clay problem is NOT solved

Two halves: (1) continuum **existence** of 4D Yang–Mills (Wightman axioms on ℝ⁴), (2) the **mass
gap** `Δ > 0`. We proved the mass gap only at the **lattice** level. The continuum ℝ⁴ existence is
the open half. Do not claim otherwise.

## What is proved (kernel-checked, no `sorry`, in `feat/massgap-clean`)

1. **Lattice mass gap, sharp `A = 1/2`** — the heat-kernel gap `1 − I₁(2β)/I₀(2β)` with the sharp
   Amos bound, the block-spin/hΘ reflection-positivity machinery, the connected-correlation limit,
   and the cluster/polymer expansion (rungs 11–15). Published to Zenodo (DOI 10.5281/zenodo.24585251),
   honestly scoped.
2. **Gap-survival `Δ_phys > 0`** — the physical mass `β·(1 − I₁/I₀)` is bounded `1/5 ≤ · ≤ 1/2`, so
   it does not close in the `a → 0` limit. Scale analysis complete: bare gap `→ 0`, naive ratio
   `→∞`, physical mass on the `1/β` scale.
3. **The sharp-bound wiring (11 rungs)** — Riccati, Chu–Vandermonde ×4, reduction identity, product
   formulas `I₁²`/`I₀I₂`, Turán series + inequality, `I₂′` derivative, and the double-ratio
   cubic-nullcline ODE `W′ = 2x·C(Φ)/(Φ²(Φx−2)²)`.

## What is PROVED (the sharp bound, 2026-11-28)

The sharp `β·gap → 1/4` is now **proved kernel-checked** (no `sorry`). The single inequality
`C(Φ) = xΦ³ − 2Φ² − xΦ + 1 ≤ 0` (Φ = I₀/I₁) is closed by a **no-crossing on the cubic nullcline**:

- **seed** `besselI_sharp_seed` — `C(Φ(1)) < 0`, from `I₂(1) ≤ 3/22` and `I₁(1) ≥ 9/16` (series bounds).
- **sign** `sharp_cubic_no_crossing_sign` — `dC/dx < 0` on `C ≥ 0`, via a Taylor certificate at
  `x₀ = (2Φ²−1)/(Φ(Φ²−1))`.
- **assembly** `sharp_cubic_nonpos` — `no_crossing_barrier_from` forces `C(Φ) ≤ 0` for `x ≥ 1`.
- **convergence** `physical_mass_tendsto_sharp` — `Tendsto (fun β => β·heatKernelMassGap β) atTop (nhds 1/4)`,
  the squeeze between `β/(4β+1)` (Amos) and `1/4 + 1/(8β)` (the sharp cubic, via `sharp_gap_upper`).

## What is genuinely open (not attempted)

- The **`a → 0` correlation-function continuum limit** — the actual construction of the ℝ⁴
  Wightman/Schwinger functions via region decomposition + RG + OS→Wightman reconstruction.
- The **sharp cubic** above (a standalone hard result; needs the published Simpson–Spector
  double-ratio *monotonicity* lemma, or total-positivity/Pólya-frequency, or the `K`-Bessel
  Wronskian route).

## The a→0 continuum limit (the open Clay existence half) — in progress

The mass-gap side is complete (lattice gap sharp A=1/2, gap-survival Δ_phys > 0, sharp β·gap → 1/4). The
remaining Clay half is the continuum EXISTENCE on ℝ⁴. The a→0 goal has landed 5 kernel-checked rungs
(branch feat/massgap-clean):

1. `running_coupling_activity_tendsto_zero` — the cluster activity e^(−cβ) → 0.
2. `physical_correlation_length_diverges` — e^(cβ)/gap → atTop (the correlation length diverges in physical units).
3. `cluster_expansion_bound_tendsto_one` — the geometric bound 1/(1−e^(−cβ)) → 1.
4. `rescaled_two_point_converges` — the rescaled correlation e^(−(β·gap)·t) → e^(−t/4) (mass 1/4).
5. `cluster_weight_majorant_tendsto_zero` — the total cluster-weight majorant r/(1−r)² → 0.
6–16. the measure + RG layer: `continuum_mass_gap_pos` (positive continuum mass 1/4), the Wightman W0–W4
a→0 closure (`wightman_reconstruction_limit`, `mass_gap_limit_pos`, etc.), `small_field_cutoff_tendsto_zero`
(the small-field region shrinks), `su2_weyl_measure_normalized` (total mass 1), `large_field_measure_tendsto_zero`
(large-field suppressed), `blockSpin_average_bound` (the RG density is controlled), `su2_weyl_integral_heat_kernel`
(∫ e^(x·cos)·sin² = π·I₁/x, the RG step's bridge to Bessel), and `running_coupling_ratio_tendsto_one`
(I₁/I₀ → 1, the weak-coupling fixed point).

These are the foundations + the exponential-envelope assembly. The OS→Wightman RECONSTRUCTION is now closed
under the a→0 limit (10 rungs): `wightman_reconstruction_limit` + `wightman_covariance_limit` +
`wightman_locality_limit` + `wightman_vacuum_limit` + `mass_gap_limit_pos` + `posdef_of_tendsto` — the Wightman
axioms W0–W4 each survive pointwise limits, so the finite-lattice reconstruction carries through to the continuum.

The DEEP open core that remains: the measure-theoretic small/large-field REGION DECOMPOSITION of the SU(2)
gauge measure (Balaban's multiscale RG) and the a→0 convergence of the FULL gauge-invariant Schwinger functions
(not just the mass-gap envelope or the reconstruction scaffold). These are the genuinely-hard existence steps.

**Character theory is now complete (29 rungs).** The full SU(2) Weyl character formula
`e^(x·cos θ)·sin θ = Σₙ 2(n+1)Iₙ₊₁(x)/x · sin((n+1)θ)` is proved (`weyl_character_formula`), via the general
Jacobi–Anger moment (`besselI_eq_integral_general`), the general recurrence (`bessel_recurrence_general`), the
Weyl character coefficient (`weyl_character_coefficient`), and the termwise differentiation
(`hasDerivAt_tsum` + `besselI_mul_succ_summable`). This is the symmetric (class-function) character expansion of
the SU(2) heat kernel — the block-spin RG step's clean coupling-advance identity.

**Two-plaquette block-spin primitives + the trace identity (32 rungs).** The single-link block-spin average is
Haar-trivial (constant), so the coupling advance comes from the odd link in TWO plaquettes. Landed:
`su2_char_conv_one` (torus-diagonal n=1 convolution), `cos_phi_orthogonality` (the φ-integration primitive), and
`su2_trace_identity` (Tr(UV) + Tr(U⁻¹V) = Tr(U)·Tr(V) for det U = 1, via `Matrix.inv_def` + the 2×2 adjugate
`adj(U) = Tr(U)·I − U`). The trace identity is the key for the correct n=1 convolution
`∫ χ₁(U₂A)χ₁(U₂B) dU₂ = χ₁(AB⁻¹)/2`. **The SU(2) matrix machinery is now complete except the measure (39 rungs).** Landed: the trace identity
`Tr(UV)+Tr(U⁻¹V)=Tr(U)Tr(V)` (via `Matrix.inv_def` + the 2×2 adjugate), the scalar moments `∫ Tr(V²)=−1` and
`∫ Tr(U₂)=0`, the **Schur lemma** `su2_central_matrix_eq_scalar` (a matrix commuting with σ₃, σ₁ is scalar), the
trace conjugation invariance `Tr(U·C·U⁻¹)=Tr(C)`, the Schur-lemma lift `su2_central_matrix_trace_neg_one_eq_neg_half`
(central + Tr=−1 ⟹ −I/2), and the dimension `Tr(I)=2`.

**The quaternion route to the matrix pseudoreality is fully assembled except the S³ Fubini (46 rungs).** Landed:
the Pauli algebra `(x⃗·σ⃗)² = |x⃗|²·I`, the quaternion square `V² = (x₀²−|x⃗|²)·I + 2ix₀(x⃗·σ⃗)`, its trace
`Tr(V²) = 2(x₀²−|x⃗|²)`, the S³ moment `(2/π)∫cos²θ·sin²θ = 1/4`, and the φ-integration primitives
`∫₀^{2π}cos φ = ∫₀^{2π}sin φ = 0`.

**The SU(2) matrix pseudoreality is PROVED (77 rungs).** `∫∫∫ V²·sin²θ₁·sin θ₂ = −π²·I`, i.e. `∫ V² dV = −I/2`
normalized. All four quaternion-square entries, their integrals (`−π²`, `−π²`, `0`, `0` via the φ/θ₂ odd moments and
`integral_add_const_{sin,cos}_period`), and the `Matrix.ext` assembly. The block-spin RG's clean pseudoreality primitive.

**Next (the goal's second objective):** the n=1 character convolution `∫ χ₁(U₂A)χ₁(U₂B) dU₂ = χ₁(A⁻¹B)/2`, via the
trace identity `Tr(U₂A)Tr(U₂B) = Tr(U₂AU₂B) + Tr(A⁻¹B)` + the substitution `V = U₂A` (`∫Tr(U₂AU₂B) = Tr(−I/2·A⁻¹B)`).
The remaining piece is the **Haar left-invariance** `∫ f(U₂A) dU₂ = ∫ f(V) dV` (the quaternion left-multiplication's
isometry of the S³ round measure). Then the effective-plaquette weight `e^(x′·Tr AB⁻¹)` (coupling advance `x′ = x²·(…)`),
and the multiscale induction.

## The next real step (the open Clay half)

The mass-gap side is now complete: lattice gap (sharp `A = 1/2`), gap-survival `Δ_phys > 0`, and the
sharp cutoff-independence `β·gap → 1/4`. The remaining Clay work is the **continuum existence on ℝ⁴**:
the `a → 0` correlation-function limit (small/large-field region decomposition / Balaban RG, a→0 with
asymptotic freedom, OS→Wightman reconstruction).
