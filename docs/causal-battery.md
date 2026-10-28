# The known-truth battery for causal estimators

Every method used to estimate a causal effect can be scored on data where **the true effect is known
by construction**. Almost nobody publishes that as a standard. This does.

## The result

60 replications per cell, tolerance 15% of the planted effect, one seed, reproducible from
`python3 scripts/causal_battery.py`.

| design | estimator | median estimate | planted effect | recover | verdict |
|---|---|---|---|---|---|
| clean DiD | difference-in-differences | +1.028 | 1.00 | 70% | recovers |
| **broken trends** | difference-in-differences | **+1.830** | 1.00 | **0%** | **FAILS** |
| staggered adoption | two-way fixed effects | +1.106 | 1.00 | 57% | borderline |
| staggered adoption | not-yet-treated | +0.994 | 1.00 | 75% | recovers |
| **weak instrument** | 2SLS | +1.053 | 1.00 | **10%** | **FAILS** |
| weak instrument | OLS | +1.799 | 1.00 | 0% | FAILS |
| **measurement error** | OLS | **+0.504** | 1.00 | **0%** | **FAILS** |
| measurement error | 2SLS | +0.999 | 1.00 | 100% | recovers |

**4 of 8 cells recover the planted effect in at least half of replications.**

Read it as a matrix, not a verdict: each estimator wins the design matched to it and loses the
others. That is the point — there is no "the estimator", only an estimator and a design.

## The three failures worth quoting

**1. Difference-in-differences under broken trends: +83% bias, zero recoveries.** The treated group
was already on a different path. The estimator reports 1.83 when the truth is 1.00. This is not a
small-sample problem; it is the estimator answering a different question.

**2. 2SLS with a weak instrument is right on average and wrong most of the time.** Median 1.053,
close to the truth — but only **10% of replications** land within 15% of it. A mean would have called
this estimator "unbiased". The recovery rate exposes it: **an estimator can be unbiased and still
almost always wrong**, which is exactly why reporting a point estimate plus a standard error is not
enough.

**3. OLS under measurement error lands on 0.504 — the textbook attenuation factor.** The truth is
1.00 and the theoretical result is `var(x*)/(var(x*)+var(e)) = 0.5`. The battery reproduces it to
three digits, which is how we know the battery is measuring something real rather than a coding
accident.

## The mechanism, not just the number

For staggered adoption the battery does not merely report that two-way fixed effects is biased. It
shows **what the bias tracks**:

| effect growth | TWFE | not-yet-treated |
|---|---|---|
| flat (0.0) | +1.000 | +1.034 |
| growing (1.2) | **+1.209** | +1.034 |

TWFE moves with the growth of the effect; the not-yet-treated comparison does not move at all. A
check that only said "TWFE is biased here" would pass even if both estimators were broken. This one
fails if either is mis-implemented.

## Why this matters

The replication crisis in medicine, economics and social science is, at bottom, a **known-truth**
problem. Methods are adopted because they are popular, not because anyone showed they recover an
effect that was planted. The battery is cheap — minutes on a laptop, no dependencies — and it scores
the four most-used estimators in applied work.

The honest reading of this table is not "these methods are bad". It is **"each of these methods is
right about the design it was built for, and they are used far outside it."**

## Reproduce

```
python3 scripts/causal_battery.py
```

Every cell is deterministic given the seed; the same seed produces the same table, and a test asserts
it. Verification lives in `tests/test_causal_battery.py` (8 tests): the control design must recover,
the naive estimators must fail where they are documented to, OLS attenuation must land on 0.5, and
the staggered mechanism must show TWFE moving while not-yet-treated does not.
