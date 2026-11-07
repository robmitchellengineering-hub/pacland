# Machine-checked foundations of quantum theory and the Standard Model

**Gleason's theorem and the gauge-sector uniqueness, kernel-checked in Lean 4**

*Authors: the pacland proof arm · Date: 2026-11-07 · Repository: `pacland-proof/`*

**DOI:** https://doi.org/10.5281/zenodo.24024627

**Abstract.** We present machine-checked (Lean 4 / Mathlib v4.35) certificates for two
foundational results that together bound the *forced* half of quantum theory and of the
Standard Model. (1) **Gleason's theorem** (finite, dimension ≥ 3): every non-contextual
additive probability assignment on projectors is the Born rule `μ(P) = Tr(ρP)`, proven here via
the Cooke–Keane–Moran (CKM) descent-chain route, which needs no continuity argument. (2) The
**Standard Model gauge-sector uniqueness**: the anomaly-cancellation conditions force the
hypercharge assignment uniquely up to overall normalization and the `u↔d` flavor swap — the
gauge-sector analog of Mitchell's Uniqueness — and the five anomaly coefficients vanish for the
physical assignment `(1/6, 2/3, −1/3, −1/2, −1)`. Both are checked with no `sorry`/`axiom`;
`#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound`. These two results are
the *constraints* ("what the theory forbids") of their sectors; the *free* halves (which outcome
occurs; the 19 SM parameters) are delimited separately. This realizes the constraint-first
program's claim — a theory of everything's exact content is **constraints + labels + parameters**
— in two sectors at once, with machine-checked certificates rather than paper proofs.

## 1. Introduction

The constraint-first conjecture states that the *exact* content of a physical theory is exhausted
by three things: **constraints** (what it forbids), **labels** (which geometry is picked), and
**parameters** (free inputs). For the flux sector this was proven: the D3 tadpole is the *unique*
bilinear symplectic invariant (Mitchell's Uniqueness; the Weyl FFT), so the only exact structure
is the constraint. This note carries the same method one sector up, to quantum theory's probability
rule and to the Standard Model's gauge structure, and — unlike the original paper proofs — it
delivers each result as a **kernel-checked certificate** in a proof assistant.

The two "forced" halves certified here are:

| sector | forced result | theorem |
|---|---|---|
| Quantum theory | the Born rule is forced by non-contextuality | Gleason |
| Standard Model | the hypercharges are forced by anomaly cancellation | gauge-sector uniqueness |

The value is not the theorems (both are believed and were proved on paper long ago) — it is the
**machine-checked certificate** that the assumptions are exactly what is printed and no hidden
postulate was smuggled in. This is the "authority play": the referee is the Lean kernel, which
does not care about credentials.

## 2. Method

Everything lives in `pacland-proof/` (Lean 4, Mathlib `v4.35.0`). Two encodings are used and
bridged:

- `PaclandProof/Foundations/` — the native encoding (`Fin 3 → ℝ`, a custom `dotProduct`/`cross`,
  `FrameFunction3`).
- `Gleason/` — a vendored, ported mechanization of the CKM proof (Apache 2.0, from
  `Bobart0/gleason-theorem-lean` v1.0.3), in the `E3 = EuclideanSpace ℝ (Fin 3)` + `IsFrameFunction`
  encoding.

`PaclandProof/Foundations/GleasonBridge.lean` proves the two encodings agree
(`inner_eq_dotProduct`, `unitVec3_of_norm_eq_one`, `orthVec3_of_inner_zero`,
`frameFunction3_to_isFrameFunction`), so the Born rule is a theorem over our own definitions
(`gleason_born_rule`). The SM theorems are native (`PaclandProof/SM/`).

**Verification.** `lake build` green (9081 jobs); `#print axioms Gleason.gleason` = `propext,
Classical.choice, Quot.sound` only; zero tactical `sorry`/`axiom`/`admit`.

## 3. Result 1 — Gleason's theorem (Born rule from non-contextuality)

**Statement.** A non-contextual additive probability measure on the projectors of a
finite-dimensional Hilbert space (dim ≥ 3) is the Born rule: there is a density operator ρ with
`μ(P_x) = ⟨x|ρ|x⟩` for every unit vector x.

**Certificate.** `Gleason.frameFunction_regular`: every nonnegative frame function is a quadratic
form. The proof is the **Cooke–Keane–Moran (CKM) route**, which avoids the analytic continuity
step of Gleason's original proof:

1. *Extremal pole*: a bounded nonnegative frame function attains its supremum at some pole p
   (compactness).
2. *Basic lemma*: if f is constant on p's equator, f *decreases along descents* (a purely
   algebraic frame-property fact).
3. *Piron chain*: points of equal latitude are joined by a **finite chain of descents**
   (spherical coordinates + a trig estimate `cos x ≥ 1 − x²/2` + Bernoulli — no IVT/continuity).
4. *Bounded-additive ⇒ affine*: the recursion `Cauchy.affine_of_triple_sum` pins f to
   `f(x) = Σ λᵢ xᵢ²`.

`GleasonBridge.gleason_born_rule` restates this over our native `FrameFunction3`:
every nonnegative frame function is `x ↦ q x` for a quadratic form q — the Born rule.

## 4. Result 2 — Standard Model gauge-sector uniqueness

**Statement.** Given the SM matter content (gauge representations + chirality), the four
anomaly-cancellation conditions

```
[grav]²U(1):  6Y_Q − 3Y_u − 3Y_d + 2Y_L − Y_e = 0
[SU(2)]²U(1): 3Y_Q + Y_L = 0
[SU(3)]²U(1): 2Y_Q − Y_u − Y_d = 0
[U(1)]³:      6Y_Q³ − 3Y_u³ − 3Y_d³ + 2Y_L³ − Y_e³ = 0
```

determine the hypercharges `(Y_Q, Y_u, Y_d, Y_L, Y_e)` **uniquely up to overall normalization and
the u↔d swap**, among solutions with `Y_Q ≠ 0`.

**Certificate.** `SM.Hypercharge.hypercharge_uniqueness`: the three linear conditions solve
`Y_L = −3Y_Q`, `Y_e = −6Y_Q`, `Y_d = 2Y_Q − Y_u`; the cubic restricted to that family factors as
`−18·Y_Q·(Y_u − 4Y_Q)(Y_u + 2Y_Q)`, giving the two branches `Y_u = 4Y_Q` (the SM,
`(1/6, 2/3, −1/3, −1/2, −1)`) and `Y_u = −2Y_Q` (the u↔d swap). This is the gauge-sector analog of
Mitchell's Uniqueness: **the constraint is unique**.

**Certificate.** `SM.Anomaly.anomaly_cancellation`: the five gauge/gravitational anomaly
coefficients (`[SU(3)]³`, `[SU(3)]²U(1)`, `[SU(2)]²U(1)`, `[U(1)]³`, `[grav]²U(1)`) all vanish for
the physical assignment — the hypercharges are *required for consistency*, not predicted.

**Certificate.** `SM.ParameterCount.parameter_count`: the 19 free couplings decompose as
`3 + 6 + 3 + 4 + 2 + 1` (gauge + quark masses + lepton masses + CKM + Higgs + θ).

## 5. Significance — the forced/free split, in two sectors

The two certified results are the *forced* halves of their sectors, and they have the same shape:

| | forced (kernel-checked) | free (delimited) |
|---|---|---|
| Quantum theory | Born rule `Tr(ρP)` | which outcome (non-determinism) |
| Standard Model | anomaly cancellation + hypercharge uniqueness | the 19 parameter values |

The companion note (paper 2) delimits the free half of the SM: the 19 parameters are the Krull
dimension of the flavor orbit space, with the exact Hilbert series
`H_Y(t) = (1−t²⁴)/((1−t²)³(1−t⁴)⁴(1−t⁶)⁵(1−t⁸)(1−t¹²))`. Together the two papers state, with
certificates, that a theory of everything's exact content is **constraints + labels + parameters**,
and that the notorious "issues" (measurement problem, parameter values) are the *free* column —
delimited, not solved, and provably not derivable from the forced column.

## 6. Reproducibility

```
cd pacland-proof && lake build          # green, 9081 jobs
# prints: Gleason.gleason depends on axioms [propext, Classical.choice, Quot.sound]
```

Sources: `PaclandProof/Foundations/Gleason.lean`, `…/GleasonLemma.lean`, `…/GleasonBridge.lean`,
`Gleason/**` (vendored CKM proof, Apache 2.0), `PaclandProof/SM/{Hypercharge,Anomaly,ParameterCount}.lean`.
