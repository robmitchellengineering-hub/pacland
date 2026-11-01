# Which channel should the access point be on? — from the scans

**Reproduce:** `python3 scripts/channel_plan.py` · **Data:** 16 scans from the phone, **33 distinct networks**

The phone heard every BSS in range with its frequency and level. That is an interference census, and it answers a
question every installer guesses at.

## Method

For each candidate channel, **sum the received power of every other network whose spectrum overlaps it** (a ±10 MHz
adjacency allowance at 20 MHz), then compare that total with our own network's level.

**Only channels where something was actually observed are ranked.** A channel with no observation is reported as
**unverified**, not as clear — because the phone only hears what it hears, and "we saw nothing" is not "there is
nothing".

## The result

| band | our network | interference on it | quietest *observed* channel | margin |
|---|---|---|---|---|
| **2.4 GHz** | ch 11 at **−33 dBm** | **−57 dB** | **ch 1** (−74 dB) | **24 dB** |
| **5 GHz** | ch 36 at **−28 dBm** | **−61 dB** | **ch 44** (−89 dB) | **31 dB** |

**2.4 GHz channel 11 is the busiest channel in the neighbourhood**: it carries our AP at −33, **AustralCafe at −55,
two hidden networks at −55**, The Foundry at −70 and Telstra2CD5 at −80. Channel 1 carries six networks, **all of them
between −81 and −87** — 24 dB below our own signal, i.e. nothing.

**5 GHz channel 36** has the same story: ours at −28, with AustralCafe at −59 and two hidden networks at −67. **Channel
44 has one network at −89.**

## Why 24 dB is a real recommendation and 3 dB would not be

**The same instrument measured 16 dB of fading at a fixed spot** (`docs/fading-is-rayleigh.md`). The tool enforces that:
**a recommendation under 6 dB is reported as "not a finding"**, because it is inside the measurement's own noise.

**24 dB and 31 dB are both well outside it.** These are the first *actionable* RF conclusions in this project that do
not depend on a floor plan.

## What this is and is not

- **is**: an interference census taken from 16 walks around the house, converted into a channel recommendation with a
  stated margin and a stated noise floor.
- **is not**: a site survey. A proper one averages over time and position; this is 16 snapshots taken while walking.
  **The recommendation should be re-taken at the spot where the AP will live**, and it would be better taken twice a
  day apart, because occupancy changes.

**Falsifier:** if a Wi-Fi analyser at the AP's own position shows the ch-11 neighbours more than 10 dB weaker than
these scans suggest, the aggregation is over-counting (it takes the strongest sighting from anywhere in the house).
