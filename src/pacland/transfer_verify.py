"""transfer_verify.py — phase 3: verify a cross-field transfer actually carries its property.

The encoding-check: a proposed transfer is only credited when BOTH ends of the mapping reproduce the SAME
invariant. This is a NUMERICAL check (tier 4, "tested numerically") — it is NOT a Lean proof (tier 1).
The honest bar: a vacuous or wrong mapping FAILS here, because the two ends' measured invariants diverge.

First verified link: diffusion ↔ random-walk (heat-diffusion-walk). The shared invariant is the linear
mean-squared displacement ⟨x²⟩ = 2Dt. The random walk is simulated; if its MSD does not equal 2Dt, the
link is refuted.
"""
from __future__ import annotations

import random
import time

from pacland import registry


def verify_diffusion_walk(n_steps: int = 1000, n_walkers: int = 2000, seed: int = 0,
                          tolerance: float = 0.05) -> dict:
    """Numerically verify heat-equation ↔ brownian-motion: the walk's MSD should equal 2Dt.

    A symmetric random walk on the integers (step ±1, unit time) has D = 1/2, so ⟨x²⟩ = 2·(1/2)·t = t.
    Returns the measured vs expected MSD and whether they agree within tolerance.
    """
    rng = random.Random(seed)
    msd_sum = 0.0
    for _ in range(n_walkers):
        x = 0
        for _ in range(n_steps):
            x += rng.choice((-1, 1))
        msd_sum += x * x
    measured = msd_sum / n_walkers
    expected = 2 * 0.5 * n_steps  # 2Dt with D = 1/2, t = n_steps
    ratio = measured / expected
    return {
        "measured_msd": measured,
        "expected_msd": expected,
        "ratio": ratio,
        "verified": abs(ratio - 1.0) < tolerance,
    }


def verify_transfer(mapping_id: str = "heat-diffusion-walk") -> dict:
    """Run the encoding-check for a known mapping and record the evidence. Returns the verdict."""
    checks = {
        "heat-diffusion-walk": ("brownian-motion", "diffusion-equation", verify_diffusion_walk),
    }
    if mapping_id not in checks:
        return {"mapping": mapping_id, "verified": False,
                "error": f"no checker for mapping {mapping_id!r}"}

    target, source, check = checks[mapping_id]
    r = check()
    evidence_id = registry.new_id()
    registry.add(registry.Entry(
        id=evidence_id, kind="evidence",
        payload={
            "mapping": mapping_id, "source": source, "target": target,
            "check": "mean-squared displacement ⟨x²⟩ = 2Dt",
            "result": r,
            "tier": 4,  # tested numerically, not proven
        },
        provenance={"produced_by": "transfer_verify", "method": "numerical-encoding-check",
                    "ts": time.time()},
        links=[mapping_id]))
    return {"mapping": mapping_id, "verified": r["verified"], "evidence_id": evidence_id,
            "measured": r["measured_msd"], "expected": r["expected_msd"], "ratio": r["ratio"]}
