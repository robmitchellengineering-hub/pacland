# Zenodo submission — mass-gap reduction paper

**Status:** draft metadata + paper skeleton for review before upload.
**Honest positioning:** a methods + formalization + negative-results record. **Not** a claim of the
mass gap.

---

## 1. Zenodo metadata

| field | value |
|---|---|
| **Title** | A falsifier-first, kernel-checked reduction of the Yang–Mills mass gap to the Gribov–Zwanziger horizon condition |
| **Upload type** | Publication → Preprint |
| **Authors** | Rob Mitchell |
| **Publication date** | (date of upload) |
| **License** | Creative Commons Attribution 4.0 (CC-BY-4.0) |
| **Language** | English |
| **Keywords** | Yang–Mills; mass gap; asymptotic freedom; Gribov–Zwanziger; Coulomb confinement; formal proof; Lean; Mathlib; transfer matrix; falsification |
| **Related identifier** | `https://github.com/robmitchellengineering-hub/pacland` (is supplemented by / is source of this record) |
| **Description** | (the abstract, §2) |

## 2. Abstract (the honest one)

We present a machine-checked (Lean/Mathlib) reduction of the 4D SU(2) Yang–Mills mass-gap problem to
a single named statement: the positivity of the dimensionless ratio `m/Λ` (equivalently `m/√σ ≈ 3.2`),
uniformly in the volume. The exponential `e^{−cβ}` is identified as the known one-loop beta function
(Gross–Wilczek–Politzer), not as the open content of the problem.

Against a lattice referee (`m(β) = 25.28·e^{−1.182β}`, `m/√σ ≈ 3.2`), we falsify the candidate
mechanisms that fail — the plaquette concentration (power law `1/β`), the cluster expansion (`log β`),
the Dobrushin coupling (dies at the ceiling), and the chessboard surface-tension bound (circular) —
we kernel-check (no `sorry`) the Casimir → Faddeev–Popov constant-mode gap → positive-semidefinite
transport chain, and MODEL (`M(p) = p²` chosen, NOT derived) the IR suppression `G(0) = 0` → the `1/p⁴`
singularity → the linear Coulomb potential. We correct an earlier step by showing the Casimir *mass* is
deconfining (Yukawa), while the *IR suppression* is the confining mechanism. Open: the horizon condition.

**We do not prove the mass gap.** The remaining rung — the infinite-dimensional horizon condition
(`γ > 0` for the full Faddeev–Popov operator) — is stated precisely and left open.

## 3. The explicit non-contribution (put this in the paper, not only in chat)

> This paper proves no new bound and no new theorem about the mass gap. It contributes a verified
> map of the problem — what is assumed, what is proven, what is falsified, and exactly what remains —
> not a solution.

## 4. Contribution bullets (honest)

1. **A kernel-checked reduction artifact.** The first machine-verified statement of exactly what
   remains unproven: `refereeScalingLaw ⟺` the volume-uniform positivity of `C = m/Λ`.
2. **A falsification record.** Which candidate routes are eliminated and why, each tested against the
   referee before any proof attempt.
3. **A reproducible method.** Falsifier-before-believe applied to a Millennium problem, with the
   Lean kernel as the final gate.

## 5. Paper skeleton

1. **Introduction** — the problem; the honest scope (map, not solution); the standing rule that no
   open rung is claimed.
2. **The method** — falsifier before believe: referee → SEXTANT falsifier → Lean kernel. The order
   matters.
3. **The referee** — the lattice data `m(β) = 25.28·e^{−1.182β}`, `m/√σ ≈ 3.2`; the power-law vs
   exponential distinction that drives everything.
4. **The transfer-matrix diamond** — the six equivalent faces of the mass gap, proven equivalent
   through the spectral theorem; contraction, strict gap, volume-uniform decay, chessboard estimate,
   surface-tension bridge.
5. **The gradient flow and the asymptotic-freedom scale** — the Wilson flow, the contraction rate, the
   suppression `e^{−2β}`, the known one-loop beta function `e^{−1/(b₀g²)}`.
6. **The reduction** — dimensional transmutation `m = C·Λ`; `refereeScalingLaw ⟺ C > 0`
   volume-uniformly; the exponential is known, the ratio is the open content.
7. **The Coulomb route, corrected** — the Casimir mass deconfines (Yukawa `1/p²`); the Gribov horizon's
   IR suppression confines (`G(0) = 0` → `1/p⁴` → linear potential). Checked: Casimir → FP gap → PSD
   transport. Modelled: IR suppression → 1/p⁴. Open: the horizon condition.
8. **The falsifications** — the table of eliminated candidates and why.
9. **The open rung** — the infinite-dimensional horizon condition, stated precisely.
10. **The honest boundary** — proven vs assumed vs open.
11. **Reproducibility** — `lake build` (9157 jobs, exit 0), the file locations, the falsifier bench.
12. **Acknowledgments and AI-use statement** — the formalization was carried out with an AI coding
    assistant under human direction; the human is the author; the kernel, not the assistant, is the
    source of truth.
13. **References** — Gross–Wilczek–Politzer (1973); Gribov (1978); Zwanziger (2004, Coulomb
    confinement); the lattice referee's source.

## 6. What goes in the archive (the Zenodo payload)

- This paper (rendered to PDF) — the honest abstract + the 13 sections.
- `docs/MASS-GAP-METHODS.md` — the traceable methods record.
- `pacland-proof/PaclandProof/QM/MassGapDiamond.lean` — the spectral diamond + the Coulomb/Gribov route.
- `pacland-proof/PaclandProof/QM/GradientFlow.lean` — the flow + the AF scale + the reduction.
- `src/pacland/runner.py`, `src/pacland/hypotheses.py` — the falsifier bench + registry.
- A `README` pointing at the exact `git` commit and the `lake build` command.

## 7. Review checklist before upload

- [ ] The abstract does **not** claim the mass gap (it says "we do not prove").
- [ ] The non-contribution line (§3) is in the paper body, not only the metadata.
- [ ] The referee numbers are cited to their source (the lattice run), not presented as derivations.
- [ ] `lake build` is green at the exact commit the DOI points to.
- [ ] The AI-use statement names the tooling without making the assistant an author.
