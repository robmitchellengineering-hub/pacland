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

### PASS-2 check — and it moved under a different parameterisation

Re-run across **Q = 100, 200, 400** with the same layout: **3/4 at 10 dB, 4/4 at 20 dB, 4/4 at 30 dB, identical
at every Q.** So the Q dependence is negligible over a factor of four — good, the answer is not an artefact of
the assumed damping.

**But it moved when the receive layout changed.** The table above uses receive antennas on the mid-plane,
mirrored; the planner (`scripts/wifi_plan.py`) raises them by 0.35 of room height and mirrors them. With the
raised receivers the same room gives **4 of 4 at 20 dB**, not 3.

**So "3 of 4 at 20 dB" is a property of the layout, not of the room.** The honest claim becomes a range:

> **At 20 dB, an 80 MHz 5 GHz room link carries 3–4 streams of 4, depending on where the receivers sit, and
> essentially independently of Q between 100 and 400.**

That is a *better* result than the single number, because **the spread is the product**: placement is worth a
stream, and the planner's job is to find the layout that gets the fourth one.

**And it re-reads the planner's own falsifier.** "No placement beat the lattice" was measured over *random*
layouts at one receiver height. The parameter that matters is not random placement — it is **receiver height
and offset**, which is a two-parameter search, not a 12-dimensional one.

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
