# PACLAND — Roadmap and paper outline

The linear argument, from first sentence to last, in the shape of a paper. Each section
is a paragraph of the actual argument plus a pointer to the doc that carries the detail.
This file is the spine; the `docs/` files are the flesh.

---

## Status

Spec complete for the verification core (L3), the search layer (L4), the knowledge
layer (L5), and the observable measure. L2 (oracle engineering) and L6 (the measure
problem) are specified as *boundaries*, not as solvable-by-us. **No code. No claims of a
prediction. The product of the framework is a number, not a vacuum.**

---

## Paper outline

### Title

**Probably Approximately Correct String Theory: verification, search, and the
measurable-physics bound for the landscape.**

### Abstract (draft)

String theory's landscape contains on the order of 10⁵⁰⁰ vacua and no experiment
distinguishes most of them, so "unified string theory" conflates two problems —
*verification* (does some vacuum match our universe?) and *selection* (why that one?).
We separate them. Importing Leslie Valiant's computational learning framework, we make
verification precise as a **probably-approximately-correct certificate**: with
probability ≥ 1−δ a candidate vacuum's physics agrees with observation within tolerance
ε, *even when the verifier is itself approximate* — a two-level bound we derive. We show
single-candidate verification needs **no learnability assumption**, while *search* over
the landscape is governed by Valiant's evolvability theorem (*evolvable ⇒ learnable*),
yielding one necessary-condition conjecture: the compactification→observables map is
SQ-learnable. Finally, making the observable measure finite collapses the sampling term
and exposes the binding constraint — verification is bounded by the number of
*measurable* points of the true theory, ~19 for the Standard Model, which today gives a
certificate radius of ~43%, not ~1%. The framework's product is not a solution to
unification but a **quantitative statement of the verification deficit** — and a precise
sense in which string theory is, today, barely verifiable.

### 1. Introduction

*The argument:* unification is stalled not (only) because the physics is hard, but
because two claims are fused — "a vacuum exists that matches us" (verification) and "a
measure picks this one" (selection) — and neither is well-posed as a claim one could
check. The first is checkable in principle and we formalize how; the second is not, and
we name it as the boundary.

*Doc:* [`docs/open-questions.md`](docs/open-questions.md) §1, §5.

### 2. Background: Valiant's three ideas, and prior ML-of-the-landscape

*The argument:* PAC learning (1984) gives the semantics of approximate verification;
evolvability (2009) gives a model of search whose power is *provably bounded by
learnability*; educability (2024) gives the notion of accumulating and reusing knowledge
across sources. Prior machine-learning work on the landscape (neural CY metrics, flux
enumerators, supervised surrogate models) is *complementary machinery*, not this
framework: none of it emits a verification guarantee, which is the whole point here.

*Docs:* [`docs/architecture.md`](docs/architecture.md) (L1–L6 map).

### 3. The two-level certificate: verification with an imperfect verifier

*The argument (contribution 1):* the target `p_* = Pr[|h − c*| > ε]` is unknowable
directly, but the triangle inequality splits it into a candidate-vs-oracle term
(estimable by sampling) and an oracle-vs-truth term (estimable by validation), giving the
four-term bound

```
p_*  ≤  p̂_g  +  p̂_e  +  sqrt( ln(1/δ_s)/(2n) )  +  sqrt( ln(1/δ_e)/(2m) )
```

with total confidence `1 − δ_s − δ_e`. This is verification in the presence of an
*imperfect labeler*, the generalization of PAC's clean oracle that string theory
actually requires.

*Doc:* [`docs/verification-formal.md`](docs/verification-formal.md) §1–§5.

### 4. Verification needs no learnability; search does

*The argument (contribution 2):* verifying a *single* handed-to-you candidate is a
Bernoulli-rate estimate — Hoeffding, no VC dimension. But *search* selects the empirical
best of many candidates, and that selection is biased; bounding it requires uniform
convergence, hence `VCdim(C)` (or `SQdim(C)`). Consequence: if the learnability
conjecture fails, the *search* dies but the *verifier survives* — the system degrades
gracefully to verifying external proposals. This separation is what makes the framework
honest about which failure is fatal.

*Doc:* [`docs/verification-formal.md`](docs/verification-formal.md) §6.

### 5. The search layer and the learnability conjecture

*The argument (contribution 3):* Valiant's evolvability model is not an analogy bolted
onto a GA — its statistical-query restriction is *already how our search works*, because
L4's only access to fitness is the L3 certificate. The theorem's contrapositive is the
gate:

> If the class of vacuum-induced prediction functions is not SQ-learnable, no
> certificate-only evolutionary search can converge to a near-optimal vacuum.

The conjecture — `SQdim(C) = O(poly(p))` — is testable on the IIB flux corner first, and
either answer is a finding: *true* means the landscape is navigable, *false* means no
search can find our vacuum, a negative result about the whole program.

*Docs:* [`docs/evolvability.md`](docs/evolvability.md); [`docs/encoding.md`](docs/encoding.md).

### 6. The observable measure, and the measurable-physics bound

*The argument (contribution 4):* `D` — the measure over observables that defines "close
to our universe" — is made finite and log-space (ten dimensionless observables, uniform
weights as a stated placeholder). The finite-set move **collapses the sampling term**:
you compute the exact weighted disagreement, no `n`. What remains is the oracle-error
term, bounded by `m`, the number of *measured* points of the true theory. With `m ~ 19`:

```
radius  =  sqrt( ln(1/δ_e) / (2m) )  ≈  0.43   (at δ_e = 0.025)
```

This is the paper's headline number: **string theory is today verifiable only to ~43%
tolerance in the observables that matter, and the bottleneck is measurable physics, not
compute.** A 1% certificate needs `m ≈ 18,000` — four orders of magnitude more than we
have.

*Doc:* [`docs/observable-measure.md`](docs/observable-measure.md) §5–§7.

### 7. Results

Three claims the framework actually delivers, in increasing order of substance:

1. **A certificate is computable** from quantities we can measure (`p̂_g`, `p̂_e`) plus
   declared budgets (`ε, β, δ_s, δ_e`). Verification stops being a vibe.
2. **The verification deficit is quantified.** ~43% today, ~1% only with ~18k measured
   points. "We can't verify string theory" becomes a number with a denominator.
3. **A falsifiable structural claim.** The learnability conjecture, attackable on small
   classes, whose false branch is a genuine negative result about landscape search.

*Docs:* [`docs/verification-formal.md`](docs/verification-formal.md) §10; [`docs/evolvability.md`](docs/evolvability.md) §6.

### 8. Discussion and limits

*The argument, made explicit so no one has to:* this framework **does not unify**. It
does not select a vacuum (L6 is untouched), does not eliminate oracle error (it bounds
it), does not assume `D` away (every certificate is conditional on it), and does not
turn a surrogate into truth (no certificate, no claim). Its real content is narrower and
more durable: it turns three ill-posed questions into well-posed ones, and it attaches a
number to the distance between "we believe" and "we verified."

*Docs:* [`docs/open-questions.md`](docs/open-questions.md) §6–§7; [`docs/educability.md`](docs/educability.md) §7.

### 9. Conclusion

*The closing argument:* the obstacle to unified string theory is not a shortage of
cleverness but a shortage of *checkable claims* — and the deepest checkable claim in
reach is not "is this vacuum ours?" but "is the map from compactification to observables
learnable?" Answer that, and you know whether the landscape is searchable at all.
Verification, done with Valiant's guarantees, is the honest first move; selection is the
hard second, and no amount of the first buys the second.

---

## Ledger: proven / conjectured / open

| Claim | Status |
|---|---|
| Two-level certificate bound (Theorem 2) | **derived** (standard concentration; PACLAND's composition) |
| Single-candidate verification needs no VC dimension | **derived** (Hoeffding on one proportion) |
| Search needs uniform convergence / VC·SQ dimension | **imported** (standard learning theory) |
| Evolvable ⇒ learnable | **imported** (Valiant 2009; Feldman 2008/09) |
| `SQdim(C) = O(poly(p))` | **conjecture** — the governing question |
| Measurable-physics bound (~43% today) | **derived** (given the finite-`D` and `m ~ 19` inputs) |
| Educability instantiation (assimilation rule) | **defined** (PACLAND's formalization of Valiant's concept) |
| Evolvability with imperfect performance oracle | **open** — the most publishable generalization |
| The landscape measure (selection) | **open** — physics, not ours to solve |

## References (standard; tools with URLs are in `docs/tooling.md`)

- Valiant, *A Theory of the Learnable*, CACM 27(11), 1984.
- Kearns, *Efficient noise-tolerant learning from statistical queries*, J. ACM 45(6), 1998.
- Valiant, *Evolvability*, J. ACM 56(1), 2009.
- Feldman, *Evolvability from learning algorithms*, STOC 2008; and *A complete characterization of statistical query learning…*, 2009.
- Valiant, *Probably Approximately Correct*, Basic Books, 2013.
- Valiant, *The Importance of Being Educable*, Princeton UP, 2024.
- Bousso & Polchinski, *Quantization of four-form fluxes…*, JHEP, 2000.
- Douglas, *The statistics of string/M theory vacua*, JHEP, 2003.
- Susskind, *The anthropic landscape of string theory*, 2003.
- Ooguri & Vafa, *On the geometry of the string landscape and the swampland*, 2007.
- He, *Deep learning the geometry of Calabi-Yau…*, 2017 (and the subsequent neural-metric line).
- **Tools and prior art with verified URLs:** [`docs/tooling.md`](docs/tooling.md) — CYTools, cymetric, cohomCalg, the Kreuzer–Skarke census, and the ML-for-the-landscape literature.

## Next steps

1. **Make the CYTools adapter real** — install `cytools`, confirm the API in
   `CyToolsAdapter`, generate the discrete half of the genotype (`docs/tooling.md`).
2. **Exact-background benchmark** — run the certificate loop on `exact_toric_oracle`
   (build #2 seed) end to end before trusting any approximate oracle.
3. **Empirical attack on the conjecture** — measure (or bound) the SQ dimension on a
   tiny flux subclass, once CYTools supplies real flux-vacua samples.
