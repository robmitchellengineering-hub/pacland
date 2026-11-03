# Deterministic in use — the scoped claim

**Claim.** In the enumerable window of the flux sector, every question this programme answers terminates
in an **exact count** verified against **full enumeration** — no sampler, no probability, no run-to-run
variance. The physics is deterministic *in its use* there, even though nothing here touches quantum
determinism in nature.

## The two qualifiers are the claim

Drop either and the sentence stops being true:

1. **the flux sector** — not quantum mechanics. No amplitudes, no Born rule, no measurement, no hidden
   variables; Bell is not addressed because nothing here can address it.
2. **the enumerable window** (today `b3 ≤ 8`) — not the physical flux range. The quintic is `b3 = 204`,
   so the exact tier reaches ~4% of it.

## Evidence

| b3 | flux pairs | orbits verified | matches closed form |
|---|---|---|---|
2 | 81 | 80 | yes |
4 | 6,561 | 6,560 | yes |
6 | 531,441 | 531,440 | yes |
**8** | **43,046,721** | **43,046,720** | **yes** |

`count(N) = [x^N] P(x)^(b3/2)` with `P = 4x² + 20x + 33 + 20x⁻¹ + 4x⁻²`, minus 1 at `N = 0`.
The b3 = 8 run: `{"b3": 8, "matches": true, "orbits": 43046720, "total_predicted": 43046720}`, 194.2 s on
`pacland-rog`.

Two more exact results in the same window: the invariant ring is `ℂ[N]` (one generator, proven), and the
measure space has dimension **exactly** `b3` (proved, not fitted).

## Why it is worth saying at all

The alternative method for the same questions is sampling with a budget, and it cannot reach this: the
accessibility study needs per-point sampling and returns 0.00137 points/try at `b3 = 12`. Forty-three
million exact pairs is a computation no sampling budget gets to.

## The second line of evidence, and what is still owed

`scripts/tadpole_independent_count.py` reaches the same distribution by a deliberately different route —
nested loops over the definition, `math.gcd` for primitivity, **no numpy, no polynomial, no shared code** —
so agreement is evidence rather than a tautology. It agrees exactly at `b3 = 2, 4, 6` (6,560 / 531,440
orbits, every class), and `tests/test_tadpole_independent.py` keeps it that way.

**And it has now run at `b3 = 8`** (`pacland-rog`, job `2026-11-03T1102Z-pacland-rog-independent-count-b3-8`):

```
primitive orbits : 43,046,720      classes: 17      all pairs - 1: 43,046,720
agreement        : YES — exact match on every class        elapsed: 69 s
```

Two implementations that share no code path agree at every rung up to `b3 = 8`. The claim is **PASS-2** on
that basis: two independent lines, not one run repeated.

## What would falsify it

- The independent implementation disagreeing at any rung — the `b3 ≤ 6` agreement is the check that
  already passed; `b3 = 8` is the outstanding one.
- A re-run on different hardware producing a different total — which would mean the count is not
  deterministic after all.
- A claim inside the window that turns out to need a sampling to settle.

## How to check it

```
python3 scripts/tadpole_distribution.py          # the ladder, b3 = 2, 4, 6
python3 scripts/tadpole_distribution.py --b3 8   # the 43M orbit run (~3 minutes)
```

## What this page is not

Not a claim about nature. Not "quantum mechanics is deterministic". Not "string theory solved". If a
sentence about this work cannot carry both qualifiers above, it is not this claim.
