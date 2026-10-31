# One command, one room — `rf_plan.py`

The deliverable the whole engine exists for. A wireless engineer runs **one command** on a confined space and
gets the mode structure, the stream count with its spread, the placement levers, the chamber question and the
thermal ceiling — **each carrying its PASS mark and the check that could falsify it.**

```
python3 scripts/rf_plan.py --room 3,4,2.5 --band 5.18 --antennas 4 --snr 20
```

Output for a 3 × 4 × 2.5 m room at 5.18 GHz, 4 × 4, 20 dB:

| section | what it says | mark |
|---|---|---|
| **1 mode structure** | **1,296,344** modes below 5.18 GHz; Weyl **−0.096%**; **84.0%** exact degeneracies | **PASS-2** |
| **2 streams** | **4 of 4** as a perfect-polarisation **ceiling**; 3–4 across receiver heights; polarisation-corrected **3–4** | **PASS-2** |
| **3 placement levers** | receiver height is worth **up to one stream** | **PASS-2** |
| **4 chamber question** | LUF rule of thumb **112.4 MHz**, mode-density LUF **192.6 MHz** (**1.71×** the rule) | **PASS-2** |
| **5 thermal ceiling** | **1,910 samples/bit** at contrast 0.1, BER 1e-3 — a bound, not a prediction | **PASS-1** |

And the last block is the point of the whole thing:

```
WHAT WOULD FALSIFY THIS PLAN
   a measured 4x4 link at 20 dB giving FEWER than 2 streams -> the ceiling is wrong
   the same link giving MORE than 4 streams -> the model is pessimistic and polarisation is over-charged

   One measurement settles it. Anything above is a model until that measurement exists.
```

## The rule it follows

**Every number carries the measurement it depends on.** If a survey file is supplied
(`--survey survey.json`, produced by `rf_survey_from_iw.py`), the SNR is the **measured** one and the report says
so; without it, the assumption is printed as an assumption.

## What it refuses to do

- **quote the ceiling as a prediction.** Practice is 2–3 of 4 at 20 dB and the model says 4; the gap is
  **channel sounding**, not field, and the report says that rather than printing 4 and moving on.
- **hide a PASS-1.** The thermal bound is derived and unmeasured, and is marked as such in the output.

## A defect this command caught in itself

The first version printed **"1,910 samples/bit"** next to a meaningless formula — a **hardcoded number
presented as computed**. It now calls `thermal_capacity()` and prints what comes back. **A number that looks
computed and is typed is the defect this programme exists to catch**, and it appeared in the very file meant to
demonstrate the discipline.

## Tests

Five: every section present, PASS marks present, a falsifier stated, an incomplete room refused, a negative
dimension refused.
