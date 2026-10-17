# The Valiant certificate — verification semantics (L3)

This document is the intellectual core of PACLAND. It defines what "verified" means in
a regime where (a) exact verification is physically and computationally impossible, and
(b) the labeler is itself approximate.

## 1. Objects

| Symbol | Meaning |
|---|---|
| `X` | Instance space: the set of observables (masses, couplings, Λ, spectrum data) |
| `D` | A probability measure over `X` — *which observables we sample, and with what weight* |
| `c* : X → Y` | Target concept: the true low-energy physics of our universe |
| `Ô : X → Y` | The **oracle** (L2): approximate labeler with an error model |
| `h : X → Y` | A candidate vacuum's hypothesis (its predicted observables) |
| `ε` | Tolerance: how close counts as "matches" |
| `δ` | Confidence: probability the guarantee holds |

## 2. The impossible goal, restated

The naive ask is to prove `h = c*`. That fails twice:

1. **Underdetermination** — the landscape has many vacua observationally close to ours;
   point equality is the wrong target.
2. **No ground truth** — we never observe `c*` directly; we observe `Ô`, an
   approximate simulator, and finite astronomical data.

So the target becomes: bound the **error probability**

```
err_D(h) = Pr_{x ~ D}[ |h(x) − c*(x)| > ε ]
```

and certify it is ≤ some small value with high confidence.

## 3. The two-level bound

Standard PAC assumes the oracle labels by the *true* concept. Here it does not, so we
decompose the error with the triangle inequality:

```
|h(x) − c*(x)|  ≤  |h(x) − Ô(x)|  +  |Ô(x) − c*(x)|
```

- **Systematic term** `|Ô(x) − c*(x)|`: the oracle's own bias. Bound it by `β`, from the
  L2 error model. (In general `β` is a random variable with its own confidence `δ_β`,
  not a constant — see open questions.)
- **Statistical term** `|h(x) − Ô(x)|`: the disagreement between the candidate and the
  oracle, estimated empirically.

Then:

```
|h(x) − c*(x)| > ε   ⇒   |h(x) − Ô(x)| > ε − β
```

so

```
err_D(h)  ≤  Pr_{x ~ D}[ |h(x) − Ô(x)| > ε − β ]
```

The right-hand side is now **empirically estimable** from `n` i.i.d. samples, because it
compares two things we can both compute (`h` and `Ô`). A Hoeffding bound turns the
empirical disagreement rate into a confidence interval at level `δ`. Composing with the
oracle's own `δ_β` gives the total confidence.

## 4. The certificate

A **Valiant certificate** for candidate vacuum `v` (hypothesis `h`) is the tuple

```
(ε, δ, n, agreement, oracle_bias)
```

asserting:

> With probability at least `1 − δ`, the true physics of `v` is within `ε` of
> observation — where `δ` composes the sampling confidence and the oracle's
> systematic-confidence, and `agreement` is the empirical match rate measured against
> the oracle on `n` samples.

The philosophical claim: **this is what verification in underdetermined science always
was — probably-approximately-correct — and Valiant's framework is what lets us state the
tolerance and confidence explicitly instead of pretending.**

## 5. Sample complexity and the VC dimension

To certify with tolerance `ε` and confidence `δ`, the number of observables sampled must
satisfy (up to constants) the standard bound

```
n  ≳  ( VCdim(C) / ε² ) · log(1/δ)
```

where `C` is the concept class — the set of observable-prediction functions induced by
vacua.

**The governing question of the whole system:**

> What is `VCdim(C)` for the `compactification → observables` map?

- **Low** → the map is efficiently learnable, hence (by Valiant's evolvability theorem)
  **evolvable** — the landscape can be navigated by L4's evolutionary search with
  provable guarantees.
- **Unbounded / astronomically high** → **no** search can find our vacuum; this is a
  deep *negative* result about the landscape program.

Either answer is a real scientific finding, and it is testable on *small* vacuum classes
long before anyone touches the full 10⁵⁰⁰.

## 6. What the certificate does and does not do

| Does | Does not |
|---|---|
| Certify observational indistinguishability within (ε, δ) | Prove `h = c*` |
| Bound oracle error explicitly | Eliminate oracle error |
| Give a concrete, checkable claim per vacuum | Select among *multiple* certified vacua |
| Expose the learnability structure of the map | Supply the landscape measure |
