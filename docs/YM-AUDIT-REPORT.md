# Yang–Mills formalization landscape — audit report v1

Version 1 · 2026-11-17 · pacland worktree @ `b5761ac` · author: pacland audit session

This is the versioned report for Michael Douglas (LGT) and the Gross committee's repo
(`yang-mills-group/OpenAI-YM-20261028`). It consolidates three audits: the strong-coupling result (LGT),
the existence claim (the committee repo), and the draft mass-gap statement (`MassGapSpec.lean`).
Every claim below is grounded in the source files read, not in secondary reports.

---

## 1. Strong coupling (IR end) — DONE, verified

**`mrdouglasny/lgt`** (Douglas + Rajasekaran) proves the d ≥ 2 strong-coupling mass gap:

- `ym_mass_gap_exponential_decay` + `ym_mass_gap_rate_exists` — U(n) Wilson lattice gauge theory on
  (ℤ/Nℤ)^d, d ≥ 2, β < 1/(32n(d−1)), via the Dobrushin method (Chatterjee 2026 Ch. 16).
- **Zero sorries, zero project axioms** — `#print axioms` = `{propext, Classical.choice, Quot.sound}`.
- **Independently verified by the Lean FRO comparator** at commit `ec975bd` ("Lean default kernel
  accepts the solution").
- Source-level check (`StrongCoupling.lean`): `ym_mass_gap_strong_coupling` is a real theorem with a
  full proof — it discharges ~20 measure-theoretic hypotheses and leaves only the genuinely-hard
  analytic ones (representation continuity, the Dobrushin influence bound, the caller distance). The
  hard core is `gibbsCondMeasure_cylinder_ratio` (the strong-coupling influence bound).

**Status: the IR/strong-coupling mass gap is done.** Any new work should adopt this, not re-derive it.
The open end is the `Bridge/` (TRG → Dobrushin), whose fields are still hypotheses.

## 2. Existence — claimed, with two fidelity gaps

**`yang-mills-group/OpenAI-YM-20261028`** (the Gross committee's repo, 9,477 files): the headline
`JointExistence` is a real, detailed formalization (Wightman axioms W0–W3 + the Wilson lattice +
continuum limit + reconstruction). The public statement files lint clean; 0 axioms; the only `sorry` is
the challenge placeholder.

**But two clauses are weaker than Clay's existence statement:**

1. **The running coupling is not pinned to Yang–Mills.** `WilsonRegularity.running` only requires
   `β/log(1/mesh) → slope` for **some positive slope** — the slope is free, not the YM beta-function
   value `11C₂/(48π²)`. ("MS-bar matching out of scope" per the README.) This is the biggest gap: the
   asymptotic-freedom clause (Clay's clause 2) is reduced to "runs with *some* log".
2. **Subsequence-only, non-unique limit.** `JointExistence` = `∃ C … ∀ p, ∃ q (subsequence), ∃ T`.
   The theory is constructed along a subsequence with no uniqueness of the infinite-volume limit.

**Faithful:** the Wilson family is the plain Wilson action × product Haar (no hidden parameters); the
Wightman clauses (`uniqueVacuum`, `acts` non-zero field, `injective`/`covers`/`represents`, `mixture`)
and the non-freeness test (`TraceTest.excludes`) force a non-trivial structure.

**Verdict: even if the kernel proof is accepted, the claim establishes a YM-flavored relativistic QFT
along a subsequence — not the full Clay existence clause.**

## 3. The mass gap — untouched, draft statement reviewed

The committee's `WightmanTheory` carries the projection-valued `energyMomentum` measure, so a spectral
mass-gap statement needs no new structures. `MassGapSpec.lean` drafts it:

- `HasEnergyGap := ∃ Δ > 0, projection {p ≠ 0 ∧ time p < Δ} = 0` — **this is Clay's "spectrum of H on
  the vacuum complement ⊂ [Δ, ∞)", given W0's unique vacuum.** (Review Q1: yes.)
- `HasMassGap` — the Lorentz-scalar form, correctly excluding massless particles on the light cone.

**Two weakenings, flagged for the experts:**

- **Subsequence (Q3):** `JointExistenceWithGap` inherits the committee's subsequence quantifier, so the
  gap holds "for some limit along some subsequence", not the full limit. Recommend quantifying over
  every limit point.
- **Selected phase (Q4):** `T.theory` is the theory for the *selected* character, while `Reconstructed.mixture`
  makes the phase measure a mixture. The gap binds only one phase; Clay's gap is a property of the theory
  (every phase).

**Sanity controls to build (Q5):** (a) trivial Hilbert space passes `HasEnergyGap` but fails `Properties`;
(b) massless free field (joint spectrum on the light cone) must fail `HasMassGap`.

## 4. The open front — the crossover

The single genuinely-open piece connecting the two proven/claimed ends is the **crossover** (β from
strong to weak coupling, the continuum limit):

- LGT's `Bridge/` (EKR tensor-RG certificate → Dobrushin mass gap) — fields still hypotheses.
- A multiscale Bakry–Émery criterion via the Polchinski equation (done for sine-Gordon β < 6π, not for
  gauge theory).
- Computer-assisted block-spin RG region (done for 2D Ising/XY, not for 4D gauge).

**Recommendation:** aim new formalization at the crossover — gauge-theory TRG certificates + the
Polchinski–Bakry–Émery criterion for gauge measures — and treat LGT as the strong-coupling foundation
to build on, not re-derive.

---

## Review questions for the recipients

1. Is `HasEnergyGap` (as drafted in `MassGapSpec.lean`) exactly Clay's mass-gap clause given the unique
   vacuum — and should the gap be stated for every phase or just the selected character?
2. Does the committee's subsequence-only + non-unique limit need strengthening to "every limit point" to
   meet Clay's existence clause?
3. Does `WilsonRegularity.running` need to pin the slope to the YM beta function (currently it does not)?
4. Are the proposed sanity controls (trivial model, massless free field) the right negative tests?
