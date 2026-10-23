# The cosmological-constant distribution — flux vs uplift

Status: **measured** (pre-uplift, pacland-rog) + **literature under test** (uplift, two passes in
flight). Read tier labels — proven / measured / conjectured — and never read one into another.

## The question

The statistical-selection pass found the flux measure is **flat** (no selection). The one place
a selection could still hide is the **cosmological constant after uplift**. Bousso–Polchinski
(hep-th/0004134) claim the CC is ~uniform near zero, so the small observed `Λ` is the tail of a
flat discretuum — not a selection. This doc pins the honest boundary between what the node can
measure and what is model-dependent.

## What the node measured (pre-uplift, computable)

The tree-level CC is identically zero (no-scale). The *pre-uplift* CC is the KKLT AdS depth
`Λ_AdS ∝ −|W₀|²`. So the pre-uplift CC distribution is the `|W₀|²` distribution. Measured on
100 SUSY flux vacua (h12 = 2, `N ≤ Q() = 276`):

| `|W₀|` threshold | fraction below |
|---|---|
| 0.5 | 1% |
| 1.0 | 3% |
| 2.0 | 9% |
| 3.0 | 18% |
| 5.0 | 51% |
| 8.0 | 85% |

The cumulative grows **quadratically** in `|W₀|` (`1% → 3% → 9% → 18%`), so the density
`dN/d(|W₀|²)` is **constant near zero** (`|W₀|² ≲ 9`) — i.e. the pre-uplift CC `∝ −|W₀|²` has a
**uniform density near zero**. At larger `|W₀|²` the density falls (the finite-flux cutoff), so
"uniform" is precisely the *near-zero* statement — which is exactly the Bousso–Polchinski claim
(the small CC is the tail of a flat discretuum, not a peak).

## What the uplift adds — the honest boundary (computable vs model-dependent)

The post-uplift CC is `Λ = Λ_AdS + D/σ³` (KKLT anti-D3) or the LVS analogue, with
`Λ_AdS = −3|W₀|²/(8σ³)` and `D ∝ p·e^{4A₀}` (warp factor, anti-brane count). The chain from
`(W₀, N, g_s)` to `Λ` splits cleanly:

- **COMPUTABLE (sampler output):** the joint distribution of `(W₀, N, g_s)` and the marginal
  `|W₀|²` — which is the *pre-uplift scaling variable* `−3|W₀|² = Λ_AdS·8σ³`, **not** `Λ_AdS`.
- **MODEL-DEPENDENT (not in the no-scale sampler):** `A` and `a` (the non-perturbative
  superpotential `W = W₀ + A e^{−aT}`) → `σ_min` via `W₀ = −A e^{−aT}(1+2aσ/3)`; then
  `e^K = (2σ)⁻³` → `Λ_AdS`; and `D` (throat flux pair `K,M`, anti-brane count `p`, geometry)
  → the post-uplift `Λ`.

**Verdict:** the post-uplift `Λ` distribution **cannot** be measured from the current sampler —
it needs `A, a, D`, none of which the no-scale sampler carries. Claiming a "distribution of the
cosmological constant" from `W₀` alone would be an **overclaim**: at most it is the distribution
of the pre-uplift scaling variable `|W₀|²`.

Two specific traps, flagged: (1) `|W₀|² = Λ_AdS` up to a factor is only true *in units of*
`8σ_min³`, so it is not the CC; (2) the total `N` does **not** fix the warp factor — `D` needs
the per-cycle split `(K,M)`. The uplift term itself is a model assumption (the anti-D3 uplift as
a controlled 10d solution is actively debated: Moritz–Retolaza–Westphal arXiv:1707.08678,
Gao–Hebecker–Junghans arXiv:2009.03914, Kachru–Kim–McAllister–Zimet arXiv:1908.04788).

## Precise statement (fan-out verdict) — "uniform" is an overclaim, "locally flat" is the theorem

The precise Bousso–Polchinski result (hep-th/0004134 §2) is a **power law**, not uniform:

> `dN/dλ = D · ω_{J−1} · [2(λ−λ_bare)]^{(J−2)/2} / Πᵢ qᵢ`

so the vacua-per-unit-`Λ` count **vanishes** at `λ → λ_bare` for `J > 2` (flat only at `J = 2`).
The defensible statement is **"locally flat over the 10⁻¹²⁰ anthropic window"**, not "uniform".
The **uniform** result that *is* proven is **Denef–Douglas** (hep-th/0404116): `W₀` is uniform
near zero (`dN/d²W₀ ≈ const`), which is what this pass measured — but that is about `W₀`, not
`Λ`. The link `W₀`-uniform → `Λ`-uniform is a **heuristic** (needs the joint `(W₀, D, σ)`
distribution), the **uplift** to metastable dS is **contested** (anti-D3/KPV instability:
Moritz–Retolaza–Westphal 1707.08678, Córdova–de Luca–Tomasiello 1812.04147, Dall'Agata et al.
2203.12636, Hebecker–Schreyer–Venken 2208.02826), and "anthropic selection" is **unresolved**
(the measure problem). The dS swampland conjecture (1806.08362; 1807.05193; 1810.05506), if true,
empties the positive-`Λ` discretuum entirely.

## Falsifiable statement

> The **pre-uplift scaling variable** `|W₀|²` has **uniform density near zero** (measured — the
> Denef–Douglas result, proven). The flux discretuum is therefore **locally flat** over the tiny
> anthropic window, so the observed small `Λ` is the anthropic tail — *not* a dynamical
> selection. The post-uplift `Λ = −3|W₀|²/(8σ³) + D/σ³` is **model-dependent and contested**
> (needs `A, a, D`; the uplift itself is debated), so no sampler of `(W₀, N, g_s)` alone can
> claim its distribution.
>
> **Falsifiers:** a measured non-uniform `dN/d|W₀|²` near zero; a proof of the dS swampland
> bound `|∇V| ≥ cV` in a controlled compactification (kills the positive-`Λ` discretuum); or a
> rigorous no-go on the anti-D3 uplift (kills the mechanism producing positive `Λ`).

## Sources

Bousso–Polchinski hep-th/0004134 · KKLT hep-th/0301240 · GKP hep-th/0105097 ·
Klebanov–Strassler hep-th/0007191 · KPV hep-th/0112197 · Ashok–Douglas hep-th/0307049 ·
Denef–Douglas hep-th/0404116 · BKQ hep-th/0309187 · Obied–Ooguri–Spodyneiko–Vafa 1806.08362 ·
Moritz–Retolaza–Westphal 1707.08678 · Córdova–de Luca–Tomasiello 1812.04147 ·
Dall'Agata–Emelin–Farakos–Morittu 2203.12636 · Hebecker–Schreyer–Venken 2208.02826 ·
Kachru–Kim–McAllister–Zimet 1908.04788.
