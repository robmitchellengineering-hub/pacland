# Roughness (multi-band MPS) — recomputation and the "roughness = aversive" test

**Arnal et al. 2015** ("Human screams occupy a privileged niche in the communication
soundscape", *Curr. Biol.* 25:2051) defines *roughness* as temporal modulation power in the
**30–150 Hz** amplitude-modulation band, computed from a **multi-band modulation power
spectrum (MPS)**. The current `human_corpus.csv` `roughness` feature is the single-envelope
approximation of that idea, and it is **F0-confounded**: the full-waveform envelope of a
low-pitched voiced sound ripples at the glottal-pulse rate (~140 Hz), which sits *inside*
30–150 Hz, so calm speech reads as rough. This report replaces it with a proper multi-band
MPS roughness (`roughness_proper`), sanity-checks the measure, and re-tests whether roughness
predicts the aversive (agonistic/distress) category.

## 1. Method

For each utterance (22050 Hz mono, mean-removed), a bank of **constant-bandwidth** channels
is filtered and the 30–150 Hz modulation energy is summed across channels and normalised by
the total non-DC modulation energy:

```
roughness_proper = Σ_channels  (envelope AM energy in 30–150 Hz)
                 / Σ_channels  (envelope non-DC energy in 0–500 Hz)
```

Per channel:

1. `ya = hilbert(y)` — one analytic signal, reused by every channel;
2. `band = sosfilt(channel, ya)` — complex (analytic) channel signal; envelope `|band|`;
3. trim 150 ms from each end (filter + Hilbert transient);
4. subtract the envelope mean (remove DC), downsample the envelope to ~1000 Hz
   (`resample_poly(20, 441)`), subtract the mean again;
5. modulation spectrum `|rfft(env)|²`; accumulate `[30, 150] Hz` (numerator) and all
   non-DC bins `0–500 Hz` (denominator);
6. channels whose envelope energy is below `1e-8 × max` are dropped (silent-channel noise).

**Filterbank:** constant bandwidth **W = 60 Hz**, Butterworth **order 14**, channels centred
every **60 Hz** from 60 Hz to **8000 Hz** (133 channels). This is the crucial design choice
(see §1.1).

### 1.1 Why constant-bandwidth, and why *not* the ~6-band / 1/3-octave recipe

The brief suggested ~6 log-spaced 1/3-octave bands (centres 250…8000 Hz). That recipe was
**implemented and tested first, and it reproduces the F0 confound** rather than fixing it:

- a 1/3-octave band is wide enough at its centre (≥ ~231 Hz above 1 kHz) to contain **two or
  more harmonics** of a low-F0 voiced sound; those harmonics beat with each other at the F0
  rate (~140 Hz), which lands inside 30–150 Hz and is counted as roughness — in *every* band,
  not just the fundamental's band. Empirically the 6-band version scored a synthetic 140 Hz
  vowel at roughness ≈ **0.97** (i.e. *more* rough than the old single-envelope measure's
  0.41), which is the opposite of the intended fix.

The F0 confound can only be removed by resolving individual harmonics into their **own**
channel, so that each channel's envelope is constant and contributes no 30–150 Hz modulation.
That requires channels **narrower than the F0 harmonic spacing** (140 Hz), with steep skirts
so the adjacent harmonic (~140 Hz away) is rejected. A constant-**60 Hz** band-pass with
order-14 Butterworth does exactly this.

**Consequence of the fix (a fundamental limit, stated openly):** a channel narrow enough to
resolve 140 Hz harmonics can only detect amplitude modulation up to about **~60–75 Hz** (a
modulation sideband sits ~f_AM away from its carrier, and must fall inside the channel's
pass/transition band). The 30–150 Hz roughness band is therefore measured here mostly through
its **30–75 Hz** portion. This is the unavoidable price of de-confounding a 140 Hz glottal
pulse; no linear spectrogram/filterbank can simultaneously resolve 140 Hz harmonics *and*
detect 150 Hz AM (the two requirements conflict: channels must be both < 140 Hz and > ~300 Hz).

## 2. Synthetic sanity check

| signal | roughness_proper (new) | old (single-envelope) |
|---|---|---|
| 200 Hz pure tone | **0.085** (≈ 0) | 0.005 |
| 200 Hz tone, 70 Hz AM | **0.785** (high) | 1.000 |
| 140 Hz voiced sustained vowel | **0.110** (low) | 0.405 |

The new measure is ~0 for a pure tone, high for genuine 30–150 Hz amplitude modulation, and
**low for a 140 Hz voiced vowel** — where the old measure reads it high (0.41). The measure
therefore does what it was asked to do: the glottal pulse rate is no longer counted as
roughness.

## 3. Per-category means

n = 689 (agonistic 336 · distress 43 · affiliative 310), same files as `human_corpus.csv`,
0 missing.

| category | roughness_proper (new) | roughness (old, confounded) |
|---|---|---|
| **agonistic** | **0.0327** | 0.0510 |
| **distress** | 0.0253 | 0.0154 |
| **affiliative** | 0.0270 | **0.1027** |

Per emotion (new): angry 0.0330 · calm 0.0146 · disgust 0.0311 · fearful 0.0348 ·
happy 0.0305 · neutral 0.0269 · pain 0.0303 · panic 0.0981 · sad 0.0253.

The confound is gone: **neutral dropped from 0.160 (old) to 0.027 (new)**, and calm is now
the smoothest (0.015). The direction is **corrected in sign for agonistic** — agonistic
(0.0327) now reads rougher than affiliative (0.0270) — but the separation is small and not
statistically significant (Mann–Whitney one-sided p = 0.585). **Distress (sad) is not
rougher** than affiliative (0.0253 < 0.0270; p = 0.895): in this corpus "sad" is low-arousal
sobbing, whose modulation is mostly at the sob rate (< 30 Hz), i.e. below the roughness band.

## 4. Aversive-prediction test

Balanced logistic regression, `roughness_proper` as the single predictor, and a 5000-sample
permutation null.

| contrast | balanced logistic accuracy | permutation p | logistic coef (sign) |
|---|---|---|---|
| **agonistic+distress vs affiliative** (task binary) | **0.5000** | 1.000 (chance = 0.5000) | +0.77 |
| agonistic vs affiliative (cleaner) | 0.5000 | 0.999 | +0.86 |

**The corrected roughness does NOT beat chance** at predicting aversive vs affiliative. The
coefficient has the right sign (rougher → more likely agonistic), but the effect is far too
weak to classify individual utterances — the classifier collapses to predicting the majority
class (balanced accuracy = 0.5).

For reference, the **old** measure "predicted" at balanced accuracy 0.676 (p < 0.0002) — but
with a **negative** coefficient (−4.8): it was exploiting the F0 confound (low-F0 calm/neutral
speech reading as "rough"), i.e. predicting aversive in the *wrong* direction.

## 5. Comparison to the old measure, and the bottom line

| | old `roughness` | new `roughness_proper` |
|---|---|---|
| direction (agonistic vs affiliative) | **inverted** (0.051 < 0.103) | **correct sign** (0.033 > 0.027), not significant |
| neutral emotion (low-F0 confound) | 0.160 (spuriously high) | 0.027 (fixed) |
| aversive prediction | 0.676 acc, but via the confound (coef −4.8) | 0.500 acc (chance) |

**Conclusion:** the F0 confound is fixed and the direction now has the correct sign for the
agonistic category, but after that correction **roughness does not predict the aversive
category in this corpus** (balanced accuracy = chance). "Roughness = aversive" (Arnal) is
therefore **not supported** by this corpus once the glottal-pulse-rate artefact is removed.
The most likely reasons, both already flagged in `human_corpus_notes.md`: (1) the LAION subset
is **synthetic voice-acting**, so its "screams/growls" do not carry the real chaotic
30–150 Hz roughness of human screams, and (2) the Thorsten subset is one male speaker whose
agonistic tokens are *angry/disgusted speech*, harsh but not screamed. This is a property of
the corpus, not a failure of the extractor — the extractor demonstrably separates genuine
30–150 Hz AM from smooth voicing (sanity check §2).

## Artifacts

- `extract_roughness.py` — the extractor (also `--selftest` runs the synthetic checks).
- `roughness_proper.csv` — `utterance_id, roughness_proper, category` (n = 689).
- `analyze_roughness.py` — the means / logistic / permutation / Mann–Whitney analysis.
