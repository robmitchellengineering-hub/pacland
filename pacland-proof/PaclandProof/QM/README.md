# QM falsification suite — kernel-checked no-go's

The "no" side of the yes/no engine: theorems that *exclude* a class of completion, each with
the forced/free framing (forced half = the inequality/constraint, kernel-checked; free half =
what it delimits).

| no-go | excludes | forced half | status |
|---|---|---|---|
| **Bell / CHSH** | *local* hidden variables | `S ≤ 2` for deterministic ±1 assignments (`QM.CHSH.chsh_local_bound`) | ✅ kernel-checked |
| **Kochen–Specker** | non-contextual 0/1 value assignments (dim ≥ 3) | `Gleason.no_dispersion_free` (no dispersion-free measure) | ✅ kernel-checked (in the vendored Gleason proof) |
| **No-cloning** | copying an unknown quantum state | the map `v ↦ v⊗v` is not linear | ⏳ next (needs the tensor product) |
| **Tsirelson bound** | (the "yes" side) | QM saturates `S = 2√2` | ⏳ next (tensor-level computation) |

The Bell/CHSH bound is the pure locality no-go; Kochen–Specker is Gleason's finite corollary
(already in the vendored CKM proof). No-cloning and the Tsirelson bound both need the tensor
product of qubits, which is the next lift.
