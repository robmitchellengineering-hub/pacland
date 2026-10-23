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

## Tier 2 — the dynamical rank: the dimension bound (done) and the symmetry question (open)

The dynamical rank has two parts, and they split cleanly:

### 2a. The dimension bound (exact, done)

In a concrete compactification the 19 parameters are functions of the moduli: gauge
couplings of the dilaton + Kähler moduli (`2·h¹¹` real), masses + CKM of the holomorphic
Yukawas of the complex-structure moduli (`2·h²¹` real), θ_QCD of one axion (already in the
dilaton/Kähler imaginary part), and the Higgs terms of **discrete** flux (no continuous
moduli dependence). Hence

> **rank(moduli → 19 params) ≤ 2·h¹¹ + 2·h²¹ + 2**, so the 19 is dynamically reducible
> (rank < 19) **iff `h¹¹ + h²¹ ≤ 8`**, and only generically a real floor (rank = 19) for
> `h¹¹ + h²¹ ≥ 9`.

| h¹¹ | h²¹ | bound | verdict |
|---|---|---|---|
| 2 | 2 (the repo's truncated h12=2) | 10 | reducible |
| 3 | 3 (T⁶ diagonal) | 14 | reducible |
| 4 | 4 | 18 | reducible |
| 4 | 5 | 20 | rank 19 possible |
| 2 | 272 (full model) | 550 | rank 19 possible |
| 1 | 101 (quintic) | 206 | rank 19 possible |

This is a pure dimension count — exact, no model ambiguity — and it answers the "small
h¹¹+h²¹" case the floor question asked about: **in any compactification with fewer than 9
total Kähler+CS moduli, the 19 cannot be independently realized; the floor is reducible.**
The repo's own measurements (h12=2, `h¹¹+h²¹=4`) sit far below the threshold, which is why
they see the parameter space as "collapsed" — they are inside the reducible regime.

### 2b. The symmetry question — known GUTs collapse 5 (SU(5)) or 12 (SO(10)) of the 19, never 19

The flux lesson is *not* the dimension bound — it is that a **symmetry** (Sp duality + FFT)
collapses 2·b₃ inputs to 1, *far below* the dimension bound. The analogous question for the
SM is whether a UV symmetry forces a similar collapse. The **only** known candidate — GUT
unification — is computed here as an exact Jacobian rank:

| relation | SM rank | GUT rank | drop |
|---|---|---|---|
| gauge: `(g_GUT) → (g_Y, g_2, g_3)` | 3 | **1** | 2 |
| `Y_e = Y_dᵀ`: `m_e=m_d, m_μ=m_s, m_τ=m_b` | 6 | **3** | 3 |
| **total** (minimal SU(5)) | | | **5** |

Minimal SU(5) collapses exactly **5 of the 19** (gauge unification 3→1 = 2, plus
`Y_e = Y_dᵀ` = 3 mass relations), and single-Higgs SO(10)/E₆/Pati–Salam/trinification
collapse **12** (`Y_u=Y_d=Y_e`, `V_CKM=1`) — but those exact mass relations are
*numerically wrong* against data, so only gauge unification (2) survives. The GUT Higgs
sector grows ~2 back — a *shuffle*, not a collapse. There is **no known symmetry that
collapses all 19**: the flux-style total collapse (`2·b₃ → 1`) needs a duality group +
FFT, which the SM's couplings simply do not have. Even the up-to-12 relations are
*relations*, never a value, so no completion reaches a single number.
⚠️ corrected 2026-10-23 (falsifier #2): see docs/falsification-status.md

## Status

- **Tier 1 (kinematic): done, exact, three ways.** The SM's own symmetry leaves 19 free;
  it does not collapse them. Flux's own symmetry leaves 1. The asymmetry is now a *measured
  Jacobian rank*, not a slogan.
- **Tier 2a (dynamical dimension bound): done, exact.** Rank ≤ 2·h¹¹ + 2·h²¹ + 2; the 19 is
  reducible for `h¹¹+h²¹ ≤ 8`, generically real only for `h¹¹+h²¹ ≥ 9`.
- **Tier 2b (symmetry collapse): done for the known case.** Minimal SU(5) collapses 5 of the
  19, SO(10)/E₆/Pati–Salam/trinification 12 — never all 19, and only gauge unification (2)
  survives data. No flux-style total collapse exists for the SM, because it has no duality
  group + FFT.

## The answer

The "19 floor" is **real**: it is reducible only by the trivial dimension bound (small
`h¹¹+h²¹ ≤ 8`) or by *partial* symmetry relations (SU(5): 5 of 19; SO(10)/E₆/PS: 12 —
only gauge unification (2) survives data), never by a total symmetry collapse. The flux sector collapses to 1 because it *has* a duality group; the SM
does not — that asymmetry is the whole of the constraint-first result, now measured as
Jacobian ranks on both sides.
