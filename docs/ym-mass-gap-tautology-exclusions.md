# Mass-gap theorem classification — state it, don't delete it

The tautologies are **scaffolding**: definitions, conventions, normalizations and consistency
checks. They are useful and belong in the paper — in a clearly-labelled **"definitions and
conventions"** section, never in the **"results"** section. The only error is mislabelling a
definition as a result. This file is the classification that keeps the two apart.

## The five-way classification (with the correct home for each)

- **REAL** — a theorem that follows from a computation or proof. -> **Results** section.
- **CONDITIONAL** — a valid lemma whose hypothesis (e.g. "the gap scales as e^{-cβ}") is assumed.
  -> **Results**, with the hypothesis stated explicitly as an assumption.
- **DEFINITION** — a `def` naming an object or a cited constant. -> **Definitions & conventions**.
- **NORMALIZATION / CONSISTENCY** — a ratio or identity that fixes units or checks consistency.
  -> **Definitions & conventions**, stated as "we set …" / "… checks out".
- **SETUP** — an identity (e.g. `i² = −1`) that prepares a construction. -> **Definitions & conventions**.

## The classification (what each thing actually is, and where it goes)

| file | theorem | class | correct statement |
|---|---|---|---|
| `AsymptoticFreedom.lean` | `betaFunctionCoefficient` | DEFINITION | "we define b₀ = 11N/48π² (the GWP one-loop value)" |
| `OneLoopBeta.lean` | `oneLoopBeta` | DEFINITION | same — a cited constant, not a derivation |
| `OneLoopBeta.lean` | `asymptoticFreedomExponent_eq`, `su2_exponent_derived` | DEFINITION | algebra on the definition |
| `SpacingUniform.lean` | `latticeSpacing`, `latticeGap` | DEFINITION | "we define the spacing and gap to run as e^{-cβ}" |
| `SpacingUniform.lean` | `spacing_uniform_exact` | NORMALIZATION | "in units of Λ_QCD the physical mass is 1" |
| `MassGapJoin.lean` | `mass_gap_join` | NORMALIZATION | "the gap and spacing share the same exponent, so their ratio is the unit scale" |
| `WickRotation.lean` | `wick_rotation_metric`, `wick_rotation_involutive` | SETUP | "the imaginary-time substitution maps Euclidean to Lorentz signature" |
| `SpacingUniform.lean` | `spacing_uniform` | CONDITIONAL | "given the scaling hypothesis, m_phys is bounded" |

## The paper rule (state it, don't delete it)

1. The paper has two sections: **Definitions & conventions** and **Results**.
2. Every definition / normalization / setup goes in the first, worded as "we define …" or "we set …"
   or "we cite …" — never as "we prove …".
3. Only REAL and clearly-labelled CONDITIONAL theorems go in **Results**.
4. A constant typed into a `def` is a **definition**, not a derivation; say "cite" not "derive".
5. The two open rungs (full-lattice collective instanton, OS⟹Wightman reconstruction) are stated as
   **open**, not "scaffold = done".
