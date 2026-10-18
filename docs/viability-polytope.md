# The viability polytope — the answer is a region, not a point

Constraint-first (`docs/new-approach.md`) says the answer to "which vacuum?" is
*not* a point but the *feasible region*: the intersection of verified constraints.
This document makes that region an explicit, computable object — a **polytope** —
and states the reframe it buys.

## The reframe

> **The landscape is not big; the constraint system is small.**

10⁵⁰⁰ is the *cardinality* of a set. But the viable class is described by **k
inequalities** — k numbers — regardless of how many points the landscape has. If k
independent constraints each eliminate fraction ≥ p, the survivor fraction is
(1−p)ᵏ, *independent of the set's size*. So "search the landscape" is the wrong
problem; "solve the polytope" is the right one, and it is polynomial in k.

This is the missing link between the two camps the new approach unified: the
search camp treats the landscape as a huge set to enumerate; the constraint camp
treats it as a small system of inequalities. The polytope is the *object* that
makes the second reading rigorous — and it is exactly what the verification
discipline can certify.

## The computation

Each verified constraint is a half-space in observable space. In the (log g_s,
log W₀) plane:

| constraint | half-space |
|---|---|
| weak coupling (g_s < 1) | log g_s ≤ 0 |
| small \|W₀\| < 1 | log W₀ ≤ 0 |
| combined g_s·\|W₀\| < 0.1 *(illustrative)* | log g_s + log W₀ ≤ ln 0.1 |

Intersecting these with the sampled box gives the viable polygon
(`src/pacland/viability.py::viable_polytope`, Sutherland–Hodgman clipping in pure
stdlib). On the 107-vacua data, three constraints cut the box to **5.6%**, with
four vertices:

```
(-4.269, -0.909)  (-1.394, -0.909)  (-2.303, 0.000)  (-4.269, 0.000)
```

Those four vertices *are* the answer, in the constraint-first sense: the extremal
viable vacua. A fifth constraint would clip this polygon further; each independent
one multiplies the survivor fraction, and the object stays a polygon — describable
by its vertices, never by enumerating its interior.

Run it: `pacland viable data/vacua_observables.json`.

## What this is and is not

- **It is** a mechanism for turning verified constraints into a characterized
  viable class — the inverse problem of `new-approach.md`, answered by
  *intersection* rather than *search*.
- **It is** falsifiable: every half-space is a claim ("g_s < 1"), each checkable.
  A wrong constraint shrinks the polygon wrongly, and that shows up as a
  contradiction with data.
- **It is not** a selection mechanism: the polygon has *many* points, and no
  measure is imposed on it. Selection remains the open measure problem
  (`docs/open-questions.md` §1). The polytope only certifies *viability*.

## Honest limits

- 2D only, in one coordinate slice (log g_s, log W₀). The real viable class lives
  in the full observable space (gauge couplings, masses, topology); the polytope
  generalizes to higher dimension but vertex enumeration there is a heavier
  computation.
- The "combined" bound g_s·|W₀| < 0.1 is **illustrative, not a measured swampland
  bound** — it is there to show how a non-axis-aligned constraint makes the
  polygon non-trivial. Do not cite it as a physics result.
- The fraction (5.6%) is measured against the *box* (uniform log-space), not the
  sample distribution; `pacland constrain`'s 99.1% is the sample measure. The two
  are different named measures (the choice of D, `docs/open-questions.md` §4).

## Where this lives

- `src/pacland/viability.py` — `clip_polygon`, `polygon_area`, `viable_polytope`,
  `elimination_compression`.
- `src/pacland/cli.py` — the `viable` command.
- `tests/test_viability.py` — the geometry, pinned.
