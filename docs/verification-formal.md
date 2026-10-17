# L3 formalization — the two-level Valiant certificate

This is the rigorous companion to [`verification.md`](verification.md). It turns the
loose statement into bounds you could actually implement and, more importantly, compute
costs from.

Status: draft math, not yet peer-reviewed. Assumptions are named in §9.

---

## 1. Notation

| Symbol | Meaning |
|---|---|
| `X` | Instance space — the set of observables |
| `D` | Probability measure over `X` (the observable measure) |
| `c* : X → Y` | Target concept — true low-energy physics of our universe |
| `Ô : X → Y` | Oracle (L2) — approximate solver |
| `h : X → Y` | Candidate hypothesis — a vacuum's predicted observables |
| `g(x) = |h(x) − Ô(x)|` | Candidate-vs-oracle disagreement (measurable) |
| `e(x) = |Ô(x) − c*(x)|` | Oracle error (unknown, to be bounded) |
| `ε` | Tolerance — how close counts as "matches" |
| `β` | Oracle-bias threshold — "error above β counts as an oracle failure" |
| `p_g(τ) = Pr_{x~D}[g(x) > τ]` | Disagreement rate of `h` vs oracle above `τ` |
| `p_e(β) = Pr_{x~D}[e(x) > β]` | Oracle exceedance rate above `β` |
| `p_* = Pr_{x~D}[|h(x) − c*(x)| > ε]` | **The target** — true error of `h` against reality |

## 2. The target, and why it decomposes

We want to certify `p_* ≤ δ`. We can never observe `p_*` directly, because `c*` is only
reachable through the imperfect oracle `Ô`. The triangle inequality does the split:

```
|h(x) − c*(x)|  ≤  |h(x) − Ô(x)| + |Ô(x) − c*(x)|  =  g(x) + e(x)
```

Therefore, if `|h(x) − c*(x)| > ε`, then `g(x) + e(x) > ε`, which implies at least one of

```
g(x) > ε − β      or      e(x) > β
```

for any chosen split point `β ∈ (0, ε)`. Taking probabilities (a union bound):

```
p_*  ≤  p_g(ε − β)  +  p_e(β)          (⋆)
```

Both terms on the right are now *estimable*, for different reasons:

- `p_g(ε − β)` compares two things we can both **compute** (`h` and `Ô`) — estimate by
  sampling observables.
- `p_e(β)` is the oracle's own failure rate — estimate by **validating the oracle** on
  points where `c*` is known (measurement or exact computation).

This is the whole trick: decompose an unknowable quantity into two knowable ones.

---

## 3. Single-candidate verification — no learnability needed

For a **fixed** hypothesis `h`, `p_g` is a single Bernoulli rate. Sample `n` observables
`x₁…xₙ ~ D` i.i.d., compute the empirical disagreement rate

```
p̂_g  =  (1/n) Σᵢ  1[ g(xᵢ) > ε − β ]
```

A one-sided Hoeffding bound gives, for every `δ_s ∈ (0,1)`:

**Theorem 1 (candidate bound).** With probability ≥ `1 − δ_s`,

```
p_g(ε − β)  ≤  p̂_g  +  sqrt( ln(1/δ_s) / (2n) )
```

No VC dimension, no learnability assumption — this is just concentration on a single
proportion. **Verifying what you are handed is cheap.** The cost is `n`, and it is
explicit: the confidence radius shrinks like `1/√n`.

---

## 4. The oracle-error model and its validation (meta-PAC)

`p_e(β)` is the probability the oracle is wrong by more than `β`. We do not know it, so
we *learn* it — and that learning is itself a PAC statement.

**Validation set.** Collect `m` observables `z₁…zₘ` where `c*(z)` is known from an
independent trusted source (direct measurement, or exact computation on a tractable
case). Compute the empirical oracle-exceedance rate

```
p̂_e  =  (1/m) Σⱼ  1[ |Ô(zⱼ) − c*(zⱼ)| > β ]
```

The same one-sided Hoeffding bound gives, with probability ≥ `1 − δ_e`:

```
p_e(β)  ≤  p̂_e  +  sqrt( ln(1/δ_e) / (2m) )          (Theorem 1′)
```

This is **meta-PAC**: the oracle's reliability is itself a hypothesis we verify
probably-approximately-correctly, on a *different* distribution than the candidate is
sampled from.

### The binding constraint

`m` is **not** bounded by compute — it is bounded by *physics*. There are only ~19 free
Standard-Model parameters plus cosmological parameters, and only one universe to measure
them in. So in practice `m` is small, `p̂_e` is coarse, and the oracle-validation radius
`sqrt(ln(1/δ_e)/(2m))` is the **dominant** term in the certificate — not the candidate
sampling term. The honest bottleneck of the whole system is: *how many points of the
true theory can we actually measure?*

---

## 5. The two-level theorem (the certificate)

**Theorem 2 (two-level Valiant certificate).** Fix `ε > 0`, split point `β ∈ (0, ε)`,
and confidence budgets `δ_s, δ_e ∈ (0,1)`. Independently:

- sample `n` observables for the candidate (as in §3), and
- sample `m` observables for oracle validation (as in §4).

Then with probability at least `1 − δ_s − δ_e`:

```
p_*  =  Pr[ |h(x) − c*(x)| > ε ]
     ≤  p̂_g  +  p̂_e  +  sqrt( ln(1/δ_s)/(2n) )  +  sqrt( ln(1/δ_e)/(2m) )
```

That is: the true error of the candidate against reality is bounded by a sum of **four
terms** — two empirical rates and two confidence radii — with the total confidence
composed by the union bound over the two independent failure events.

**The certificate** is the tuple

```
(ε, β, n, m, p̂_g, p̂_e, δ_s, δ_e)
```

from which the bound above is computed. This is what L3 emits.

---

## 6. Verify vs search — where the VC dimension actually enters

The bound above is for **one fixed `h`**. The search (L4) is different: it picks the
*empirically best* of many hypotheses, and that selection is biased — the empirical
minimum overestimates how good the winner really is.

- **Finite class**, `|C|` hypotheses evaluated: a union bound over all `|C|` gives
  confidence radius `sqrt( ln(|C|/δ)/(2n) )` — each extra hypothesis costs `log |C|`
  samples.
- **Infinite class**: `log |C|` is replaced by `VCdim(C) · log(1/ε)` (up to constants),
  the standard uniform-convergence bound.

So the governing question from `verification.md` belongs **here**, to the search, not to
single-candidate verification:

> Search over class `C` with tolerance `ε` and confidence `δ` needs
> `n ≳ (VCdim(C) / ε²) · log(1/δ)` samples per generation.

The consequence for the architecture is important and worth stating plainly:

- **If the learnability conjecture is FALSE** (`VCdim(C)` astronomical), then L4 — the
  *search* — is infeasible, **but L3 survives**. You can still verify any candidate you
  are handed (e.g. proposed by a human, or by another theory), because §3–§5 never
  invoke `VCdim`.
- The system degrades gracefully from "search + verify" to "verify only." That is the
  honest fallback position.

---

## 7. The learnability conjecture, stated formally

Let `V` be a fixed vacuum class (e.g. IIB orientifold flux vacua on Calabi-Yau
threefolds with tadpole bound `L`, per `encoding.md`), and let

```
C = { h_v : X → Y  :  v ∈ V }
```

be the class of observable-prediction functions induced by those vacua.

**Conjecture (bounded VC dimension).** `VCdim(C) = O(poly(p))`, where `p` is the number
of effective parameters (flux quanta + moduli) in the encoding — i.e. the dimension
grows polynomially, not exponentially, in the description length.

- **True** ⇒ `C` is efficiently PAC-learnable ⇒ by Valiant's evolvability theorem
  (*evolvable ⇒ learnable*), `C` is **evolvable** — L4's evolutionary search navigates
  the landscape with provable guarantees.
- **False** ⇒ no efficient search (evolutionary or otherwise) can reliably find the
  target vacuum. A negative result about the landscape program — and one that is
  *testable on small subclasses first*.

The conjecture is deliberately stated so it can be attacked empirically on the IIB flux
corner without ever touching 10⁵⁰⁰.

---

## 8. Worked example (toy numbers)

*(The finite-`D` version that supersedes the illustrative `n` below is in
[`observable-measure.md`](observable-measure.md) §5–§7 — for a finite observable set the
sampling term vanishes and the oracle-validation term dominates.)*

Goal: a certificate at total confidence 95%, tolerance `ε = 0.01`, split point
`β = 0.002`, split the confidence budget evenly `δ_s = δ_e = 0.025`.

- **Candidate sampling.** For a confidence radius ≤ `0.005`:
  `ln(1/0.025) ≈ 3.69`, so `2n ≥ 3.69 / 0.005² = 147,600` ⇒ **`n ≈ 74,000`** oracle
  evaluations. Explicit, affordable-in-principle, and *per candidate*.
- **Oracle validation.** The same radius needs **`m ≈ 74,000`** points where `c*` is
  *known*. This is **not** affordable — it exceeds the ~19 measurable SM parameters by
  four orders of magnitude. Hence the validation term dominates and the certificate is
  only as good as the (tiny) validation set.

The example's lesson: the framework converts "how much does verification cost" into a
number, and that number is dominated by *measurable physics*, not compute. If you want a
tighter certificate, you need more *known* points of the true theory — which is exactly
the thing string theory does not currently give us enough of.

---

## 9. Assumptions (named, not hidden)

1. **`D` exists and is chosen.** The observable measure is stipulated (§4 of
   `open-questions.md`). Every certificate is relative to `D` and must say so.
2. **`e(x)` and `g(x)` are treated as rates over `D`.** The oracle error is folded into
   a failure rate `p_e(β)` rather than a per-point guarantee. If the oracle is
   adversarially correlated with `D`, the bound is vacuous — this is the imperfect-oracle
   gap (open question #3).
3. **Validation distribution ≈ target distribution.** §4 assumes the `m` points where
   `c*` is known are drawn from `D`. They are not (they are drawn from "what we can
   measure"). The resulting distribution shift adds an unmodeled term; see
   `open-questions.md` §4 and §7.
4. **Independence.** The `n` candidate samples and `m` validation samples are
   independent, so the union bound in Theorem 2 is valid.
5. **Hoeffding is used, not Clopper–Pearson.** The one-sided Hoeffding radii are simple
   and slightly conservative; exact binomial intervals tighten them for small `n`, `m`.

## 10. What this buys

- A certificate that is **computable from quantities we can actually measure** (`p̂_g`,
  `p̂_e`) plus declared budgets (`ε, β, δ_s, δ_e`).
- An explicit cost model: `n` per candidate, `m` per validation, with `m` the real
  bottleneck.
- A clean separation of the **verification** problem (Theorem 1, no VC dimension) from
  the **search** problem (§6, VC dimension) — which is what makes the learnability
  conjecture a *search* conjecture, not a *verification* conjecture.
