# Cross-species "decodability deficit" benchmark

A self-contained, runnable benchmark that measures, across many species, how much of a
behavioural (or species) label is *not* decodable from measured acoustic features. The
instrument is the **numpy-only three-check split** from `pacland/animal/learnability.py`,
vendored here with its `pacland.structure` dependency inlined so the directory runs on a
Linux box with **no further research**.

## What it runs

For every corpus in `corpora.json` the runner:

1. loads a **tabular acoustic feature table** (rows = calls/vocalisations, columns =
   measured acoustic features) plus a label column;
2. winsorises each feature (1/99), drops rows with a missing feature/label;
3. runs the three-check split: per-coordinate **mutual information** (+ permutation z),
   joint **one-vs-rest ridge 5-fold CV balanced accuracy**, and a **label-permutation
   null** z-score;
4. emits one result row per (corpus, label).

The three checks are independent and a LEARNABLE claim is made only when the arms agree
(the "Rule of Three" from the anchor corpora).

## The deficit definition

For a categorical label with `n_classes` classes, chance = `1/n_classes`, and

```
D = 1 - (balanced_accuracy - chance) / (1 - chance)
```

- `D = 0` → the label is decodable to ceiling from the acoustic features.
- `D = 1` → the classifier is at chance (no decodable structure).

`D` is reported for **referent** and **context** labels. Species / dialect / call-type
labels are **constraint** measurements and are reported as balanced accuracy + permutation
z, *not* as a deficit (they are expected to be acoustically encoded). Sequence corpora
(sperm whale) are reported separately (Zipf / temporal MI / combinatorial MDL).

## Roles

| role | report | meaning |
|------|--------|---------|
| `referent` | deficit D | behavioural referent (e.g. predator type) |
| `context` | deficit D | behavioural/social/environmental context |
| `species` / `dialect` | bal-acc + z | species identity (constraint) |
| `call-type` | bal-acc + z | call/repertoire type (constraint) |
| `sequence` | Zipf/MI/MDL | sequential (combinatorial) structure |

## Run it

```bash
python3 -m venv venv
./venv/bin/pip install numpy scipy scikit-learn pandas openpyxl
./venv/bin/python benchmark.py
```

Only `numpy`, `pandas` and `openpyxl` are actually used (`scipy`/`scikit-learn` are listed
for parity with the anchor pipeline; the instrument is numpy-only). Outputs:

- `results.json` — machine-readable rows (`corpus`, `species`, `label`, `role`, `n`,
  `bal_acc`, `chance`, `deficit`, `z`, `verdict`) plus a `sequences` block.
- `ranking.md` — deficit rows sorted by `D` ascending (most decodable first).

A corpus that fails to parse is emitted as a row with `verdict = "parse-error"` (or
`"insufficient-classes"`), never a crash.

## Anchor reproduction (verified)

| corpus | label | expected | measured |
|--------|-------|----------|----------|
| macaque (Rebout et al., Zenodo 3877581) | context | bal-acc ≈ 0.597, D ≈ 0.60 | bal-acc 0.597, D 0.605 |
| dwarf mongoose (Collier et al., Zenodo 5005321) | referent | bal-acc ≈ 1.00, D ≈ 0 | bal-acc 1.000, D 0.000 |
| sperm whale (Sharma et al., Zenodo 10817697) | sequence | LEARNABLE | LEARNABLE (Zipf α=-1.491, temporal MI=0.953, MDL z≈-104) |

## Manifest and licences

16 corpora (3 anchors + 13 additional), 20 label rows + 1 sequence corpus. All additional
corpora were downloaded from Zenodo and are **CC0-1.0** except the sperm-whale corpus
(**CC-BY-4.0**). Full per-corpus metadata (species, title, URL, DOI, licence, file md5,
feature columns, label column, role, n_classes) is in `corpora.json`.

| corpus | species | label(s) | licence |
|--------|---------|----------|---------|
| macaque | Macaque (4 spp.) | context, species | CC0 |
| mongoose | Dwarf mongoose | referent, call-type | CC0 |
| sperm-whale | Sperm whale | sequence | CC-BY-4.0 |
| meerkat-closecall | Meerkat | context, call-type | CC0 |
| shrew | Long-clawed shrew | context, call-type | CC0 |
| spotted-seal | Spotted seal | call-type | CC0 |
| capuchin | Bearded capuchin | call-type | CC0 |
| houbara | Houbara bustard | context (kinship) | CC0 |
| oriole-call | Orchard oriole complex | species | CC0 |
| oriole-song | Orchard oriole complex | species | CC0 |
| phyllodytes | *Phyllodytes luteolus* | context (noise) | CC0 |
| prairie-dog | Prairie dog | context (colony) | CC0 |
| crocodile | American crocodile | context (size class) | CC0 |
| tungara | Túngara frog | context (condition) | CC0 |
| frog-noise | Little torrent frog | context (noise) | CC0 |
| shearwater | Manx shearwater | call-type, context | CC0 |

## Notes on scope

- **Raw audio is out of scope.** Corpora that turned out to be audio-only (no published
  per-call feature table) were excluded, not counted as tabular. Examples surveyed and
  rejected as audio-only / non-tabular: the European starling song library (Zenodo
  3237218, audio zips), the bottlenose-dolphin encounter record (Zenodo 17534727 —
  whistle contours only n=15), the Antarctic minke / harbour-seal presence records
  (Zenodo 4087133 / 4985662 — passive-acoustic *detection* counts and received levels,
  not per-call spectral features), and species-mean comparative tables (arini 4955475,
  neotropical-frogs 4947661 — one row per *species*, not per call).
- Two `.xls`/grouped files were converted to clean CSVs under `data/` for the runner's
  fixed dependency set: the shrew table (`.xls` → CSV, legend columns dropped) and the
  little-torrent-frog table (merged `Group` column forward-filled).

## Vendored instrument

`learnability.py` is a byte-for-byte copy of `pacland/animal/learnability.py`
(`winsorize`, `ridge_cv_balanced_accuracy`, `ridge_cv_pearson`, `permutation_z`,
`single_coord_mi`, `referent_verdict`, `learnability_split`) with the two functions it
imported from `pacland.structure` (`mutual_information`, `mi_significance`) inlined. No
scikit-learn, no pacland import, numpy + stdlib only.
