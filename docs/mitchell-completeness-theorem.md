# Mitchell's Completeness Theorem — no exact invariant selector

`scripts/validate_mitchell_completeness.py` proves the result that turns the
constraint-first program from "we could not find a fingerprint" into "**no exact
polynomial invariant selector can exist**". It says the D3 tadpole is the **unique**
duality-invariant of the flux, and that over the reals each tadpole level set is a single
orbit while over the integers there are only *finitely many* orbits per tadpole.

## Theorem (Mitchell)

> **Over ℝ (or ℚ), for `N ≠ 0` the level set `{Fᵀ J H = N}` is a single
> `Sp(b₃, ℝ)` orbit (transitivity). Over the integer group `Sp(b₃, ℤ)`, the orbits are
> classified by the content `d = gcd(F, H)` with `d² | N`, so there are *finitely many*
> orbits per tadpole — one per divisor `d` of √N — and `N = 0` is a union of several
> lower-dimensional orbits.**

Consequence for selection:

> **No exact, polynomial, duality-invariant function of the flux can single out a
> vacuum: the only exact invariant is the tadpole, and over the integers it alone does
> not even distinguish the finitely many orbits sharing a tadpole (that needs the
> content `d`). This is a no-go on *exact invariant* selectors — it does *not* rule out
> statistical, moduli-dependent, or non-polynomial selection criteria.**

## Two lemmas, both exact

**Lemma 1 — only the tadpole is an invariant (Constraint-First / FFT, Weyl 1939).**
Every Sp(b₃)-invariant polynomial in (F, H) is a polynomial in `Fᵀ J H`. Proved
across all degrees in `validate_constraint_first.py` (5/5). So any invariant
observable is a function of the tadpole **alone**.

**Lemma 2 — over ℝ, each level set is a single orbit; over ℤ, finitely many.**
Over ℝ, `Sp(b₃)` acts transitively on each level set `{Fᵀ J H = N}`, `N ≠ 0`: the orbit
tangent space has rank `2b₃ − 1` (= 11 for b₃ = 6), equal to the level set's codimension-1
dimension, and the orbit is open + closed in the connected level set, hence equals it. Over
the *integer* group this real-manifold argument does not apply — the content `d = gcd(F, H)`
is a `Sp(b₃, ℤ)`-invariant with `d² | N`, so a non-squarefree `N` splits into multiple
integral orbits (Wall's theorem).

Together: the invariant ring says "anything invariant is a function of N", and over ℝ
transitivity says "within a fixed N there is no further continuous structure"; over ℤ the
residual invariant is the content `d`, giving finitely many orbits per tadpole.

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

**Does claim (rigorously):** the flux sector has exactly one duality-invariant exact
polynomial — the tadpole — and over ℝ the duality group identifies any two fluxes with the
same (non-zero) tadpole; over ℤ there are finitely many orbits per tadpole, labelled by the
content. The "structure map" finding (tadpole r = 1.0, all else uniform) is therefore
*forced*: there is nothing else for an exact, duality-respecting learner to find.

**Does not claim:** a no-go on *statistical* or *moduli-dependent* selection — the theorem
is about exact polynomial invariants only. Nor does it cover the *other* exact structures —
topology (h¹¹, h²¹, c₂, κ), D-brane charges, anomaly cancellation, charge quantization —
which live outside the flux-invariant ring.

**Boundary of the argument:** the real transitivity rests on two standard facts (the orbit
is closed; the `N ≠ 0` level set is connected), and the integral "finitely many orbits" on
the content classification (Wall's theorem). Both are classical and stated here as such; the
machine-checked (Lean) upgrade is the deferred proof-arm.

## Reproduce

```
python3 scripts/validate_mitchell_completeness.py   # 6 exact + 2 numeric
python3 scripts/validate_constraint_first.py      # Lemma 1, all degrees (5/5)
python3 scripts/validate_mitchell_uniqueness.py   # Lemma 1, degree 2 (6/6)
```
