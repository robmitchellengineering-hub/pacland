"""The belief ledger — numeric degrees of belief, updated by evidence.

The deterministic ledger records what is exact. This ledger records what we believe about the
*open* questions: each hypothesis carries a posterior probability, moved by every test result via
Bayes' rule. Each update is a generation, so a belief shifted by evidence is a posterior, not a
pass log. Zoubin Ghahramani's point, applied to the ledger: Bayesian updating does continual
learning without catastrophic forgetting, so the record converges instead of flip-flopping.

Usage:
    python -m pacland.belief_ledger demo
"""
from __future__ import annotations

import sys

from pacland import belief, hypotheses


class BeliefLedger:
    """A store of belief states with their update history."""

    def __init__(self) -> None:
        self.beliefs: dict[str, belief.Belief] = {}
        self.history: list[dict] = []

    @classmethod
    def from_stated(cls) -> "BeliefLedger":
        ledger = cls()
        for s in hypotheses.stated_beliefs():
            ledger.beliefs[s["name"]] = belief.Belief(
                name=s["name"], prior=s["prior"],
                likelihood=belief.Likelihood(s["tp"], s["fp"]), cost=s["cost"])
        return ledger

    def record_result(self, name: str, positive: bool) -> belief.Belief:
        """Apply one test result to a hypothesis and append the move to history."""
        before = self.beliefs[name]
        after = belief.update(before, positive)
        self.beliefs[name] = after
        self.history.append({"name": name, "positive": positive,
                             "prior": before.prior, "posterior": after.prior})
        return after

    def report(self) -> dict[str, float]:
        """Current posteriors, highest first."""
        return {name: b.prior for name, b in
                sorted(self.beliefs.items(), key=lambda kv: -kv[1].prior)}


def main(argv: list[str]) -> int:
    ledger = BeliefLedger.from_stated()
    print("belief ledger — posterior per hypothesis (from stated priors):")
    for name, p in ledger.report().items():
        print(f"  {name:<24s} P = {p:.3f}")

    # one hypothesis, updated by a run of consistent positive evidence (falsifier never triggers)
    print("\n  ym-mass-gap, updated by five clean tests (falsifier never triggers):")
    for i in range(5):
        after = ledger.record_result("ym-mass-gap", positive=True)
        print(f"    test {i + 1}: P = {after.prior:.4f}")

    # and one hit of negative evidence (the falsifier triggers)
    after = ledger.record_result("ym-mass-gap", positive=False)
    print(f"    then one falsifier trigger: P = {after.prior:.4f}")

    print("\n  Reading: the posterior rises with consistent evidence and falls on a single")
    print("  falsifier trigger — the ledger converges, it does not flip-flop.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
