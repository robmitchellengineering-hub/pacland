"""Exactness instruments — the four kinds that work everywhere.

`docs/plan-exact-terms.md` groups the exactness available to this programme into eight kinds. Three of
them (topological, closed form at a locus, structural closure) exist only in special places; the four
below need no closed form and are therefore usable in the **interior** of moduli space, where every
vacuum we hold actually lives:

    X4  invariance            `invariance`   — change the description, the physics must not move
    X5  definitional identity `invariance`   — true by construction; a failure is a bug
    X7  finite-window exhaustion `windows`   — the lattice below a bound is finite, so enumeration is exact
    X8  known-answer control  `controls`     — the reference's answer is exact by construction

`identities` is the X5/X1 battery over the corpus itself: the first time the recorded vacua are checked
against the geometry they claim to come from.

Nothing here is a result. Each function states what it would falsify, and each one is tested for the
ability to go red — an exactness check that cannot fail is decoration.
"""
from . import controls, identities, invariance, windows  # noqa: F401

__all__ = ["controls", "identities", "invariance", "windows"]
