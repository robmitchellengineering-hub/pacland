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

## Honest current status

| | |
|---|---|
| the machinery | **verified**, reused from the zeros work |
| the spectrum | **not yet computable** — needs `V`; the naive choice is a lattice, measured |
| the answer | **open** |
| the next step | implement and validate `V` on T⁶, then compute the Hessian spectrum |

This is what an honest research arm looks like from the inside: one question, one failed first
approach that taught us what the observable has to be, and a named next build.
