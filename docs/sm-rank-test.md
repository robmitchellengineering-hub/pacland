# The rank test — the SM "floor" question, computed as an exact Jacobian rank

The floor question (`docs/sm-floor-notes.md`) asks: is the SM's **19 free parameters** a
*real* floor (irreducible), or *dynamically reducible* — does some symmetry force them to
be functions of fewer than 19 inputs, the way the flux sector collapses everything to the
single tadpole?

This note records the rank test: the question stated as an **exact Jacobian-rank
computation** (`scripts/validate_sm_rank_test.py`, rational arithmetic, zero floating
point), and the honest split it exposes.

## Two readings, separated (the fan-out's meta-lesson, applied)

"Rank" hides two different questions:

- **Tier 1 — kinematic rank.** The rank of the SM's *own* flavor/reparametrization group
  action on the raw Yukawa matrices. This asks: does the SM's own symmetry collapse the
  19? **Answer below: no — rank = 19.**
- **Tier 2 — dynamical rank.** In a concrete string compactification with ≥ 19 moduli, the
  Jacobian of the map *moduli → the 19 parameter values*. This asks: does the *geometry*
  force the 19 to be functions of fewer geometric inputs, the way the flux geometry
  (Sp duality + Weyl's FFT) collapses 2·b₃ → 1? **This is the decisive "floor" test, and it
  is NOT settled by this script** — it needs a ≥19-moduli geometry (the bigger machine).

## Tier 1 — the exact result

### Control: the flux sector collapses to rank 1

The map `(F,H) → (N, N²)` where `N = FᵀJH` is the tadpole has Jacobian rank **1** (the
gradient of `N²` is `2N·∇N`, collinear with `∇N`). Twelve flux integers in, one invariant
out — the constraint-first collapse, reproduced as a Jacobian rank. This is the positive
control proving the rank-test instrument detects a collapse when one exists.

### The SM's own flavor symmetry does *not* collapse

| sector | group | orbit rank (exact) | orbit-space dim | physical content |
|---|---|---|---|---|
| quark | U(3)_QL × U(3)_uR × U(3)_dR (dim 27) | **26** | 36 − 26 = **10** | 6 masses + 4 CKM |
| lepton | U(3)_LL × U(3)_eR (dim 18) | **15** | 18 − 15 = **3** | 3 charged-lepton masses |
| gauge / Higgs / θ | — | — | 3 + 2 + 1 | — |
| **total** | | | **19** | |

The stabilizers come out exactly as the literature says — quark `U(1)_B` (dim 1), lepton
`U(1)³` (dim 3) — which is an independent consistency check on the computation.

**Conclusion (Tier 1):** within the SM, the 19 parameters are the *terminal* invariants of
the flavor group — the orbit space is exactly 19-dimensional. The SM's own symmetry does
**not** collapse them below 19 (unlike flux, whose own symmetry collapses 2·b₃ → 1).

## Rule of Three — three independent confirmations

1. **Jacobian rank** (this script): quark 26 → 10, lepton 15 → 3, total 19.
2. **Orbit-dimension formula** (`scripts/validate_sm_invariant_ring.py`): `36 − 27 + 1 =
   10`, `18 − 18 + 3 = 3`, total 19.
3. **Literature** (Bento–Silva–Trautner, JHEP 2024, Hilbert series + plethystic
   logarithm): the flavor-group orbit space is exactly the 19 physical parameters.

All three agree on 19. The kinematic floor is settled: **19, no collapse from the SM's own
symmetry.**

## What is still open — Tier 2, the decisive test

The flux lesson is *dynamical*: a clean duality group (Sp) plus a known invariant theory
(FFT) collapses the *geometry's* inputs to one invariant. The SM's couplings have **no such
group action**, which is exactly why the analogous collapse is not automatic. The decisive
test is therefore:

> In a flux compactification with **≥ 19 moduli**, write the 19 invariants as functions of
> the moduli and compute the Jacobian rank. Rank = 19 means the geometry can dial all 19
> independently (the floor is real in that class); rank < 19 means the geometry forces
> relations (the floor is dynamically reducible).

This requires (a) a concrete model in which the SM structure is realized geometrically
(Yukawas from period integrals / wavefunction overlaps, gauge couplings from cycle
volumes), and (b) ≥ 19 moduli, so the result is not the trivial "too few moduli" bound.
Both point at the bigger-machine chase (`h12 = 272`, the full-model JAXVacua build), which
is the speed problem documented in `AGENTS.md` — memory is solved, sampling speed is not.

## Status

- **Tier 1 (kinematic): done, exact, three ways.** The SM's own symmetry leaves 19 free;
  it does not collapse them. Flux's own symmetry leaves 1. The asymmetry is now a *measured
  Jacobian rank*, not a slogan.
- **Tier 2 (dynamical): open.** The decisive "does the geometry collapse the 19" test needs
  the ≥19-moduli bigger machine and a concrete geometric SM — the next compute target after
  the speed chase lands.
