# Oracles without oracles

**How to verify a field that has no empirical ground truth to check against.**

Status: **method, with three worked disciplines** — physics (exact), climate (measured), economics
(identity + invariance). The invariance gate it describes is implemented at
`src/pacland/economics/invariance.py` and runs green with four seeded faults
(`python3 scripts/economics_invariance.py` → 4/4).

---

## The problem, stated properly

Physics can check a claim against a measurement. Climate can check a model against conservation
laws the Earth obeys. Economics can measure the past — and **cannot** measure the future it
forecasts. The obvious conclusion is that such a field is unverifiable.

That conclusion is wrong, and it is wrong because it assumes an oracle is *an empirical truth you
go and find*. An oracle is anything that can tell you your claim is false **without you knowing
the answer in advance**. There are five such things, and an empirical measurement is only one.

| # | class | what it is | what a failure means |
|---|---|---|---|
| 1 | **definitional** | true by construction: identities, conservation laws, exact structure | a bug — the arithmetic is wrong, or the model contradicts itself |
| 2 | **invariance** | change the *description*, not the world; the claim must not move | the claim was about the description, not the system |
| 3 | **null** | the dumbest possible predictor: no change, trend, persistence | the claim bought nothing over knowing nothing |
| 4 | **synthetic** | a world where *you* wrote the answer, then demand the method recover it | the method cannot find a truth that is definitely there — so it is not measuring that quantity |
| 5 | **cross-source** | the same quantity from a second, independent pipeline | either the finding or one of the sources is fragile |

**Cost runs the other way from power.** Classes 1–3 cost no data at all and can be run on day one.
Class 4 costs a toy model. Class 5 costs a second dataset. The empirical oracle, when it exists,
is the most expensive and the most convincing — which is exactly why a field that lacks it should
stop waiting for it and start at the top of the list.

## The decision rule

For any claim, walk the classes in cost order and stop at the first that can check it:

```
definitional  ->  invariance  ->  null  ->  synthetic  ->  cross-source  ->  no oracle
```

**If none of the five can check it, the claim is not verifiable** — and that is a *result about
the field*, publishable and fundable, not a failure of effort. It belongs in the report as
`m = 0`, with the same prominence as a success.

A certificate then fits in one line: **(oracle class, m, radius)** — which class checked it, how
many observables were actually used, and the error bound those observables buy.

## Worked example 1 — physics: the oracle is exact structure

The tadpole is a single exact invariant; every other quantity in the flux landscape is covariant.
So the physics oracle is **class 1**, and it is machine-checked in Lean. The five laws of duality
covariance are **class 2**: change the duality frame and the observables must transform, not
change their content.

The payoff is a negative result that no measurement could have given as cheaply: *a theory of
everything predicts relations, never values.* That sentence is a theorem, not a slogan.

## Worked example 2 — climate: the oracle is conservation

The Earth's energy budget closes to 0.01 W/m² **only with all reservoirs**, and misses by
0.15 W/m² on the upper ocean alone. Fifteen of nineteen CMIP6 models leak heat, one at nearly
twice the signal it is predicting. That is **class 1** — physics cannot be voted away.

The trend — *continue the warming already measured in a straight line* — is **class 3**, and it beats
persistence in every window tested. It does **not** reliably beat the emulators built from published
climate sensitivities: which of the two wins flips with the choice of start years (0.165 vs 0.178–0.192
on one window; the trend loses on two of four). That is the climate invariance gate doing its job —
see check 3 below, whose first draft failed and then narrowed the claim.
The per-model certificate (`m = 3 / 2 / 1`) is the deficit attached to class-1 checks.

## Worked example 3 — economics: the oracle is the bookkeeping, then the description

Nominal GDP components add up to **1e-4 of GDP**; the chained-dollar decomposition leaks by up to
**25 percentage points in 2020**, because chained dollars are not additive. Both facts are
**class 1**, and both are checkable with no forecast and no future.

Then the invariance gate (**class 2**), which this doc exists to introduce:

| check | what it demands | the seeded fault it catches |
|---|---|---|
| **units** | scale every nominal level by 1000: shares and the additivity residual must not move | rescaling one component moves the shares |
| **base year** | rebase the price index: inflation rates unchanged, index levels changed | reporting a level where a rate is claimed |
| **deflator** | nominal adds, real does not — the **asymmetry is asserted** | an "additive" real record, i.e. not chained dollars at all |
| **parametrisation** | invent a power law with a known elasticity; the estimator must recover it | dropping the intercept, or reading an elasticity off a level fit |

The last row is also **class 4**: we know the truth because we wrote it. Its result is uncomfortable
and that is the point — the log-log estimator recovers the true elasticity (0.62) to nine digits,
while a level-OLS fit returns 0.650, off by 0.030. **An elasticity read off a level fit is
description-dependent, so the gate refuses it.** No amount of data would have told us that; a
world we invented told us in one line of arithmetic.

And the failures that made this discipline credible are all class-3 or class-4:
structural inflation forecasts **lose** to the no-change null (1.03×); the Phillips slope cannot be
recovered from the model's own synthetic data (truth 0.18 → estimate 1.00); a VAR **beats** the
null (0.86×) and GDPNow beats it 4:1 — which is what makes the null a real test rather than a
ritual.

## Worked example 4 — the same gate on climate, where it corrected us

`src/pacland/climate/invariance.py` runs three checks, each with a seeded fault:

| check | what it proved |
|---|---|
| **baseline period** | move the 1951-80 reference to 1900-1930: anomaly offsets move, the trend rate does not (drift **0.0**) |
| **units** | Celsius to Kelvin: levels move by 273.15, skill scores move by **4e-14** |
| **window** | shift the hindcast start years: the trend beats persistence in **every** window; the trend-versus-emulator ranking is **not stable** and is therefore **not claimed** |

The third check is the one worth the module. It was written to assert *"the trend beats the emulators,
and it survives a one-year shift."* The first draft **failed** — moving the start years by one flips
the winner between the trend and two different emulators, and an emulator wins two of four windows.
The claim was therefore narrowed to what survives, and the narrowing was propagated into the site
card, the figures page, the model roster and the plain-speak one-pager in the same commit.

**A method that only ever confirms is not a method.**

## Worked example 5 — economics: the class-4 suite, and what it says about each estimator

`src/pacland/economics/recovery.py` puts every estimator the roster publishes against a truth
that we wrote, and asks two different questions: **is it correct** (noiseless recovery), and
**how much data would fix it** (the sampling law).

| estimator | noiseless recovery | what that means |
|---|---|---|
| **VAR(1)** | exact to **3.3e-14** at n = 400 | the estimator is right; only sampling error remains |
| **policy rule** | exact to **3.1e-15** at n = 600 | recoverable **when the regressor is exogenous** |
| **scorer** (MAE, null ratio) | perfect forecast → **0.0**, offset of 1.0 → **1.0** | the convention is honest at the edges, so the verdicts built on it are |
| **sampling law** | error falls as **n^-0.43**, so a 1% estimate needs **n ≈ 27,700** | the price of precision, in observations |
| **measurement error** | estimate sits at **0.50 of a true 1.0 at every n** | the bias does **not** shrink with data — an identification failure, not a noise problem |

The last row is the one worth the module, and it is the κ result generalised. Sampling error
falls as n^-1/2 and can be bought with data. **Attenuation from an error-ridden regressor does
not fall at all** — 1600, 6400 and 25600 observations all return ≈0.50 for a true 1.0. So when a
field says *"we need more data"*, the first question is **which of those two regimes it is in**.
If it is the second, the answer is not a larger sample; it is different evidence.

That distinction is now machinery rather than an argument, and it is the sharpest thing this
whole document has to offer: **a number that does not move as n grows is telling you it is
measuring the wrong thing.**

## Worked example 6 — what one archive can still tell you (and the gap it leaves)

The class-5 gap in this repo is real: the real-time vintages come from **one** archive (ALFRED).
The Philadelphia Fed's real-time set is behind a form, DBnomics does not serve the vintages, and
inventing a second source would be the exact failure this document is written against.

So the gap stays on the record as **open**. What can be done with one archive is nearly as
useful, and it is what `src/pacland/economics/vintage_sensitivity.py` does: hold the forecast
fixed and change **what counts as having happened**.

| regime | truth | forecasts scored |
|---|---|---|
| **latest** | the newest vintage — what the data says now | 26 |
| **next** | the vintage published immediately after the forecast — the **first revision** | 23 |

| model | ratio to the null, latest | ratio to the null, next revision |
|---|---|---|
| AR(1) | 0.92 / 0.88 / 0.69 | 0.89 / 0.79 / 0.74 |
| **VAR(1)** | **0.86 / 0.79 / 0.63** | **0.77 / 0.67 / 0.60** |

Both models beat the null at **every horizon in both regimes**, and the worst change in the VAR's
advantage across regimes is **0.111**. So the finding — *a plain VAR beats "tomorrow equals
today" on real-time data* — is a statement about **forecasting**, not about this archive's
revision pattern. It is also *stronger* under first revisions than under final ones, which is the
opposite of what a revision artefact would look like.

**What this is not.** It is not class 5. It is a class-2 check — the same claim under a different
*description of the target* — and it is labelled that way in the module, the script output and
here. Two sources remain the only way to close the gap, and that work is still to do.

The seeded fault is the one that matters: score each forecast against **the vintage it was made
from** and every model predicts the present perfectly, collapsing the error to zero. The check
notices and refuses it, which is what makes the two honest regimes worth anything.

## Worked example 7 — climate's fourth measured invariant: carbon

`structure.py` names five conservation laws. Three were measured (energy, ocean mass, salinity)
and two were **named but unmeasured**: water and carbon. Carbon is now measured, at
`src/pacland/climate/carbon.py`, which takes the count from **3 of 5** to **4 of 5**.

The identity, over 1979–2023 (45 paired years, two independent inputs — emissions from the
Global Carbon Budget via OWID, concentrations from NOAA GML):

| | |
|---|---|
| emitted | **1,518 GtCO2** |
| stayed airborne | **669 GtCO2** — a fraction of **0.441** |
| taken up by oceans and land | **849 GtCO2** |
| per-year fraction | 0.186 – 0.700 (s.d. 0.111) |

The mean airborne fraction, **0.44**, is the published value; the per-year swing is the El Niño
signal, and the check reports it rather than smoothing it away. What the gate demands is only
what physics demands: the fraction must be **between none and all** of emissions every year, and
its mean must sit in 0.35–0.60. The seeded fault is a budget with **no sink term** — every
emitted tonne staying airborne, fraction 1.0 — which the check refuses.

Water remains the one named-but-unmeasured invariant, and that is now a single, specific ask: a
global precipitation and evaporation pair (GPCP and an ERA5-class product) at annual resolution.

## Worked example 8 — drug discovery: the method transfers, and the assay trap

A third discipline, and the first where the verifying truth is not merely unmeasured but
**unmeasurable at the price anyone will pay**: whether a compound works in humans. That is
exactly where classes 2 and 4 earn their keep, because both run before a single dose is given.

`src/pacland/drugs/recovery.py` — 3/3 with three seeded faults:

| check | result |
|---|---|
| **class 4** dose-response recovery | invent a curve with IC50 = 50 nM, Hill = 1.0, asymptotes 10–90; the fit returns **50.0000 / 1.0000** |
| **class 4** the assay trap | pin the asymptotes at the textbook **0/100** when the truth is 10/90 → IC50 comes out **43.6% high**, while looking precisely fitted |
| **class 2** units | express concentrations in a 1000× finer unit: IC50 scales **exactly**, Hill slope moves by **0.000000** |

The middle row is the one to carry into a lab meeting. A pinned-asymptote fit is not *slightly*
off — it is off by nearly half, with a tight-looking confidence interval, and nothing in the
output says so. The invention of a known truth is what makes that visible; no amount of real
screening data would have.

## The one gap still open: water

Climate's fifth invariant — `precipitation = evaporation + d(storage)/dt` — remains **named and
unmeasured**, and it is now a single specific dependency rather than a missing idea:

**Closed** (worked example 11): both fields are available as **OPeNDAP ASCII text**, so no netCDF
client and no API key were ever needed. The earlier "blocked on a dependency" note was wrong, and is
kept here only as a reminder that a gap must record its *exact access path*.

That is the honest form of the gap: two named datasets and the reason each is out of reach
today. It is the same shape as the class-5 vintage gap — tested around where possible, left open
where not, and written down so the next session does not rediscover it.

## Worked example 9 — epidemiology: the wall, measured instead of mourned

Epidemiology was the last discipline on the site still labelled *"queued"*. Its wall is
identifiability, and `src/pacland/epidemiology/recovery.py` measures it rather than naming it.

| class | check | result |
|---|---|---|
| **4** | a cohort with a relative risk we wrote (**RR = 2.00**) and a confounder (exposure and baseline risk both rise with age) | the **crude** estimate says **RR = 4.98 — 149% too high**; the **stratified** (Mantel–Haenszel) estimate returns **2.000000** |
| **1** | persons are conserved: every case in exactly one stratum, strata rebuilding the cohort | holds, and a table that **repeats a stratum is refused** |
| **2** | re-bin the population more finely | homogeneous effect: drift **0.0** (invariant); effect modification present: drift **50% of the estimate** |

The third row is the wall in one number. With a homogeneous effect, how you bin cannot matter —
and the check proves it does not. With effect modification, **half the answer is the analyst's
binning choice**, and no confidence interval on a single estimate discloses that. This is the
honest form of an observational result: report the movement across binnings, not just the point.

Meanwhile the first row is what the cheap oracles buy: a 149% error is visible on day one, in
synthetic data, before anyone recruits a participant — because we wrote the truth and asked the
method to find it.

## Worked example 10 — drug discovery's class-5 answer: the centre is reproducible, the value is not

Class 5 asks whether an independent pipeline reports the same thing. For drug discovery the
candidate is obvious — an IC50 is published, numeric, and supposedly *the same quantity* in every
database. Two independent curation pipelines were queried keylessly
(`src/pacland/drugs/second_source.py`, `scripts/fetch_drug_second_source.py`):

| source | IC50s for imatinib | median | 10th–90th percentile | fold range |
|---|---|---|---|---|
| **ChEMBL** (EMBL-EBI) | 1,016 | **10,872 nM** | 8 – 19,000 nM | **2,293×** |
| **PubChem BioAssay** (NCBI) | 1,120 | **10,000 nM** | 4 – 10,000 nM | **2,526×** |

**Cross-source agreement on the median: 1.09×.** Two independent pipelines agree on the central
value to within 9% — that is a real, positive class-5 result, and it is what makes the second
number worth stating.

**Within-source spread: 2,293× and 2,526×.** Each database disagrees with *itself* by three
orders of magnitude across its own assays, because the assays are not measuring the same thing:
different targets, different ATP concentrations, different cell lines, one label.

So the honest statement about a single IC50 is not "this compound has potency X". It is:

> **the centre of the distribution is reproducible across independent curation; an individual
> value is not.**

That is the kind of sentence a certificate can carry and a press release cannot. It also explains
why class 5 is worth running even when it agrees: the agreement is only interpretable next to the
spread it sits inside.

## Worked example 11 — water: the last named invariant, closed with free data

The water gap was recorded as blocked on two dependencies: GPCP precipitation is netCDF behind
OPeNDAP, and ERA5 evaporation needs an API key. **Both were avoidable.** NOAA/PSL serves the fields
through OPeNDAP's **ASCII** interface — plain text over HTTPS — so water closes with no credential
and no client library (`scripts/fetch_water_budget.py`, `src/pacland/climate/water.py`).

| | product | measured |
|---|---|---|
| **precipitation** | GPCP v2.3 monthly mean | **2.84 – 3.10 mm/day** |
| **evaporation** | NCEP/NCAR latent heat flux, converted at 2.5×10⁶ J/kg | **2.67 – 2.94 mm/day** |

Five Januarys across four decades, area-weighted by cos(latitude). **P/E within 8.4% in every
sampled month**, which is what the published global water budget gives — and it takes the climate
checklist to **5 of 5**: energy, water, carbon, ocean mass, salinity, every one measured.

Two guards, both about the measurement rather than the physics:

- **weighting** — an unweighted grid mean sits **14.9–16.1% below** the area-weighted one. Without
  the guard, a missing cos(latitude) would look like a 15% disagreement between products.
- **units** — leaving the flux in W/m² makes the balance read **0.037 instead of ~1.0**, a 29×
  error with no physical meaning anywhere in the output.

The lesson for the framework is not that water was hard. It is that **"blocked on a dependency" was
wrong for two days**: the data was free, in text, and the only thing standing in the way was an
assumption about the format. A named gap should carry the *exact* access path, not a category —
which is now how the remaining gaps are written.

## Worked example 12 — economics class 5, and the target that changes the answer

The vintage gap was recorded as open. It closes in the only sense available: **a second archive now
exists in this repo**. The McCracken–Ng **FRED-MD historical vintages** are an independently assembled
real-time archive, keyless, one CSV per vintage; `src/pacland/economics/second_archive.py` compares
it with the ALFRED vintages month by month on the unemployment rate.

**8,718 series-months across three series and four vintages, and the two archives agree exactly** —
the same number to the last decimal, every month, every series (worst gap **0.000**). The series are
unemployment, industrial production and the CPI, each verified to be a level in FRED-MD before the
column was trusted. The seeded fault is an as-of control: against the vintage one year earlier,
**2,302** series-months disagree (worst 2.0 pp), so the check is sensitive to the date rather than to
the series.

Honest scope: this is a second **pipeline**, not a second **release**. It catches a wrong vintage, a
transcribed column, or an API returning the wrong as-of date. It cannot catch an error made by the
statistical agency itself, and the doctrine says so wherever the result is used.

### And the result it found on the way

Testing the archives led to the first GDP print, and to a number this repo was getting wrong by
omission. On 37 quarters (`src/pacland/economics/revisions.py`):

| question | answer |
|---|---|
| biased? | **yes, upward** — mean revision **+0.565 pp**, t = 2.39, 24/37 upward (sign-test p = 0.099) |
| memory? | **no** — AR(1) = **0.017** |
| exploitable? | **no** — a bias correction is **1.22× worse** out of sample |
| does the nowcast beat the print? | **no, against the final number** — print **0.92 pp**, nowcast **1.54 pp** |

**And it replicates.** The Philadelphia Fed publishes its own First/Second/Third/Most-Recent release
ladder for real GNP/GDP back to **1965** — a different assembly, **239 quarters**, 6.5× the history.
The same three questions give: **+0.469 pp** first→most recent (**t = 3.68**, 62% upward), **AR(1) =
−0.066**, and a bias correction that is **1.02× worse** out of sample — a wash. The 37-quarter result
was not a 2016–2025 artefact.

So *"GDPNow beats the no-change null 4:1"* stays true, and *"GDPnow is the best estimate of GDP"*
does not follow. Beating a naive null is a low bar; the thing to beat is the official first print,
and against the final number it wins. That correction is now on the site card, in the roster and in
the doctrine — in the same commit as the evidence.

## Why this transfers to every oracle-poor field

Epidemiology, drug discovery, nutrition, education, criminology, macro-finance and any model of a
complex system share the same condition: the counterfactual is unobservable, and the field mistakes
that for unverifiability. The five classes are field-independent. What changes is **which
constraint is definitional**:

| field | likely class-1 oracle | likely class-2 invariance |
|---|---|---|
| epidemiology | case-count arithmetic; conservation of persons across strata | changing the age-binning or the population denominator |
| drug discovery | mass balance, dose accounting, assay stoichiometry | changing the unit, the cell line's normalisation, the plate layout |
| nutrition | energy and nitrogen balance | changing the dietary recall instrument or the portion database |
| education | enrolment and attainment accounting | changing the test scale or the cohort definition |
| macro-finance | the accounting identities (already built here) | base year, deflator, units, reparametrisation |

A field that finds **no** class-1 constraint has said something real about itself: its quantities
are not conserved, so its claims must be carried by classes 3–5, and it should expect to certify
skill and invariance rather than structure.

## What "verified" can then mean

For an oracle-poor field, a certificate can honestly assert three things and no more:

1. **internal consistency** — the claim survives the field's own identities (class 1);
2. **description-independence** — it does not depend on units, base year, deflator, labels or how
   the model was parametrised (class 2);
3. **skill over the null** — it beats knowing nothing, on data published at the time (class 3).

What it cannot assert is a **value**: the behavioural parameters that would make a point forecast
true are not recoverable from aggregates, and no oracle class in this list can conjure them. That
is the same theorem physics reached from the other end — *relations, never values* — and it is why
the honest output of this work is the deficit, not the number.

## The gaps, named

- **The invariance gate covers economics only.** Climate and drugs have no equivalent yet; the
  obvious climate version is invariance under regridding, area weighting and the choice of
  baseline period.
- **Class 5 now has a second archive in economics** (worked example 12: FRED-MD vintages vs ALFRED,
  8,718 series-months across three series agreeing exactly) — with the scope stated: a second *pipeline*, not a second
  *release*. What remains open is a second **release**, which no free source provides.
- **Class 4 now covers five subjects in economics** (VAR, policy rule, attenuation, scorer,
  sampling law) and **one** in climate (the trend-versus-emulator ranking, which is what the
  window check turned out to be). Physics has none beyond its symbolic proofs.

Each of those is a slice of work with a number attached, which is the only kind this project
accepts.

---

Reproduce: `python3 scripts/economics_invariance.py` · `PYTHONPATH=src python3 -m unittest
tests.test_economics_invariance -q` · the bar itself: [`docs/verify-bar.md`](verify-bar.md) · the
method this sits inside: [`docs/SOP-FIGURING-SYSTEMS-OUT.md`](SOP-FIGURING-SYSTEMS-OUT.md).
