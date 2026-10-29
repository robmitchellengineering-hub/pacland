# The audio analysis — in plain English

What it does, what already works, and what it will let us do. The detailed maths is in
[identifiability-of-room-modes.md](identifiability-of-room-modes.md); the programme plan is AirMatrix's
`PLANS/PLAN-airmatrix-audio-lab.md`; the code is `src/pacland/spectral/` here and `rob-meter` / `rob-dsp`
in the AirMatrix repo.

## In one sentence

It turns a PA system into an **audio lab that can certify what it measured** — and, before any of that, it
answers the question every room-correction product skips: *how much of a room can this microphone setup
actually know?*

## What already works — measured, not planned

These are in the tree and verified with figures, not promises:

| capability | verified |
|---|---|
| loudness (K-weighted, M/S/I, LRA, true peak) | EBU Tech 3341 to **0.1 LU**, 3342 to **1 LU** |
| levels — sample peak/hold, PPM (DIN/Nordic/BBC/EBU), VU | PPM burst to **0.05 dB**; VU 300 ms / 1.5% overshoot |
| spectrum — FFT analyser, 1/3-octave RTA, spectrogram | pink flat to **1.5 dB**, 25 Hz–16 kHz |
| transfer function + **coherence** + delay finder | +6 dB peak to **0.3 dB**, coherence > 0.95; sub-sample delay |
| 31-band graphic EQ, master bus | exact at band centres — **12.00 dB for a 12 dB request**; transparent at rest |
| parametric EQ (per-band Q, frequency, gain) | `Eq::magnitude(hz)` exposes the realised curve |

So the measuring instruments are real. What is **not** present yet: a stimulus generator, room acoustics
(RT60/EDT/C50/C80/STIPA), modal analysis, a battery orchestrator, the per-venue certificate, and a
correction engine that targets *modes* rather than *bands*.

## The finding that shapes the whole design

**A 1/3-octave graphic EQ is the wrong instrument for correcting a room.** A 12 dB cut at 63 Hz at the
graphic's Q of 4.32 spills **9.29 dB into the neighbouring third-octave**. Narrow it and the spill falls
(0.68 dB at Q = 10, 0.18 dB at Q = 20) — but a graphic EQ cannot place a narrow notch at a mode.

That single number decides the architecture: room correction is **parametric notches at identified modal
frequencies with fitted Q**, plus a shallow shape for the broad tilt. And the parametric band is already
in the tree — it was always there; nobody had measured that the graphic could not do the job.

## What the analysis adds — three questions, and the honesty in each

**1. How many microphones do you need?** Answered by nudging each unknown in the room model and counting
which directions the measurements actually move.

| stage | answer | what it means |
|---|---|---|
| what is visible at all | one microphone separates every resonance in the 1-D case | true, and *false to publish alone* |
| how well separated | one omni leaves **six** directions ten orders below the rest — noise, not information | **two** is the real minimum |
| at real noise | at **−60 dB**, about **3 of 36** parameters to 10%; at **−50 dB**, none | the honest number |

Publishing the first line alone would have been a confident false claim. The useful statement is:
*at normal measurement noise you can reliably measure a handful of combinations, not a table of every
resonance* — which is exactly what an equaliser and an anti-feedback system need, and not what a
"here are your 36 resonances" readout needs.

**2. Is the room solver right?** A room's resonances have a spacing signature. A plain box produces
clustering modes (Poisson); an irregular room produces repelling ones (the same signature the Riemann
zeros have). Both are known in advance from the room's shape, so a solver can be checked **without knowing
the answer** — and there is also a Weyl count check for the number of modes, measured to **0.02%** on
analytic boxes. Nobody else applies this to room solvers.

**3. What should the corrector actually do?** Target the modes that were identified, minimise the **worst
seat** rather than the average curve, and always report per seat. On a synthetic room the target is a
**≥ 6 dB** reduction in worst-seat ripple with no band boosted beyond +6 dB; on a real room, the report
names every mode it did **not** fix, and why.

## The binaural node — three jobs, and which are measured

The capture hardware is a **binaural node**: two capsules 17 cm apart, stereo in, on batteries, over
Wi-Fi. Not a microphone — a sensor with two correlated channels, with three planned jobs:

1. **Walking capture.** The engineer walks and presses; the desk already has the remote. **Measured:** one
   binaural position does the work of *two* omni positions, so a four-position route can be two — and the
   system can say "you have enough", and which directions are still weak.
2. **A stationary pair at front of house** — a calibrated, always-on reference channel. *Designed, not
   measured.*
3. **The stage mics as the measurement array.** Every stage mic is a receiver and the desk knows what it
   is sending, so **the show itself is the stimulus** — no sweeps, no stopping the gig. *Designed, not
   measured*, with a named risk: the sends are not a known stimulus unless logged, and parameters change
   during a show.

The node is **not** "a machine that tunes the room". The engineer stays the sensor; the system is the
recorder and auditor. At the end the route *is* the report.

## The suite, in phases — each with its own pass mark

| phase | produces | pass mark |
|---|---|---|
| **1 · measurement spine** | stimulus + deconvolution to an impulse response, coherence per mic, validity gating | loopback flat **±0.25 dB** 20 Hz–20 kHz, delay to **1 sample**; a capture with a dropout is **refused**, not averaged |
| **2 · room acoustics** | RT60/EDT/T20/T30, C50/C80, noise floor, STIPA | RT60 within **5%** of a synthetic decay; C50/C80 within **0.5 dB** of a two-path model |
| **3 · modal analysis + correction** | mode identification, Weyl and spacing checks, the notch corrector | **≥ 6 dB** worst-seat ripple reduction, no boost beyond +6 dB, every unfixed mode named |
| **4 · the lab product** | one command per venue → a **certificate** (gate, result, evidence, producer, falsifier, remedy) with a manifest hash | a third party can verify the file |
| **5 · the claim** | "the world's best audio lab" — only after 1–4, defined by evidence, not by adjective | the evidence page is linked |

## What it lets us do

- **Certify instead of assert.** Every venue visit produces a file with the falsifier and the remedy in it,
  checkable by someone who does not trust us.
- **Compare venues as numbers.** Same fields everywhere, so "this room is worse than that one" stops being
  an opinion.
- **Size hardware honestly.** Two capsules or two positions, not five.
- **Make claims that survive a hostile engineer.** Margin and correction, not a modal table.
- **Reuse the method.** The same rank/noise/spacing tests answer the same question for speaker placement,
  venue tuning, and any "how much can my sensors know" problem — that is the asset, not the room.

## What would make this wrong

- The modal model is **linear and low-frequency** — it does not describe a room above a few hundred Hz, and
  it says nothing about loudspeaker nonlinearity.
- It says what is **identifiable**, not what is **audible**. Those are different questions.
- Every number moves with the **noise assumption**, which is why the noise figure is printed beside it.
- The stage-mic array assumes a logged stimulus; if the desk's sends are not recorded, the show is not a
  measurement.

## How to check us

The 1-D case has an **exact analytic answer** — modes at known pitches, shapes in closed form — so no
solver has to be trusted. The 3-D case is a real 6 × 4.5 × 3 m room with the modes below 100 Hz computed
and cross-checked. The instrument figures above come from the AirMatrix tree's own tests. The reasoning,
including the stage where the headline had to be corrected, is in
[identifiability-of-room-modes.md](identifiability-of-room-modes.md).
