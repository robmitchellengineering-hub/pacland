# A bound for two-state ambient-thermal-noise communication

**Target:** *"First-principles channel model and capacity-achieving transmission scheme in thermal noise
backscatter links"*, PNAS, [doi:10.1073/pnas.2606732123](https://www.pnas.org/doi/abs/10.1073/pnas.2606732123)
— reported as **up to 1,000× less transmitter energy** than RF, with a **100× rate improvement** after their
channel model.

**Reproduce:** `python3 scripts/thermal_noise_bound.py`

## What this is, and what it is not

It is **not** a reproduction of their result — the numeric parameters (bandwidth, contrast, achieved bit
rate, noise temperature) are behind the publisher's paywall and were not obtainable from the public release,
so none of their figures are quoted here. What is derived below is the **bound their design must satisfy**,
expressed as a function of those parameters, so the comparison can be completed in one substitution.

## The model

A resistor at temperature `T` presents available noise power `P = k_B T B` in bandwidth `B` (Nyquist). A
switch between an absorbing and a reflecting state changes the power the receiver sees by a contrast `η`:

```
P_0 = k_B T B            (reflecting)
P_1 = k_B T B (1 + η)    (absorbing)
```

A radiometer integrating for `τ` obtains `m = Bτ` independent samples. Thermal noise is Gaussian, so a power
estimate is exponentially distributed and its **relative** standard deviation is `1/√m`.

Per-sample Fisher information for the state, from the difference of means over the standard deviation:

```
I = (ΔP)² / var = (ηP)² / (P²/m) = η²·m
```

Binary decision: `ε = Q(√(I/2))`. Achievable spectral efficiency (one observation per sample-pair, binary
input): `C/B = 1 − H₂(ε)`.

## The bound, which has one term that matters

**`η²·m = 2·[Q⁻¹(ε)]²`** — a fixed product for a target error rate. It does not care how the contrast is
generated, how clever the receiver is, or which switch technology is used.

| contrast η | samples for BER 1e-3 | samples for BER 1e-6 | τ at B = 1 MHz |
|---|---|---|---|
| 1e-3 | 1.9e+07 | 4.5e+07 | 19.1 s |
| 1e-2 | 1.9e+05 | 4.5e+05 | 0.19 s |
| 0.1 | **1.9e+03** | 4.5e+03 | **1.9 ms** |
| 0.5 | 76 | 181 | 76 µs |
| 1.0 | 19 | 45 | 19 µs |

**So the rate is bought entirely with the product `η²·m`.** Their 100× improvement, if it came from a better
channel model rather than from a better switch, is a 100× in the *effective* `m` — which is a statement about
how much of the available noise they can actually use, not about the noise itself.

## The sharp point: which side is the energy counted on?

**The transmitter's energy per bit can be made arbitrarily small**, because the switch dissipates only its
own switching energy and radiates nothing. That is where a 1,000× figure comes from, and it is real *for the
transmitter*.

**The receiver pays in integration**: `m = η²`-inverse samples at roughly `P` each. So a 1,000× saving at the
transmitter can be a large *cost* at the receiver, and **a claim of the form "1,000× less energy" means
nothing until it says which side of the link it is counting.** That is the same defect this repository keeps
finding: a number whose measurement basis is unstated.

**The comparable figure is joules per bit end-to-end**, or joules per bit at the receiver for a stated rate —
and the bound above is what makes that comparison possible.

## What is needed to finish the comparison

Four figures from the paper, none of which the public release carries:

1. **achieved bit rate** (bit/s) and the **BER** it was quoted at;
2. **bandwidth** `B` of the noise being switched;
3. **contrast** `η` — the fractional change in what the receiver sees between the two states;
4. **energy per bit**, and whether it is transmitter-only or end-to-end.

Substituting (1)–(3) into `η²·m = 2[Q⁻¹(ε)]²` gives the samples actually used; dividing the paper's energy
per bit by that gives joules per sample, which is the one number that can be compared with a conventional
link.

## Falsifier

If their reported rate requires `η²·m` more than a few times the bound above, the scheme is not
capacity-achieving and the 100× is an artefact of the comparison's baseline. If it sits at the bound, the
model is right and the remaining question is entirely the switch's contrast — which is a materials problem,
not an information one.
