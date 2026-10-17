# The observable measure D — a toy definition

This makes the certificate in `verification-formal.md` concrete. `D` is the measure
over observables that defines what "close to our universe" *means*; until it is pinned
down, every certificate is abstract. Here it is pinned down for a toy case — and the
act of pinning it down changes the worked example's conclusion.

Status: draft, for a toy case. The exact observable list and weights are a *scientific
commitment* to be settled with the physics community, not a technical default.

---

## 1. Design principles

1. **Finite support.** `X` is a finite, named list of observables — not a continuum. A
   finite set makes `D` a weight vector and makes the error rate directly computable.
2. **Dimensionless.** Every observable is a dimensionless ratio, so "tolerance `ε`" means
   the same thing across all of them. You cannot mix `α_s ≈ 0.1` with `Λ ~ 10⁻¹²²`
   without a shared scale.
3. **Log-space.** Each observable is represented as its natural logarithm. Then
   "disagreement > ε" means "multiplicative disagreement > e^ε ≈ 1 + ε". This makes a
   1% tolerance uniformly meaningful from the fine-structure constant down to Λ.

## 2. The log-space convention

For an observable `o` (a positive dimensionless quantity), the representation is
`ℓ = ln o`. The disagreement metric between a candidate's prediction `h` and the target
`c*` is

```
|ℓ(h) − ℓ(c*)|  =  |ln( h / c* )|
```

- `ε = 0.01` ⇒ "within ~1% multiplicatively" (`e^0.01 ≈ 1.01005`).
- Λ in Planck units (`ln Λ ≈ −281`) and a gauge coupling (`ln α ≈ −5`) now sit on the
  same footing: a 1% log-error is the same statement about both.

## 3. The toy observable set

Ten observables, chosen to span the hard cases (couplings, hierarchies, mixing, Λ) while
staying dimensionless. Target values are **illustrative** (order-of-magnitude correct,
not authoritative).

| # | Observable | `ℓ = ln o` (target, approx) | Computable by oracle? |
|---|---|---|---|
| 1 | `α_s(M_Z)` strong coupling | −2.14 | easy |
| 2 | `α_em(M_Z)` EM coupling | −4.85 | easy |
| 3 | `m_t / m_Z` top mass ratio | +0.64 | easy |
| 4 | `m_b / m_t` bottom/top | −3.72 | medium |
| 5 | `m_μ / m_τ` muon/tau | −2.82 | medium |
| 6 | `m_u / m_d` up/down | −0.75 (uncertain) | hard |
| 7 | `θ_C` Cabibbo angle | −1.49 | medium |
| 8 | `sin²θ_W(M_Z)` Weinberg angle | −1.46 | easy |
| 9 | `m_H / m_Z` Higgs mass ratio | +0.32 | hard |
| 10 | `Λ · M_Pl⁻⁴` cosmological constant | −280.9 | hardest |

Two features of the table matter more than the numbers:

- **Computability is heterogeneous.** The oracle can evaluate some observables reliably
  (couplings) and others barely at all (Λ needs full moduli stabilization). This
  asymmetry drives §6.
- **The target is not always a point.** `m_u/m_d ≈ 0.47` carries an experimental
  uncertainty of ~±0.06 — `c*` is itself fuzzy for some observables. See §8.

## 4. The weight vector

`D` assigns a weight `w_i` to each observable, `Σ w_i = 1`. Default (and placeholder):
**uniform**, `w_i = 1/10`.

What the weights encode is the real scientific content, and it must be said out loud:

- Uniform weights treat "1% wrong on the up-quark mass" as equal to "1% wrong on Λ".
- Weighting Λ at, say, `w = 1/2` would make the certificate dominated by the one number
  string theory is least able to compute — which may be the *correct* commitment, but it
  must be chosen, not assumed.

The rule: **every certificate states its `D`**, because a vacuum is only "(ε,δ)-close"
*under a named observable measure*.

## 5. The finite-set insight: sampling collapses

This is the payoff of going finite. With `N = 10` observables and an oracle that can
evaluate all of them, the candidate-vs-oracle disagreement rate is **exact** — no
sampling, no `n`, no Hoeffding:

```
p_g(ε − β)  =  Σ_i  w_i · 1[ |ln(h(x_i)/Ô(x_i))| > ε − β ]
```

The "`n = 74,000` samples" from `verification-formal.md` §8 was a red herring: for a
finite, fully-computable observable set, the *candidate-sampling* term vanishes because
you compute the whole sum, not a sample of it.

So the certificate collapses to

```
p_*  ≤  p_g(exact)  +  p̂_e  +  sqrt( ln(1/δ_e) / (2m) )
```

where `m` is the number of observables with a *measured* target `c*`. **The only
remaining uncertainty is the oracle-error term — and it is bounded by `m`, the number of
measured points, not by compute.**

## 6. Computable vs measurable — the 2×2 that decides everything

| | `c*` known (measured) | `c*` unknown |
|---|---|---|
| **Ô can compute** | **verification zone** — contributes to the certificate | prediction zone — falsifiable *later*, contributes nothing *now* |
| **Ô cannot compute** | unverifiable | — |

Only the top-left cell tightens the certificate. The top-right cell is where a vacuum's
*content* lives (novel predictions), but it cannot reduce today's uncertainty. A vacuum
whose only interesting predictions are in the top-right cell is — under this framework —
**scientifically sterile today**, regardless of how elegant it is.

## 7. The worked example, corrected

With `N = 10` computable observables and `m = 10` measured targets, `δ_e = 0.025`:

```
oracle-validation radius  =  sqrt( ln(1/0.025) / (2·10) )
                          =  sqrt( 3.689 / 20 )
                          ≈  0.43
```

A **43%** confidence radius. The certificate is effectively vacuous — and the framework
*tells us so, with a number*. The honest conclusion of the toy case:

> To drive the oracle-error radius below 1% at 97.5% confidence, you need
> `m ≈ 18,000` *measured* points of the true theory — four orders of magnitude more than
> the ~19–25 free parameters the Standard Model actually gives us to measure.

This is the quantitative statement of the deficit that has been implicit since the first
message: **the framework's value is not that it solves unification, but that it turns
"how far are we from being able to verify any of this" into a number.** Verification is
bounded by *measurable physics*, not by compute.

## 8. The caveats, named

1. **`D` is stipulated, not derived.** The weight vector is a choice (open question #4 of
   `open-questions.md`). The correct response to this is not to hide it but to make
   every certificate conditional on it.
2. **`c*` is not a point.** Some targets are experimental values with error bars
   (`m_u/m_d`), some are inferred from other measurements (indirect), and the
   measurement distribution is *not* `D` — it is "what the one universe lets us
   measure." This is the distribution-shift assumption of `verification-formal.md` §9.3.
3. **Computability ≠ correctness.** "Ô can compute" says nothing about how wrong it is;
   the per-observable error model (§6 of `encoding.md`, and the L2 spec yet to be
   written) is what feeds `p̂_e`.
4. **Finite ≠ complete.** Ten observables are a toy. The real list is longer but still
   finite and still small (~tens), so the finite-set conclusion (§5) is robust — it is
   the *smallness of `m`*, not the toy, that drives the 43%.

## 9. Open items

1. **Fix the real observable list and weights** with domain input — this is a physics
   decision, the single most consequential "spec choice" the project will make.
2. **Per-observable oracle error models** — the L2 contract that turns "computable" into
   a `p̂_e` term per observable.
3. **Target fuzziness** — extend the certificate so `c*(x)` is an interval, not a point,
   for observables with experimental error (a third layer of uncertainty alongside
   sampling and oracle error).
4. **The top-right cell** — decide whether a vacuum's *future* falsifiability (prediction
   zone) should carry any weight today. The framework currently says no; that is a
   stance, not an oversight, and it should be defended or changed explicitly.

## 10. One-sentence summary

`D` is a finite, log-space, weighted list of dimensionless observables; making it finite
collapses the sampling term and reveals that verification is bounded by the number of
*measurable* points of the true theory — which today is ~19, and therefore the current
certificate radius is ~43%, not ~1%.
