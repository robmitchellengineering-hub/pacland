# Falsifiable predictions — what PACLAND claims that can be checked

A verification discipline earns its keep by *predicting* something checkable, not
just by certifying what is already known. This doc lists the claims PACLAND makes
that a future measurement can confirm or refute. Each is stated with its
falsification criterion, so the framework is science, not taxonomy.

## 1. The mass spectrum is statistically uniform in flux (the headline prediction)

**Claim.** Once the IIB flux mass spectrum is computable, its eigenvalues will carry
*no more information about the flux than W₀, g_s, and the gauge couplings do* — all
measured at |r| < 0.25 (ridge on quadratic features). The geometric fingerprint is
**not** in the mass spectrum; it lives only in the *constraints* (the tadpole, which
is exactly the symplectic pairing, r = 1.0).

**Grounds.** Every flux-determined observable measured so far is statistically
uniform in flux — W₀ (r = 0.099), g_s (r = 0.210), gauge couplings (r ≈ −0.16…+0.17) —
by Denef–Douglas uniformity. The mass spectrum is determined by the same flux,
through the instanton-stabilized moduli, so uniformity is the null hypothesis.

**Falsification.** Compute the mass eigenvalues for a sample of flux vacua and run
`pacland.structure.ridge_cv_predictability(fluxes, eigenvalue)`. If any eigenvalue
gives **r > 0.5**, the prediction is falsified — the mass spectrum *does* carry the
fingerprint, and the structure miner's target is real. If all eigenvalues give
r < 0.25, the prediction is confirmed and the "fingerprint" search is closed.

**Status.** Untestable today — the mass spectrum computation is killed even at
n = 10 (the unmeasurable wall, `docs/boundary-map.md` #6). This is exactly where
"use the wall" applies: the unmeasurability is *not* a dead end, it is the
**specification of the falsification test** that will decide claim 1.

## 2. New flux-vacua samples will reproduce log-uniform W₀ (R² ≈ 0.92)

**Claim.** The |W₀| distribution is log-uniform on the natural (ISD) measure.

**Falsification.** Sample a new batch of SUSY vacua with JAXVacua's ISD measure;
if the CDF of log|W₀| deviates from linearity (R² ≪ 0.9), the claim is refuted.

**Status.** Measured once on 380 vacua (R² = 0.92) — reproducible, not yet reproduced.

## 3. The D3 tadpole is always the exact symplectic pairing

**Claim.** For any flux, N_flux = Fᵀ J H with J = [0 I; −I 0], exactly (r = 1.0).

**Falsification.** A single flux whose tadpole is not this bilinear form refutes it.

**Status.** Confirmed at machine precision on 107 real vacua — effectively a theorem.

## 4. Weak-coupling and small-W₀ are independent constraints

**Claim.** The two phenomenological constraints compose multiplicatively
(interaction z = 0.74, i.e. consistent with perfect independence).

**Falsification.** A larger sample where the 2×2 survival table departs from
independence (|z| > 2) would refute it.

**Status.** Measured on 107 vacua; the "+0.8% interaction" is one vacuum of noise.

## What this is for

The whole program — the deficit, the boundary map, the constraint-first solver —
terminates in these four checkable claims. Claim 1 is the frontier: it is the single
prediction whose test requires building the one oracle we do not yet have (the mass
spectrum). That is the definition of "closing the deficit IS finishing the solve."
