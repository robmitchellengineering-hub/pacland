"""validation_gate.py — the withheld-problem validation gate (action 5).

The non-negotiable gate: before placing confidence in the engine, it must demonstrate BLIND discovery —
solve a problem whose answer was withheld, with the falsifier verifying it AND a re-run reproducing it.
This is the honest answer to "has the engine actually discovered something new?", and it is the gate the
whole phase stands or falls on.
"""
from __future__ import annotations

from pacland import benchmarks as b
from pacland import registry


def run_withheld(generator, problem: dict) -> dict:
    """Induce a candidate for a withheld problem and falsify it (held-out prediction)."""
    pre = "points: " + ", ".join(f"({x},{y})" for x, y in problem["points"])
    cands = generator(pre)
    if not cands:
        return {"survived": False, "reason": "no candidate proposed", "jump": problem["jump"]}
    expr = cands[0]
    survived, evidence = b.falsify_law(expr, problem["points"] + [problem["held_out"]])
    return {"survived": survived, "evidence": evidence, "candidate": expr,
            "jump": problem["jump"]}


def reproducible(generator, problem: dict, n_seeds: int = 3) -> list[dict]:
    """Does the engine induce + survive the SAME withheld problem across re-runs? (The problem is held
    fixed; only the generator's own non-determinism varies.)"""
    return [run_withheld(generator, problem) for _ in range(n_seeds)]


def blind_discovery_gate(generator, n_problems: int = 5, n_seeds: int = 3) -> dict:
    """The gate. PASS iff the engine solves ≥1 withheld problem AND a re-run reproduces it.

    'solved' = the falsifier verified the candidate (held-out prediction). 'reproducible_solved' = it
    also survived every re-run. The verdict is recorded as an auditable claim.
    """
    suite = b.synthetic_induction_suite(n_problems, seed=0)
    solved = 0
    reproducible_solved = 0
    details: list[dict] = []
    for problem in suite:
        res = run_withheld(generator, problem)
        repro = reproducible(generator, problem, n_seeds)
        all_survive = all(r["survived"] for r in repro)
        solved += res["survived"]
        reproducible_solved += (res["survived"] and all_survive)
        details.append({"jump": problem["jump"], "survived": res["survived"],
                        "reproduced": all_survive,
                        "candidate": res.get("candidate")})
    passed = reproducible_solved == n_problems
    verdict = ("blind discovery established" if passed
               else "blind discovery NOT yet established")
    registry.record_claim(
        "claim-blind-discovery-gate",
        "the engine solves a withheld problem and a re-run reproduces it",
        "survived" if passed else "failed",
        problem="blind-discovery",
        reason=f"{reproducible_solved}/{n_problems} withheld problems solved and reproduced",
        produced_by="validation-gate",
    )
    return {"passed": passed, "solved": solved, "reproducible_solved": reproducible_solved,
            "n_problems": n_problems, "verdict": verdict, "details": details}
