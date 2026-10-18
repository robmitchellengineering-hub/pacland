# The structure map — every observable classified (Rule-of-Three verified)

Each row is a flux-determined observable, tested with the joint ridge-quadratic CV
`r` on the natural (ISD, wide-flux) measure, plus the narrow-flux number where it
exists. "Uniform" = r < 0.25 on *both* measures; "weakly learnable" = r ≈ 0.3–0.6;
"exact" = r = 1.0 (the positive control).

| observable | narrow-flux r | wide-flux r | verdict |
|---|---|---|---|
| **tadpole N_flux** | 0.99 | **1.00** | **exact** — the symplectic pairing FᵀJH |
| W₀ (log\|W₀\|) | 0.10 | **0.62** | **weakly learnable** — scale via the tadpole |
| saxions (moduli sizes) | — | 0.30–0.42 | weakly learnable — flux stabilizes sizes |
| g_s | 0.21 | 0.12 | uniform |
| gauge couplings | ≈0.15 | 0.02–0.12 | uniform |
| mass-spectrum shape (ratios) | — | < 0.25 | uniform |
| axions (moduli phases) | — | 0.15 | uniform |
| axio-dilaton (Re τ) | — | 0.13 | uniform |
| AdS potential V | — | 0.00 | uniform |

## What this says

The low-energy observables are a **mostly-unstructured cloud**: g_s, the gauge
couplings, the mass-spectrum *shape*, the axions, the dilaton, and the cosmological
constant are all statistically uniform in flux. Two things carry weak structure —
**W₀** (its scale tracks the tadpole) and the **saxions** (flux stabilizes the
sizes). Exactly one thing is *exactly* structured: **the tadpole**, the D3
constraint.

The geometric **fingerprint** (an observable with r > 0.9 that would pin the
compactification) is **absent** — nowhere except the constraint itself. The
constraint-first thesis, restated precisely: *the landscape's only exact structure
is what it forbids; everything it produces is noise plus a weak scale.*

## Honesty ledger (what this map cost)

- **W₀ "zero-information" was retracted** — it was a single-coordinate artifact; the
  joint test gives r = 0.62 on wide flux (see `docs/learnability-negative.md`).
- **"Search over W₀ not evolvable" was re-derived** — the target is 20 σ_pred outside
  the observed range, so search is hopeless by rarity + extrapolation, not by
  zero-information.
- **g_s and the gauge couplings were re-verified** — uniform on wide flux, so their
  "random" claims are robust (unlike W₀'s).
- The **Rule of Three** (`AGENTS.md`) is what forced every one of these corrections.
