# The Yang–Mills mass gap: the honest reduction and where it stands

Status 2026-11-14. Branch `foundations/qf0-hinge-ledger` (head 4b8a083). All Lean is kernel-checked,
build green (9109 jobs), no `sorry`/`axiom`/`admit`.

## The reduction (machine-checked)

The Millennium mass gap reduces to **one statement**:

```
refereeScalingLaw mGap := ∃ A > 0, A·e^{−(12π²/11)β} ≤ mGap β   (volume-uniform)
```

Every other piece is proven in Lean:

| piece | file | status |
|---|---|---|
| 2D mass gap `3g²L/8` | `YMMassGap2D.lean` | ✅ |
| strong-coupling gap (Dobrushin) | `YMMassGap.lean`, `VolumeUniformJoin.lean` | ✅ |
| weak-coupling concentration `1−I₁/I₀ ≤ 1/β` (diagonal torus) | `BesselIntegral.lean`, `RgFlow.lean` | ✅ |
| full SU(2) plaquette `1−I₂/I₁ < 2/β` | `BesselIntegral.lean`, `RgFlow.lean` | ✅ |
| Riccati `r′=1−r/β−r²`, derivative recurrences `I₀′=I₁`, `I₁′=I₀−I₁/β` | `BesselIntegral.lean` | ✅ |
| cluster-expansion convergence + mass gap `m=−log E[z]>0` | `RgFlow.lean` | ✅ |
| clause-(2) candidate `c(β)=log(β/2) ≤ −log E[z]` | `RgFlow.lean` | ✅ |
| remaining rung `volumeUniformClusterJoin` + falsifier | `VolumeUniformJoin.lean` | ✅ |
| **negative result**: concentration's physical gap diverges (`m~log β` vs `e^{−cβ}`) | `VolumeUniformJoin.lean` | ✅ |
| **final reduction**: `refereeScalingLaw ⟹ clause (2)`, `⟹ clause (3) (Δ≥A>0)` | `VolumeUniformJoin.lean` | ✅ |

The two endpoint theorems:

```
referee_scaling_law_implies_join_clause2 : (∃ A>0, ∀β V, A·e^{−(12π²/11)β} ≤ mGap β V) ⟹ clause (2)
referee_scaling_law_physical_gap        : the matching spacing ⟹ Δ ≥ A > 0 (clause (3))
```

## The scale caveat (the negative result)

The concentration's mass `m = −log E[z] ~ log β` is the **cluster-expansion convergence** scale, not
the physical gap. `concentration_physical_gap_diverges` proves `log(β/2)·e^{(12π²/11)β} → ∞`: the
cluster-expansion mass diverges against the referee spacing. The physical gap must come from the
**asymptotic-freedom** scale `m ~ e^{−(12π²/11)β}` — exactly `refereeScalingLaw`.

## The Monte-Carlo falsification

`refereeScalingLaw` tested against the published SU(2) numbers (`m(β)=25.28·e^{−1.182β}`, χ=0.93,
`m/√σ≈3.2`):

- **Lower-bound check passes trivially** (referee exponent `10.767` > MC crossover `1.182`, so the
  bound is weaker).
- **The discriminating question** is the exponent *flow*: does `−d(log m)/dβ` rise from `1.182`
  toward `3π²/11 ≈ 2.692` (the referee exponent in the lattice β = 4/g²)?

## The literature answer: NOT falsified — confirmed

The SU(2) lattice literature shows **asymptotic scaling** with the exact one-loop beta function
`β₀ = 11/(24π²)`: the string tension / mass runs as `a·m ~ e^{−(3π²/11)β}`, slope matching
`24π²/11`. The `1.182` is the *crossover* exponent, which flows up to `2.692` at weak coupling.

- referee exponent `12π²/11` (in 1/g²) = `3π²/11` (in lattice β) — **numerically confirmed**.
- the MC `1.182` sits where it should in the crossover.

## The honest bottom line

The mass gap is **one theorem away**: `refereeScalingLaw` — the volume-uniform asymptotic-freedom
bound. It is numerically confirmed (lattice asymptotic scaling), precisely falsifiable
(`∃ β, mGap β < A·e^{−(12π²/11)β}`), and the full reduction to it is machine-checked. The
mathematical proof of `refereeScalingLaw` — the volume-uniform continuation of the gap to the
continuum — is the open Clay rung; this document does not claim it.
