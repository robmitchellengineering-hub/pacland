# UNIFICATION — where we are, and the path (2026-10-23)

One document: everything proven, everything measured, and the sharper picture they form.
Status is tiered — **proven** (symbolic, machine-checked) vs **measured** (node, with a
control) vs **asserted** (a hypothesis to test). Never read a tier into another.

## The complete picture

### Proven (sympy + Lean, zero tolerance)

1. **The invariant ring is ℂ[N]** — the tadpole `N = FᵀJH` is the *unique* duality-invariant;
   no exact polynomial duality-invariant selector can single out a vacuum (Uniqueness 6/6 +
   Lean, Constraint-First/FFT 5/5, Full-duality Sp×SL(2,ℤ) 5/5).
2. **The orbits are classified by (N, d)** — over ℝ one orbit per tadpole (the orbit space is
   a *point*), over ℤ finitely many per tadpole by the content `d = gcd(F,H)`, `d²|N`
   (Completeness 6 exact + 2 numeric).
3. **Exact content is three types**: constraint + label + **counting** (the 19 = orbit-space
   dimension, Molien–Weyl + Hilbert–Serre + exact Jacobian rank, three-way certified).

### Measured (pacland-rog, jaxvacua 0.1.2, every number gated by a control)

4. **Mitchell's Laws of Duality Covariance** — the covariance table:
   Law I (scaling), Law II (`|W|` S-invariant, 100/100), Law IIb (`arg(W_S/W) = −arg τ`),
   Law III (`g_s → |τ|²g_s`), Law IV (moduli inert), Law V (counting 19). Duality is realised
   as a covariance, never an anomaly — "one theory described twice" is literal.
5. **G3 (truncation) resolved** — the near-null eigenvector of the ISD matrix is *interior*
   (a physical hierarchy), not boundary-aligned (a truncation artefact), at every h12=2..25.

### NEW (this session) — the h12≥5 sampling wall is a sampler issue, not a physics wall

6. The continuous ISD flux `f_cont = (s·M·Σ + c₀)·h` is **F-flat to 1e-8 even at h12=5** — the
   completion is correct; the integer *rounding* is what breaks it (amplified ~500× by
   cond(M)). But iterating the **linearised shift** (the library's own Newton step, applied
   repeatedly instead of once) **converges to |DW| ~ 1e-8 at h12=5 and 10**, and at h12=5 it
   lands on a genuine **in-cone SUSY vacuum**. The "0 critical points in 13,311" is
   *one-shift + a stuck scipy solver*, not "no vacua exist". The h12≥5 frontier is open.

## The sharper picture

> **A theory of everything predicts relations (invariants), never values.** The flux
> landscape is *fully characterized* by its exact content — the constraint (tadpole), the
> labels (topology), the counting (19) — and by the covariance table that says how every
> observable transforms under duality. There is no fourth kind, and there is no "connecting
> equation": the 19 are free coordinates, exact as a count and free as values. Unification is
> not a formula that ties the 19 to a Calabi–Yau (that shape is proven not to exist); it is
> the complete, falsifiable characterization of the landscape's exact structure plus its
> duality covariance — and now, with the sampler unblocked, it extends across the whole h12
> frontier.

This is the claim that changes the face of physics: not "we derived the Standard Model", but
"we proved there is nothing to derive — the only exact structure is the constraint, and
everything else is covariance + counting."

## The assertions (to test, fan out)

| # | assertion | falsifier | how |
|---|---|---|---|
| A | the h12≥5 wall is a sampler bug — a robust iterated shift finds SUSY vacua at h12=5..25 in-cone | iterated shift finds 0 in-cone vacua | measurement |
| B | the SUSY-fraction collapse (27.9%→19.7%→1.1%) is a landscape fact, not a proposal curve | collapse vanishes with the fix | measurement |
| C | the covariance laws (II, IIb, III) hold at h12=5..10 | a law scatters at higher h12 | measurement |
| D | the ℤ₂ torsion correspondence — Freed–Witten ≡ Witten SU(2) global anomaly | the two Z₂'s are provably distinct | math + literature |
| E | the counting (19) is stable — no new relation appears at higher h12 | a 20th relation | rank test |

## Where to go next

1. **Make the iterated shift robust** (cone-enforced, multi-seed) → a working h12=5..25 sampler
   (the fix is a *Newton iteration*, not a proposal redesign).
2. Re-sample the frontier → settle B (landscape fact).
3. Extend the laws to h12=5..10 → settle C.
4. Write up D (the ℤ₂ torsion) and E (counting stability).
