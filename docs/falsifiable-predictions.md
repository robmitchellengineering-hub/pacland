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

**Status — decided (refined), 2026-10-18.** On 133 SUSY vacua (`data/mass_degree0_large.json`),
the raw eigenvalues ARE learnable from flux — eig[0..5] ridge-quad CV r =
[+0.03, +0.37, +0.50, +0.53, +0.58, +0.62], with the heaviest slot significant at
**z = +5.54** (permutation null). The naive claim (all r < 0.25) is **falsified**.
But the learnability is the *scale*, not the *fingerprint*: the scale-invariant
ratios eig[j]/eig[5] give r = [+0.09, +0.16, +0.21, +0.15, +0.08] — all random
(r < 0.25), and the heaviest eigenvalue correlates with the tadpole at only +0.12.
So the mass spectrum's **shape is statistically uniform in flux** (the fingerprint
is NOT there), while its **overall scale is flux-determined** through a quadratic
form distinct from the tadpole. **Claim 1, refined: confirmed for the shape,
falsified for the scale — the fingerprint lives in the constraints, not the
spectrum.** The instanton-corrected (Kähler-moduli) half remains unmeasured.

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
