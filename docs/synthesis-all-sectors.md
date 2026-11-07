# The Complete Exact Structure Theorem — across all three sectors

**The synthesis of the proof arm + the verification arm.**

This is the cross-sector statement the constraint-first program has been building toward: the
same *forced/free* decomposition, now machine-checked or measured in **three** sectors.

## The theorem

> A theory's **exact** content is exhausted by three classes — **constraints** (what it forbids),
> **labels** (which geometry is picked), and **parameters** (free inputs) — and its notorious
> "issues" (the measurement problem, the free parameter values) are *provably the free column*:
> not bugs, and not derivable from the forced column.

| sector | forced (kernel-checked) | free (delimited) | the "issue" |
|---|---|---|---|
| Quantum theory | Born rule `Tr(ρP)` (Gleason, CKM route) | which outcome occurs | non-determinism / measurement problem |
| Standard Model | anomaly cancellation + hypercharge uniqueness | the 19 (→ 26/28 with ν) | "why these values" |
| Flux / string | the D3 tadpole = unique invariant (Mitchell/FFT) | W₀, g_s, masses, Λ | "which vacuum" |

## The real answers this gives

1. **Non-determinism is not a bug to patch.** Gleason (kernel-checked) shows the Born *rule* is
   forced by non-contextuality but the *outcome* is not — so no exact structure can make QM
   deterministic. The measurement problem is the free column, delimited, not solved.

2. **The 19 (26/28) are not hiding a missing symmetry.** The invariant theory shows the SM's own
   flavor symmetry leaves them, the known UV groups (GUTs) reduce them but give wrong answers, and
   the exact Hilbert series `H_Y(t) = (1−t²⁴)/…` pins their orbit-space dimension. "Why these
   values" has no *known* answer and no *known* symmetry forces one.

3. **The two free columns are the same kind of thing.** QM's free outcome and the SM's free
   parameters are both "what the theory hands you" — and the flux sector shows the pattern is
   universal: one sector's free column was *collapsed* by a duality group (Sp → the tadpole), the
   SM's was *not* (flavor leaves 19; GUTs fail), and QM's *cannot be* (no non-contextual
   deterministic completion).

## What this closes, and what it leaves open

**Closed:** the loose "issues" are now precise — three sectors, each with a kernel-checked forced
half and a delimited free half, so the ToE's exact content is a *complete classification*
(constraints + labels + parameters), not a slogan.

**Open (and now sharp):**
- the **measurement problem** (Gleason gives the rule, not the collapse);
- the **19/26/28 values** (free under known groups, not predicted);
- the **gravity/QG sector** — whether gravity also decomposes as forced + free (the SEXTANT lane),
  and whether Molien/Hilbert–Serre can be kernel-checked in Lean (the remaining formalization gap).

The value is not that we solved the issues — it is that we've **delimited exactly where the free
column is**, in three sectors, with machine-checked certificates on the forced side, so a whole
class of wrong answers (deterministic QM, a hidden symmetry fixing the 19) is now *closed off*.

## Update 2026-11-07 (4) — quantum gravity's forced half

`Gravity/QG.lean`: the QG forced content is the *union* of the Born rule (Gleason) and the
Einstein equation (Lovelock). The new forced condition joining them — the **semiclassical
consistency** — is kernel-checked: the Einstein tensor is divergence-free (`einstein_divergence_free`),
so its source (classical matter or a quantum expectation value `⟨T_ab⟩`) must be conserved,
`∇^a T_ab = 0`. The free column is `{which outcome, G, Λ, the QM-gravity coupling}`.
