# MITCHELL'S LAWS OF DUALITY COVARIANCE

The **duality covariance table** of the flux landscape: five laws specifying how the
observables of a flux vacuum transform under the duality group `Sp(b₃,ℤ) × SL(2,ℤ)` and under
flux rescaling — the empirical half of the unification programme. The theorem
(`docs/constraint-first-theorem.md`) says the only exact invariant is the tadpole `N`; these
laws say everything else is *covariant*, never anomalous — so duality is a true symmetry,
literally one theory described twice.

| # | name | one line |
|---|---|---|
| **I** | the scaling law | the content `d = gcd(F,H)` is a bookkeeping label, not a selector |
| **II** | the superpotential law | `W` is S-covariant: `\|W_S\|/\|W\| = 1` (magnitude) and `arg(W_S/W) = -arg τ` (phase) |
| **III** | the string-coupling law | `g_s = 1/Im τ` transforms as `g_s → \|τ\|² g_s` (S), `g_s → g_s` (T) |
| **IV** | the moduli law | the complex-structure moduli are inert at degree 0 |
| **V** | the counting law | 19 = the Standard-Model orbit-space dimension (exact as a count, free as values) |

**Verified at h12 = 2 (100 primitive SUSY vacua) and h12 = 5 (12 in-cone SUSY vacua, found by
the iterated linearised shift).** Laws II, IIb, III hold *exactly* at both: `|W_S|/|W| =
1.000000` (std 3.7e-15), `arg(W_S/W) = −arg τ` (residual 7.4e-16), `g_s` ratio `1.000000`
(std 1.8e-16). Law I is symbolic (h12-independent); Law V is the SM orbit-space dimension.

A result earns the name **Mitchell's Law** only when all four hold:

1. **stated precisely** — symbols defined, no hedge words ("approximately", "appears to");
2. **verified** — either a symbolic proof at zero tolerance, or a measurement with a control
   that could have failed;
3. **scoped** — the regime where it holds, stated in the same breath as the law;
4. **falsifiable** — it names the observation that would kill it.

Anything that fails (2) is a *conjecture* and belongs in `docs/unification-claim.md`, not here.
A law whose falsifier cannot be written down is not a law, it is a slogan. Law II has two
halves, recorded as Law II (magnitude) and Law IIb (phase); together they close the full
complex S-row of `W`.

---

## Mitchell's Law I — the scaling law

**Statement.** For a flux compactification with superpotential `W` linear in the flux, and
tadpole `N = FᵀJH`:

```
W(dF, dH)   = d · W(F, H)          (degree 1)
DW(dF, dH)  = d · DW(F, H)         ⇒ the SUSY condition's zero set is invariant
N(dF, dH)   = d² · N(F, H)         (degree 2)
gcd(dF, dH) = d · gcd(F, H)        (the integer content scales with d)
```

**Consequence — the part that matters.** Every SUSY vacuum at moduli `z` has a SUSY vacuum at the
**same** `z` with flux scaled by `d`, whose `W₀` is `d×` larger and whose tadpole is `d²×` larger.
So the ℤ-orbit content `d = gcd(F,H)` — the label that distinguishes the finitely many orbits
sharing a tadpole — **carries no physics beyond a rescaling**. It is bookkeeping, not a selector.

**Evidence.**
- Symbolic, exact: `scripts/validate_flux_scaling_lemma.py` → **5/5 PASS** at zero tolerance
  (`W` homogeneous 1, `DW` homogeneous 1, `N` homogeneous 2, content scaling over 200 random
  integer cases, and an explicit witness `DW(2F) = 2·DW(F)`).
- Against the library, on a real vacuum: `scripts/verify_flux_scaling_numeric.py`, job
  `2026-10-22T2143Z` on `pacland-rog` (jaxvacua 0.1.2): `|W(F)| = 9.517164883845e-01`,
  `|W(2F)| = 1.903432976769e+00`, ratio **2.0**, tolerance 1e-10 → PASS.
- Corpus consistency: `d² | N` on all **5,885** committed rows (this is arithmetic, forced by
  bilinearity — it tests the data fields, not the law).

**Scope.** Holds whenever `W` is linear in the flux — i.e. at tree level in flux for every
compactification of this type. It does **not** cover a flux-dependence that is non-linear (a
non-perturbative correction entering `W` itself rather than the Kähler potential), and it says
nothing about the *potential* `V`, which is not invariant under scaling (`V` changes with `W`).

**Falsifier.** A measured vacuum whose `DW` zero set is not preserved under flux scaling, or a
demonstration that the library's superpotential contains a term non-linear in flux.

---

## Mitchell's Law II — the S-duality invariance of the superpotential

**Statement.** Under the S-generator of the duality group acting on the flux pair and the
axio-dilaton,

```
(F, H) -> (-H, F)        tau -> -1/tau        moduli held fixed
```

the superpotential is **invariant in magnitude**: `|W(-H, F; τ = -1/τ)| = |W(F, H; τ)|`.
Equivalently: the realised transformation law is `|W_S|/|W| = |τ|^0` — the exponent is zero.

**Why it matters.** It is the first direct evidence for **C3's well-definedness** half of the
unification claim: a duality transformation maps a vacuum to a vacuum carrying the *same*
superpotential, so the orbit-space coordinates are consistent across dual descriptions. It is
also the reason the tadpole invariance under S is not a coincidence: `N' = (-H)ᵀJF = FᵀJH = N`
because `J` is antisymmetric, and the same antisymmetry is what leaves `W` invariant.

**Evidence.** `scripts/validate_s_duality_vacua.py`, job `2026-10-22T2150Z` on `pacland-rog`
(jaxvacua 0.1.2), 25 primitive SUSY vacua with **0 failures**:

```
evaluated 25   failed 0
transformation law fit: |W_S|/|W| = exp(-0.0000) * |tau|^-0.0000
  residual rms in log: 0.0000
  verdict: LAW
```

The sample spans `|τ|` from 2.16 to 11.49, i.e. nearly a decade in coupling, and the ratio is
`1.0000e+00` on **every** row — not a fit through scattered points but a constant. The test
deliberately did **not** assume the textbook law; it fitted `a` and `b` freely, and both came
back zero.

**Scope.** Verified for `h12 = 2`, `model_ID = 1` (the KS truncation), on primitive
(`d = 1`) SUSY vacua, for the **magnitude** `|W|`. The complex phase of `W` under S-duality is
**not** verified here — the fit constrains the modulus, not the argument — and no claim is made
about `h12 ≥ 3` or about the potential `V`, which is not invariant (`V ∝ e^K(...)` changes with
the Kähler data even when `W` does not).

**Falsifier.** Any vacuum in the same class whose `|W_S|/|W|` departs from 1 by more than the
fit's tolerance (log residual > 0.10). A phase measurement departing from a fixed law would
weaken the statement to magnitude-only invariance, which is what is claimed today.

---

## Mitchell's Law IIb — the phase of W under S-duality

**Statement.** Under the S-generator the gauge-invariant superpotential transforms by a pure
phase: `arg(W_S/W) = -arg(τ)` exactly, equivalently `W_S = W · τ̄/|τ|`. Combined with Law II
(`|W_S|/|W| = 1`) this closes the full complex S-row: `W_S = W · conj(τ)/|τ|`.

**Evidence.** `scripts/measure_phase_law.py`, job `2026-10-22T2340Z` on `pacland-rog`, 100
primitive SUSY vacua: fit `arg(W_S/W) = a·arg(τ) + b` gives **a = −1.0000, b = 0.0000, residual
rms 0.0000**. The control (the magnitude of the same ratio) reproduces Law II: `|W_S|/|W| =
1.000000` (std 4.4e-16), so the phase is measured on a validated path.

**Scope.** `h12 = 2`, `model_ID = 1`, primitive (`d = 1`) SUSY vacua, degree 0 (fixed moduli).
The gauge-invariant (Kähler-normalised) `W`; the raw `W` has a different modular weight.

**Falsifier.** A phase that departs from `-arg(τ)` by more than the fit tolerance (residual > 0.10).

---

## Mitchell's Law III — the string-coupling covariance

**Statement.** With `g_s = 1/Im(τ)`: under S (`τ → −1/τ`), `g_s' = |τ|²·g_s` (which is `1/g_s`
only when `C₀ = 0`); under T (`τ → τ+1`), `g_s' = g_s`.

**Evidence.** `scripts/measure_covariance_table.py`, 100 primitive SUSY vacua: `g_s'/(|τ|²g_s) =
1.000000` (std 1.4e-16) under S, and `g_s'/g_s = 1.000000` (std 0) under T. **Definitional** — `g_s`
is read off `τ`, so a deviation is a measurement bug, not a physics finding; it exposed the earlier
`2209Z` "`g_s 0.21 → 3.9e7`" as a bug (the correct law is `|τ|²·g_s`, not `1/g_s` at general `C₀`).

**Scope.** Any `τ` (definitional); verified on the same 100-vacuum sample.

**Falsifier.** `g_s' ≠ |τ|²·g_s` under S at a point where `g_s = 1/Im(τ)` is the convention.

---

## Mitchell's Law IV — the moduli are inert at degree 0

**Statement.** At degree 0 (no instanton corrections) the S/T generators act on the flux pair and
the axio-dilaton only; the complex-structure moduli are inert, `z_i → z_i`. Their monodromy is a
degree > 0 effect and is deferred.

**Evidence.** By definition of the degree-0 duality action, and confirmed by G2
(`scripts/test_g2_sdual_stability.py`): the transformed point at fixed `z` is a vacuum
(`|DW| = 1.8e-12 ≤ 1e-6`, control reproduced the stored `3.2e-12`).

**Scope.** Degree 0 (tree level). Not a claim about the full monodromy group.

**Falsifier.** A degree-0 duality transformation that requires a moduli shift to remain a vacuum.

---

## Mitchell's Law V — the counting law (19 = orbit-space dimension)

**Statement.** The Standard Model's exact content includes a **counting** type: the dimension of
its orbit space under the SM's own flavor group is **19** (quark 10 + lepton 3 + gauge 3 + Higgs 2
+ θ_QCD 1). Exact as a count, free as values — a ToE predicts relations, never values.

**Evidence.** Three independent routes agree (all exact): (a) the counting formula
`dim(V/G) = n − g + s` (`validate_sm_invariant_ring.py`); (b) the exact Jacobian rank
(`validate_sm_rank_test.py`, GF(p) modular rank at three primes); (c) the Molien–Weyl /
Hilbert–Serre cert (`validate_molien_weyl.py`, with an S₃-on-ℂ³ Molien-series control matching
`1/[(1−t)(1−t²)(1−t³)]`). The only known UV symmetry (GUT) collapses exactly 3 of the 19 (gauge
3→1, b–τ 2→1).

**Scope.** The SM's own flavor/reparametrization group; the *dynamical* rank is bounded by
`2h¹¹ + 2h²¹ + 2` (reducible for `h¹¹+h²¹ ≤ 8`).

**Falsifier.** A 20th independent invariant — an exact UV relation among the 19 beyond the GUT
collapses.

---

## Candidate laws (not yet named — pending verification)
| the injectivity law | distinct duality orbits at fixed `N` never share low-energy data | not written yet (corpus-only, no jaxvacua needed) | queued as test 2 of C3 |

**Naming rule for what comes next.** A candidate is written up here the moment its test lands,
under the next number, with the evidence command and the job id. A candidate that fails is
recorded too — in `docs/unification-claim.md` — because a law's refutation is worth as much as
its confirmation, and a register that only lists successes is not a register.
