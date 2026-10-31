# The measurement that settles the plan — and the harness ready for it

**Reproduce:** `python3 scripts/validate_streams.py --room 3,4,2.5 --band 5.18 --ap 1.5,2.0,2.4 positions.csv`

The plan predicts a **ceiling**. This is the tool that takes real stream counts and says whether the ceiling
survived. It exists now so that the moment there is data, the test is one command.

## The data it wants

```
x,y,z,nss,snr_db
0.5,1.2,0.9,3,20.0
2.6,3.4,0.9,2,18.5
```

One row per position: where the client was, **the number of spatial streams the link actually agreed**, and the
SNR the AP reported.

## The falsifier, stated before any data exists

| outcome | reading |
|---|---|
| **any measurement exceeds the ceiling** | **FALSIFIED** — the ceiling is not a ceiling, and the model is wrong on the low side |
| **mean shortfall ≥ 2 streams** | **FALSIFIED** — the ceiling is too high; polarisation or sounding must be re-examined |
| otherwise | **CONSISTENT** — no measurement beat the ceiling and the shortfall is inside the documented channel-sounding gap |

**And a note on what "consistent" can mean:** hardware agreeing *fewer* streams than the ceiling is the expected,
documented behaviour. So this test checks the **order and the bound**, not the absolute value — and it says so in
its own output rather than letting a reader over-read it.

## The defect this harness caught in itself

The first version modelled **one antenna at each end** and therefore predicted **1 stream for every row**. A 1 × 1
link cannot carry more than one stream — the harness was comparing MIMO measurements against a non-MIMO model.
Both ends are now arrays at **half-wavelength spacing**, which is what a real AP and client present.

**It would have reported "CONSISTENT" on nonsense.** That is the failure mode this programme keeps meeting: a
check that cannot fail in the way you fear.

## Self-tests

Four, and two of them prove it can **fail**: a measurement beating the ceiling must report FALSIFIED, hardware
two or more streams below must report FALSIFIED, a small shortfall must report CONSISTENT, and an empty table must
be refused.
