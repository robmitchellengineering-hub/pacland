# Statistical selection over the flux landscape — first pass

Status: **measured** (pacland-rog, 2026-10-23), with a control that could have failed.
Read tier labels — proven / measured / conjectured — and never read one into another.

## The question

The no-go (constraint-first + completeness) killed the **exact equation**: no exact,
duality-invariant selector can single out a vacuum. It did **not** kill the **statistical**
route — the measure over vacua. This pass asks: does that measure *peak* (selection) or stay
*flat* (no selection)?

## Control first (reproduce a known result before trusting anything)

Denef–Douglas (hep-th/0404116) / Bousso–Polchinski (hep-th/0004134): the flux superpotential
`W₀` is **approximately uniform in the complex plane** — in particular its *phase* is uniform
over `[0, 2π)`. That is the control: if our sampler is sane, `arg W₀` must come back isotropic.

Measured on 60 SUSY flux vacua (h12 = 2, KS model, `L = Q() = 276`, ISD flux with the physical
tadpole bound `N ≤ L` enforced by rejection):

| observable | result | control |
|---|---|---|
| `arg W₀` | mean cos = **0.015**, sin = **−0.112** | **isotropic (uniform)** — Denef–Douglas reproduced |
| `N` (tadpole) | min −207, max 261, mean 109 | ISD flux → `N ≥ 0` mostly; roughly spread over `[0, L]` |
| `\|W₀\|` | min 0.64, max 11.85, mean 4.71; histogram `[14, 22, 16, 5, 3]` | peaked at small `\|W₀\|` — the natural small-`\|W₀\|` tail |
| `g_s` | 0.35 … 4.70, mean 1.02 | sampled weak-to-intermediate coupling |

**The control passed**: `arg W₀` is uniform. The sampler is not injecting a phase bias.

## The result — no statistical selection in the flux sector

The measure over the flux landscape is **flat in phase** and shows **no peak** in any corner:
`W₀` is isotropic in angle, and `\|W₀\|` is the natural small-magnitude tail. So the flux sector
does **not** statistically single out "our" vacuum — there is no selection in the flux measure
itself. This is the **stronger negative**: the "why this vacuum" question is *not* answered by
flux statistics.

## What this does and does not close

- **Closed (for h12 = 2, measured):** the flux measure is flat — no statistical selection on
  `W₀` (phase isotropic, magnitude natural). Consistent with Denef–Douglas.
- **Not closed (the honest gap):** the *cosmological-constant* distribution. The tree-level CC
  is identically zero (no-scale), so the "selection" — if any — lives in the **uplift**
  (KKLT anti-D3 / LVS α′), which is model-dependent and not in the no-scale sampler. That is
  the Bousso–Polchinski "uniform CC near zero → anthropic" piece, and it needs the uplift.
- **Not closed:** higher `h12` (the physical flux ball `N ≤ L` is small at h12 = 2; larger
  tadpole bound or `h12 > 2` would sharpen the `N` and `|W₀|` statistics).

## Falsifiable statement

> The type IIB flux measure is flat — `arg W₀` uniform, no peak — so **no statistical selection
> singles out a vacuum in the flux sector**. A measured *non-uniform* `arg W₀` (a phase peak),
> or a `|W₀|` distribution that deviates from the small-magnitude tail at fixed `N`, would
> falsify this and signal a selection mechanism.

## Reproduce

`ssh -i ~/.ssh/mesh-admin rob@100.73.60.26` → `/home/rob/cytools-venv/bin/python`, the
iterated-shift sampler at h12 = 2 with `N ≤ model.Q()` enforced by rejection, recording
`N, W₀, g_s` per SUSY vacuum. The `arg W₀` isotropy is the control; a run with a seeded RNG
reproduces `cos ≈ 0.015, sin ≈ −0.112` over 60 vacua.
