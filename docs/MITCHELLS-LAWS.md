# MITCHELL'S LAWS

A result earns the name **Mitchell's Law** only when all four hold:

1. **stated precisely** — symbols defined, no hedge words ("approximately", "appears to");
2. **verified** — either a symbolic proof at zero tolerance, or a measurement with a control
   that could have failed;
3. **scoped** — the regime where it holds, stated in the same breath as the law;
4. **falsifiable** — it names the observation that would kill it.

Anything that fails (2) is a *conjecture* and belongs in `docs/unification-claim.md`, not here.
A law whose falsifier cannot be written down is not a law, it is a slogan.

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

## Candidate laws (not yet named — pending verification)
| the injectivity law | distinct duality orbits at fixed `N` never share low-energy data | not written yet (corpus-only, no jaxvacua needed) | queued as test 2 of C3 |

**Naming rule for what comes next.** A candidate is written up here the moment its test lands,
under the next number, with the evidence command and the job id. A candidate that fails is
recorded too — in `docs/unification-claim.md` — because a law's refutation is worth as much as
its confirmation, and a register that only lists successes is not a register.
