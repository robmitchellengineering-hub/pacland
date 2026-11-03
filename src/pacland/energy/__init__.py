"""Energy — the discipline whose wall is not a number but a *decision*.

The other disciplines hit walls of measurement: climate has no ground truth, drugs has no assay,
economics has no counterfactual. This one hits a different wall — **the field cannot choose between
its own candidate theories**, and has not been able to for ninety years.

That makes it the right discipline for this repository, because PACLAND's method is exactly the thing
that is missing. The method is not "find the answer"; it is *state the claim so that it can die, run
the test, and record which limb it lost*. Applied to quantum gravity the method becomes a referee:
every candidate framework scored against every condition it must satisfy, at once, with `UNKNOWN`
where the evidence is absent.

Two arms live under this name:

* **energy claims** (registered separately, in ``docs/energy-conjectures.md``) — stored-energy ceilings,
  fusion scaling, and the energy cost of verification itself;
* **SEXTANT** — the gravitational sector: six candidate frameworks, thirteen conditions, and the
  equation each surviving framework must produce.

The rule for both arms is the repository's rule: a claim is published only with the observation that
would kill it, and a reading that the evidence does not support is recorded as ``UNKNOWN``, never as a
pass.
"""
from __future__ import annotations

from .lattice import (
    CANDIDATES,
    CONSTRAINTS,
    EVIDENCE_CLASSES,
    MACHINES,
    Candidate,
    Constraint,
    Evidence,
    table,
    verdict,
)
from .referee import render, run, self_test, summarise

__all__ = [
    "CANDIDATES",
    "CONSTRAINTS",
    "EVIDENCE_CLASSES",
    "MACHINES",
    "Candidate",
    "Constraint",
    "Evidence",
    "table",
    "verdict",
    "render",
    "run",
    "self_test",
    "summarise",
]
