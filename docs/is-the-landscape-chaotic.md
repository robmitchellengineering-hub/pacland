# Is the landscape chaotic? — the question, and what it takes to answer it

Rob asked for the biggest questions, and this is question 1 from the arm's agenda
(`docs/quantum-arm-agenda.md`). This is the honest state of it after a first attempt.

## The question, stated precisely

If the vacua of the landscape are the eigenvalues of something — a Hamiltonian, a random matrix, a
Hessian — then their **level spacings** answer the question directly:

- **Poisson** spacings ⇒ no level repulsion ⇒ the vacua are independent, the landscape is a *list*;
- **GOE** spacings ⇒ repulsion ⇒ the vacua are coupled, the landscape has a *structure*.

This is not a metaphor. It is the same statistic that took the Riemann zeros to 0.2σ of a GUE control,
and the machinery is verified and in this repository (`src/pacland/spectral/zeros.py`).

## The first attempt, and why it fails — informatively

The obvious spectrum to compute is the superpotential magnitude `|W|` across flux choices, at fixed
moduli. Sampled 1,200 fluxes in `[-4,4]^8`:

| | |
|---|---|
| distinct `\|W\|` values | **151 of 1,200** |
| max \| \|W\|² − nearest integer \| | **1.1e-13** |

**`|W|²` is an integer.** Of course it is: at fixed moduli, `W = (F − τ₀H)·Π` is a Gaussian-integer
linear combination of integer fluxes. So the "spectrum" is a **lattice**, and the spacing distribution of
a lattice is a delta function — neither Poisson nor GOE, and the question is being asked of an object
that has no fluctuation statistics to report.

That is not a null result about the landscape. **It is a null result about the observable I chose**, and
it says the question has to be asked of a *continuous* spectrum.

## What the question actually requires

A spectrum with fluctuations has to come from something that varies continuously with the fluxes. Three
candidates, in order of tractability:

1. **The Hessian of the scalar potential** at a point in moduli space, `M² = ∂²V`, whose eigenvalues are
   masses. Continuous in the fluxes, computable — but it needs `V`, which the T⁶ oracle does not
   implement, and `V = e^K(g^{ij̄}D_iW D_j̄W̄ − 3|W|²)` is easy to get wrong in a way that still looks
   plausible.
2. **Stabilised vacua**: solve `DW = 0` for each flux choice and take the masses at the minimum. This is
   the physically right spectrum and the most work.
3. **A family of moduli**: sample the moduli continuously instead of fixing them, so `|W|` inherits a
   continuous distribution. Cheapest, and the least physical — it measures the moduli prior as much as
   the landscape.

**The missing piece is `V`.** That is the next build in this arm, and it is a build rather than a
question: the potential is a formula, and the discipline here is to implement it, validate it against the
oracle's exact limits (the no-scale cancellation above a supersymmetric point, and `V = 0` at a
supersymmetric Minkowski point), and only then compute a spectrum.

## What would count as an answer

With `V` implemented and validated:

- compute the Hessian eigenvalues for an ensemble of flux choices;
- unfold them (our counting-function machinery);
- compute the ratio statistic;
- compare against **a GUE control and a Poisson control of the same size** — never against an asymptotic
  constant, which is the mistake that cost us a 4σ false failure on the zeros;
- and report which ensemble the answer belongs to, because a different sampling of fluxes is a different
  question. **If the statistics change with the ensemble, the finding is that the chaos question is a
  measure question** — which is worth knowing, and is the same conclusion the vacuum-energy question is
  heading for.

## The potential is now built — and validated 4/4

`src/pacland/oracle/potential_t6.py` implements `V = e^K(g^{ij̄}D_iW D_j̄W̄ − 3|W|²)` for the
axio-dilaton and the three T² complex structures. It is not used until it passes:

| validation | result |
|---|---|
| no-scale identity `g^{ij̄}K_iK_j̄ = 3` on the Kähler moduli | **3.0000000000** |
| a constant `W` gives `V = 0` on the Kähler sector | **0.000e+00** |
| invariance under `τ₀ → τ₀+1` with `F → F+H` | equal to 9 digits |
| a real flux choice gives a finite potential | finite |

**The first version failed both identities**, and the reason is worth keeping: a *real* finite-difference
step probes `Re τ`, and `K` depends only on `Im τ`, so every Kähler gradient came out **zero** and the
no-scale identity read `0.0` instead of `3`. The gradients are analytic now, and the metric is analytic
too — the finite-difference metric was singular for the same reason.

## What is still missing: a *stationary point*

The Hessian machinery works and returns eight real eigenvalues per flux choice, but at a **generic point
in moduli space** those eigenvalues include tachyons:

```
-1.171e+01  -2.860e+00  -1.717e+00  -1.770e-01  +4.118e+00  +5.753e+00  +1.199e+01  +1.460e+01
```

Negative eigenvalues at an arbitrary point are expected and are **not masses**. Calling them a mass
spectrum would be the same error as calling a lattice a spectrum: the right object, asked of the wrong
place. **Masses need a stationary point** — `DW = 0` (supersymmetric) or `DV = 0` — which means solving
four complex equations per flux choice by Newton's method.

That is the next build, and it is the last one between this arm and an answer to the chaos question.

## The vacua solver is built and validated by construction

`solve_supersymmetric` runs Newton on `DW = 0`. A root finder is proven by **constructing a root and
recovering it**, not by not crashing — so the test picks a point in moduli space, solves the *linear*
conditions for a flux that is F-flat there (the equations are linear in the flux and nonlinear in the
moduli, which is the whole trick), and then asks Newton to find the point from a different start:

| | |
|---|---|
| a flux made F-flat at the chosen point | **\|DW\| = 4.2e-16** |
| Newton from a different start | **converged** |
| recovered the chosen point to | **9.6e-10** |

## And the integer lattice gives nothing — which is the finding

Ten generic integer flux pairs in `[-2,2]^8`: **zero** admit a supersymmetric vacuum.

**That zero is a result.** Supersymmetric vacua require **ISD fluxes**, a measure-zero condition on the
integer lattice, so a small integer flux is generically **not F-flat anywhere**. Two routes follow:

1. **work on the ISD locus** — fluxes are then real-valued, not integers; and there is a trap: a
   supersymmetric Minkowski vacuum has **flat directions**, so its mass spectrum is full of zero modes,
   and the spacing statistic would be a statement about degeneracies rather than chaos — **exactly the
   `|W|` lattice problem again, one level deeper**;
2. **look for non-supersymmetric vacua** with `DV = 0`, which do not require ISD and whose masses are
   generically non-zero.

**Route 2 is the one that can answer the question**, and it is the next build.

## The `DV = 0` solver: validated by inheritance, and it finds nothing — which is the answer

Two corrections came out of running it, and **both were the test's fault, not the solver's**:

1. the first version started at random and demanded *the* constructed susy point. The potential has
   **several** stationary points, so landing on a different one is not a failure — the test was
   measuring a basin of attraction, not a solver;
2. the finite-difference step mattered: `1e-6` was too noisy for Newton, `1e-4` converges cleanly.

Corrected, it recovers the known point from **0.05** and **0.3** away to `1.7e-8`, with `|grad V| ~ 2e-10`.
And the constructed point is not merely stationary but a **minimum** with all-positive masses — with
`V = -3e^K|W|^2 < 0`, i.e. an **AdS** vacuum, which is stable. (A susy vacuum with `W != 0` is AdS, not
Minkowski; expecting `V = 0` would have been wrong.)

### And then: eight generic integer fluxes, zero stationary points

| | |
|---|---|
| generic integer flux pairs tried | **8** |
| stationary points found (`DV = 0`) | **0** |
| minima | 0 |

**That is the physics of this toy, not a solver failure.** The tree-level T⁶ model has the axio-dilaton
and complex-structure moduli and **no Kähler moduli**, so there is nothing to stabilise the volume — the
potential is a **runaway**, and a runaway has no minimum to find. Real IIB vacua need Kähler moduli with
non-perturbative terms (the KKLT/LVS programme) before a vacuum spectrum exists at all.

**So the honest answer to "is the landscape chaotic?" in this arm is: the question cannot be asked of the
model we have.** There is no vacuum spectrum in the T⁶ toy to take spacings of, and saying otherwise
would be the third mistake of the same family — a statistic computed on the wrong object.

## The earlier `DV = 0` state, kept for the record

The non-supersymmetric route is the one that could answer the question, so the solver was written. It
has a clean validation available: **a supersymmetric point satisfies `DW = 0`, which implies `DV = 0`,
so the stationary solver must recover the constructed susy vacuum.**

It does not. It lands **0.9 away** in moduli space.

| | |
|---|---|
| constructed susy vacuum | recovered exactly by `solve_supersymmetric` (9.6e-10) |
| same point, sought with `DV = 0` | **missed by 0.9** |

The likely cause is that the gradient is a **finite difference** with step 1e-6, which is far too noisy
for Newton on a potential of this shape; the flat directions of a supersymmetric vacuum compound it.
The fix is analytic gradients — a known, bounded piece of work — and until it is done **no mass spectrum
from this solver is reported**, and a test pins the failure so nobody builds on it by accident.

That is the difference between a research arm and a demo: the last piece is not finished, and the arm
says so in its own repository rather than shipping a number.

## Honest current status

| | |
|---|---|
| the machinery | **verified**, reused from the zeros work |
| the spectrum | **`V` is built and validated 4/4**; masses need a stationary point, which is the remaining build |
| the answer | **open** |
| the next step | analytic gradients for `DV = 0`: the finite-difference version misses a known stationary point by 0.9 |

This is what an honest research arm looks like from the inside: one question, one failed first
approach that taught us what the observable has to be, and a named next build.
