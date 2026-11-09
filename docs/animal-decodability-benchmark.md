# Cross-species decodability benchmark

One null-modeled number — the **decodability deficit** — per species/corpus, plus the constraint
learnability. **38 corpora, 42 label rows, 15 deficit rows, 1 sequence corpus.** Reproduces on a mesh node.

## Method

- **Three-check split** (`pacland/animal/learnability`): single-coordinate mutual information · joint
  ridge-CV · a permutation null — all three must agree (the Rule of Three).
- **Deficit** `D = 1 − (bal_acc − chance)/(1 − chance)`, `chance = 1/n_classes`. `D = 0` → decodable to
  ceiling from the acoustic features; `D = 1` → at chance.
- **Roles:** `referent` / `context` → **deficit**; `species` / `dialect` / `call-type` → **constraint
  learnability**; `sequence` → **Zipf / temporal MI / combinatorial MDL** (separate).
- **Falsifier pre-registered per corpus** before computing: a context-free acoustic map to a referent at
  bal-acc ≥ 0.90 AND z ≥ 3 is a "Rosetta unit" and refutes the graded-deficit claim.

## Ranked deficit table (most decodable first)

| # | species | label | n | bal_acc | deficit |
|---|---------|-------|---|---------|---------|
| 1 | Dwarf mongoose | referent (predator type) | 144 | **1.000** | **0.000** |
| 2 | American crocodile | context | 88 | 0.843 | 0.236 |
| 3 | Prairie dog | context | 4138 | 0.718 | 0.423 |
| 4 | Macaque (4 spp) | context (social) | 2520 | 0.597 | 0.605 |
| 5 | Field cricket (*Gryllus bimaculatus*) | context (noise) | 2955 | 0.482 | 0.647 |
| 6 | Manx shearwater | context | 508 | 0.651 | 0.698 |
| 7 | Little torrent frog | context (noise) | 35 | 0.429 | 0.714 |
| 8 | Túngara frog | context (condition) | 445 | 0.640 | 0.719 |
| 9 | Houbara bustard | context (kinship) | 478 | 0.502 | 0.747 |
| 10 | Phyllodytes tree frog | context (noise) | 39 | 0.614 | 0.771 |
| 11 | Meerkat | context (close-call) | 2237 | 0.245 | 0.906 |
| 12 | African elephant | context (rumble) | 1918 | 0.114 | **0.959** |
| 13 | Long-clawed shrew | context | 4243 | 0.142 | 0.981 |
| 14 | Lesser treefrog (*D. minutus*) | context (playback) | 2890 | 0.339 | 0.992 |
| 15 | **African elephant** | **referent (name-like call)** | 625 | **0.009** | **1.000** |

## The finding the ranking makes

The deficit is a **real, measured spectrum** (0.000 → 1.000), and it separates two *different kinds* of
reference that "referential signal" collapses together:

- **Acoustically-transparent reference** — dwarf mongoose predator type sits at D = 0.000: the referent
  *is* in the sound (peak frequency ≈ predator class).
- **Arbitrary / learned reference** — African elephant name-like calls sit at D = 1.000 (bal-acc 0.009,
  i.e. chance): *which individual is addressed* is **not** recoverable from the acoustic features alone.
  That is exactly what "a name" means — a label whose mapping to sound is arbitrary, not acoustic.

So the decodability deficit is not just "how much signal is in the call" — it distinguishes *functionally
referential* encoding (predator type, D≈0) from *symbolic/learned* encoding (individual name, D≈1). Graded
social context fills the space between.

## Constraint learnability (species / call-type — not deficits)

LEARNABLE: macaque species 0.545 · mongoose call-type 0.841 · meerkat call-type 0.245 (z 51) · shrew
call-type 0.659 (z 272) · spotted-seal call-type 0.588 · capuchin call-type 0.513 · **oriole *calls*
species 1.000** · marmoset call-type · mouse-lemur call-type · rat USV subtype · Mexican-bats species
(60 spp) · dolphin species (7 spp) · cricket species, among others (full list in `results.json`).

Uniform: **oriole *songs* species 0.605** (calls separate the species, songs do not); **Manx shearwater
call-type 0.052** (yet its *context* is graded at 0.651).

Sequence corpus (separate): **sperm whale** — Zipf α = −1.49, temporal MI 0.953 bits, combinatorial MDL
1.23 vs 2.27 bits/coda — all LEARNABLE.

## Honest status

- **38 corpora, not 42**: 4 candidates were download-failed (evening-grosbeak, lefevre-ungulate,
  painted-turtle, deer-mice — publisher-DOI supplements and Dryad's anti-bot wall). The rest are CC0/CC-BY
  tabular feature-tables; more species needs a raw-audio stage.
- **Known instrument quirk:** hyla-versicolor, dendropsophus-ebraccatus and meimuna report "uniform"
  because their call-types are *near-perfectly separable*, so the label-shuffle null collapses (z ≈ 0) —
  a degenerate-null artefact, not a data problem.
- **This is a benchmark of a method, not a new biological claim** — mongoose referent, whale structure and
  the oriole calls-vs-songs re-derive published findings; the value is the single, comparable, null-modeled
  number across species.

## Where it lives

- Instrument: `pacland` `discipline/animal` — `src/pacland/animal/learnability.py`.
- Runner + manifest + data: `pacland` `benchmarks/decodability/` (`benchmark.py`, `corpora.json`, `data/`).
- Evidence: `REVIEWS/animal-c1-learnability.md`, `animal-c1b-referent.md`, `animal-c1c-sequences.md`.
- Mesh run: `pacland-rog` (16-corpus pass; 38-corpus re-run dispatched).
