# Animal communication — constraint-first

**The lane.** Decoding animal communication is an **underdetermined inverse problem**: infinitely many
"meanings" fit any signal, and there is no ground-truth translation key (no Rosetta Stone). The pacland
move for the underdetermined wall is *compute the set's invariants — the constraints — not the nonexistent
point*. So we measure the **constraints** (the only learnable structure), and we measure the **meaning map**
to see whether it is deterministic (a Rosetta unit), uniform, or graded.

**The claim (falsifiable).** In a vocal corpus, the constraints (combinatorial rules, dialect,
context-dependence, structural ordering) are **LEARNABLE**; the context-free acoustic → referent map is
**graded** — statistically informative but never deterministic. The falsifier: a context-free acoustic map
to a behavioural referent at ridge-CV balanced accuracy ≥ 0.90 AND permutation z ≥ 3. That would *be* a
Rosetta unit and would refute the claim.

**The instrument** (`pacland.animal.learnability`): the Rule of Three, re-expressed for acoustic features —
single-coordinate mutual information (reuses `pacland.structure`), joint ridge-CV (classifier for
categorical targets, regression for continuous), and a label-permutation null. A claim of LEARNABLE vs
uniform is made only when the arms agree.

## First measured result (C1 — macaques, 2,520 calls, Rebout et al. 2020, CC0)

| feature | role | joint (ridge-CV) | perm z | verdict |
|---|---|---|---|---|
| quantile-ordering q1≤q2≤q3 | constraint (positive control) | r = **+0.929** | +31.6 | LEARNABLE |
| unit-inventory (clusters) | constraint | silhouette **+0.403** | +28.3 | LEARNABLE |
| dialect (acoustic → species) | constraint | bal-acc **0.544** (chance 0.25) | +36.7 | LEARNABLE |
| context-dependence (acoustic → context) | constraint | bal-acc **0.597** (chance 0.33) | +176 | LEARNABLE |
| acoustic → referent (falsifier) | meaning | bal-acc **0.597** (< 0.90) | +176 | **graded — no Rosetta unit** |

The positive control (r = 0.93) recovers a deterministic spectral constraint — the physics reference
recovered its constraint at r = 0.99 — so the three checks fire on real structure. The meaning map is
graded (0.60 vs chance 0.33), not uniform: macaque calls are partially context-informative but nothing
decodes deterministically.

## Limits (named)

1. C1's referent is a **proxy** (social context, not an external referent). A true referential test
   (alarm-call → predator type) is a separate run (C1b).
2. The C1 corpus is a **per-call feature table, not sequences** — combinatoriality/Zipf/temporal
   constraints are untestable on it (C1c).
3. **Linear models only** — a non-linear decoder could push the meaning map toward 0.90; that bounds what
   "no Rosetta unit" can currently claim.
4. The **module** (`pacland.animal.learnability`) is numpy-only; the full C1 pipeline's unit-inventory
   arm (k-means + silhouette) needs **scikit-learn**, which is imported only in
   `scripts/measure_animal_constraints.py` (a manual run, not part of CI).

## Where this lives

- `src/pacland/animal/learnability.py` — the three-check split (reusable).
- `scripts/measure_animal_constraints.py` — the C1 pipeline, re-runnable.
- Data: CC0, Zenodo 3877581 (`data/animal/`), Rebout et al. 2020, Proc. R. Soc. B 287:20200439.
