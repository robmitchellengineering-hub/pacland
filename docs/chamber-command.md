# Chamber analysis as one command — and it caught itself contradicting

**Reproduce:** `python3 scripts/chamber_plan.py --chamber 3,2.5,2.2 --frequency 0.3 --q 200`

A test house asks one question of a chamber: **is it over-moded at this frequency.** This answers it from the
chamber's own dimensions and its **measured Q**, and reports two LUF estimates side by side:

```
CHAMBER   3.0 x 2.5 x 2.2 m   V = 16.50 m3   S = 39.2 m2   Q = 200
          assessed at 0.300 GHz
  modes below the frequency          130   Weyl 135 (+4.18%)
  distinct frequencies                88   (32.3% degenerate)
  modal width at this Q             1.50 MHz
  modes inside one width               0   -> NOT diffuse

  LUF by rule of thumb             149.9 MHz
  LUF by closed form (Weyl)        235.1 MHz   (1.57x the rule)
  LUF by exact mode count          339.5 MHz   (2.26x the rule)
  -> the closed form DISAGREES with the count by -31%; the COUNT is the ground truth

  VERDICT: MARGINAL at 0.300 GHz — above the rule of thumb but BELOW the exact LUF
           the rule would pass this chamber here; the criterion this engine uses would not.
```

## Two defects it found in itself, in one sitting

**1. It said USABLE and NOT diffuse at the same frequency.** The verdict compared the frequency to the closed-form
LUF while the line above it counted real modes in the window — two different computations, disagreeing. **Fixed by
deciding the verdict on the same count it prints.**

**2. The closed form overestimates at low mode count, and a bisection cannot find the LUF.** Weyl's *density* is
asymptotic; near the fundamental it predicts a diffuse field where the exact enumeration finds **zero** modes in a
modal width. And because the window count is **not monotonic** in frequency — different frequencies sample different
degenerate clusters — a bisection returned 290 MHz for a chamber whose window at 300 MHz holds nothing. **The LUF is
now found by an upward scan that remembers the last frequency that failed**, which is robust to the clusters.

**So the closed form is the fast asymptotic answer and the count is the ground truth; when they disagree by more
than 5%, the tool says so by name and uses the count.**

## Why it matters commercially

The **rule of thumb says this chamber is usable from 150 MHz. The count says 340 MHz.** That is a factor of 2.3, on
a verdict a lab uses to decide whether a measurement means anything — and the rule has **no Q in it at all**, while
the number it should depend on moves 60% between Q = 100 and Q = 400.

## Falsifier, printed with every run

> **If a measured field-uniformity run is acceptable while this says MARGINAL or UNUSABLE, the criterion is too
> strict. If uniformity is unacceptable while this says USABLE, it is too loose. One uniformity-versus-frequency
> measurement settles it.**

## Tests

Six, including the one that would have caught defect 1: **the tool may never say `VERDICT: USABLE` while its own
window count says `NOT diffuse`** — and the first version of that test passed for the wrong reason, because
"UNUSABLE" contains "USABLE".
