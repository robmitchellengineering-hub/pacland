# Methods from the bench: what a known-answer inverse problem teaches the landscape

**Rob, 2026-11-02:** *"all of the above is an analogy for unifying string theory but we might be able to do it here and
extrapolate results and methods back to physics work on unifying string theory."*

This note takes that seriously. The acoustic and RF work of the last two days is **not a metaphor** for the landscape
problem; it is the **same inverse problem carried out where the answer is known**, and four of its results are methods that
transfer whether or not the analogy does. Each is stated with the number that produced it and the way to apply it there.

## Rule 1 — Explaining everything is not evidence of being right

**Measured here, today.** Recovering a room's dimensions from its modes, scoring on "what fraction of the measured peaks
does this candidate explain":

| scoring | recovered room | explains | true error |
|---|---|---|---|
| **one-sided** (explained peaks only) | 3.0 × 4.0 × 5.25 m | **100%** | **33.9%** |
| **two-sided** (explained × observed) | 2.63 × 6.00 × 6.13 m | 100% | **1.7%** |

**A candidate that explained every measurement was a third wrong**, because a room with more modes can always cover every
peak. The one-sided objective rewards *invention*.

**To the landscape:** the same trap is *"this structure explains all the observables"*. A model with more free structure
will always cover the observations. **The counterweight is the second direction** — what the candidate predicts that was
*not* used to fit it. A flux vacuum that explains every observable and predicts something checkable is worth ten that
explain the same list.

**Concretely**: every claimed unification result should carry **the observables it did not fit and predicts anyway.** If the
list is empty, the claim is one-sided and its agreement is not evidence.

## Rule 2 — Isospectrality: the answer is not unique, and that is a property, not a failure

A rectangular room's frequencies determine its dimensions **only up to** the symmetry class; and Kac's question has a
general **no** (Gordon–Webb–Wolpert: drums with the same spectrum and different shapes). **The first recovery I ran found a
room 34% wrong that explained every peak**, which is this theorem arriving as an engineering problem.

**To the landscape:** a spectrum does not determine the object that produced it. **So a claim of the form "the masses
determine the vacuum" is false in general** unless the question is restricted — and the restriction is the physics.
**The useful output is not the point estimate but the equivalence class** and what breaks the tie.

## Rule 3 — Priors are what break the tie, and they must be measured

In the room problem the tie is broken by things known independently: **the ceiling height, 2.58 m ± 0.09 m from a
barometer and three ARCore measurements**, and the fact that a room is a box. **The prior is a measurement, not a
preference** — that is the whole difference between a regularised inversion and a wish.

**To the landscape:** the tie-breakers are the measured constraints — gauge symmetry, the tadpole, `b3`, the observed
gauge group. **Which of them are measurements and which are assumptions must be stated per claim**, in the same way the
room's prior carries its error bar.

## Rule 4 — A statistic can be robust to an artefact and therefore blind to it

**Measured in `scripts/truth_bench.py`:** the spacing statistic ⟨r⟩ on a box's exact spectrum reads **0.378** (Poisson
0.386, GOE 0.531), and it **moves by 0.014 when 80% of the modes are deleted**. So a ⟨r⟩ verdict survives truncation — and
**cannot detect it.**

**To the landscape:** a diagnostic that is insensitive to the artefact it is meant to catch is not a diagnostic. **Before
cond(M) is read as evidence of truncation vs hierarchy, the question "does cond(M) move when I truncate a system whose
answer I know?" must be answered on a system whose answer is known.** That is the bench's job, and it is the same one
`truth_bench.py` does for ⟨r⟩.


## Rule 5 — Bandwidth does not buy identification, and counting cannot be rescued by more data

**Rob's hypothesis, tested:** *"higher the frequency, higher the resolution."* On the room, with a two-sided score:

| band | modes | recovered | score | error |
|---|---|---|---|---|
| 30–180 Hz | 89 | 3.00 × 4.62 × 6.06 | 0.96 | **23.6%** |
| 30–250 Hz | 211 | 3.06 × 4.75 × 6.00 | 0.98 | 21.5% |
| 30–500 Hz | 1 466 | 3.06 × 4.75 × 6.00 | **1.00** | 21.5% |
| 30–1000 Hz | 10 720 | 3.06 × 4.75 × 6.00 | **1.00** | 21.5% |

**A hundredfold more modes bought nothing.** The wrong room — **3.06 × 4.75 × 6.00 m against a true 6.05 × 6.05 × 2.58**,
a different *shape* with a similar volume — scores a **perfect 1.00** from 500 Hz upward, **at every bandwidth**.

**And the residual is worse.** Replacing the count with the mean nearest-mode distance prefers a **denser** spectrum that can
sit within **0.05 Hz** of every measurement — and lands **152%** away. **A finer grid of predicted levels fits anything.**

**Why, and what it means for the landscape:** the information *is* in the spectrum — a box's frequencies determine its
sides up to permutation, a theorem. **The objectives cannot reach it**, because a free search over three dimensions has
enough freedom to fit any score you write.

**So the frame that works is not fitting. It is label recovery**: the modes satisfy

```
4 f² / c²  =  nx²/a² + ny²/b² + nz²/c²
```

so the **squared** frequencies are **integer combinations of three unknowns**. Recovering the integer lattice is an
**algebraic** problem with a unique answer; fitting is a statistical problem with many.

**To the landscape, directly:** *a structure that explains every observation may be a different object with the same
footprint, and no amount of extra data at finer scale resolves it.* **What resolves it is exploiting the algebra that
generates the spectrum** — the integer/lattice structure of the charges, the flux quantisation, the grading — rather than
fitting the masses.


## Rule 6 — The algebra recovers what the fit cannot: 0.00% against 21.5%

**The frame that works, tested.** A box's squared frequencies are integer combinations of three unknowns,

```
f^2 = A n_x^2 + B n_y^2 + C n_z^2 ,     A = (c_air/2a)^2 , B = (c_air/2b)^2 , C = (c_air/2c)^2
```

so recovering the room is a **lattice** problem. Seeded from the smallest frequencies, scored two-sided (measured peaks on the
lattice **and** lattice modes observed), and preferring the **coarsest** lattice that explains the data:

| spectrum | recovered | error |
|---|---|---|
| **clean**, 20–180 Hz | **2.58 × 6.05 × 6.05 m** | **0.00%** |
| fitting, every band 250 Hz–1 kHz | 3.06 × 4.75 × 6.00 m | 21.5% |
| 30% of modes dropped, 0.3 Hz jitter | 2.59 × 6.06 × 6.06 m | 0.2% |
| 50% of modes dropped, 1.0 Hz jitter | 2.44 × 3.91 × 6.08 m | **35%** |

**The algebra found exactly what the fit could not**, and the hardening was not more search — it was **the measured prior**.

**Fixing C from the ceiling measured by a barometer and three ARCore readings (2.58 m ± 0.09) removes a third of the search
and, more importantly, the freedom that let a wrong lattice satisfy the score:**

| damage | recovered | error |
|---|---|---|
| 50% of modes dropped, 1 Hz jitter | **2.58 × 6.04 × 6.16 m** | **1.8%** |
| 30% of modes dropped, 0.3 Hz jitter | 2.58 × 6.10 × 6.11 m | **0.9%** |
| 60% of modes dropped, 1.5 Hz jitter | 2.58 × 3.86 × 6.21 m | **36%** |

**The prior did what the algebra could not do alone** — which is Rule 3, arriving as code. And the last row is the honest
limit: **below about thirty identified modes, a ceiling is not enough of a prior.**

**And each of the three scoring attempts taught the same lesson one level up**: one-sided scoring invented a room; residual
scoring preferred a finer grid; a fine-enough lattice passes through every measurement. **Every version of "it explains
everything" needed the other direction plus a complexity penalty to stop being satisfiable.**

**To the landscape, exactly:** a structure claim should be scored on **what it explains × what it predicts that was not
fitted**, and among structures that explain the data, **the coarsest wins**. If a landscape candidate needs a fine-grained
structure to cover the observables, that fineness is the evidence against it, not for it.

## What to build from this, in order

| step | why |
|---|---|
| **a two-sided objective for the landscape's structure claims** (fit × prediction) | Rule 1, and it needs no new data |
| **the equivalence class, not the point estimate**, for any "masses determine the vacuum" claim | Rule 2 |
| **a truth bench for cond(M)**: a synthetic system with a *planted* null direction, truncated at the same orders | Rule 4, and it settles the blocked question |
| **a register of which constraints are measured and which assumed**, per claim | Rule 3 |

## The falsifier for this note

> **If the landscape work adopts the two-sided objective and nothing changes in any verdict, then the one-sidedness was not
> a real risk there and this note was about the room, not the landscape.** That is a cheap test: it costs one rescoring,
> and it is the first thing to try.
