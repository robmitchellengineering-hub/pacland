# Solving string theory — the programme, specified

This is the founding specification. `docs/unification-claim.md` states *the claim*;
`docs/MITCHELLS-LAWS.md` records *the laws that hold*; this document states **what "solved"
means, what the objects are, and how each gap gets closed or falsified**.

---

## 1. The target, defined so it can be wrong

"Solving string theory" cannot mean "derive the 19 Standard-Model parameters from topology",
because this programme's own theorem rules that shape out: the flux sector's exact content is
the constraint `N = FᵀJH` and the topological labels, and **nothing else exact** exists
(Constraint-First 5/5 via Weyl FFT; Uniqueness 6/6 + Lean; Completeness 6 exact + 2 numeric).
Any target that ignores this is aimed at something provably not there.

**Definition — string theory is *solved* for a sector when:**

> **(a)** every exact invariant of that sector is enumerated and proven to generate the
> invariant ring; **(b)** every physical observable's transformation law under the duality
> group is known in closed form (the **covariance table**); and **(c)** a computable map
> assigns every low-energy parameter either to a **constraint/label** or to a **free
> coordinate**, with a certified error bound — the number of parameters certified in (c) is
> the Mitchell Verification Deficit **m**.

So "solved" is not a slogan and not a number: it is `(a) + (b) + (c)`, and `m` measures
progress along `(c)`. Today: `(a)` is **proven for the flux sector only**; `(b)` has **one
row** (Law II, S-invariance of `|W|`); `(c)` is **not started**. `m = 9`.

## 2. The three objects, and their exact status

| object | what it is | status |
|---|---|---|
| **the group** | `Sp(b₃,ℤ) × SL(2,ℤ)` acting on the flux pair and the axio-dilaton | **proven** — full-duality 5/5; S and T both preserve `N` by antisymmetry of `J` |
| **the invariant ring** | `ℂ[N]` — a single generator, the tadpole | **proven** — FFT 5/5 + Uniqueness 6/6 (+ Lean, general *n*) |
| **the orbits** | over ℝ, transitivity on each tadpole level set (**one orbit per tadpole**); over ℤ, finitely many, labelled by `(N, d)` | **proven** — Completeness. **Note the consequence: the orbit space is a point per tadpole, so observables cannot be *coordinates* on it** |
| **the covariance table** | `W`, `g_s`, moduli, couplings as covariant functions on the orbit | **in progress** — Law II is row 1 |
| **the dictionary** | the map from orbit data to the low-energy parameters, with bounds | **not started** |
| **the deficit** | `m`, counting certified parameters | **9**, audited from the code |

The orbit-space-is-a-point result is the sharpest correction this week: it kills the tempting
"observables are coordinates" framing and forces the covariance-table framing instead. A
programme that had not noticed it would have spent a year looking for a coordinate chart on a
point.

## 3. What the covariance table has to contain

For each generator `g ∈ {S, T}` and each observable `O ∈ {W, g_s, z_i, τ, gauge couplings,
Yukawa matrices}`:

    O  ->  f_g(O, τ, z)      with f_g written in closed form

- **Law II** gives `|W| → |W|` under S (25/25 vacua, log residual 0.0000, `|τ|` from 2.16 to
  11.49). Its **phase** is the open half — the table script measures the complex ratio
  precisely so a phase law cannot hide.
- `g_s → 1/g_s` under S is the textbook expectation; whether the library realises it is a
  measurement, not an assumption.

**The table is the dictionary.** If every observable has a closed-form transformation law, then
any two dual descriptions can be translated exactly, which is what "one theory described twice"
means operationally. Where a law fails to close, the failure is a finding.

## 4. How each gap gets closed (with its falsifier attached)

| gap | method | falsifier |
|---|---|---|
| **G1** covariance rows for S and T | measure the complex ratio on real vacua (`diag_transformation_laws.py`) | phase moves by anything not a fixed function of `τ` |
| **G2** the S-dual of a stable vacuum must itself be stable | apply S to a vacuum and re-check `|DW| ≈ 0` at the transformed point | the transformed pair is not a vacuum ⇒ well-definedness fails |
| **G3** truncation-independence | `cond(M)` at the **proposal** stage across `h12` (`diagnose_isd_conditioning.py` + `2207Z` hook) | invariant structure changes with `h12` ⇒ every frontier number is a slice artefact |
| **G4** brane / K-theory sector enters `(a)` | extend the invariant-ring analysis to D-brane charges (charges = `K(X)` classes, tadpole = total charge) | a second exact invariant appears that is not a constraint or a label |
| **G5** the dictionary `(c)` | write low-energy parameters as functions on orbit data for one tractable stratum | freedom beyond the GUT-style collapses (3 gauge, 2 b–τ) ⇒ parameters are not functions of invariants |

`G1` and `G2` are cheap and running or runnable now. `G3` is one hook away. `G4` and `G5` are
the long poles, and `G5` is where `m` actually grows.

## 5. Standards this programme holds itself to

1. **Rule of Three** — no structure/randomness claim from one test; three agreeing arms
   (this is how the `W₀` "random" claim was caught and retracted).
2. **A guard for every number** — `tests/test_doc_claims.py` now fails when a doc's `m`, test
   count, or landscape total contradicts the code.
3. **A law needs four things** (see `MITCHELLS-LAWS.md`): precise statement, verification with
   a control that could fail, stated scope, named falsifier.
4. **Every measurement names its stage.** The `1e135` incident: `cond(M)` at a *converged*
   vacuum is meaningless because `⋆G = iG` makes the ISD matrix singular there by construction.
   Stage-free numbers are not results.
5. **A test that can only return `NO-TEST` is mis-specified**, not passed (Test 2).
6. **Truncation is not the theory.** Everything measured at `h12 ≤ 4` lives in a slice of 272
   moduli; until `G3` closes, no frontier number is a fact about string theory.

## 6. What "solved" would look like, in this programme's own terms

All three of `(a)`, `(b)`, `(c)` closed for the sector containing our world:
the invariant ring enumerated, **every** observable's transformation law known, and every SM
parameter either forced by a constraint/label or certified free with an error bound — with `m`
equal to the number certified, and no exact relation among the free ones beyond those the
symmetry forces.

What it would **not** look like: a formula tying the 19 numbers to a Calabi–Yau's topology.
That is the shape the theorem forbids, and a programme that promised it would be promising
something it has already disproved.

---

**Cross-references:** `docs/unification-claim.md` (C1–C4 + ladder results), `docs/MITCHELLS-LAWS.md`
(Law I, Law II, naming rules), `docs/five-pillars.md` (the theorems the structure rests on),
`docs/complete-exact-structure.md` (why no fourth kind of exact content exists).
