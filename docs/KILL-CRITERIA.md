# Kill criteria — budget and stop rules per rung

Without a stop rule, the discovery loop is an open-ended grind that burns budget on a dead framing. These
are the rules that force a re-frame instead.

## Per-candidate budget

- A falsifier must be **cheap enough to be worth running**: if its cost exceeds the `EIG/cost` threshold,
  find a cheaper falsifier or mark the candidate `open` (deferred), never run the expensive test.
- A candidate is **falsified**, not re-tried: once a falsifier kills it, it is dead. No "but a variant…"
  without a *new* `id` and a *new* falsifier.

## Per-rung stop rule

For each rung (e.g. Rung A = the crossover, Rung B = the mass gap):

- **Budget:** `K` candidates tried (default `K = 10`) and `C` falsifier-cost (tokens/wall-time), whichever
  is hit first.
- **Stop:** when `K` candidates have been falsified with **no survivor**, stop generating candidates for
  this rung. The current framing is exhausted. Do **not** re-prompt with the same five questions.
- **Re-frame:** after the stop, the rung's *assumptions* are re-examined (which assumption did all K
  candidates share?), and one assumption is inverted *before* any new candidate is generated. A re-frame
  that does not change an assumption is not a re-frame.

## Global stop rule

- If two consecutive rungs hit their stop rule with no survivor, stop the whole loop and report: the
  taxonomy as framed is not producing survivors. That is a *result* (the taxonomy is wrong or the problem
  is framed wrong), not a failure to keep going.

## The honest point

The kill criteria are what separate "systematising discovery" from "spending forever." A discovery system
must be able to say **"this framing is dead, invert and restart"** — and, at the limit, **"we found
nothing, here is exactly what failed"**. That is the opposite of a grind; it is a search with a stopwatch.

**Current status of the two rungs under these rules:**

- Rung A (crossover): candidates tried = 1 (the scale-wise BE inversion); survivor = the toy
  `effectiveHessian_bounded_below`. Budget remaining: 9 candidates.
- Rung B (mass gap): candidates tried = 1 (the spectrum-exclusion inversion); survivor = the
  `HasMassGap` *statement*. Budget remaining: 9 candidates.
