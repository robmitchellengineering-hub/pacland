# The impostor count: the observables DO identify a vacuum — my first measurement of this was wrong

**Correction, 2026-11-02, same day as the first version.** The first version of this note reported that `(N, V, |DW|)` left
up to **43 vacua indistinguishable**, and drew the conclusion that the room's lesson transferred to the landscape. **That
number was an artefact of my own arithmetic, not a property of the physics.**

The binning used was `round(x, -int(round(log10(|x|) - log10(rel))))`. For a vacuum energy `V ~ 8.9e-19` with `rel = 1e-3`
that computes `digits = 15`, and **`round(8.9e-19, 15)` is `0.0`** — so every vacuum's `V` collapsed to zero and most
`|DW|` values did too. The classes were made of vacua that shared *nothing*, because two of the three numbers had been erased.

## The corrected measurement, 5,885 vacua, 14 corpora

Binning on the mantissa instead of the exponent, at **one significant figure** — the coarsest precision a measurement could
plausibly claim:

| corpus | vacua | distinct **flux** | distinct **(N, V, \|DW\|)** | worst class |
|---|---|---|---|---|
| h12_2_m1 | 500 | 500 | **500** | **1** |
| h12_2_m3 | 504 | 504 | 503 | **2** |
| h12_2_m5 | 500 | 500 | 499 | **2** |

**And against precision, over all corpora:**

| significant figures | identifiable | worst class |
|---|---|---|
| 0 | 0.960 | 5 |
| 1 | 0.997 | 2 |
| 2 | 0.999 | 2 |
| 3 | 1.000 | 1 |

## What this actually says

**The three scalars identify a vacuum almost always** — 99.7% at one significant figure, and **96% even at order-of-magnitude
precision.** The map from generator to observation is **nearly one-to-one**, not many-to-one.

**So the room's lesson does NOT transfer as I claimed it did.** There a spectrum that explained 100% of the peaks belonged to
a room 33.9% wrong, because many boxes share a footprint. **Here, three numbers out of five thousand label a vacuum. The
landscape is far more identifiable than a room's mode spectrum, not less.**

## What survives from the transfer, and what does not

**Survives**: the *method* — measure the degeneracy of the observable set before claiming an inversion is possible, and
check the claim against a system whose answer is known. **That is what caught this.**

**Does not survive**: the *conclusion*. The landscape's observables are strongly discriminating, so **an inversion from
observables to vacuum is not blocked by ambiguity** — the h12 wall is a computational problem, not an information problem.

## The falsifier this note failed, and how

The first version carried this falsifier: *"if every observable signature is unique, then the observables DO determine the
vacuum, the room's lesson does not transfer, and this note is wrong about the landscape."*

**That is precisely what the corrected run found, and the falsifier fired.** The note is kept with the correction rather than
deleted, because the failure is the useful part: **a binning bug produced a headline number, and the falsifier written
beforehand is what exposed it.**
