# The constraint-first conjecture — what PACLAND claims, and how to refute it

This is the theoretical statement behind the measured structure map
(`docs/structure-map.md`, `paper/structure-map.pdf`). It turns a measurement into a
*claim the field can break*, which is what makes it science rather than a report.

## The conjecture

> **In the IIB flux landscape, the only observables that are *exactly* determined
> by the flux are the topological charges — the D3 tadpole (r = 1.0, the symplectic
> pairing FᵀJH). Every observable that depends on the *moduli stabilization* —
> W₀, g_s, gauge couplings, the mass spectrum, the axions, the dilaton, the
> cosmological constant — is statistically uniform in flux (r < 0.25).**

In one line: **the landscape's only structure is what it forbids; everything it
produces is noise plus a weak scale.**

## Why it should be true (the argument, not just the measurement)

- **Topological charges** (the tadpole) are *fixed by the flux integers alone* —
  no moduli stabilization enters. So they are exact quadratic forms: r = 1.0.
- **Stabilization-dependent observables** (W₀, g_s, masses, …) are set by the
  moduli VEVs, which solve the F-term equations D W = 0. Denef–Douglas (2004) shows
  the flux superpotential is statistically uniform across the flux ensemble; the
  same uniformity inherits to every quantity derived from the stabilized moduli.
  So they are random in flux: r < 0.25.

The measurement is the *support*; the argument is the *reason*. The conjecture is
the falsifiable claim that they agree in general, not only on the 2-moduli slice we
could sample.

## The benchmark (how the field refutes it)

This is the part that makes it matter. Any future "we learned structure in the
string landscape" paper now has a number to beat:

- **Refute the conjecture** by exhibiting a flux-determined, *non-topological*
  observable with cross-validated r > 0.9 against the flux. One clean example ends
  the whole thesis.
- **Reproduce it** by running `scripts/verify_results.py` (the 9-check
  self-assertion) and confirming the structure map numbers.

Either way, the field has to engage: the structure map is a *benchmark*, not an
opinion. A learning algorithm that claims to "find" our vacuum in observables must
explain why its signal (r > 0.9) survives on the observables we measured at r < 0.25.

## The swampland connection

"The only structure is the constraint" *is* the swampland program, stated as a
measurement. The swampland conjectures (Weak Gravity, Distance, no global
symmetries) are all statements of the form "consistency *forbids* X" — i.e. the
landscape's structure lives in its constraints, not in what it produces. Our
conjecture is the *empirical* version of that premise:

- **Swampland says:** the interesting physics is in the constraints.
- **We measured:** the only structured observable is the constraint (the tadpole);
  everything else is a featureless cloud.

This is not a proof of any single swampland conjecture; it is evidence that the
constraint-first *frame* is the right one — which is what the swampland program has
claimed and the search program has denied.

## Honest scope

- Measured on the h¹²=2 KS model, 174 SUSY vacua, degree-0 spectrum, flux
  coordinates. The 2-moduli truncation is a real limit (see `AGENTS.md` TO-DO).
- The conjecture is *supported by* the measurement and *motivated by* Denef–Douglas;
  it is not yet proven for all CY geometries, all moduli, or all observables.
- Each named limit is where a refutation could hide — which is exactly why the
  benchmark is stated before the proof.
