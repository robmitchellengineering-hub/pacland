# Come help machine-check a Theory of Everything (three pick-up-able Lean theorems)

**pacland** is a constraint-first ToE ("relations, never values") with a **kernel-checked proof arm**:
361 theorems + 138 defs across 44 Lean 4 + Mathlib files, `lake build` green, **no `sorry`/`axiom`**.
Citable snapshot: `10.5281/zenodo.24073510`. Site: https://pacland.morpheus.nz.

The four layers already proven: Mitchell's Uniqueness + the FFT degrees (flux/SM), the quantum no-go suite
(no-cloning, LOCC, CHSH = 2√2, Gleason ⇒ Born, PBR, Mermin), the matchgate even/odd split (det = Pf² at
2/4/6×6), and the geometry (entanglement = area = D^m exactly, the forced emergence). Reproduce it in one
command: `cd pacland-proof && lake build`.

## Three open theorems — each is a clean, self-contained issue

We're looking for Lean formalizers to close the three *named* frontiers. Each issue tells you exactly which
Mathlib facts to use and which one hard step remains:

- **#430 — Švarc–Milnor** (quasi-isometry `tree ≃ H²`): Mathlib already has `UpperHalfPlane/Metric.lean`
  (the hyperbolic metric + its isometries), `MoebiusAction.lean`, and `ProperAction.lean` (the proper
  action — the key hypothesis). The lemma *itself* isn't in Mathlib. Prove PSL(2,ℤ) acts properly +
  cocompactly (fundamental domain `{|z| ≥ 1, |Re z| ≤ 1/2}`), then prove-or-cite the lemma. The orbit map
  `word(s)·i` is already defined.
- **#431 — even-n Cayley** (`det A = (Pf A)²`): the recursive Pfaffian, the 2/4/6×6 cases, the
  `pfaffian_rec_2/4` reproduction, and the m=1 base are all done. Remaining: the general induction — the
  permutation → perfect-matching expansion + Plücker cross-term cancellation. Mathlib has *no* Pfaffian, so
  this is greenfield.
- **#432 — Gromov–Hausdorff convergence** (rescaled MERA cone → H²): Mathlib has `GromovHausdorff.ghDist`
  *and* its ε-approximation lemma `ghDist_le_of_approx_subsets`. Remaining: define the rescaled cone metric
  and show `ghDist (cone) H² → 0`.

## The rules (one of them, really)

`no sorry, no axiom, lake build green, one lemma per commit`. See `pacland-proof/CONTRIBUTING.md`.

## Try it without Lean first

`python -m pacland.sextant_node` — a self-contained referee serving the 28 FORCED/FREE/IMPOSSIBLE claims
and their falsifiers. Every verdict is kernel-checked or live-computed, never asserted.

---
Repo: https://github.com/robmitchellengineering-hub/pacland — issues #430, #431, #432.

