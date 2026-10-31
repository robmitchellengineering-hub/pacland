# Bold but provable — the research arm, pointed at unification

**The guiding light, stated at the top so nothing below drifts from it: this research arm exists to
contribute to a unified theory.** AirMatrix is where findings become hardware; this is where they become
structure. Every claim in this document is judged by one question: **does it constrain the joint structure of
flux, geometry and dynamics — or only one sector of it?**

The failure mode to avoid is the one this estate has been good at: producing impeccable facts about *our data*.
A claim that only describes our sample is not a contribution to unification, however true it is.

## What we already hold that bears on it

| result | why it is unification-relevant |
|---|---|
| **No de Sitter in the T⁶ F-term potential** (`V = −3e^K\|W\|² ≤ 0` at `DW = 0`, proved) | an impossibility about the vacuum structure, not a sample |
| **Conifold coefficients are exact rationals** (`37/30`, `2309/1800`, …) while the **basis change** carries `ζ(3)`, `π²` and has no relation below `10⁶` | the split is structural: exactness sits in *recursive* quantities and is lost in *normalisation* |
| **Flux scaling is a discrete gauge symmetry**; the orbit space is a point per tadpole | the landscape's gauge-invariant content is labelled by `(N, orbit)` — a counting structure, not a measure |
| **`max\|N\| = b3` exactly** in the enumerable window | the invariant content is *bounded and computable*, not `10^500` |
| **Sampler rate 0.00137 per try at `h12 = 5` vs 0.1325 at `h12 = 2`**, arrivals Poisson, ≤1 per call | the landscape is geometrically hard to reach — a fact about dimension, not about solution density |

## The claims, boldest first

Each carries what it would **exclude**. A claim that cannot name an exclusion is not admitted.

### B1 — The landscape's statistics depend on the tadpole alone, not on the moduli count

**Statement.** The SUSY fraction is a function of the flux tadpole `N`; the observed `h12` strata
(27.9% / 20.2% / 1.2%) are a **sampling** artefact, produced by the rate collapse (`96×`) interacting with the
`N`-distribution of what each campaign could reach.

**Why provable now.** Bin the 5,965 stored rows by `N` and compare `h12` strata *at fixed `N`*. If the
fractions agree within their intervals, the stratification is explained by the `N` mix and the sampler's rate,
not by physics. This uses only data on disk plus the measured rate.

**What it excludes.** That the moduli count shapes the landscape's statistics — i.e. it would kill the
"landscape changes character with `h12`" story and replace it with an invariant `(N, orbit)` classification.

**STATUS: REFUTED (2026-10-30).** Binned by tadpole, the `h12 = 4` rate is far below `h12 = 2` at **every**
bin (0.00 vs 0.17 at `2²`; 0.01 vs 0.34 at `2⁴`). The strata are not the `N` mix. Out of the same table came a
real positive: the SUSY fraction **rises monotonically with the tadpole** at every `h12` (0.03 → 0.49), which is
structure the compression engine's linear model class could not see. Next question: what tracks `h12` beyond `N`?

### B2 — Exactness is preserved by recursion and broken by normalisation

**Statement.** In this framework, a quantity is exactly computable **iff** it is defined by a recursion on
integers; anything requiring the large-complex-structure basis change acquires `ζ(3)`/`π²` and admits no small
rational relation.

**Why provable now.** The claim makes a *prediction about a quantity we have not computed*: pick one with a
recursive definition and one requiring the basis change, predict each one's form, then compute both. We already
have the two halves — `37/30` versus the `10⁶`-bounded PSLQ null.

**What it excludes.** That exact computability is accidental. If the pattern holds, it tells us **which
quantities in string theory can ever be exact** — a statement about the theory's structure, not about our
arithmetic.

**Confidence.** Medium-high; the prediction step is the test.

### B3 — De Sitter requires a Kähler modulus, not an uplift

**Statement.** With the dilaton/complex-structure sector alone, `V ≤ 0` identically at `DW = 0` (proved). Adding
an uplift multiplies a non-positive quantity — so **dS needs a Kähler modulus**, and with a single
non-perturbative term the one-dimensional `T` potential has a provable sign structure.

**Why provable now.** The `T`-potential with `W = W0 + A e^{−aT}` is one-dimensional and closed-form; its
critical points' sign can be classified algebraically across the parameter space, not sampled.

**What it excludes.** That an uplift alone can produce dS in this class. That is the sharpest statement
available in this direction, and it is the KKLT question asked precisely.

**Confidence.** High for the sign analysis; the claim's strength depends on the parameter range.

### B4 — The wall is geometric, and a warm start is a lens on the landscape

**Statement.** The per-try success probability falls roughly exponentially in the solve dimension, and a warm
start (seeding from a nearby solution) multiplies it by a constant substantially greater than one — so
`h12 ≥ 5` is expensive but **reachable**, and the cost is a computable function of dimension.

**Why provable now.** Twenty-call runs at `h12 = 3, 4` give the law's shape; one warm-start run at `h12 = 5`
tests the multiplier. Both are ~30-minute node jobs.

**What it excludes.** That the wall is fundamental — i.e. that `h12 ≥ 5` physics is unreachable.

**Confidence.** High; the risk is that the multiplier is ~1, which would itself be an answer.

### B5 — The invariant content of the landscape is countable and bounded

**Statement.** Modulo the discrete gauge symmetry, flux vacua are classified by `(N, orbit)`, and in a
`|component| ≤ 1` window `max|N| = b3` exactly — so the *invariant* count is a computable function of the
tadpole bound `L`, not `10^500`.

**Why provable now.** The exact ladder gives `max|N| = b3`; the orbit count at fixed `N` is an enumeration we
can do at `b3 = 2, 4, 6` and fit.

**What it excludes.** The `10^500` framing as a statement about distinct physics. That number counts flux
vectors; the invariant content is far smaller, and its size is a number we can compute.

**Confidence.** Medium — the counting is doable, whether it *matters* is the open question.

## The angle we have not been hitting

Everything above is computed **within one model**. Unification needs a statement that *links* two sectors. The
one link we already hold and have never used: **the same lattice that gives `max|N| = b3` is the lattice whose
dimension sets the sampler's rate.** That is a genuine cross-sector coupling — the *classification* (combinatorial)
and the *accessibility* (geometric) are two faces of the same integer `b3`.

**If B1 and B4 both hold**, they compose into something stronger than either: the landscape's statistics are
governed by `(N, orbit)` while its accessibility is governed by the dimension — so a complete statement needs
both, and `b3` appears in both. That composition is the closest thing to a unification-shaped claim this arm
currently has, and it is cheap to test.

## What unification would look like from here

A falsifiable target: **a single invariant `I(L, h12)` that predicts both the SUSY statistics and the sampling
rate.** If such an `I` exists, the two "independent" findings are one. If it provably cannot exist, that is an
impossibility in the same class as B3 — and an impossibility about the *framework* is a real contribution.

## Sequence

1. **B1** — hours, data on disk, and it decides whether the landscape story survives.
2. **B4** — a node run, and it decides whether `h12 ≥ 5` is reachable.
3. **B3** — closed-form algebra, and it is the sharp KKLT statement.
4. **B2 and B5** — the structural pair, once the first three have set the frame.

## Applications, kept in view

The estate's other consumer is AirMatrix, and two of these travel directly: **B4's rate law** is a statement
about solvers in high dimension (the same geometry governs the room-mode fits), and **B2's exactness
criterion** is the same one that decides which acoustic quantities can be computed exactly rather than measured.
The research arm should surface those when they land, not after.

## What would make this plan wrong

- If B1 fails — the strata survive at fixed `N` — then the landscape *does* vary with `h12` and the invariant
  content is not `(N, orbit)`. That would be the most interesting failure, and it sends the work back to the
  flux lattice with a new question.
- If B2's prediction step fails for one of the two chosen quantities, the criterion is wrong and exactness is
  accidental — which would undercut the whole exactness programme's significance.
- If B3's sign analysis leaves the parameters essentially unconstrained, the claim collapses to "dS needs
  freedom", which is not worth stating.
