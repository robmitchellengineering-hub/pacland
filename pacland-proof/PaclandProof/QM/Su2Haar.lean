import Mathlib

/-!
# SU(2) as the unit quaternions, with Haar measure — M0 of the real-group formalization

Claude's step 2, milestone M0. The model: SU(2) ≅ the unit quaternions ≅ S³ = `Metric.sphere (0 : ℍ) 1`.

**Reconnaissance (Mathlib v4.35.0, verified by `#synth`):** the instances all EXIST, so M0's
topological-group blocker is NOT a blocker:
- `Metric.unitSphere.instGroup` — the unit sphere has a `Group` (quaternion product).
- `Metric.sphere.compactSpace 0 1` — the sphere is `CompactSpace`.
- `Metric.sphere.instIsTopologicalGroup` — `IsTopologicalGroup`.
- `MeasureTheory.Measure.haarMeasure` + `MeasureTheory.Measure.IsHaarMeasure` — the Haar machinery.

`Matrix.specialUnitaryGroup (Fin 2) ℝ` has NO `CompactSpace` in v4.35.0 — so the quaternion route is the
one to use.

This file is M0's first deliverable: the DEFINITIONS + the TARGET STATEMENT, before any proof.
Per Claude's process rule: write the statement and definitions first, have them reviewed, THEN prove.
-/

open scoped Quaternion

noncomputable section

namespace QM

/-- **SU(2) = the unit quaternions = S³** (the SUBTYPE of the sphere, where the group instance lives). -/
abbrev SU2 := ↥(Metric.sphere (0 : Quaternion ℝ) 1)

-- M0 (PROVEN): SU(2) = the unit quaternions is a compact topological group. All three instances
-- synthesize from Mathlib (the quaternion route; the matrix `specialUnitaryGroup` route has no
-- `CompactSpace`). This fills the compact/topological-group part of the formal-conjectures
-- `sun_compactSimpleLieGroup` gap, for SU(2).
instance : Group SU2 := inferInstance
instance : CompactSpace SU2 := inferInstance
instance : IsTopologicalGroup SU2 := inferInstance
instance : MeasurableSpace SU2 := borel SU2
instance : BorelSpace SU2 := ⟨rfl⟩

-- M0 (PROVEN): the Haar measure on SU(2). The whole compact group is a positive compact set; the
-- Haar measure is `haarMeasure`. (Not yet normalized to probability 1 — that is the next M0 step.)
noncomputable def su2PositiveCompact : TopologicalSpace.PositiveCompacts SU2 :=
  { carrier := Set.univ, isCompact' := isCompact_univ,
    interior_nonempty' := by rw [interior_univ]; exact ⟨1, Set.mem_univ _⟩ }

noncomputable def su2Haar : MeasureTheory.Measure SU2 :=
  MeasureTheory.Measure.haarMeasure (K₀ := su2PositiveCompact)

-- M0 (normalization, PROVEN): the Haar measure is a PROBABILITY measure (K₀ = Set.univ, so the whole
-- group has measure 1).
theorem su2Haar_probability : su2Haar Set.univ = 1 := by
  unfold su2Haar
  have h : (MeasureTheory.Measure.haarMeasure (K₀ := su2PositiveCompact)) su2PositiveCompact.carrier = 1 :=
    MeasureTheory.Measure.haarMeasure_self (K₀ := su2PositiveCompact)
  simpa [su2PositiveCompact] using h

-- M0 obligations (TODO, in order):
-- 0. `SU2` above is the SET `Metric.sphere (0 : ℍ) 1`; the group instance `Metric.unitSphere.instGroup`
--    lives on the bundled subtype `Metric.unitSphere`. Use the subtype (or `Metric.unitSphere`) for the
--    group/Haar ops. `conjInvariant` (adjoint-invariance of `reTr`) is defined after this is fixed.
-- 1. `reTr q := 2 · (real part of q)` — needs the quaternion field access (the type is the generalized
--    quaternion `ℍ[R,-1,-1]`, whose `re` projection is not yet named in this file).
-- 2. prove `Re tr q = 2·re q` (the quaternion↔Pauli correspondence).
-- 3. `su2Haar` — the normalized Haar probability measure, from `MeasureTheory.Measure.haarMeasure`
--    applied to the compact group `SU2` (all instances exist; the remaining work is normalization).
-- 4. `conjInvariant reTr` (conjugation invariance of the trace).

-- TARGET THEOREM (M1–M3), stated before proof:
--   For SU(2) lattice gauge theory on a d-torus of side L with the Wilson action, there is an explicit
--   β₀ > 0 such that for all β < β₀, the correlations of gauge-invariant local observables decay
--   exponentially with a rate UNIFORM in L.
--   This is a STRONG-COUPLING result (far from the continuum): it says nothing about the Clay rungs.
--   Do NOT call it a "mass gap" until M4 (clustering ⟹ transfer-matrix gap) exists; call it
--   "uniform exponential clustering". The precise covariance-decay statement is the next definition.

end QM
