# Roughness → aversive: the REAL-voice check (RAVDESS emotional speech)

**Question.** Does the *corrected* multi-band MPS roughness (`roughness_proper`,
constant-60 Hz Butterworth channels, Hilbert envelope, 30–150 Hz AM band —
`extract_roughness.py`, reused unchanged) predict the **aversive** category in
**real human voices**? The prior test (LAION synthetic + Thorsten) found the
corrected measure at chance and concluded the "roughness = aversive" lead was
dead on *synthetic/acted* data with no real screams. This is the real-voice check
on RAVDESS.

## 1. What was downloaded and used

- **Source:** Zenodo record **1188976** — `Audio_Speech_Actors_01-24.zip`
  (audio-only *speech*, not song), **199 MB** compressed / 590 MB uncompressed.
  MD5 `bc696df654c87fed845eb13823edef8a` (matches the record's checksum).
  License **CC BY-NC-SA 4.0** — the audio is NC, so it is kept on disk only and
  is **not** committed or pushed.
- **Subset extracted:** all **24 actors** (12 male, 12 female) × the six target
  emotions × both statements × both intensities × both repetitions. Neutral has
  only the normal intensity in RAVDESS (no "strong"), so it contributes 4 files
  per actor; the other five emotions contribute 8. **n = 1056 utterances**
  (44/actor). sad(04) and surprised(08) were excluded per the brief.
- **Emotion → category:** aversive = angry(05), fearful(06), disgust(07)
  (n = 576); non-aversive = happy(03), calm(02), neutral(01) (n = 480).
- Audio loaded mono at **22050 Hz** (`librosa.load(sr=22050)`), exactly as the
  existing extractor expects.

## 2. Per-emotion roughness (multi-band MPS, proper)

| emotion | roughness_proper | roughness_old (confounded) | n |
|---|---|---|---|
| neutral | 0.0168 | 0.0592 | 96 |
| calm    | 0.0144 | 0.0665 | 192 |
| happy   | 0.0251 | 0.0288 | 192 |
| angry   | **0.0287** | 0.0230 | 192 |
| fearful | 0.0238 | 0.0255 | 192 |
| disgust | 0.0266 | 0.0431 | 192 |

## 3. Per-category roughness

| category | roughness_proper | roughness_old (confounded) | n |
|---|---|---|---|
| **aversive** | **0.0264** | 0.0305 | 576 |
| **non-aversive** | 0.0191 | **0.0500** | 480 |

The **direction is correct** on the proper measure: aversive is *rougher* than
non-aversive (0.0264 vs 0.0191). The old confounded measure is **inverted**
(non-aversive reads *rougher*), the same F0 artefact seen in the prior corpus.

## 4. Prediction test (as specified)

Balanced logistic regression, roughness as the single predictor, 2000-permutation
null (identical procedure to the prior corpus test):

| measure | balanced logistic accuracy | permutation p | logistic coef (sign) |
|---|---|---|---|
| **roughness_proper (new)** | **0.5000** | 1.000 | **+1.86** (rougher → aversive) |
| roughness_old (confounded) | 0.5797 | 0.0000 | −3.31 (rougher → *non*-aversive) |

The new measure's coefficient has the **correct sign** (+1.86), unlike the old
measure (−3.31, i.e. exploiting the F0 confound backwards — the old measure
"predicts" aversive at 58% but for the *wrong* reason).

## 5. Why "accuracy = 0.5000" understates the signal (the honest nuance)

The specified balanced-logistic-accuracy statistic is **degenerate** for a single
modest predictor: the logistic fits a threshold that predicts **every utterance
as aversive** (the 0.5-probability cutoff falls left of the whole data range), so
balanced accuracy is *exactly* 0.5 and the permutation null is *also* all 0.5 —
hence p = 1.0 by construction. That metric cannot see the effect, so it must not
be read as "no effect". Every non-degenerate test says the effect is **real and
in the correct direction**:

| statistic (proper measure) | value | p |
|---|---|---|
| Mann–Whitney, aversive > non-aversive | U = 200114 | **< 0.0001** |
| Cohen's d (aversive − non-aversive) | **+0.83** (large) | — |
| ROC AUC (raw roughness, aversive positive) | **0.724** | < 0.0005 (2000-perm) |
| point-biserial r | **+0.38** | 6.5 × 10⁻³⁸ |

The old measure's AUC is **0.454** — *below* chance, in the wrong direction
(permutation p = 0.99), confirming the confound rather than a real signal.

## 6. Bottom line

**The lead partially revives in real (acted) voices.** On RAVDESS the corrected
multi-band MPS roughness is **significantly higher for aversive than
non-aversive utterances** — correct sign (coef +1.86), large effect (Cohen's
d = 0.83, AUC = 0.72), and unambiguously significant (Mann–Whitney p < 0.0001).
This is a genuine change from the synthetic corpus, where the corrected measure
showed *no* significant difference (Mann–Whitney p = 0.585).

**But** the effect size is not enough for roughness to be a *classifier*: a
single-predictor logistic collapses to the majority class (balanced accuracy =
chance), because the within-category spread (std ≈ 0.008–0.009) is comparable to
the between-category gap (0.007). Roughness is a **group-level acoustic
correlate** of aversiveness — real, in the right direction, but too weak alone to
sort individual utterances.

**Honest limits.** (1) RAVDESS is *acted* speech — trained actors performing
anger/fear/disgust, **not real screams**, so this still does not test Arnal's
core claim about genuine screams; the biggest roughness values here (~0.05) are
an order of magnitude below the 0.785 a true 70 Hz AM signal scores in the
extractor's selftest. (2) One database, one recording protocol, English only.
(3) The aversive/non-aversive split is 576/480 (neutral lacks a "strong"
intensity), which balanced metrics already absorb. A decisive test would need a
corpus with genuine (un-acted) distress vocalisations.

## Artifacts

- `ravdess_roughness.csv` — 1056 rows × 11 cols (filename, actor, sex,
  emotion_code, emotion, intensity, statement, repetition, aversive,
  roughness_proper, roughness_old).
- `ravdess_extract.py` — parallel extraction (imports `extract_roughness.py`
  unchanged).
- `ravdess_analyze.py` — means + balanced logistic + 2000-permutation null.
- Audio under `data/human/ravdess/Actor_*/` — **NC, do not commit/push**.
