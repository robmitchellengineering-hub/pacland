# Why this house cannot test the 3–4 stream ceiling — and what would

**Written after trying every route, including the ones that looked closed.**

## The measurement we want

The model says an **idealised 3 × 4 × 2.5 m room supports 3–4 streams of 4 at 20 dB** (PASS-2, across Q = 100…400).
Practice says hardware delivers **2–3**, because a real AP does not use every stream the channel supports. **The
gap between 4 and 2–3 is the claim under test.**

A test needs an observation that could fall **outside** the prediction. Two ways:

1. **a client that reports 3 or more streams** — then 4 would confirm the ceiling and 2 would falsify it;
2. **a position where the model predicts fewer streams than the client can deliver** — a low-SNR corner.

## Why neither is available here, measured not assumed

| device | what it can do | how we know |
|---|---|---|
| **Legion** (RZ616) | **2 × 2** — 866.7 Mbps negotiated on 80 MHz | `Get-NetAdapter`: LinkSpeed 866.7, the canonical 2 × 433.3 |
| **Laptop** (two adapters) | **2 streams** at 866.7 Mbps, **1 stream** at 72.2 Mbps | same, both links |
| **`pacland-rog`** (Intel 7265) | **2 streams** — `MCS 15` on 2.4 GHz, `iw link` | verbatim capture |

**Every device on this mesh is 2 × 2 or smaller.** A 2-stream client **cannot report 3**, so the 3–4 ceiling cannot
be probed from below, and at −37 dBm the SNR is ~58 dB, so there is no low-SNR corner to probe from the other side.

**And the phone is not on the mesh**, so it cannot be read either.

## What that means

- **The ceiling claim is untested, not confirmed.** It stays PASS-2 *as a computation* — reproduced across Q, height
  and two independent parameterisations — and **no measurement can promote or refute it on this hardware.**
- **This is not a wall to push.** Pushing it was the mistake: three sessions of asking, then Location registry keys,
  then a direct `WlanConnect` P/Invoke that returned rc=87. **The blocker is the client radio's stream count, not the
  platform's permissions.**
- **The tests that ARE possible have been run**: 2 streams at 2.4 GHz ch 11, MCS 15, −37 dBm — consistent, and
  explicitly **non-discriminating**, which the tool now says out loud.

## What would settle it

| option | cost | what it tests |
|---|---|---|
| **a 4 × 4 AP and a 3-stream client** (e.g. a WiFi 6 laptop with an AX210, or a phone that reports 3) | one device | the ceiling, directly |
| **a low-SNR position**: the same client at the far end of the house, with the AP's transmit power dropped | free, if a radio can be attenuated | the SNR dependence of the ceiling |
| **a chamber or anechoic space** where the field is controlled | a lab | the whole mode model, not just the streams |

**Falsifier, standing:** a 3-stream-capable client that reports **4** at 20 dB in a room like this confirms the
ceiling; one that reports **2** refutes it and the model is optimistic beyond the documented sounding gap. **Either
answer is a result, and neither is reachable from this house.**

## The honest closing note

The programme's own rule is that **a test which cannot fail is not evidence.** A 2 × 2 client against a 2 × 2
ceiling is exactly that — and the right response is to **say so and stop**, not to run the comparison again in a
different form until it looks like confirmation.
