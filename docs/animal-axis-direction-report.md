# Cross-species acoustic direction, re-cut into three motivational categories

**Question.** Does the acoustic (peak-frequency) direction hold **per axis** once
"agonistic/distress" is split into **aggression** vs **distress/alarm**?

- **Axis A — aggression vs contact.** Hypothesis: aggression is *lower* (size signal) → Δpeak < 0.
- **Axis B — distress vs contact.** Hypothesis: distress is *higher* (urgency) → Δpeak > 0.

Δ = group mean − contact mean. "flat" = |Δpeak| ≤ 5% of the contact mean (within noise).

## Axis A — aggression vs contact (hypothesis: aggression LOWER)

### Axis A table

| species | n (group/contact) | mean peak group (Hz) | mean peak contact (Hz) | Δ peak (Hz) | Δ dur (s) | Δ bw (Hz) | peak verdict |
|---|---|---|---|---|---|---|---|
| human | 284 / 310 | 560.4 | 375.1 | 185.3 | 0.2 | 267.3 | **flip** |
| cheetah | 95 / 39 | 268.6 | 570.6 | -302.0 | 1.0 | 319.3 | **agree** |
| ungulate | 173 / 241 | 374.4 | 505.3 | -130.9 | -0.6 | 126.0 | **agree** |
| elephant | 154 / 56 | 46.4 | 38.3 | 8.1 | -1.9 | 2.5 | **flip** |
| capuchin | 18 / 67 | 922.8 | 817.5 | 105.3 | 0.2 | 90.9 | **flip** |
| pig | 57 / 1,725 | 2,024.6 | 736.6 | 1,288.0 | 0.1 | 963.7 | **flip** |

**Verdict.** agree 2 / flip 4 / flat 0.
- agree (aggression lower): cheetah, ungulate
- flip  (aggression higher): human, elephant, capuchin, pig
- flat  (no difference): —

## Axis B — distress vs contact (hypothesis: distress HIGHER)

### Axis B table

| species | n (group/contact) | mean peak group (Hz) | mean peak contact (Hz) | Δ peak (Hz) | Δ dur (s) | Δ bw (Hz) | peak verdict |
|---|---|---|---|---|---|---|---|
| human | 95 / 310 | 805.9 | 375.1 | 430.8 | 3.0 | 215.7 | **agree** |
| marmoset | 39,488 / 98,145 | 8,853.3 | 8,883.8 | -30.6 | 0.1 | n/a | **flat** |
| ungulate | 2,335 / 241 | 413.4 | 505.3 | -91.8 | -0.2 | 15.2 | **flip** |
| elephant | 239 / 56 | 47.3 | 38.3 | 9.0 | -0.6 | 2.6 | **agree** |
| pig | 5,105 / 1,725 | 1,220.9 | 736.6 | 484.3 | 0.2 | 164.2 | **agree** |

**Verdict.** agree 3 / flip 1 / flat 1.
- agree (distress higher): human, elephant, pig
- flip  (distress lower): ungulate
- flat  (no difference): marmoset

## Category means (full transparency)

**human** (peak=peak_freq, dur=duration, bw=bandwidth (all from human_corpus.csv `emotion`))
  - aggression: n=284, peak=560.4 Hz, dur=5.3 s, bw=2,239.1 Hz
  - distress: n=95, peak=805.9 Hz, dur=8.0 s, bw=2,187.5 Hz
  - contact: n=310, peak=375.1 Hz, dur=5.0 s, bw=1,971.8 Hz

**marmoset** (peak=Peak frequency, dur=Duration, no bandwidth; excluded 4609 undecodable codes (9,12,32,23,33,41,55,62,77))
  - distress: n=16,493, peak=7,589.6 Hz, dur=0.7 s, bw=n/a Hz
  - distress/alarm: n=22,995, peak=9,759.6 Hz, dur=0.1 s, bw=n/a Hz
  - contact: n=98,145, peak=8,883.8 Hz, dur=0.2 s, bw=n/a Hz

**cheetah** (peak=fpeak, dur=duration, bw=q75-q25; meow excluded (n=60))
  - aggression: n=95, peak=268.6 Hz, dur=1.5 s, bw=1,240.1 Hz
  - contact: n=39, peak=570.6 Hz, dur=0.5 s, bw=920.9 Hz

**ungulate** (peak=peakFreq_median, dur=duration, bw=quartile75-quartile25 (7 spp); 432 rows outside the three keyword groups excluded (Food anticipation / In pair with food and toys))
  - aggression: n=173, peak=374.4 Hz, dur=0.9 s, bw=1,486.0 Hz
  - distress: n=2,335, peak=413.4 Hz, dur=1.3 s, bw=1,375.2 Hz
  - contact: n=241, peak=505.3 Hz, dur=1.5 s, bw=1,360.0 Hz

**elephant** (peak=pfc_mean, dur=total_dur, bw=pf_range; joined 539 rumbles (45 unmatched); nrs+logistics excluded)
  - aggression: n=154, peak=46.4 Hz, dur=1.4 s, bw=13.9 Hz
  - distress: n=239, peak=47.3 Hz, dur=2.7 s, bw=14.0 Hz
  - contact: n=56, peak=38.3 Hz, dur=3.3 s, bw=11.4 Hz

**capuchin** (peak='peak frequency on the mean spectrum', dur=duration (sec), bw='range of spectral energy'; only 2 named call types kept, 8 other call types excluded)
  - aggression: n=18, peak=922.8 Hz, dur=0.2 s, bw=197.8 Hz
  - contact: n=67, peak=817.5 Hz, dur=0.0 s, bw=106.9 Hz

**pig** (peak=Fpeak, dur=Dur, bw=Q75-Q25; 'Run' (n=737) is in the contact group per the brief but has NO acoustic features (737/737 Fpeak NaN) -> counts toward n but not the mean)
  - aggression: n=57, peak=2,024.6 Hz, dur=0.3 s, bw=2,869.6 Hz
  - distress: n=5,105, peak=1,220.9 Hz, dur=0.4 s, bw=2,070.1 Hz
  - contact: n=1,725, peak=736.6 Hz, dur=0.2 s, bw=1,905.9 Hz

**macaque** (negative mixes aggression+submission -> unsplittable; reported separately, not in either axis):
  - negative: n=682, peak=2,185.3 Hz, dur=0.2 s, bw=1,463.4 Hz
  - neutral: n=1,145, peak=862.1 Hz, dur=0.2 s, bw=601.3 Hz
  - positive: n=693, peak=937.5 Hz, dur=0.2 s, bw=821.5 Hz

## Marmoset "distress/alarm" is itself a cancellation (do not read it as null)

The Axis-B flat for marmoset (−30.6 Hz) is **not** an absence of effect: the merged bucket
hides two groups pointing opposite ways.

| marmoset sub-group | n | mean peak (Hz) | Δ vs contact |
|---|---|---|---|
| cry / compound-cry (distress proper) | 16,493 | 7,589.6 | -1,294.3 |
| tsik / ekk (alarm) | 22,995 | 9,759.6 | 875.8 |
| contact | 98,145 | 8,883.8 | — |

So even inside marmoset, **alarm (tsik) is high** (consistent with urgency) while
**distress/cry is low** — the same axis split seen species-wide, at the sub-label level.

## Ungulate peak-column sensitivity

Ungulate is the only species whose axis sign changes with the choice of "peak" column:

| column | aggression | distress | contact | ΔA (agg−contact) | ΔB (dist−contact) |
|---|---|---|---|---|---|
| peakFreq_median (used) | 374.4 | 413.4 | 505.3 | -130.9 | -91.8 |
| pitch_median (F0) | 301.6 | 231.8 | 306.4 | -4.8 | -74.6 |
| specCentroid_median | 1,716.5 | 1,578.0 | 1,673.7 | 42.8 | -95.7 |

The ungulate **distress-lower** flip is robust to all three (−92 / −75 / −96 Hz), but its
**aggression-lower** "agree" is *not* (it flattens with pitch ≈ −5 Hz and reverses with
centroid +43 Hz). That removes ungulate from the "robust agree" column of Axis A.

## Honest limits

1. **Label re-cut assumptions.** The three-way split re-labels the same corpora; it does not
   re-measure. Each mapping follows the brief's finest label column. Where a corpus had no
   clean group for an axis it is dropped from that axis (marmoset and cheetah have no
   aggression group; cheetah and capuchin have no distress group).
2. **"peak frequency" is not one physical quantity** across corpora:
   human `peak_freq` · marmoset `Peak frequency` (Hz at max amplitude) · cheetah `fpeak` ·
   ungulate `peakFreq_median` (spectral peak, not F0) · elephant `pfc_mean` (mean peak
   frequency contour) · capuchin "peak frequency on the mean spectrum" · pig `Fpeak` ·
   macaque `q2_frequency` (spectral median). Signs are the robust signal; magnitudes are not
   cross-comparable.
3. **Marmoset** "distress" bucket merges cry/compound-cry (n=16,493)
   with tsik/ekk (n=22,995) into one "distress/alarm" group;
   the two sub-groups point opposite ways (see above). Contact n=98 145. 4 609 undecodable
   codes excluded. No spectral-bandwidth feature (bw n/a).
4. **Capuchin** aggression is *very thin*: "Aggressive contact note" n=18 vs "Contact note"
   n=67; the other 8 call types (n=304) are excluded, so its Axis-A flip rests on 18 calls.
5. **Macaque** `negative` mixes aggression + submission with no finer label → kept as one
   group, reported separately, **not** counted in either axis.
6. **Pig** "Run" (n=737, contact) has no acoustic features (all 737 Fpeak/Dur/Q rows NaN) so
   it inflates the contact *count* without entering the contact *mean*; the pig Axis-A flip
   also rests on a thin Fighting group (n=57).
7. **Ungulate** pooled across 7 species (cow-heavy); 432 rows outside the three keyword
   groups (Food anticipation, "In pair with food and toys") excluded; the contact group is
   only n=241.
8. **Elephant** contact (af) is thin (n=56); only 494/539 rumbles join a context label. Its
   Axis-A "flip" is a real +8.1 Hz (21% of the 38 Hz contact mean) but rests on those 56 af
   calls.
9. **Cheetah** "meow" (n=60) excluded as neither cleanly aggressive nor affiliative.
10. **Human** distress mean is inflated by `panic` (n=2, peak 2 325.6 Hz); dropping panic the
    distress mean is 773.2 Hz — still clearly above contact,
    so the Axis-B agree is robust.

## Bottom line

- **Axis A ("aggression = low size signal") does NOT generalize.** 2 agree (cheetah, ungulate)
  / 4 flip (human, elephant, capuchin, pig). Only cheetah's aggression-low is robust;
  ungulate's is column-dependent. Human, elephant, capuchin and pig all have aggression
  *higher* than contact.
- **Axis B ("distress = high urgency") is the stronger, but still not universal, claim.**
  3 agree (human, elephant, pig) / 1 flip (ungulate) / 1 flat (marmoset). Marmoset's flat is a
  cancellation (alarm high, cry low), so "alarm-high" is better supported than "distress-high".
