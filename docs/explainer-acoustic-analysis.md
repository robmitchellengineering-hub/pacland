# What the acoustic analysis does — in plain English

No jargon where a plain word will do. The maths behind it is in
[identifiability-of-room-modes.md](identifiability-of-room-modes.md) and the code in `src/pacland/spectral/`.

## In one sentence

Before anyone spends money on microphones or promises a customer a corrected room, this tells you **how
much of a room's sound a given microphone setup can actually know** — as a number, with the assumptions
printed next to it.

## The problem it answers

Room correction is sold by microphone count. Buy more mics, get a better room. Nowhere does anyone
publish the answer to the obvious question: *how many microphones do you need before you have all the
information there is?* We can answer that, and the answer is smaller and stranger than the sales copy —
which is exactly why it is worth having.

There is a second question behind it. When software works out a room's resonances, how do we know it got
them right? A room's own acoustics turn out to contain a check on that, and we use it.

## How it works, in four steps

**1. A room is a set of resonances.** At low frequencies a room rings at particular pitches — its *modes*.
Each one is described by three numbers: where it rings, how fast it dies away, and how loud it is.

**2. A microphone gives you one kind of evidence.** At each seat, a microphone reports loudness against
frequency. That is all it reports; anything you cannot see in that curve, you cannot recover later, no
matter how clever the software.

**3. Nudge each unknown and watch what moves.** Take every unknown number in the room model and nudge it
a hair. Some nudges change the microphone curves, some change nothing that any microphone can see. Count
the independent directions that actually move — that count is the answer to "how much can a microphone
setup know". An unknown whose nudge moves nothing is *invisible*, and no amount of processing will get it
back.

**4. Then add the noise, because that is the honest question.** Real measurements are noisy. Nudge the
unknowns and ask not *can* we see the change but *how precisely* can we pin each number down, given the
noise. That is the honest answer, and it is considerably smaller than the noiseless one.

## What it found — three answers, each correcting the last

| stage | answer | verdict |
|---|---|---|
| how many unknowns are visible at all | **one** microphone separates every resonance in a simple 1-D case; two is the maximum useful | encouraging, and *wrong to publish on its own* |
| how well are they separated | one microphone leaves **six** directions ten orders of magnitude below the rest — that is noise, not information. Two separate them all | two is the real minimum |
| how precisely, at real noise | at a realistic **−60 dB** you can pin about **3 of 36** parameters to within 10%; at **−50 dB**, none. To get 36 you would need about −70 dB and one microphone per direction | **the honest number** |

**The correction matters.** Publishing the first line would have been a confident, false claim — "one
microphone identifies everything". The noise model is what turns a true statement into a useful one, and
the useful one is: *at normal measurement noise you can reliably measure a handful of combinations, not
a table of every resonance.*

That is not a disappointment. **A handful of combinations is exactly what an equaliser or an
anti-feedback system needs.** It is only a table of 36 resonances that we cannot honestly promise.

## The walking rig, checked

A binaural pair 17 cm apart — two capsules at one position — does the work of **two separate omni
positions**. One such position conditions everything an omni pair needs two positions for. So the rig is
justified by measurement, and it makes a walking capture **half the positions** for the same information.

The honest limit: the advantage is at *one* position. If you are already walking to three positions, the
second capsule buys robustness, not information.

## The second thing it does: checking a solver against the room

A room's resonances are not arbitrary — their *spacing* has a signature. A plain rectangular room
produces resonances that fall independently (they cluster); an irregular room produces resonances that
repel each other, the same signature the Riemann zeros have. Both are known in advance from the room's
shape, which means a solver can be checked **without knowing the answer**: solve for the resonances,
measure the spacing signature, and see which family it belongs to. A solver that gets the signature wrong
is wrong even when its output looks plausible.

That is a free test that no one else applies to room solvers, and it came out of the same statistics
toolkit as the number-theory work.

## What it lets us do

- **Size the hardware honestly** — two capsules or two positions, not five. Cheaper, and defensible.
- **Place microphones on purpose** — away from a resonance's null, where that mode is invisible.
- **Promise only what survives the noise** — "margin and correction", not "here are your 36 resonances".
- **Design the anti-feedback feature around the thing that is measurable** (loop gain near the critical
  frequency is a combination, and combinations survive).
- **Reuse it anywhere** — the same test answers the same question for speaker placement, venue tuning,
  and any "how much can my sensors know" problem. That is the transferable asset, not the room.

## Where it stops, said plainly

- It is a **low-frequency** method — the modal region, roughly below 200 Hz in a room. Above that, sound
  is not a set of resonances and this does not apply.
- It assumes the **room's shape is known** (the mode shape is fixed by geometry).
- It is **linear**; it says nothing about nonlinearity in the loudspeaker.
- It says what is **identifiable**, not what is **audible**. Those are different questions and the second
  one needs ears.
- The numbers move with the **noise assumption**, which is why the noise figure is printed beside every
  number.

## How to check us

- The 1-D case has an **exact analytic answer** — modes at known pitches, shapes known in closed form — so
  there is no solver to trust. The answer was checked against that.
- The 3-D case uses a real 6 × 4.5 × 3 m room with the modes below 100 Hz computed and cross-checked.
- Everything is code in this repository with tests that run, and the full reasoning — including the stage
  where the headline had to be corrected — is in
  [identifiability-of-room-modes.md](identifiability-of-room-modes.md).
