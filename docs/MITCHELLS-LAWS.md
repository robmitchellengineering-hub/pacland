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

## Candidate laws (not yet named — pending verification)

| candidate | what it would say | test | status |
|---|---|---|---|
| the S-duality transformation law | `\|W_S\|/\|W\| = e^b · \|τ\|^a` with a clean fit across vacua — i.e. the library realises `(F,H)→(−H,F)`, `τ→−1/τ` as a genuine duality | `scripts/validate_s_duality_vacua.py`, job `2150Z` | **running** — becomes **Mitchell's Law II** only if the log residual < 0.10 |
| the injectivity law | distinct duality orbits at fixed `N` never share low-energy data | not written yet (corpus-only, no jaxvacua needed) | queued as test 2 of C3 |

**Naming rule for what comes next.** A candidate is written up here the moment its test lands,
under the next number, with the evidence command and the job id. A candidate that fails is
recorded too — in `docs/unification-claim.md` — because a law's refutation is worth as much as
its confirmation, and a register that only lists successes is not a register.
