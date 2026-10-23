# Compare-notes: the SM "floor" question — second fan-out

The first fan-out refined the SM conjecture to *"a ToE predicts relations, never
values."* That named a sharper question — **what is the minimum number of free
parameters any consistent UV completion can reach?** Five agents attacked it. The
spread reveals the question itself was hiding a conflation.

## The raw spread

| angle | floor estimate | confidence |
|---|---|---|
| GUT ladder | ~10 (Yukawa sector); no *total* floor below 19 | medium |
| String theory | **0 continuous** (fully moduli-stabilized vacua) | medium |
| Swampland | **1 discrete** (the tadpole); 0 continuous | medium |
| Mathematical | **0 in principle**; 18 ratios + 1 scale | medium |
| Flux-sector lesson | **19** (the flavor ring has 19 invariants) | medium |

Every agent gave a different number — 0, 1, 10, 19 — and none is wrong. That is the
finding.

## The pivot: "free parameter" has three meanings

The five answers are answering three different questions:

1. **Continuous free parameters** — massless moduli you can dial. *Floor = 0.* String
   vacua (KKLT, LVS, IIA flux) stabilize every modulus; there is no residual
   continuous knob. (Swampland + string agree: 0 continuous.)

2. **Discrete free parameters** — the flux/topology integers. *Floor = 1* — the D3
   tadpole, the one thing not fixed by stabilization, bounded but not pinned. But the
   discrete landscape is ~10⁵⁰⁰, so "1 discrete constraint" comes with an enormous
   discrete degeneracy.

3. **Invariants** — the SM's 19 are *not* free parameters in the continuous/discrete
   sense; they are the **orbit-space dimension** of the flavor group, i.e. the number
   of independent *relations* any UV completion must reproduce. The mathematical and
   flux-lesson angles agree: the flavor ring has exactly 19 fundamental invariants, and
   a UV completion is *allowed* to have fewer parameters — it just predicts (19 − N)
   relations and lands on a subvariety of the orbit space.

So the question "what is the floor?" has no single answer, because "free parameter" was
doing three jobs.

## The refined answer: the floor is a *structure*, not a number

> **A consistent UV completion can reach 0 continuous free parameters and 1 discrete
> one (the tadpole) — but it must still *produce* the 19 flavor invariants as relations.
> The floor is therefore: 0 continuous, 1 discrete, 19 relations — and the 19 relations
> can be generated from a smaller number of UV parameters (GUTs do ~19 → 14 in the
> Yukawa sector), which is precisely "predicts relations, never values."**

This is the first fan-out's refinement, now made fully precise. The "19 parameters are
unpredicable" was never the right frame — the correct frame is: **the 19 are the
relations a ToE must reproduce; how few parameters it needs to produce them is the real
(open) question, and the flux mechanism (duality + FFT ⇒ collapse to 1) does *not*
generalize, because the SM's SU(3)⁵ is a reparametrization group, not a duality.**

## What this changes

- **The "floor" question is retired as ill-posed** and replaced by the tripartite
  statement above. (Second conflation the fan-out caught — this is the tool working.)
- **The flux-sector lesson does not generalize** — the flux floor of 1 comes from a
  *duality* group (Sp), whose orbit space collapses; the SM's flavor group is a
  *reparametrization* group, whose orbit space is 19-dimensional. A reduction below 19
  needs a genuinely new mechanism (dynamical Yukawas as functions of fewer moduli).
- **The real open question is now concrete**: can the 19 invariants be generated from
  fewer than ~14 UV parameters, and what is the *actual* lower bound? The flux-lesson
  angle names the test: express the 19 invariants as holomorphic functions of the
  moduli in a small-h²¹ compactification and compute the rank of the moduli→invariants
  map.

## Named next steps (kept)

1. **Fix a counting convention** and tabulate total parameter count for minimal SU(5),
   SO(10), E6, Pati-Salam, trinification vs the SM's 19 (GUT ladder).
2. **The rank test**: in a flux compactification with small h¹¹+h²¹, express the 19
   invariants as functions of moduli and compute whether the Jacobian has rank < 19
   (flux-sector lesson) — the decisive test for whether the floor is dynamically
   reducible.
3. **The discrete-vs-continuous bookkeeping**: decide whether discrete flux/topology
   data counts as "parameters"; if yes, the string answer (huge discrete landscape)
   contradicts any small floor — so the synthesis must define the term before merging.
4. **Swampland bound**: verify whether tadpole cancellation gives a strict lower bound
   (≥1) or only an upper bound on the flux integer.

## The meta-lesson, twice now

Two fan-outs, two conflations caught before they shipped: first "unpredicable" (two
readings), now "free parameter" (three meanings). A single angle would have picked one
meaning and answered confidently. Only the spread forced the disambiguation. The fan-out
is not a rubber stamp — it is the instrument that keeps the *ideas* honest the way the
Rule of Three keeps the *measurements* honest.

*Sources: the five structured verdicts are in `research/floor-fanout.js`; the run
returned the aggregated results this note synthesizes.*

## Resolved (the four named next steps, closed)

1. **GUT ladder** (`scripts/validate_gut_parameter_count.py`): SM 19, SU(5) 19, SO(10) 20,
   E6 21, Pati-Salam 21, trinification 20 — all ~19, shuffle not reduction. No row drops
   below 17, none at the naive 14 (the Higgs growth offsets the gauge unification).
2. **The rank test** (`scripts/validate_sm_rank_test.py`, `docs/sm-rank-test.md`): the SM's
   own flavor symmetry leaves orbit-space rank **19**; the dynamical bound is
   `rank ≤ 2·h¹¹+2·h²¹+2`; the only known UV symmetries (GUTs) collapse 5 (minimal SU(5)) or
   12 (SO(10)/E₆/Pati–Salam/trinification) of 19 — only gauge unification (2) survives data. The
   19 floor is real. ⚠️ corrected 2026-10-23 (falsifier #2): see docs/falsification-status.md
3. **Discrete-vs-continuous bookkeeping** (this section): the "19" and the "10⁵⁰⁰" count
   *different* things, so there is no contradiction to merge.
4. **Swampland bound** (`scripts/validate_swampland_bound.py`): the tadpole gives only an
   upper bound `N_flux ≤ L`; it can be 0 or negative, so there is no lower bound `≥ 1` from
   tadpole cancellation alone (a positive bound needs the ISD/SUSY assumption).

## The bookkeeping decision (item 3, settled)

The "19 free parameters" are **continuous** (real couplings, masses, angles). String
compactifications also carry **discrete** data — flux integers, Hodge numbers, brane
wrapping numbers — which label the huge discrete landscape (~10⁵⁰⁰ vacua). Counting the
discrete data as "parameters" would make the string answer "enormously many", flatly
contradicting any "small floor" like 19. The resolution is the constraint-first
classification, which already separates the two:

- **labels** (discrete, topological/geometric): flux quanta, `h¹¹,h²¹,c₂,κ`, brane
  wrapping numbers — these index *which* vacuum, and there are ~10⁵⁰⁰ of them;
- **parameters** (continuous): the 19 couplings — these are the *dimension* of the
  low-energy parameter space at each vacuum.

So the "floor" (19) is a **continuous floor** — the dimension of the parameter space —
while the "landscape" (10⁵⁰⁰) is a **discrete count** of vacua. They are different
quantities and do not compete: a theory with 19 continuous parameters can still have
10⁵⁰⁰ discrete vacua. The floor question is *only* about the continuous dimension; the
discrete landscape is the answer to a different question ("how many vacua?"), not a
counterexample to the floor.
