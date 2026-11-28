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

These are the foundations + the exponential-envelope assembly. The DEEP open core remains: the small/large-field
region decomposition of the SU(2) measure, the a→0 convergence of the FULL gauge-invariant Schwinger functions
(not just the mass-gap envelope), and the OS→Wightman reconstruction on ℝ⁴ (beyond the finite-lattice
`os_reconstruction_actual`).

## The next real step (the open Clay half)

The mass-gap side is now complete: lattice gap (sharp `A = 1/2`), gap-survival `Δ_phys > 0`, and the
sharp cutoff-independence `β·gap → 1/4`. The remaining Clay work is the **continuum existence on ℝ⁴**:
the `a → 0` correlation-function limit (small/large-field region decomposition / Balaban RG, a→0 with
asymptotic freedom, OS→Wightman reconstruction).
