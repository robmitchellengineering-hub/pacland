# Mass-gap theorem audit — what is real vs what must NOT go in the paper

The Clay paper must carry only **real** results. Anything that types a constant in as a `def` and
calls it "derived", or defines two things equal and proves their ratio is 1, is excluded. This file
is the exclusion list.

## The five-way classification

- **REAL** — the result follows from a computation or a proof, not from a definition. ✅ in the paper.
- **CONDITIONAL** — the theorem is valid, but its *hypothesis* (e.g. "the gap scales as e^{-cβ}") is
  assumed, not proven. ⚠️ in the paper ONLY with the hypothesis stated explicitly as an assumption.
- **DEFINITIONAL** — a `def` plus algebra; the number was typed in, not computed. ❌ out.
- **TAUTOLOGICAL** — defines two things equal and proves their ratio is 1. ❌ out.
- **TRIVIAL** — an identity like `i² = −1`, presented as if it were the deep theorem. ❌ out.

## The exclusions (what must NOT be claimed as results)

| file | theorem | class | why |
|---|---|---|---|
| `SpacingUniform.lean` | `spacing_uniform_exact` | TAUTOLOGICAL | defines `latticeGap = latticeSpacing = e^{-cβ}`, proves ratio = 1 |
| `MassGapJoin.lean` | `mass_gap_join` | TAUTOLOGICAL | defines `massGap = runningSpacing = e^{-cβ}`, proves ratio = 1 |
| `MassGapJoin.lean` | `mass_gap_join_strong` | TRIVIAL | `e^0 = 1` |
| `WickRotation.lean` | `wick_rotation_metric` | TRIVIAL | `(i·t)² + x² = x² − t²` is `i² = −1`, not the OS analytic continuation |
| `WickRotation.lean` | `wick_rotation_involutive` | TRIVIAL | `i·(i·t) = −t` |
| `OneLoopBeta.lean` | `oneLoopBeta` | DEFINITIONAL | `def oneLoopBeta N = 11N/(48π²)` — the number is typed, not computed |
| `OneLoopBeta.lean` | `asymptoticFreedomExponent_eq` | DEFINITIONAL | algebra on the typed constant |
| `OneLoopBeta.lean` | `su2_exponent_derived` | DEFINITIONAL | arithmetic on the typed constant |
| `AsymptoticFreedom.lean` | `betaFunctionCoefficient` | DEFINITIONAL | `def ... = 11N/(48π²)` — the beta-function is asserted, not derived |
| `AsymptoticFreedom.lean` | `su2_exponent` | DEFINITIONAL | `c = 12π²/11` by definition + arithmetic |

## What IS allowed, and how it must be labelled

- `SpacingUniform.lean` `spacing_uniform` — **CONDITIONAL** (real lemma): *if* `m(β)` and `a(β)` are
  each bounded by `C·e^{-cβ}`, *then* `m/a` is bounded by `C₁/C₄ ≤ m/a ≤ C₂/C₃`. In the paper ONLY as
  "given the scaling hypothesis, the physical mass is bounded" — never as "the scaling is proven."

## The paper rule

1. Every theorem in the paper must carry a class tag; only **REAL** and clearly-labelled **CONDITIONAL**
   statements are cited as results.
2. No constant may appear on the right of a `def`/`let` and then be called "derived".
3. The exponent `c` is cited as a **value** (not a derived relation) unless a loop integral or heat-kernel
   coefficient is actually computed and `11N/48π²` falls out as its output.
4. The two genuinely-open rungs (the full-lattice collective instanton, and the OS⟹Wightman
   reconstruction) are stated as **open**, not as "scaffold = done".
