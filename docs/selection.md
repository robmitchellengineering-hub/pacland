# Selection (L6) — what is buildable, and what is not

The measure problem is the half of "unified string theory" that verification does not
touch: *why this vacuum, and not one of the other 10^500?* This doc separates what we
can build from what we cannot, so the selection question gets the same treatment the
verification question got.

## The problem

A fully-verified vacuum class certifies *membership* in "looks-like-our-universe." It
does not say *why*. The **landscape measure** — the probability distribution over vacua
that nature actually realizes (eternal inflation, quantum cosmology) — is the missing
half, and it has been open for roughly 40 years.

## The key distinction

- **Deriving** the correct measure is physics theory. It is a law of nature to be
  discovered, not a thing to be computed. No tooling derives it — same way no amount of
  software derives Newton's laws.
- **Evaluating** a candidate measure is buildable. This is exactly the move we made for
  verification: stop trying to *prove* the answer, and instead *certify* whether a
  proposed measure matches observation.

The first is closed to us; the second is open and reuses everything already built.

## The measure-verifier (buildable now)

The same two pieces that power verification — the certificate (L3) and the sampler
(L4) — apply to the measure with one change of target:

1. **A candidate measure** is a probability distribution over vacua — e.g. "uniform in
   the cosmological constant," or an eternal-inflation weighting.
2. **Sample vacua under it** — reuse the JAXVacua `FluxVacuaFinder` (installed and
   verified, 37 real vacua on the first run).
3. **Compute its predictions** for cosmological observables (Λ, and in principle CMB /
   large-scale-structure statistics).
4. **PAC-verify the measure** against observation — the same two-level certificate, with
   the hypothesis now a *distribution* rather than a single vacuum.

This is L6's *evaluation* half, and it is not a new subsystem — it is L3 + L4 pointed at
the measure.

## First concrete build: the Λ-typicality test

The classic, concrete selection claim in the landscape literature: across vacua the
cosmological constant Λ is (roughly) uniformly distributed, so our small-but-nonzero
observed Λ is *typical* — the Weinberg anthropic argument. That is a falsifiable
measure-level statement, and it is testable with what we have:

1. Sample many vacua (JAXVacua).
2. Compute Λ for each — related to the scalar potential `V` at the minimum, which
   JAXVacua already returns. (The hard step is the de Sitter *uplift*, which is
   contentious; note it, do not hide it.)
3. Check the empirical distribution of Λ and ask whether observed Λ is typical under
   the candidate measure — exactly a certificate over a distribution.

## Honest effect on the odds

- **It does not move "solve unified string theory" off <1%.** The correct measure is a
  physics discovery, not a tool; no build changes that.
- **It does three real things:** (a) completes the framework — every layer L1–L6 is then
  built, not just L1–L5; (b) yields a second, complementary citable contribution — "a
  PAC-verification framework for landscape measures"; (c) attacks the one lever that can
  close the loop at all, because *verification + selection together* are what
  "unification" means.

Net: building the measure-verifier does not make the impossible likely, but it removes
the last "we have not even tried that half" gap, and it is the only remaining build that
moves the top-line number at all.
