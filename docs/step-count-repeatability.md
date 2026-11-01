# The pedometer's own repeatability — and why it bounds the map

**Data:** `runs/phone/calib-1793491916406-27steps` (2026-11-01T00:11:56Z) and `runs/phone/walk-1793491548547-hallway_walk_2_0`

Two measurements of the same corridor, by the same app, on the same phone:

| measurement | distance | counts | counts per metre |
|---|---|---|---|
| **calibration** (known 10 m) | 10 m | **27** | **2.70** |
| **hallway walk** (10 m out and back) | 20 m | **44** | **2.20** |

**A 23% difference in counts per metre between two walks of the same corridor.**

## What that means, and why it is the important number

The calibrated stride (**0.370 m per count**) makes distance correct *for a walk whose cadence matches the
calibration*. On the other walk the same stride gives **27 × 0.370 = 10.0 m for the 10 m leg**, but the walk actually
produced 22 counts per 10 m, so applying that stride there gives **8.1 m** — a **19% distance error**, with no heading
error at all.

**So the map's accuracy is bounded by step counting, not only by heading**, and the bound is about **±20%** until the
detector is more consistent.

## Why the counts vary, stated as a hypothesis rather than a finding

`counts per metre` of 2.2–2.7 with a stride in the region of 0.6–0.7 m implies **roughly two counts per stride** — that
is, the detector is counting **every footfall rather than every stride**, and at some speeds it may be catching both
the heel strike and the toe-off of the same foot.

**The calibration absorbs the average of that**, which is why the distance comes out right on average. **It cannot
absorb the variation**, which is what this note measures.

## What would fix it

1. **a longer calibration** — 30 m rather than 10 m, so one missed step is 3% rather than 10%;
2. **two calibrations at different speeds** — a slow walk and a normal walk, to see whether the count per metre is
   speed-dependent (it will be);
3. **a stride model** rather than a constant: `stride = a + b · cadence`, fitted from three known distances.

**Falsifier for this note:** if a 30 m calibration and a 10 m calibration of the same corridor agree within 3% in
counts per metre, then the variation above was the short baseline and not the detector, and this note is wrong.
