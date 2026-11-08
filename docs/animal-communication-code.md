# There is no universal acoustic code of animal meaning — measured

For Aza Raskin / Earth Species Project · 2026-11-08

## The question

Is there a shared acoustic code across species — a "Rosetta Stone" of vocal meaning — such that a call's
shape tells you its meaning regardless of species? We measured it instead of arguing it: null-modeled,
with falsifiers registered before computing.

## The two instruments (both reusable, mesh-verified)

1. **Decodability deficit** `D = 1 − (bal_acc − chance)/(1 − chance)` — how far a label is from
   deterministic decode given the acoustic features. D = 0 decodable, D = 1 at chance.
2. **Direction test** — for a motivational label, which way does the acoustic feature move, and is that
   direction *consistent across species*?

## What we measured

### 1 · Meaning is decodable, but per species (38 corpora, 42 label rows)

Ranked, most decodable first:

| # | species | label | n | bal_acc | deficit |
|---|---|---|---|---|---|
| 1 | dwarf mongoose | referent — predator type | 144 | 1.000 | **0.000** |
| 2 | American crocodile | context | 88 | 0.843 | 0.236 |
| 3 | prairie dog | context | 4138 | 0.718 | 0.423 |
| 4 | macaque | social context | 2520 | 0.597 | 0.605 |
| 5 | field cricket | context (noise) | 2955 | 0.482 | 0.647 |
| 6 | Manx shearwater | context | 508 | 0.651 | 0.698 |
| 7–10 | frogs / bustard | context | — | 0.43–0.77 | 0.71–0.77 |
| 11 | meerkat | close-call context | 2237 | 0.245 | 0.906 |
| 12 | African elephant | rumble context | 1918 | 0.114 | 0.959 |
| 13 | long-clawed shrew | context | 4243 | 0.142 | 0.981 |
| 14 | lesser treefrog | context (playback) | 2890 | 0.339 | 0.992 |
| 15 | **African elephant** | **referent — name-like call** | 625 | **0.009** | **1.000** |

The two *referents* sit at opposite ends: mongoose predator type at D = 0.000 (the referent **is** in the
sound), elephant name-like call at D = 1.000 (**which individual is addressed is not** in the sound). So
"referential" is not one thing — predator type is acoustically transparent, an individual name is an
arbitrary, learned label.

### 2 · The "core sounds" are species niches, not meaning types

Pooling all calls across species and clustering gives **K = 3** archetypes — ultrasonic shrew, long frog
call, and "mid-frequency everything else." Shape → constraint is **at chance** (agonistic vs affiliative
= 0.50). Shape predicts *who is calling*, not *what it means*.

### 3 · "Agonistic = higher" holds only 4/8

| species | Δ peak freq (agonistic − affiliative) | direction |
|---|---|---|
| macaque | +1248 Hz | ↑ agree |
| human | +216 Hz | ↑ agree |
| capuchin | +105 Hz | ↑ agree |
| pig | +386 Hz | ↑ agree |
| cheetah | **−302 Hz** | ↓ flip |
| ungulate (7 spp) | **−105 Hz** | ↓ flip |
| marmoset | −31 Hz | ≈ flat |
| elephant | +0.8 Hz | ≈ flat |

4 agree / 2 flip / 2 flat. No single direction.

### 4 · Splitting "agonistic/distress" explains the flips — and reveals the real structure

Re-cut into two axes and re-test:

- **"Aggression = low" (Morton's size-signal claim): 2/6 only** — cheetah, ungulate. Human, elephant,
  capuchin and pig all have aggression *higher* than contact.
- **"Distress/alarm = high" (urgency): 3/5** — human, elephant, pig. Stronger, but not universal.
- **Inside marmoset, "distress" itself splits**: cry (distress) = −1294 Hz (low), alarm (tsik/ekk) =
  +876 Hz (high). Alarm calls go high, distress cries go low — opposite directions, one species.

## The conclusion

**There is no single universal acoustic code of "negative" meaning across mammals.** The code is:

- **Species-specific** — shape predicts who, not what (the deficit + the K=3 species niches).
- **Multi-dimensional** — at least *valence × urgency/dominance*, with alarm-high and distress-cry-low
  pointing opposite ways even inside one species.
- **Not Morton's rule** — "low = aggressive" survives 2/6; "high = alarm" is real but narrow.

Morton's motivation-structural rules — the 50-year hypothesis of a cross-species acoustic code — mostly
**does not survive** null-modeled contact with the data. That is a measured negative, and it is the useful
answer: **do not build a universal Rosetta Stone from acoustic shape. Build per-species, per-dimension
maps** (species × valence × urgency), and the two instruments here are how you do it.

## What this offers ESP

1. A **falsifiable, measured answer** to "is there a universal acoustic code?" — no; it is species ×
   valence × urgency.
2. **Two reusable instruments** (deficit + direction) to map meaning per species, with registered
   falsifiers and permutation nulls.
3. A **benchmark** — 38 corpora, CC0/CC-BY, mesh-verified, extendable by anyone.

## Honest limits

- Feature heterogeneity: "peak frequency" is not the same physical quantity across corpora (spectral peak
  vs F0 vs mean-spectrum peak), so per-axis signs are qualitative.
- Thin groups in a few species (capuchin aggression n=18, pig fighting n=57).
- Half the human data is synthetic voice-acting (the only permissive nonverbal set we found).
- 38 corpora is not the full tree of life: the "no universal code" is a strong null on this sample, not a
  proof for every animal.

## Where it lives

- Instrument: `pacland` `discipline/animal` — `src/pacland/animal/learnability.py`.
- Benchmark: `pacland` `benchmarks/decodability/` (`benchmark.py`, `corpora.json`, `data/`).
- Evidence: `REVIEWS/animal-c1*.md`, `archetype-report.md`, `alarm_contact_report.md`,
  `axis_direction_report.md`, `human_corpus_notes.md`.
- Mesh runs: `pacland-rog` (16- and 38-corpus passes).
