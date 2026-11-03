# SEXTANT — an equation for quantum gravity, or the proof that the field cannot choose one

**Status: REGISTERED, NOT RUN.** Every cell of the table in this document is `UNKNOWN`, and that is the
honest state of the field, not a gap in this repo. Nothing here is a physics result.

**Discipline:** energy · **Oracle class:** derivation + observation (per condition, see §3) ·
**Falsifier:** named per condition; the programme's own falsifier is §8.

---

## 1. What this is not

- It is **not** a theory of everything. This repo has already established that no connecting equation
  derives the 19 Standard-Model parameters. SEXTANT does not reopen that; it aims at the *gravitational
  sector*, which that theorem leaves untouched.
- It is **not** a claim to have solved quantum gravity. It claims to *decide between candidates*, which
  is the step that has been missing.
- It is **not** an experimental prediction invented in an office. §6 freezes the prediction against an
  existing bound **before** the comparison runs, and if the bound cannot be read from a primary source
  it is not used.
- It is **not** a new conjecture. It is a referee: the repo's `claim → falsifier → evidence → certificate`
  spine, applied to the frameworks themselves rather than to one claim.

## 2. Why the field is stuck — the diagnosis this rests on

Graviton perturbation theory is non-renormalisable: `[G_N] = -2`, so a new counterterm is required at
every loop order. The consequence is a **degeneracy, not a mystery**: infinitely many ultraviolet
completions reduce to Einstein gravity below the Planck scale, so *every* candidate framework matches
*every* current observation automatically. Below the Planck scale they are all general relativity, and
that is why experiment has not discriminated between them — it structurally cannot.

Discrimination can therefore come from only two places:

1. an observable where a completion **must** deviate from general relativity, or
2. a condition a framework **must** satisfy and does not.

The field industrialises (1)'s invention and checks (2) one framework at a time, inside each
community. Nobody runs every condition against every framework and publishes the truth table. That gap
is machinery, and machinery is what this repository builds.

## 3. The lattice — 13 conditions, 6 frameworks, 78 cells

Every condition carries the four things this repo requires of a claim: a **predicate**, a **falsifier**,
an **evidence class** (`derivation` / `observation` / `argument`), and a **machine class** in the
vocabulary `pacland.swampland` already uses (`TESTABLE-NOW` / `NEEDS-BIGGER-MACHINE` /
`NOT-TESTABLE-IN-TRUNCATION`).

| id | condition | class | machine |
|---|---|---|---|
| C1 | low-energy limit is Einstein-Hilbert with the measured `G_N` | derivation | TESTABLE-NOW |
| C2 | diffeomorphism invariance preserved, or its recovery mechanism exhibited | derivation | TESTABLE-NOW |
| C3 | no propagating ghost — or a stated Lee–Wick/PT resolution with a unitary S-matrix | derivation | TESTABLE-NOW |
| C4 | exactly two graviton polarisations, or the extra modes screened | derivation | TESTABLE-NOW |
| C5 | `S = A/4G` with coefficient 1, not a fitted normalisation | derivation | TESTABLE-NOW |
| C6 | an account of the vacuum energy, `ρ_Λ/M_Pl⁴ = 1.1e-123` (≡ `Λ/M_Pl² = 2.9e-122`), or a plain admission there is none | argument | NOT-TESTABLE-IN-TRUNCATION |
| C7 | Planck-scale dispersion modification below the observed bound | observation | TESTABLE-NOW |
| C8 | `v_gw = c` to multimessenger precision | observation | TESTABLE-NOW |
| C9 | new scalars screened, or below equivalence-principle bounds | observation | TESTABLE-NOW |
| C10 | shadow size and ringdown inside the measured intervals | observation | NEEDS-BIGGER-MACHINE |
| C11 | swampland conditions hold, slack *or* tightness stated exactly | derivation | TESTABLE-NOW |
| C12 | the framework's own equations possess a semiclassical GR solution | derivation | NEEDS-BIGGER-MACHINE |
| C13 | early-universe predictions inside the measured bounds | observation | NEEDS-BIGGER-MACHINE |

Two deliberate non-kills:

- **C6 is `UNKNOWN`, never `KILLED`.** No framework accounts for the size of the cosmological constant.
  Scoring it as a kill would kill all six by fiat, which is not a measurement.
- **C11 is asked only of string-derived candidates.** For the others it is recorded as *not asked*, not
  as a failure. The control is this repo's own exact result: on the `T⁶` oracle `α = 1.0000` and
  `z = 1.0000` — the swampland bounds are **saturated, not slack**, which is the standard any
  string-derived candidate must meet.

## 4. The verdict alphabet — and why all 78 cells are `UNKNOWN`

    KILLED    a verifier ran and the candidate provably fails
    SURVIVES  a verifier ran and the candidate satisfies the predicate as far as the evidence goes
    UNKNOWN   no verifier has run against a verified bound

There is deliberately **no path from "nothing found" to `SURVIVES`**. A bound counts only when it has
been read from a primary source (`verified_on` is set, and the dataclass refuses one without a
`source`).

### SX-0, part done (2026-11-03): four bounds read, three named as gaps

Attempting SX-0 found a defect in the lattice itself: **`bound` was doing three jobs**, and the gate
"every constraint has a verified bound" could not be met honestly. Unitarity and the graviton degrees of
freedom are not numbers — there is nothing to verify from a paper, and demanding a bound for them would
have produced a fabricated one. The field `bound_kind` now separates them:

| kind | meaning | count |
|---|---|---|
| `measured` | an external measurement — this is what "verify the bound" means | 7 |
| `theorem` | a proven result (`S = A/4G`, the `T⁶` saturation) — verified by the proof | 2 |
| `procedure` | a derivation condition with no number (C2, C3, C4, C12) | 4 |

Six of the seven measured bounds are now read from their own papers (or, for C6, computed from the
paper's own constants):

| id | bound | source |
|---|---|---|
| C6 | `ρ_Λ/M_Pl⁴ = 1.1e-123` (≡ `Λ/M_Pl² = 2.9e-122`) | [arXiv:1807.06209](https://arxiv.org/abs/1807.06209), A&A 641:A6 — `H₀ = 67.4 ± 0.5`, `Ω_m = 0.315 ± 0.007`, arithmetic in `energy.vacuum` |
| C7 | linear dispersion: the quantum-gravity mass scale is *significantly above* `M_Pl` | [arXiv:0908.1832](https://arxiv.org/abs/0908.1832), Nature 462:331 (2009) |
| C8 | `-3e-15 <= (v_gw - c)/c <= +7e-16` | [arXiv:1710.05834](https://arxiv.org/abs/1710.05834), ApJL 848:L13 (2017) |
| C9 | `η(Ti,Pt) = [-1.5 ± 2.3 ± 1.5]e-15` at 1σ | [arXiv:2209.15487](https://arxiv.org/abs/2209.15487), PRL 129:121102 (2022) |
| C10 | M87* shadow diameter `42 +/- 3` micro-as | [arXiv:1906.11238](https://arxiv.org/abs/1906.11238), ApJ 875:L1 (2019) |
| C13 | `r_0.05 < 0.036` at 95% confidence | [arXiv:2110.00483](https://arxiv.org/abs/2110.00483), PRL 127:151301 (2021) |

**C6 found a dimensional error in v0.** The lattice said `Λ/M_Pl⁴ ~ 1e-122`, which is not a ratio that
exists: the cosmological constant has mass dimension 2, so `Λ/M_Pl²` is the dimensionless statement and
`ρ_Λ/M_Pl⁴` is the other one. Both are ≈1e-122 — which is precisely how the error survived a reading.
`energy.vacuum` computes both from Planck's abstract, and a test asserts they differ by exactly `8π`.

One bound is **not** read, and is named in `PENDING_BOUNDS` so it cannot be quietly forgotten:

- **C1** — Cassini's post-Newtonian `γ`: Nature 425, 374 (2003) is paywalled and was not fetched. The
  bound is quoted everywhere second-hand; quoting it without reading the paper is the failure this gate
  exists to prevent.

Two of the six verified bounds cover only *half* their condition, and say so in the record: C10 verifies
the shadow but not the ringdown; C13 verifies the tensor-to-scalar ratio but not the spectral index or
its running; C9 verifies the laboratory half, since its solar-system half is C1. A half-verified
condition is not a verified condition.

**Every cell is still `UNKNOWN`.** A verified bound makes a condition *evaluable*; it does not decide it.
Deciding requires the candidate's own predicted value, which is SX-1.

There is deliberately **no path from "nothing found" to `SURVIVES`**, including the six rows where the
condition is not asked at all.

## 5. The target equation — named, not gestured at

Two carriers run in parallel, because betting the programme on one derivation is not a plan.

**Carrier A — the effective average action at a non-Gaussian fixed point.** The functional
renormalisation group equation

```
k ∂_k Γ_k[g]  =  ½ STr[ ( Γ_k^{(2)}[g] + R_k )^{-1} · k ∂_k R_k ]
```

solved in a truncation ladder gives a fixed point `(G*, Λ*, λ*, …)` and its critical exponents. The
**equation** is the infrared endpoint of that trajectory — an equation of motion whose coefficients are
*computed*, not fitted:

```
G_μν + Λ_eff g_μν + α R² + β R_μν R^μν + γ R_μνρσ R^μνρσ  =  8π G_eff T_μν
```

Falsifiers: the fixed point must survive at least two truncation orders; and if reaching the observed
`Λ` needs an initial condition tuned to `10^-122`, the programme has renamed the cosmological-constant
problem and must say so rather than claim a solution.

**Carrier B — the group-field-theory condensate.** The condensate's hydrodynamics gives a closed-form
modified Friedmann equation

```
( ȧ/a )²  =  (8πG/3) ρ · ( 1 − ρ/ρ_c )  +  …
```

with `ρ_c` computable from the condensate kinetics and a GR limit that must carry the measured `G_N`.
Falsifier: the coefficient must land inside the BBN/CMB window, or the carrier is dead.

## 6. Phases, gates, and the pre-registration

| # | phase | gate |
|---|---|---|
| SX-0 | fill the lattice: every bound read from a primary source | no `bound: None` survives; a deliberately wrong bound is rejected |
| SX-1 | the referee runs; the six-framework truth table is published | a known-bad candidate (Stelle quadratic gravity) is `KILLED` at C3; absent evidence returns `UNKNOWN` |
| SX-2 | Carrier A: the truncation ladder | fixed point persists across ≥ 2 orders, or is reported absent |
| SX-3 | the double-copy oracle: graviton amplitudes from gauge amplitudes | matches the published amplitude, and fails when the squaring is broken |
| SX-4 | **pre-registration** | the surviving equation's discriminating prediction is committed with a hash **before** the comparison is computed |
| SX-5 | certificate over SX-0…SX-4 | an outside party re-runs one result, or refuses with a named reason |

SX-4 is the step that makes the rest worth anything. A prediction compared after the fact is not a
prediction; it is a description.

## 7. The three engines

- **F — the referee** (`src/pacland/energy/`): the lattice and the verdict machine. Produces certain
  negatives.
- **D — the derivation**: the two carriers of §5. Produces the positive object.
- **O — the oracle** (SX-3): gravity amplitudes as the square of gauge amplitudes (KLT/BCJ) — an
  independent number to check any claimed `R²` coefficient, built as a known-truth battery in the same
  pattern as `pacland.causal.battery`.

## 8. How this loses — the falsifiers of the programme itself

- **The lattice kills all six.** Then the result is *"the joint constraint set is unsatisfiable by every
  named framework"*, plus the least-confident condition that must be relaxed. That is a stronger
  statement than any one framework surviving, and it is this repository's own method turned on the
  field.
- **Carrier A has no fixed point.** Asymptotic safety is dead, with a reproduced computation.
- **The equation survives and predicts nothing observable.** Then *why the field is stuck* is proved
  rather than asserted: the constraint set cannot discriminate.
- **The prediction fails at SX-4.** The kill is on the record, with the prediction frozen first.

In every branch the artefact is a truth table and a certificate. That is the point: the programme does
not have to be right to be worth running.

## 9. Reproduce

```
PYTHONPATH=src python3 -m pacland.energy.referee              # the 78-cell table, as it stands
PYTHONPATH=src python3 -m pacland.energy.referee --self-test  # prove it can KILL, and cannot pass by absence
PYTHONPATH=src python3 -m unittest tests.test_energy_sextant -v
```

(`PYTHONPATH=src` because the checkout is not installed; the tests set it themselves.)

## 10. What makes it real

One sentence, and it is checkable: **a practitioner of one of the six frameworks re-runs the referee on
their own framework and either accepts the verdict or names the exact condition this repo got wrong.**
That is a better success metric than a citation, which is why it is the SX-5 gate.
