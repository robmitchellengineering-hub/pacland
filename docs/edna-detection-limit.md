# eDNA detection theory — a methods-only discipline, and the pass it had to survive first

**Added 2026-11-02, with directives.** Rob: *"add it with these directives as another discipline."* The directives are the
three in `src/pacland/edna/__init__.py`: **methods only**, **enter through the control**, **the falsifier first**.

## Directive 3 came first, and it partly fired

**The falsifier**: *if the field already has a standardised known-composition control with published error bars, the
contribution is zero and this discipline should not exist.*

**What a literature pass found:**

- **mock communities are standard practice** — a known-composition control *does* exist, and occupancy modelling is used
  alongside it to handle detection error ([Methods in Ecology and Evolution, 2025](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210x.70328));
- **contamination is a named, serious problem** — *"contamination induced during on-site sampling … can massively affect"*
  results ([Springer, 2025](https://link.springer.com/chapter/10.1007/978-3-032-15904-5_13));
- **reference databases are the acknowledged weak point** — *"high quality, comprehensive DNA reference databases … is a
  problem for all types of eDNA monitoring."*

**So the falsifier fires on the broad claim** — *"we will bring a calibrated control"* is **already done by the field** — and
**the discipline is narrowed to survive it**: what is **not** standard is the **limit curve** — *how many species N samples
and a read budget can distinguish, at what error rate*, as a function of effort and contamination. **That is the deliverable,
and nothing wider.**

## What the laws say

`src/pacland/edna/limit.py` — four statements about a Poisson counting process. **No species, no ecosystem, no abundance of any
real sample.**

| law | statement |
|---|---|
| **detectability** | P(detect) = 1 − e^(−λ), and needing two reads is strictly harder than one |
| **the floor** | with contamination ε per sample, a detection must clear the Poisson quantile of ε·N — **the eDNA form of the 6 dB action floor** |
| **the limit** | the **species' own** read contribution needed to clear that floor at 95% — and it falls as **1/√N** in samples |
| **resolution** | how many species a read budget carries once the noise between them is accounted for — **the mode-count analogue** |

**Run**: `python3 scripts/edna_limit.py`

```
samples lower the limit: True | contamination raises it: True
```

## The two failures this discipline produced on its first day

**1. The units were wrong, and the run said so.** The first version claimed *"more samples lower the detection limit"* and
reported the **total** limit — which **rises** with N, because more samples mean more total background. **The law is about the
limit PER SAMPLE, which falls as 1/√N.** The falsifier in the script caught it before anything was published.

**2. The floor and the limit are different units, and a test caught it.** The floor is a **total** read count; the limit is
the **species' contribution above the background**. At ε = 1.0 over 10 samples the background alone is 10 of the floor's 15,
so a species needs only about 12 of its own — **below the floor, and correctly so.** A test asserting `limit ≥ floor` failed
and was corrected, not the code.

**Both are recorded because they are the discipline working**: a claim, a check that could fail, and the correction.

## What this discipline may and may not say

**May**: *"at this contamination rate and this sampling effort, a species contributing fewer than X reads could not be
distinguished from the library's own background."*

**May not**: that a species is present, absent, rare, or threatened. **That is a biological claim and this arm does not make
them.**


## The bench, on a REAL mock community — and the test that could not fail

**Data**: a published mock-community run with a **known composition** — eight bacterial species at stated relative abundances,
five polymerases × four PCR cycle numbers = **160 species-conditions**, each with the expected abundance beside the observed
count. Table: `data/edna/mock_bias_species.tsv` (Schloss lab, Sze et al., mSphere 2019 — public, and it carries the truth).

**The first test was vacuous, and the script now says so before it runs.** At full depth **all 160 species-conditions were
detected** — the shallowest run still had 1,022 reads for eight species — so the empirical detection probability was **1.000
everywhere and the law could not fail**. *A test that cannot fail is not a test.*

**So the test is a rarefaction**: subsample each real run down to a stated depth, keeping the real composition and the assay's
own biases, and ask whether the species survives. 67,200 species-draws over seven depths.

### The measured curve

| expected reads | n | **observed P** | Poisson P | gap |
|---|---|---|---|---|
| **0.3 – 1.0** | 1,200 | **0.716** | 0.504 | **+0.211** |
| 1.0 – 3.0 | 4,800 | 0.898 | 0.847 | +0.051 |
| 3.0 – 10.0 | 16,800 | 0.980 | 0.997 | −0.017 |
| 10.0 + | 25,200 | 1.000 | 1.000 | 0.000 |

### What it says — a correction, not a confirmation

- **Above ~3 expected reads the Poisson law is excellent.** The counting law holds where it is claimed to hold.
- **Below ~1 expected read it is wrong, and in the safe direction**: **observed 0.716 against a predicted 0.504**. Real reads are
  **more clustered than a pure Poisson process**, so a species at a fraction of a read is still often caught.
- **So the closed-form limit is CONSERVATIVE at the bottom of the range** — the opposite of how a limit is usually assumed to
  fail. The formula is right in the middle and pessimistic at the edge.

### Why this is the discipline working

**The falsifier was written before the data was touched**, and the run **falsified the tidy version of the law** — twice:
once because the test could not fail (fixed by rarefaction), once because the law is biased low at the edge (recorded, not
tuned away).

**Both are in the script's own docstring and output**, so the next person reads the correction before the claim.

## The next artefact

**A known-composition synthetic community through a real pipeline**, swept over samples, depth and contamination — producing
the **limit with its error bar** on real output rather than on the closed form. **That is `truth_bench.py` for DNA**, and it is
the only thing that would turn these laws into a measurement.

## The falsifier for the discipline itself

> **If the limit curve turns out to be a restatement of standard occupancy-detection mathematics with no new operational
> content — that is, if an operator could get the same answer from existing tools — then this arm is a duplicate and should be
> closed.** The narrow hope is that the curve gives a **sample-size prescription** (what effort buys what limit) that the
> existing tools do not present, and that is testable against them directly.
