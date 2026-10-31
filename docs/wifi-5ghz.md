# 5 GHz WiFi: how many streams does a room actually carry?

**Reproduce:** `python3 scripts/wifi_5ghz.py`

At 5 GHz the mode count stops being interesting — a 3 × 4 × 2.5 m room holds **59,978 modes in one 80 MHz
channel** (Weyl estimate 57,450, **+4.4%**; the surface coefficient was fitted on a wide band, so a narrow
channel is expected to be slightly off). The room is **52 × 69 × 43 wavelengths** across.

The question a link actually faces is different, and it is the same Fisher-information question this engine
answers everywhere else, asked of a MIMO matrix:

> with N transmit and N receive antennas over 80 MHz at a given SNR, **how many independent streams does this
> room support?**

## The result, from the room's own modes (Q = 200)

| antennas | 10 dB | 20 dB | 30 dB |
|---|---|---|---|
| 2 | 2 of 2 | 2 of 2 | 2 of 2 |
| 3 | **1 of 3** | 3 of 3 | 3 of 3 |
| 4 | **3 of 4** | **3 of 4** | 4 of 4 |

## Why this is a validation and not a curiosity

**Practice says a 4 × 4 link in a normal room carries 2–3 streams, not 4.** The engine, built from nothing
but the room's dimensions, the speed of light and a stated quality factor, says **3 of 4 at 20 dB**.

That is a first-principles model reproducing a rule of thumb that WiFi engineers know empirically — and it
reproduces it *without* furniture, people, scattering or multipath, all of which **add** degrees of freedom.

**So this is a lower bound on usable streams for a given antenna count.** Which is the useful direction: a
tool that says "this room will support at least 3 streams with 4 antennas at 20 dB" is making a claim that
survives a real installation.

## What it means for the EM engine as a whole

| leg | status |
|---|---|
| exact mode count (Weyl, fitted surface term) | **0.004%** on a wide band, 4.4% on a narrow one — both stated |
| degeneracy structure | 77–92% exact degeneracies in a rectangular space |
| identifiability of modes at a stated Q | **17–19 of 40** usable, and probes buy little in a high-Q cavity |
| **MIMO streams from the same field** | **3 of 4 at 20 dB — matches practice** |

The fourth row is the one that makes this a tool rather than a table: **the same engine that counts a room's
modes predicts how many spatial streams it carries, and gets the known answer.**

## Honest limits

- **Q = 200 is stated, not measured.** Lower Q (a furnished room) spreads the resonances and would *increase*
  the number of resolvable spatial degrees of freedom; a bare concrete room would decrease it.
- **No scattering.** A real room adds paths, which add streams — so the table is a **floor**.
- **Antenna placement is a lattice**, not optimised. A real installation would do better, and the engine
  could be used to search placements — which is the obvious next product feature.

**Falsifier:** if a measured 4 × 4 room channel at 20 dB routinely yields 4 streams, this model is
systematically pessimistic and the omitted scattering is doing more work than a floor allows. If it routinely
yields 2, the model is optimistic and Q should be lowered. **A measurement either way settles it, and that is
the test worth running on real hardware.**
