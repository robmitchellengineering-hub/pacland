# Probably Approximately Correct String Theory: A Verification Discipline for the Landscape

**Rob Mitchell**

*PACLAND · github.com/robmitchellengineering-hub/pacland*

---

## Abstract

The string landscape contains on the order of 10⁵⁰⁰ vacua, and no experiment
distinguishes most of them, so "unified string theory" is two conflated problems —
*verification* (does some vacuum match our universe?) and *selection* (why that one?).
We separate them, and build a **verification discipline** for the first: a
probably-approximately-correct certificate that bounds a candidate's error even when
the verifier is itself approximate (Theorem 2), a proof that search over the flux
superpotential is **not evolvable** (Denef–Douglas uniformity + Valiant's contrapositive,
measured on 380 real SUSY vacua), a **measured** log-uniform prior for |W₀| (CDF
linearity R² = 0.92), a certified **Mitchell Verification Deficit** that is total today (m = 0
validated oracle outputs), and a **boundary map** — a taxonomy of the four senses in
which the problem is "uncomputable," each with its certified positive remainder. We do
not claim to select the vacuum. We claim something narrower and we believe more useful:
*the field currently has no verification layer for its unverifiable theory, and this is
one.*

---

## 1. Introduction

String theory is not a single theory but a family of ~10⁵⁰⁰ metastable vacua — the
*landscape* [1,2,3]. "Unified string theory" decomposes into two claims the literature
habitually fuses: **verification** (there exists a vacuum matching our universe) and
**selection** (a measure singles it out). The first is checkable in principle; the
second is the open measure problem. This paper concerns the first, and does so
rigorously.

Two facts make verification hard. First, the search space is astronomically large.
Second, and more fundamentally, the *verifier is not ground truth*: the map from a
compactification to its low-energy observables is computed by an approximate solver,
with systematic error from α′ corrections, non-perturbative truncations, and the
Kaluza–Klein tower. Any rigorous statement about verification must contend with an
*imperfect labeler*.

We import the framework built for exactly this regime — Valiant's
probably-approximately-correct (PAC) learning [4] — and apply it to verification
itself. The result is a certificate whose two error terms are separately estimable,
three consequences (a verify/search separation, a necessary-condition conjecture, and a
measurable-physics bound), and, on running the machinery against real data, a set of
empirical findings summarized in the abstract.

**Field context.** Independently of us, the field is converging on verification from
three directions: Michael Douglas is formalizing QFT in Lean 4 [13]; PhysProver is the
first LLM theorem-prover for physics [14]; and a 2025 line formalizes *falsification*
targets at a collider [15]. Our contribution is the complementary angle: guards,
certificates, and measured limits — verification for the regime where ground truth is
absent.

## 2. The two-level certificate

Let X be the observable space, D a measure over X, c\* : X → Y the target (our
universe's true physics), and h : X → Y a candidate's prediction. We observe c\* only
through an approximate **oracle** Ô. Define

```
g(x) = |h(x) − Ô(x)|,     e(x) = |Ô(x) − c*(x)|,
```

and the true error

```
err_D(h) = Pr_{x ~ D}[ |h(x) − c*(x)| > ε ].
```

The triangle inequality splits the unobservable error into two estimable pieces, and a
union bound gives, for any β ∈ (0, ε),

```
err_D(h)  ≤  p_g(ε − β) + p_e(β),                                   (⋆)
```

where p_g(τ) = Pr[g > τ] and p_e(β) = Pr[e > β]. The two terms are *separately
estimable*: p_g compares two things we can both compute (h and Ô), while p_e is the
oracle's own failure rate, estimated by validating Ô on points where c\* is known.

**Theorem 1 (candidate bound).** *For fixed h, with n samples x₁…x_n ~ D and empirical
disagreement rate p̂_g, with probability ≥ 1 − δ_s:*

```
p_g(ε − β)  ≤  p̂_g + sqrt( ln(1/δ_s) / (2n) ).
```

**Theorem 1′ (oracle bound).** *On m points where c\* is known, with empirical
exceedance p̂_e, with probability ≥ 1 − δ_e:*

```
p_e(β)  ≤  p̂_e + sqrt( ln(1/δ_e) / (2m) ).
```

**Theorem 2 (two-level Valiant certificate).** *With probability ≥ 1 − δ_s − δ_e:*

```
err_D(h)  ≤  p̂_g + p̂_e + sqrt( ln(1/δ_s)/(2n) ) + sqrt( ln(1/δ_e)/(2m) ).
```

The certificate is the tuple (ε, β, n, m, p̂_g, p̂_e, δ_s, δ_e). This is verification in
the presence of an imperfect labeler — the generalization of PAC's clean oracle that
string theory actually requires.

## 3. Verification without learnability; search with it

Theorem 2 never invokes the complexity of the hypothesis class: **verifying what you are
handed is cheap**, a Bernoulli-rate estimate. *Search* is different — it selects the
empirically best of many hypotheses, which is biased, and bounding the bias needs
uniform convergence (VC dimension, or the statistical-query dimension SQdim). The
consequence is a graceful-degradation statement: if search is infeasible, the verifier
survives and can still certify any externally proposed candidate.

## 4. The measurable-physics bound, and the total deficit

Make D **finite**: X is a finite list of N log-space observables. Then the candidate term
is *exact* — no sampling:

```
p_g(ε − β)  =  Σ_i w_i · 1[ |ln(h(x_i)/Ô(x_i))| > ε − β ],
```

and the certificate collapses to the oracle term alone, bounded by **m, the number of
validated oracle outputs** — observables that are simultaneously *measured* (c\* known),
*computable* (Ô evaluates them), and *validated* (Ô calibrated against c\*).

**The honest finding.** For our universe, c\* is known but Ô is not (the compactification
is unknown); for exact/tractable backgrounds, Ô is computable but they are not our
universe. The intersection — the true m — is **zero** today. With m = 0 the radius
sqrt(ln(1/δ_e)/(2m)) is **infinite**: the certificate is vacuous, and the verification
deficit is *total*, not "~31%" as an earlier conflation of "measured" with "validated"
suggested. The binding constraint is validated oracle outputs, not compute; each
observable that gains a calibrated error model moves m from 0 toward the ~10–19 targets
and shrinks the radius from ∞.

## 5. The negative result: W₀ is log-uniform, hence not evolvable

Denef–Douglas [6] shows the flux superpotential W₀ is statistically uniform in the
complex plane across the flux ensemble, so the map flux → W₀ carries ~zero mutual
information. We measured the distribution directly.

**Measurement.** 380 SUSY flux vacua, sampled by JAXVacua's natural (ISD) measure [11].
The empirical CDF of log|W₀| is linear to R² = 0.92 (the |W₀|² CDF is not, R² = 0.45):

| variable | CDF linearity R² |
|---|---|
| log\|W₀\| (log-uniform) | **0.923** |
| \|W₀\|² (area-uniform) | 0.450 |

So |W₀| is **log-uniform** — the standard KKLT prior, now measured rather than assumed.
(Uniform-in-a-box sampling does *not* reproduce this: R² ≈ 0.2–0.3 regardless of box
width; the natural measure is required.)

Valiant's evolvability theorem [5]: **evolvable ⇒ learnable.** A log-uniform (hence
zero-information) map is not learnable, hence — by the contrapositive — **not
evolvable**: no certificate-only evolutionary search over W₀ can converge. The
graceful-degradation statement of §3 applies: the *search dies, the verifier survives.*

A direct consequence, measured: P(|W₀| < 1) = **42.6%** (so "small W₀" eliminates ~57%,
not the ~95% that biased sampling suggested), while the KKLT target |W₀| ~ 10⁻⁴ lies
7.6 nats below the observed range — its tuning probability is an extrapolation the data
cannot confirm.

## 6. Empirical characterization: structure, constraints, uniformity

**Structure mining.** A non-linear miner (mutual information with permutation test, plus
a ridge-on-quadratic-features learnability test, self-validated on the deterministic
tadpole control at r = 0.99) finds no strong geometric fingerprint in the flux-sector
observables: W₀ random (ridge r = 0.10), g_s weakly structured (r = 0.21), the gauge
couplings at noise (r ≤ 0.17). The geometry-pinning structure, if it exists, lives in
the observables we have not yet computed (the full spectrum with instanton corrections).

**Constraint verification.** Treating constraints as certifiable statements — "this
constraint eliminates fraction p of the sampled vacua, with confidence 1 − δ" — we
measure, on the natural-measure sample:

| constraint | eliminates | 95% CI |
|---|---|---|
| weak coupling (g_s < 1) | 68.7% | [59%, 78%] |
| small W₀ (\|W₀\| < 1) | 57.4% | (measured) |

A single constraint eliminates a large, certified fraction; a chain of them narrows by
elimination, which is the search-free route the framework is designed for.

## 7. The boundary of the computable

The object we actually want — pin down the compactification — is uncomputable in several
distinct senses. The contribution of this paper is to *name* them and certify each as
data, so that "uncomputable" is a map, not a wall:

| sense | meaning | the move |
|---|---|---|
| **intractable** | answer exists, no feasible algorithm | prove intractability |
| **unmeasurable** | answer exists, data/ground-truth absent | compute the deficit |
| **underdetermined** | no unique answer exists | compute the set's invariants |
| **undecidable** | provably no algorithm | prove undecidability |

Seven questions are certified to date (search over W₀ = intractable; verify-today and
KKLT-tail and full-EFT and small-Λ = unmeasurable; the measure and the inverse problem
= underdetermined). **None is undecidable** — the landscape problem is an *epistemic*
and *underdetermination* limit, not a Turing limit. That is itself a finding: the path
forward is not "invent a faster computer" but "build the missing oracles" and "compute
the invariants of the underdetermined set."

## 8. Discussion and limits

**The framework does not unify.** It does not select a vacuum; the measure problem
remains open physics. It does not eliminate oracle error; it bounds it. Every
certificate is conditional on the stipulated observable measure D.

**What we do not claim.** No new prediction, no measure, no unique compactification. The
negative result is scoped to the IIB flux corner and to W₀ (g_s is weakly structured;
the full-spectrum observables are unmeasured). The log-uniform prior is measured over
3.7 nats; its extension to the KKLT tail is explicitly an extrapolation.

**What we do claim.** A verification discipline for a theory that currently has none: a
certified deficit, a mutation-tested computation vault, a measured prior, a negative
result, and a boundary map — built in the exact gap the field's leaders (Douglas [13],
PhysProver [14]) are independently formalizing. The two approaches — our
guard/certificate discipline and their Lean formalization — are complementary, not
competing.

## 9. Conclusion

The obstacle to unified string theory is a shortage of *checkable claims*, and the
deepest checkable claim in reach is not "is this vacuum ours?" but "is the
compactification→observables map learnable?" — answered negatively for W₀, and mapped
for the rest. Verification, done with Valiant's guarantees, is the honest first move;
the boundary map makes the *second* move (where does computation end?) equally honest.
We have not solved the theory. We have built, tested, and measured the missing
verification layer — and the field's convergence on the same gap suggests that is the
right thing to have built.

## References

[1] Bousso & Polchinski, *Quantization of four-form fluxes…*, JHEP 2000.
[2] Douglas, *The statistics of string/M theory vacua*, JHEP 2003.
[3] Susskind, *The anthropic landscape of string theory*, 2003.
[4] Valiant, *A theory of the learnable*, CACM 27(11), 1984.
[5] Valiant, *Evolvability*, J. ACM 56(1), 2009.
[6] Denef & Douglas, *Distributions of flux vacua*, hep-th/0404116.
[7] Kearns, *Efficient noise-tolerant learning from statistical queries*, J. ACM 45(6), 1998.
[8] Feldman, *A complete characterization of statistical query learning…*, FOCS 2009.
[9] Valiant, *Probably Approximately Correct*, Basic Books, 2013.
[10] Demirtas et al., *CYTools*, arXiv:2211.03823.
[11] Dubey, Krippendorf, Schachner, *JAXVacua*, arXiv:2306.06160.
[12] Kachru, Kallosh, Linde, Trivedi, *de Sitter vacua in string theory*, hep-th/0301240.
[13] Douglas et al., *Formalizing QFT in Lean 4*, arXiv:2603.15770.
[14] *PhysProver*, arXiv:2601.15737.
[15] *How to falsify string theory at a collider*, arXiv:2412.13192, PRR 2025.
