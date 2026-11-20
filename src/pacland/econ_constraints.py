"""econ_constraints.py — constraint-first economics: use the proven hard-science laws as CONSTRAINTS.

Each verified unification is a PROVEN law (a hard-science theorem applied to economics). A valid economic
model must satisfy ALL the laws that apply to it; a model that violates any one is refuted. This is the
constraint-first methodology: decompose a question into FORCED (the constraints) + OPEN (the rest), and the
solution is the model that satisfies every forced constraint. The power is the INTERSECTION: several
constraints together narrow the valid model space dramatically.
"""
from __future__ import annotations

# Each constraint: name → (the law, a checker that returns True iff the model satisfies it).
CONSTRAINTS: dict[str, dict] = {
    "wealth-boltzmann-bulk": {
        "law": "the wealth bulk is exponential P(w) ∝ e^{−w/T} (thermal equilibrium)",
        "check": lambda m: m.get("bulk") == "exponential"},
    "wealth-pareto-tail": {
        "law": "the wealth tail is a power law P(w) ∝ w^{−(α+1)} (Pareto)",
        "check": lambda m: m.get("tail") == "power-law"},
    "wealth-conserved": {
        "law": "total wealth is conserved (closed exchange)",
        "check": lambda m: m.get("conserved", False) is True},
    "business-cycle-limit-cycle": {
        "law": "the cycle is SUSTAINED and amplitude-independent of start (a limit cycle)",
        "check": lambda m: m.get("cycle") == "limit-cycle"},
    "goodwin-conserved": {
        "law": "the employment-wage cycle has a conserved first integral (Lotka-Volterra)",
        "check": lambda m: m.get("goodwin") == "conservative"},
    "tatonnement-converges": {
        "law": "the price converges to the equilibrium (a gradient flow)",
        "check": lambda m: m.get("convergence") == "converges"},
    "quantity-theory": {
        "law": "MV = PY (the quantity theory / ideal gas law)",
        "check": lambda m: m.get("mv_py", False) is True},
    "capm-linear": {
        "law": "expected return is linear in beta (the security market line)",
        "check": lambda m: m.get("capm") == "linear"},
}


def check_model(model: dict, constraint_names: list[str]) -> dict:
    """Check a candidate model against a set of constraints. Returns {satisfied, violated, valid, verdict}."""
    satisfied, violated = [], []
    for name in constraint_names:
        c = CONSTRAINTS[name]
        (satisfied if c["check"](model) else violated).append(name)
    return {"satisfied": satisfied, "violated": violated,
            "valid": not violated,
            "verdict": "VALID — satisfies all constraints" if not violated
                       else f"REFUTED — violates {len(violated)}: {', '.join(violated)}"}


def constraint_first(question: str, candidates: list[dict], constraint_names: list[str]) -> dict:
    """The constraint-first analysis: which candidate models survive ALL the forced constraints?"""
    for cand in candidates:
        cand["result"] = check_model(cand, constraint_names)
    survivors = [c for c in candidates if c["result"]["valid"]]
    return {
        "question": question,
        "forced_constraints": [CONSTRAINTS[n]["law"] for n in constraint_names],
        "candidates": candidates,
        "survivors": [c["name"] for c in survivors],
        "answer": (survivors[0]["name"] if survivors else "none — every candidate is refuted"),
    }
