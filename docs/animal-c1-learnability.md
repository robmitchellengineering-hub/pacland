# C1 — animal communication, constraint-first: first run (learnability split)

- **Job:** C1 of `PLANS/PLAN-animal-communication-constraint-first.md`
- **Date:** 2026-11-08
- **Executor:** agent `session-…` (delegated subagent), running on `mac`
- **Verdict up front:** **C1 HOLDS on the falsifier (no Rosetta unit) but does NOT reproduce
  the clean uniform column.** All four candidate constraints are LEARNABLE; the context-free
  acoustic → referent map is **graded** (balanced accuracy 0.60), far below the r≥0.9 Rosetta
  threshold yet well above chance. No animal was "decoded" or "translated".

---

## 1 — Dataset, licence, citation

| field | value |
|---|---|
| Title | Acoustic data in four species of macaques |
| Repository | Zenodo — https://zenodo.org/records/3877581 (version v1, 2021-06-29) |
| DOI | 10.5061/dryad.905qfttgw |
| Licence | **CC0 1.0 (Creative Commons Zero — public-domain dedication). Reuse permitted.** |
| File | `Rebout_et_al_data_excel.xlsx` (176,151 bytes) |
| File URL | https://zenodo.org/records/3877581/files/Rebout_et_al_data_excel.xlsx?download=1 |
| File md5 | `cbfcefc715a38ad797cc09df960f6fcd` |
| Creators | Rebout, Nancy; Thierry, Bernard; Lemasson, Alban; Micheletta, Jérôme; Cozzolino, Roberto |
| Source paper | Rebout N, De Marco A, Lone J-C, Sanna A, Cozzolino R, Micheletta J, Sterck EHM, Langermans JAM, Lemasson A, Thierry B. 2020. *"Tolerant and intolerant macaques show different levels of structural complexity in their vocal communication."* **Proc. R. Soc. B** 287: 20200439. doi:10.1098/rspb.2020.0439 |

**Contents:** 2,520 calls, adult females of four macaque species (Tonkean `n=700`, crested
`n=696`, rhesus `n=639`, Japanese `n=485`), 89 individual emitters. Each call has **7
context-free acoustic variables** measured in Raven Pro v1.4 — `duration` (s), `Q2_ratio`,
`q1_frequency`, `q2_frequency`, `q3_frequency` (Hz), `aggregate_entropy`, `average_entropy` —
plus a **behavioural label** `context` with three levels.

**Label note (recorded, not glossed):** the Zenodo *description* names the three contexts
"agonistic / affiliative / neutral"; the data *file* codes them `negative` / `positive` /
`neutral`. This run reads `negative` = agonistic (aggression / response to aggression),
`positive` = affiliative, `neutral` = not in a social interaction — the mapping the description
states. Counts: neutral 1145, positive 693, negative 682.

---

## 2 — The falsifier (registered BEFORE computing — see `research/animal-c1/REGISTERED-FALSIFIER.md`)

C1 is refuted iff a **context-free** acoustic map to the behavioural referent is
near-deterministic — a Rosetta unit. Either arm firing kills C1:

- **JOINT (ridge-CV) arm:** ridge classifier on the 7 context-free acoustic features predicts
  context at **5-fold CV balanced accuracy ≥ 0.90** AND **permutation z ≥ 3**.
- **SINGLE-COORDINATE (Rosetta) arm:** the best single acoustic feature alone predicts context
  at **CV balanced accuracy ≥ 0.90** AND **MI permutation z ≥ 3**.

Bands: ≥0.90 → **REFUTED** · ≈0.333 within null → **uniform** · in between → **graded**
(C1 holds, split not clean). *(Registration file written 2026-11-08 before any number was
computed; not retrofitted.)*

---

## 3 — What ran (commands + numbers, quoted)

Environment: venv at `research/animal-c1/venv` — numpy 2.0.2, scipy 1.13.1, scikit-learn 1.6.1,
pandas 2.3.3, openpyxl 3.1.5. Setup:

```
python3 -m venv venv
./venv/bin/pip install openpyxl scikit-learn pandas
```

Analysis (single script, re-runnable):

```
./venv/bin/python measure_animal_c1.py
```

**Preprocessing (stated, not hidden):** each of the 7 features winsorized to [1%, 99%] (the
`Q2_ratio` column has a raw max of 243 against a median of 0.47 — a data-entry outlier), then
z-scored. Classification target = `context` (3-class) / `species` (4-class); the continuous
control target = `q3_frequency`. Models: `RidgeClassifier(alpha=1.0)` one-vs-rest, 5-fold
`StratifiedKFold`; continuous control uses `Ridge(alpha=1.0)` with 5-fold `KFold` and Pearson r
— the same metric as the physics reference. Class imbalance (neutral = 45%) is handled by
reporting **balanced accuracy**; chance = 1/3 (context) and 1/4 (species).

**Reuse statement (as the brief requires):** the single-coordinate MI arm reuses
`pacland.structure.mutual_information` / `mi_significance` (8-bin naive estimator, permutation
null) — the reference's own estimator. The joint arm is **reimplemented** as a classifier here
because `pacland.structure.ridge_cv_predictability` is regression-only (Pearson r) and the
animal targets are categorical; only the continuous positive control keeps plain ridge + Pearson
r. This is stated explicitly, not silently substituted.

### 3.1 Positive control — quantile ordering (the "tadpole" of this dataset)

```
q1 <= q2 <= q3 holds on 2520/2520 calls (100.00%)   [structural constraint, exact by def]
MI(q2_frequency; q3_frequency) = 0.676 bits, z = +282.04
ridge-CV r (q3 from 6 other feats) = +0.929, null_mean = -0.011, perm z = +31.60
```

The instrument is shown to recover a near-deterministic spectral constraint at r = +0.93 (the
physics tadpole sat at r = +0.99) — i.e. the three checks do fire on real deterministic
structure in this feature set.

### 3.2 Constraint — unit inventory (discrete cluster structure)

```
mean silhouette, k=2..8: +0.403 +0.264 +0.258 +0.229 +0.223 +0.195 +0.200
best k = 2, silhouette = +0.403 vs shuffled null mean -0.021 (sd 0.015), z = +28.29
```

Real data is clearly clustered (silhouette 0.40) against a shuffled null (−0.02) — the signal
has a discrete 2-way structure (consistent with the paper's own tonal/atonal split), not a
featureless continuum.

### 3.3 Constraint — dialect (acoustic → species, 4-class, chance 0.25)

```
best single-coord MI: average_entropy (mi 0.365 bits, z +171.71)
JOINT ridge-CV balanced acc = 0.544 (null 0.250 ± 0.008), perm z = +36.71
```

Species is recoverable from acoustics at 0.54 balanced accuracy (chance 0.25) — the dialect
constraint is real.

### 3.4 Constraint — context-dependence (acoustic → context, 3-class, chance 0.333)

```
best single-coord MI: q1_frequency (mi 0.253 bits, z +155.49)
JOINT ridge-CV balanced acc = 0.597 (null 0.333 ± 0.001), perm z = +176.11
```

The signal is structured by social context at 0.60 balanced accuracy (chance 0.33) — the
context-dependence constraint is real.

### 3.5 Meaning — context-free acoustic → referent (the falsifier)

```
SINGLE-COORDINATE Rosetta: best single feature q2_frequency, balanced acc = 0.506 (null 0.333), z = +382.36
JOINT Rosetta: 7 feats -> context, balanced acc = 0.597, z = +176.11
raw accuracy = 0.642 (majority-class chance 0.454)
```

Both the single-feature and joint decoders sit at **~0.51–0.60**, i.e. **far below the 0.90
Rosetta threshold** (falsifier NOT fired → C1 holds), yet **well above chance** (not uniform).
The permutation null is degenerate (see §5): under shuffled labels the linear classifier
collapses to chance, so the null range is `[0.329, 0.340]` and the true value `0.597` sits
~185 null-std away. The honest reading is "real, moderate signal — not a Rosetta unit".

---

## 4 — The Rule-of-Three table

| feature | role | MI (best single-coord; z) | ridge-CV (joint) | permutation z | verdict |
|---|---|---|---|---|---|
| quantile-ordering q1≤q2≤q3 | constraint (control) | 0.676 bits (+282) | r = **+0.929** | +31.6 | **LEARNABLE** |
| unit-inventory (clusters) | constraint | n/a (structural) | silhouette **+0.403** | +28.3 | **LEARNABLE** |
| dialect (acoustic→species) | constraint | 0.365 bits (+172) | bal-acc **0.544** (chance 0.25) | +36.7 | **LEARNABLE** |
| context-dependence (acoustic→context) | constraint | 0.253 bits (+155) | bal-acc **0.597** (chance 0.33) | +176 | **LEARNABLE** |
| acoustic → referent (falsifier) | meaning | 0.253 bits (+155) | bal-acc **0.597** (< 0.90) | +176 | **graded — C1 holds, not clean** |

The `context-dependence` (constraint) and `acoustic → referent` (meaning) rows are the **same
measurement read against two different thresholds**, and this is deliberate: the plan's
constraint "context-dependence" claims the signal is *structured by* context (above null), while
the falsifier claims the signal *deterministically decodes* the referent (≥0.90). Both are
checked; they agree on the number (0.597) and disagree on the threshold it crosses.

---

## 5 — Honest limits (named)

1. **The meaning arm is a proxy, not a referential test.** This corpus' only behavioural label
   is the *social situation* (context). It carries no external referent (predator / food /
   alarm type), so "context-free acoustic → behavioural referent" is tested against *context*
   as the referent stand-in. A true referential falsifier (e.g. vervet/macaque alarm-call →
   predator-type) needs a corpus with referent labels — a later job, not this one.
2. **The split is graded, not the physics split.** The physics corner separated a deterministic
   constraint (tadpole r=0.99) from uniform observables (|r|<0.22). Here the meaning map is
   neither deterministic (0.60, not 0.90) nor uniform (0.60, not 0.33): macaque calls are
   *graded* and partially context-informative. C1's falsifier does not fire, but C1's strong
   "uniform" column is **not** reproduced on this corpus — reported as such, not dressed up.
3. **The classification permutation z is degenerate.** With random labels the linear classifier
   collapses to chance, so the null std is ~0.0014 and z is inflated (185). The robust statement
   is the effect size (0.60 vs 0.33) and that the true value sits outside the null range
   `[0.329, 0.340]`; the exact z magnitude should not be quoted as precision.
4. **Feature set is the paper's 7 Raven variables, not raw audio.** No waveform/spectrogram, no
   librosa, no foundation model (out of scope for C1). The "unit inventory" is a k-means cluster
   structure, not a self-supervised discrete unit code; a real combinatoriality/Zipf or
   temporal-dependency constraint needs *sequences*, which this per-call table does not contain.
5. **Linear models only.** Ridge is linear; non-linear decoders could raise the meaning map
   toward (or over) 0.90. That is exactly a later, heavier job — but note it bounds what this
   run can claim about "no Rosetta unit".
6. **Label tokens differ from metadata** (negative/positive vs agonistic/affiliative); the
   mapping used is the one the Zenodo description states, but the file itself does not spell it.
7. **Preprocessing choices** (winsorize 1/99, z-score) were fixed before running; no
   per-feature log-transform was applied (frequencies are right-skewed), so the ridge numbers
   are a lower bound on what a log-space linear model could reach.

---

## 6 — Where this lives

- Analysis: `research/animal-c1/measure_animal_c1.py` (re-runnable)
- Data: `research/animal-c1/data/Rebout_et_al_data_excel.xlsx`
- Falsifier registration: `research/animal-c1/REGISTERED-FALSIFIER.md`
- This review: `REVIEWS/animal-c1-learnability.md`
- Not committed, not pushed to `pacland` (per the brief; the `discipline/animal` formalization
  is a later step).
