# How many microphones identify how many modes?

The question the audio lab's correction engine depends on, and one nobody publishes an answer to.
Answered the way we answered Smets–Wouters: by the **rank of the Jacobian** of what is observed with
respect to what is fitted.

- **Observed:** `|p_s(f)|` — the magnitude response at *N* seats and *F* frequencies. That is what a
  microphone gives you.
- **Fitted:** per mode, `{f_n, γ_n, A_n}` (frequency, damping, amplitude), or `{γ_n, A_n}` when the
  geometry already fixes the mode frequencies.
- **Testbed:** a 1-D rigid tube (modes at `nπc/L`, shapes `cos(nπx/L)`) — analytic, so the truth is
  known exactly and no solver has to be trusted.

## The answer

| microphones | geometry unknown (15 params, 5 modes) | geometry known (10 params) |
|---|---|---|
| **1** | **rank 6 / 15 (40%)** | **rank 4 / 10 (40%)** |
| 2 | **15 / 15** — saturated | **10 / 10** — saturated |
| 3, 4, 5, 6, 8 | 15 / 15 | 10 / 10 |

**Two microphones identify the entire modal set of a 1-D room. One microphone identifies about 40% of
it.** More than two adds nothing, in this geometry.

That is a concrete, useful, checkable answer — and it is not the answer anyone would have guessed from
practice, where five-mic arrays are sold for room correction.

## And in a real room: 3-D, because a tube is not a room

Rob: *"does a 1d room exist, no, can we do it in a 3d room please."* Correct — so the same test, on a
6 × 4.5 × 3 m room, 18 modes below 100 Hz, 36 parameters (damping and amplitude per mode; the geometry
fixes the frequencies):

| microphones | rank | directions above a 60 dB floor | weakest direction |
|---|---|---|---|
| **1** | 36 / 36 | **30 / 36** | 4.3e-11 |
| **2** | 36 / 36 | **36 / 36** | 3.5e-2 |
| 3 | 36 / 36 | 36 / 36 | 4.9e-2 |
| 4 | 36 / 36 | 36 / 36 | 6.2e-2 |
| 8 | 36 / 36 | 36 / 36 | 6.7e-2 |

**Two microphones condition the whole modal set of a room below 100 Hz; one leaves six directions
effectively unidentified** (they sit 10 orders of magnitude below the first, which is noise, not
information). The third and fourth mic buy margin — the weakest direction improves by ~5 dB — not new
parameters.

Note how different this is from the naive answer. **Rank says one microphone identifies everything.**
Conditioning says one microphone is ten parameters short of usable. Rank is a yes/no answer to a
question that is quantitative, and quoting rank alone would have been a confident, wrong claim.

## A binaural pair, 17 cm apart — the rig Rob described

> *"a binaural 17cm rig that gets walked around for capture — a wireless node on batteries, stereo in,
> sent over the wifi."*

The maths on that rig, using the same 3-D room:

| positions | omni mic — usable directions | binaural pair — usable directions | weakest omni | weakest pair |
|---|---|---|---|---|
| **1** | **30 / 36** | **36 / 36** | 4.3e-11 | **5.9e-3** |
| 2 | 36 / 36 | 36 / 36 | 3.5e-2 | 4.0e-2 |
| 3 | 36 / 36 | 36 / 36 | 4.9e-2 | 5.0e-2 |
| 4 | 36 / 36 | 36 / 36 | 6.2e-2 | 6.4e-2 |

**One binaural position does what two omni positions do.** A single omni capture leaves six directions
buried; a single head-spaced pair conditions all 36. Beyond one position the pair adds margin, not
parameters.

So the rig is justified by measurement, and it makes the walk **cheaper**: roughly half the positions for
the same conditioning. The honest limit is that the advantage is specifically at one position — if you
are already walking to three positions, the second capsule is buying robustness, not information.

## With a noise model, the answer changes — and it is the honest one

Rank and conditioning have no noise in them. A real capture does, and the right instrument for that is
the **Cramér–Rao bound**: given the measurement noise, how precisely can each modal parameter possibly be
estimated? Parameters are counted as usable when the bound is below 10% of their own value.

3-D room, 18 modes below 100 Hz, 36 parameters, 60 frequencies per capture, **complex** data:

| noise (SNR) | usable at 10% | usable at 25% | median bound |
|---|---|---|---|
| 1e-4 (−80 dB) | **23 / 36** | 30 / 36 | 0.05 |
| 3e-4 (−70 dB) | 13 / 36 | 22 / 36 | 0.16 |
| 1e-3 (−60 dB) | 3 / 36 | 10 / 36 | 0.53 |
| 3e-3 (−50 dB) | **0 / 36** | 2 / 36 | 1.60 |

And the microphone count, at −60 dB with complex data:

| microphones | usable at 10% | usable at 25% | median bound |
|---|---|---|---|
| 1 | 1 / 36 | 6 / 36 | 1.86 |
| 2 | 2 / 36 | 8 / 36 | 0.69 |
| 3 | 3 / 36 | 10 / 36 | 0.53 |
| 4 | 4 / 36 | 11 / 36 | 0.48 |

**So the earlier headline needs a correction, and this is it.** Rank said one capture identifies
everything and conditioning said two were enough; with a noise model, **identifying 36 modal parameters
to 10% needs roughly −70 dB of measurement noise and one microphone per usable direction — and at a
realistic −60 dB you get about three.** At −50 dB you get nothing.

That is not a failure of the method, it is the honest arithmetic: amplitude and damping trade off
against each other almost exactly, so the parameters are nearly degenerate even when the *response* is
well measured. What is well determined at realistic noise is a handful of **combinations** — which is
precisely what an equaliser needs, and not at all what a modal-parameter table needs.

**Product consequence:** the lab should promise *margin and correction*, not a modal parameter table.
The anti-feedback design (AirMatrix 34) needs the loop gain near the critical frequency, which is a
combination and survives this; a "here are your 36 modes" readout would be a confident lie at normal
measurement noise.

## Can a box stand in for a room? Yes — if you randomise it

Rob: *"you can't test this in the box, like you did for a 1-D room?"* You can, and doing it properly
changes the numbers twice.

### First: break the symmetry

A 6 × 4.5 × 3 m box has rational side ratios, so its modes are **exactly degenerate** — 38 of 104 modes
below 200 Hz share a frequency. A real room's modes sit apart. Replacing the sides with incommensurate
lengths (6 × 4.37 × 3.11 m) removes every degeneracy:

| geometry | modes below 200 Hz | degenerate | usable at 3 mics |
|---|---|---|---|
| 6 × 4.5 × 3 | 104 | **38** | 3 / 36 |
| 6 × 4.37 × 3.11 | 100 | **0** | 3 / 34 |

**Degeneracy is not the limiting factor.** Making the room non-degenerate changes the count by nothing —
the amplitude/damping trade-off is what limits it. That is worth knowing, because it was my first
hypothesis and it was wrong.

### Then: make the ensemble a room population

A single geometry answers a question about that geometry. A customer asks about *a room like this*. So
run the test across an **ensemble of rooms whose mode spacings follow GOE statistics** at the box's mean
density — chaotic, repelling levels, which is what a real room has:

| microphones | usable at 10% (median) | 10–90% across rooms |
|---|---|---|
| 2 | **4** | 4 – 4 |
| 3 | **5** | 4 – 7 |
| 5 | **7** | 6 – 7 |

Two things fall out:

1. **A chaotic room is *easier* than a box, not harder** — 5 usable directions at 3 mics against 3 in the
   degenerate box. Resolvable modes are identifiable modes.
2. **The answer is a spread, not a number.** Across eight rooms of the same size and the same microphone
   count the usable count ranges 4–7. Quoting a single figure for "a room" would be quoting one draw.

So the honest statement for the product becomes: **for a room of this size, at 3 microphones and −60 dB,
expect about five combinable modal parameters, and between four and seven depending on the room.** That is
a range a customer can use, and it is more informative than the number it replaces.

## What the 3-D run actually needed — and what it still needs

It failed twice before it worked, and the failures are instructive:

1. **The linear algebra, not the physics.** Pure-Python Gram–Schmidt on the finite-difference Jacobian
   reported ratios of 1e-32 and "usable directions" that *fell* as microphones were added — an
   impossible answer. A real SVD gives the clean table above. numpy is already a dependency of this
   repository's theorem validators, so this is not a new one.
2. **Degeneracies exist and must be handled.** Of 18 modes below 100 Hz, 3 are exactly degenerate
   triples — a box has symmetry, a real room does not. The parameterisation has to work on degenerate
   *subspaces*, not on individual triples, or the Jacobian is structurally deficient before any
   measurement happens.

**Still needed before the number is quotable for a venue:**

- **Complex observations.** We used `|p|`. A dual-channel transfer function gives magnitude *and* phase,
  and phase pins directions that magnitude leaves weak — AirMatrix already measures it. The 3-D number
  will improve, and by how much is unknown until it is run.
- **A noise-referenced criterion.** "Above 1e-3" is a 60 dB conditioning floor chosen by hand. The real
  threshold is set by measurement SNR and mic self-noise: a direction is usable when its noise
  amplification stays under what the correction can tolerate.
- **Wall impedance and air absorption.** The box assumes rigid walls; a room's modes are shifted and
  broadened by both. That matters for "geometry known" — the frequencies we treat as known are not
  exactly the frequencies a room has.
- **A real room.** The box is an idealisation with exact degeneracies. The number must be re-run on
  captured data from an actual venue, where modes veer and are non-degenerate.

## The surprising part, which the test now asserts

**Knowing the geometry does not raise the identified fraction.** With the mode frequencies known there
are 10 parameters instead of 15, and one microphone identifies 4 rather than 6 — the *same 40%*. Knowing
the geometry shrinks the set that has to be identified; it does not make one microphone better.

My first version of this test asserted the opposite ("knowing the geometry buys identifiability")
because that is intuitive. The measurement said no, and the test was changed to assert what was
measured — with the reason written next to it.

## A bug caught by an impossible number

The first rank routine used an absolute tolerance and returned **rank 16 for a 15-parameter model**. A
rank above the parameter count is impossible; it was finite-difference noise in the normalised columns
being counted as independent directions. The tolerance is now relative to the largest row norm, and a
test asserts `rank <= params` — because the cheapest way to catch a numerical rank bug is to check it
against a bound it cannot legitimately cross.

## What this means for the product

1. **The claim survives, in a sharper form.** The sentence a customer can use is *"two positions
   condition the modal set; the third and fourth buy margin, not information."* That is defensible, and
   it is measured rather than asserted.
2. **It kills the arms race.** Five-mic arrays are sold for a job two positions can do — but the honest
   version sells mics 3–5 on *robustness*, which is what the conditioning curve actually supports.
3. **Rank is the wrong headline.** The usable number is the conditioning curve. Any claim built on rank
   alone ("one mic identifies everything") would have been confidently wrong.

## Reproduce

```
python3 scripts/spectral_identify.py
```

Tests: `tests/test_spectral_identify.py` — the rank cannot exceed the parameter count, one microphone
does not identify everything, saturation by two mics in 1-D, and the fraction is unchanged by knowing
the geometry.
