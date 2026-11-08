# AdS/CFT roadmap — from the discrete ToE to the smooth limit

The honest goal: a kernel-checked **"entanglement = geometry"** claim, from the discrete MERA cone
up to the smooth hyperbolic plane. This is the geometric heart of AdS/CFT — *not* the full
Maldacena duality, which stays named as the open frontier.

## The big think — two jobs, very different hardness

### Job 1 — the geometric continuous limit (provable)

The MERA causal cone is a **binary tree**. We have already kernel-checked the two invariants that
*make* it hyperbolic:

- **0-hyperbolicity** (`treeDist_four_point` — Gromov's four-point condition).
- **exponential volume** (`ballVolumeExponential` = 2^(r+1)−1, `ballVolume_growth_class`).

Gromov's classification then does the heavy lifting: **a geodesic space that is 0-hyperbolic with
exponential growth is quasi-isometric to the hyperbolic plane H².** The tree *is* such a space, so:

```
tree is 0-hyperbolic  ∧  tree has exponential growth   ⟹   tree ≃_QI H²
```

That is the honest "continuous limit" in the **coarse (quasi-isometry) sense** — the same geometry
as the smooth plane, up to bounded distortion. The *fine* version (Gromov–Hausdorff convergence to
the literal metric `ds² = dr² + sinh²(r)dθ²`) is the next rung and needs the metric-geometry stack.

**Concrete rungs (kernel-checkable, in order):**
1. Define quasi-isometry (two-sided bounded distortion).
2. Prove the tree's exponential growth is a QI invariant (already: `ballVolume_growth_class`).
3. Define H² (the Poincaré disk, or the tree itself as the model) + its metric.
4. Prove `tree ≃_QI H²` via the growth-class + 0-hyperbolicity invariants.

### Job 2 — the structural AdS/CFT (state precisely, prove the pieces)

Maldacena's full duality (string theory on `AdS₅×S⁵` ↔ `N=4` SYM) is **25 years open** — we state
it, we do not claim to prove it. But its *constraint-first* core is provable:

- **The area law** — entanglement entropy ≤ cut area (`areaLaw_rank`, done) — this is the
  Ryu–Takayanagi bound in discrete form.
- **The emergence direction** — the entanglement structure *forces* the geometry: 0-hyperbolicity +
  exponential volume are the geometry that the area law implies.
- **The dictionary** — the constraint-first pattern matches on both sides: boundary (conformal
  labels, entanglement) ↔ bulk (geometry, the tadpole/area constraint). Relations, never values.

**Concrete rungs:**
1. State Maldacena's conjecture as a precise theorem (what "dual" means — a matching of invariants).
2. Kernel-check the area law ↔ Ryu–Takayanagi correspondence (minimal surface = entanglement).
3. Prove the emergence: `areaLaw ∧ 0-hyperbolic ∧ exponential` ⟹ the geometry is hyperbolic.

## The honest claim we are building toward

> **"The entanglement structure of the MERA network is a discrete hyperbolic space (0-hyperbolic,
> exponential volume, area law), quasi-isometric to the hyperbolic plane — entanglement = geometry,
> kernel-checked from the discrete up to the smooth limit. The full AdS/CFT duality is the open
> frontier this sits inside."**

That is a *true* ToE claim — the discrete fully proven, the continuous limit proven in the coarse
(QI) sense, the physics duality honestly named as the frontier.
