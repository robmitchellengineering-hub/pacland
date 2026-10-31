# The plan meets the link — one command, and it says whether the measurement can prove anything

**Reproduce:** `python3 scripts/rf_plan.py --room 4,5,2.4 --antennas 2 --iw-link iw-link.txt`

A capture of `iw dev <if> link` is now an input. The plan reads the **measured** band, the **measured** stream
count (from the MCS index, not a bitrate), and prints them beside the modelled ceiling:

```
RF PLAN   4.0 x 5.0 x 2.4 m   2.46 GHz   2 x 2 antennas   20.0 dB (assumed 20 dB)
...
6. MEASURED LINK (from `iw link`)                     measured, not modelled
   ssid Telstra3696   2.4 GHz   2462.0 MHz   -37.0 dBm
   streams in use            2 of at most 2   (from MCS 15)
   predicted ceiling         2-2 of 2
   -> consistent, but NOT DISCRIMINATING: a 2-element ceiling cannot be beaten by a
      2-stream observation, so this row confirms the toolchain and not the model.
```

## The sentence that matters

**"Consistent, but NOT DISCRIMINATING."** A 2 × 2 ceiling cannot be exceeded by a 2-stream observation, so the
comparison is **incapable of failing** — and the tool says so rather than printing "consistent" and letting a
reader hear "confirmed."

**A test that cannot fail is not evidence.** This programme has now caught four of those: a hardcoded thermal
number, a 1 × 1 validation harness, a substring match on `UNUSABLE`, and this one. The guard is to make the tool
**declare its own discrimination** before any verdict is read.

## What the plan now refuses to do

| behaviour | instead |
|---|---|
| keep the assumed 5.18 GHz when the link says 2462 MHz | the **measured band replaces the assumption** and the header shows it |
| print a falsifier asking for "fewer than 0 streams" | the bound is clamped to the real range, and the wording is generated from it |
| report "consistent" without qualification | says **NOT DISCRIMINATING** when the ceiling equals the observation |

## The two defects this caught in itself

1. **The header kept the assumed band** while the mode count used the measured one — the title said 5.18 GHz and the
   body computed 2.46 GHz. Two numbers from two sources, in one report.
2. **The falsifier read "fewer than 0 streams"** — arithmetic on a ceiling of 2 with a `lo - 1` clamp. A generated
   sentence with a nonsense number in it is the same defect class as a hardcoded one.

## Tests

Nine on this file now, four of them on the measured path: the band replaces the assumption, the streams come from
the MCS, the row declares itself non-discriminating, and **the falsifier never asks for a negative stream count**.
