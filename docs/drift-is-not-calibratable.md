# The loop cannot be closed by a drift model — measured, not assumed

**Question:** can the walk's drift be corrected well enough to give a map without an external frame?

**Answer: no.** Three tests, in increasing order of how decisively they fail.

## 1. A distance-proportional bend (yaw bias per metre)

Fitting a yaw bias and a scale per loop drives both parameters **to the edges of the search range** and still leaves
5–70% open. **No interior solution.**

## 2. A constant yaw rate (gyro bias) plus a scale

A better model: a real gyro bias is per *second*, not per metre. Fitted over ω ∈ ±2 °/s and scale 0.85–1.15:

| | before | after |
|---|---|---|
| median closure | **17.6%** | **6.8%** |

**It looks like progress, and it is not.** Every walk's scale ran to the 0.85 bound and half the yaw rates ran to
±2.0 °/s — the fit is absorbing error through its bounds rather than finding a parameter.

## 3. The decisive test: is the fix unique?

If a corrected path closes for **one** (ω, scale) pair and not for its neighbours, the fit has identified something.
So the whole grid was tested for closure under 2 m:

| walk | fraction of a 4,961-point grid that closes to <2 m |
|---|---|
| bedroom next to router | **0.0%** |
| bedroom full house | **3.2%** |
| hallway walk 2 | **0.0%** |
| full house walk | **0.0%** |
| full house walk again | **0.0%** |
| whole house last time | **0.0%** |
| look another whole house (×2) | **0.0%** |

**Seven of eight loops cannot be closed to 2 m at all by any constant yaw rate and scale in the range.**

## What this settles

- **The 6.8% median is the optimiser working, not the model fitting.** With two free parameters and one constraint,
  closure can be bent toward; it cannot be *found*.
- **The drift is not a constant**, so it cannot be calibrated from these walks.
- **A frame has to come from outside the walk** — a sketch, a plan, a photo-derived layout, or LiDAR.

**This is the difference between a disappointing result and a useful one:** the question "can we avoid the atlas?" has
now been asked properly, and the answer is no. That closes a route instead of leaving it open to be re-tried.
