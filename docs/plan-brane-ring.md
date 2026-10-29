# F3 — the brane invariant ring: the one build that can overturn our own claim

**Status:** plan. Owner: whoever holds `pacland-rog` (this session). Written after the parallel session's
first figures landed (F1 #212, F2-M1 #213), because **they change the direction** — this records why.

## What the other session's figures did to the plan

| figure | what it meant for me |
|---|---|
| **F1: the small-tadpole fraction is 0.071 (tadpole-uniform) vs 0.361 (log-N) vs 0.2015 (flux-uniform) — a factor 5.05** on an exactly enumerated lattice | the "fraction of vacua" language is **measure-first**. Any ensemble claim I make about the landscape has to name its measure or it is a draw from a prior I chose |
| **F2-M1: the conifold sits exactly on the radius of convergence** (`r → 0.9933` at `z_c = 1/5⁵`; tail bound degrades to 9.4e-5), so **no practical number of hypergeometric terms certifies the conifold period** | **R1 is not a quick win and is not mine.** It needs a local Frobenius expansion at `z_c`, which is F2-M2. I stop looking at R1 |
| F2-M1 also found the coefficient-space operator check is a **tautology** and that nested `mp.diff` at fourth order gives 1e78 residuals | two method traps I would otherwise have walked into in the ring computation |

**Direction taken from that:** not R1, not B3's build, not the measure engine. **F3**, which the plan
already assigns to this node, needs no periods, and is the only item that can falsify a claim we are
currently making.

## The claim F3 attacks

> *The D3 tadpole `FᵀJH` is the unique exact (moduli-independent) structure of the flux.*

Everything the programme says about "exact tier" rests on it. Two prior attempts to test it are on record
and both are honest failures of *my* method, not of the claim:

- `validate_uniqueness_at_scale.py` confirmed **one** invariant against the full `sp(2m)` algebra for
  b3 = 2, 4, 6, and found **four** with two independent flux pairs — so the claim is scoped to one pair;
- the **higher-degree** question (quartic, sextic invariants) was **never computed** — two attempts failed
  (a subgroup masquerading as the full group; a monomial action giving 4 instead of 1) and the claim still
  carries the label *"reasoned from the first fundamental theorem for Sp, not computed."*

## Why the brane route is different, and can actually settle it

The polynomial-invariant route asks about functions of the fluxes alone. The **brane** route asks what
*charges* the geometry can support, built from quantities CYTools already gives:

- `intersection_numbers()` — `κ_ijk` on `H²(X)`;
- `second_chern_class()` — `c2_i`, the curvature contribution to D3 charge;
- `chi`, `h11`, `h12`.

If every moduli-independent integer one can build from `(F, H, κ, c2)` is a combination of the tadpole and
`c2·D`, then the tadpole is alone at every degree **in the coefficient ring the geometry actually
provides** — which is a stronger and more physical statement than a polynomial-invariance count.

**Falsifier, stated before the run:** a second independent integer invariant built from `(F, H, κ, c2)`
that is **not** a function of the tadpole and `c2·D`. If one exists, our "exact tier is unique" sentence
is wrong and the programme keeps a second exact handle — which would be a find, not a failure.

**Null outcome:** only the tadpole and `c2·D` survive ⇒ the uniqueness claim gains a *computed* leg at
every degree, replacing the phrase "reasoned from the standard theorem".

## First step, and the API wall already measured

The first computation is on **one** manifold where every input is available and hand-checkable: the
quintic (`h11 = 1`, `h12 = 101`, `χ = -200`). Then a multi-parameter model, because the ring only becomes
interesting when there is more than one divisor.

Measured on pacland-rog while writing this plan, so the next session does not repeat it:

- `cytools.calabiyau.CalabiYau(Polytope(...))` → **`AttributeError: 'Polytope' object has no attribute
  'triangulation'`** — a bare polytope is not enough;
- `cytools.polytope.Polytope(verts, make_simplicial=True)` → **`TypeError: unexpected keyword argument`**
  — this CYTools build does not take that flag;
- `cytools.polytope.fetch_polytopes` does not exist in this build (it is on `cytools`, not the
  submodule).

So the first build task is **getting a triangulated polytope into `CalabiYau`** — `Triangulation` and
`all_triangulations` *are* exposed in `cytools.polytope`, so the path is
`Polytope(...) → Triangulation → CalabiYau`, and that is the next concrete step, not another probe.

## Order

1. quintic: intersections, `c2`, and the charge lattice from `(F, H, κ, c2)` — with the tadpole as the
   only survivor, or not;
2. one multi-parameter model, where a second invariant has room to exist;
3. the write-up: replace "reasoned from the FFT for Sp" with either a computed uniqueness or a second
   invariant.

No claim is made here beyond the two measurements above.
