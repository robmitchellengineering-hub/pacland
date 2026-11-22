# SEXTANT — Plan for the Non-Perturbative Inequality

The perturbative side is complete (the scale, the controlled flow, the consistent routes). What remains
is the single non-perturbative inequality that turns "controlled flow" into "positive mass gap." This
plan is the attack on that inequality — the lemmas, the mechanism, the falsifiers, and the measure of
progress.

---

## 0. The target theorem (the one inequality)

> For lattice SU(N) Yang-Mills (N ≥ 2, d = 4), the transfer matrix has a spectral gap
> `m(β) ≥ C·e^(−cβ) > 0` for some `C > 0`, with `c = 12π²/11` (the asymptotic-freedom coefficient),
> **uniformly in volume and surviving the continuum limit.**

Proving this one statement is the Clay problem. The plan breaks it into the smallest lemmas each of
which can be formalized and falsified.

---

## 1. The mechanism (primary: Wang's criterion)

The curvature/functional-inequality route, because it is the one with the most already in the Lean tower.

**Wang's criterion** (the theorem to formalize): for a Markov process with generator `L` and
Bakry-Émery curvature `Γ₂`, if the negative-curvature region is **measure-negligible** *and* a
**Lyapunov drift** pulls the dynamics back toward the positive-curvature region, then the spectral gap
is **positive and β-uniform**.

Applied to the SU(2) 1-plaquette (S³ with the Wilson measure `e^(2β·cosθ)`), the pieces are:

| lemma | statement | status in the repo |
|---|---|---|
| W1 | the curvature is `1/4 + 2β·cosθ`, negative at the antipode θ=π iff β > 1/8 | ✅ kernel-checked (`Su2Curvature.lean` #513) |
| W2 | the negative-curvature region is the antipode — **measure-zero** on S³ | ⬜ to formalize |
| W3 | the Wilson measure concentrates on θ=0 (the trivial connection) — the **Lyapunov drift** | ⬜ to formalize |
| W4 | **Wang's theorem** itself (negligible negative curvature + drift ⇒ positive β-uniform gap) | ⬜ to formalize |

---

## 2. The phases

**Phase 1 — the 1-plaquette (formalize Wang's criterion + apply it).**
Prove W4 (the general theorem), then check W1 + W2 + W3 hold for the SU(2) 1-plaquette. Result: the
1-plaquette spectral gap is positive, β-uniformly — the first non-perturbative positivity result.

**Phase 2 — the full lattice (extend W2/W3 beyond one plaquette).**
The negative curvature stays on a measure-negligible set for the full gauge-orbit quotient, not just
one plaquette. This is the hard extension (gauge-fixing + the orbit geometry, i.e. the Gribov track).

**Phase 3 — the limits (volume + continuum).**
The gap survives V → ∞ (A1) and a → 0 (A3). The Osterwalder-Schrader reconstruction (OS3, already in
the repo #510) is the bridge; the work is proving the β-uniform gap carries through both limits.

---

## 3. The secondary mechanism (in parallel, not instead)

**Strong-coupling resummation** — extend the cluster expansion past its radius of convergence to the
exponential scale. This is the RG-track route: the flow is controlled (done), and a resummation of the
cluster expansion at weak coupling would give the exponential bound directly. Keep it as a second
programme; SEXTANT arbitrates which produces the first result.

---

## 4. The falsifiers (each lemma is testable)

- **W2** falsifier: a point other than the antipode where the curvature is negative at β > 1/8.
- **W3** falsifier: a β where the measure does *not* concentrate on θ=0 (no drift).
- **W4** falsifier: a counterexample — a process with negligible negative curvature but a vanishing gap.
- **Phase 2** falsifier: a full-lattice configuration with negative curvature on a measure-non-negligible set.
- **Phase 3** falsifier: a β-uniform lattice gap that closes in the continuum or infinite-volume limit.

---

## 5. The measurable definition of progress

Progress is **which lemma is next-proven**, not theorem count. The sequence W4 → W2 → W3 → Phase 2 →
Phase 3 is the ladder; each rung is a Lean-checked theorem, and the race records it. The one metric is
unchanged: **how much closer are we to `m(β) ≥ C·e^(−cβ)` uniformly in volume and coupling.**

---

## 6. The first concrete move

Formalize **W4 (Wang's theorem)** in Lean — it is the general tool every other rung needs, and it is a
known, citable result (Wang's spectral-gap criterion), so it is the highest-value first lemma. Then apply
it to the 1-plaquette (W1 already done).
