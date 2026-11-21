# Plan — RG-discovery for the Yang–Mills mass gap (SEXTANT cross-field search)

Status: proposed 2026-11-21, from Rob's direction. This is the *strategic* thread that supersedes
the direct lattice horizon probe as the thing to invest in.

## The question

How does Yang–Mills change as we move through scales — and is there a **gauge-invariant** formulation
that keeps a **positive curvature estimate** (quantitative decay + a spectral gap) all the way to the
continuum?

## The obstruction (why the naive route fails — state it, don't assume it away)

The standard machinery that gives a spectral gap (Bakry–Émery curvature-dimension, Lichnerowicz,
log-Sobolev, Poincaré) needs a **strictly log-concave** measure. The Yang–Mills measure
`μ(A) ∝ e^{-S(A)}` is **gauge-invariant**, so:

1. it has **flat directions** (the gauge orbits — the Hessian of S is degenerate along them),
2. the **Faddeev–Popov operator** (the metric on the orbit space) develops **zero modes at the Gribov
   horizon**, so the curvature vanishes there,
3. the **continuum limit** concentrates the measure on non-smooth fields, so any estimate must survive
   the UV singular structure.

So "positive curvature" for YM is *not* a starting assumption — it is the thing to **discover or
refute**. The OU/Gaussian results are the seed, not the answer.

## The cross-field search (what SEXTANT proposes)

For each candidate, SEXTANT: propose a **transferable structure** → **prove the transfer** (why it
applies to a gauge-invariant YM formulation) → **test it against a genuine obstruction** → record the
verdict.

| field | transferable structure | the obstruction it must survive |
|---|---|---|
| differential geometry | orbifold / Bakry–Émery curvature on the gauge-orbit quotient | FP operator `λ_min → 0` at the horizon |
| functional inequalities | log-Sobolev on the Landau/FMR gauge slice | log-Sobolev constant `→ 0` at the horizon |
| renormalisation | block-spin RG contraction toward a fixed point | contraction rate `→ 0`, or trivial fixed point |
| statistical mechanics | cluster expansion / correlation decay | fails in the weak-coupling (continuum) regime |
| operator theory | spectral gap of the gauge-fixed Hamiltonian | ground-state degeneracy / zero modes |

## What we already measured — it is the falsifier, not the answer

The FP spectrum we ran is exactly the **first candidate's obstruction**: `λ_min ≈ 2.4` (flat in N) is
the unfixed covariant-Laplacian gap. The GZ horizon is the boundary where `λ_min → 0` — i.e. where the
**orbifold curvature vanishes**. So the horizon plan and this RG plan are the *same* question from two
sides: the horizon is the place the positive-curvature estimate must not die.

## SEXTANT claims to file first (propose → falsify → record)

1. `ym-orbifold-curvature` — the YM measure on the gauge-orbit quotient has Bakry–Émery curvature
   `K ≥ λ_min(FP)`, so a spectral gap iff `λ_min > 0` uniformly. **Falsifier:** `λ_min → 0` in the
   continuum (the horizon) → refutes positive curvature, confirming GZ.
2. `ym-log-sobolev` — the gauge-fixed (FMR) measure satisfies log-Sobolev with constant `C ~ 1/λ_min`.
   **Falsifier:** the log-Sobolev constant blowing up as `λ_min → 0`.
3. `ym-rg-contraction` — one block-spin RG step contracts the measure. **Falsifier:** the contraction
   coefficient `→ 1` at the horizon / in the continuum.

## First concrete step

File the three claims above into SEXTANT's catalog, wire the FP spectrum (`lattice_ghost.py`) as the
falsifier for #1/#2, and run the discovery loop on `ym-orbifold-curvature` first — it is the claim our
existing measurement can already test, so it is the cheapest falsification with real content.
