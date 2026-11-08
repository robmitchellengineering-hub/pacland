# Roughness → aversive: the cross-mammal (ungulate) check

**Question.** Does the corrected multi-band MPS roughness (`roughness_proper`, `extract_roughness.py` reused **unchanged**) predict the **aversive** category in **animal vocalisations**, as it does in real human voices (RAVDESS: aversive rougher, d = +0.83, AUC = 0.724)? This is the cross-mammal confirmation on the ungulate valence set.

## 1. What was downloaded and used

- **Source:** Zenodo record **14636641** — "Machine Learning Algorithms Can Predict Emotional Valence Across Ungulate Vocalizations" (Lefèvre, Sypherd & Mandel-Briefer), DOI `10.5281/zenodo.14636641`, license **CC-BY-4.0**.
- **SoundsDatabase.zip** — 286,854,334 bytes, MD5 `46a08a874f8b0b57cc2bbd1d5286bfef` (matches the record's checksum `46a08a874f8b0b57cc2bbd1d5286bfef`). 3,181 WAV files.
- **Data S1.xlsx** — the repartition sheet (animal ID, species, call type, valence, context, n calls, reference). Used to confirm species/valence counts; valence is read from the filename's own field, which matches exactly.

### Corpus composition (all 3,181 files, parsed from filenames)

| species | Negative | Positive |
|---|---|---|
| cattle | 1179 | 75 |
| goat | 268 | 93 |
| horse | 200 | 77 |
| pig | 316 | 248 |
| przewalski_horse | 45 | 22 |
| sheep | 342 | 54 |
| wild_boar | 158 | 104 |

The valence field is imbalanced (2,508 Negative vs 673 Positive), so a balanced subset is drawn.

### Subset selected (balanced, species-balanced by design)

200 Negative + 200 Positive = 400 WAVs. Spread **evenly** across all 7 species (cattle, sheep, goat, horse, pig, wild boar, Przewalski's horse) and, within each species, across animal IDs (round-robin), so neither a single species nor a single animal dominates the valence contrast. Seed 0; reproducible.

| species | n Negative | n Positive | mean roughness (Neg) | mean roughness (Pos) |
|---|---|---|---|---|
| cattle | 29 | 30 | 0.0594 | 0.0681 |
| goat | 29 | 29 | 0.0897 | 0.0774 |
| horse | 29 | 29 | 0.0753 | 0.0870 |
| pig | 28 | 31 | 0.2461 | 0.2704 |
| przewalski_horse | 28 | 22 | 0.0787 | 0.0970 |
| sheep | 29 | 28 | 0.0630 | 0.0737 |
| wild_boar | 28 | 31 | 0.1591 | 0.2815 |

## 2. Per-valence roughness (RAW, as specified)

| valence | mean roughness_proper | std | n |
|---|---|---|---|
| Negative (aversive) | **0.1094** | 0.1027 | 200 |
| Positive (affiliative) | **0.1406** | 0.1804 | 200 |

## 3. Statistics (RAW)

| statistic (roughness_proper) | value | p |
|---|---|---|
| Mann–Whitney U (Negative > Positive, the predicted direction) | U = 18473.0 | 0.907 |
| Mann–Whitney, two-sided | — | 0.187 |
| Cohen's d (Negative − Positive) | **-0.21** | — |
| ROC AUC (Negative = positive class) | **0.462** | one-sided 0.911 (reversal 0.090); 2000-perm null |
| point-biserial r (rougher → Negative) | -0.106 | 0.034 |

**The raw result is a REVERSAL, not a confirmation:** Positive (affiliative) calls score *rougher* than Negative (aversive) calls (d = −0.21; AUC = 0.46, i.e. below chance in the predicted direction). The point-biserial correlation is significant (p = 0.034) but **negative** — higher roughness tracks *affiliative*, the opposite of the human finding. But this reversal does not survive a duration check, below.

## 4. The duration confound (the reversal is an artefact)

`roughness_proper` is strongly **anti-correlated with clip duration** in this set (Pearson r = -0.375 over 400 files): the shorter the clip, the higher the scored roughness. The extractor trims 150 ms from each end of every channel envelope, so a ~0.3 s clip is left with only ~0.02 s of usable modulation signal — its 30–150 Hz band is a handful of unstable FFT bins, not a roughness estimate. Truncating one and the same signal and re-scoring it shows the value blowing up and becoming non-monotonic below ~1 s:

- `99048-WildBoar-AgonisticInteractions-Negative-3179.wav` (full 4.28 s → roughness 0.083):
  0.2s→0.074, 0.3s→0.000, 0.4s→0.112, 0.5s→0.124, 0.6s→0.127, 0.8s→0.119, 1.0s→0.074, 1.5s→0.069, 2.0s→0.077, 3.0s→0.073
- `31-Pig-FoodAndToys-Positive-303.wav` (full 0.33 s → roughness 0.978):
  0.2s→0.112, 0.3s→0.000

The short clips are not evenly spread across valence: Positive (affiliative) calls — pig `FoodAndToys` grunts and wild-boar `FoodAnticipation`/`Affiliative` calls — are systematically ~0.3 s long (52 Positive vs 29 Negative clips under 0.5 s). The handful of near-1.0 'very rough' values in the raw analysis are almost all these short Positive clips (see the top of the CSV). The reversal is therefore an artefact of the extractor on short clips, not a property of affiliative sound.

### Statistics with short clips removed

| min duration kept | n Neg | n Pos | mean Neg | mean Pos | Cohen's d | AUC | MW p (Neg>Pos) |
|---|---|---|---|---|---|---|---|
| ≥ 0.4 s | 179 | 161 | 0.0955 | 0.1002 | -0.056 | 0.495 | 0.567 |
| ≥ 0.5 s | 171 | 148 | 0.0876 | 0.0842 | +0.054 | 0.511 | 0.372 |
| ≥ 0.6 s | 160 | 138 | 0.0804 | 0.0771 | +0.069 | 0.507 | 0.413 |
| ≥ 0.8 s | 129 | 120 | 0.0734 | 0.0766 | -0.072 | 0.480 | 0.703 |
| ≥ 1.0 s | 116 | 94 | 0.0707 | 0.0782 | -0.167 | 0.457 | 0.859 |

Once clips shorter than ~0.5–0.6 s are dropped, the valence difference collapses to noise (d ≈ 0, AUC ≈ 0.5, Mann–Whitney n.s. in both directions).

## 5. Bottom line — does roughness → aversive hold in animals?

**No. There is no cross-mammal confirmation.** In the ungulate valence set, the corrected multi-band MPS roughness does **not** separate aversive (Negative) from affiliative (Positive) vocalisations. Taken at face value the sign is *reversed* (Positive is rougher, d = −0.21, AUC = 0.46), and that reversal is itself an artefact: roughness here is driven by clip duration (r = −0.38), short affiliative clips score spuriously high, and after removing clips shorter than ~0.5 s the effect is gone (d ≈ 0, AUC ≈ 0.5).

So the human-voice finding (RAVDESS d = +0.83, AUC = 0.72) does **not** generalise to these mammals. Either the roughness↔aversive link is human-voice-specific, or the ungulate set's valence is too confounded with call context (Negative = separation/agonistic, Positive = reunion/food anticipation) and with recording protocol for the effect to appear at the same magnitude.

## 6. Honest limits

- **Duration confound (the headline limit):** the extractor's 150 ms edge trim makes any clip under ~0.6 s unreliable; a full re-run on a corpus of long clips would be needed for a clean animal test, and that is exactly what the duration-controlled rows above approximate.
- **Valence is confounded with call context** by the corpus's own design (Negative = separation/agonistic, Positive = reunion/food anticipation).
- **Pseudo-replication:** many calls per animal; the subset spreads across animal IDs but the tests are file-level, so the effective N is smaller than the file count.
- **Species/recording heterogeneity:** files come from different studies, microphones and recording conditions; species are balanced by design so this cannot explain the valence contrast, but it adds noise.
- The extractor's 60-Hz channels resolve harmonics only where F0 ≳ 60 Hz; pig and wild-boar grunts can sit near or below that, so the F0 confound the extractor removes for human voices is not guaranteed removed here.

## Artifacts

- `ungulate_roughness.csv` — one row per WAV (filename, animal_id, species, context, valence, duration_s, roughness_proper, roughness_old).
- `ungulate_roughness.py` — this script (download/subset/extraction/stats).
- Audio under `data/human/ungulate/` — **CC-BY, kept on disk, not committed.**

