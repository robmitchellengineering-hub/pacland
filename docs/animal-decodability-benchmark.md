# Cross-species decodability benchmark

One null-modeled number — the **decodability deficit** — per species/corpus, plus the constraint
learnability. 16 corpora, 20 label rows, 1 sequence corpus. The numbers below reproduce on a mesh node.

## Method

- **Three-check split** (`pacland/animal/learnability`): single-coordinate mutual information · joint
  ridge-CV · a permutation null — all three must agree (the Rule of Three).
- **Deficit** `D = 1 − (bal_acc − chance)/(1 − chance)`, `chance = 1/n_classes`. `D = 0` → the label is
  decodable to ceiling from the acoustic features; `D = 1` → at chance.
- **Roles:** `referent` / `context` → **deficit**; `species` / `dialect` / `call-type` → **constraint
  learnability** (balanced accuracy + permutation z); `sequence` → **Zipf / temporal MI / combinatorial
  MDL**, reported separately.
- **Falsifier pre-registered per corpus** before computing: a context-free acoustic map to a referent at
  bal-acc ≥ 0.90 AND z ≥ 3 is a "Rosetta unit" and refutes the graded-deficit claim.

## Ranked deficit table (most decodable first)

| # | species | label | n | bal_acc | deficit | verdict |
|---|---------|-------|---|---------|---------|---------|
| 1 | Dwarf mongoose | referent (aerial/terrestrial predator) | 144 | **1.000** | **0.000** | REFUTED (Rosetta unit) |
| 2 | American crocodile | context | 88 | 0.843 | **0.236** | graded |
| 3 | Prairie dog | context | 4138 | 0.718 | **0.423** | graded |
| 4 | Macaque (4 spp) | context (social) | 2520 | 0.597 | **0.605** | graded |
| 5 | Manx shearwater | context | 508 | 0.651 | **0.698** | graded |
| 6 | Little torrent frog | context (noise) | 35 | 0.429 | **0.714** | graded |
| 7 | Túngara frog | context (condition) | 445 | 0.640 | **0.719** | graded |
| 8 | Houbara bustard | context (kinship) | 478 | 0.502 | **0.747** | graded |
| 9 | Phyllodytes tree frog | context (noise) | 39 | 0.614 | **0.771** | uniform (within null) |
| 10 | Meerkat | context (close-call) | 2237 | 0.245 | **0.906** | graded |
| 11 | Long-clawed shrew | context | 4243 | 0.142 | **0.981** | graded |

**The spectrum is real, not binary.** Referential signals sit at D ≈ 0 (a Rosetta unit *exists* where
communication is functionally referential); graded social context spans the middle; weakly-informative
context (shrew) sits at D ≈ 0.98. That is the corrected thesis, now a measured ranking.

## Constraint learnability (species / call-type — not deficits)

LEARNABLE: macaque species 0.545 · mongoose call-type 0.841 · meerkat call-type 0.245 (z 51) · shrew
call-type 0.659 (z 272) · spotted-seal call-type 0.588 · capuchin call-type 0.513 · **oriole *calls*
species 1.000** (z 4.3).

Uniform: **oriole *songs* species 0.605 (z 1.3)** — calls separate the species, songs do not (the source
paper's own title); **Manx shearwater call-type 0.052 (z 0.6)** — yet its *context* is graded at 0.651.

## Sequence corpus (separate)

**Sperm whale** — Zipf α = −1.49 (z −116), temporal MI 0.953 bits (z +31), combinatorial MDL 1.23 vs
2.27 bits/coda (z −104) — all LEARNABLE.

## Honest status

- **16 corpora, not 20–30.** Permissively-licenced *tabular* acoustic feature-tables with a behavioural
  label are scarce; this is the real per-call tabular count (audio-only and species-*mean* tables were
  found and excluded, not fabricated). Reaching more species needs a raw-audio feature-extraction stage.
- **This is a benchmark of a method, not a new biological claim** — the mongoose referent and whale
  structure re-derive published findings; the value is the single, comparable, null-modeled number.
- Licences: 15 × CC0-1.0, 1 × CC-BY-4.0 (sperm whale). Full per-corpus metadata (URL, DOI, md5) is in
  `corpora.json`.

## Where it lives

- Instrument: `pacland` `discipline/animal` — `src/pacland/animal/learnability.py`.
- Runner + manifest + data: `pacland` `benchmarks/decodability/` (`benchmark.py`, `corpora.json`, `data/`).
- Evidence: `REVIEWS/animal-c1-learnability.md`, `REVIEWS/animal-c1b-referent.md`, `REVIEWS/animal-c1c-sequences.md`.
- Mesh run: `pacland-rog` (3-corpus pass); full 16-corpus re-run dispatched.
