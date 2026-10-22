# The Mitchell Verification Deficit

### Why string theory can't be verified — *yet* — measured, not just argued

---

> **Correction (2026-10-22).** This document was written on 2026-10-18, when nothing was
> validated and the deficit was therefore zero, so the argument below started from that
> zero. The deficit has since been climbed — topology 4 + flux 1 + SM 4 — so `m` is 9
> today, and the numbers and the radius below are updated to match. The argument is
> unchanged; only what is true has moved.
> History: `m = 0` → 5 → 9, commit `0c6bfe0` (it was 5 before the SM rungs).

---

## The one honest sentence

People have said string theory is untestable for decades. We didn't discover
*that*. We built the instrument that turns the criticism into a **number**.

## The number

A claim like "this vacuum matches our universe" can only be *verified* with a
certificate, and every certificate has a confidence radius:

```
√( ln(1/δ) / 2m )
```

where `m` is the number of observables that are simultaneously:

1. **measured** — we know the real answer,
2. **computable** — a solver can evaluate them, and
3. **validated** — the solver's error is calibrated.

For string theory today, **m = 9** — topology 4, flux tadpole 1, and the Standard
Model's exact structure 4 all satisfy the three conditions at once. So the radius is:

```
√( ln(1/δ) / 2·9 )  =  0.45   at δ = 0.025
```

**The certificate is finite — but a 45% error bound is not a verification.** That's
not "hard." That's a measured, named, number.

## What we did *not* discover

The *why* was already known:

- the compactification → observables map is brutally hard to compute,
- the cosmological constant needs the unresolved uplift step,
- the measure (why this vacuum) is a mystery.

Smolin, Woit, and the whole field have known string theory is hard to test for
thirty years. Nothing here is a new reason.

## What we *did* build — the instrument

Three things the criticism never had:

1. **The separation.** Verification fails for one reason (`m = 9` — finite but coarse,
   and still zero once you ask for a *value*); selection fails for a different reason
   (it's underdetermined). They were always conflated; now they're split, and each has
   its own name and its own fix.

2. **The number.** Not "it's really hard," but "the certificate is finite but coarse,
   and here is exactly what would close it."

3. **The path.** Each observable that gains a *validated* error model moves `m` from
   9 toward ~19, shrinking the radius from ~45% toward ~31%. The deficit is a dial,
   not a wall.

## Why that matters for actually finding a solution

A criticism ends the conversation. An instrument tells you what to build next.

This one says, precisely: **build the first validated oracle** — a full spectrum
computation calibrated against an exact case. That's a concrete, checkable, named
task. Not a vibe. Not a debate. A job.

That's the real contribution, and it's a modest one: **we didn't find a new reason
string theory is unverified — we quantified the known one, which is what makes it
measurable, buildable, and improvable instead of just arguable.**

## The name

**The Mitchell Verification Deficit.**

The quantity: `m` (validated oracle outputs). The headline result: **`m = 9` for exact
structure today; the deficit is still total for the *values* — the SM's 19 free
parameters are measured, but not validated as *predictions* (m counts exact structure,
not values).**
