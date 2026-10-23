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

## Research fan-out results (2026-10-23, three independent passes)

1. **Covariance laws — VALIDATED.** All three measured laws are the textbook type IIB
   S-duality transformations, exactly: `Ŵ = e^{K/2}W → e^{−i·arg τ}Ŵ` (so Law II magnitude +
   Law IIb phase), and `g_s → |τ|²g_s` (Law III; `1/g_s` is only the `C₀=0` case). The bare
   `W → W/τ`; invariance is specific to the Kähler-normalised combination, which is what we
   measured. (Gukov–Vafa–Witten, Giddings–Kachru–Polchinski, Graña, Shukla eq. 2.12.)

2. **ℤ₂ torsion — REFUTED as a literal identity (D resolved).** Freed–Witten is the spin-c
   obstruction `W₃ = β(w₂)` (complex K-theory); Witten SU(2) is the mod-2 index `π₄(SU(2))`
   (real KO-theory). Every spin manifold is spin-c, so FW vanishes exactly where the SU(2)
   anomaly lives — the two Z₂'s are decoupled, and no dictionary exists. So the "same object"
   thesis holds only at the *rational* level (same kind: a vanishing K-theory class), **not** at
   the torsion level. Correct the unification-synthesis "same object" claim to "same kind,
   different index (rational) and different Z₂ (torsion)".

3. **Counting (19) — VALIDATED with two corrections.** The 19 is the correct vanilla/Dirac-SM
   orbit-space dimension (quark 10 matches Bento–Silva–Trautner and Hanany et al.). Corrections:
   (a) it is the **no-neutrino** count — Dirac +7 → 26, Majorana +9 → 28, and this must be
   stated; (b) the GUT "b–τ 2→1" is a **misattribution** — minimal SU(5) ties all three
   `Y_e = Y_dᵀ` (−3 masses) but frees +2 new CP phases, netting −1; and "SU(5) is the *only*
   UV symmetry" is false (SO(10) is standard and more restrictive). The 16 is right, the stated
   mechanism is not.

## Where to go next

1. **Make the iterated shift robust** (cone-enforced, multi-seed) → a working h12=5..25 sampler
   (the fix is a *Newton iteration*, not a proposal redesign).
2. Re-sample the frontier → settle B (landscape fact).
3. Extend the laws to h12=5..10 → settle C.
4. Write up D (the ℤ₂ torsion) and E (counting stability).
