# Gate protocol — every candidate lemma must clear these before proof effort is spent

The system's job is to *raise the odds of finding the truth* and *make failure informative* (Claude).
A candidate mechanism that cannot clear the early gates is dropped before anyone spends proof effort.

The gates, in order (cheapest first):

1. **Fidelity-reviewed statement.** The lemma is written as a faithful formal statement, paired with its
   textbook source in `FIDELITY.md`. If the source cannot be named, the lemma does not proceed.
   Anchor for the top-level claim: the Jaffe–Witten statement, cross-checked against
   `google-deepmind/formal-conjectures` PR #7636 (verify its fidelity, do not trust it).

2. **Non-vacuity.** The hypotheses hold in an explicit example, and the `β = 0` case gives independence.
   Run `scripts/vacuity_linter.py` — a vacuous/tautological statement is rejected here.

3. **Numeric sanity on small lattices.** The mechanism reproduces an exact small-volume computation on a
   finite subgroup of SU(2) (or a 1-plaquette integral), not the fitted curve.

4. **U(1) negative control.** The mechanism must *provably fail* for 4D weak-coupling U(1) (no gap
   expected) — `u1_coulomb_tension_zero` is the standing gate. If it "proves" a gap for U(1), it is wrong.

5. **2D/3D reproduction.** The mechanism reproduces the solvable (2D) and super-renormalizable (3D) cases.
   A mechanism that cannot do those is not worth taking to 4D.

6. **Kernel proof.** The statement is proved in Lean, `lake build` green, `#print axioms` clean (no
   `sorry`, no `Classical.choice` surprises on the key theorems).

7. **External review.** An adversarial pass — like the one that caught the vacuous `orbit_spectral_gap_*`
   and the overclaimed "β-independent mass gap" — runs against every new theorem before it is recorded
   as a result.

8. **Ledger entry.** The theorem is tagged in `CLAIM-LEDGER.md` (`proven-general` / `proven-in-a-model` /
   `conditional` / `cited` / `open` / `vacuous`), and the tag is part of the record.

A mechanism that clears gates 1–5 but fails 6–8 is *in progress*, not *done*. A mechanism that fails 1–5
is dropped.

## What this replaces

The old flow ("add a candidate, run the fitted referee, report survivors") let a circular candidate
(`gribov_ir_suppression = referee_m`) and vacuous theorems through. The gate protocol makes the fitted
referee the *last* resort, not the first: exact small-volume computations (gate 3) and the U(1) control
(gate 4) come first.

## The falsifier bench (gate 3's engine)

Replace the fitted `25.28·e^{−1.182β}` with:
- exact 1-plaquette SU(2) integrals (Bessel ratios `I₁/I₀`);
- exact small-volume (2×2, 3×3) computations on finite subgroups of SU(2);
- 2D/3D lattice computations;
- U(1) as the negative control.

No candidate reads from the fitted curve.
