# PACLAND

**Probably Approximately Correct Landscape** — a Valiant-verification system for the
string landscape. Live: [pacland.netlify.app](https://pacland.netlify.app) ·
`pip install pacland`

## The result, in one sentence

> **The landscape's only exact structure is what it *forbids* — the constraint.**
> Everything it produces (couplings, masses, phases, the cosmological constant) is
> noise plus a weak scale; no observable carries the geometric fingerprint a search
> would need. So no search can find our vacuum in observables — the only navigable
> move is elimination by verified constraint.

That is the **constraint-first theorem**, established by measurement on real
supersymmetric flux vacua and stated as a paper:
[`paper/structure-map.pdf`](paper/structure-map.pdf).

## What is measured (the structure map)

Every flux-determined observable, classified by a joint learnability test gated by a
positive control (the tadpole must come back r = 1.0):

| observable | r | verdict |
|---|---|---|
| **tadpole N_flux** | **1.00** | **exact** — the symplectic pairing FᵀJH |
| W₀ | 0.62 | weakly learnable (scale via the tadpole) |
| saxions | 0.30–0.42 | weakly learnable (stabilization) |
| g_s, gauge couplings, mass-shape, axions, dilaton, AdS V | < 0.25 | uniform |

## The headline results

- **The Mitchell Verification Deficit** — the count `m` of observables simultaneously
  measured + computable + validated. It read ∞ (vacuous) and has been **climbed to
  m = 5**: CYTools topology (h11, h21, c2, κ) = 4, JAXVacua tadpole = 1. The SM-physics
  sector is the open frontier (m = 0).
- **Search over W₀ is hopeless** — by *rarity + extrapolation*: the KKLT target sits
  ~20 prediction-errors outside the observed range.
- **The mass spectrum carries no fingerprint** — its shape is uniform in flux
  ([`paper/fingerprint.pdf`](paper/fingerprint.pdf)).
- **The no-scale theorem confirmed** — SUSY vacua sit at V = 0 to machine precision.

## The methodology (this is the point)

- **The Rule of Three** — no "structured vs. random" claim from one test. Three
  independent confirmations must agree (single-coordinate MI, joint ridge-quadratic
  CV r, permutation null). This rule caught and corrected our own W₀ over-reach.
- **Use the wall, don't hit it** — "uncomputable" is four walls (intractable /
  unmeasurable / underdetermined / undecidable), each with a way around; the way
  around *is* the result.
- **Mirror symmetry** is a free validation target (h11 ↔ h21, χ → −χ).

Every headline number is reproducible: `python3 scripts/verify_results.py`
regenerates and asserts all of them from committed data.

## Papers

- [`paper/PACLAND-preprint.pdf`](paper/PACLAND-preprint.pdf) — the verification discipline
- [`paper/fingerprint.pdf`](paper/fingerprint.pdf) — the mass spectrum carries no fingerprint
- [`paper/structure-map.pdf`](paper/structure-map.pdf) — the constraint-first theorem

## CLI

```sh
pip install pacland
pacland limits            # the boundary map (four walls)
pacland deficit           # the Mitchell Verification Deficit (m = 5)
pacland mine data.json    # classify observables: structured vs random
pacland constrain data.json
pacland solve data.json   # constraint-first: the certified viable class
pacland viable data.json  # the viability polytope
pacland climb             # run the deficit climber on the mesh
```

## Tests

```sh
python3 -m unittest discover -s tests   # 119 tests
```

## Honest frontier

The next `m` requires the **Kähler-moduli mass spectrum**, which needs instanton
corrections — diagnosed as an XLA autodiff hang (not physics, not data), with the
shortcut specified (finite-difference the Kähler metric + the 2-term instanton
superpotential) and the conifold limit as the alternative geometry. See
`docs/boundary-map.md` and `docs/structure-map.md`.
