# Contributing to pacland-proof

The proof arm is a Lean 4 + Mathlib project. You do **not** need to be a mathematician to help — you
need to be able to write a `theorem` the kernel accepts. Here is the map.

## The one rule (non-negotiable)

```
no sorry, no axiom, no admit, no native_decide
lake build must stay green
one lemma per commit, on branch foundations/qf0-hinge-ledger
```

A theorem with a `sorry` is not a theorem — it's a placeholder, and it silently corrupts the claim
that "everything is kernel-checked". If you are stuck, **leave a TODO comment and a `theorem` statement
without a proof**, or open an issue naming the exact sub-lemma you need. Never commit a `sorry`.

## The flow

1. Fork `robmitchellengineering-hub/pacland`, branch off `foundations/qf0-hinge-ledger`.
2. `cd pacland-proof && export PATH="$HOME/.elan/bin:$PATH" && lake build` (install elan + let mathlib's v4.35 cache download).
3. Add your lemma to the right file, or a new file under `PaclandProof/QM/` (then `import` it in `PaclandProof.lean`).
4. `lake build` — it must be green, and `grep -rn "sorry\|axiom\|admit" PaclandProof/` must return nothing.
5. Open a PR against `foundations/qf0-hinge-ledger`.

## The sharded work, by size

### Hard (the frontier — the three named open theorems)

| item | statement | where |
|---|---|---|
| **Švarc–Milnor** | the Stern-Brocot tree (via `FareyTree.fareyPoint`) is quasi-isometric to H²: PSL(2,ℤ) acts cocompactly on ℍ | new file, needs the group action + cocompactness |
| **even-n Cayley** | `det A = (Pf A)²` for every even-dimensional antisymmetric `A` | `QM/Matchgate.lean` has the recursive `pfaffian`; the general induction needs the perfect-matching / Plücker cancellation |
| **GH convergence** | the rescaled MERA cone → H² in the Gromov–Hausdorff sense (use Mathlib's `GromovHausdorff.ghDist`) | new file |

### Medium (self-contained, clear statements)

- **the Farey child lemmas** — prove `fareyPoint (p ++ [false]) = L (fareyPoint p)` and the `[true]` analogue (`FareyTree.lean` already defines `word`/`fareyPoint`).
- **the symmetry dictionary** — `AdSCFT.lean` has the Möbius action `mobius`; prove it is a group action (composition matches matrix multiplication), the CFT side of AdS/CFT.
- **the matchgate general det** — `det_fin_five` and a general `det_fin_(n)` reduction in `QM/Matchgate.lean`.

### Good first issues (small, the fastest way to prove you can do it)

- a small trig/hyperbolic bound in `QM/HyperbolicPlane.lean` (e.g. `sinh x ≤ exp x` for `x ≥ 0` — already done; find the next one).
- a `Fin`-summation simplification lemma (`Fin.sum_univ_four`, `Fin.sum_univ_five`).
- a `List` lemma for the Stern-Brocot encoding (e.g. `rational` of a reversed path).

## The SEXTANT download node (run the claims without Lean)

You don't need the Lean build to *see* what's claimed. The self-contained referee runs anywhere:

```
python -m pacland.sextant_node      # serves http://127.0.0.1:8090
```

It serves the 28-claim FORCED/FREE/IMPOSSIBLE catalog, the "run the falsifier" button, the open-question
registry (the global quest), and the "contribute a discovery" flow. Every verdict is kernel-checked (Lean)
or live-computed (Phantom), never asserted. This is the contributor door — download, run, click, add.

## Where the claim is recorded

- `../docs/TOE.md` — the consolidated ToE statement (the four layers, the scoping, the frontiers).
- `../docs/ads-cft-plan.md` — the AdS/CFT plan and its honest corrections.
- `THEOREM-INDEX.md` — every theorem, by file.
- Zenodo `10.5281/zenodo.24073510` — the versioned proof-arm snapshot.
