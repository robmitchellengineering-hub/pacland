# The h12 wall's conditioning number — reproducing it, and the bug that stopped the first attempt

**The wall document's central number** (`docs/h12-25-sampling-wall.md`, measured 2026-10-21):

| h12 | `M` eig min | `M` eig max | **cond(M)** | \|dV\| after ISD+round |
|---|---|---|---|---|
| 2 | 7.4e-2 | 1.35e1 | **1.8e2** | 0.73 |
| 25 | 4.5e-4 | 2.20e3 | **4.8e6** | 669 |

and across h12: **2 / 5 / 10 / 15 / 20 / 25 → 1.8e2 / 1.1e10 / 2.9e6 / 7.5e7 / 7.3e8 / 4.8e6**, with h12=25 across `model_ID` 1–9
ranging **4.8e6 to 2.7e10**.

**Every "the wall is ill-conditioning" conclusion in that document rests on this one row of numbers.** The diagnostic's own
docstring says why it exists: *"there was no script in the repo that produced it, so the result could not be reproduced or
attacked."*

## Checked: no run on the hub produces those numbers

Searched `runs/pacland-rog/*`: the 2026-10-21 overnight run is the **sampling** run (0 critical points in 183+ batches) and
contains **no conditioning output at all**. **No job on the hub ever printed 1.8e2, 4.8e6 or any of the across-h12 row.** The
numbers exist only in the document.

## The bug that made the first reproduction attempt meaningless

**First attempt (job `2026-11-02T1619Z`)**: fed `committed_moduli(2)` — the first row of `data/h12_2_m1_stats.json` — and
measured:

```
degree 0..3:  dim 6   eig_min 9.415e-46   eig_max 1.323e+90   cond 1.405e+135
```

**cond(M) = 1.4e135** against the document's **1.8e2** — a hundred-and-thirty-three orders of magnitude apart.

**The cause is the moduli point, and it is visible in the number**: `committed_moduli` returned the first row whose `moduli`
had the right *length*, and that row carries values like **`-1.98e20 + 8.51e29 i`**. **A complex-structure modulus of a
Calabi–Yau at large volume is O(1)–O(100); 1e29 is a corrupt or unconverged row, not a point in moduli space.** Measuring a
matrix built there produces garbage — and, tellingly, **identical garbage at every degree**, which is what first showed the
"ladder" was not a ladder.

**Fixed**: `committed_moduli` now rejects any row outside `[1e-3, 1e3]` in `|z|`, prints the rejection with the magnitude that
caused it, and falls through to the sampler's own ISD initial guess.

## The reproduction, dispatched

**Job `2026-11-02T1919Z`** on `pacland-rog`: h12 = 2, 5, 10, 15, 20, 25, each with the model's own ISD initial guess, printing
`dim`, `eig_min`, `eig_max`, `cond(M)` and **the magnitude of the point used** — because the point is what broke the last
attempt and it must never be silent again.

### The decision rule, written before the numbers arrive

| what comes back | what it means |
|---|---|
| **h12=2 reads ≈1.8e2 and h12=25 ≈4.8e6** | the wall document is **reproduced** — the ill-conditioning is real, the h12≥5 wall is a numerics problem, and the fix is preconditioning or a better proposal |
| **h12=2 reads ≈1.8e2 but h12=25 does not read 4.8e6** | **half the document is right**; the across-h12 row is wrong and the wall's mechanism is not established |
| **h12=2 does not read 1.8e2** | the document's number was measured at a **different object** (different matrix, different moduli convention) and **no conclusion in the wall document is currently supported** |
| **the model fails to build at some h12** | the ladder stops there; report the last rung that built and say so |

## Why this is the honest next step for h12

**The wall document is the reason h12 ≥ 5 is considered blocked.** Every downstream decision — the hypothesis ladder, the
"truncation or hierarchy" question, the sampling strategy — rests on a number that **has no script, no run and no
reproduction**. Making it reproducible is worth more than adding another theory on top of it.
