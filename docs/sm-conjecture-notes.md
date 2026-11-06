# Compare-notes: the SM "unpredicable" conjecture — first fan-out

Five independent agents attacked the same claim from five angles. The spread is the
result — and it refines the conjecture in a way a single angle would have missed.

## The claim under test

> The SM's ~19 free parameters are "unpredicable in any UV completion" — no
> theory-of-everything can derive them, because there is no invariant for them to be a
> function of.

## The raw spread

| angle | verdict | confidence |
|---|---|---|
| GUT unification | **falsifies** | high |
| String constructions | **falsifies** | high |
| Invariant-theory analog | **unknown** | medium |
| Swampland constraints | confirms | high |
| Cosmological constant (Λ) | confirms | high |

Two falsify, two confirm, one is genuinely unresolved. That asymmetry is the finding.

## The pivot: "unpredicable" has two readings

The two `falsifies` and the two `confirms` are not contradicting each other — they are
answering two different questions that one word was hiding:

1. **"No invariant relates them."** *Falsified.* GUTs relate the parameters: the three
   gauge couplings are one running coupling plus a group-theory normalization
   (predicting sin²θ_W = 3/8 at the GUT scale), and bottom–tau unification relates two
   masses. String constructions go further: Yukawa couplings are computed from geometry
   (intersection numbers, wavefunction overlaps), gauge couplings from moduli volumes.
   The invariant ring is **smaller** than 19 in a UV completion.

2. **"No unique absolute value is derived."** *Survives.* Every relation reduces the
   parameter *count*, but the residual freedom — α_GUT, the dilaton/Kähler moduli VEVs,
   the open-string moduli — is itself unpinned. Nothing derives an absolute value; the
   parameters become functions of a *smaller set of free inputs*, not functions of
   nothing. And the only thing any UV completion actually **fixes** is the constraint
   (the tadpole, the anomaly).

The swampland and Λ angles confirm reading 2: the swampland gives only
order-of-magnitude postdictions (no sharp value), and Λ is the cleanest case — a
parameter unprotected by any constraint or label, explained statistically (anthropic /
landscape), never computed.

The invariant-theory angle is the most interesting: the SM *does* have an FFT-style
result — the flavor/reparametrization group SU(3)⁵ acts on the Yukawa matrices, and its
invariant ring is exactly the ~19 physical parameters (Bento–Silva–Trautner,
JHEP 2024, Hilbert series + plethystic logarithm). So *within* the SM, the 19 are the
terminal invariants — nothing relates them, by a theorem. But a UV completion with a
**larger** group (SU(5), SO(10), the string geometry) shrinks the ring — which is
precisely why the theorem cannot extend to "any UV completion."

## The refined conjecture

> **The SM's 19 parameters are not derivable as unique values in any UV completion.
> They are functions of a smaller set of invariants — which UV completions keep
> shrinking — and those residual free inputs are pinned only by constraints and labels,
> never by a prediction.**

That is the constraint-first lesson, stated correctly one sector up. The original
"unpredicable" was too strong; the surviving claim is *stronger than it looks* because
it now says something precise: **a theory of everything predicts relations (invariants),
never values.**

## What this changes

- The conjecture, as first stated, is **retracted as overclaim** and **replaced** by the
  refined form above. (This is the Rule of Three doing its job at the level of ideas:
  two independent passes caught the overreach.)
- The flux-sector theorem survives untouched — it was always about *relations* (the only
  invariant is the tadpole), never about values.
- The honest open question is now sharper: **what is the *minimal* invariant ring any
  consistent UV completion can reach?** Is there a floor — a minimum number of free
  parameters below which no ToE can go? The flux sector's floor is 1 (the tadpole); the
  SM's floor is unknown.

## Named next steps (from the agents, kept)

1. **Quantify the reduction** (GUT): count exactly how many of the 19 a given UV
   completion turns into functions of fewer invariants, weighted against the new
   parameters it introduces (SUSY's ~105 soft terms make unification net-negative).
2. **Compute the invariant-ring dimension drop** (invariant theory): Hilbert series for
   the full SM (~19) vs SU(5)/SO(10) GUTs — show the dimension falls by exactly the
   number of unification relations.
3. **Find the floor**: is there a lower bound on the number of free parameters any
   consistent UV completion must leave? (The "minimal invariant ring" question.)
4. **Track DESI/Euclid** on w(z): if dark energy is dynamical, Λ stays a parameter; if
   the dS swampland conjecture is ever proven, Λ reclassifies as a constraint — the rare
   counterexample that would sharpen the refined claim further.

## The meta-lesson

This is what the fan-out is *for*. One angle (say, swampland alone) would have said
"conjecture confirmed"; one other (GUT) would have said "falsified." Only the spread
exposed the pivot — the one word with two readings — and produced the refinement. A
fan-out that only confirms is a rubber stamp; this one paid for itself by catching an
overstatement before it shipped.

*Sources: the five structured verdicts are in `research/sm-conjecture-fanout.js`; the
run itself returned the aggregated results this note synthesizes.*

## Update 2026-11-07 — the invariant-ring dimension drop is now computed (item 2 closed)

`scripts/validate_sm_invariant_dimension.py` computes the Krull dimension of the SM
coupling orbit space at three group levels (exact cross-section, cross-checked against the
rank test's Lie-algebra orbit ranks):

| group | Yukawa invariants | total | drop |
|---|---|---|---|
| SM (flavor only) | 13 | **19** | 0 |
| SU(5) (`Y_d = Y_e`) | 10 | **14** | 5 (3 mass ties + 2 gauge) |
| SO(10) (`Y_u = Y_d = Y_e`) | 3 | **7** | 12 (6 mass unifications + 4 CKM + 2 gauge) |

**This closes the "no clean duality group" question: that phrase is FALSE as stated.** The
GUT embeddings DO act on the couplings and DO shrink the orbit space (19 → 14 → 7). The
precise truth replaces the stale `sm-frontier.md` line: the SM's *own* flavor symmetry leaves
19; the only *known* larger groups are the GUTs, which reduce it — but of their relations only
gauge unification (drop 2) survives data, the Yukawa unifications are numerically wrong.

The remaining "empty gap" is the **full Hilbert/Molien series** (degree-by-degree, not just
the Krull dimension), which needs Molien/Hilbert–Serre — still absent from mathlib, the named
Lean target.

## Update 2026-11-07 (2) — the syzygy-refined Hilbert series is now EXACT (gap closed)

`scripts/validate_sm_molien_weyl.py` computes the Molien–Weyl series (torus constant-term +
Weyl averaging, validated against the single-matrix classical result) and finds the exact
closed form — including the Jarlskog syzygy, which the earlier free-ring approximation missed:

    H_Yukawa(t) = (1 − t²⁴) / ((1−t²)³ (1−t⁴)⁴ (1−t⁶)⁵ (1−t⁸) (1−t¹²))

* The **14 generators** (degrees 2×3, 4×4, 6×5, 8, 12) correct the earlier 13-generator count:
  the missing ones are `tr(Hᵤ²H_d²)` (degree 8) and the CP-odd **Jarlskog** `J` (degree 12).
* The **numerator (1 − t²⁴)** is the Jarlskog identity `J² = (CP-even polynomial)` — one
  syzygy at degree 24, cutting the Krull dimension from 14 to **13** (9 masses + 4 CKM),
  matching the Lie-algebra rank test.
* This is the "Molien/Hilbert–Serre" step the Lean plan named as an empty gap — now *computed*
  (sympy), though not yet *kernel-checked* in Lean.
