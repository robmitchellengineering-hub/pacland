# The Yang–Mills Mass Gap — a Proposed Resolution

**Status: a falsifiable proposal, not a theorem.** The matching at the crossover (§3) is not yet
proven. This document states the idea precisely, says what it would mean, and lists exactly what a
proof must establish.

---

## 1. The proposal, in one paragraph

The Yang–Mills mass gap is **not one inequality — it is a matching.** The theory has a single coupling
that runs from weak to strong, and the mass gap is the scale where its two effective descriptions meet:

- **ultraviolet** (weak coupling, `a → 0`): the theory is asymptotically free — a nearly-Gaussian
  measure whose Bakry–Émery curvature `1/4 + 2β·cos θ` is positive except on a measure-negligible
  antipode (Wang's criterion);
- **infrared** (strong coupling, `V → ∞`): the theory confines — the Wilson loop's area law, with
  V-independent clusters (the cluster expansion).

The mass gap `m(β, V, a)` is the **matched envelope** of the two:

```
m(β, V, a) ≥ max( m_strong(β),  m_weak(β) )
```

uniform in volume `V`, surviving the continuum `a → 0`.

---

## 2. The two mechanisms (what they are, where they are)

| regime | mechanism | the bound | status |
|---|---|---|---|
| UV (weak coupling) | Gaussian comparison — Bakry–Émery + Wang | `Γ₂(f) ≥ (1/4 + 2β·cos θ)·Γ(f)` → `m_weak(β)` | abstract theorems proven (`BakryEmery`, `WangCriterion`, `Su2Curvature`); the Bochner formula is in progress (`BochnerProof`) |
| IR (strong coupling) | cluster expansion | `m_strong(β) = −log u(β)`, V-independent | proven (`ClusterExpansion`, `ClusteringGap`); computed in `find_K` — valid for β ≤ ~4 |

Neither alone suffices: `find_K` proved the cluster expansion *exceeds* the true gap at weak coupling,
and the Gaussian comparison is a finite-plaquette result that has not yet been carried to `V → ∞`.

---

## 3. The matching — the genuinely new mathematics

The resolution is the claim that the two bounds **glue** at a crossover `β₀`:

1. `m_strong` is a valid lower bound on `(−∞, β₀]` — strong coupling, V-uniform (proven);
2. `m_weak` is a valid lower bound on `[β₀, ∞)` — weak coupling, continuum (needs the Bochner formula);
3. **the match** — the two meet at `β₀` with no gap, and the envelope `max(...)` is **uniform in `V`**
   and **survives `a → 0`**.

That third obligation *is* the renormalization-group statement: **the two effective descriptions agree
at the crossover, uniformly in the regulators.** It is the open step, and it is where the Clay problem
lives.

---

## 4. What it means, if true

1. **It explains the hardness.** The mass gap is hard *because* it is a matching problem: no single
   mechanism (cluster expansion, or Gaussian comparison alone) covers both ends of the coupling.
2. **It unifies two phenomena.** Asymptotic freedom (the UV) and confinement (the IR) are revealed as
   two ends of *one* renormalization-group flow, meeting at the mass gap.
3. **It is falsifiable.** Each of the three obligations in §3 can fail — a wrong crossover, a V-dependent
   envelope, or a gap that closes in the continuum — which is what makes the proposal a scientific claim
   rather than a slogan.

---

## 5. The honest boundary

Everything in §2 is either proven in the QM tower or in active iteration. §3.3 — the uniform matching
at the crossover — is **not proven**. This document is the proposed *reason* for the mass gap and the
map of its proof, not the proof itself.
