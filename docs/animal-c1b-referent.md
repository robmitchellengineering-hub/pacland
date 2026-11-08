# C1b — animal communication, constraint-first: the REFERENTIAL test (real predator referent)

- **Job:** C1b of `PLANS/PLAN-animal-communication-constraint-first.md` — extend C1 from a
  *proxy* (social context) to a *real external referent* (predator type).
- **Date:** 2026-11-08
- **Executor:** agent (delegated subagent), running on `mac`
- **Verdict up front:** **the registered falsifier FIRES — C1 is REFUTED for a real referent.**
  A context-free acoustic map to the referent is near-deterministic: joint ridge-CV balanced
  accuracy **1.000** and best single feature **0.955**, both ≥ 0.90 with permutation z ≥ 3. Where
  C1's *social-context proxy* was graded (0.60), a genuine *functionally-referential* system
  (dwarf mongoose aerial vs terrestrial alarm calls) is **discrete and deterministic** — a Rosetta
  unit exists. C1's "meaning is graded/uniform" result does **not** survive contact with a real
  referent. No animal was "decoded" or "translated": the finding is that the two referential call
  types are acoustically discrete, which is exactly what "functionally referential" means.

---

## 1 — Dataset, licence, citation

| field | value |
|---|---|
| Title | Data from: Wild dwarf mongooses produce general alert and predator-specific alarm calls |
| Repository | Zenodo — https://zenodo.org/records/5005321 (mirror of Dryad) |
| DOI | 10.5061/dryad.49d81 |
| Licence | **CC0 1.0 (Creative Commons Zero — public-domain dedication). Reuse permitted.** |
| Files used | `Alarm-call-acoustic-parameters.txt` (42,006 B) · `Alarm-calls-predator-presentations.txt` (24,615 B) · `Natural-Alarm-calls.txt` (60,095 B) |
| File md5 | acoustic-parameters `859cde2075c0ee14eed4ec0154e0191d` · presentations `2a62c776e92dc417e73239d40ee8b652` · natural `b5d0e77e355b81cc2d632de1eab389e1` |
| Creators | Collier, Katie; Radford, Andrew N.; Townsend, Simon W.; Manser, Marta B. |
| Source paper | Collier K, Radford AN, Townsend SW, Manser MB. 2017. *"Wild dwarf mongooses produce general alert and predator-specific alarm calls."* **Behavioral Ecology**, doi:10.1093/beheco/arx091 |

**Contents:** `Alarm-call-acoustic-parameters.txt` is 307 calls from 7 wild groups, each with a
call `Type` (type-1 … type-5) and **14 context-free acoustic features** measured in Raven —
`Length`, `Overall.peak.frequency`, `Peak.frequency.Mean/Maximum/Minimum`,
`Fundamental.frequency.Mean/Maximum/Minimum`, `Peak.frequency.change.Mean`,
`Fundamental.frequency.change.Mean`, `Wiener.entropy.Mean`, `Frequency.bandwidth.Mean`,
`Within.syllable.gap`, `No.Elements`. The **referent** is carried by a separate, controlled
experiment: `Alarm-calls-predator-presentations.txt` presents a **helium-balloon (simulated aerial
predator)** or a **dog (terrestrial predator)** and records the call type emitted.

**Referent assignment (fixed before computing — see the registration):** the controlled
experiment is the ground truth, independent of the acoustics.

| call `Type` | balloon (aerial) | dog (terrestrial) | referent |
|---|---|---|---|
| type-1 | 197 | 2 | **aerial** |
| type-4 | 0 | 194 | **terrestrial** |
| type-2 | 49 | 3 | non-specific (excluded) |
| type-3 | 216 | 48 | general alert (excluded) |
| type-5 | 7 | 13 | rare/mixed (excluded) |

→ **aerial** = type-1 (65 calls), **terrestrial** = type-4 (79 calls), n = 144, chance = 0.50.
This matches the paper's own abstract: *"Of the 5 commonly emitted alarm-call types, 3 appeared to
be non-specific and 2 predator-specific, given to aerial and terrestrial predators respectively."*

---

## 2 — The falsifier (registered BEFORE computing — `research/animal-c1b/REGISTERED-FALSIFIER.md`, 2026-11-08 15:27 AEDT)

C1 is refuted iff a **context-free** acoustic map to the referent is near-deterministic — a Rosetta
unit. Either arm firing kills C1:

- **JOINT (ridge-CV) arm:** ridge on the 14 context-free acoustic features predicts referent
  (aerial/terrestrial) at **5-fold CV balanced accuracy ≥ 0.90** AND **permutation z ≥ 3**.
- **SINGLE-COORDINATE (Rosetta) arm:** the best single feature alone predicts referent at
  **CV balanced accuracy ≥ 0.90** AND **MI permutation z ≥ 3**.

Bands (chance = 0.50): ≥ 0.90 + z ≥ 3 → **REFUTED** · ≈ 0.50 within null → **UNIFORM** · in
between → **GRADED**. *(Registration written before any ridge-CV / MI number; only dataset
structure and label counts had been inspected.)*

---

## 3 — What ran (commands + numbers, quoted)

Environment: reuse of `research/animal-c1/venv` — numpy 2.0.2, scipy 1.13.1, scikit-learn 1.6.1,
pandas 2.3.3, openpyxl 3.1.5. Analysis (re-runnable):

```
/Users/mac/Documents/DeepSeek/research/animal-c1/venv/bin/python measure_animal_c1b.py
```

**Preprocessing (stated, not hidden):** each feature winsorized to [1%, 99%], then z-scored.
Model: `RidgeClassifier(alpha=1.0)` one-vs-rest, 5-fold `StratifiedKFold`, **balanced accuracy**
(the same method as C1). MI via `pacland.structure.mutual_information` / `mi_significance`
(8-bin naive estimator, permutation null) — the reference's own estimator. The joint ridge-CV arm
is reimplemented as a classifier (as in C1) because `ridge_cv_predictability` is regression-only.

### 3.1 Positive control — the instrument fires on deterministic structure

```
min <= mean <= max holds on 144/144 calls (100.00%)   [structural, exact by def]
MI(Peak.Max; Peak.Mean) = 1.019 bits, z = +18.20
ridge-CV r (Peak.Mean from 13 other feats) = +0.991, null_mean=-0.040, perm z = +8.88
```

The instrument recovers a near-deterministic spectral constraint at r = +0.99 (C1's tadpole sat at
r = +0.93) — the three checks fire on real deterministic structure.

### 3.2 Constraint — acoustic → call type (5-class, chance 0.20)

```
JOINT ridge-CV balanced acc = 0.856 (null 0.202 ± 0.019), perm z = +34.59
```

The five call types are **not** linearly separable at 1.0 (0.856) — the three non-specific types
overlap acoustically, consistent with the paper's "graded" non-specific calls. This is the
internal consistency check: the linear instrument separates the *referential* types far better
than the *non-specific* ones (below).

### 3.3 Meaning — context-free acoustic → REAL referent (the falsifier)

```
per-feature MI(x; referent):
  Peak.frequency.change.Mean      = 0.917 bits, z = +49.69
  Fundamental.frequency.change.Mean = 0.912 bits, z = +47.01
  Fundamental.frequency.Mean      = 0.837 bits, z = +43.51
  Peak.frequency.Mean             = 0.829 bits, z = +43.42
  Within.syllable.gap             = 0.605 bits, z = +29.66
  No.Elements                     = 0.595 bits, z = +28.27
  Overall.peak.frequency          = 0.433 bits, z = +21.14
  Peak.frequency.Maximum          = 0.424 bits, z = +18.36
  Fundamental.frequency.Maximum   = 0.419 bits, z = +18.79
  Peak.frequency.Minimum          = 0.380 bits, z = +19.74
  Fundamental.frequency.Minimum   = 0.342 bits, z = +16.79
  Length                          = 0.307 bits, z = +12.49
  Frequency.bandwidth.Mean        = 0.250 bits, z = +10.73
  Wiener.entropy.Mean             = 0.224 bits, z = +9.52

SINGLE-COORDINATE Rosetta: best feature Peak.frequency.Mean, balanced acc = 0.955
  (null 0.488 ± 0.028), z = +16.66
JOINT Rosetta: 14 feats -> referent, balanced acc = 1.000 (null 0.488 ± 0.048), z = +10.62
```

Both arms fire: the joint map is **1.000** and a **single feature** (peak frequency) reaches
**0.955** — far above the 0.90 threshold, far above chance (0.50). A context-free acoustic map to
the referent **is** near-deterministic.

**Robustness (mapping choice does not change the verdict):**

```
aerial = type-1          vs terrestrial = type-4        : 1.000
aerial = type-1 + type-2 vs terrestrial = type-4        : 0.995
aerial = type-1          vs terrestrial = type-4 + type-5: 0.960
3-way aerial / terrestrial / general-alert              : 0.920 (chance 0.333)
```

**The concrete acoustic signature (raw group means, quoted):**

| feature | aerial (type-1) | terrestrial (type-4) |
|---|---|---|
| `Peak.frequency.Mean` | 5,838 Hz | 3,632 Hz |
| `Fundamental.frequency.Mean` | 5,838 Hz | 3,591 Hz |
| `Frequency.bandwidth.Mean` | 778 Hz | 1,266 Hz |
| `No.Elements` | 4.92 | 1.57 |
| `Within.syllable.gap` | 202 ms | 23.8 ms |

Aerial alarm calls are **~2.2 kHz higher** in peak/fundamental frequency and multi-element;
terrestrial alarm calls are lower, broader-band and single-element. Peak frequency alone is the
Rosetta coordinate (0.955).

---

## 4 — The Rule-of-Three table

| measure | role | metric | value | perm z | verdict |
|---|---|---|---|---|---|
| min ≤ mean ≤ max (structural) | constraint (control) | exact | 100.0% | n/a | **LEARNABLE** |
| Peak.Mean from 13 feats (control) | constraint (control) | ridge r | **+0.991** | +8.9 | **LEARNABLE** |
| acoustic → call type (5-class) | constraint | bal-acc | **0.856** (chance 0.20) | +34.6 | **LEARNABLE** |
| acoustic → referent (joint, 14 feats) | meaning (falsifier) | bal-acc | **1.000** (chance 0.50) | +10.6 | **REFUTED** |
| acoustic → referent (single, peak freq) | meaning (falsifier) | bal-acc | **0.955** (chance 0.50) | +16.7 | **REFUTED** |

Both falsifier arms cross the ≥ 0.90 threshold with z ≥ 3, and they agree with each other and with
the MI arm (top feature 0.917 bits, z +49.7). The constraints stay LEARNABLE; the meaning map is
deterministic, not uniform — the opposite of C1's clean-uniform prediction.

---

## 5 — Honest limits (named)

1. **The referent is type-level, and the types are acoustically defined.** Each call's referent is
   assigned via its call *type* (type-1 → aerial, type-4 → terrestrial), and the types were built by
   acoustic clustering in the source paper. A score of 1.0 therefore measures that the two
   referential call types are acoustically **discrete** — which is the definition of functional
   reference — **not** a de novo "decode" of the referent from acoustics with the type label
   discarded. This is disclosed, not hidden (it is in the registration too). The cleanest
   anti-circularity test — per-call acoustic features joined to a per-call independently-observed
   referent in one table — is not available in this corpus (features and referents live in separate
   files joined only by type).
2. **This is the expected behaviour of a referential system, and that is the point.** C1's graded
   0.60 was measured on macaque *social context*, which macaques encode without discrete referential
   call types. The dwarf mongoose encodes predator type with discrete referential types; the same
   instrument now reads 1.0. The contrast is the result: "meaning is graded/uniform in the signal"
   is not a universal — it holds for non-referential encoding and breaks for functional reference.
   (C2's strong "no exact context-independent meaning unit" was already known to be false for
   referential systems — vervet eagle/leopard/snake calls, 1980; C1b now *measures* it with the same
   instrument rather than importing the prior.)
3. **Small n.** The referent set is 144 calls (65 aerial, 79 terrestrial), 14 features. 5-fold CV
   mitigates overfitting (predictions are out-of-fold), and the permutation null (0.488 ± 0.048)
   confirms chance is 0.50; but n = 144 is a quarter of C1's 2,520. The robustness variants
   (0.995 / 0.960 / 0.920) all stay ≥ 0.90, so the verdict is not an artefact of the exact mapping.
4. **Linear models only.** Ridge is linear; a linear separation at 1.0 is the *strongest* possible
   linear claim, so a non-linear model cannot raise it further — but this run still cannot claim
   anything about non-linear structure in the *non-specific* types (the 0.856 five-class result is a
   linear lower bound on how graded those are).
5. **Feature set is the paper's 14 Raven variables, not raw audio.** No waveform/spectrogram, no
   librosa, no foundation model (out of scope for C1b). "Referent" is the predator class
   (aerial/terrestrial), not a finer food-type or individual-predator label.
6. **The natural-observation labels are noisier than the controlled experiment** (`Natural-Alarm-calls.txt`
   shows type-1 also given to "observer" and "unid"). The controlled presentation (dog vs balloon)
   is used as the referent ground truth because it is experimentally manipulated; the natural table
   is used only to cross-check the mapping (type-4 → "scent"/terrestrial, type-1 → "aerial").

---

## 6 — Where this lives

- Analysis: `research/animal-c1b/measure_animal_c1b.py` (re-runnable)
- Data: `research/animal-c1b/data/` (3 CC0 files, md5 above)
- Falsifier registration: `research/animal-c1b/REGISTERED-FALSIFIER.md`
- This review: `REVIEWS/animal-c1b-referent.md`
- Not committed, not pushed to `pacland` (per the brief).
