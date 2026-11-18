# Retrodiction test — does the jump-seeking loop beat a baseline?

The five-type taxonomy is retrospective until this passes. The test: run the loop **blind** on historical
problems with the jump withheld, and compare it against the **same pipeline without the taxonomy**.

## Design

- **Arms.** (a) TAXONOMY: generate candidates via the five typed questions; (b) BASELINE: generate
  candidates with the same budget but *untyped* ("propose hypotheses for this anomaly"). Everything else —
  model, falsifier, budget — identical. Only the *prompt structure* differs.
- **Metric.** For each historical problem, both arms emit a *ranked* candidate list. Score per arm:
  (1) rank of the true jump (lower = better); (2) falsifier-cost to reach it (cheaper = better);
  (3) count of surviving non-jump candidates (a tax of false positives). The taxonomy **helps** iff it
  beats baseline on (1)+(2) at fixed (3), across N problems, at a significance level agreed in advance.
- **Blind + no hindsight leakage.** The problem statement is reconstructed from the *pre-jump* literature
  only. The true jump and its post-discovery vocabulary must NOT appear in any prompt. The scorer is a
  fixed rubric (the jump's canonical statement, applied identically to both arms) — never a human reading
  "does this look like Planck?".

## Starter dataset (pre-jump state given, jump withheld)

| # | Problem (pre-jump state) | Withheld jump |
|---|---|---|
| 1 | Blackbody spectrum diverges at short wavelength (Rayleigh–Jeans) | energy quantisation `E = hν` |
| 2 | Photoelectric threshold depends on frequency, not intensity | light quanta (Einstein 1905) |
| 3 | Mercury's perihelion precesses 43"/century beyond Newton | GR / spacetime curvature |
| 4 | Ampere's law is inconsistent with charge conservation | Maxwell's displacement current |
| 5 | Michelson–Morley finds no aether drift | Lorentz invariance / SR |
| 6 | Spectra of atoms are discrete, not continuous | Bohr quantisation (then QM) |
| 7 | β-decay appears to violate energy conservation | the neutrino (Pauli) |
| 8 | The anomalous Zeeman effect (half-integer splittings) | electron spin |
| 9 | Strong interactions preserve isospin but not locality | non-abelian gauge symmetry (Yang–Mills) |
| 10 | Weak+EM couplings look unrelated at low energy | electroweak unification |

Each entry gets a `pre-state` file (the anomaly + what was known, dated), a `withheld` file (the jump),
and a `confirm` file (the post-jump prediction that closed it). The scorer checks only `withheld`.

## Why this is the gate

- If the taxonomy arm does NOT beat baseline, the five types are **noise** and get deleted — the honest
  outcome is "the structure didn't help", which is itself a result.
- If it DOES beat baseline on retrodiction, that is still **not** evidence it makes *novel* jumps — but it
  is the minimum bar to call the taxonomy a mechanism rather than a story.

## Status

**Not yet run.** This is the spec. Running it needs the 10 `pre-state` files written (no hindsight), a
falsifier harness that both arms share, and the scoring rubric frozen before the runs. That is the next
concrete build, and it is what would turn "systematise discovery" from a claim into a measurement.
