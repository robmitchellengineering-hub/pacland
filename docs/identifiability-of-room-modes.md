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

1. **The claim survives.** "How many mics you need" is a real question with a non-trivial answer, not a
   triviality. It becomes a sentence a customer can use: *"for modal correction in a room like this, two
   positions identify the modes; a third buys robustness to a bad mic, not new information."*
2. **It kills the arms race.** Five-mic arrays are sold for a job two mics can do. The honest version of
   the product says so — and then sells the *third* mic as robustness, which is a defensible claim.
3. **It is a 1-D result.** A real room is 3-D with mode veering and near-degeneracies; the same
   machinery must be run on a 3-D geometry before the number is quoted for a room. That is the next
   measurement, and this document will change when it lands.

## Reproduce

```
python3 scripts/spectral_identify.py
```

Tests: `tests/test_spectral_identify.py` — the rank cannot exceed the parameter count, one microphone
does not identify everything, saturation by two mics in 1-D, and the fraction is unchanged by knowing
the geometry.
