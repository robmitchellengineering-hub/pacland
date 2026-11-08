"""Animal communication — constraint-first (discipline/animal).

Decoding animal communication is an underdetermined inverse problem; the move is to
measure the constraints (the only learnable structure), not the meaning (graded, never
deterministic). See docs/animal-constraint-first.md.
"""
from .learnability import (  # noqa: F401
    winsorize,
    ridge_cv_balanced_accuracy,
    ridge_cv_pearson,
    permutation_z,
    single_coord_mi,
    referent_verdict,
    learnability_split,
)

__all__ = [
    "winsorize",
    "ridge_cv_balanced_accuracy",
    "ridge_cv_pearson",
    "permutation_z",
    "single_coord_mi",
    "referent_verdict",
    "learnability_split",
]
