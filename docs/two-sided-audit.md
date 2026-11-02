# Rule 1 applied to the landscape: which claims it touches, and which it does not

The bench's first rule came from a room — **a candidate that explained 100% of the measured peaks was 33.9% wrong**,
because more free structure can always cover more data. `scripts/two_sided_audit.py` runs that rule over the landscape's own
structure claims. **Its first useful output is which claims the rule does not apply to.**

## The three claims

| claim | exact or fit? | degrees of freedom | what it predicts that was not fitted |
|---|---|---|---|
| **landscape_count** — *"the 10^500 framing is not inflated by gauge copies"* | **exact enumeration** | none | **nothing is owed** |
| **content** — orbit count against `b3` | **fit**, 2 parameters through 3 points | **1** | the per-interval factors |
| **accessibility** — sampler yield against `b3` | **fit**, 2 parameters through 3 points | **1** | the per-interval factors |

## What the audit found

**The refutation is arithmetic.** At `b3 = 6`, **531,440 of 531,441** flux pairs are primitive — the gauge quotient removes
**one**. There is nothing fitted, so **no two-sided score is owed and manufacturing one would be a ritual.**

**The content scaling is a description, not a law.** The per-interval factors are **1.0112 apart** — the fit did not consume
them, so the agreement is real evidence for an exponential form. **But the counts are exact integers: there is no noise for a
1% residual to hide in.** *"A power law that fits to about 1%"* is what the data support; *"scales as `b3^2.15`"* is more
than they say.

**The accessibility fit does not hold its own intervals.** They disagree by a factor of **1.868 per unit `b3`** — and
**R² 0.957 hides that entirely**, which is the whole reason the intervals are reported. **The module already says so**, which
means *this claim was two-sided before the bench existed.* **It is the best-behaved of the three and the one to copy.**

## What changes

**None of the verdicts.** The refutation stands on arithmetic; the content scaling was already labelled a fit.

**What changes is the status of the two exponentials**: one is a description at the 1% level **on exact data**, so **a fourth
`b3` point would test it and three cannot**; the other is **not an exponential at all**.

## The cheapest next test

**One more `b3` value for the content count.** Two parameters through three points **cannot fail a form**; four points can.
That is the same statement as *"a room with forty identified modes still needs the peaks it did not fit"*, one level up.

## The falsifier for this audit

> **If the fourth `b3` point lands on the exponential to within the same 1%, the exponential is established and this audit
> was a formality about degrees of freedom.** If it does not, the "two scales" comparison in `b3_scaling` loses one of its
> two scales, and the product `A*B` loses its meaning as well.
