# Cross-species alarm-vs-contact acoustic direction test

**Question:** is the direction "agonistic/distress calls are *higher* (peak frequency) and *broader*
(bandwidth) than affiliative/contact calls" consistent across species?

**Verdict: NO — it is not consistent.** The peak-frequency direction holds clearly in 4/8 species,
*reverses* in 2 (cheetah, ungulate), and is absent (≈0) in 2 (marmoset, elephant). The two flips are
both **agonistic** (aggression) corpora, where threat calls are *low*-pitched size signals — the
opposite of a high-pitched distress/alarm call. The phrase "agonistic/distress" in the hypothesis
conflates two things that point in opposite directions.

## Cross-species direction table

Δ = alarm/agonistic mean − contact/affiliative mean. Positive Δpeak = agonistic higher (consistent);
negative = agonistic lower (flip). `direction` refers to **peak frequency**.

| species | n (alarm/contact) | Δ peak_freq (Hz) | Δ duration (s) | Δ bandwidth (Hz) | peak direction |
|---|---|---|---|---|---|
| macaque (given) | 682 / 693 | **+1248.0** | ≈ 0 | **+642.0** | ↑ agree |
| human (given) | 336 / 310 | **+216.0** | +0.70 | **+269.0** | ↑ agree |
| marmoset | 39 488 / 98 145 | −30.6 | +0.061 | n/a | ≈ 0 |
| cheetah | 95 / 39 | **−302.0** | +1.001 | +319.2 | ↓ **flip** |
| ungulate (7 spp.) | 2 508 / 673 | **−104.6** | +0.453 | −384.1 | ↓ **flip** |
| elephant | 154 / 295 | +0.8 | −1.438 | +0.3 | ≈ 0 |
| capuchin | 18 / 67 | **+105.3** | +0.181 | +90.9 | ↑ agree |
| pig | 4 572 / 2 315 | **+385.5** | +0.233 | −193.3 | ↑ agree |

## Sign-consistency result

**Peak frequency ("agonistic higher?") — NOT consistent.**
- **Agree** (agonistic higher, clear margin): macaque, human, capuchin, pig → **4 / 8**.
- **Disagree / flip** (agonistic *lower*): **cheetah** (−302 Hz), **ungulate** (−105 Hz) → **2 / 8**.
- **≈ no difference**: marmoset (−30.6 Hz = 0.3 % of a ~8.9 kHz mean), elephant (+0.8 Hz = 1.7 % of a
  ~46 Hz mean) → **2 / 8**.

Strict sign-only count: 5 ↑ (macaque, human, elephant, capuchin, pig) vs 3 ↓ (marmoset, cheetah,
ungulate) — but marmoset and elephant are within noise, so the honest reading is
**4 agree / 2 flip / 2 flat**.

**Bandwidth ("agonistic broader?") — NOT consistent either.**
- Broader (agree): macaque, human, cheetah, capuchin → **4**.
- Narrower (flip): ungulate (−384 Hz), pig (−193 Hz) → **2**.
- ≈ 0: elephant (+0.3 Hz) · n/a: marmoset (no spectral-bandwidth feature).

**Duration ("agonistic longer?") — mostly consistent (secondary).**
- Longer (agree): human, marmoset, cheetah, ungulate, capuchin, pig → **6**.
- Shorter (flip): elephant (−1.44 s) · ≈ 0: macaque → **1 each**.

**Bottom line.** The headline "higher + broader" does **not** survive the fold-in: it holds as a
family-resemblance trend (4 species), but cheetah and ungulate cleanly reverse the peak-frequency
direction, and marmoset/elephant show no peak-frequency effect at all. The "broader" claim is even
weaker (2 of 7 measurable species flip). Only "longer" is broadly consistent (6/8).

## Honest limits

### Feature-mapping assumptions (the biggest limit)
"peak frequency" is **not the same physical quantity** across corpora, so the Δ signs are not strictly
comparable in kind:
- macaque `q2_frequency` (spectral median) · human `peak_freq` · marmoset `Peak frequency` (Hz at max
  amplitude) · cheetah `fpeak` (max-amplitude frequency) · **ungulate `pitch_median` (median F0)** ·
  elephant `pfc_mean` (mean peak frequency) · capuchin `peak frequency on the mean spectrum` · pig
  `Fpeak`.
- Ungulate uses *fundamental frequency* (F0) as "peak frequency" per the brief, which is a lower,
  different quantity than a spectral peak/centroid. Sensitivity: ungulate Δpeak is −105 Hz with
  `pitch_median`, −295 Hz with `specCentroid_median` (the brief's fallback), +1.8 Hz with
  `peakFreq_median` — the *sign* (flip) is robust to the choice, but the magnitude is not.
- "bandwidth" likewise ranges from q3−q1 (macaque) / q75−q25 (cheetah, ungulate, pig — energy
  quartiles) to `pf_range` (elephant) / "range of spectral energy" (capuchin). Marmoset has no
  spectral-bandwidth feature → left blank, not zero.

### Label coarsening
- The binary "agonistic/distress vs affiliative/contact" conflates **aggression** (low-pitch size
  signal) with **distress/alarm** (high-pitch urgency). The two flips are both agonistic corpora, so
  this conflation is doing real work in the negative results.
- Elephant `sep` (separation) is lumped into contact/affiliative **as the brief instructs**, but it is
  arguably distress; if `sep` were moved to the alarm side, elephant Δpeak would shift from +0.8 Hz to
  ≈ +8.7 Hz (agonistic higher) — still not a flip, but the call is material.

### Per-corpus quirks
1. **Marmoset** — `Label` is numeric; decoded via the workbook `legend` sheet. alarm = {1 cry, 2
   compound cry, 7 tsik, 8 ekk}; contact = {3 trill, 4 twitter, 5 trill-phee, 6 phee, 11 grunt,
   31/51/61 segmented trill/phee}. **4 609 calls excluded** as un-decodable/transition codes
   (9 "peep" n=3948, 32 "cry-trill" n=332, 12 n=319, and ≤3 each of 23/33/41/55/62/77). Legend marks
   `11=grunt` "not used" but it is present (n=301) and the brief lists it as contact — kept as contact.
2. **Cheetah** — brief names agonistic = growl/how/hiss and contact = chirp/purr, but the table also
   has **chirr** (97 % courting → affiliative, added to contact) and **meow** (solicitation/frustration,
   neither cleanly agonistic nor affiliative → excluded, n=60). Direction is robust to all three
   labelings (strict chirp+purr, +chirr, +chirr+meow): Δpeak = −291 / −302 / −619 Hz — always flip.
   Some missing fpeak (9) and duration (22) rows dropped.
3. **Ungulate** — the feature table is **not** in the Zenodo record (which holds only the 3 181 WAVs
   plus a repartition sheet); it is the paper's **Data S2** (iScience 2025, PMC11847267), downloaded
   from the Elsevier CDN. `pitch_median` has 120 unvoiced calls (NaN) excluded from the peak mean, not
   imputed to 0 (the paper imputes 0 before ML; imputing 0 here would inflate the flip). Pooled across
   7 ungulate species with no within-species weighting beyond raw counts (Negative n=2508 is cow-heavy).
4. **Elephant** — `context analysis.txt` joins `acoustic analysis single combined rumbles.txt` on
   `unique_ID` **after stripping the `.wav_*` suffix** (the two files use different ID spellings):
   494/539 rumbles join; 45 unmatched + 29 `nrs` + 16 `logistics` excluded (90 total). `total_dur` is
   in seconds; `pfc_mean`/`pf_range` in Hz.
5. **Capuchin** — agonistic = "Aggressive contact note" (**n=18, very thin**); contact = "Contact note"
   (n=67). The other 8 call types (Hip, Trill, Grgr, Chihui, Food-associated WS, Double hip, Raspy
   oestrous, Sirena; 304 calls) are out of the brief's two named categories and excluded.
6. **Pig** — `Valence` Neg→alarm (4572), Pos→contact (2315). Fpeak→peak, Dur→duration, Q75−Q25→bandwidth.

### Inputs used as-is (not recomputed)
macaque (Δpeak +1248 Hz, Δbw +642 Hz, Δdur ≈ 0; from `data/macaque_Rebout_et_al_data_excel.xlsx`,
context negative/positive) and human (Δpeak +216 Hz, Δbw +269 Hz, Δdur +0.7 s; from
`human_corpus.csv`, category agonistic/affiliative). n reported here is the group size only.

## Data files
- `alarm_contact_direction.csv` — one row per species (this table).
- Corpora under `data/new_corpora/` (marmoset.xlsx, cheetah.xls, ungulate_s2/Data S2.xlsx,
  elephant_rumbles.txt + elephant_context.txt, capuchin.xlsx, pig.xlsx).
