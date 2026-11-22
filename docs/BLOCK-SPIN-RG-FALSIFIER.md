# Spec — the block-spin RG falsifier (`ym-rg-contraction`)

Status: spec, not yet built. This is the missing falsifier for the RG-contraction claim in
`docs/RG-DISCOVERY-PLAN.md`. Written down so the build is a job, not a decision to re-derive.

## What it must test

The claim: *one block-spin RG step contracts the Yang–Mills measure (positive contraction
coefficient), so the mass gap is the RG contraction rate.*

The falsifier: *the contraction coefficient → 1 (no contraction) — or the flow lands on the trivial
Gaussian fixed point — which would refute the claim.*

## The blocking transformation (what "one RG step" means on the lattice)

1. On a lattice of size `N`, partition into blocks of `2^d` sites (so `N → N/2`, spacing `a → 2a`).
2. The **block link** `Ū_μ` between two blocks is the projected average of the fine links
   connecting the block faces — the standard choices are:
   - the **projected sum** of the `2^(d-1)` straight 2-link paths across the face, projected back to
     SU(2) (`_proj` = normalise the quaternion), or
   - a **Villasenor/APE-weighted** sum with the staples (reuses the existing `ape_smear`), then
     projected.
3. This is a *deterministic* map `U → Ū` — no Monte-Carlo at the blocking step itself.

## The contraction coefficient (the observable)

Measure the RG-invariant mass in **lattice units** before and after one block:

- before: `m` (Polyakov screening mass, or `√σ` from the string tension) at spacing `a`;
- after: `m̄` at spacing `2a`.

Correct RG behaviour for a **gapped** theory: the physical mass is fixed, so in lattice units
`m̄ = m/2` (and `σ̄ = σ/4`). The **contraction coefficient** is the ratio of the correlation length
in lattice units:

```
ρ = ξ̄ / ξ = (m / m̄)  ∈ [1, 2]
```

- `ρ → 2` = the expected gapped behaviour (the mass halves under a doubling of the spacing).
- `ρ → 1` = **no contraction** — the correlation length does not shrink under blocking → the claim
  is refuted (this is the falsifier's trigger).

## The verdict contract (same shape as the other falsifiers)

`verify_rg_contraction(beta, N)` returns `(survived, evidence)`:

- `survived = True` when `ρ` is measurably > 1 (contraction present, and it survives two N values);
- `survived = False` when `ρ ≈ 1` within tolerance (no contraction) — the honest refutation;
- `survived = False` with `unresolved` in the message when the mass is noise-dominated at the
  available N/configs (a demonstration, not a measurement).

## What blocks the build right now (named, not hidden)

1. The **block-link projection** is the one genuinely new piece — the rest (Polyakov mass, string
   tension, `ape_smear`) already exists.
2. The **mass extraction** at `N/2` needs enough statistics, or `m̄` is noise — the same
   Polyakov-correlator noise caveat as Phase 2.
3. Whether `ρ` is stable across β (does the contraction *persist* toward the continuum?) is the
   second half — it needs two β values, like the other falsifiers.

## Acceptance (done = verified)

The falsifier is built when a mutation of the block-link projection to the identity (no blocking)
returns `ρ ≈ 1` and `survived = False`, while the real projection returns `ρ > 1` and
`survived = True` at the same β, N. That single mutation proves the falsifier can actually see the
difference between "contracts" and "doesn't".
