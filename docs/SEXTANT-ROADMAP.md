# SEXTANT — consolidated roadmap (assessed from Rob's messages)

North star: **Milestone 3** — a *new* uniform analytic bound (or a new cross-structure connection),
independently verified, more significant than another thousand simulation runs.

## What SEXTANT is (the five engines, one architecture)

Mathematical (search + prove) · Computational (simulate + test) · Empirical (real datasets) ·
Knowledge (scientific record) · Supervisory (allocate + choose next frontier) — all through **one
common evidence and claim architecture**.

Every claim carries: statement · explicit assumptions · proposed proof · computational test ·
counterexample search · Lean certificate · record of what remains unproved. SEXTANT must be able to
say **"this direction failed"** — and log it.

## The five milestones (Yang–Mills mass gap)

1. Reproduce reliable SU(2)/SU(3) lattice spectral results — **tools exist** (`lattice_ym_su2/su3`,
   `glueball`).
2. Demonstrate controlled continuum scaling — **partial** (m/√σ at two couplings).
3. **Discover a new uniform analytic bound** — **OPEN** (the key original contribution).
4. Prove the bound survives infinite-volume + continuum limits — partial lemmas, no new bound yet.
5. Construct the quantum theory + positive physical gap — the destination.

## Work plan

### DONE — P0 (validated end-to-end)

- [x] **P0 — Fix autonomous challenge wiring.** Challenge sequence no longer rejects tested candidates
      (lookup by falsifier key, not candidate id; assumptions + the runner's falsifier result threaded).
      PR #625.
- [x] **P0 — End-to-end autonomous test.** `tests/test_end_to_end.py`: proposal → falsify → gate →
      evidence, asserts a tested survivor is not gated-out. PR #625.
- [x] **Registry rebuild protection.** `registry.add` upserts by id (bumps version); `ingest_all` no
      longer clears — re-ingestion preserves accumulated evidence (discoveries, negatives, provenance).
      PR #625.

### NEXT — P1 (in order)

- [ ] **P1 — Unify memory + registries.** One evidence/claim architecture: the runner's JSONL stores
      (memory, discoveries, rejected) and the five registries become one queryable substrate with the
      full claim checklist + a first-class "failed direction" record. Prereq for everything else.
- [ ] **P1 — Generalise transfer verification.** Verify *arbitrary* cross-field mappings, not just the
      hand-coded ones (the 282 sourced unifications become a test suite; new mappings get a verifier).
- [ ] **P1 — Strengthen blind benchmarks.** Prove genuine novelty beyond recall (the M3 yardstick):
      a candidate is "new" only if it is not already in the known-unifications library *and* survives a
      web-novelty check *and* a real falsifier.

### THEN — P2

- [ ] **P2 — Expand field specialists.** One field proven effective before scaling to many.
- [ ] **P2 — Supervisor + deployment.** Continuous autonomous operation (resource allocation, missing-
      lemma detection, failed-approach tracking, frontier selection).

### The M3 build (the north star)

A **bound-discovery loop**: cross-field unifications + proven Lean lemmas → candidate analytic bounds →
constraint-first filter → referee test (`verify_mass_gap_scaling`, m(β)=25.28·e^(−1.182β)) → record
survivors *and* honest failures. This is where the five engines first earn their keep together.

## Status

P0 delivered (PR #625). Next step: **P1 — unify memory + registries** (the one common evidence/claim
architecture), which is the substrate the benchmark and the M3 loop both build on.
