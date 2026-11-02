# The landscape fractions are computed over a mixture — and half the corpus is not vacua

**Audit of the committed corpus, 2026-11-02.** Every landscape statistic this programme quotes — the SUSY fraction, the
vacua counts, the impostor classes — is computed over `data/h12_*_stats.json`. **That corpus contains two populations, and
only one of them is vacua.**

## The two populations

| | n | flagged SUSY | flagged minima | median \|DW\| | median N |
|---|---|---|---|---|---|
| **moduli in O(1)–O(100)** | **2,907** | **42.4%** | **80.6%** | 0.62 | 23 |
| **moduli outside** (\|z\| up to 1e42) | **2,978** | **0.4%** | **0.0%** | **2.4e+22** | 8 |

**The second population is not a minimisation failure — it is the opposite.** Their residuals are **smaller** (median 3.5e-40
against 1.4e-11) and their vacuum energies **lower** (median 4.5e-18 against 6.5e-3), because at `|z| ~ 1e30` the potential is
exponentially suppressed and there is nothing left to minimise. **They are runaway points that the optimiser reached and
correctly stopped at**, and the corpus **correctly flags them**: **0.0% are minima**, 0.4% are SUSY, and their `|DW|` is
**1e22**.

**So the labels are right and the aggregates are wrong.** Any statistic computed over *all rows* is computed over a mixture of
vacua and runaway points, and the mixture changes with h12.

## What that does to the headline fraction

| h12 | rows | genuine minima | **runaways** | SUSY frac, **all rows** | SUSY frac, **minima only** |
|---|---|---|---|---|---|
| 2 | 3,424 | 1,692 | 1,295 | **27.9%** | **55.9%** |
| 3 | 1,417 | 577 | 730 | **19.7%** | **48.0%** |
| 4 | 1,044 | 74 | 953 | **1.1%** | **14.9%** |

**The published decline — 27.9% → 19.7% → 1.1% — is substantially a composition artefact.** The runaway share of each corpus
goes **38% → 52% → 91%**, so the fraction over all rows falls partly because **there are fewer vacua in the denominator**.

**Over genuine minima the decline is 55.9% → 48.0% → 14.9%**: **still a decline, from twice the height, and the dramatic part
is h12 = 4 — where there are only 74 minima**. That is a small sample, not a trend.

## What this changes and what it does not

**Does not change**: the runaways are correctly identified by the flags, so no individual claim about a *labelled* vacuum is
wrong. The counts of minima are what they are.

**Changes**: every statement of the form *"the SUSY fraction is X%"* needs to say **over what**. The numbers in the table above
are the honest pair, and **the mixed version should not be quoted again without the minima-only number beside it.**

**And it explains something that has been puzzling**: the corpus's apparent behaviour across h12 is dominated by **how many
runaway points the sampler produced**, which is a property of the sampling, not of the landscape.

## The falsifier

> **If a re-run of the sampler at h12 = 2, 3, 4 with a moduli bound enforced produces the same *minima-only* SUSY fractions
> (55.9 / 48.0 / 14.9), the composition artefact was benign and the decline is a landscape fact.** If constraining the moduli
> changes the minima count more than it changes the runaway count, then even the minima-only number is sampling-dependent and
> the fraction is not a landscape statistic at all.

## The audit's own provenance

Every number above is computed from the committed files; the classification is `max |z|` in `[1e-3, 1e3]` — the same window
the ISD diagnostic now enforces after a corrupt row made it report `cond(M) = 1.4e135` where the wall document said `1.8e2`.
