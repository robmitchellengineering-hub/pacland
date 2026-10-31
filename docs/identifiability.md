# Identifiability, PASS-2: how many modes are usable is a property of the space, not of Q

**Reproduce:** `python3 scripts/identifiability_pass2.py`

The registry held identifiability at **PASS-1** — one parameterisation (Q = 50, one space, −60 dB). This sweeps a
**factor of four in Q** and four spaces:

| space | modes below 1.571 GHz | Q = 25 | Q = 50 | Q = 100 |
|---|---|---|---|---|
| 0.50 m cube | 147 | **11** | **11** | **11** |
| 1.00 m cube | 1,185 | 16 | 16 | 16 |
| 2.00 m cube | 9,594 | 16 | 16 | 16 |
| 3 × 4 × 2.5 m | 36,096 | **17** | **17** | **17** |

**The usable count moves by exactly ×1.00 across a factor of four in Q, in every space.** The falsifier — a
factor-of-two change means it is not a room property — did not fire.

**So: PASS-2.** How many modal directions survive at −60 dB is set by the **space and the noise floor**, not by the
damping you assume.

## The second finding, which is the interesting one

**The count saturates at 16–17 while the mode count grows by 245×** (147 → 36,096). A larger room has far more
modes and **almost the same number of usable directions**:

| modes | usable |
|---|---|
| 147 | 11 |
| 1,185 | 16 |
| 9,594 | 16 |
| 36,096 | 17 |

**More modes is not more information.** Past about a metre, extra modes arrive as near-degenerate clusters that a
−60 dB measurement cannot separate — which is exactly the degeneracy finding from the acoustic work, showing up as
a saturation here.

**This is the sentence a customer needs and no heat map says:** *making the room bigger stops helping, and the
ceiling is about 16 directions at −60 dB with three probes.*

## What it does not say

- **Three probes, −60 dB.** More probes or a quieter floor raise the ceiling; the sweep fixes both.
- **`usable_10pct`** — the criterion is a 10% bound on the recovered parameters, and that criterion is named rather
  than assumed.
- **Empty rectangular spaces.** Furniture adds scattering paths, which can add directions the free-space field does
  not have.

**Falsifier for the promotion:** a second measurement at a different probe count or noise floor that moves the count
by more than a factor of two reopens this as PASS-1.
