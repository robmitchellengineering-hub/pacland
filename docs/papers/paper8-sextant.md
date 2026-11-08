# SEXTANT: a kernel-checked referee for quantum and physical claims (FORCED / FREE / IMPOSSIBLE)

**The executable form of the constraint-first theory of everything**

*Author: Rob Mitchell · the pacland proof arm · Date: 2026-11-09 · Repository: `pacland/` (proofs in `pacland-proof/`)*

**Abstract.** SEXTANT is a **kernel-checked referee** that classifies claims about quantum and physical
systems into exactly three verdicts — **FORCED** (a theorem: the claim is the only consistent option),
**FREE** (a label: a value nothing forces), or **IMPOSSIBLE** (a no-go: the claim contradicts a checked
constraint) — and it **never predicts values**. It is the executable form of the constraint-first program:
*don't ask a complex system for its values; ask for its constraints, its count, and its deficit — everything
else is covariance, not knowledge.* The referee holds a catalog of **28 claims** — CHSH ≤ 2√2 (Tsirelson),
Clifford circuits classically simulable, matchgates = Pfaffians (the even/odd split), no-cloning, the MERA
area law `D^m`, Mermin contextuality, the SM's anomaly cancellation and 19 free parameters, the D3-tadpole
uniqueness theorem, and more — each with a theorem name (a Lean 4 + Mathlib certificate, no `sorry`/`axiom`)
and a **falsifier** (the minimal observation that would refute it). A **falsifier loop** runs every claim's
falsifier against a live oracle (a simulated quantum computer, `phantom.py`: state-vector, Stim, Quimb) and
reports SURVIVES/REFUTED, so no verdict is asserted, only executed. A **hypothesis registry** holds the 11
open questions, each decomposed into what is *forced* vs what is *open*, with candidate answers and their
falsifiers — 6 of them answered or closed this arc. And the **SEXTANT node** (`web/node.html` +
`src/pacland/sextant_node.py`) is a self-contained, no-harness app anyone can download to browse claims, run
falsifiers, contribute a discovery, and point at their own model — the contributor door, with no server in
the middle. `python scripts/validate_sextant.py` reports `catalog OK: 28 claims`, with the CHSH control exact
at 2√2 and the classical wall exact at 2.

## 1. What this is — a referee, not an oracle

A theory of everything that *predicts values* is the thing the constraint-first program argues cannot exist:
the exact content of physics is **constraints** (tadpole, anomaly cancellation, no-cloning, …) plus
**labels** (N_gen = 3, the 19 couplings, G) — and the values are free, not forced. SEXTANT operationalises
that distinction as a classifier with three exhaustive verdicts:

- **FORCED** — a *theorem*. The claim is the unique consistent option, kernel-checked in Lean 4 + Mathlib
  (e.g. CHSH ≤ 2√2, Clifford simulability, matchgates = Pfaffians).
- **FREE** — a *label*. A value nothing forces; every consistent assignment is allowed (e.g. the
  gravitational coupling G, N_gen = 3, the 19 SM parameters).
- **IMPOSSIBLE** — a *no-go*. The claim contradicts a checked constraint (e.g. no-cloning, no-broadcasting,
  a non-contextual value assignment to the Mermin square).

The referee **never predicts values** — that is the point. It only says where each claim sits relative to the
constraints. A claim's verdict is not a matter of authority: every claim carries a theorem name and a
falsifier, and the falsifier loop (§3) runs the falsifier, so the verdict is executed, not asserted.

## 2. The catalog — 28 claims, three verdicts

`src/pacland/sextant.py` (`CATALOG`) holds 28 claims, each with `claim`, `theorem` (the Lean certificate),
`falsifier`, `oracle`, `verdict`, and `why`. The verdict breakdown is 21 FORCED, 3 FREE, 4 IMPOSSIBLE:

| verdict | count | representative claims |
|---|---|---|
| FORCED | 21 | CHSH ≤ 2√2 (`QM.Tsirelson`), Clifford polynomial (`QM.Stabilizer`), matchgates = Pfaffians (`QM.Matchgate`), MERA area law + hyperbolic cone (`QM.MERA` + `QM.Hyperbolic`), the Born rule (Gleason), gravity must be quantum, Lovelock uniqueness, ADM constraints, hypercharge uniqueness, anomaly cancellation, tadpole uniqueness (`Mitchell`), PBR, PR-box at 4 |
| FREE | 3 | the coupling G (`coupling-free`), N_gen = 3 (`generation-free`), the 19 parameters (`the-19`) |
| IMPOSSIBLE | 4 | no-cloning, no-broadcasting, Mermin contextuality (no ±1 assignment), LOCC cannot create entanglement |

Examples, to fix the idea:

- **FORCED — CHSH.** `chsh`: "no quantum state violates the CHSH inequality beyond 2√2", theorem
  `QM.Tsirelson`, falsifier "a state exceeding 2√2". The live oracle (`phantom.chsh_value`) computes
  `S = 2√2` exactly for the Bell state under the four optimal settings; the classical wall is 2
  (`QM.CHSH`/Bell), so the free column is the gap `[2, 2√2]` — the entanglement that LOCC cannot create.
- **FREE — the coupling.** `coupling-free`: "the gravitational coupling G is not derived", theorem
  `Gravity.QG.coupling_free`, falsifier "a derivation of G from the forced halves". ∇·G = 0 involves no κ,
  so the Einstein equation is consistent for every κ ≠ 0 — G is a label, like N_gen and the 19.
- **IMPOSSIBLE — no-cloning.** `no-cloning`: "no machine clones an arbitrary quantum state", theorem
  `QM.NoCloning`, falsifier "a universal cloner". Linearity + unitarity forbid the map
  |ψ⟩|0⟩ → |ψ⟩|ψ⟩ for all |ψ⟩.

## 3. The falsifier loop — every claim names and runs its falsifier

A claim is only as strong as its falsifier, and a falsifier that is never run is a number, not evidence.
SEXTANT therefore couples each live claim to a **falsifier that runs** (`phantom.FALSIFIERS`):

- `verify_chsh` — computes the Bell-state CHSH value and checks nothing exceeds `2√2`.
- `verify_clifford` — runs a 1000-qubit H/CNOT Clifford circuit in Stim and checks it stays polynomial
  (no `2^n` blowup; the T gate is the single escape).
- `verify_mermin` — computes the nine-observable Mermin–Peres square and checks rows = +I while column 3 = −I.
- `verify_bell` — exhausts all deterministic local strategies and checks the classical wall is 2.
- `verify_mera` — builds a random MPS and checks the central-cut entropy obeys the area-law bound log D.
- `verify_hyperbolic` — exhausts all quadruples of 4-bit strings and checks the four-point (0-hyperbolicity)
  condition holds.

`python -m pacland.sextant --verify` runs all of them and reports `n/28 claims survive their falsifier`;
`python -m pacland.sextant verify <claim>` runs one. The Lean certificates prove the falsifier *impossible*
for the kernel-checked claims (no live oracle needed); the live oracles prove it *empirically* for the
simulable ones.

## 4. The hypothesis registry — 11 open questions, 6 answered this arc

`src/pacland/hypotheses.py` holds the **open** questions, each decomposed constraint-first into what is
*forced* (kernel-checked) vs what is *open*, with candidate answers each carrying its own falsifier:

- `ads-limit` — does the MERA cone's graph metric converge to the smooth AdS metric? (discrete half complete;
  the smooth GH-limit gated on a DG stack).
- `separation-classes` — which circuits beyond Clifford are simulable? (matchgate even/odd split now
  kernel-checked).
- `cayley-even-n` — does det A = Pf(A)² for every even n? (**6×6 closed** this arc; the general induction
  remains).
- `which-2` — gauge unification collapses exactly 2 of the 19 — which two? (**ANSWERED**: the gauge couplings).
- `ngen-3` — why 3 generations? (**ANSWERED**: N_gen = |χ|/2, a free label, not a forced value).
- `mera-lung` — is the MERA cone and the lung the same exponential-branching object? (**ANSWERED**,
  theoretically + Weibel's model).
- `swampland-new` — which swampland conjectures become theorems beyond T⁶? (**ANSWERED** on T⁶, quintic a
  compute task).
- `npu-contraction` — does the ROG's NPU accelerate tensor contraction? (**CLOSED**, measured dead end).
- `t-count-boundary`, `morpheos-rust-service`, `quantum-ready-crypto` — open (T-count threshold, the native
  Rust falsifiers, the post-quantum crypto audit).

The research move is the same everywhere: run the falsifiers, keep the hypotheses that survive — the
surviving set *is* the new relation.

## 5. The node — the contributor door

`src/pacland/sextant_node.py` + `web/node.html` is a self-contained, no-harness app: `python -m
pacland.sextant_node` serves `http://127.0.0.1:8090`, and anyone can download it, browse the 28 verdicts,
run a falsifier (`/api/verify`), read the open-question registry (the "global quest"), **contribute a
discovery** (a pre-filled GitHub "new file" URL opens a PR into `proofs/` — no git needed), and point the
node at their own OpenAI-compatible model to attack a quest. Every verdict a visitor reads is kernel-checked
(Lean) or live-computed (Phantom), never asserted.

## 6. What is NOT claimed (honest)

- **No value prediction.** SEXTANT classifies, it never predicts. FORCED/FREE/IMPOSSIBLE is a verdict on a
  claim's status, not a number for an observable.
- **No complete ToE.** The catalog is 28 claims; the registry is 11 questions, 6 answered. The full
  constraint-first theory — every claim classified, every question closed — is the program, not a finished
  result.
- **Certificates live in their own tree.** Each theorem name points at a Lean 4 + Mathlib proof in
  `pacland-proof/` (no `sorry`/`axiom`); the papers (`docs/papers/`) carry the full statements. SEXTANT is the
  *index*, not the proofs themselves.
- **The live oracles are simulated evidence, not proofs.** The CHSH/Clifford/Mermin/Bell/MPS numbers are
  computed by `phantom.py` (numpy/Stim/Quimb); the theorems are the proofs, the oracles are the running
  falsifiers.

## 7. Reproducibility

```
python scripts/validate_sextant.py     # → "catalog OK: 28 claims, CHSH control exact (2√2), ..."
python -m pacland.sextant --list       # the 28 verdicts
python -m pacland.sextant --verify     # run every falsifier
python -m pacland.sextant_node         # the node — http://127.0.0.1:8090
```

Sources: `src/pacland/sextant.py` (catalog + classifier), `src/pacland/phantom.py` (the simulated quantum
computer + falsifiers), `src/pacland/hypotheses.py` (the open-question registry), `src/pacland/sextant_node.py`
+ `web/node.html` (the node), and `pacland-proof/` (the Lean certificates). The guard that fails is a guard:
`scripts/validate_sextant.py` fails if any claim is malformed, if the CHSH control drifts off 2√2, or if any
falsifier fires against its own claim.
