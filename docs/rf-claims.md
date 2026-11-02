# The RF claims registry — what the radio work may quote, and what it may not

**`docs/rf-claims.json` · enforced by `tests/test_rf_claims.py`**

Nine numbers, each with the script that reproduces it, the document it appears in, and **the check that could make it
wrong**. Modelled on the physics registry (`docs/claims.json`), because the physics work has one and the radio work — which
produces numbers a customer will act on — did not.

## The states

| status | meaning | what it may be quoted as |
|---|---|---|
| **PASS-2** | reproduced by an **independent path** — another measurement, another tool | a result |
| **PASS-1** | one run, falsifier satisfied | **provisional — not a certificate, not an invoice** |
| **withdrawn** | published, then failed, with the reason | evidence of the retraction |

## What is registered

| claim | status | note |
|---|---|---|
| **ceiling 2.58 m ± 0.09** | **PASS-2** | three sessions, plus Rob's statement that the ceilings are identical |
| **ARCore beats step counting** | **PASS-2** | 92/92/62 counts, strides 0.326 vs 0.484 m, loops closing to 9–25% |
| **16 dB fading at a fixed spot**, power exponential (1.21) | **PASS-2** | two rooms, same shape |
| **6 dB action floor** | **PASS-2** | the floor every finding is measured against |
| **33 dB house spread, −28 to −61 dBm** | **PASS-2** | 12 spots, 9 of 10 walks agree |
| **2.4 GHz ch 11 → ch 1 for −24 dB** | **PASS-1** | **one plan, not yet applied — this is the change waiting on the login** |
| **5 GHz ch 36 → ch 40/44 for 31–34 dB** | **PASS-1** | two independent plans agree; still unapplied |
| **the room is a diffuse cavity** | **PASS-1** | one walk series |
| **lattice recovery to 1.83% under damage** | **PASS-1** | simulated spectrum, not yet a measured one |

## What the registry says that the prose did not

**Four of nine are PASS-1** — including **both channel changes**, the two numbers with money and risk attached. **They are
provisional until a post-change scan reproduces them**, and that is exactly the change the network login unlocks.

**`lattice-recovery` is PASS-1 for a specific reason**: it was demonstrated on a **simulated** spectrum. Its falsifier names
the missing test — *recovery failing on a measured room spectrum at the same damage* — and **that has not been run.**

**Nothing is withdrawn yet.** The physics registry has three withdrawn claims; this one starting at zero is not a virtue, it
is just a shorter history.

## The falsifier for the registry itself

> **If every PASS-1 becomes PASS-2 on its first independent check, the statuses were conservative and the registry is
> bookkeeping.** That is the cheap case. **The valuable case is the opposite** — a number that looked solid and turns out to
> be PASS-1, which is why the two channel changes are flagged rather than buried.
