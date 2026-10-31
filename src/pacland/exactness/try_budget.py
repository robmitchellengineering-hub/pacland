"""The try-budget wrapper — spending a stated budget on a sampler that counts something else.

`sample_critical_points(..., n_target=N)` asks for **points**, not tries. The library caps its own search at 400
tries per call, so a "1200-try" run silently does 400 (this is T1's blocker: the escalation never happened).

**What can be observed from outside** is calls, points and wall-clock — *not* tries. So this wrapper's budget is
stated in the units the API actually exposes, and the try count is reported as **unknown** rather than inferred:

    calls     how many times the sampler was invoked
    seconds   wall-clock spent
    points    total critical points accumulated
    yield     points per call and per second

That is a weaker budget than "tries" and it is the honest one. Inferring tries from calls would repeat the
mistake this module exists to prevent.

Run:        python3 scripts/try_budget.py    (a dry sampler; the real one needs the node)
Guarded by: tests/test_try_budget.py
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class BudgetRun:
    """What a budgeted run can honestly report."""
    calls: int = 0
    points: list = field(default_factory=list)
    per_call: list = field(default_factory=list)
    seconds: float = 0.0
    stopped_because: str = ""

    @property
    def tries(self) -> str:
        return "unknown (the sampler does not expose its try count)"

    @property
    def yield_per_call(self) -> float:
        return len(self.points) / self.calls if self.calls else 0.0

    @property
    def yield_per_second(self) -> float:
        return len(self.points) / self.seconds if self.seconds else 0.0


def run_to_budget(sampler, calls: int = 5, seconds: float | None = None,
                  stop_when_found: int | None = None) -> BudgetRun:
    """Invoke `sampler()` until the **call** budget (and an optional wall-clock budget) is spent.

    `sampler()` must return a list of points. `stop_when_found` stops early once that many points exist — useful
    when the question is "is there any?", where the first hit ends the search.
    """
    run = BudgetRun()
    t0 = time.monotonic()
    while run.calls < calls:
        got = list(sampler() or [])
        run.calls += 1
        run.per_call.append(len(got))
        run.points.extend(got)
        if stop_when_found is not None and len(run.points) >= stop_when_found:
            run.stopped_because = f"found {len(run.points)} point(s) after {run.calls} call(s)"
            break
        if seconds is not None and (time.monotonic() - t0) >= seconds:
            run.stopped_because = f"wall-clock budget of {seconds}s spent after {run.calls} call(s)"
            break
    run.seconds = time.monotonic() - t0
    if not run.stopped_because:
        run.stopped_because = f"call budget of {calls} spent"
    return run


def dry_sampler(script):
    """A deterministic stand-in for the real sampler — used by the tests and the dry run."""
    it = iter(script)

    def sample():
        try:
            return list(next(it))
        except StopIteration:
            return []
    return sample


__all__ = ["BudgetRun", "run_to_budget", "dry_sampler"]
