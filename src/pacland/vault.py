"""The Verification Vault — approach #1.

Composes the Valiant Verification discipline into one pipeline:

    oracle (L2)  ->  guards  ->  (all pass?)  ->  certificate (L3)
                                  (any fail?)  ->  refuse — no certificate

The load-bearing invariant that makes this *verification* and not *compute*: a
computation that fails ANY guard emits NO certificate. Guards are admission
control — the "a skipped/neutral check is a fail, never a silent pass" rule,
applied to physics outputs.

Real oracle outputs (CYTools Hodge numbers, JAXVacua flux vacua, cymetric
metrics) plug in through ``oracle.adapters``; until then the exact toric toy in
``tests/test_vault.py`` exercises the full loop. Each guard has a seeded-fault
mutation proving it refuses the fault.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VaultVerdict:
    """Outcome of running one computation through the Vault."""

    passed: bool
    failures: tuple[str, ...]  # (name: message) for each violated guard
    message: str


def run_vault(oracle, genotype, guards) -> VaultVerdict:
    """Run a computation through the guards and admit or refuse it.

    ``oracle``    : callable(genotype) -> dict[name, value]
    ``guards``    : iterable of (name, check) where check(observables: dict)
                    -> (ok: bool, message: str)

    The verdict is ``passed`` only if every guard passes. A guard that cannot
    run (missing output) is treated as a failure, never a silent pass.
    """
    observables = oracle(genotype)
    failures: list[str] = []
    for name, check in guards:
        try:
            ok, msg = check(observables)
        except Exception as exc:  # a guard that errors is a failure, not a pass
            ok, msg = False, f"guard raised {type(exc).__name__}: {exc}"
        if not ok:
            failures.append(f"{name}: {msg}")
    if failures:
        return VaultVerdict(False, tuple(failures), "guard failure — no certificate")
    return VaultVerdict(True, (), "all guards passed — certificate may be minted")


__all__ = ["VaultVerdict", "run_vault"]
