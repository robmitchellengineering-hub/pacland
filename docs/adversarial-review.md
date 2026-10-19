# Adversarial review — the verification system broke its own result

Six agents were told to *attack* six pieces of the constraint-first result before
publication. They found **two fatal flaws, three serious, one held**. This is the Rule
of Three at the level of theorems: trying to falsify, not just confirm. Everything below
is what must be corrected before the paper ships.

## Verdicts

| piece | verdict | severity |
|---|---|---|
| The no-search consequence | **flaw found** | **fatal** |
| Transitivity / Completeness | **flaw found** | **fatal** |
| SM hypercharge uniqueness | **flaw found** | serious |
| Five Pillars citations (CST) | **flaw found** | serious |
| The FFT claim (which group) | **flaw found** | serious |
| Invariant-ring count = 19 | held | minor |

## The two fatal flaws (must fix before publish)

**1. "Search is provably dead" is overclaimed.** The theorem proves only: *no exact,
polynomial, duality-invariant function of the flux can uniquely single out a vacuum.*
It does **not** rule out moduli-dependent selectors (couplings, Yukawas, Λ are set by
moduli VEVs and transform under duality), non-polynomial criteria, or **statistical**
selection (the very thing the landscape program uses — CC distributions, vacuum
counting). Worse, `N ≤ L` *bounds the search space* (finite), which *supports* ranked
selection rather than forbidding it.

> **Correction:** downgrade to *"no exact, polynomial, duality-invariant flux function
> can single out a vacuum"* — a claim about a narrow class of selectors, not about
> search in general. The headline "search is dead" must be withdrawn or sharply scoped.

**2. The tadpole is not a complete invariant over the integers.** The transitivity proof
is a *real-manifold* argument (orbit open+closed ⇒ equals the level set), but the physical
fluxes are **integral** and the physical group is Sp(2b₃, **ℤ**). Over ℤ, the **content**
`d = gcd(F,H)` is an extra invariant with `d² | N`, so a non-squarefree tadpole splits into
*multiple* orbits. At `N = 0` transitivity fails even over ℝ.

> **Correction:** replace "complete invariant / same tadpole ⟺ dual-equivalent" with the
> tiered truth: over ℝ (or ℚ), `{N ≠ 0}` is a single orbit (Witt's theorem); over ℤ the
> orbits are classified by content `d | √N` — *finitely many orbits per tadpole, one per
> divisor*, not one. Mitchell's Completeness Theorem must be restated as
> "**finitely many orbits per tadpole, enumerated by content**", and `N = 0` handled
> separately.

## The three serious flaws

**3. Hypercharge uniqueness has a third branch.** The cubic `18 Y_Q (2Y_Q+Y_u)(4Y_Q−Y_u)`
has **three** factors, not two. The `Y_Q = 0` root gives a one-parameter family
`(0, t, −t, 0, 0)` — anomaly-free but unphysical. Uniqueness holds only with the extra
assumption `Y_Q ≠ 0` (equivalently, the correct electric-charge relation). The script and
doc must state this assumption.

**4. Chevalley–Shephard–Todd is misapplied.** CST certifies a free polynomial ring only
for **finite** complex reflection groups; Sp is an *infinite* Lie group. The "tadpole ring
is free" claim needs a different justification (coregularity theory) or a finite reflection
subgroup — or it must be dropped.

**5. The FFT group is conflated.** The paper says "duality group Sp(b₃)", but the group
that naturally pairs (F,H) into a doublet is **S-duality SL(2,ℤ)**, under which the
invariant ring is the Plücker ring `Gr(2,2n)` (all 2×2 minors), *larger* than `C[tadpole]`.
Under the *monodromy* Sp(2n) the FFT genuinely gives `C[tadpole]`. The fix: state the group
explicitly — the **full** duality group Sp(2b₃,ℤ) × SL(2,ℤ), for which the invariant ring
*is* `C[tadpole]` (the intersection, as the full-duality script proves), and add the
Zariski-density step (Sp(2n,ℤ) dense in Sp(2n,ℂ)).

## What survives (the core is intact)

The central result is **not** broken by any of this:

- **The tadpole is the unique Sp(2b₃)-invariant bilinear form** (Mitchell's Uniqueness) — *held*.
- **The constraint-first framework** (only constraints + labels are exact) — *held*, modulo the
  two fatal corrections' scoping.
- **The invariant-ring count = 19** — *held* (with a massless-neutrino qualifier and θ̄-not-θ).
- **Darboux, Atiyah–Singer, K-theory, Gromov** — *held* (only the CST "free ring" pillar is broken).

What breaks is the *scope of the headline*, not the *content of the theorem*: "search is
dead" narrows to "no exact invariant selector"; "complete invariant" narrows to "finitely
many orbits per tadpole."

## What to do before publishing

1. **Fix the two fatal corrections** in the paper, the site, and `AGENTS.md` — "search is
   dead" → "no exact polynomial invariant selector"; Completeness → "finitely many orbits
   per tadpole (content d | √N)".
2. **Add `Y_Q ≠ 0`** to the hypercharge-uniqueness statement.
3. **Replace the CST citation** (or drop the "free ring" pillar).
4. **Name the group explicitly** (full duality group Sp×SL(2,ℤ)) in the FFT statement.
5. Re-run the review on the *corrected* claims before you submit.

## Meta

This is the verification system doing the job it was built for — catching our own
over-reach *before* a referee does. Four fan-outs now, four upgrades: two caught
conflations ("unpredicable", "free parameter"), one found the Five Pillars, and this one
found **two fatal overclaims and three serious over-citations**. The instrument paid for
itself again, and the paper is stronger for the corrections.
