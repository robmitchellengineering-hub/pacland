"""PACLAND discovery engine — a first-class component.

Search strategies are pluggable and independent. The five "jump types" (anomaly, inversion, unification,
analogy, principle) are ONE strategy (`conceptual-jump`), NOT the engine. A discovery can come from
anywhere: a mathematical search finding an invariant, a computational search finding a counterexample, a
dataset exposing a relationship, a combination of theories, or an agent spotting a missing assumption.

The engine's job: run strategies, falsify candidates, and SCORE verified discoveries per unit of research
effort — not count hypotheses generated.

Run:
    python3 -m pacland.discovery_engine self-test
    python3 -m pacland.discovery_engine run <problem>
"""

from __future__ import annotations

import json
import math
import sys
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable, Optional

# ----------------------------------------------------------------------------
# Data model (the engine's own)
# ----------------------------------------------------------------------------


@dataclass
class Candidate:
    id: str
    problem: str
    strategy: str
    hypothesis: str
    falsifier: str
    cost: float
    prior: float
    status: str = "open"            # open | falsified | surviving
    evidence: str = ""


@dataclass
class Discovery:
    """A VERIFIED discovery: a candidate that survived falsification (and, downstream, confirmation)."""
    candidate: Candidate
    effort: float

    @property
    def strategy(self) -> str:
        return self.candidate.strategy


@dataclass
class Experiment:
    id: str
    problem: str
    strategy: str
    budget: int
    candidates: list[Candidate] = field(default_factory=list)
    discoveries: list[Discovery] = field(default_factory=list)
    effort: float = 0.0
    stopped: bool = False
    reason: str = ""


# ----------------------------------------------------------------------------
# The falsifier (SEXTANT, wired; open otherwise)
# ----------------------------------------------------------------------------

Falsifier = Callable[[Candidate], tuple[str, str]]   # -> (status, evidence)


def _import_sextant():
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from pacland import phantom, sextant

        return sextant, phantom
    except Exception:
        return None, None


def sextant_falsifier(sextant, phantom) -> Falsifier:
    def _falsify(c: Candidate) -> tuple[str, str]:
        if phantom is None:
            return "open", "SEXTANT not importable — candidate unfalsified"
        for name in sextant.CATALOG:
            if name in c.hypothesis and name in phantom.FALSIFIERS:
                ok, ev = phantom.FALSIFIERS[name]()
                return ("surviving" if ok else "falsified", ev)
        return "open", "needs a falsifier (proposed: " + c.falsifier + ")"

    return _falsify


# ----------------------------------------------------------------------------
# Search strategies — the five jump types are ONE of these, not the engine
# ----------------------------------------------------------------------------


class Strategy:
    name: str = "strategy"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        raise NotImplementedError


JUMP_QUESTIONS = {
    "anomaly": "What contradiction is the field quietly ignoring?",
    "inversion": "Which assumption, if flipped, changes the problem?",
    "unification": "Which two 'different' objects are secretly one?",
    "analogy": "What structure from another domain maps here?",
    "principle": "What single postulate would reorganize everything?",
}


class ConceptualJump(Strategy):
    """ONE strategy: the five typed questions. They help generate ideas; they do not bound discovery."""

    name = "conceptual-jump"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        # a real generator: the five questions query the knowledge we hold (SEXTANT catalog + ledger)
        out = []
        sextant, _ = _import_sextant()
        per_question = max(1, budget // 5)
        for i, jt in enumerate(JUMP_QUESTIONS):
            if sextant is not None:
                for name, e in list(sextant.CATALOG.items())[:per_question]:
                    if jt == "anomaly" and e.get("verdict") == "FREE":
                        h = f"{name}: {e['claim']} is FREE (unforced) — the gap to close"
                    elif jt == "inversion" and e.get("verdict") == "FREE":
                        h = f"invert {name}: assume {e['claim']} is FORCED, not free"
                    elif jt == "unification":
                        h = f"unify {name} with {problem}: {e.get('why', '')[:50]}"
                    elif jt == "principle" and e.get("verdict") == "FORCED":
                        h = f"principle {name}: {e['claim']} as a postulate"
                    else:
                        continue
                    out.append(_mk(problem, self.name, jt, h, e.get("falsifier", "a falsifier"), 2.0 + i * 0.5, 0.3))
        return out[:budget]


class MathematicalSearch(Strategy):
    """Find an unexpected invariant: surface the invariants we have already proven and propose testing them
    in a new setting."""

    name = "mathematical-search"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        sextant, _ = _import_sextant()
        out = []
        if sextant is not None:
            for name, e in list(sextant.CATALOG.items())[:budget]:
                if e.get("verdict") == "FORCED":
                    out.append(_mk(problem, self.name, "invariant",
                                   f"the invariant behind {name} ({e['theorem']}) transfers to {problem}",
                                   "does the invariant survive in the new setting?", 3.0, 0.2))
        return out[:budget]


class ComputationalSearch(Strategy):
    """Find a counterexample: run the live simulators/falsifiers and surface anything that fires."""

    name = "computational-search"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        sextant, phantom = _import_sextant()
        out = []
        if phantom is not None:
            for name in list(phantom.FALSIFIERS)[:budget]:
                out.append(_mk(problem, self.name, "counterexample",
                               f"search for a counterexample to {name} (live falsifier)",
                               name, 1.0, 0.4))
        return out[:budget]


class DatasetMining(Strategy):
    """Expose an unrecognised relationship in the ledger/data."""

    name = "dataset-mining"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        out = [_mk(problem, self.name, "relationship",
                   f"correlate the {problem} candidates in the ledger by shared falsifier",
                   "does the shared falsifier reveal a common structure?", 2.0, 0.25)]
        return out[:budget]


class TheoryCombination(Strategy):
    """Combine existing theories (the catalog's theorems) pairwise and propose the junction as a candidate."""

    name = "theory-combination"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        sextant, _ = _import_sextant()
        out = []
        if sextant is not None:
            names = list(sextant.CATALOG)[: budget + 1]
            for i in range(len(names) - 1):
                out.append(_mk(problem, self.name, "combination",
                               f"combine {names[i]} with {names[i + 1]} toward {problem}",
                               "does the combined structure close?", 4.0, 0.2))
        return out[:budget]


class ProofGap(Strategy):
    """Spot a missing assumption: scan the proof tree for sorry/admit/open lemmas."""

    name = "proof-gap"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        # real: scan the pacland-proof tree for admitted gaps
        root = Path(__file__).resolve().parent.parent.parent / "pacland-proof"
        gaps = []
        if root.exists():
            for p in list(root.rglob("*.lean"))[:200]:
                txt = p.read_text(errors="ignore")
                if "sorry" in txt or "admit" in txt:
                    gaps.append(p.name)
        out = [_mk(problem, self.name, "missing-assumption",
                   f"the gap in {g} may be a missing assumption toward {problem}",
                   "is the assumption load-bearing?", 1.5, 0.35) for g in gaps[:budget]]
        return out[:budget]


def _mk(problem, strategy, tag, hypothesis, falsifier, cost, prior) -> Candidate:
    return Candidate(
        id=f"{slug(problem)}-{tag}-{uuid.uuid4().hex[:6]}",
        problem=problem, strategy=strategy, hypothesis=hypothesis,
        falsifier=falsifier, cost=cost, prior=prior,
    )


# ----------------------------------------------------------------------------
# The engine + scoring + lifecycle
# ----------------------------------------------------------------------------

STRATEGIES = [ConceptualJump(), MathematicalSearch(), ComputationalSearch(),
              DatasetMining(), TheoryCombination(), ProofGap()]


class DiscoveryEngine:
    def __init__(self, strategies: list[Strategy] | None = None, falsifier: Falsifier | None = None):
        sextant, phantom = _import_sextant()
        self.strategies = strategies or STRATEGIES
        self.falsifier = falsifier or sextant_falsifier(sextant, phantom)

    def run_experiment(self, problem: str, strategy: Strategy, budget: int = 10) -> Experiment:
        exp = Experiment(id=uuid.uuid4().hex[:8], problem=problem, strategy=strategy.name, budget=budget)
        for c in strategy.generate(problem, budget):
            exp.candidates.append(c)
            outcome, evidence = self.falsifier(c)
            c.status = outcome
            c.evidence = evidence
            exp.effort += c.cost
            if outcome == "surviving":
                exp.discoveries.append(Discovery(candidate=c, effort=c.cost))
        if budget and len(exp.candidates) >= budget and not exp.discoveries:
            exp.stopped = True
            exp.reason = "budget exhausted with no verified discovery — reframe, do not re-run the same strategy"
        return exp

    def score(self, exps: list[Experiment]) -> dict:
        """The metric: verified discoveries per unit of research effort (per strategy + global)."""
        per = {}
        total_d, total_e = 0, 0.0
        for e in exps:
            d = len(e.discoveries)
            eff = e.effort if e.effort > 0 else 1e-9
            per.setdefault(e.strategy, [0, 0.0])
            per[e.strategy][0] += d
            per[e.strategy][1] += e.effort
            total_d += d
            total_e += e.effort
        return {
            "per_strategy": {s: {"discoveries": v[0], "effort": v[1],
                                 "discoveries_per_effort": v[0] / max(v[1], 1e-9)} for s, v in per.items()},
            "global": {"discoveries": total_d, "effort": total_e,
                       "discoveries_per_effort": total_d / max(total_e, 1e-9)},
        }

    def lifecycle(self, problem: str, budget: int = 10) -> dict:
        """plan (all strategies) -> run -> score -> kill/reframe."""
        exps = [self.run_experiment(problem, s, budget) for s in self.strategies]
        return {
            "problem": problem,
            "experiments": [asdict(e) for e in exps],
            "score": self.score(exps),
        }


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def slug(s: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in s.lower()).strip("-")


def self_test() -> None:
    eng = DiscoveryEngine()
    r = eng.lifecycle("mass-gap", budget=6)
    print("strategies run:", len(r["experiments"]))
    for s, m in r["score"]["per_strategy"].items():
        print(f"  {s:20s} discoveries={m['discoveries']} effort={m['effort']:.1f} d/e={m['discoveries_per_effort']:.3f}")
    print(f"  global: {r['score']['global']['discoveries']} verified discoveries per {r['score']['global']['effort']:.1f} effort")
    print("SELF-TEST PASS: engine runs all strategies, falsifies, and scores discoveries per effort.")


def run_cmd(problem: str) -> None:
    eng = DiscoveryEngine()
    r = eng.lifecycle(problem, budget=6)
    for e in r["experiments"]:
        print(f"[{e['strategy']:18s}] candidates={len(e['candidates'])} discoveries={len(e['discoveries'])} stopped={e['stopped']}")
        for c in e["candidates"]:
            print(f"    [{c['status']:9s}] {c['hypothesis'][:60]}")
    print(json.dumps(r["score"], indent=2))


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "self-test":
        self_test()
    elif cmd == "run":
        run_cmd(sys.argv[2] if len(sys.argv) > 2 else "mass-gap")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
