# What the physics discipline can give the other disciplines

**Rob, 2026-11-02**: catch up on the physics methodologies and see what is transferable. This is the inventory. Each row is a
**method**, where it was bought, and the first concrete use elsewhere. Nothing here is a metaphor: a method that only names
an analogy is not transferred, so every row ends in something that can be built or checked.

## The methods, as they now stand in the physics work

| # | method | where it was bought |
|---|---|---|
| **M1** | **the completion criterion is (a)+(b)+(c)** — invariants enumerated, covariance laws in closed form, the dictionary **ranked** | `docs/UNIFICATION-METHOD-v2.md` |
| **M2** | **the deliverable is the rank, not the formula** — a theorem can forbid the formula, and then the honest product is the rank and its collapses | same, and the orbit-space correction |
| **M3** | **negative theorems are results** — a map with nothing to quotient by gives a theorem of absence | same |
| **M4** | **every claim is a type: constraint, label, or count** — and the three are certified differently | `unification-synthesis.md` |
| **M5** | **pre-registration** — the prediction is written down before the run, then refuted or survived | `#346`, `#351` → refuted at `#356` |
| **M6** | **the claims registry** — PASS-1 / PASS-2 / withdrawn, each with its script, its document, and the check that could make it wrong | `docs/claims.json` + `tests/test_claims_registry.py` |
| **M7** | **a false pass is a defect class** — G2 was wrong for weeks and read as a pass | `UNIFICATION-METHOD-v2` §why |
| **M8** | **the control runs at the same dimension, the same N, the same pooling** — and refuses a verdict when the bands overlap | the X8 gate, `docs/plan-exact-terms.md` |
| **M9** | **an authority test on the pipeline itself** — GOE matrices must read GOE, and a repulsion-destroying resample must read Poisson | same |
| **M10** | **a calibration on a system whose answer is known** — before a statistic is believed where the answer is not known | `scripts/truth_bench.py`, `docs/methods-from-the-bench.md` |
| **M11** | **two-sided scoring** — what a candidate explains **×** what it predicts that was not fitted; and among candidates that explain, the **coarsest** wins | same |
| **M12** | **the falsifier is written before the number** — and a fired falsifier is kept with the note, not deleted | every note in the last week, including the one that caught my own binning bug |

## The transfer, discipline by discipline

### To RF / AirMatrix

| method | transfer |
|---|---|
| **M2, M3** | **A site has a rank too.** Design 42's `cannot` list is already this: *"a predicted level"* is refused until an AP has a position, *"a device drawn where it is"* is refused until it is located. **That is a negative theorem about the site, and it should be labelled as one** rather than read as a missing feature. |
| **M4** | **The layout's numbers are three types**: room dimensions are a **count** (measured), the placement is a **label** (chosen), the predicted level is a **constraint** (bounded by the engine). Mixing them is how a guessed position becomes a certificate. |
| **M6** | **The RF claims should be registered like the physics ones** — `-24 dB on 2.4 GHz`, `34 dB on 5 GHz`, `16 dB fading`, with a script, a document, and the check that could make each wrong. **Three of the eleven physics claims are withdrawn; the RF work has no such record.** |
| **M8, M9** | **The channel plan already does this** (same channel set, same neighbours, a 6 dB floor). **What it lacks is an authority test**: a synthetic scan in which the *right* answer is known, run through the same pipeline. That is one script. |
| **M12** | **Every RF claim here already carries a falsifier** — that habit came *from* this discipline and should stay. |

### To audio / the lab

| method | transfer |
|---|---|
| **M10** | **the room still needs its truth bench.** The acoustic arm has measured RT60, C50/C80 and NC, but a metric like C50 has no known-answer system behind it. **A synthetic room with a known IR is the same move as `truth_bench.py`.** |
| **M11** | **a correction claim should be scored two-sided**: what it corrects × what it changes that nobody measured. |
| **M8** | **the audio statistics are already control-gated** (the X8 gate came from here) — that is the one arm that has never needed the lesson. |

### To the app (robmesh-android)

| method | transfer |
|---|---|
| **M5** | **pre-registration at capture time**: before a scan, the app should state what would make it invalid — *"if any spot is heard at two levels more than 16 dB apart, the label is wrong"*. That is a falsifier carried by the instrument instead of remembered by the operator. |
| **M7** | **the app already knows the false-pass shape** — `suspect` for a zero-BSS scan and for a sensor that produced no events. **The rule it still lacks: a scan that succeeded but whose spots are all within 1 dB of each other is more likely a stuck reading than a survey.** |
| **M4** | the payload already distinguishes measured from derived (`distance_source: steps`); **the same label belongs on every field.** |

### To the estate / the way work is run

| method | transfer |
|---|---|
| **M7, M12** | **the mesh has the states and not the registry.** `pass|suspect|fail` exists; what does not is a record of *which claims were withdrawn and why*. **The physics repo has `docs/claims.json`; the mesh has `CORRECTIONS.md`, which is the same shape for corrections.** |
| **M8** | **the trust ladder already says "one machine proposes, another disposes".** X8 is the numerical form of it. |

## What has already transferred, honestly

- **the falsifier discipline** — every RF document in this repo carries one, and it caught a real defect (the 20 dB "decay"
  that was start-versus-middle).
- **the claims registry** — exists for physics; **not for RF**, which is the gap this note names.
- **the same-dimension control** — used in the channel plan; **no authority test behind it**.
- **the truth bench** — built for the room this week; **not built for the acoustic metrics**.

## The three worth doing first

1. **Register the RF claims** (M6) — `-24 dB`, `34 dB`, `16 dB fading`, `1.83%` — with scripts and falsifiers. **It costs an
   afternoon and it is the difference between a measurement and a number in a chat.**
2. **An authority test for the channel plan** (M9) — a synthetic scan whose right answer is known, through the real
   pipeline. **One script.**
3. **The acoustic truth bench** (M10) — a synthetic IR whose RT60/C50 are known, through the real analysis. **One script.**

## The falsifier for this note

> **If, after registering the RF claims, none of them turns out to be PASS-1 rather than PASS-2, this note overstates the gap
> and the RF work was already held to the standard.** The registry is cheap enough that being wrong about this costs nothing
> — which is why it should be done before arguing about whether it is needed.
