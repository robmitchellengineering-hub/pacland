# SEXTANT proof tiers — the five-way distinction at the heart of the identity

A sextant does not create the stars; it reads your position from them. The mass-gap program is giving
SEXTANT its sharpest case study yet, because it forces the system to separate five things that are easy
to conflate and fatal to conflate:

## The five tiers

1. **A mathematical identity.** A statement that is true by definition or by an algebraic identity —
   e.g. `∏_p (1 + ρ p) = Σ_{S ⊆ P} ∏_{p∈S} ρ p` (the subset identity). No hypothesis; it is simply
   the case. Its proof is combinatorics, not physics.

2. **A formally verified lemma.** A single statement with a machine-checked proof — e.g.
   `walk_count_bound : #(walks of length n) ≤ maxDegreeⁿ`. It is *proved*, and the proof is a
   certificate (a Lean term), not an assertion.

3. **A verified chain of lemmas.** Several lemmas whose composition is checked — e.g. the entire
   single-cluster cluster-expansion layer (subset identity → linked-cluster log-factorization →
   Taylor weights → geometric decay → absolute summability). The chain is a theorem in its own right;
   its value is the *wiring*, not any single link.

4. **A theorem conditional on an outstanding hypothesis.** A statement of the form "if H then T",
   where T is proved and H is named but unproved — e.g.
   `refereeScalingLaw_of_radius_bound : ρ(β) ≤ e^{−A·e^{−cβ}} ⟹ m(β) ≥ A·e^{−cβ}`. The theorem is
   *proved*; the mass gap itself is *not*, because H is the open rung. Conflating this with tier 5 is
   exactly the failure SEXTANT must never commit.

5. **A completed result established without that outstanding hypothesis.** The unconditional statement
   T with H discharged. For the Yang–Mills mass gap this tier is **not yet reached** — H (the Balaban
   linked-cluster contraction, and beneath it the lattice-animals bound `#{connected clusters of size n}
   ≤ Δ^{2(n−1)}`) is still open.

## Why the distinction is central

The four existing verdicts (FORCED / FREE / IMPOSSIBLE / IRREDUCIBLE) answer *where a claim sits*.
The five tiers answer *how far the proof actually goes*, which is a different question and the one
that matters for honesty:

- A claim can be **FORCED** (kernel-checked) and still be only **tier 2** (a lemma), not tier 3.
- A claim can be **IRREDUCIBLE** (computable, no closed form) and still be **tier 4** (the conditional
  theorem is proved) while **tier 5 is missing**.

The mass-gap reduction is the live exhibit of the difference: *"mass gap ⟺ H" is a proved conditional
(tier 4); the mass gap is not proved (tier 5 is open).* SEXTANT must be able to say both sentences in
the same breath, and the tiers are what let it.

## The mass-gap mapping (the case study)

| Artifact | Tier | Status |
| --- | --- | --- |
| `polymer_expansion_subset` — `∏(1+ρ) = Σ_S ∏ρ` | 1 identity | proved |
| `walk_count_bound` — `#(walks) ≤ Δⁿ` | 2 lemma | proved |
| the single-cluster cluster-expansion layer | 3 chain | proved |
| `refereeScalingLaw_of_radius_bound` — `ρ ≤ e^{−A·e^{−cβ}} ⟹ m ≥ A·e^{−cβ}` | 4 conditional | proved, H open |
| the Yang–Mills mass gap `m(β) ≥ A·e^{−(12π²/11)β}` | 5 result | **open** |
