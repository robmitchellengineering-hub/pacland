import Mathlib

/-!
Copyright (c) 2026 Rob Mitchell. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Rob Mitchell
-/
/-!
# M3 — the cluster/polymer expansion convergence criterion

The third piece of the weak-coupling multiscale RG scaffolding. The cluster/polymer expansion of the
partition function in the small-field (weak-coupling) regime is a geometric series in the "activity"
(the deviation from the trivial connection), and it converges exactly when the activity is small.
This is the core convergence fact that makes Balaban's small-field region well-defined.
-/

open scoped BigOperators

noncomputable section

namespace QM

/-- The cluster-expansion convergence criterion: the geometric series in the activity `z`
converges exactly when `|z| < 1` — the weak-coupling / small-field expansion converges precisely
when the activity is small. This is the core of the polymer/cluster-expansion framework. -/
theorem cluster_expansion_converges_iff {z : ℝ} :
    Summable (fun n : ℕ => z ^ n) ↔ |z| < 1 := by
  simpa using (summable_geometric_iff_norm_lt_one (ξ := z))

end QM
