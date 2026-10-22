"""The sweep — find the minimal check-set that covers a claim's failure modes.

Implements the machine + sweep of ``docs/verification-config.md``. A *check* is
``input -> (ok, msg)``; a *failure mode* is a function that turns the good input
into one where that mode is the truth. ``sweep`` measures the coverage matrix
(inject each mode, observe which checks go red), then finds the minimal set cover
— the fewest checks that still catch every failure mode. That set is the
discipline's "N independent checks"; N is whatever the cover needs, never a
fixed ritual.

Pure stdlib.
"""
from __future__ import annotations


def measure_coverage(checks, failure_modes, base) -> list[list[int]]:
    """Coverage matrix ``C[i][j]`` = 1 if check i goes red when mode j is injected."""
    C = []
    for _name, check in checks:
        row = []
        for _mode_name, mutate in failure_modes:
            ok, _ = check(mutate(base))
            row.append(0 if ok else 1)
        C.append(row)
    return C


def minimal_cover(coverage: list[list[int]]) -> list[int] | None:
    """Greedy set cover: the fewest check indices covering every failure mode.

    Returns ``None`` when some mode is caught by no check — the config is blind
    to that failure mode, which is the honest signal, never a silent pass.
    """
    n_checks = len(coverage)
    n_modes = len(coverage[0]) if coverage else 0
    uncovered = set(range(n_modes))
    chosen: list[int] = []
    while uncovered:
        best = max(range(n_checks),
                   key=lambda i: sum(coverage[i][j] for j in uncovered))
        caught = sum(coverage[best][j] for j in uncovered)
        if caught == 0:
            return None
        chosen.append(best)
        uncovered -= {j for j in uncovered if coverage[best][j]}
    return chosen


def sweep(checks, failure_modes, base) -> dict:
    """Run the sweep and return the config.

    ``checks`` is ``[(name, fn)]``; ``failure_modes`` is ``[(name, mutator)]``.
    Returns ``complete`` True with the minimal check names, or False naming the
    failure modes no check catches (a blind spot, reported loudly).
    """
    coverage = measure_coverage(checks, failure_modes, base)
    chosen = minimal_cover(coverage)
    if chosen is None:
        uncovered = [
            failure_modes[j][0]
            for j in range(len(failure_modes))
            if all(coverage[i][j] == 0 for i in range(len(checks)))
        ]
        return {
            "names": [],
            "n_checks": 0,
            "coverage": coverage,
            "complete": False,
            "uncovered_modes": uncovered,
        }
    return {
        "names": [checks[i][0] for i in chosen],
        "n_checks": len(chosen),
        "coverage": coverage,
        "complete": True,
        "uncovered_modes": [],
    }


__all__ = ["measure_coverage", "minimal_cover", "sweep"]
