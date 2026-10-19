# No-Fingerprint No-Go Theorem — search can only eliminate, never select

`scripts/validate_no_fingerprint.py` proves the result that turns the
constraint-first program from "we could not find a fingerprint" into "**no
fingerprint can exist**". It says the D3 tadpole is a **complete** invariant of the
flux under duality.

## Theorem (No-Fingerprint No-Go)

> **The D3 tadpole `N = Fᵀ J H` is a complete invariant of the flux pair (F, H)
> under the duality group Sp(b₃): for `N ≠ 0`, two pairs are dual-equivalent
> **if and only if** they have the same tadpole.**

Consequence for search:

> **No exact, frame-independent quantity can distinguish two flux vacua that share
> a tadpole. The only exact selector is the tadpole itself, and it is *bounded*
> (`N ≤ L`). Therefore a landscape search can only *eliminate* (by the constraint
> `N ≤ L`) — it can never *select* a special vacuum, because there is no invariant
> left to select with.**

## Two lemmas, both exact

**Lemma 1 — only the tadpole is an invariant (Constraint-First / FFT, Weyl 1939).**
Every Sp(b₃)-invariant polynomial in (F, H) is a polynomial in `Fᵀ J H`. Proved
across all degrees in `validate_constraint_first.py` (5/5). So any invariant
observable is a function of the tadpole **alone**.

**Lemma 2 — the tadpole level sets are single duality orbits (proved here).**
Sp(b₃) acts transitively on each level set `{Fᵀ J H = N}`, `N ≠ 0`. Proof by
dimension: the orbit tangent space at a pair is the image of `X ↦ (XF, XH)` for
`X ∈ sp(b₃)`, and its rank is `2b₃ − 1` (= 11 for b₃ = 6), which is exactly the
codimension-1 dimension of the level set. The orbit is open in the level set, closed
(algebraic group orbit), and the level set is connected for `N ≠ 0`, so the orbit
*is* the level set.

Together: the invariant ring says "anything invariant is a function of N", and
transitivity says "within a fixed N there is no further structure to be invariant
*to*". Hence **N is complete**.

## The verification (6 exact + 2 numeric)

| check | statement | grade |
|---|---|---|
| Lemma 1 | tadpole sp-invariant + generates the ring | exact (5/5 in the FFT script) |
| Lemma 2.1 | orbit tangent ⊂ level-set tangent (grad N · (XF, XH) = 0, 21 generators) | exact |
| Lemma 2.2 | orbit tangent rank = 2b₃−1 = 11 at 3 generic pairs | exact (integer rref) |
| Lemma 2.3 | orbit tangent rank = 11 **at** the canonical pair (e₀, e₃) | exact |
| Lemma 2.4 | 200 duality transforms of one pair all keep N = 1 (distinct vacua) | numeric |
| Corollary | the only invariant is constant on a fixed-N slice (std ~ 0) while a raw component varies (std ~ 1.9) | numeric |

## What this does and does not claim

**Does claim (rigorously):** the flux sector has exactly one duality-invariant
exact structure — the tadpole — and the duality group identifies any two fluxes
with the same tadpole. The "structure map" finding (tadpole r = 1.0, all else
uniform) is therefore *forced*, not just measured: there is nothing else for a
duality-respecting learner to find.

**Does not claim (yet):** the same for the *other* exact structures — topology
(h¹¹, h²¹, c₂, κ), D-brane charges, anomaly cancellation, charge quantization.
Those are exact but live outside the flux-invariant ring; the open question the
ToE must answer next is whether **all** exact structure is constraint structure
(the "complete list of constraints" program), with the flux sector now proven to
be one single constraint.

**Boundary of the argument:** global transitivity rests on two standard facts
(the orbit of an algebraic group is Zariski-closed; the `N ≠ 0` level set is
connected). These are classical and stated here as such; the machine-checked
(Lean) upgrade is the deferred proof-arm, as with the other theorems.

## Reproduce

```
python3 scripts/validate_no_fingerprint.py        # 6 exact + 2 numeric
python3 scripts/validate_constraint_first.py      # Lemma 1, all degrees (5/5)
python3 scripts/validate_mitchell_uniqueness.py   # Lemma 1, degree 2 (6/6)
```
