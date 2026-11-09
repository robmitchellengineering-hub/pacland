# pacland-proof — the kernel-checked theorem arm of the constraint-first ToE

> **Relations never values.** The only exact structure in nature is the **constraint**. Everything
> else that is exact is either **FORCED** (a theorem), **FREE** (a label with no exact value), or
> **IMPOSSIBLE** (a no-go). Nothing exact is derived from below — it is delimited from above, by what
> cannot be otherwise.

This directory is the **machine-checked proof** of that claim: Lean 4 + Mathlib, **361 theorems and
138 definitions across 44 files**, `lake build` green, **no `sorry`/`axiom`/`admit`** anywhere. A
stranger can reproduce the whole thing in one command (`lake build`) and confirm the kernel checked
every statement.

- **Site:** https://pacland.morpheus.nz
- **Repo:** https://github.com/robmitchellengineering-hub/pacland (branch `foundations/qf0-hinge-ledger`)
- **Citable snapshot (Zenodo):** [`10.5281/zenodo.24073510`](https://doi.org/10.5281/zenodo.24073510)
- **Theorem index:** `THEOREM-INDEX.md` (every theorem, by file)

## The four layers (what is proven)

| layer | the exact structure it forces | files |
|---|---|---|
| **flux / SM** | Mitchell's Uniqueness (FᵀJH is the *unique* bilinear symplectic invariant), the FFT degrees 1–4, N_gen = 3 = \|χ\|/2, the SM 19 | `Mitchell.lean`, `General.lean`, `Degree*.lean`, `Transitivity.lean`, `SM/` |
| **quantum** | no-cloning, no-broadcasting, LOCC cannot entangle (IMPOSSIBLE); CHSH = 2√2, Bell = 2, Gleason ⇒ Born, PBR, Mermin (FORCED) | `QM/CHSH.lean`, `QM/NoCloning.lean`, `QM/Entanglement.lean`, `QM/Tsirelson.lean`, `Foundations/` |
| **matchgate** | det = Pf² at 2×2, 4×4, 6×6; the recursive Pfaffian; general odd → det = 0 | `QM/Matchgate.lean` |
| **geometry** | the MERA cone is 0-hyperbolic with exponential volume; **entanglement = area = D^m EXACTLY**; the hyperbolic geometry is **forced**; the Stern-Brocot/Farey map into H² | `QM/MERA.lean`, `QM/Hyperbolic.lean`, `QM/HyperbolicPlane.lean`, `QM/HyperbolicMetric.lean`, `QM/SternBrocot.lean`, `QM/FareyTree.lean` |

## Build it (one command)

```
cd pacland-proof
lake build          # needs elan + a mathlib v4.35 cache; ~7 GB in .lake
```

`lake build` succeeding *is* the verification: the Lean kernel has accepted every `theorem`, and
there is no `sorry`/`axiom` to silently assume anything. Grep to confirm:

```
grep -rn "sorry\|axiom\|admit" PaclandProof/    # should return nothing
```

## The honest frontiers (named, not proven — here is where help is wanted)

The claim is kernel-checked *up to these*, which are standard theorems we cite rather than fake:

- **Švarc–Milnor** — the full quasi-isometry `Stern-Brocot tree ≃ H²` (PSL(2,ℤ) acts cocompactly on ℍ).
- **the Gromov–Hausdorff convergence** — the rescaled cone → smooth H² (the *definition* `GromovHausdorff.ghDist` is in Mathlib; the *proof* is open).
- **the general even-n Cayley** — `det = Pf²` for all even n (2/4/6×6 + the recursive Pfaffian are done; the matching induction is open).
- **the full AdS/CFT duality** — Maldacena's 25-year-open conjecture.

## Contribute

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the sharded work items, the "good first issues", and the
one-rule discipline: **no `sorry`, no `axiom`, `lake build` green, one lemma per commit.**
