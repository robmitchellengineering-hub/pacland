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
    "phillips-isotherm": {
        "law": "inflation × unemployment is bounded (the hyperbolic trade-off)",
        "check": lambda m: m.get("phillips") == "hyperbolic"},
    "supply-demand-restoring": {
        "law": "price is pulled back to equilibrium by excess demand (Hooke's law)",
        "check": lambda m: m.get("price_dynamics") == "restoring"},
    "nash-fixed-point": {
        "law": "the equilibrium is a fixed point of the best-response map",
        "check": lambda m: m.get("equilibrium") == "fixed-point"},
    "solow-relaxation": {
        "law": "capital converges to its steady state (relaxation)",
        "check": lambda m: m.get("growth") == "converges"},
    "interest-exponential": {
        "law": "value compounds/decays exponentially (dx/dt = λx)",
        "check": lambda m: m.get("value_dynamics") == "exponential"},
    "multiplier-geometric": {
        "law": "the spending rounds sum to 1/(1−c) (a geometric series)",
        "check": lambda m: m.get("multiplier") == "geometric"},
    "diversification-clt": {
        "law": "portfolio variance falls as 1/N (the central limit)",
        "check": lambda m: m.get("diversification") == "1/N"},
    "laffer-critical": {
        "law": "revenue has a single maximum (a critical point)",
        "check": lambda m: m.get("laffer") == "single-peak"},
    "epidemic-threshold": {
        "law": "an outbreak grows iff R0 = β/γ > 1 (the percolation threshold)",
        "check": lambda m: m.get("spread") == ("yes" if m.get("R0", 0) > 1 else "no")},
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


# The solver layer: once the surviving MODEL is identified, its hard-science SOLVER yields the numbers.
SOLVERS: dict[str, object] = {
    "thermal + super-rich": lambda m: {
        "mean wealth (T)": m.get("T", 1.0),
        "Pareto tail exponent α": m.get("alpha", 1.6),
        "prediction": "the bulk is exponential with scale T; the tail decays as w^{−α}"},
    "van der Pol limit cycle": lambda m: {
        "limit-cycle amplitude": 2.0, "period (approx)": 2 * 3.14159,
        "prediction": "the cycle is sustained at amplitude ≈ 2 regardless of the shock that started it"},
    "hyperbolic Phillips": lambda m: {
        "isotherm constant k": m.get("k", 10.0),
        "prediction": "inflation × unemployment ≈ k — you cannot lower both at once"},
    "tatonnement gradient flow": lambda m: {
        "equilibrium price p*": m.get("p_star", 4.0),
        "convergence rate": m.get("rate", 2.0),
        "prediction": "the price converges to p* exponentially at that rate"},
    "epidemic": lambda m: {
        "R0": m.get("R0", 1.5), "spreads": m.get("R0", 1.5) > 1,
        "prediction": "the outbreak grows iff R0 > 1"},
}


def solve_survivor(question: str, candidates: list[dict], constraint_names: list[str]) -> dict:
    """Constraint-first elimination + the solver: the surviving model, AND its concrete numbers."""
    r = constraint_first(question, candidates, constraint_names)
    if r["survivors"]:
        name = r["survivors"][0]
        model = next(c for c in candidates if c["name"] == name)
        solver = SOLVERS.get(name)
        r["solution"] = solver(model) if solver else {}
    return r
