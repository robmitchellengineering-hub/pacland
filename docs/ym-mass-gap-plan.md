# Yang-Mills mass gap — the plan (post research fan-out, 2026-11-12)

The residual open sentence (from the hypothesis engine): **non-Abelian YM has exponential clustering
at weak coupling (β → ∞) in d ≥ 3.** This file is the roadmap to attack it, built from a 5-way
research fan-out. It records PROVEN vs OPEN precisely so the next session does not re-derive it.

## The exact state (verified against the literature)

| result | status | source |
|---|---|---|
| strong-coupling mass gap, d ≥ 2 | PROVEN (lattice) | Osterwalder–Seiler 1978; machine-checked `lgt` |
| 2D exact mass gap `g²(N²−1)/(4N)` | PROVEN, **unformalized** | Migdal 1975, Witten 1991, Gross–Taylor 1993 |
| 2D existence mass gap (all β) | PROVEN (Doeblin) | `lgt/MassGap2D.lean` (sorry-free) |
| UV stability + continuum *existence*, d=3,4 | PROVEN | Balaban 1984–1989 |
| **weak-coupling mass gap, d ≥ 3** | **OPEN (the Clay problem)** | — |
| clustering ⟺ transfer-operator gap | machine-checked, **abstract** | Eriksson 2026 (AIRR) — no RP/transfer-operator for YM yet |
| Dobrushin ceiling | `β_W < 2/9` at d=4, `m = −log(6(d−1)|β|)` | Bhattacharjee–Bhattacharya 2026 |

## The wall (precise)

The weak-coupling cluster expansion fails because the **gauge orbit's flat directions are
non-compact** (the trivial connection's gauge orbit `G^{|V|−1}` diverges in infinite volume) — not a
technicality, and Gribov–Singer says no global non-Abelian gauge fixing exists. So the low-temperature
cluster expansion has no compact "soft-mode" target, unlike O(N) spin models. Balaban's answer was a
**multiscale RG in axial gauge** — which gives stability, not a mass gap.

**The move**: (1) formalize every SOLVABLE non-Abelian mass gap (2D exact), (2) build the
gauge-respecting machinery (axial-gauge multiscale RG) as the next formalization target, (3) keep the
d ≥ 3 weak-coupling mass gap as the explicit open endgame.

## Milestones (in order — each is shippable and none fakes the Clay problem)

### M1 — the exact 2D SU(N) mass gap (PROVABLE, greenfield)
Formalize the heat-kernel result:
```
Z(h,A) = Σ_R (dim R)^{2−2h} exp(−(g²A/2) C₂(R))
σ_F    = g²(N²−1)/(4N),   m_gap = g²L(N²−1)/(4N)
```
Sub-steps: (a) SU(N) Casimirs + dim R; (b) the partition-function sum; (c) the exact mass gap
`m = g²L·C₂(fund)`. This is the first *explicit, non-Abelian, all-β* mass gap in Lean.

### M2 — apply the clustering ⟺ gap bridge to YM
The Eriksson bridge (Thm 5.1) is abstract. To apply it to lattice YM, formalize the missing pieces:
reflection positivity of the Wilson measure (OS3) + the transfer-operator `T = e^{−H}` + a dense
gauge-invariant observable family. Then "exponential clustering ⇒ spectral gap" becomes a YM theorem,
not just an abstract one.

### M3 — the weak-coupling attack (the endgame)
Build toward a gauge-respecting low-temperature expansion (axial gauge, multiscale RG — Balaban's
program, reconstructed by Dimock 2013–14). This is the actual Clay attack; M1 + M2 are its scaffolding.

## Next action
M1 step (a): formalize SU(N) Casimirs + the fundamental/adjoint `C₂` in Lean, then the heat-kernel
partition function. Sources: Migdal 1975, Witten 1991 (CMP 141, 153), Gross–Taylor hep-th/9301068.
