# A New Approach: Constraint-First String Theory

The synthesis of this project plus the leading research, stated as one program.

## What we now know — three results point the same way

1. **No exact invariant selects a vacuum, and no certificate-only search converges
   (ours, proved).** W0 is statistically uniform (Denef–Douglas), so `flux → W0` has
   ~zero mutual information; by Valiant's contrapositive (*evolvable ⇒ learnable*),
   no certificate-only evolutionary search converges. We confirmed the uniformity on
   163 real flux vacua. `docs/learnability-negative.md`.

2. **The deficit is total, and that's a measurement problem, not a conceptual one
   (ours).** `m = 0` validated oracle outputs today, so the certificate is vacuous —
   but it closes as calibrated oracles are built. `docs/verification-deficit.md`.

3. **The literature was never searching.** Denef–Douglas (uniformity), the swampland
   program (constraints), and the S-matrix bootstrap (consistency) all attack the
   landscape by *constraint*, not by scan. We never had to search; the field already
   knew the right frame and we re-derived it from the other side.

**The synthesis:** search was always the wrong frame. The landscape is a space to be
*constrained*, not a space to be *scanned*. Our negative result did not close a door —
it proved the door was never there.

## The new approach: mine structure, then eliminate by verified constraint

Stop asking *"which vacuum?"* Start asking two better questions.

**Q1 — "Which observables carry information about the geometry?"** (structure mining)
W0 doesn't (proved). But gauge couplings, masses, and topological invariants might.
Classify every observable by its *mutual information* with the compactification — not
linear correlation (which misses nonlinear structure), but full information content.
The structured observables are the geometry's *fingerprint*.

**Q2 — "Which constraints eliminate the most vacua, and can we verify them?"**
(constraint verification)
Every swampland conjecture, every bootstrap bound, every consistency condition is a
*certifiable statement*: "with confidence δ, this constraint rules out fraction ε of
the landscape." A chain of verified constraints narrows the viable space by
elimination — pinning down the compactification without ever searching for it.

**The connection between Q1 and Q2.** The structured observables are exactly the
coordinates the constraints should be phrased in. Mine structure to find the
fingerprint; verify constraints in the fingerprint's coordinates; the intersection of
verified constraints *is* the viable compactification class. The inverse problem
("given measured observables, what must the geometry be?") is answered by elimination,
not by search.

## Why this is genuinely new

The field splits into "search" (ML landscape scans) and "constrain"
(swampland/bootstrap), and treats them as separate camps. We unify them under one
discipline — *verified* constraint, with information-theoretic structure mining on one
side and certificates on the other. Nobody does the search side (it's dead), and nobody
*certifies* the constraint side (there's no framework). We now have both halves of the
framework, and the point where they meet is where the compactification gets pinned down
— or provably can't.

## The first build: a non-linear structure miner

The prior pass found ~zero *linear* correlation between flux and observables. But that
only rules out linear structure. A mutual-information miner catches nonlinear structure
that Pearson misses, and a permutation test separates real structure from finite-sample
noise. This tool is the fork: it either finds the fingerprint (a positive result — an
observable that pins the geometry) or strengthens the negative result (the map is
information-theoretically empty, and the landscape is underdetermined in these
coordinates). Either branch is a finding, and both are buildable now.

## Where this lives

- `src/pacland/structure.py` — mutual information + significance + classification.
- `scripts/mine_structure.py` — run the miner over the real flux-vacua data.
- `tests/test_structure.py` — the miner, tested against known structured/random classes.
