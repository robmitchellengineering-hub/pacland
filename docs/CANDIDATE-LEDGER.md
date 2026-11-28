# Candidate ledger — the falsifier-before-believe belief layer

Every hypothesis is logged with its jump type, falsifier, cost and status, and fed into the belief layer
so the system allocates its falsifier budget to the highest expected-information-gain-per-cost candidate
first. This is the "yes/no hypothesis" bookkeeping that makes the discovery loop a *decision process*, not
a brainstorm.

## Record schema (one entry per hypothesis)

| field | meaning |
|---|---|
| `id` | stable id, e.g. `mg-rungA-001` |
| `problem` | the rung / question it answers |
| `jump_type` | anomaly · inversion · unification · analogy · principle · `none` (baseline arm) |
| `hypothesis` | the candidate, verbatim |
| `prior` | P(h) before any test (from the model, calibrated — see below) |
| `falsifier` | the cheapest test that can kill it |
| `cost` | falsifier cost (tokens / wall-time / a t-shirt number) |
| `status` | open · falsified · surviving |
| `evidence` | the test result, quoted not summarised |
| `posterior` | P(h) after the test |
| `info_gain` | expected information gain per unit cost (the ranking key) |
| `brier` | the calibration score of the prior when resolved |

## Belief-layer rules

- **Prior calibration is mandatory.** We measured ourselves overconfident (**Brier 0.41**). So a prior is
  not a number; it is a *calibrated* number. Priors are rescaled by the measured overconfidence until the
  Brier score of *resolved* entries approaches 0.25 (skill).
- **Rank by expected information gain per cost.** `EIG/cost` = `(entropy(prior) − expected entropy after
  test) / cost`. The next falsifier run is the highest `EIG/cost` among `open` entries. A cheap decisive
  falsifier beats an expensive decisive one; a test that cannot move the posterior is never run.
- **Falsifier before belief.** A hypothesis enters as `open`, never as `surviving`. Only a falsifier that
  *fails to kill it* moves it toward `surviving`. "Sounds plausible" is not a status.

## Starter ledger (the actual hypotheses of this arc)

| id | problem | type | hypothesis | falsifier | status |
|---|---|---|---|---|---|
| mg-001 | finite-β gap | principle | transfer-matrix spectral radius < 1 | kernel-check `secondEigenvalueBelowOne` | falsified (β-independent version) |
| mg-002 | strong-coupling gap | analogy | Dobrushin single-site coupling | LGT proves the *real* result (FRO) | superseded → cite LGT |
| mg-003 | confining mechanism | principle | Casimir mass ⇒ gap | show it is Yukawa, not confining | falsified |
| mg-004 | confining mechanism | principle | IR suppression `G(0)=0` ⇒ 1/p⁴ | `M(p)=p²` is *chosen*, not derived | surviving (model, not proof) |
| mg-rungA-001 | crossover | inversion | scale-wise BE: effective curvature κ_Λ bounded below | toy `effectiveHessian_bounded_below` | surviving (toy only) |
| mg-rungB-001 | mass gap | inversion | exclude spectrum in (0,Δ) off vacuum | `HasMassGap` statement + sanity controls | open |
| mg-rungB-002 | weak-coupling gap | unification | the cluster-expansion condition `(Δ+1)²|ρ| < 1` IS the RG contraction: the renormalised activity is `ρ' = (Δ+1)²·|ρ|²` (quadratic), so the animals summability + blockSpinPow iterate to `ρ_n → 0` | numeric: a `ρ` with `(Δ+1)²|ρ| < 1` whose renormalised `ρ' = (Δ+1)²ρ²` violates `(Δ+1)²|ρ'| < 1` | open |
| mg-crossover-001 | the β≈1 crossover | anomaly | the strong-coupling `1/κ` and weak-coupling `e^(−cβ)` are the SAME gap, and the field proves only the two ends, not the middle; candidate `m(β) ≥ min(1/κ, e^(−(12π²/11)β))` | numeric: a β in the crossover where BOTH regime bounds fail | open |
| mg-rungB-003 | weak-coupling gap | inversion | flip "contraction on the field" to "contraction on the correlation": `⟨AB⟩−⟨A⟩⟨B⟩ ≤ e^(−cβ)‖A‖‖B‖` (the clustering), what reflection positivity gives directly | a reflection-positive measure whose two-point decay is slower than `e^(−cβ)` | open |
| mg-gd-001 | non-Abelian Gaussian domination | analogy | heat-kernel Gaussianization: at weak coupling the SU(2) Haar `sin²θ dθ` + `e^(β cos θ) ≈ e^(−βθ²/2)` is Gaussian, so the scalar/Abelian Gaussian domination lifts via the heat kernel, volume-uniform | numeric: the `e^(β cos θ)` vs `e^(−βθ²/2)` ratio fails to be volume-uniform as β varies (the approximation is weak-coupling only) | falsified (heat_kernel_gaussian_not_uniform @142f37b5) |
| mg-gd-002 | non-Abelian Gaussian domination | inversion | the trace is LINEAR in the character basis (Peter–Weyl `Tr U = Σ χ_r`), so Gaussian domination per character composes; the chessboard estimate applies to each character, then sums | a character sum that fails to be volume-uniform (the infinite character series) | falsified — the character sum IS `e^(2β cos θ)` (wilson_heat_kernel_chebyshev), so the SAME non-uniformity as mg-gd-001 applies |
| mg-gd-003 | non-Abelian Gaussian domination | principle | the chessboard estimate on the PHYSICAL (gauge-invariant) Hilbert space — reflection positivity holds there (Osterwalder–Seiler), so the Gaussian chain runs on the physical space, not the gauge-fixed | the physical-space chessboard estimate fails for the trace observable (the non-linearity) | surviving (the open candidate) |

`status: open` = still hunting; `surviving` = survived a falsifier but not yet a proof. This ledger is the
input to the belief layer; it is what `CANDIDATE-LEDGER.md` must keep growing so the discovery loop has a
memory.
