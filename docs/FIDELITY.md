# FIDELITY — pairing each formal definition with its textbook counterpart

Claude's process rule for the real-group formalization: *definition fidelity is where formalizations
usually go wrong.* Every definition below is paired with its mathematical source. If a definition is
found to diverge from its source, it is a bug, not a simplification.

| Lean definition | file | textbook counterpart | fidelity status |
|---|---|---|---|
| `SU2 := Metric.sphere (0 : ℍ) 1` | `Su2Haar.lean` | SU(2) ≅ unit quaternions ≅ S³ | **to verify** — the `Metric.unitSphere.instGroup` product must equal quaternion multiplication |
| `reTr q := 2·q.re` | `Su2Haar.lean` | `Re tr U = 2·re q` for `U ∈ SU(2)` in the 2×2 rep | **to prove** — needs the quaternion↔Pauli correspondence |
| `wilsonPlaquetteAction β q := β·(1 − reTr q)` | `Su2Haar.lean` | `S = β·Σ(1 − Re tr U_plaq)` | **to verify** — matches `Su2Curvature`'s `e^{−β·Re tr}` up to the constant shift |
| `conjInvariant f` | `Su2Haar.lean` | `Tr(g U g⁻¹) = Tr U` (gauge invariance) | **to verify** — the adjoint action must match `trace_conj_inv` |
| `su2Haar` | `Su2Haar.lean` | normalized Haar measure on SU(2) | **to synthesize** — needs `IsTopologicalGroup SU2` |
| `uniformExponentialClustering d L` | `Su2Haar.lean` | Osterwalder–Seiler strong-coupling clustering | **placeholder** — the covariance-decay statement is not yet precise |

## Non-vacuity obligations (Claude's rule)

For every theorem in this program:
1. the hypotheses must hold in an explicit example;
2. the `β = 0` case must give **independence** (the Wilson action is constant, so observables decouple).

## Kill criterion (M0)

If `IsTopologicalGroup SU2` (or the quaternion product = `Metric.unitSphere.instGroup`) cannot be
established within a few sessions, switch to the **matrix group** `SU(2) = {U : Matrix (Fin 2) (Fin 2) ℝ
// unitary}` and check compactness there — `Matrix.specialUnitaryGroup` has NO `CompactSpace` in Mathlib
v4.35.0, so the matrix route would require building it (a bigger lift).
