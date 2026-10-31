# The RF engine — one page, for a wireless engineer

**If you have one minute:** run this on your room.

```
python3 scripts/rf_plan.py --room L,W,H --band 5.18 --antennas 4 --snr 20
```

Add `--chamber` if the space is a reverberation chamber, `--iw-link <capture>` if you have a link to compare
against, `--json` if you want it as data.

It prints five blocks, **each with the status of the claim behind it**, and finishes with **what would falsify the
plan and the measurement that settles it.**

## What it claims, and how strongly

| block | claim | status |
|---|---|---|
| mode structure | Weyl count with a fitted surface term, degeneracies counted separately | **PASS-2** — 0.004% room, −0.08% chamber, 0.02% acoustic |
| streams | **3–4 of 4 at 20 dB** in an idealised room | **PASS-2** — across Q = 100…400 and three heights — **but see the limit below** |
| placement | receiver **height** is worth up to one stream | **PASS-2** |
| chamber LUF | `LUF = (Q c³ / 8πV)^(1/3)`, and the "3 × fundamental" rule is optimistic by 1.2–2× | closed form **PASS-2**, rule comparison **PASS-1** |
| thermal ceiling | `η²m = 4[Q⁻¹(ε)]²` samples per bit | **PASS-2** — derived **and** simulated |

## The limit that matters most

**The stream count is a CEILING, and no measurement in this programme has yet tested it.** Every device on the mesh
is 2 × 2 or smaller, so **no observation can exceed 2** and the 3–4 prediction cannot be probed. The one real
measurement (2.4 GHz ch 11, MCS 15, −37 dBm, 2 streams) is **consistent and explicitly non-discriminating**, and the
tool says so in its own output.

> **Practice is 2–3 of 4 at 20 dB. The model says 4. The gap is channel sounding — the standard's CSI budget, not
> the field.** That is a strong hypothesis, not a result.

## What is NOT claimed

- **Not a wave solver.** No diffraction, no material database, no CAD import. It counts modes, resolves what is
  identifiable and bounds what follows.
- **No polarisation in the shipped default** (the vector model exists and gives 3–4, but the scalar ceiling is what
  the plan reports).
- **No furniture, people or scattering** — all of which *add* degrees of freedom, so the ceiling is the ideal case.
- **The noise floor is unavailable on the hardware here** (`iw survey dump` returns nothing on the Intel 7265), so
  SNR is an assumption unless a survey supplies it.

## The documents, in reading order

| why | read |
|---|---|
| run it | `rf-plan-command.md`, `one-command.md` |
| what it claims and how it was verified | `claims-registry.md` (and `claims.json`) |
| the EM twin of the acoustic engine | `em-mode-capacity.md` |
| the chamber wedge | `chamber-analysis.md`, `chamber-command.md` |
| the stream result and its ceiling | `wifi-5ghz.md`, `polarisation.md` |
| what has actually been measured | `measured-2026-10-31.md`, `validation-limit.md` |
| how to falsify it yourself | `validate-streams.md` |
| why the numbers can be trusted at all | `execution-gate.md`, `operator-ask-gate.md` |

## The three numbers that would change my mind

1. **A 3-stream client reporting 2** at 20 dB → the ceiling is too high; polarisation or sounding is larger than
   documented.
2. **A 3-stream client reporting 4** → the ceiling holds, and the sounding gap is the whole story.
3. **A measured chamber whose field is uniform at or below the rule of thumb** → the LUF criterion is too strict.

**Each is one measurement, and each is written into the document that would have to change.**
