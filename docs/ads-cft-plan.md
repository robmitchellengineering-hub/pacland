# THE PLAN — finish "entanglement = geometry"

Four kernel-checkable rungs, in dependency order. Do them in this order. One frontier, named not deferred.

## Rung 1 — the explicit quasi-isometry map `tree → H²` (NEXT)
- Define the map: each tree vertex (a `List Bool` path) ↦ a point in `Hyperboloid` (horocyclic/exponential coordinates).
- Prove the two QI inequalities (bounded distortion + quasi-surjectivity).
- Depends on: `Hyperboloid` ✅, `quasiIsometric` ✅, `treeDist` ✅.
- Done when: `quasiIsometric treeDist hyperbolicDist <map>` is a theorem.

## Rung 2 — Ryu–Takayanagi "=" (entanglement = area, exactly)
- Prove the equality: for a MERA-optimal state, entanglement across a cut *equals* `D^m` (the cut bonds), not just `≤`.
- Depends on: `areaLaw_rank` ✅ (the bound), `bondConfigurations` ✅ (`D^m`).
- Done when: the `≤` becomes `=` for the optimal state.

## Rung 3 — emergence, discrete (entanglement → geometry)
- Prove: minimizing cross-cut entanglement *forces* logarithmic depth + exponential circumference — i.e. the hyperbolic tree is the unique optimum.
- Depends on: `causalConeDoubles` ✅, `meraDepth` ✅.
- Done when: "the MERA optimum is 0-hyperbolic with exponential volume" is a theorem.

## Rung 4 — Gromov–Hausdorff convergence (the fine limit)
- Define the GH distance; prove the rescaled cone converges to smooth H².
- Depends on: `Hyperboloid` ✅, the QI map (Rung 1).
- Done when: `d_GH(rescaled cone, H²) → 0`.

## Frontier — the partition-function equality (name it, don't fake it)
- `Z_bulk = Z_boundary`. Needs non-perturbative string theory on AdS (does not exist). State it precisely; our four rungs are the kernel-checked evidence.

## Rung 2 (general "=") — the precise path (infrastructure confirmed)

The general `srank (Σᵢ eᵢ⊗eᵢ) = D` is provable, and the Mathlib infrastructure EXISTS (verified):

- `Basis.tensorProduct` (Mathlib/LinearAlgebra/TensorProduct/Basis.lean:37) — the tensor product of bases.
- `Matrix.rank` (Mathlib/LinearAlgebra/Matrix/Rank.lean:134) — the matrix rank.
- `Matrix.rank_one` (Rank.lean:154) — the identity matrix has rank `n`.

The proof, in three lemmas:
1. **flatten** — a tensor `t = Σⱼ aⱼ⊗bⱼ` maps (via the basis `Basis.tensorProduct e e`) to a matrix
   `M = Σⱼ (aⱼ)ᵀ(bⱼ)`, a sum of `r` outer products, so `Matrix.rank M ≤ r`.
2. **diagonal** — `t = Σᵢ eᵢ⊗eᵢ` maps to the identity matrix, so `Matrix.rank M = D` (by `rank_one`).
3. **connect** — `srank t = Matrix.rank M` (the Schmidt rank is the matrix rank), giving
   `D = rank M ≤ srank t` and the "=".

That's the one formalization that lifts the rank-1 case (`srank_simple_eq_one`) to the general `D^m`.

## Rung 1 correction (found round 13) — the map must be fixed, not the inequality

The current `treeToH2` (uniform binary-expansion angle `pathAngle s = Σ sᵢ·2⁻ⁱ⁻¹`) is **not** a
quasi-isometry. Two siblings at depth `d` have `Δθ = 2⁻ᵈ` but sit on a horosphere of scale
`sinh d ≈ eᵈ`, so `hyperbolicDist ≈ (e/2)ᵈ` — unbounded distortion, violating `≤ K·treeDist + C`.

The tree **is** quasi-isometric to H², but via the Švarc–Milnor orbit map (F₂ acting cocompactly on
H²) or the Farey-tree subdivision — a map with **constant** sibling separation, not the uniform-angle
one. Correct fixes: (a) base-`e` angular spacing `θ = Σ sᵢ·e⁻ⁱ⁻¹` (siblings at constant distance, but
the image then lives in a horoball so surjectivity must be handled coarsely), or (b) the Schottky/Farey
construction. The honest next step is to **redefine `treeToH2`**, then re-prove the two QI inequalities
for the corrected map. Everything already proven (`treeToH2_depth`, injectivity, the diameter bound)
stays true but transfers to the corrected map.

## Rung 4 finding (round 16) — the GH distance is ALREADY in Mathlib

The shard that stalled on Rung 4 was re-deriving something Mathlib already has:
`Mathlib/Topology/MetricSpace/GromovHausdorff.lean` defines `GromovHausdorff.ghDist` (the Gromov-
Hausdorff distance between nonempty compact metric spaces), the `GHSpace` quotient, and the key
lemmas `ghDist_le_hausdorffDist` / `ghDist_eq_hausdorffDist` / `hausdorffDist_optimal`. So "define
the GH distance" is already done — just `import Mathlib` and use `GromovHausdorff.ghDist`. The
REMAINING Rung 4 work is the *convergence proof* (rescaled cone → H²), which is the genuinely hard
part, not the definition.
