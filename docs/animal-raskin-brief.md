# The decodability deficit
### How far a species' communication is from a Rosetta stone — measured

*For Aza Raskin / Earth Species Project · 2026-11-08 · three corpora, one null-modeled instrument, falsifiers registered before computing.*

---

## The thesis, corrected by measurement

"Decode animal language" is usually posed as a search for a Rosetta Stone — a translation key into a known
language. Framed that way it is an underdetermined inverse problem: infinitely many meanings fit any signal.
Our first pass concluded the meaning was always *graded*, never a deterministic code. **That conclusion was
wrong — and the test that caught it is the point of this note.**

The corrected, measured statement:

1. **The constraints are always the learnable structure** — unit inventory, dialect, context-dependence,
   sequence structure. On every corpus we tested (macaque, mongoose, sperm whale) the constraints are
   robustly learnable under null models.
2. **The meaning side is a spectrum, captured by one number we call the decodability deficit** — the
   normalised gap between the information a signal carries about a referent and deterministic decode.
3. **A Rosetta unit exists exactly where communication is functionally referential.** Dwarf-mongoose alarm
   calls encode predator type (aerial vs terrestrial) near-deterministically — one acoustic coordinate,
   peak frequency, reaches 0.955, the joint map 1.000. The same instrument reads the macaque social-context
   map at 0.60: a ~60% decodability deficit.

So the Rosetta Stone is **not a missing object**. It is a *property* that referential signals have and graded
signals lack — and it is now a **measurable number**.

---

## What we measured (three corpora, one instrument)

Method everywhere: a three-check learnability split — single-coordinate mutual information · joint ridge-CV ·
a permutation/shuffle null — with the falsifier **registered before computing**, never retrofitted.

| corpus | what it tested | result | decodability deficit |
|---|---|---|---|
| **C1** macaques — 2,520 calls, social context ([CC0](https://zenodo.org/records/3877581)) | context-free acoustic → context | bal-acc **0.597** (chance 0.33) — graded | **≈ 0.60** |
| **C1b** dwarf mongooses — 144 calls, real predator referent ([CC0](https://zenodo.org/records/5005321)) | context-free acoustic → predator type | bal-acc **1.000** joint / **0.955** single — deterministic | **≈ 0.00** |
| **C1c** sperm whales — 3,840 coda sequences, CETI corpus ([CC BY 4.0](https://doi.org/10.1038/s41467-024-47221-8)) | sequence constraints (Zipf / temporal / combinatorial) | all three **LEARNABLE** (α=−1.49; MI 0.95 bits; 1.23 vs 2.27 bits/coda) | n/a — structure, no referent |

The decodability deficit is the normalised gap **D = 1 − (bal-acc − chance)/(1 − chance)**. Referential
signals sit near zero; graded signals sit near 0.60. The same instrument, pointed at your own sperm-whale
data, found the sequence structure (the *constraints*) robustly learnable — the "structure before meaning"
half of the field's current result, now a repeatable null-modeled measurement rather than a one-off.

---

## The instrument (open, reusable)

A **constraint audit**: feed it a vocal corpus (with optional behaviour/referent labels) and it returns which
constraints hold and the decodability deficit. numpy-only core, scikit-learn only in the manual pipeline;
the CC0 corpora ship with it. Lives in the pacland `discipline/animal` branch (merged: [PR #413](https://github.com/robmitchellengineering-hub/pacland/pull/413)).

## What this offers ESP

1. **A single, comparable, null-modeled number** — the decodability deficit — to say *which* signals can be
   decoded (referential) and which cannot (graded), and how far each is. This replaces "we are looking for a
   Rosetta Stone" with "here is how far each species' communication is from one."
2. **A reusable audit** for "structure before meaning", runnable across species — demonstrated here on your
   own sperm-whale data.
3. **A discipline that catches its own overclaiming.** The falsifier that refuted our first conclusion is the
   same one that would flag an overclaim in anyone else's — registered before computing, never retrofitted.

## The honest correction (recorded, not hidden)

Our first claim — *"meaning is graded, never deterministic"* — was **refuted** by the referential test. That
is the method working as intended: a falsifier written before the numbers were computed caught our own
overclaim. The surviving claim — the **decodability-deficit spectrum** — is both true and more useful, and it
matches what the field already knows (functionally-referential alarm calls have existed since vervet
eagle/leopard/snake calls, 1980); what is new is that the referential-vs-graded distinction is now a
*falsifiable, single-number measurement* rather than a taxonomy.

## The deeper symmetry (for you specifically)

You work on two instances of the same problem: **decoding animal minds** (Earth Species Project) and
**keeping AI under human control** (Center for Humane Technology). Both reduce to one move — *measure what is
exact and falsifiable (the constraints; the control surface), not the unmeasurable (meaning;
capability-in-general)* — and both must survive their own falsifier. That single methodology, aimed at both
your fields, is the wider thing this note is an instance of.

---

*Method trace: `REVIEWS/animal-c1-learnability.md` · `REVIEWS/animal-c1b-referent.md` ·
`REVIEWS/animal-c1c-sequences.md` · instrument `pacland/src/pacland/animal/` · falsifiers
`research/animal-c1{,b,c}/REGISTERED-FALSIFIER*.md`.*
