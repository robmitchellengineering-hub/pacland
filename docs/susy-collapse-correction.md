# CORRECTION — the "SUSY-fraction collapse" is a sampler artefact, not a landscape fact

**2026-11-14.** The headline *"the SUSY fraction collapses 27.9% → 19.7% → 1.1%"* — recorded as a
**CONFIRMED landscape fact** in `docs/UNIFICATION-STATUS.md` §"The frontier" and quoted across
`docs/sampling-frontier.md`, `docs/known-positives.md`, `docs/plan-facts.md` — is **wrong**.

## What actually happened

The corpus (`data/h12_*_stats.json`) was produced by a sampler that did **not** hold the modulus in its
own declared domain. At b3=10 (h12=4) **91% of its rows are runaway points at |z| ~ 1e29** — correctly
`is_minimum = False`, but still feeding the denominator of the quoted fraction. The "collapse" is the
runaway share growing with h12, not the SUSY vacua disappearing.

## The measurement that settles it

Two samplers, run on `pacland-rog` against the same theory:

| method | h12=4 result |
|---|---|
| `sample_critical_points(ISD−)` (`scripts/sample_h12.py`) | **0 SUSY** out of 400 candidates |
| `data_sampler` + scipy `root` (`scripts/sample_h12_ds.py`) | **547 SUSY in 177 s, 338 in-domain, 0 runaway** |

The correct sampler (`data_sampler`), at every rung, **0 runaway**:

| b3 | h12 | SUSY vacua | in-domain |
|---|---|---|---|
| 6 | 2 | 1513 | **79.0%** |
| 8 | 3 | 474 | **59.5%** |
| 10 | 4 | 547 | **61.8%** |

**No collapse — the in-domain SUSY fraction is ~60–80% and roughly flat.** The 27.9% / 19.7% / 1.1%
numbers are composition artefacts of the runaway-laden corpus.

## What is corrected

- `docs/UNIFICATION-STATUS.md` §"The frontier" — the "collapse is a landscape fact" claim is retracted.
- `docs/sampling-frontier.md` — the "collapses ~25×" statement is a sampler artefact.
- `docs/known-positives.md` — the stratified 27.9% / 20.2% / 1.2% numbers are sampler artefacts.

The effective sampler is `scripts/sample_h12_ds.py` (PR #575).

## The replacement (not just the retraction)

- **Corrected corpus**: `data/h12_2_ds.json`, `data/h12_3_ds.json`, `data/h12_4_ds.json` — the
  `data_sampler` SUSY vacua (0 runaway), added to replace the runaway-laden `data/h12_*_stats.json`.
- **Corrected analysis**: `scripts/susy_ds_fraction.py` — the in-domain SUSY fraction per b3 with a
  Wilson interval:

  | b3 | h12 | SUSY | in-domain | fraction | 95% CI |
  |---|---|---|---|---|---|
  | 6 | 2 | 1513 | 1195 | **79.0%** | [76.9%, 81.0%] |
  | 8 | 3 | 474 | 282 | **59.5%** | [55.0%, 63.8%] |
  | 10 | 4 | 547 | 338 | **61.8%** | [57.7%, 65.8%] |

  Flat (59.5%–79.0%), every interval tight (n ≥ 200) — the opposite of the retracted "collapse".
