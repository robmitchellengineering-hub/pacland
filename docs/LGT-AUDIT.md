# Audit — Douglas's LGT library (the strong-coupling mass gap is already proved)

Fetched and read the [LGT reservoir page](https://reservoir.lean-lang.org/@mrdouglasny/LGT) and its
README. **This is a verified, real, complete result — and it supersedes the M2/M3 skeleton in this repo.**

## The headline result (verified)

`LGT/MassGap/StrongCoupling.lean`, by **Michael R. Douglas (CMSA, Harvard) + Fred Rajasekaran**:

- **`ym_mass_gap_exponential_decay`** — `|⟨Re Tr(U_p)·Re Tr(U_q)⟩_c| ≤ 32n²/(1−α)·α^((plaqDist−1)/2)` for
  U(n) Wilson lattice gauge theory on (ℤ/Nℤ)^d, d ≥ 2, β < 1/(32n(d−1)).
- **`ym_mass_gap_rate_exists`** — the packaged `∃ m > 0, |⟨…⟩_c| ≤ C·exp(−m·plaqDist)`.
- Via the **Dobrushin uniqueness method** (Chatterjee 2026, Ch. 16).
- **Zero sorries, zero project axioms.** `#print axioms` = `{propext, Classical.choice, Quot.sound}`.
- **Independently verified by the Lean FRO comparator** at commit `ec975bd` ("Lean default kernel accepts
  the solution", whitelist `{propext, Quot.sound, Classical.choice}`).

## What this means for pacland

**My M2/M3 (Dobrushin + Wilson + β₀) is redundant.** LGT has it, more strongly (U(n), d ≥ 2, quantitative
rate), axiom-clean, and FRO-kernel-verified. Re-deriving it here would be wasted effort.

**What IS still valuable here (the revised role):**

1. **Audit layer.** LGT is kernel-verified but the *statement fidelity* against the Clay description is
   not — the README even notes the Bridge's "several fields still stated as hypotheses". The vacuity
   linter + `#print axioms` + the claim ledger + statement-fidelity checks are exactly the audit this repo
   should run against LGT and against the Gross-committee's AI-made existence-proof repo.
2. **The crossover.** LGT's **Bridge/** (layer 8) connects a tensor-RG (EKR) certificate to the Dobrushin
   mass gap — but "several fields still stated as hypotheses". That is the genuinely-open, un-claimed
   piece: gauge-theory TRG certificates, and the Polchinski–Bakry–Émery multiscale criterion.
3. **The M0 real-group + Doeblin work here** is a thin, publishable seed but is superseded by LGT for the
   strong-coupling conclusion.

## Version note

The reservoir metadata lists many Lean versions, but the README pins **Lean/Mathlib v4.29.0** (with
`markov-semigroups` + `gaussian-field` deps). This repo is on v4.35.0 — porting LGT here (or auditing it
in its own checkout) is the concrete next step, not re-derivation.
