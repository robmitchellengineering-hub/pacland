# Machine-checked falsification of quantum foundations

**Bell, Tsirelson, no-cloning, and Kochen–Specker, kernel-checked in Lean 4**

*Authors: the pacland proof arm · Date: 2026-11-07 · Repository: `pacland-proof/`*

**DOI:** https://doi.org/10.5281/zenodo.24027302

**Abstract.** We present machine-checked (Lean 4 / Mathlib) certificates for the main *falsification*
results of quantum foundations — the theorems that exclude a class of hidden-variable completion of
quantum mechanics. (1) **Bell's theorem**: the CHSH correlation `S = a₀b₀ + a₀b₁ + a₁b₀ − a₁b₁`
satisfies `S ≤ 2` for *local* hidden variables — both the deterministic ±1 form (a 16-case analysis,
`S = ±2`) and the general local-realism form `|a|,|b| ≤ 1` (via the sharp bound `|x+y| + |x−y| ≤ 2`).
(2) **The Tsirelson bound**: quantum mechanics saturates `S = 2√2` (Bell state + Pauli
measurements), exceeding the local bound — so locality is *violated*, not merely bounded.
(3) **No-cloning**: no linear map `T` satisfies `T v = v ⊗ v` for all `v` (the Segre map is
quadratic, not linear). (4) **Kochen–Specker**: no non-contextual 0/1 value assignment in dimension
≥ 3 (the `no_dispersion_free` corollary of Gleason). Each result is kernel-checked with zero
`sorry`/`axiom`; `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound`.

## 1. The forced/free shape

Each no-go has the same shape as the rest of the proof arm: a **forced** half (an inequality or
constraint, kernel-checked) and a **free** half (what the theorem *delimits* — it does not resolve).

| no-go | forced (kernel-checked) | free (delimited) |
|---|---|---|
| Bell / CHSH | `S ≤ 2` for local hidden variables | which side QM violates |
| Tsirelson | `S = 2√2` is attained | the specific state/measurements |
| No-cloning | `v ↦ v⊗v` is not linear | which state cannot be copied |
| Kochen–Specker | no 0/1 non-contextual assignment (dim ≥ 3) | the context that resolves it |

## 2. Result 1 — Bell's theorem (the locality no-go)

`QM.CHSH.chsh_local_bound`: for deterministic ±1 assignments, `S = (a₀+a₁)b₀ + (a₀−a₁)b₁ = ±2 ≤ 2`
(16 cases). `QM.CHSH.chsh_local_bound_general`: for `|a|,|b| ≤ 1`, `S ≤ |b₀+b₁| + |b₀−b₁| ≤ 2`,
using the sharp two-point bound `|x+y| + |x−y| ≤ 2` (proven from `abs_le`/`abs_sub_le_iff`, reducing
to the four box constraints).

## 3. Result 2 — the Tsirelson bound (the "yes" side)

`QM.Tsirelson.tsirelson_bound`: for the Bell state `|Φ⁺⟩ = (|00⟩+|11⟩)/√2` and the measurements
`A₀=σ_z, A₁=σ_x, B₀=(σ_z+σ_x)/√2, B₁=(σ_z−σ_x)/√2`, the four expectation values are
`1/√2, 1/√2, 1/√2, −1/√2`, summing to `4/√2 = 2√2`. `QM.Tsirelson.chsh_quantum_violates_local`:
`2 < 2√2`, so QM exceeds the local bound.

## 4. Result 3 — no-cloning

`QM.NoCloning.no_cloning`: no linear map `T : (Fin 2 → K) →ₗ (Fin 2 → K) ⊗ (Fin 2 → K)` satisfies
`T v = v ⊗ v` for all `v`. Linearity gives `T(e₀+e₁) = e₀⊗e₀ + e₁⊗e₁`, while cloning forces the
cross terms `e₀⊗e₁ + e₁⊗e₀`; the coordinate functional `(proj 0 ⊗ proj 1)` then multiplication
sends the sides to 1 and 0 — a contradiction in any field.

## 5. Result 4 — Kochen–Specker

`Gleason.no_dispersion_free`: no `ProjMeasure` (a non-contextual additive probability on projectors,
dimension ≥ 3) is dispersion-free — i.e., takes only 0/1 values. This is the no-go that excludes
non-contextual *value assignments*, kernel-checked as a corollary of Gleason's theorem (the CKM
descent-chain route, vendored from `Bobart0/gleason-theorem-lean` v1.0.3 and bridged to our encoding).

## 6. What this closes

Combined with the Born rule (Gleason), these four theorems close the three doors people mean when
they ask whether QM's non-determinism can be "sorted out": **non-contextuality** (Gleason/KS),
**locality** (Bell/CHSH + Tsirelson), and **copying** (no-cloning). Each is a theorem, not an
assertion — the referee is the Lean kernel. The "issues" (which outcome occurs) are provably the
*free* column, delimited not resolved.

## Reproducibility

```
cd pacland-proof && lake build          # green, 9088 jobs
# prints: contracted_bianchi / tsirelson_bound / no_cloning depend on axioms
#          [propext, Classical.choice, Quot.sound] only
```

Sources: `PaclandProof/QM/{CHSH,Tsirelson,NoCloning}.lean`, `Gleason/**` (vendored CKM proof).
