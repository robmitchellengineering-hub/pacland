# Plan — from falsification to answers

**Why this document exists.** Six instruments now say what is *not*, and a process exists for turning those
negatives into questions. What has not yet happened is a single answer about **nature** rather than about our
data. This is the plan for changing that, and it names what is missing rather than adding a seventh instrument
of the same kind.

## The diagnosis, in three parts

1. **Every fact rests on one sampling campaign.** The corpus is a heuristic ISD sample: 5% of its rows are
   non-vacua, 0.05% are scaling copies, and it covers 0.0024% of the primitive orbits in the one window we can
   enumerate exactly. A conclusion drawn from it is a conclusion about the campaign until something else is
   shown.
2. **Most negatives are about tooling.** This week's findings — the rounding flag, the choice-dependence, the
   coverage defect — are true, useful, and constrain nothing about the universe. They constrain our data.
3. **No transfer has been worked.** The dictionary certifies three maps and has never been used to compute
   something unreachable in the easy frame. Until it has, it is bookkeeping.

Each gap has one route, and the routes are independent.

## Route C — the transfer payoff *(cheapest; a capability)*

**What.** Use the mirror-map entry to compute a period **outside** the large-complex-structure radius of
convergence but inside the conifold one, by translating into the conifold frame, computing there, and
translating back.

**Why it is an answer and not a demonstration.** It produces a *number that the easy frame cannot produce*, and
that number is then checkable: the continued period must still satisfy the Picard–Fuchs equation at points
where the `z`-series does not converge. A capability that verifies itself.

**Cost.** Mac, a day. **Pass mark:** a period value at `|z| > z_c` with a residual against the PF equation
below `1e-10`, and the same value obtained from a second, independent route (the conifold series alone at a
point where both converge) agreeing to `1e-12`.

**Falsifier.** If the translated value fails the PF check at every point outside the radius, the map is a
relabelling and not a translation — and the dictionary is then bookkeeping, honestly labelled.

## Route A — the scaling study *(cheap; reframes everything)*

**What.** Every headline fact, recomputed as a function of `b3` across the windows that can be enumerated
exactly (`b3 = 4, 6, 8, 10` at `max_abs = 1`, and `max_abs = 2` where the lattice permits). Does the SUSY
fraction, the tadpole bound, the null-cone occupancy, the primitivity rate **move with `b3`**?

**Why.** A fact that holds for every `b3 ≤ B` is a statement about the *lattice family*, not about one sample.
A fact that moves with `b3` is a warning that every pooled number we quote is size-dependent. Either answer
changes how the corpus is read.

**Cost.** Mac, hours — all exact enumeration, no node, no solver. **Pass mark:** each fact has a value at
every `b3` and a verdict (scale-invariant / scale-dependent with the direction), recorded on the positives page
with the window.

**Falsifier.** If the SUSY fraction is not monotone in `b3`, the "landscape" framing itself is size-dependent
and the pooled corpus numbers must carry a size caveat permanently.

## Route B — an impossibility about the spectrum *(expensive; permanent)*

**What.** Turn the measured "no de Sitter from the SU spectrum" into an **exhaustive statement**: for small
`b3`, enumerate the whole flux lattice in a stated window and check the scalar potential's sign at every
critical point (or prove none has `V > 0`). Same for the tadpole bound `N ≤ L`.

**Why.** An impossibility is the strongest kind of positive: it excludes a class of construction permanently,
and it does not decay when new data arrives.

**Cost.** Node, days, and it needs the try-budget wrapper (below) to be meaningful. **Pass mark:** a statement
of the form *"no vacuum with `V > 0` exists in window W at `b3 = B`"*, with W enumerated and its size given,
plus the same check repeated at two `b3` so the result is not a single-size artefact.

**Falsifier.** One object with `V > 0` in the window kills the claim — which is exactly what the existence
engine is for, and why the two must be aimed at the same window.

## The three process items

- **Try-budget wrapper.** `sample_critical_points` exposes `n_target`, not a try count, so every "escalated"
  run so far silently did 400 tries (T1). A loop that accumulates tries until a budget is spent unblocks T1 and
  makes every future yield number meaningful.
- **The cycle log.** One entry per closed loop: the negative that opened it, the question it forced, the object
  it produced, and **what it excluded**. Generated from the registers where possible. This is how the loop's
  rate becomes measurable instead of claimed.
- **The threshold discipline.** `is_minimum` is exactly `λ_min > 1e-6`; every minima count must carry its
  threshold. Generalise: any quoted number that depends on a stated threshold prints it, or it does not ship.

## Sequence

1. **Route C** — a day, produces a capability and tests the dictionary's value.
2. **Route A** — hours, and it may change what Route B should even ask.
3. **Route B** — needs the try-budget wrapper first; days, and it produces the first permanent answer.
4. **Cycle log** — built alongside C and A, since they are the first two loops it will record.

## What would make this plan wrong

- If Route A finds every fact scale-dependent, then the corpus is not a window on a family and Route B's
  window statements are the only honest kind — which changes the sequencing but not the plan.
- If Route C's translated value fails the PF check, the dictionary is a relabelling: then the next instrument
  is *not* a fourth engine but a decision about whether to keep it at all.
- If Route B finds a `V > 0` object in the window, the "no de Sitter" claim is refuted at small `b3` — the most
  informative possible outcome, and the plan should say so before the run.

## What we deliberately do not do

Build another engine of the same species. The estate has six, two registers and a process; the binding
constraint is no longer instrumentation. It is that nothing we have yet produced is a statement about nature.
