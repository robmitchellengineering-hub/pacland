# Plan — the dictionary engine

**Decision it rests on.** Recorded 2026-10-30 in the planning room (`DECISIONS.md`, D17): the falsifier
engine yields certain *negatives*, and only **construction** or **equivalence** can yield a certain
positive — so the next instruments are a dictionary engine (certified equivalences) and a counterexample
search. This document is the first of those.

**Why.** The estate can certify what is *not*; it cannot certify that two descriptions are the *same
object*. That second thing is worth more, because one certified map pays out on every fact on both sides at
once: anything proven in one frame becomes proven in the other, for free.

**What an entry has to be.** Not "we checked an invariance". A dictionary entry is a **map with an inverse
and a running test**:

1. the two frames named, and the coordinate change `T` in closed form;
2. `T⁻¹` in closed form;
3. `T ∘ T⁻¹ = id` verified numerically on a sample, with a stated bound;
4. at least one **named observable** carried across, whose transformed value is computed and compared —
   not assumed invariant;
5. the **failure boundary**: where the map stops closing, and why. A dictionary that claims to work
   everywhere and cannot say where it stops is a slogan.

**Order of certification (cheapest first).**

| # | duality | state today | what it needs |
|---|---|---|---|
| 1 | **flux scaling** `(F,H) → d(F,H)` | proven (the flux-scaling lemma, 5/5 exact + a numeric control) | packaging only: `T` closed form, `T⁻¹` = divide, one observable (`W → dW`, `N → d²N`) |
| 2 | **mirror map** LCS ↔ conifold | both ends exist, **connected today**: `src/pacland/periods/connection.py` gives three of four conifold columns with residuals 2.3e-21 / 9.0e-14 / 1.8e-13 | the flat coordinate `t = ω₁/ω₀`, `T` and `T⁻¹` as series with bounds, and one observable carried across (the Yukawa coupling, or `W`) |
| 3 | **S/T duality** | Law II measured on 25 vacua (log residual 0.0000) and the full duality group proven (5/5) | the *phase* half of Law II — currently the open half — expressed as a map rather than a fit |

**Acceptance for the first entry (flux scaling).** A `dictionary.entry()` that returns the two maps, the
identity residual, the carried observable's residual, and the boundary — and a **mutation test**: perturb
`T` and the identity check must fail. If the check cannot fail it is not a dictionary.

**Falsifier per entry.** The identity residual grows, or the carried observable does not transform by the
stated law, or the boundary is claimed empty on a finite sample where it demonstrably is not.

**Where.** Mac. No node: every input is already on disk or already computed.

**What it is not.** It does not discover a new duality. It certifies ones we half-own, and turns each into
a worked instrument that can translate a question into the frame where it is easy.
