# The claims registry — PASS-1, PASS-2 and withdrawn, made mechanical

**`docs/claims.json` · enforced by `tests/test_claims_registry.py`**

Every published number in this work now carries a status, the script that reproduces it, the document it appears
in, and the check that could make it wrong. Eleven claims are registered, and **three of them are withdrawn.**

## The three states

| status | meaning | what it may be quoted as |
|---|---|---|
| **PASS-2** | reproduced with a different parameterisation — another Q, another band, another layout, or an independent path | a result |
| **PASS-1** | one run, falsifier satisfied | **provisional. Never a result, never in a paper or a certificate** |
| **withdrawn** | published, then failed — with the reason recorded | evidence of the retraction, not the claim |

## What the guard enforces

1. **every claim has a script**, and the script exists in the repository (the first run of this guard immediately
   found `scripts/node_polarisation_converge.py` **missing from main** — the file had been cited in a merged
   document and never merged, which is the third time that has happened here);
2. **every claim has a document**, and the document exists;
3. **PASS-2 requires at least two independent evidence lines** — so the status cannot be typed on;
4. **a withdrawn claim must state its reason**, so a retraction cannot be silent;
5. **a live claim must state a falsifier**, so it cannot be unfalsifiable by construction.

## The eleven claims

| claim | status |
|---|---|
| Weyl mode count, fitted surface term | **PASS-2** |
| 77–92% exact degeneracies in a rectangular space | **PASS-2** |
| scalar streams: 3–4 of 4 at 20 dB (ceiling) | **PASS-2** |
| polarised streams: 3–4 at 20 dB | **PASS-1** |
| chamber `LUF = (Qc³/8πV)^(1/3)` | **PASS-2** |
| the 3 × fundamental rule is optimistic by 1.2–2× | **PASS-1** |
| thermal ceiling `η²m = 2[Q⁻¹(ε)]²` | **PASS-1** |
| 17–19 of 40 modes usable at −60 dB | **PASS-1** |
| **"3 of 4 streams matches practice"** | **withdrawn** — it was the receive layout, not the room |
| **"degree 2 fixes the h12 yield"** | **withdrawn** — degree 0 silently disabled the corrections |
| **"the solve is the h12 wall"** | **withdrawn** — the criterion's two fields disagreed by 75 orders |

## Why a registry and not a habit

The failure mode this whole programme keeps meeting is **a number that was true of the setup being quoted as
true of the world.** A status field and a two-evidence rule cannot catch that on their own — but they make it a
**deliberate act** to promote a claim, and they leave a record when it is demoted.

**Three withdrawals from one night is the evidence that the registry is needed, not that it is excessive.**
