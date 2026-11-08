# Cross-species decodability benchmark

One null-modeled number — the **decodability deficit** — per species/corpus, plus the constraint
learnability. The instrument is the pacland `animal` discipline; the numbers below reproduce on a mesh
node (not just locally).

## Method

- **Three-check split** (`pacland/animal/learnability`): single-coordinate mutual information · joint
  ridge-CV · a permutation null — all three must agree (the Rule of Three).
- **Deficit** `D = 1 − (bal_acc − chance)/(1 − chance)`, `chance = 1/n_classes`. `D = 0` → the label is
  decodable to ceiling from the acoustic features; `D = 1` → at chance.
- **Roles:** `referent` / `context` → **deficit**; `species` / `dialect` / `call-type` → **constraint
  learnability** (balanced accuracy + permutation z, not a deficit); `sequence` → **Zipf / temporal MI /
  combinatorial MDL**, reported separately.
- **Falsifier pre-registered per corpus** before any number is computed: a context-free acoustic map to a
  referent at bal-acc ≥ 0.90 AND z ≥ 3 is a "Rosetta unit" and refutes the graded-deficit claim.

## Ranked table (most decodable first)

| # | species | label (role) | n | bal_acc | deficit | verdict |
|---|---------|--------------|---|---------|---------|---------|
| 1 | Dwarf mongoose (*Helogale parvula*) | referent — aerial vs terrestrial predator | 144 | **1.000** | **0.000** | REFUTED (Rosetta unit) |
| 2 | Macaque (Tonkean, crested, rhesus, Japanese) | context — social | 2520 | **0.597** | **0.605** | graded (no Rosetta unit) |

Constraint rows (not ranked as deficits): macaque `species` bal-acc 0.545 (z 33.8, LEARNABLE); mongoose
`call-type` bal-acc 0.841 (z 32.1, LEARNABLE).

Sequence corpus (separate): **sperm whale** — Zipf α = −1.49 (z −116), temporal MI 0.953 bits (z +31),
combinatorial MDL 1.23 vs 2.27 bits/coda (z −104) — all LEARNABLE.

## Honest status (what this is, and is not)

- **Corpus count is 3 today.** Permissively-licenced *tabular acoustic feature tables* with a behavioural
  label are genuinely scarce — most public bioacoustics is raw audio or spectrograms, which this tabular
  pass deliberately excludes. Curating more is in flight (realistic ~8–12, not 20–30, without adding an
  audio feature-extraction stage).
- **This is a benchmark of a method, not a new biological claim.** The mongoose referent result and the
  whale sequence structure re-derive published findings (Collier et al. 2017; Sharma et al. 2024); the
  value is the single, comparable, null-modeled number, not the discovery.
- Licences: macaque CC0-1.0, mongoose CC0-1.0, sperm whale CC-BY-4.0.

## Where it lives

- Instrument: `pacland` `discipline/animal` — `src/pacland/animal/learnability.py`.
- Runner + manifest + data: `pacland` `benchmarks/decodability/` (`benchmark.py`, `corpora.json`).
- Evidence: `REVIEWS/animal-c1-learnability.md`, `REVIEWS/animal-c1b-referent.md`, `REVIEWS/animal-c1c-sequences.md`.
- First mesh run: dispatched to `pacland-rog` 2026-11-08T0504Z (result pending).
