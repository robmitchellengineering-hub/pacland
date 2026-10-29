# Room correction from the mode spectrum: diagnose, fix, and check the fix away from the seat

AirMatrix models rooms. This turns the spectral work into something it can *act* on, in three steps
that each have to survive a check:

1. **Diagnose** — is the solver right? Weyl's law is an oracle that needs no measurement.
2. **Fix** — derive a bounded corrective EQ from the modal response.
3. **Check the fix away from the tuning point** — the test that separates a demo from a solution.

## 1. The diagnosis: Weyl's law with the surface term

A rigid rectangular room's modes are `f = (c/2) sqrt((nx/lx)² + (ny/ly)² + (nz/lz)²)`, and the
integrated count must follow

    N(f) = 4 pi V f³ / (3 c³)  +  pi A f² / (4 c²)

| box (m) | modes ≤ 500 Hz | ≤ 1 kHz | ≤ 2 kHz | error at 2 kHz |
|---|---|---|---|---|
| 6.0 × 4.5 × 3.0 | 1,259 | 9,208 | 70,371 | **−0.02%** |
| 5.0 × 5.0 × 2.5 | 994 | 7,188 | 54,563 | **−0.02%** |
| 8.0 × 3.0 × 2.8 | 1,058 | 7,723 | 58,735 | **+0.01%** |

The volume term alone is 4.6% high at 2 kHz; the surface term is what closes it. **A solver whose
count drifts from this has a bug, and no reference measurement is needed to say so.**

## 2. The fix: a bounded inverse

Each mode contributes at a seat weighted by its shape, `psi_n = cos(nx pi x/lx) cos(...)  cos(...)`.
Sum the resonances, smooth to a third of an octave, invert towards the band mean, and **bound the
gains** at +12 / −18 dB. The bound is the honest part: an unbounded inverse always "works" on paper
and eats all the headroom.

## 3. The check that matters: does the fix travel?

One correction derived at the **listener**, then applied everywhere:

| seat | ripple before | after 1-point EQ | after multi-point EQ | Δ 1-point | Δ multi |
|---|---|---|---|---|---|
| (2.0, 1.5, 1.2) — tuned | 12.8 dB | 2.7 dB | 9.0 dB | **−10.1** | −3.9 |
| (1.0, 3.0, 2.0) | 21.8 dB | 15.2 dB | 13.2 dB | −6.6 | −8.6 |
| (3.0, 2.2, 1.6) | 18.7 dB | 18.1 dB | 12.1 dB | **−0.6** | −6.6 |
| (4.5, 1.0, 0.9) | 37.0 dB | 28.6 dB | 21.2 dB | −8.4 | **−15.8** |

**Tuning at one seat is a local fix.** It buys 10.1 dB at the microphone and **0.6 dB two metres
away**. Averaging several seats before inverting buys less at the sweet spot (−3.9 dB) and **more
everywhere else** (up to −15.8 dB).

That difference — *the seat* vs *the room* — is the whole product question for a live PA, and it is
measurable before anyone plugs anything in.

## What this is not

- A box is not a real room: real rooms have non-rigid walls, absorption, furniture, and an audience
  that changes the damping. The numbers here are the **idealised** correction, not a prediction of a
  specific venue.
- The correction is **minimum-phase EQ**, which is what a PA processor can do. It cannot fix a null
  that comes from a reflection (you cannot fill a null with EQ without destroying headroom) — the fix
  for those is placement and delay, not gain.

## Reproduce

```
python3 scripts/spectral_rooms.py
```

Tests: `tests/test_spectral_rooms.py` — Weyl's law for three boxes, the correction bounds, and the
seat-specificity of single-point EQ (a test that would fail if the fix silently became global).
