# The mass gap — the complete mathematical accounting (2026-11-25)

This is the reconciliation Rob asked for: not two reductions, not five, but the **whole accumulation**
collapsed into one dependency graph with three states and one root obligation.

## The true inventory

| surface | count |
|---|---|
| Lean theorems in the tower (total) | **487** |
| mass-gap / reduction / bound theorems among them | **~60** |
| SEXTANT `ym-*` claims | **20** |
| mass-gap planning/consolidation docs | **13** |

Every one of the ~60 theorems and 20 claims is an *entry point into the same target*. The honest
question is not "which reduction is right" — it is "which of these are the same obligation, and what
is actually left."

## The three states

1. **proved-lemma** (tier 1–3) — a single statement or a chain with a machine-checked proof, no open
   input. Examples: `fss_join`, `fss_reflection_positivity_square`, `posdef_*`, `casimir_infrared_bound`,
   `ir_bound_su2`, `gradientFlow_contraction_rate`, `rg_contraction_positive`, `stringTension_eq_casimir`,
   the whole single-cluster cluster-expansion layer, `walk_count_bound`.

2. **proved-transport** (tier 4) — an `if X then mass gap` theorem whose *implication* is checked and
   whose *hypothesis X* is the open bit. These are the "reductions" — and there are ~20 of them, each
   with a different X:
   - `mass_gap_from_hypotheses` (X = a bundle of hypotheses)
   - `mass_gap_from_mixing` (X = spectral mixing)
   - `mass_gap_from_volume_independent_tension` (X = volume-independent string tension)
   - `mass_gap_iff_positive_ratio` (X = a positive ratio)
   - `mass_gap_of_radius_bound` / `mass_gap_of_radius_exponential` (X = the radius bound ρ ≤ e^{−A·e^{−cβ}})
   - `mass_gap_join` / `mass_gap_join_strong` (X = the joined bound)
   - `mass_gap_reduction` / `mass_gap_reduction_volumeUniform` (X = volume-uniformity)
   - `mass_gap_bounds_string_tension` / `string_tension_iff_gap` (X = the tension)
   - `mass_gap_dimensional_transmutation` / `mass_gap_follows_beta_not_instanton` (X = the running-coupling route)
   - `clustering_iff_gap` / `clustering_implies_cluster_expansion` (X = clustering)
   - `infrared_bound_gives_volume_uniform` (X = the infrared bound)
   - `refereeScalingLaw_of_radius_bound` (X = the radius bound, the transport to `m ≥ A·e^{−cβ}`)

3. **open-obligation** (tier 5's missing rung) — the X's themselves, plus the SEXTANT claims that carry
   them: `ym-linked-cluster-contraction`, `ym-fss-nonabelian-closable`, `ym-volume-uniform-su2`,
   `ym-rg-contraction`, `ym-log-sobolev`, `ym-finite-truncation-posdef`, `ym-posdef-limit`, `ym-os-existence`.

## The collapse — how many distinct obligations actually remain?

The ~20 "open X's" are **not 20 independent problems**. They form chains of implication, several of
which are already proved, and the reconciliation's job is to close those chains into a small set of
roots. The shared core every open X points at:

> **The SU(2) two-point function (of the trace observable) is dominated by the free propagator,
> uniformly in the volume and in the decimation scale** — the single statement that makes the finite
> Casimir gap `2` survive the thermodynamic and continuum limits with the running-coupling exponent
> `c = 12π²/11`.

Under that core sit the named rungs, which are the *concrete* obligations:

| obligation | current first rung | state |
|---|---|---|
| the block-spin contraction `ρ(β) ≤ e^{−A·e^{−cβ}}` | the lattice-animals bound `#{connected clusters of size n} ≤ Δ^{2(n−1)}` (on top of `walk_count_bound`, proved) | open |
| the volume-uniform FSS for the SU(2) character | the FSS non-Abelian estimate (the linear/Abelian version is proved: `fss_join`, `falk_bruch`) | open |
| the log-Sobolev / mixing gap | the mixing estimate | open |

**To be established by the reconciliation (not assumed):** whether the three named rungs are
*equivalent* or genuinely distinct. The block-spin contraction and the volume-uniform FSS are almost
certainly the same fact in two frameworks (RG vs thermodynamic); proving that equivalence is itself a
reconciliation step, and it would reduce the open set from three to (likely) one.

## What this means for SEXTANT

The accounting is the single source of truth the other three priorities need:

- **the infrastructure** stores this graph as one node-schema (tier + state + proof + falsifier + tasks);
- **the engine** loops on the "open-obligation" nodes — propose an approach, the falsifier + kernel
  decide, the state updates;
- **the interface** renders the three states live, so a visitor sees the ~20 transports converging on
  the one root, and the root's remaining rungs.

The next step is to make this machine-readable and *verify the equivalence-collapse* against the tower,
rather than asserting it.
