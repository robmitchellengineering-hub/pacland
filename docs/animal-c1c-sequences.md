# C1c — animal communication, sequence constraints (frequency / temporal / combinatorial)

- **Job:** C1c of `PLANS/PLAN-animal-communication-constraint-first.md` — the SEQUENCE constraints.
- **Date:** 2026-11-08
- **Executor:** delegated subagent, running on `mac` (CPU only; 55 s total).
- **Verdict up front:** **All three sequence constraints HOLD (LEARNABLE), none is uniform.** On the
  sperm-whale coda *sequences* the unit-type frequency distribution is a strong power law, the
  temporal order of codas is predictable beyond chance, and a 2-symbol bigram grammar compresses the
  116-type inventory far better than a flat or shuffled inventory. This is the mirror image of C1:
  where C1 found the context-free *meaning* map graded (no Rosetta unit), C1c finds the *sequence
  structure* (the constraints) robustly learnable — which is exactly the plan's thesis.

---

## 1 — Dataset, licence, citation

| field | value |
|---|---|
| Title | Contextual and Combinatorial Structure in Sperm Whale Vocalisations |
| Source paper | Sharma P, Gero S, Payne R, Gruber DF, Rus D, Torralba A, Andreas J. 2024. *Nature Communications* **15**: 3617. DOI [10.1038/s41467-024-47221-8](https://doi.org/10.1038/s41467-024-47221-8) (open access, CC BY 4.0) |
| Data repo | [github.com/pratyushasharma/sw-combinatoriality](https://github.com/pratyushasharma/sw-combinatoriality) (official code+data release) |
| Archived copy | Zenodo [10.5281/zenodo.10817696](https://doi.org/10.5281/zenodo.10817696) (version DOI 10.5281/zenodo.10817697) |
| **Licence** | **CC BY 4.0** — quoted from the Zenodo record: `"license": {"id": "cc-by-4.0"}`. Reuse permitted with attribution. |
| File used (primary) | `data/sperm-whale-dialogues.csv` (500,380 bytes; blob sha `dd200dc254984eeb26ae9e6bdd5d8674822fc458`) |
| File used (robustness) | `data/DominicaCodas.csv` (747,518 bytes; blob sha `fef50004b8340eb7d8094bb31722a9383a21853b`) |

**Why this corpus:** it is a corpus of **sequences, not a per-call feature table**. Each row is one
*coda* (a click sequence) with its inter-click intervals, and `sperm-whale-dialogues.csv` carries the
**temporal order** — a recording id `REC`, a whale id `Whale`, and a timestamp `TsTo` — so the *order
of call units in time* is recoverable. That is precisely what C1's per-call macaque table lacked (C1
§5.4: "a real combinatoriality/Zipf or temporal-dependency constraint needs *sequences*, which this
per-call table does not contain").

**Shape (quoted from my inspection):** `sperm-whale-dialogues.csv` = 3,840 codas, 219 recordings,
`(REC,Whale)` groups = 411, codas per group median 6 (max 379), nClicks range 1–29. `DominicaCodas.csv`
= 8,719 codas with 35 classic `CodaType` labels.

---

## 2 — The falsifier (registered BEFORE computing — see `research/animal-c1c/REGISTERED-FALSIFIER-2026-11-08T152326+1100.md`)

Written 2026-11-08T15:23:26+1100, before any test statistic was computed; not retrofitted. The
**unit** is fixed: each coda's inter-click intervals are tempo-normalised by the coda's own median ICI,
then discretised to a 2-symbol alphabet `{S, L}` (`L` iff ratio ≥ 1.5); the coda's **unit type** = its
ordered `S/L` "rhythm string"; a **sequence** = one whale's unit types ordered by `TsTo`.

- **T1 frequency structure (Zipf):** LEARNABLE iff Zipf exponent `α ≤ −0.8` **and** `z ≥ 3` (vs a
  uniform-over-vocabulary null); UNIFORM iff `|z| < 2`.
- **T2 temporal dependency:** LEARNABLE iff `MI(next;current) ≥ 0.01 bits` **and** `z ≥ 3` (vs a
  shuffle-within-recording null); UNIFORM iff `|z| < 2`.
- **T3 combinatoriality:** LEARNABLE iff a 2-state bigram Markov grammar over `{S,L}` has
  `NLL < flat-inventory NLL` **and** `z ≤ −3` (vs a symbol-shuffle null); UNIFORM iff no advantage.

*(Registration defect, recorded not hidden — see §6.1: the T1 "z ≥ 3" glyph used the wrong sign for a
one-sided Zipfian alternative; the effect is one-sided negative. The substantive threshold α ≤ −0.8 and
the magnitude |z| = 117.85 are both met.)*

---

## 3 — What ran

Environment: `research/animal-c1c/venv` — numpy 2.0.2, scipy 1.13.1, scikit-learn 1.6.1, pandas 2.3.3.

```
python3 -m venv venv
./venv/bin/pip install numpy scipy scikit-learn pandas
./venv/bin/python measure_animal_c1c.py     # 55 s, CPU only
```

Re-run script: `research/animal-c1c/measure_animal_c1c.py`; machine-readable output
`research/animal-c1c/results.json`. Null models: 1,000 draws each, seeded `np.random.default_rng(20261108)`.

---

## 4 — The constraint table (numbers quoted, not summarised)

| constraint | statistic (observed) | null (mean ± sd) | z | effect size | verdict |
|---|---|---|---|---|---|
| **frequency structure (Zipf)** | exponent **α = −1.4911**, R² = 0.9713 | uniform α = −0.1669 ± 0.0112 | **−117.85** | 118σ below uniform; α far past −1 | **LEARNABLE** |
| **temporal dependency (predictability)** | **MI(next;current) = 0.9530 bits**; bigram acc 0.7696 vs unigram 0.6952 (+0.0744) | shuffle MI = 0.5226 ± 0.0146 | **+29.43** | +0.43 bits over the recording-composition null | **LEARNABLE** |
| **combinatoriality (grammar MDL)** | bigram Markov **NLL = 4719.81 bits (1.2291/coda, k=4)** vs flat **8735.63 bits (2.2749/coda, k=115)** | symbol-shuffle NLL = 5836.91 ± 10.84 | **−103.02** | Markov beats flat by 4,799.55 bits; beats shuffle by 0.291 bits/coda | **LEARNABLE** |

**T1 detail.** 116 distinct rhythm-string types; the rank-frequency distribution is a clean power law
(R² = 0.971). Dominant type `SSSS` (the regularly-spaced "steady" coda) = 2,644/3,840 (69%); next
`LSSS` 282, `SSS` 276, `SSSSS` 58. Robustness check on the **independent classic taxonomy**
(`DominicaCodas.csv`, 35 `CodaType` labels, 8,719 codas): exponent **α = −1.6082**, R² = 0.9390, top
types `1+1+3`=3,589, `5R1`=1,510, `5R3`=642 — the same strong-skew result on a different, larger
annotation. Note the exponent is *steeper* than human-language Zipf (α ≈ −1): the whale "lexicon" here
is more dominated by a single canonical coda than human word frequency.

**T2 detail.** 3,429 within-recording transitions. The temporal signal is real but **~65% of the MI is
self-transition (repetition runs)**: self-transition rate 0.7157, MI from self-transitions = 0.6228 of
0.9530 bits; mean same-type run length 2.77 (median 1, max 34). The dominant transition is
`SSSS→SSSS` (2,048 of 3,429 = 59.7%). So "temporal dependency" is mostly *coda repetition-run
structure* with a smaller cross-type sequential component (e.g. `SSSS↔LSSS`, 127 and 125).

**T3 detail.** A 4-parameter 2-state Markov grammar describes the whole coda corpus in 1.23 bits/coda,
vs 2.27 bits/coda for a flat 115-atom inventory (MDL 4,748 vs 9,548 bits), and vs 1.52 bits/coda for
symbol-shuffled null (z = −103). Units recombine systematically: a tiny alphabet + local transition
rules generate the 116-type inventory more economically than listing the types as independent atoms.

---

## 5 — Verdict

**The sequence constraints hold.** All three are LEARNABLE; none is uniform. Frequency structure is a
strong power law, temporal order is predictable, and unit recombination is captured by a minimal
grammar. This is the positive half of the plan's Rule-of-Three split: the *constraints* are the
learnable structure in the sequence signal — the complement to C1's finding that the context-free
*meaning* map is graded (0.60 balanced accuracy, no Rosetta unit). No animal was "decoded" or
"translated".

---

## 6 — Honest limits (named)

1. **T1 sign-convention defect (mine).** The registered "z ≥ 3" used the wrong sign: a power law makes
   the exponent *more negative* than the uniform null, so the one-sided threshold is z ≤ −3 (or |z| ≥ 3
   with the sign matched). Observed z = −117.85 and α = −1.491 both meet the substantive criteria; the
   registration glyph is recorded as wrong rather than silently flipped. (T2 and T3 registered the
   correct direction and are unambiguous.)
2. **Temporal dependency is ~65% repetition runs.** Most of the predictability is a whale repeating the
   same coda type in bursts (self-transition 0.72; max run 34), not rich inter-type sequencing. The
   cross-type sequential component exists (`SSSS↔LSSS`) but is the minority. "Predictable" here is
   closer to "run/rhythm structure" than "syntax".
3. **Discretisation is my documented choice, not the paper's pipeline.** The `{S,L}` alphabet with a
   1.5×median threshold is a clean, tempo-independent reduction, but it is not the paper's full
   rhythm × tempo × rubato × ornamentation feature space. A richer alphabet or the authors' own rhythm
   clustering could shift the exponent and the grammar's parameter count — though the null-model
   *direction* of all three results is unlikely to flip.
4. **"Combinatoriality" here is a description-length argument**, not the paper's full
   feature-combinatoriality. I show a small alphabet + local order generates the type inventory; I do
   not reproduce the paper's rhythm×tempo×rubato×ornamentation decomposition.
5. **The Markov "grammar" is a 2-state bigram**, the lightest possible sequence model (deliberately:
   the brief forbids a foundation model and heavy compute). It is a lower bound on what a richer model
   would find.
6. **Tempo is collapsed out by normalisation** and not itself analysed (out of scope for the three
   sequence constraints).
7. **No referent/context labels are used** — this is a structure-only test, so it says nothing about
   "meaning" (which is C1/C2's job, and which C1 already found to be graded).
8. **Sample is one population** (Dominica, mostly clan EC1 in the classic table). Cross-population
   generality is untested here.

---

## 7 — Where this lives

- Analysis: `research/animal-c1c/measure_animal_c1c.py` (re-runnable)
- Data: `research/animal-c1c/data/sperm-whale-dialogues.csv`, `research/animal-c1c/data/DominicaCodas.csv`
- Falsifier registration: `research/animal-c1c/REGISTERED-FALSIFIER-2026-11-08T152326+1100.md`
- Machine output: `research/animal-c1c/results.json`
- This review: `REVIEWS/animal-c1c-sequences.md`
- Not committed, not pushed to `pacland` (per the brief).
