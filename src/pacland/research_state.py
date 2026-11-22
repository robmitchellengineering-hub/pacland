"""research_state.py — the durable research supervisor (P2: mature autonomous operation).

The runner has a loop; this module gives it the SUPERVISOR the assessment asked for: task decomposition,
resource allocation (a budget per sub-task), retry policies, stopping criteria, and a durable research
state that survives sessions and crashes — so an autonomous campaign can stop, restart, and resume
without re-deriving what it already tried.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

STATUSES = ("pending", "running", "resolved", "failed", "exhausted")


@dataclass
class Task:
    id: str
    description: str
    status: str = "pending"
    attempts: int = 0
    max_attempts: int = 3          # retry policy: give up after this many failed attempts
    budget: float = 1.0            # resource allocation: this task's share of the run budget
    evidence: str = ""


@dataclass
class ResearchState:
    problem: str
    tasks: list[Task] = field(default_factory=list)
    round: int = 0
    max_rounds: int = 10           # stopping criterion: an outer cap
    budget: float = 10.0           # stopping criterion: total research effort
    spent: float = 0.0
    history: list[dict] = field(default_factory=list)

    # -- task decomposition -------------------------------------------------
    def decompose(self, descriptions: list[tuple[str, str, float]]) -> "ResearchState":
        """Turn a research goal into sub-tasks: (id, description, budget-share) each."""
        for i, (tid, desc, share) in enumerate(descriptions):
            self.tasks.append(Task(id=tid, description=desc, budget=share))
        return self

    # -- resource allocation -------------------------------------------------
    def next_task(self) -> Task | None:
        """The next unit of work: the first pending task, in allocation order."""
        for t in self.tasks:
            if t.status == "pending":
                t.status = "running"
                return t
        return None

    # -- retry policy --------------------------------------------------------
    def record_attempt(self, task_id: str, succeeded: bool, evidence: str) -> None:
        """Record one attempt: success resolves the task; failure retries up to max_attempts, then
        the task is EXHAUSTED (a recorded failed direction, not a silent retry loop)."""
        t = next((x for x in self.tasks if x.id == task_id), None)
        if t is None:
            return
        t.attempts += 1
        t.evidence = evidence
        self.spent += t.budget / max(t.max_attempts, 1)
        if succeeded:
            t.status = "resolved"
        elif t.attempts >= t.max_attempts:
            t.status = "exhausted"
        else:
            t.status = "pending"      # retry on a later round
        self.history.append({"task": task_id, "succeeded": succeeded, "evidence": evidence,
                             "ts": time.time()})

    # -- stopping criteria ----------------------------------------------------
    def should_stop(self) -> tuple[bool, str]:
        """Stop when (a) every task is resolved, or (b) the budget is spent, or (c) the round cap is
        reached, or (d) every outstanding task is exhausted (nothing left to retry)."""
        if all(t.status == "resolved" for t in self.tasks):
            return True, "all tasks resolved"
        if self.spent >= self.budget:
            return True, "budget exhausted"
        if self.round >= self.max_rounds:
            return True, "round cap reached"
        if self.tasks and all(t.status in ("resolved", "exhausted") for t in self.tasks):
            return True, "every task resolved or exhausted (nothing left to retry)"
        return False, ""

    def step(self) -> dict:
        """Advance one round: mark the round + return the stop verdict."""
        self.round += 1
        stopped, reason = self.should_stop()
        return {"round": self.round, "stopped": stopped, "reason": reason}

    # -- durable state --------------------------------------------------------
    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        return p

    @classmethod
    def load(cls, path: str | Path) -> "ResearchState":
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        s = cls(problem=d["problem"], round=d.get("round", 0),
                max_rounds=d.get("max_rounds", 10), budget=d.get("budget", 10.0),
                spent=d.get("spent", 0.0), history=d.get("history", []))
        s.tasks = [Task(**t) for t in d.get("tasks", [])]
        return s
