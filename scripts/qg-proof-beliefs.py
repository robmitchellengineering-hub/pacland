#!/usr/bin/env python3
"""The QG proof-belief graph — apply the belief layer to the three deferred proofs.

C/P-classify Gleason n>=3, the QM reconstruction, and the BDGZ no-go (which are
theorems to prove = Mode C, which are plural axiom/interpretation choices = Mode P),
then order the Mode-C sub-lemmas by expected information gain per cost and print
the single next step to kernel-check.

Run:  PYTHONPATH=src python3 scripts/qg-proof-beliefs.py
Exit: 0 on success (the report prints).
"""
from pacland.belief import (
    Belief,
    Likelihood,
    Mode,
    detect_mode,
    rank_by_eig,
)


def L(tp: float, fp: float) -> Likelihood:
    return Likelihood(true_positive=tp, false_positive=fp)


# --- the three deferred proofs, as sub-lemma DAGs ----------------------------
# prior = belief the sub-lemma is formalizable in the current Lean setup;
# cost  = estimated authoring hours; likelihood = how the "attempt + lake build"
# test answers under formalizable / not-formalizable.

GLEASON = [
    Belief("G1 continuity lemma (Gleason's lemma, analytic)", 0.25, L(0.80, 0.20), 24.0),
    Belief("G2 quadratic-form extension", 0.55, L(0.80, 0.20), 14.0),
    Belief("G3 spectral -> Born (density matrix)", 0.45, L(0.80, 0.20), 18.0),
    Belief("G2' discrete frame-family -> quadratic form (finite slice)", 0.75, L(0.85, 0.15), 6.0),
]

RECONSTRUCTION = [
    Belief("R0 a unique reconstruction exists", 0.5, None, 1.0, ground_truth_available=False),
    Belief("R1 2-level self-duality (the qubit state space)", 0.70, L(0.85, 0.15), 10.0),
]

BDGZ = [
    Belief("B1 1+1D two-frame Lorentz no-go (tractable)", 0.70, L(0.85, 0.15), 8.0),
    Belief("B2 full 4D Lorentz no-go (relativistic)", 0.25, L(0.80, 0.20), 40.0),
    Belief("B3 'a preferred foliation is unacceptable' (interpretation)", 0.5, None, 1.0, ground_truth_available=False),
]

GROUPS = {
    "Gleason n>=3": GLEASON,
    "QM reconstruction": RECONSTRUCTION,
    "BDGZ no-go": BDGZ,
}


def main() -> int:
    print("== C/P classification ==")
    for name, beliefs in GROUPS.items():
        v = detect_mode(beliefs)
        tail = f"  -- {', '.join(v.reasons)}" if v.reasons else ""
        print(f"  {name:20s} {v.mode.value:16s}{tail}")

    # Only the Mode-C (convergent) sub-lemmas may be EIG-ranked.
    convergent = [
        b
        for g in GROUPS.values()
        for b in g
        if b.ground_truth_available and b.likelihood is not None
    ]
    if not convergent:
        print("\nNo Mode-C sub-lemma to rank.")
        return 1

    order = rank_by_eig(convergent)
    print("\n== Mode-C sub-lemmas, ordered by EIG/cost ==")
    for name, score in order:
        print(f"  {score:6.4f}  {name}")
    print(f"\nNEXT: {order[0][0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
