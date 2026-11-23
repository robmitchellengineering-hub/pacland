# Plan — renormalized continuum near-zero FP density at the GZ horizon

Status: proposed 2026-11-21, after the finite-N probe concluded the ~2.4 FP gap is the UV cutoff,
not the horizon. This is the computation that actually reaches the Gribov–Zwanziger condition.

## The target, in one line

Measure the Landau-gauge (adjoint) Faddeev–Popov operator's eigenvalue density near zero, in
**physical** units, and test the GZ prediction `ρ(λ_phys) ~ λ_phys^(-1/2)` as the lattice spacing
`a → 0`.

## The physics (why this, not more eigenvalue runs)

- `M = -∇·D` (adjoint rep, Landau gauge) is positive-definite inside the first Gribov region Ω.
- The **horizon ∂Ω** is where its lowest eigenvalue `λ₁ → 0`.
- GZ: near ∂Ω the density of eigenvalues diverges as `ρ(λ) ~ λ^(-1/2)` (the IR ghost enhancement,
  `G(p) ~ 1/p⁴`).
- The finite-N probe we already ran measures `λ_min ≈ 2.4` in **lattice** units = `λ/a²`, which
  diverges as `a → 0` — the UV cutoff. The horizon is invisible at fixed β, fixed N; it is an IR,
  continuum property.

## The three hard parts (and why each is hard)

1. **Gauge fixing + FMR.** Landau gauge (local minimisation) lands in the *first* Gribov region, not
   the *fundamental modular region*. The horizon is at the FMR boundary (the global minimum of the
   gauge-fixing functional). This needs a Gribov-copy search: several random gauge transforms, keep
   the lowest functional, so we sit near the FMR, not at an arbitrary copy.
2. **Renormalisation.** `λ_phys = λ/a²`, and `a(β)` must be measured (string tension `√σ`, or the
   Wilson-flow scale `t₀`). Without a physical scale the -1/2 power is a lattice-unit artefact.
3. **Continuum limit.** Several `β` at fixed **physical** volume, then extrapolate `a → 0`. The
   singularity only emerges in the limit; a single β cannot show it.

## Phases (each with a checkpoint that can pass or fail honestly)

- **Phase 0 — raw horizon signal.** Landau-gauge-fix at fixed β; FP spectrum; near-zero density.
  Checkpoint: does `λ_min → 0` under proper gauge fixing (vs the unfixed gap ~2.4)? *Falsifies the
  whole route if no.*
- **Phase 1 — FMR restriction.** Gribov-copy search (k random transforms, lowest functional wins);
  re-measure. Checkpoint: does the near-zero density sharpen toward the boundary?
- **Phase 2 — renormalisation.** Measure `a(β)` via string tension / Wilson flow. Checkpoint:
  stable scale in the continuum window.
- **Phase 3 — continuum.** `β = 2.2 … 2.6` (SU(2)) at fixed physical volume; extrapolate.
  Checkpoint: does the exponent converge?
- **Phase 4 — the verdict.** Fit `ρ_phys(λ_phys) ~ C λ_phys^(-1/2)` near zero. Confirm (exponent
  → -1/2), or refute (a gap / a different exponent — an honest negative result).

## Compute and where

- **SU(2) first** (we already have `lattice_ym_su2.py` + `lattice_ghost.py`); SU(3) after, using the
  existing `ape_smear` + string-tension code.
- Gauge fixing + FP spectrum is CPU-bound and embarrassingly parallel → `pacland-rog` (8c/31 GB) and
  `win-2` (16c), never the Mac. Rental only if we push N/β far past the mesh.
- Rough scale: Phase 0 ≈ 1 day · Phases 1–2 ≈ 1 week · Phase 3 ≈ 1–2 weeks. This is a real
  lattice-QCD project, not a session-sized task.

## First step (this session)

Phase 0, minimal: `landau_gauge_fix` + `fp_spectrum` at `β = 2.5`, `N = 8…16`, ~50 configs,
dispatch to `pacland-rog`; report the near-zero density vs the unfixed `λ_min ≈ 2.4`.
