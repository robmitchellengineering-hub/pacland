# The survey instrument you already own

An access point measures almost everything the survey needs. **No extra hardware.**

| what the survey needs | where the AP reports it |
|---|---|
| **noise floor** | `iw dev wlan0 survey dump` → `noise` in dBm, per frequency |
| **occupancy** | same command → `channel busy time` / `channel active time` |
| **streams actually in use** | `iw dev wlan0 station dump` → `tx bitrate` / MCS, which encodes the NSS |
| **radio capability** | `iw list` |

```
iw dev wlan0 survey dump   > survey.txt
iw dev wlan0 station dump  > stations.txt
python3 scripts/rf_survey_from_iw.py survey.txt stations.txt
```

Output: per-channel occupancy and noise, the quietest and busiest channel, and the station table.

## What this is actually good for — the real test

**`station dump` tells you how many spatial streams the link negotiated.** That is the number the engine
predicts. So a mesh of a few APs is a **real test of the engine, tonight, with nothing bought**:

1. put a client at several positions in a room;
2. log the NSS at each;
3. log the room's dimensions, band and channel;
4. run the engine at the same geometry.

**If the engine predicts the observed NSS ordering across positions, the model has passed a real test.** If it
doesn't, the Q or the geometry is wrong and we know where to look.

## The caveat that decides how to read it

**The AP reports the NSS it *negotiated*, capped by the client's radio as well as by the channel.** A 2 × 2
client shows 2 streams in a room that could carry 4.

**So compare stream counts *within one client* across positions — never across clients, never against the engine
as an absolute.** The engine predicts the room's ceiling; the client shows you where on that ceiling it landed.

## Two things the AP cannot give, and what to do instead

1. **The impulse response** (→ T₆₀ → Q). Most APs don't expose CSI. Substitutes, in order of cost:
   - **estimate Q from the measured channel frequency response** across the 80 MHz band if the driver exposes
     per-subcarrier data (some chipsets do, via `ath9k`/`ath10k` CSI tooling);
   - **run the engine at a range of Q** and report the stream count *as a function of Q* — which is honest and
     still useful, because an installer can compare the room's behaviour across positions without knowing Q;
   - a VNA sweep, if one is ever available.
2. **A true channel matrix.** Without CSI, the stream count is inferred from NSS, not computed from `H`.

## Why the AP route is the right first survey

It costs nothing, it runs on hardware already installed, and **it produces the one number that can falsify the
engine today** — the observed stream count at known positions. Everything else in the survey (the impulse
response) refines the model; this tests it.
