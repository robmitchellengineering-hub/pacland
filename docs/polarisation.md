# Polarisation — implemented, direction plausible, **not validated**

**Reproduce:** `python3 scripts/polarisation.py`

The scalar model treats every antenna as sampling every mode perfectly, which is why it gives **4 of 4 streams
at 20 dB** where practice gives **2–3**. Polarisation is the obvious missing term: a mode whose electric field
is perpendicular to an element contributes nothing to it, so real elements see **fewer** independent
directions.

So the mode fields are now vectors (Pozar §6.4 / Collin, standard rectangular-cavity fields) and the channel
matrix projects each antenna's polarisation onto them.

## UPDATE — the vertical-zero was a window bug, and the result is not converged

Two corrections after the first run, both found by looking at the zero rather than accepting it:

**1. The mode window was wrong.** The first version took the lowest 120 modes between `f − 1 GHz` and `f + 1 GHz`
— an arbitrary window dominated by **far-off-resonance** modes, whose fields oscillate rapidly and cancel to a
rank-deficient sum. **That is why vertical returned zero.** Physically only modes within one resonance width
contribute (`|f₀ − f| < f/Q`), which at 5.18 GHz with Q = 200 is a **26 MHz** window holding ≈ 19,000 modes.
They are now **sampled** from that window (a stated approximation, not an arbitrary cut).

With the window corrected, **vertical returns 4, not 0** — the zero was the bug.

**2. But the answer is not converged in the mode count, and that is the real problem:**

| modes sampled | 4 × 4, vertical, 20 dB |
|---|---|
| 60 | **2** |
| 120 | **4** |
| 240 | **3** |
| 480 | **4** |

Repeatable within a sample count, **not stable across them.** So the stream count is currently a property of the
truncation, not of the room — **exactly the h12 truncation failure from earlier in this work**, in a new place.

**Therefore: no polarised stream count is quoted.** The next run must converge the mode sum (all ≈ 19,000, or a
demonstrated plateau in the cap), and that is a compute job for the node, not a laptop.

## The first run, kept because the correction is the finding

| antennas | z fraction | vertical | horizontal | random | scalar (ceiling) |
|---|---|---|---|---|---|
| 3 × 3 | 0.50 | **0** | 2 | **1** | 3 |
| 3 × 3 | 0.75 | **0** | 1 | **2** | 2 |
| 3 × 3 | 0.90 | **0** | 3 | **2** | 1 |
| 4 × 4 | 0.50 | **0** | 3 | **2** | 4 |
| 4 × 4 | 0.75 | **0** | 4 | **2** | 4 |
| 4 × 4 | 0.90 | **0** | 4 | **3** | 3 |

**The falsifier fired in one direction and not the other:** the count *does* move under polarisation (4 → 2–3
with random orientations, which is what practice reports), so polarisation is a real term. But **vertical is
zero at every height**, which cannot be right.

## Why vertical-zero is not a result

`Ez ∝ sin(mπx/a) sin(nπy/b) cos(pπz/d)` — so a vertical element at `z = d/2` sees only **even-p** TM modes
(the odd ones vanish there), and at the heights tested the surviving sum evidently collapses to a
numerically rank-deficient matrix. That is either:

- a **degenerate special case** of these positions, or
- a **defect** in the field expressions or their signs.

**I cannot tell which from this run, so the run is PASS-1 and the claim is not made.**

## The converged run — polarisation is NOT the missing physics

Full resonance window (**38,985 modes** at 5.18 GHz, Q = 200), summed as a matrix product on `pacland-rog`,
caps 1,000 → 20,000, three seeds per cap, three receiver heights:

| height | 1,000 | 2,500 | 5,000 | 10,000 | **20,000** |
|---|---|---|---|---|---|
| z = 0.50 | 4,4,4 | 4,4,4 | 4,4,4 | 3,4,4 | **3,4,4** |
| z = 0.75 | 4,3,4 | 4,4,2 | 4,4,3 | 4,4,4 | **4,4,4** |
| z = 0.90 | 4,4,4 | 4,4,4 | 3,4,4 | 3,4,4 | **4,4,4** |

**The falsifier resolves cleanly:** at the largest cap the count is **3–4 of 4**, and the residual variation is
across *seeds* (the sampled mode draw), not across caps. So the mode sum is **converged in the cap** and the
polarised answer is **3–4 streams at 20 dB**.

**Which is not what practice reports.** Practice is 2–3. So:

> **Polarisation accounts for at most one stream. It is not the missing physics.**

**The next hypothesis, and it is now the leading one:** real APs do not use all the spatial streams the channel
supports — the constraint is the sounding/CSI budget and the pilot structure, not the field. A 4-antenna AP can
have a 4-stream-capable channel and still agree 3 with its client because of how it sounds the channel.

That is a testable claim, and it is *not* a physics one: it is a limit of the standard's channel-sounding
protocol, which is why no amount of mode modelling will reproduce it.

## The converged run — polarisation is NOT the missing physics

Full resonance window (**38,985 modes** at 5.18 GHz, Q = 200), summed as a matrix product on `pacland-rog`,
caps 1,000 → 20,000, three seeds per cap, three receiver heights:

| height | 1,000 | 2,500 | 5,000 | 10,000 | **20,000** |
|---|---|---|---|---|---|
| z = 0.50 | 4,4,4 | 4,4,4 | 4,4,4 | 3,4,4 | **3,4,4** |
| z = 0.75 | 4,3,4 | 4,4,2 | 4,4,3 | 4,4,4 | **4,4,4** |
| z = 0.90 | 4,4,4 | 4,4,4 | 3,4,4 | 3,4,4 | **4,4,4** |

**The falsifier resolves cleanly:** at the largest cap the count is **3–4 of 4**, and the residual variation is
across *seeds* (the sampled mode draw), not across caps. The mode sum is **converged in the cap**, and the
polarised answer is **3–4 streams at 20 dB**.

**Which is not what practice reports.** Practice is 2–3. So:

> **Polarisation accounts for at most one stream. It is not the missing physics.**

**The next hypothesis, and it is not a physics one:** real APs do not use all the spatial streams the channel
supports — the constraint is the **channel-sounding / CSI budget and pilot structure**. A 4-antenna AP can have a
4-stream-capable channel and still agree 3 with its client because of how it sounds it. No amount of mode
modelling will reproduce that, because it is a limit of the standard, not of the room.

## What validation this needs, before any claim

1. **a single-mode check**: at one (m,n,p), compare the field vector against a textbook worked example or a
   cavity solver, and confirm the *signs* — the rank structure is sign-sensitive where the scalar magnitude
   was not;
2. **a polarisation sweep at fixed position**: rotate one antenna through 90° and confirm the coupling follows
   `cos θ`, which is the one behaviour anyone can predict by hand;
3. **only then** re-run the stream table.

**Falsifier for the next attempt:** if a single-mode field vector matches the reference but vertical coupling
still collapses to zero, the degeneracy is real and the geometry is at fault. If the vector does not match, the
model is wrong and every number in the table above is void.

## What is safe to say now

- the **scalar model is a ceiling** and polarisation is a real reduction (direction: practice 2–3 sits below it);
- the **specific polarised numbers are not yet trustworthy**;
- and the honest shape of the claim — *"polarisation is the leading missing term, magnitude unquantified"* — is
  worth more than a table that looks precise.
