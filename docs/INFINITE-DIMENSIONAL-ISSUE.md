# The infinite-dimensional issue — what the engine must find

Status: 2026-11-22, the discovery target Rob set. The boundary that stops every finite-lattice result:
the actual Faddeev–Popov operator and the transfer operator act on the **infinite-dimensional**
gauge-field space, and no finite truncation establishes their spectral properties. This file names
the precise gap and the candidate structures that could bridge it.

## The gap (one sentence)

A finite-dimensional matrix (the lattice FP operator, the lattice transfer matrix) has a spectrum that
is a **lattice artifact** (the UV cutoff `λ_min/a² → ∞`); the required property — the Gribov horizon,
the mass gap — is a statement about the **infinite-dimensional operator**'s spectrum, which the finite
matrix does not determine.

## The candidates (what the engine searches, each falsifiable)

| structure | what it would provide | falsifier |
|---|---|---|
| **spectral / norm-resolvent convergence** | the lattice operator converges to the continuum operator in norm-resolvent sense as `a → 0`, so `λ_min(a)` has a genuine `a → 0` limit | `λ_min(a)` has no convergent limit (it diverges — the observed `λ_min/a²` blow-up) |
| **Gribov–Zwanziger continuum** | the horizon as an infinite-dimensional fixed point of a self-consistency equation on the gauge-field space | the fixed-point equation is only stated on a finite truncation, never on the full space |
| **constructive QFT (infinite-volume / Balaban)** | the scale-by-scale infinite-volume limit that carries the operator's spectrum to the continuum | the scale sum stops at a finite volume / coupling |
| **infinite-dimensional Perron–Frobenius (Jentzsch / Krein–Rutman)** | a positive, compact, irreducible operator has a simple positive leading eigenvalue — the infinite-dim generalisation of the finite transfer-matrix gap | the operator fails positivity / compactness / irreducibility on the infinite-dim space |

## What the harvest already surfaced

- The lattice FP spectrum is well studied ([Landau-gauge ghost/gluon propagators and the FP spectrum, hep-lat/0511053](https://export.arxiv.org/pdf/hep-lat/0511053v1)); a spectral gap for lattice YM via [Jentzsch's theorem](https://zenodo.org/records/19497901) is recorded; the [Gribov horizon in the continuum](http://vietnam.in2p3.fr/2004/trans/ps4_greensite.pdf) is the actual infinite-dim object.
- The recurring honest obstacle: the finite→infinite step is the **spectral convergence** of the operator, and it is the exact place the lattice `λ_min ≈ 2.4` (UV cutoff) fails to be a horizon.

## The engine's job (search, not manufacture)

Harvest the specific **norm-resolvent convergence** theorem (or its failure) for the lattice FP operator
and the transfer operator, and the **infinite-dimensional Perron–Frobenius/Krein–Rutman** theorem that
would replace the finite matrix inequality. Each is a falsifiable hypothesis: if the operator's
`a → 0` limit diverges or fails positivity/compactness, that is the honest refutation of that bridge.

## Status of the two falsifiable questions (2026-11-22)

1. **FP operator — norm-resolvent convergence: REFUTED.** The lattice data is decisive: `λ_min(a) ≈ 2.4`
   is flat while `λ_min/a² → ∞` as `a → 0` (the UV cutoff). So the FP spectrum has **no finite continuum
   limit** — the norm-resolvent bridge fails for the FP operator, exactly as the finite-N run showed.
2. **Transfer operator — compactness + positivity (Jentzsch/Krein–Rutman): OPEN.** The temporal transfer
   operator is the compact, positivity-improving candidate, so the gap could come from Jentzsch. The
   falsifiable question is whether the *continuum* transfer operator is compact and positivity-improving
   — this is the actual infinite-dimensional object, and it is not yet established (the finite matrix
   does not answer it).

So the frontier has moved from "the FP horizon" (refuted as a lattice artifact) to **"is the continuum
transfer operator a positive compact irreducible operator"** — the one question whose yes would deliver
the gap via Jentzsch/Krein–Rutman.

## Answer to question 2 (2026-11-22) — the compactness is the exact obstruction

The temporal transfer operator is `T = e^{-aH}` (the exponential of the lattice Hamiltonian). Its three
Krein–Rutman hypotheses split:

| hypothesis | finite volume | infinite volume (the continuum) |
|---|---|---|
| **positivity** (`T = T* ≥ 0`) | YES — `H` self-adjoint, bounded below, reflection positivity | YES — unchanged |
| **irreducibility** (no invariant subspace, unique vacuum) | YES — gauge-invariant sector, ergodicity | YES — unchanged |
| **compactness** (`e^{-aH}` compact ⟺ `H` has compact resolvent / discrete spectrum) | **YES** — finite-volume `H` has discrete spectrum `E_n → ∞` | **NO** — the infinite-volume `H` has a **continuous** spectrum (multi-particle states) |

So Jentzsch/Krein–Rutman **delivers the gap on finite volume** (that is the kernel-checked finite
matrix result) — but the **compactness is the exact hypothesis that dies in the infinite-volume
limit**. The continuum transfer operator is positive and irreducible but **not compact**, so the
Jentzsch bridge does not extend to it directly.

**The honest consequence:** the infinite-dimensional gap is *not* a Jentzsch corollary. It requires a
separate argument that the finite-volume gap survives the thermodynamic limit — which is precisely the
constructive-QFT / spectral-gap-in-the-limit rung, not the compact-operator rung. This is the sharpest
statement yet of where the mass-gap problem lives: **the finite-volume gap is Jentzsch; the infinite-
volume gap is the failure of compactness, and replacing it is the open mathematics.**

## The infrared bound (the target rung) — its exact structure and where it stands

The Fröhlich–Spencer–Simon / Fröhlich–Israel–Lieb–Simon infrared bound is a three-step mechanism, all
three of which are already partially in hand:

1. **Gaussian domination** — for a reflection-positive model, the partition function in an external
   field is dominated by the Gaussian (free-field) partition function: `⟨e^{Σ f·φ}⟩ ≤ e^{½ Σ f J⁻¹ f}`.
2. **The infrared bound** — the momentum-space two-point function is bounded by the free propagator:
   `Ŝ(p) ≤ 1/(2 J(p))`, `J(p) = Σ_δ (1 − cos(p·δ))`.
3. **The mass gap** — the infrared bound plus the sum rule forces the correlation's exponential decay,
   the spectral gap, with a rate **uniform in the volume** (the thermodynamic-limit survival).

**The honest status for 4D YM:** the mechanism is the right one, but it was proved for reflection-positive
*scalar* models and *Abelian* gauge theories. The non-Abelian case is blocked on two specific inputs that
are exactly the open part:

- **YM reflection positivity (OS3)** — the gauge-invariant sector is reflection-positive, but the
  gauge-fixed measure is not, so the reflection positivity must be established on the physical (gauge-
  invariant) Hilbert space, not the gauge-fixed one.
- **Gaussian domination for the gauge-invariant observables** — the infrared bound's seed, not yet
  established for the non-Abelian plaquette/Wilson-loop observables.

So the rung `fssInfraredBound` decomposes into **two concrete, falsifiable inputs** — YM reflection
positivity on the physical space, and the Gaussian domination — each of which is a named, testable
sub-lemma, and both of which are the precise place the non-Abelian infrared bound has not been closed.

## Status of the two inputs (2026-11-22) — one is already proved

1. **YM reflection positivity (OS3): DONE — Osterwalder–Seiler 1978.** The lattice gauge theory's
   measure is reflection-positive on the physical (gauge-invariant) Hilbert space; this is the standard
   theorem the constructive route invokes. So this input is a **known result**, not open — the physical
   Hilbert space carries reflection positivity, and only the gauge-fixed measure fails it.
2. **Gaussian domination for the gauge-invariant observables: OPEN.** The partition-function bound that
   seeds the infrared bound has not been established for the non-Abelian plaquette / Wilson-loop
   observables. This — not reflection positivity — is the actual remaining rung.

So the frontier sharpens again: of the two inputs, **one is already a named theorem (Osterwalder–Seiler),
and the other — Gaussian domination — is the single open sub-lemma** the mass-gap reduction now rests on.




