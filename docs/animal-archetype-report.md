# Cross-species "core sound" archetypes and the Morton test

**Question:** across 38 corpora, does acoustic *shape* (an unsupervised partition of pooled
call acoustics) predict behavioural *constraint* (agonistic / affiliative / neutral context,
and referent)? This is a null-modelled test of Morton's motivation-structural rules.

**Short answer:** the pooled data resolves into **K = 3 core sounds**, but they are
**species niches, not motivational types** — an ultrasonic-shrew cluster, a long-call frog
cluster, and one large mid-frequency "everything else" cluster. Shape predicts constraint
**only trivially above chance** on the 3-class context axis (0.507 vs 0.333) and **at
chance** on the actual Morton agonistic-vs-affiliative axis (0.50). The cross-species pool
is dominated by between-species acoustic variance, which swamps the within-species
motivational structure Morton's rules describe.

---

## 1. Common feature space and who joins it

Canonical features (mapped by *meaning* across each corpus's own columns, then unit-harmonised
to **seconds** and **Hz**):

- **duration** — e.g. `duration`, `Length`(ms), `Call_duration`(ms), `sound_duration`,
  `BarkDuration`, `Dtot`, `DurW`(ms), `Call duration (sec)`, `Dur`, and `end − start` for elephant.
- **peak/dominant frequency** — `q2_frequency`, `Peak.frequency.Mean`, `Fpeak_all`, `meandom`(kHz),
  `Q50`, `freq.dom`, `PeakFreq`, `Fmax`, `DomFreqW`, `peak freq(mean)`, `Dfreq`, and
  `(min+max)/2` as a centre proxy for the frog-noise corpus.
- **bandwidth / frequency range** — `q3−q1`, `Frequency.bandwidth.Mean`, `Max_F0−Min_F0`,
  `dfrange`(kHz), `Q75−Q25`, `Bandwidth (Hz)`, `quart75−quart25`.
- **entropy — excluded.** Present in only 3 corpora and on mutually incompatible scales
  (macaque 0.28–5.61, shearwater 0.125–0.353, mongoose "Wiener entropy" 180–218 dB), so it
  cannot be pooled. Documented, not used.

Two spaces were built and both are reported:

| corpus | n | duration | peak | bandwidth | joins 3-feat | joins 2-feat |
|---|---|---|---|---|---|---|
| macaque | 2520 | ✓ | ✓ | ✓ | ✓ | ✓ |
| mongoose (type-1/4) | 307 | ✓ | ✓ | ✓ | ✓ | ✓ |
| meerkat-closecall | 2237 | ✓ | ✓ | ✓ | ✓ | ✓ |
| shrew | 4289 | ✓ | ✓ | ✓ | ✓ | ✓ |
| houbara | 497 | ✓ (BD, flagged) | ✓ | ✓ | ✓ | ✓ |
| shearwater | 508 | ✓ | ✓ | ✓ | ✓ | ✓ |
| frog-noise | 35 | ✓ | ✓ (centre proxy) | ✓ | ✓ | ✓ |
| phyllodytes | 39 | ✓ | ✓ | — | ✗ (no bandwidth) | ✓ |
| prairie-dog | 4138 | ✓ | ✓ | — | ✗ | ✓ |
| crocodile | 88 | ✓ | ✓ | — | ✗ | ✓ |
| tungara | 460 | ✓ | ✓ | — | ✗ | ✓ |
| dendropsophus-minutus-calls | 2892 | ✓ | ✓ | — | ✗ | ✓ |
| gryllus-bimaculatus-noise-chirps | 2969 | — | — | — | ✗ (no spectral feature) | ✗ |
| pardo-rumble (elephant Context3) | 1918 | ✓ (`end−start`) | ✗ | ✗ | ✗ (spectral features not Hz) | ✗ |
| pardo-name (elephant referent) | 625 | ✓ (`end−start`) | ✗ | ✗ | ✗ (spectral features not Hz) | ✗ |

- **3-feature space** (the Morton triplet): **10,393 calls from 7 corpora**.
- **2-feature space** (sensitivity): **18,003 calls from 12 corpora**.

**The biggest casualty:** both elephant corpora carry the richest motivational vocabulary in
the benchmark (elephant rumble `Context3` = alarm / protest / greeting / contact / care /
suckling / musth / sex / …; elephant `Elicitor1_ID` = 119 individual "name" referents), but
their spectral features (`sprsMed`, `sprsMbw`, `sprsMc`, `V1..V74`) are standardised/derived
quantities, **not Hz**, so they cannot be pooled with the other species' Hz measurements. They
drop out of the Morton test entirely.

---

## 2. Choosing K

K was searched over 2–12 with two criteria (headline = 3-feature space):

| K | silhouette | BIC |
|---|---|---|
| 2 | 0.587 | 12,597 |
| **3** | **0.605** ← chosen | −13,064 |
| 4 | 0.591 | −17,550 |
| 5 | 0.579 | −21,454 |
| 6 | 0.531 | −28,456 |
| 7 | 0.562 | −23,684 |
| 8 | 0.557 | −24,548 |
| 9 | 0.545 | −31,268 |
| 10 | 0.546 | −31,317 |
| 11 | 0.531 | −31,253 |
| 12 | 0.535 | **−32,252** ← BIC best |

**K = 3** by silhouette (argmax, a defensible and transparent criterion). BIC keeps improving
to K = 12 — the classic signature of **non-Gaussian, species-lumped** data, where the model
keeps adding components to chase species sub-clusters rather than finding a small number of
meaningful archetypes. In the 2-feature sensitivity space, silhouette is **0.922 at K = 2**
(again: two clean clusters, i.e. a species-level split).

---

## 3. The archetypes: acoustic profile × constraint signature

Mean values are in original units (seconds, Hz). "Constraint signature" = the distribution of
the coarsened context labels, plus the mongoose referent labels.

| archetype | n | dur (s) | peak (Hz) | bw (Hz) | agonistic | affiliative | neutral | aerial | terrestrial | dominant species |
|---|---|---|---|---|---|---|---|---|---|---|
| **0** "mid-freq, short" | 7016 | 0.198 | 2,359 | 907 | 10.2% (682) | 43.7% (2,930) | 46.2% (3,097) | 45.1% (65) | 54.9% (79) | macaque 36% · meerkat 32% · shrew 13% |
| **1** "ultrasonic, tiny" | 3342 | 0.010 | 19,473 | 13,167 | 0% | 0% | 100% | — | — | **shrew 100%** |
| **2** "long call" | 35 | 5.829 | 4,345 | 747 | 0% | 0% | 100% | — | — | **frog-noise 100%** |

The headline result in plain terms:

- **Archetype 1 = ultrasonic shrew** (19.5 kHz, 10 ms) — 100% one species.
- **Archetype 2 = long frog calls** (5.8 s, 4.3 kHz) — 100% one species.
- **Archetype 0 = everything else** (mid-frequency, ~200 ms): *all* of macaque, meerkat,
  mongoose, shearwater, houbara plus 22% of shrew. Inside it sit **all 682 agonistic calls and
  all 693 macaque-affiliative calls together** — the archetype does not separate them.

No recovered archetype carries a clean Morton constraint (nothing looks like "high-freq tonal,
78% affiliative"). The partition is a **body-size / medium / species** split, not a
motivational one.

---

## 4. Does shape predict constraint? (the test)

Predictor = archetype membership (one-hot), model = balanced logistic regression, 5-fold CV,
**300 label-permutation nulls**, chance = 1 / n_classes.

| test | n | classes | balanced acc | chance | null mean ± sd | z | p | verdict |
|---|---|---|---|---|---|---|---|---|
| archetype → context (agonistic/affiliative/neutral) | 10,086 | 3 | **0.507** | 0.333 | 0.332 ± 0.009 | **19.72** | < 0.001 | nominally above chance |
| archetype → **agonistic vs affiliative** (Morton 2-class) | 3,612 | 2 | **0.500** | 0.500 | — | undefined | 1.0 | **at chance** |
| archetype → referent (mongoose aerial/terrestrial) | 144 | 2 | 0.500 | 0.500 | 0.500 ± 0.0 | undefined | 1.0 | **degenerate** |

**Reading this honestly:**

- The 3-class result *is* above chance, but the z = 19.7 is a **large-n artefact** (n ≈ 10,000):
  the effect is only +0.174 above chance, and it is carried entirely by the fact that two of the
  three archetypes happen to be single-species "neutral" clusters (shrew, frog). It is **not**
  evidence for a cross-species shape→motivation code.
- On the axis that Morton's rules actually make a prediction about — **agonistic vs
  affiliative** — the mapping is **exactly at chance (0.50)**. The clustering never separates
  macaque's negative (agonistic) from positive (affiliative) calls; they are all inside
  archetype 0.
- The **referent** test is degenerate: all 144 mongoose alarm calls fall in archetype 0, so the
  archetype cannot distinguish aerial from terrestrial predator. (For comparison, the
  decodability benchmark recovers mongoose aerial/terrestrial at balanced accuracy 1.0 from
  mongoose's *own* 14 features — the small 3-feature common space erases that structure.)

---

## 5. Honest limits

**(a) The common feature space is small (3 features).** The corpora are heterogeneous, so only
duration, peak/dominant frequency and bandwidth are common enough to pool. Entropy (3 corpora,
incompatible scales), and every corpus-specific feature (F0 contours, spectral shape, harmonicity,
amplitude) had to be dropped. A 3-feature space cannot represent the acoustic detail the
within-species benchmark uses (e.g. mongoose's 14 features).

**(b) Label coarsening is interpretive.** Exact mapping used (raw → coarse):

| corpus | raw labels → coarse |
|---|---|
| macaque | positive→affiliative · negative→agonistic · neutral→neutral |
| meerkat-closecall | all six close-call contexts (SC/EA/FO/PV/DI/MO) → **affiliative** (close calls are contact/cohesion calls) |
| shrew | all 8 locomotion/shelter categories → **neutral** |
| houbara | Son/Father/No Kin (kinship, non-motivational) → **neutral** |
| phyllodytes | natural/rodovia (environment) → **neutral** |
| prairie-dog | colony 1/2/3 (spatial) → **neutral** |
| crocodile | J/H/A (size/age class) → **neutral** |
| tungara | fed/unfed (condition) → **neutral** |
| frog-noise | 5 noise conditions → **neutral** |
| shearwater | E/I (respiration mechanism) → **neutral** |
| dendropsophus-minutus-calls | Norm/Red/Inv (playback) → **neutral** |
| mongoose (referent) | type-1→aerial · type-4→terrestrial (type-2/3/5 excluded, per manifest) |

Consequence: **"neutral" is a grab-bag** of motivational-neutral *and* environmental/ontogenetic/
condition contexts; and **agonistic comes from one species only** (macaque "negative", n = 682),
affiliative from two (macaque "positive" + meerkat). The agonistic/affiliative contrast is
therefore effectively a within-macaque signal, not a cross-species one.

**(c) Species/context confound dominates.** Archetypes 1 and 2 are 100% a single species
(shrew, frog-noise). Between-species acoustic variance (ultrasonic echolocating shrew vs 5.8 s
frog advertisement calls vs mid-frequency mammal/bird calls) dwarfs the within-species
motivational variance, so the unsupervised "core sounds" are species niches. This is the
central confound: **shape predicts *who is calling* far better than *what it means*.**

**(d) The two richest Morton corpora dropped out on units.** Elephant rumbles (alarm/protest/
greeting/contact/care contexts) and elephant "name" referents use standardised spectral features,
not Hz, and so could not join the pool. This removes the only other agonistic/affiliative
vocabulary beyond macaque — a severe limitation on the "cross-species" claim.

**(e) The referent test is degenerate** (all referent calls in one archetype; null sd = 0), so
no z can be computed for it.

**(f) "Above chance" ≠ "meaningful".** z = 19.7 on the 3-class axis reflects a +0.17
balanced-accuracy edge on 10k rows, not a strong shape→constraint code. On the theoretically
central 2-class Morton axis the result is at chance.

---

## 6. Bottom line

- **K = 3** core sounds (silhouette-selected), but they are **species clusters**, not Morton
  motivation-structural archetypes.
- **Shape → constraint does not hold cross-species** in this benchmark's pool: 0.507 vs 0.333
  on the 3-class context axis (large-n, trivial effect), **0.50 (chance)** on the agonistic vs
  affiliative axis, and the referent axis is degenerate.
- **Biggest limit:** pooling species lets between-species acoustic variance swamp the
  within-species motivational signal — the recovered archetypes are body-size/species niches,
  and the only real agonistic/affiliative contrast (macaque) collapses into one archetype.
