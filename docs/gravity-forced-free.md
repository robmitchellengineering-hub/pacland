# Gravity / QG sector — the forced/free characterization

The same recipe, applied to the gravitational sector. This is the SEXTANT lane's target, stated
in the forced/free language now standard across the other two sectors.

## The split

| class | gravity | analog |
|---|---|---|
| **forced** (constraint) | diffeomorphism invariance + the **contracted Bianchi identity** `∇·G = 0` (the Einstein tensor is divergence-free — the *consistency* condition) | the SM's anomaly cancellation; flux's tadpole |
| **label** | the topology / manifold | `h¹¹, h²¹` in flux; gauge group in SM |
| **free** (parameter) | `G` (Newton), `Λ` (cosmological constant), the matter couplings | the 19/26/28; `W₀, g_s` in flux |

## What is kernel-checkable (the forced half)

The contracted Bianchi identity `∇_a G^{ab} = 0` is a **theorem** — it follows from the second
Bianchi identity of the Riemann tensor `∇_a R + ∇_b R + ∇_c R = 0`, twice-contracted. It is the
gravitational analog of "the SM hypercharges are forced": the Einstein equation's left-hand side
is *required* to be divergence-free, which is exactly the statement that GR's source `T^{ab}` must
satisfy `∇_a T^{ab} = 0` (local stress-energy conservation). The constraint is not chosen; it is
forced by the geometry.

## The honest gap (not yet done)

- **Formalizing the contracted Bianchi identity in Lean** needs the differential-geometry stack
  (metric, Levi-Civita connection, Riemann tensor, the Bianchi identity). Mathlib has partial
  curvature machinery, but the full GR statement is unbuilt — the same status as Darboux's theorem
  ("nowhere in any proof assistant", per the Lean plan's deferred list).
- **Whether gravity has a duality group that collapses `G, Λ`** (like Sp collapses flux to the
  tadpole) is *open*: the diffeomorphism group is infinite-dimensional, not a finite duality
  group, and there is no known "FFT for gravity." So the gravitational free column is *not* known
  to be reducible — the analog of "no clean duality group" is, for gravity, **un-researched**, not
  settled.

## The read

Gravity *does* decompose as forced + free — its constraint (Bianchi/diffeomorphism) is
kernel-checkable in principle, its parameters (`G, Λ`) are free and not known-reducible. The
kernel-checking of `∇·G = 0` is the next concrete formalization target, and it is a
differential-geometry lift, not the linear algebra of the SM sector.
