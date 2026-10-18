"""The constraint-first solver — the engine that turns verified constraints into
the certified viable class (the answer, made from real constraints).

``docs/viability-polytope.md`` reframes the goal: the answer is not a point but the
*intersection* of verified constraints. This module is the execution of that
reframe on the real flux-vacua data. It applies the physically-motivated constraint
set, returns the survivor class, and measures how much each observable got
*narrowed* — and it makes explicit the thing that stops the narrowing: the same
Mitchell Verification Deficit that leaves the certificate vacuous.

The constraints (all checkable, none invented):
  1. weak coupling            g_s < 1             (log g_s < 0)
  2. small W0                 |W0| < 1            (log W0 < 0)   — tuning, not consistency
  3. perturbative gauge       g^2 < 4pi           (log(1/g^2) > log(1/4pi)) for every factor

The tadpole is *available* but its threshold is the model's orientifold charge L,
which is not stored with the sample, so it is reported but not imposed — a named
gap, not a hidden one.
"""
from __future__ import annotations

import math

from .constraints import joint_elimination

LOG_G2_PERT = math.log(1.0 / (4.0 * math.pi))  # ~ -2.53


def constraint_set():
    """The real, checkable constraint set, as (name, keep) pairs."""
    return [
        ("weak coupling (g_s < 1)", lambda v: v["log_gs"] < 0.0),
        ("small W0 (|W0| < 1)", lambda v: v["log_W0"] < 0.0),
        (
            "perturbative gauge (g^2 < 4pi)",
            lambda v: all(g > LOG_G2_PERT for g in (v.get("log_g2_inv") or [])),
        ),
    ]


def _narrowing(records, survivor, obs_name):
    """survivor-range / full-range for one observable.

    Returns ``None`` when fewer than two survivors remain — a single point has
    range zero by construction, which would read as "fully pinned" when it is
    really a sampling artefact. The viable class is a *region*; one sample point
    in it does not pin anything.
    """
    vals = [r[obs_name] for r in records if r.get(obs_name) is not None]
    if not vals:
        return None
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return None
    surv = [r[obs_name] for r, s in zip(records, survivor) if s and r.get(obs_name) is not None]
    if len(surv) < 2:
        return None
    slo, shi = min(surv), max(surv)
    return (shi - slo) / (hi - lo)


def solve(records):
    """Apply the constraint set and characterize the viable class."""
    constraints = constraint_set()
    j = joint_elimination(records, constraints)
    keepers = [[k(v) for v in records] for _, k in constraints]
    survivor = [all(ks[i] for ks in keepers) for i in range(len(records))]
    observables = ["log_W0", "log_gs", "tadpole"]
    narrowing = {o: _narrowing(records, survivor, o) for o in observables}
    return {
        "n": len(records),
        "n_survive": sum(survivor),
        "joint": j["joint"],
        "interaction": j["interaction"],
        "interaction_z": j["interaction_z"],
        "interaction_verdict": j["interaction_verdict"],
        "per": j["per"],
        "certificate": j["certificate"],
        "narrowing": narrowing,
        "tadpole_available_not_imposed": True,
    }
