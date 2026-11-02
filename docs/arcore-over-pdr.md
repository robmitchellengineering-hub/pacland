# The metre is ARCore. Step counting is not a measurement.

**Rob, 2026-11-02:** *"I think arcore for walls is better the step count and meters seems to always be off."* **He is right,
and the data says so more bluntly than the feeling does.**

## The two instruments, measured against things that are true

| what was checked | step counting (PDR) | ARCore |
|---|---|---|
| **a 30 m calibration, walked three times** | **92, 92, 62 counts** — a **33% spread** between two walks of the same distance | — |
| **the implied stride** | **0.326 m** and **0.484 m** from the same body — a 48% disagreement | — |
| **a loop that returns to its start** | closes to **9–25% of path length**, median **17.6%** | — |
| **two walls of one room, measured separately** | — | **6.05 and 6.05 m** — agree to **1 cm** |
| **the same ceiling in three rooms** | — | **2.65, 2.47, 2.62 m** — a **±9 cm** instrument (Rob: every ceiling here is the same height) |
| **a diagonal against two walls** | — | the 5.98 m reading was rejected as **longer than the room can be** |

**Step counting's error is 17–48%; ARCore's is 1–9 cm.** They are not the same kind of number, and this programme's own
rule applies: *a claim that cannot be reproduced is not a measurement.*

## The decision

1. **ARCore is the instrument for anything measured in metres** — walls, ceilings, room dimensions, device positions.
2. **Step counting is demoted to a motion detector.** It can say *the phone moved*; it cannot say *how far*.
3. **No product claim, no layout number and no certificate may be derived from step-derived distance.** Where a distance
   came from steps, the payload says so.
4. **The walks keep their real value**: the level profile along a route, the drift study that closed the door on PDR, and
   the diffuse-field measurement (std/mean 1.21 against Rayleigh's 1.00). **Those were measurements of the RADIO, not of
   the walking** — the step error did not touch them.

## Where step counting survives, and why

**The homing meter** uses metres walked as the **x-axis of a gradient**. There, a uniform scale error cancels: if every
step is 30% too long, the slope is 30% too small, and **the sign — which is what the arrow shows — is unchanged.** The
magnitude is labelled as an estimate.

**That is the whole rule**: steps are acceptable where only the *direction* of a change survives a scale error, and
nowhere else.

## What this changes

- the layout template's `w`/`h` come from ARCore measurements, with the measurement's provenance recorded;
- the walk payload now carries `distance_source: "steps"`, so nothing downstream can mistake it for a metre;
- the ±9 cm ceiling figure is the error bar for every vertical claim;
- **a room measured with ARCore needs one scan session**, because ARCore's coordinates are per session — the same reason
  two sessions' lengths cannot be combined.

## The falsifier for this decision

> **If an ARCore room dimension is ever contradicted by a tape measure by more than 10 cm, this decision is wrong and
> step counting deserves a second look.** Until then, the tape is the one thing that could overturn it, and it has not
> been applied.
