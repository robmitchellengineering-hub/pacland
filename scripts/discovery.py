#!/usr/bin/env python3
"""
The discovery loop — an executable, repeatable system for hunting jumps.

This turns docs/DISCOVERY-PROCESS.md, docs/CANDIDATE-LEDGER.md, docs/KILL-CRITERIA.md and
docs/RETRODICTION-TEST.md into runnable code. The generator and falsifier are PLUGGABLE: ship a
deterministic stub so the system runs and self-tests without an LLM; drop in an LLM-backed generator
later without changing the loop.

Run:
    python3 scripts/discovery.py self-test        # prove the loop + ledger + retrodiction execute
    python3 scripts/discovery.py run <problem>    # one loop, generator/falsifier = stubs
    python3 scripts/discovery.py retrodict         # taxonomy arm vs baseline arm on the toy dataset

No dependencies beyond the Python standard library.
"""

import json
import math
import sys
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable, Optional

# ----------------------------------------------------------------------------
# The five jump types (from DISCOVERY-PROCESS.md)
# ----------------------------------------------------------------------------

JUMP_TYPES = ("anomaly", "inversion", "unification", "analogy", "principle")

FIVE_QUESTIONS = {
    "anomaly": "What contradiction is the field quietly ignoring?",
    "inversion": "Which assumption, if flipped, changes the problem?",
    "unification": "Which two 'different' objects are secretly one?",
    "analogy": "What structure from another domain maps here?",
    "principle": "What single postulate would reorganize everything?",
}

# ----------------------------------------------------------------------------
# Candidate + Ledger (CANDIDATE-LEDGER.md)
# ----------------------------------------------------------------------------


@dataclass
class Candidate:
    id: str
    problem: str
    jump_type: str
    hypothesis: str
    falsifier: str
    cost: float
    prior: float
    status: str = "open"            # open | falsified | surviving
    evidence: str = ""
    posterior: Optional[float] = None
    info_gain: float = 0.0

    @property
    def brier(self) -> Optional[float]:
        """(prior - outcome)^2 when resolved; outcome 1 = survived, 0 = falsified."""
        if self.status == "surviving":
            return (self.prior - 1.0) ** 2
        if self.status == "falsified":
            return (self.prior - 0.0) ** 2
        return None


class Ledger:
    """A JSON-backed store of candidates with the belief-layer math."""

    def __init__(self, path: Path):
        self.path = path
        self.entries: list[Candidate] = []
        if path.exists():
            data = json.loads(path.read_text())
            self.entries = [Candidate(**e) for e in data.get("entries", [])]

    def add(self, c: Candidate) -> None:
        self.entries.append(c)

    def resolve(self, cid: str, outcome: str, evidence: str, posterior: Optional[float] = None) -> None:
        c = self.get(cid)
        c.status = outcome            # "falsified" | "surviving"
        c.evidence = evidence
        c.posterior = posterior if posterior is not None else (1.0 if outcome == "surviving" else 0.0)
        c.info_gain = binary_entropy(c.prior)  # a decisive test collapses entropy to 0

    def get(self, cid: str) -> Candidate:
        for c in self.entries:
            if c.id == cid:
                return c
        raise KeyError(cid)

    def open(self) -> list[Candidate]:
        return [c for c in self.entries if c.status == "open"]

    def resolved(self) -> list[Candidate]:
        return [c for c in self.entries if c.status in ("falsified", "surviving")]

    def brier_score(self) -> Optional[float]:
        """Mean (prior - outcome)^2 over resolved entries. Skill = 0.25; our measured prior = 0.41."""
        bs = [c.brier for c in self.resolved()]
        bs = [b for b in bs if b is not None]
        return sum(bs) / len(bs) if bs else None

    def rank_by_eig(self) -> list[Candidate]:
        """Open candidates by expected information gain per cost (binary_entropy(prior) / cost), descending."""
        return sorted(self.open(), key=lambda c: binary_entropy(c.prior) / max(c.cost, 1e-9), reverse=True)

    def save(self) -> None:
        self.path.write_text(json.dumps({"entries": [asdict(c) for c in self.entries]}, indent=2))


def binary_entropy(p: float) -> float:
    """H(p) = -[p log p + (1-p) log(1-p)] in nats."""
    p = min(max(p, 1e-9), 1 - 1e-9)
    return -(p * math.log(p) + (1 - p) * math.log(1 - p))


# ----------------------------------------------------------------------------
# Kill criteria (KILL-CRITERIA.md)
# ----------------------------------------------------------------------------


@dataclass
class KillState:
    budget: int = 10                 # K candidates per rung
    tried: int = 0
    survivors: int = 0
    stopped: bool = False
    reason: str = ""


def apply_kill_criteria(ledger: Ledger, ks: KillState) -> KillState:
    """After a candidate resolves, decide whether the rung is exhausted."""
    if ks.tried >= ks.budget and ks.survivors == 0:
        ks.stopped = True
        ks.reason = (
            f"budget {ks.budget} exhausted with no survivor — the framing is dead; "
            f"invert an assumption and restart (do not re-prompt the same five questions)."
        )
    return ks


# ----------------------------------------------------------------------------
# The loop (DISCOVERY-PROCESS.md)
# ----------------------------------------------------------------------------

# A generator maps (problem, jump_type) -> list of (hypothesis, falsifier, cost, prior).
# A falsifier maps (candidate) -> ("falsified" | "surviving", evidence).
Generator = Callable[[str, str], list[tuple[str, str, float, float]]]
Falsifier = Callable[[Candidate], tuple[str, str]]


def run_loop(
    problem: str,
    generator: Generator,
    falsifier: Falsifier,
    ledger: Ledger,
    budget: int = 10,
    typed: bool = True,
) -> KillState:
    """One jump-seeking loop with the kill criteria. Returns the stop state."""
    ks = KillState(budget=budget)
    for jt in JUMP_TYPES:
        if ks.stopped:
            break
        for (hyp, fal, cost, prior) in generator(problem, jt if typed else "none"):
            c = Candidate(
                id=f"{slug(problem)}-{jt[:3]}-{uuid.uuid4().hex[:6]}",
                problem=problem,
                jump_type=jt if typed else "none",
                hypothesis=hyp,
                falsifier=fal,
                cost=cost,
                prior=prior,
            )
            ledger.add(c)
            outcome, evidence = falsifier(c)
            ledger.resolve(c.id, outcome, evidence)
            ks.tried += 1
            if outcome == "surviving":
                ks.survivors += 1
            apply_kill_criteria(ledger, ks)
            if ks.stopped:
                break
        if ks.stopped:
            break
    return ks


# ----------------------------------------------------------------------------
# Retrodiction (RETRODICTION-TEST.md): taxonomy arm vs baseline arm
# ----------------------------------------------------------------------------


def score_arm(problem: str, generator: Generator, falsifier: Falsifier, true_jump: str, budget: int = 10, typed: bool = True) -> dict:
    """Return {rank, cost, survivors} for one arm on one historical problem."""
    ledger = Ledger(Path("/tmp/_retrodict_ledger.json"))
    ks = run_loop(problem, generator, falsifier, ledger, budget=budget, typed=typed)
    rank, cost = None, 0.0
    for i, c in enumerate(ledger.entries):
        cost += c.cost
        if c.hypothesis == true_jump:
            rank = i + 1
            break
    return {
        "rank": rank,                 # None = the true jump was never generated
        "cost_to_jump": cost if rank is not None else None,
        "survivors": ks.survivors,
    }


# ----------------------------------------------------------------------------
# Deterministic stubs (prove the system executes; swap for LLM-backed later)
# ----------------------------------------------------------------------------

# The withheld jumps of the toy dataset, by problem.
TOY_JUMPS = {
    "blackbody": "energy is quantised, E = h nu",
    "photoelectric": "light is made of quanta (photons)",
    "perihelion": "gravity is spacetime curvature (GR)",
}

# taxonomy arm: typed generator. Each problem's true jump is emitted only under its HISTORICAL jump
# type; the other four types emit distractors. This makes the five questions distinguishable.
TRUE_TYPE = {"blackbody": "principle", "photoelectric": "principle", "perihelion": "analogy"}

_TRUE = {
    "blackbody": ("energy is quantised, E = h nu", "fits the whole spectrum", 2.0, 0.3),
    "photoelectric": ("light is made of quanta (photons)", "predicts the frequency threshold", 2.0, 0.3),
    "perihelion": ("gravity is spacetime curvature (GR)", "predicts 43 arcsec/century", 2.0, 0.3),
}

_DISTRACTORS = {
    "blackbody": [("the emitter is granular (atoms)", "fails short-wavelength tail", 3.0, 0.2),
                  ("a new long-range force", "no such force observed", 4.0, 0.1)],
    "photoelectric": [("the metal's electrons are quantised", "predicts the wrong threshold", 3.0, 0.2)],
    "perihelion": [("a hidden planet (Vulcan)", "not found where predicted", 3.0, 0.2)],
}


def typed_generator(problem: str, jt: str) -> list[tuple[str, str, float, float]]:
    if problem not in _TRUE:
        return []
    if jt == TRUE_TYPE[problem]:
        return [_TRUE[problem]] + _DISTRACTORS.get(problem, [])
    return _DISTRACTORS.get(problem, [])


# baseline arm: untyped generator that omits the true jump (a weak straw-man baseline, for the demo).
def baseline_generator(problem: str, jt: str) -> list[tuple[str, str, float, float]]:
    red = {
        "blackbody": [
            ("the emitter is granular (atoms)", "fails short-wavelength tail", 3.0, 0.2),
            ("a new long-range force", "no such force observed", 4.0, 0.1),
        ],
        "photoelectric": [("the metal's electrons are quantised", "predicts the wrong threshold", 3.0, 0.2)],
        "perihelion": [("a hidden planet (Vulcan)", "not found where predicted", 3.0, 0.2)],
    }
    return red.get(problem, [])


# A falsifier: the toy dataset's true jump survives; everything else is falsified.
def toy_falsifier(c: Candidate) -> tuple[str, str]:
    if c.hypothesis == TOY_JUMPS.get(c.problem):
        return "surviving", "matches the historical confirmation"
    return "falsified", "fails the historical test"


def slug(s: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in s.lower()).strip("-")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def self_test() -> None:
    ledger = Ledger(Path("/tmp/_discovery_self_test.json"))
    ks = run_loop("blackbody", typed_generator, toy_falsifier, ledger, budget=10)
    print("loop: tried=%d survivors=%d stopped=%s" % (ks.tried, ks.survivors, ks.stopped))
    print("ledger brier:", ledger.brier_score())
    print("ranked by EIG/cost:", [c.id for c in ledger.rank_by_eig()])
    # retrodiction: taxonomy must rank the true jump higher than baseline
    tax = score_arm("blackbody", typed_generator, toy_falsifier, TOY_JUMPS["blackbody"])
    base = score_arm("blackbody", baseline_generator, toy_falsifier, TOY_JUMPS["blackbody"])
    print("retrodict blackbody: taxonomy rank=%s, baseline rank=%s" % (tax["rank"], base["rank"]))
    # honest toy claim: the taxonomy arm GENERATES the true jump (rank is not None); the baseline never does.
    assert tax["rank"] is not None and base["rank"] is None, "taxonomy must generate the jump, baseline must not"
    print("SELF-TEST PASS: loop, ledger (brier/EIG), kill criteria, and retrodiction all execute.")


def run_cmd(problem: str) -> None:
    ledger = Ledger(Path("/tmp/_discovery_run.json"))
    ks = run_loop(problem, typed_generator, toy_falsifier, ledger)
    for c in ledger.entries:
        print(f"[{c.status:9s}] {c.jump_type:10s} {c.hypothesis}")
    print("stop:", ks.reason if ks.stopped else "not stopped")


def retrodict_cmd() -> None:
    print("problem        taxonomy-rank  baseline-rank")
    for p in TOY_JUMPS:
        tax = score_arm(p, typed_generator, toy_falsifier, TOY_JUMPS[p])
        base = score_arm(p, baseline_generator, toy_falsifier, TOY_JUMPS[p])
        print(f"{p:14s} {str(tax['rank']):14s} {str(base['rank'])}")


# ----------------------------------------------------------------------------
# The real engine: wired to SEXTANT (falsifier) + a knowledge-base generator
# ----------------------------------------------------------------------------


def _import_sextant():
    """Import SEXTANT (the real yes/no engine) if present. Returns (sextant, phantom) or (None, None)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
        from pacland import phantom, sextant

        return sextant, phantom
    except Exception:
        return None, None


def knowledge_generator(sextant, phantom, problem: str, jt: str) -> list[tuple[str, str, float, float]]:
    """A REAL generator: the five questions become structured queries over SEXTANT's catalog + the
    ledger. Not an LLM's novel jump — a recombination of the knowledge we actually hold. The LLM-backed
    generator is the pluggable next step; this one runs today with no external API."""
    out: list[tuple[str, str, float, float]] = []
    if sextant is None:
        return out
    # Which catalog claims are anomalies/free/unforced for this problem? Their "why" fields carry the
    # assumptions to invert and the two-things-that-unify.
    for name, e in sextant.CATALOG.items():
        if e.get("verdict") == "FREE" and jt == "anomaly":
            out.append((f"{name}: {e['claim']} is FREE (unforced) — the gap to close", e["falsifier"], 2.0, 0.4))
        if jt == "inversion" and e.get("verdict") == "FREE":
            out.append((f"invert {name}: assume {e['claim']} is FORCED, not free", f"a derivation of {name}", 3.0, 0.3))
        if jt == "unification":
            out.append((f"unify {name} with the mass gap: {e.get('why', '')[:60]}", "a shared certificate", 4.0, 0.2))
        if jt == "principle" and e.get("verdict") == "FORCED":
            out.append((f"principle {name}: {e['claim']} as a postulate", e["falsifier"], 2.0, 0.5))
    return out[:3]


def sextant_falsifier(sextant, phantom, c: Candidate) -> tuple[str, str]:
    """The REAL falsifier: run SEXTANT's registered falsifier for a catalog claim; otherwise the
    candidate is open and needs a falsifier (proposed, not run)."""
    if phantom is None:
        return "open", "SEXTANT not importable (numpy/stim missing) — candidate unfalsified"
    # map the candidate's hypothesis back to a catalog claim name, if it names one
    for name in sextant.CATALOG:
        if name in c.hypothesis:
            if name in phantom.FALSIFIERS:
                ok, ev = phantom.FALSIFIERS[name]()
                return ("surviving" if ok else "falsified", ev)
    return "open", "needs a falsifier (proposed: " + c.falsifier + ")"


def engine_cmd(problem: str) -> None:
    """Run the loop with the REAL generator + SEXTANT falsifier."""
    sextant, phantom = _import_sextant()
    if sextant is None:
        print("SEXTANT not importable (needs src/pacland + numpy). Falling back to toy stubs.")
        run_cmd(problem)
        return
    ledger = Ledger(Path("/tmp/_discovery_engine.json"))
    gen = lambda p, jt: knowledge_generator(sextant, phantom, p, jt)  # noqa: E731
    fal = lambda c: sextant_falsifier(sextant, phantom, c)             # noqa: E731
    ks = run_loop(problem, gen, fal, ledger, budget=10)
    for c in ledger.entries:
        print(f"[{c.status:9s}] {c.jump_type:10s} {c.hypothesis[:70]}")
    if ks.stopped:
        print("stop:", ks.reason)
    print(f"brier={ledger.brier_score()}  open={len(ledger.open())}  survivors={ks.survivors}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "self-test":
        self_test()
    elif cmd == "run":
        run_cmd(sys.argv[2] if len(sys.argv) > 2 else "blackbody")
    elif cmd == "retrodict":
        retrodict_cmd()
    elif cmd == "engine":
        engine_cmd(sys.argv[2] if len(sys.argv) > 2 else "mass-gap")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
