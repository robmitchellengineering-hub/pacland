# PACLAND

> **Don't ask a complex system for its values — ask for its constraints, its count, and its
> deficit. Everything else is covariance, not knowledge.**

**Probably Approximately Correct Landscape** — a Valiant-verification system, applied
one field at a time. The string landscape (with a **proven theorem tower** and a
**Standard-Model frontier**) is the founding discipline; **climate** is the first
expansion. Live: [pacland.morpheus.nz](https://pacland.morpheus.nz) · `pip install pacland`

## Disciplines — one verification spine, many fields

| discipline | status | what it holds |
|---|---|---|
| **String landscape** | core (built) | PAC verification of the flux landscape + Standard Model |
| **Climate / Earth-system** | built — deficit + guard-suite | `docs/climate-verification-deficit.md` · `pacland climate` |
| Drug discovery / protein science | built — deficit + guard-suite | `docs/drugs-verification-deficit.md` · `pacland drugs` |
| Economics / macro-finance | built — models scored on the physics bar | `docs/economics-model-roster.md` (6 named models, bar-scored) · real-time Meese–Rogoff runs · `pacland economics` |
| Epidemiology / disease modelling | queued | identifiability as the underdetermined wall |
| AI safety / capability verification | queued (parallel lane) | the verification machine aimed at model claims |

Each discipline is its own thing — own subpackage, docs, and CLI command — sharing one
spine (two-level certificate, verification deficit, constraint-first, four-walls map).

**How a new field gets figured out:** [`docs/verify-bar.md`](docs/verify-bar.md) (the bar, and
the climate transfer test) and [`docs/SOP-FIGURING-SYSTEMS-OUT.md`](docs/SOP-FIGURING-SYSTEMS-OUT.md)
— the method, written after applying it to macro-finance: count constraints by rank rather
than by list, source and classify every one, derive the reference point, fetch the source,
seed a fault under every guard, and put the null in every table.
The registry is `src/pacland/disciplines.py`; list them with `pacland disciplines`.

## The result, in one sentence

> **A theory of everything predicts nothing exactly except what it *forbids*
> (constraints) and what it is *handed* (labels).** In the flux sector this is now a
> **proven theorem**: the D3 tadpole is the *unique* exact structure, so no exact,
> polynomial, duality-invariant flux function can single out a vacuum. That is a
> no-go on *exact invariant* selectors only — it does not rule out statistical,
> moduli-dependent, or non-polynomial selection, and `N ≤ L` *bounds* the search
> space rather than forbidding it. In the Standard Model the same two-type
> decomposition holds, and the open question is precisely stated and falsifiable.

## The theorem tower — machine-checked

Five theorems, each verified symbolically at zero tolerance, plus a Lean 4 + Mathlib
arm that machine-checks the core:

| theorem | statement | grade |
|---|---|---|
| **Mitchell's Uniqueness** | the tadpole `N = FᵀJH` is the unique bilinear symplectic invariant | 6/6 + Lean (n=1 *and* general n) |
| **Constraint-First** | the tadpole generates the *entire* invariant ring (Weyl's FFT, k=2) | 5/5 degrees |
| **Mitchell's Completeness** | `N` is a *complete* invariant (same tadpole ⟺ dual-equivalent) | 6 exact + 2 numeric |
| **Full-duality** | holds for Sp(b₃) × SL(2,ℤ), not just Sp | 5/5 |
| **Complete Exact Structure** | the ToE's exact content = constraints + labels, nothing else | assembly |

One command reproduces the tower: `python3 scripts/validate_all_theorems.py`.
Machine-checked arm: `cd pacland-proof && lake build` (no `sorry`/`axiom`/`native_decide`).

## The Standard-Model frontier — constraint-first, one sector up

The SM's exact structure decomposes exactly like the flux sector's, and it's now partly
*proven*:

| type | flux (proven) | Standard Model |
|---|---|---|
| constraint | tadpole `N ≤ L` | anomaly cancellation, charge quantization |
| label | `h¹¹, h²¹, c₂, κ` | gauge group; N_gen = 3 (topological) |
| parameter | W₀, g_s, couplings, Λ | the 19 free couplings |

- **Anomaly cancellation is a constraint** (5/5 exact) — the hypercharges are *forced*.
- **Hypercharge is unique** (4/4 exact) — the gauge-sector analog of Mitchell's Uniqueness.
- **The 19 = the orbit-space dimension** of the flavor group — the independent invariants.

Two research fan-outs refined the open claim (see `docs/sm-conjecture-notes.md`,
`docs/sm-floor-notes.md`):

> **A ToE predicts *relations* (invariants), never *values*.** And the "floor" is not
> one number but a structure: **0 continuous, 1 discrete (the tadpole), 19 relations** —
> with the 19 relations generable from fewer UV parameters.

## The methodology

- **The Rule of Three** — no claim from one test; three independent confirmations must agree.
- **Use the wall, don't hit it** — "uncomputable" is four walls, each with a way around.
- **Mirror symmetry** — a free validation target (h11 ↔ h21, χ → −χ).
- **Research fan-out** — parallel independent passes on a sharp question, then
  compare-notes (`docs/research-fanout.md`); it has caught two conflations so far.

## Papers (four)

- `paper/constraint-first-theorem.pdf` — Mitchell's Uniqueness → Complete Exact Structure (the theorems)
- `paper/structure-map.pdf` — the measurement that motivated the theorem
- `paper/fingerprint.pdf` — the mass spectrum carries no fingerprint
- `paper/PACLAND-preprint.pdf` — the verification discipline (umbrella)
- `paper/constraint-first-explainer.pdf` — the investor/partner explainer

**Published:** the flagship theorem paper is on Zenodo with a permanent DOI —
[`10.5281/zenodo.23497239`](https://doi.org/10.5281/zenodo.23497239)
(open access, CC BY 4.0).

## CLI

```sh
pip install pacland
pacland limits            # the boundary map (four walls)
pacland deficit           # the Mitchell Verification Deficit (m = 9)
pacland mine data.json    # classify observables: structured vs random
pacland constrain data.json
pacland solve data.json   # constraint-first: the certified viable class
pacland viable data.json  # the viability polytope
pacland climb             # run the deficit climber on the mesh
```

## Tests

```sh
python3 -m unittest discover -s tests   # 731 tests
```

## Honest frontier

- **Lean transitivity** (Mitchell's Completeness) is the one theorem not yet
  machine-checked.
- **The SM "floor"** — can the 19 invariants be generated from fewer than ~14 UV
  parameters? The decisive test (express the invariants as functions of moduli, check
  the Jacobian rank) is the next fan-out.
- **arXiv** — the four papers are ready, pending account + hep-th endorsement
  (`docs/arxiv-submission.md`). Priority is already secured by the Zenodo DOI above.
