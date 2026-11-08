# Human vocal corpus — notes

Prepared as the human fold-in for the cross-species "core sound / constraint"
decodability benchmark. This corpus gives the benchmark a human analogue of the animal
acoustic-shape → distress/affiliation correlations: per-utterance acoustic features plus
a coarse `category` label (agonistic / affiliative / distress) that mirrors the animal
corpora.

## Datasets used

### 1. LAION `synthetic-vocal-bursts-voice-acting` (CC BY 4.0)
- URL: https://huggingface.co/datasets/laion/synthetic-vocal-bursts-voice-acting
- Licence: **CC BY 4.0** (stated in the dataset card and `README.md`).
- Content: 2,000 nonverbal vocal-burst WAVs (44.1 kHz) across a 197-key taxonomy
  (screams, laughs, cries, sobs, sighs, growls, moans, gasps …). Each sample carries
  `vocal_burst_key`, a description, speaker `gender` and `age_group`.
- **Important caveat:** this is **synthetic voice-acting** (generated with a TTS voice-acting
  model), *not* recordings of real humans. It is the only vocal-burst source found with a
  clean permissive licence (all real-human vocal-burst databases surveyed are NC or
  research-only — see "excluded" below). Findings on this subset reflect the generating
  model's acoustics; they are a first-pass analogue, not a claim about real human vocal
  physiology.
- Subset used: `shard-0000.tar` (samples 0001–0500, **500 female** bursts: toddler_girl,
  pre_puberty_girl, teenage_girl, young_woman). Only the 102 taxonomy keys that map to a
  clear affect (laughter / joy / calm / neutral / anger / fear / panic / pain / disgust /
  sadness) are kept; the remaining 79 keys (physiological sounds — yawns, sneezes, burps,
  coughs, snoring — and exertion / musical-performance / whistling / filler items) are
  excluded as non-affective.

### 2. Thorsten-Voice Dataset 2021.06 emotional (CC0)
- URL: https://zenodo.org/records/5525023
- Licence: **CC0 1.0** (stated in the record and README).
- Content: 2,400 recordings of real human emotional **speech** — 300 German sentences read
  by one male speaker (Thorsten Müller) in 8 emotions (neutral, amused, angry, disgusted,
  sleepy, surprised, drunk, whisper). Mono, 22.05 kHz, normalized to −24 dB, no leading /
  trailing silence.
- Subset used: the 4 emotions that map cleanly onto the coarse categories —
  `neutral` → affiliative, `amused` → affiliative (happy), `angry` → agonistic,
  `disgusted` → agonistic. `surprised` / `sleepy` / `drunk` / `whisper` are **excluded**
  (no clean agonistic/affiliative/distress mapping, and whisper is unvoiced → no F0).

## Licence summary

| dataset | licence | real/synthetic | modality |
|---|---|---|---|
| LAION synthetic-vocal-bursts-voice-acting | CC BY 4.0 | synthetic voice-acting | nonverbal vocal bursts |
| Thorsten-Voice emotional | CC0 1.0 | real human (1 male speaker, German) | emotional speech |

Both licences permit redistribution and adaptation, so the extracted feature table can be
committed/shared without restriction.

## n utterances

**689 total** = 289 LAION (nonverbal bursts, synthetic) + 400 Thorsten (speech, real).

| category | n | emotion breakdown |
|---|---|---|
| agonistic | 336 | angry 159 · disgust 125 · fearful 32 · pain 18 · panic 2 |
| affiliative | 310 | happy 146 · neutral 123 · calm 41 |
| distress | 43 | sad 43 |

Source × category: LAION → agonistic 136 / affiliative 110 / distress 43;
Thorsten → agonistic 200 / affiliative 200 (no "sad" class in Thorsten).

> `distress` (n=43) is the thinnest category — it comes only from the LAION
> sobs/wails/whimpers/keens, because Thorsten has no "sad" class. Noted, not hidden.

## Emotion → category mapping (exact)

| emotion | category | rationale |
|---|---|---|
| angry | agonistic | threat/aggression (the animal "agonistic" class) |
| fearful | agonistic | alarm/threat |
| disgust | agonistic | aversion |
| panic | agonistic | alarm/distress warning |
| pain | agonistic | distress/warning — the task glosses agonistic as "distress/warning"; pain cries are the human distress/warning signal (recorded as an extension of the explicit angry/fearful/disgust/panic list) |
| happy | affiliative | pleasure/approach (incl. laughter, amusement) |
| calm | affiliative | relaxed/positive |
| neutral | affiliative | baseline |
| sad | distress | **third category**: high-arousal low-valence, distinct from agonistic (per the brief) |

- `Thorsten "amused"` → emotion `happy`; `Thorsten "disgusted"` → `disgust`.
- `Thorsten surprised/sleepy/drunk/whisper` → excluded (unmapped).
- `pain` is the only emotion not in the brief's literal list; it is assigned to `agonistic`
  under the "distress/warning" gloss, and is recorded here explicitly so the mapping is
  auditable.

## Feature-extraction parameters

All audio is loaded mono and resampled to **22050 Hz** (`librosa.load(sr=22050, mono=True)`).
Per utterance:

| feature | definition |
|---|---|
| `duration` | seconds of audio (`len(y)/sr`) |
| `peak_freq` | dominant frequency (Hz): frequency bin of the maximum of the time-averaged power spectrum (STFT `n_fft=2048`, `hop=512`), bins below 20 Hz ignored |
| `bandwidth` | spectral bandwidth (Hz): mean over frames of `librosa.feature.spectral_bandwidth(p=2)` (the energy-weighted standard deviation of frequency around the centroid) |
| `centroid` | spectral centroid (Hz): mean over frames of `librosa.feature.spectral_centroid` |
| `f0_mean` | mean fundamental frequency (Hz): **median** `librosa.pyin` F0 over voiced frames (`fmin=60`, `fmax=1200`, `frame_length=2048`, `hop=512`); **NaN** if no voiced frame (whispers / aperiodic bursts) |
| `roughness` | Arnal scream feature: fraction of the Hilbert temporal-envelope **modulation spectrum** energy in the **30–150 Hz** amplitude-modulation band (relative to total non-DC envelope energy) |

**Known limitation of `roughness` (flag, not hidden):** because the amplitude envelope of
voiced sound ripples at the glottal pulse rate, a voiced signal whose **F0 is below ~150 Hz**
places its pulse-rate modulation *inside* the 30–150 Hz band, so the raw fraction is inflated
for low-F0 voiced speech (e.g. Thorsten `neutral`, F0 ≈ 140 Hz → roughness 0.16) and suppressed
for high-F0 sounds (e.g. `sad`/`angry`, F0 ≈ 270 Hz → roughness 0.02–0.04). This is a property
of any full-waveform envelope AM measure, not a bug: a synthetic check returns ≈1.0 for 30–150 Hz
AM, ≈0 for a pure 200 Hz tone and for 200 Hz AM, and ≈0.66 for a 100 Hz pulse train. Arnal et al.
derive roughness from a *multi-band* (cochlear) modulation power spectrum, which is why their
scream result is not dominated by low-F0 voicing; the single-envelope version here is the
documented first-pass simplification. Interpret `roughness` together with `f0_mean` (or use a
multi-band MPS) before drawing the "agonistic = harsher" conclusion.

`librosa` 0.11.0 (with `numba` 0.60.0 / `scipy` 1.13.1) was installed into
`research/animal-c1/venv` via `pip install librosa`.

## Excluded datasets (NC / research-only / no-licence)

Surveyed and **not** used because the licence forbids redistribution or is unclear:

| dataset | licence / status | why excluded |
|---|---|---|
| RAVDESS | CC BY-NC-SA 4.0 | NC (non-commercial) |
| CREMA-D | research-only (request, no formal licence) | not redistributable |
| IEMOCAP | research-only (USC/SAIL, request) | not redistributable |
| TESS (Toronto Emotional Speech Set) | free for research, non-commercial | NC |
| Montreal Affective Voices (MAV) | available on request, research use; not CC | not openly redistributable |
| ESD (Emotional Speech Dataset) | CC BY-NC-SA 4.0 | NC |
| EmoV-DB | CC BY-NC-SA 4.0 | NC |
| VOC-C (Vocalisation Challenge Corpus) | no licence declared on Zenodo | unclear / no explicit grant |
| A-VB / Hume ExVo vocal bursts | research-only (competition) | not redistributable |

## Re-run

```bash
/Users/mac/Documents/DeepSeek/research/animal-c1/venv/bin/python extract_human_features.py
```

Reads `data/human/laion/shard-0000/` and `data/human/thorsten/thorsten-emotional_v02/`,
writes `human_corpus.csv` (columns: `utterance_id, emotion, category, duration,
peak_freq, bandwidth, centroid, f0_mean, roughness`).
