# Verification Config — the sweep that finds the minimal set of checks for a claim

`docs/grounding.md` settled *what transfers* between disciplines (constraints-as-
necessary-conditions, the deficit as a lower bound, mutation-tested guards) and *what
does not* (the flux trio of tests, the Calabi-Yau oracles). It ends on the right
principle — *"name its own oracle and its own Rule of Three"* — but leaves the *how*
open. This doc is the how.

## The law (one invariant, every discipline)

> A claim is **verified** only when it survives **N independent checks, each targeting
> a distinct failure mode, and they all agree.**

- **independent** — no check's verdict is implied by another's. Two checks that always
  agree are one check twice, not two confirmations.
- **distinct failure mode** — each check catches a *different way the claim could be
  false*.
- **agree** — they must all pass. One disagreement is *unresolved*, never "one says X
  so X".

## N is not 3

The number of checks is the number of failure modes, and that varies:

| discipline | claim | failure modes | N |
|---|---|---|---|
| flux | "observable is structured, not random" | single-coord, multi-coord, finite-sample noise | 3 |
| climate | "the model conserves" | energy leak, mass leak, salt leak | 3 |
| (any) | (its own claim) | (its own ways to be false) | its own N |

The flux trio (MI / ridge CV / permutation null) and the climate trio (energy / mass /
salt ledgers) are *two configs of the same law*, not two rituals. A claim with two
failure modes needs two checks; one with five needs five.

## The machine — configure a discipline

1. **State the claim** — one falsifiable sentence.
2. **Enumerate the failure modes** — every way the claim could be false. This is the
   hard step and the whole skill: a failure mode not written down is one the config is
   blind to.
3. **One check per failure mode** — a check that goes red *iff* that mode is the truth.
4. **Prove each check can fail** — mutation-test it: inject its failure mode, the check
   must go red. A check that cannot fail proves nothing (H17).
5. **Prove the checks are independent** — if check A passing implies check B passing,
   drop B; it is a second copy of A, not a second confirmation.
6. **The config is the minimal set** that covers every failure mode. Fewer = a failure
   mode uncovered; more = redundancy, not confidence.

The **oracle** (grounding.md's "always-true answer") is just one special check: it
targets the failure mode *"we are measuring the wrong thing entirely."* It is not
separate from this machine — it is a slot in it.

## The sweep — the most efficient way to "verified"

Given a claim and a pool of candidate checks, find the smallest config automatically:

1. **Coverage matrix** `C[i][j] = 1` if check `i` catches failure mode `j` — measured by
   injecting `j` and observing check `i` go red.
2. **Minimal set cover** over the matrix: the fewest checks such that every failure mode
   is covered by at least one (greedy set-cover is fine at these sizes).
3. **Independence filter**: among the cover, drop any check whose verdicts are
   perfectly correlated with another's across a corpus.
4. **Result** = the config: the minimal independent check-set that still covers every
   failure mode.

Cost-aware variant: weight each check by run cost and solve weighted set cover — the
"most efficient" config in wall-clock, not just count.

## The guarantee

If a config covers every failure mode and they all pass, the claim is verified to the
*same* confidence the Rule of Three gives flux — regardless of discipline. The
confidence comes from covering the failure-mode space, not from which specific tests
are used.

## Worked example — the physics unification

Rob's target: **unify string theory** — show the exact structure of every sector is the
same two types, constraints + labels. That is a claim, so it gets a config.

**Claim (C):** the flux tadpole `N = FᵀJH` and the SM anomaly cancellation / hypercharge
quantisation are *the same kind of object* — a constraint = a symplectic/topological
invariant of the relevant group action — and together (constraints + labels) they
exhaust the exact structure.

**Failure modes** (ways C is false):
1. *Structurally different* — the tadpole and the anomalies are not instances of one
   thing (the "one framework" claim is forced, not found).
2. *Incomplete* — there is a third kind of exact structure beyond constraints + labels.
3. *Labels aren't exact* — h¹¹, h²¹, N_gen vary and are not exact after all.

**Candidate checks** (one per mode):
1. *Shared-machinery proof* — show the same Weyl-FFT / symplectic-invariant argument
   that forces the tadpole also forces the anomaly/hypercharge result (mode 1).
2. *Exhaustion* — enumerate the invariant ring / orbit space and show nothing exact
   remains (mode 2), mutation-tested by injecting a fabricated "third" invariant and
   watching the check reject it.
3. *Label-invariance* — re-derive h¹¹/h²¹/N_gen from topology alone and check they are
   deformation-invariant (mode 3).

The sweep then tells us which of these (and in what order) is the cheapest path to a
verified C — the "run options and pick the efficient one" step.

## What stays, what changes

- **Stays:** the law, mutation-testing, independence, "must all agree".
- **Changes per discipline:** the claim, the failure-mode list, and therefore the
  checks.
- The flux trio and the climate trio remain their own configs, unchanged; new
  disciplines *configure*, they do not import.
