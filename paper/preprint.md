# Probably Approximately Correct String Theory: A PAC Verification Framework for the String Landscape

**Rob Mitchell**

*PACLAND project · github.com/robmitchellengineering-hub/pacland*

---

## Abstract

String theory's landscape contains on the order of 10⁵⁰⁰ vacua and no experiment
distinguishes most of them, so "unified string theory" conflates two problems —
*verification* (does some vacuum match our universe?) and *selection* (why that one?).
We separate them. Importing Leslie Valiant's computational learning framework, we make
verification precise as a **probably-approximately-correct certificate**: with
probability ≥ 1−δ a candidate vacuum's physics agrees with observation within
tolerance ε, *even when the verifier is itself approximate* — a two-level bound we
derive. We show single-candidate verification needs **no learnability assumption**,
while *search* over the landscape is governed by Valiant's evolvability theorem
(*evolvable ⇒ learnable*), yielding one necessary-condition conjecture: the
compactification→observables map is SQ-learnable. Finally, making the observable
measure finite collapses the sampling term and exposes the binding constraint —
verification is bounded by the number of *measurable* points of the true theory,
~19 for the Standard Model, which today gives a certificate radius of ~43%, not ~1%.
The framework's product is not a solution to unification but a **quantitative statement
of the verification deficit** — and a precise sense in which string theory is, today,
barely verifiable.

## 1. Introduction

String theory is not, in its present form, a single theory. It is a family of ~10⁵⁰⁰
metastable vacua — the *landscape* — each giving different low-energy physics
[1, 2, 3]. The statement "string theory is unified" decomposes into two claims that the
literature habitually fuses:

1. **Verification** — there exists a vacuum whose low-energy physics matches our
   universe (gauge group, spectrum, cosmological constant).
2. **Selection** — a *measure* singles out that vacuum, with weight ~1.

The first is checkable in principle; the second is not, and it is the part that has
remained open for roughly four decades. This paper concerns only the first, and does so
rigorously.

Two facts make verification hard even as a well-posed problem. First, the search space
is astronomically large. Second, and more fundamentally, the *verifier* is not ground
truth: the map from a compactification to its low-energy observables is computed by an
approximate solver — with systematic error from α′ corrections, non-perturbative
truncations, and the Kaluza–Klein tower. Any rigorous statement about verification must
therefore contend with an *imperfect labeler*.

We import the one framework built for exactly this regime. Valiant's
probably-approximately-correct (PAC) learning replaces "exact" with "with probability
≥ 1−δ, error ≤ ε" [4]. We apply that replacement to verification itself, and derive a
certificate whose two error terms are separately estimable. Three consequences follow:
a clean separation of *verification* (no learnability needed) from *search* (governed by
Valiant's evolvability theorem [5]); a necessary-condition conjecture for the whole
landscape program; and a bound that shows verification today is limited not by compute
but by *measurable physics*.

### Contributions

1. **A two-level certificate** (Theorem 2): an upper bound on the true error of a
   candidate vacuum that composes a candidate-vs-oracle term with an oracle-vs-truth
   term, valid when the verifier is approximate.
2. **The verify/search separation** (Section 4): single-candidate verification needs no
   VC dimension; search does, and the framework degrades gracefully when learnability
   fails.
3. **The measurable-physics bound** (Section 5): a finite observable measure collapses
   the sampling term, leaving a certificate radius set by the number of *measured*
   points — ~43% today, ~1% only with ~18,000.
4. **The learnability conjecture** (Section 6): the compactification→observables map is
   SQ-learnable; its false branch is a negative result about the entire landscape
   program.

## 2. Setup and notation

Let X be the **instance space** — the set of low-energy observables (masses, couplings,
the cosmological constant). Let D be a probability measure over X: *which* observables
are sampled, and with what weight. D is a stipulated scientific commitment, not given
by the physics (§5, §7).

Let c\* : X → Y be the **target** — the true low-energy physics of our universe — and
let h : X → Y be a candidate vacuum's predicted physics. We never observe c\* directly;
we observe it through an **oracle** Ô : X → Y, an approximate solver. Define the two
disagreement functions

```
g(x) = |h(x) − Ô(x)|,     e(x) = |Ô(x) − c*(x)|
```

and the **true error**

```
err_D(h) = Pr_{x ~ D}[ |h(x) − c*(x)| > ε ]
```

for a chosen tolerance ε. The goal is to certify `err_D(h) ≤ δ` for small δ. We cannot
observe `err_D(h)`, because c\* is reachable only through Ô.

## 3. The two-level certificate

The triangle inequality decomposes the unobservable error into two estimable pieces:

```
|h(x) − c*(x)|  ≤  g(x) + e(x)
```

hence, for any split point β ∈ (0, ε),

```
{|h − c*| > ε}  ⊆  {g > ε − β}  ∪  {e > β}
```

and, taking probabilities (a union bound),

```
err_D(h)  ≤  p_g(ε − β) + p_e(β)                       (⋆)
```

where `p_g(τ) = Pr[g > τ]` and `p_e(β) = Pr[e > β]`. The two terms on the right are
*individually estimable*, for different reasons: `p_g` compares two things we can both
**compute** (h and Ô), while `p_e` is the oracle's own failure rate, estimable by
**validating** Ô on points where c\* is known (measurement, or exact computation on
tractable cases).

**Theorem 1 (candidate bound).** *For a fixed h, sample n observables x₁…x_n ~ D i.i.d.
and let p̂_g be the empirical disagreement rate above ε − β. Then with probability
≥ 1 − δ_s,*

```
p_g(ε − β)  ≤  p̂_g + sqrt( ln(1/δ_s) / (2n) ).
```

This is a one-sided Hoeffding bound on a single proportion; no uniform-convergence
assumption, no VC dimension.

**Theorem 1′ (oracle validation bound).** *On m independent points z₁…z_m where c\*(z)
is known, let p̂_e be the empirical exceedance rate of |Ô − c\*| above β. Then with
probability ≥ 1 − δ_e,*

```
p_e(β)  ≤  p̂_e + sqrt( ln(1/δ_e) / (2m) ).
```

**Theorem 2 (two-level Valiant certificate).** *Fix ε > 0, β ∈ (0, ε), and confidence
budgets δ_s, δ_e ∈ (0,1). With probability at least 1 − δ_s − δ_e,*

```
err_D(h)  ≤  p̂_g + p̂_e + sqrt( ln(1/δ_s)/(2n) ) + sqrt( ln(1/δ_e)/(2m) ).
```

The certificate is the tuple `(ε, β, n, m, p̂_g, p̂_e, δ_s, δ_e)`, from which the bound
is computed. This is verification in the presence of an imperfect labeler — the
generalization of PAC's clean oracle that string theory actually requires.

**Remark (the binding constraint).** The oracle-validation radius is governed by *m*,
the number of points where the true theory is known. For the Standard Model, m is
bounded by the number of measured free parameters — not by compute. This is the crux of
Section 5.

## 4. Verification without learnability; search with it

Theorem 2 holds for a *single, handed-to-you* hypothesis h. It never invokes the
complexity of the hypothesis class. That is the point: **verifying what you are given
is cheap**, a Bernoulli-rate estimate.

Search is different. Search *selects* the empirically best of many hypotheses, and that
selection is biased — the empirical minimum overestimates the winner. Bounding
selection bias requires uniform convergence: for a finite class, a union bound gives
radius `sqrt(ln(|C|/δ)/(2n))`; for an infinite class, `VCdim(C)` (or the statistical-
query dimension `SQdim(C)`) replaces `ln|C|`.

The consequence for the architecture is a graceful-degradation statement:

> If the learnability conjecture (Section 6) is false, the *search* is infeasible, but
> the *verifier survives* — it can still certify any candidate proposed externally
> (by a theorist, or by another theory), because Sections 3's bound never uses VC
> dimension.

## 5. The observable measure and the measurable-physics bound

Make D **finite**: X is a finite, named list of N observables, each represented in
log-space so that "tolerance ε" means a uniform *multiplicative* tolerance from a gauge
coupling (O(1)) down to the cosmological constant (10⁻¹²²). D is then a weight vector
(w₁,…,w_N).

For a finite X that the oracle can fully evaluate, the candidate term is **exact**:

```
p_g(ε − β)  =  Σ_i w_i · 1[ |ln(h(x_i)/Ô(x_i))| > ε − β ],
```

computed directly — no sampling, no n. The certificate collapses to the oracle term:

```
err_D(h)  ≤  p_g(exact) + p̂_e + sqrt( ln(1/δ_e) / (2m) ).
```

The only remaining uncertainty is the oracle-validation term, bounded by **m, the number
of measured points**. With m ~ 19 (the Standard Model's free parameters) and δ_e = 0.025:

```
sqrt( ln(40) / (2 · 19) )  ≈  0.31   —   a ~31–43% radius.
```

The precise number depends on m and the confidence split, but the conclusion is
robust: to drive the radius below 1% needs `m ≈ 18,000` measured points — **four orders
of magnitude more than the theory gives us**. This is the quantitative statement of the
verification deficit: *string theory is today verifiable only to ~tens of percent
tolerance in the observables that matter, and the bottleneck is measurable physics, not
compute.*

A second, sharper consequence is a 2×2 that decides which observables matter:

| | c\* known (measured) | c\* unknown |
|---|---|---|
| **Ô can compute** | verification zone — tightens the certificate | prediction zone — falsifiable *later*, contributes nothing *now* |
| **Ô cannot compute** | unverifiable | — |

A vacuum whose only interesting predictions lie in the top-right cell is scientifically
sterile *today*, regardless of elegance — the framework states this as a theorem-like
consequence rather than a taste.

## 6. Search and the learnability conjecture

Valiant's evolvability model [5] restricts selection to **statistical-query** access to
the target: fitness is read only through aggregate statistics, never per-instance ground
truth. This restriction is not imposed here for tidiness — it is *already how the search
works*, because the only access a search has to a vacuum's fitness is the certificate of
Theorem 2 (sampled rates with confidence radii).

Valiant's theorem is:

> **Evolvable ⇒ learnable.** Any concept class evolvable in the restricted model is
> learnable in the corresponding statistical-query model.

Its contrapositive is the gate on search:

> **Conjecture.** The class `C = {h_v : X → Y : v ∈ V}` of observable-prediction
> functions induced by vacua has **polynomial SQ dimension** — i.e., the
> compactification→observables map is SQ-learnable.

- **True** ⇒ the landscape is *evolvable*: an evolutionary search with certificate-only
  access and provable guarantees can find a near-optimal vacuum.
- **False** ⇒ no search can find our vacuum — a negative result about the entire
  landscape program.

Either branch is a finding, and the conjecture is stated so it is attackable on small
vacuum classes before anyone touches 10⁵⁰⁰.

## 7. Discussion and limits

**The framework does not unify.** It does not select a vacuum — the measure (§1,
claim 2) is untouched and remains the 40-year-open physics problem. It does not
eliminate oracle error — it bounds it. It does not derive D — every certificate is
conditional on the stipulated observable measure. And it does not turn a surrogate into
truth: no error model, no certificate.

**The imperfect oracle is the through-line.** It appears in Theorem 2 (verification)
and again in Section 6 (search, where fitness is read through certificates). A fully
general treatment — *evolvability with an imperfect performance oracle* — is the natural
extension and is left open.

**What is buildable vs. not.** All of Sections 3–6 is software (the reference
implementation is in the accompanying repository). The measure problem, and the full
EFT extraction that a *non-trivial* learnability measurement requires, are physics
research, not tooling.

## 8. Conclusion

The obstacle to unified string theory is not a shortage of cleverness but a shortage of
*checkable claims* — and the deepest checkable claim in reach is not "is this vacuum
ours?" but "is the compactification→observables map learnable?" Answer that, and one
knows whether the landscape is searchable at all. Verification, done with Valiant's
guarantees, is the honest first move; selection is the hard second, and no amount of the
first buys the second. The framework's contribution is to make the first move *rigorous*
and to state, with a number, how far we are from being able to verify any of it.

## References

[1] Bousso, R. & Polchinski, J., *Quantization of four-form fluxes and dynamical
neutralization of the cosmological constant*, JHEP (2000).

[2] Douglas, M. R., *The statistics of string/M theory vacua*, JHEP (2003).

[3] Susskind, L., *The anthropic landscape of string theory* (2003).

[4] Valiant, L. G., *A theory of the learnable*, CACM 27(11), 1984.

[5] Valiant, L. G., *Evolvability*, J. ACM 56(1), 2009.

[6] Kearns, M., *Efficient noise-tolerant learning from statistical queries*, J. ACM
45(6), 1998.

[7] Feldman, V., *A complete characterization of statistical query learning with
applications to evolvability*, FOCS 2009.

[8] Valiant, L. G., *Probably Approximately Correct*, Basic Books, 2013.

[9] Demirtas, M., et al., *CYTools: A Software Package for Analyzing Calabi-Yau
Manifolds*, arXiv:2211.03823.

[10] Dubey, A., Krippendorf, S., Schachner, A., *JAXVacua — a framework for sampling
string vacua*, arXiv:2306.06160, JHEP 12 (2023) 146.
