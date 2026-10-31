# Measurement 001 — the first real link, recorded so it can be re-read

**Captured:** 2026-10-31, `pacland-rog` (Intel 7265, 2 × 2), on Rob's home network.
**Raw data:** [`docs/data/iw-link-2026-10-31.txt`](data/iw-link-2026-10-31.txt) — verbatim.
**Command that captured it:** `iw dev wlp2s0 link` — `iw` built per-user from the Ubuntu package, no root needed.

```
SSID: Telstra3696
freq: 2462.0
signal: -37 dBm
rx bitrate: 144.4 MBit/s MCS 15 short GI
tx bitrate: 144.4 MBit/s MCS 15 short GI
```

## What it establishes

| quantity | value | derivation |
|---|---|---|
| band, channel | **2.4 GHz, channel 11 (2462 MHz)** | `freq:` |
| signal | **−37 dBm** | `signal:` |
| **spatial streams** | **2** | **`MCS 15`** — HT MCS 8–15 are two streams |
| client capability | **2 × 2** | it cannot negotiate more than 2 |

**The model, at this band and two antennas, predicts 2 of 2.** Consistent — and **explicitly non-discriminating**,
because a 2-element ceiling cannot be beaten by a 2-stream observation. The tool prints that word rather than
"confirmed".

## Reproduce the comparison

```
python3 scripts/rf_plan.py --room <L>,<W>,<H> --antennas 2 --iw-link docs/data/iw-link-2026-10-31.txt
```

## What it does NOT establish

- **No room dimensions.** The room was not measured, so the plan's other blocks (mode count, chamber question) are
  illustrative for this capture, not a claim about that room.
- **No noise floor.** `iw survey dump` returns nothing on this driver, so SNR is not measurable here; −37 dBm
  against an unknown floor is not an SNR.
- **One position, one client.** No ordering test.
- **Nothing about the 3–4 stream ceiling**, which needs a client that can report 3 — see `validation-limit.md`.

## Why it is committed anyway

**Because a measurement that lives only in a chat log cannot be checked.** This file plus the raw capture plus the
command is the smallest unit of evidence this programme accepts: **a number, its provenance, and the thing that
would have to change if it were wrong.**

**Falsifier for this record:** if the capture is ever re-read and `parse_link` yields anything other than 2 streams
and 2.4 GHz, this document is wrong and so is the tool that parsed it.
