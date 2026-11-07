"""SEXTANT — the yes/no engine on the simulated quantum computer.

A sextant doesn't create the stars, it reads your position from them. SEXTANT doesn't create
quantum physics, it reads where each claim sits: FORCED (kernel-checked), FREE (delimited), or
IMPOSSIBLE (a no-go). This is the theorem registry + classifier — the first rung. The quantum
facts come from Phantom (Stim/Quimb) and the certificates from the Lean proof tower (pacland-proof/).

Usage:
    python -m pacland.sextant --list
    python -m pacland.sextant chsh
"""

from __future__ import annotations

import math

from pacland import phantom

# The theorem registry: every kernel-checked claim, its falsifier, its oracle class, and its verdict.
CATALOG: dict[str, dict] = {
    "chsh": {
        "claim": "no quantum state violates the CHSH inequality beyond 2√2",
        "simulate": phantom.chsh_value,  # live: Phantom computes S = 2√2
        "theorem": "QM.Tsirelson",
        "falsifier": "a state exceeding 2√2",
        "oracle": ["quantum-simulated (Phantom/Stim)", "kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the quantum maximum is the bound; the classical wall is 2 (QM.CHSH/Bell), so the "
               "free column is the gap [2, 2√2] — the entanglement that LOCC cannot create (QM.Entanglement).",
    },
    "no-cloning": {
        "claim": "no machine clones an arbitrary quantum state",
        "theorem": "QM.NoCloning",
        "falsifier": "a universal cloner",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "IMPOSSIBLE",
        "why": "linearity + unitarity forbid a map |ψ⟩|0⟩ → |ψ⟩|ψ⟩ for all |ψ⟩.",
    },
    "born-rule": {
        "claim": "the Born rule is the unique non-contextual probability rule",
        "theorem": "Gleason (Foundations/GleasonBridge)",
        "falsifier": "a second non-contextual probability rule",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "every frame function is Tr(ρP); the probability structure of QM is not chosen.",
    },
    "coupling-free": {
        "claim": "the gravitational coupling G is not derived",
        "theorem": "Gravity.QG.coupling_free",
        "falsifier": "a derivation of G from the forced halves",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FREE",
        "why": "∇·G = 0 involves no κ, so the Einstein equation is consistent for every κ ≠ 0 — "
               "G is a label, like N_gen and the 19.",
    },
    "gravity-quantum": {
        "claim": "the gravitational coupling must be quantum, not classical",
        "theorem": "QM.Entanglement + QM.NoCloning + Gleason",
        "falsifier": "a consistent classical (LOCC) coupling",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "a classical channel preserves separability (QM.Entanglement), so it cannot entangle; "
               "hence classical gravity cannot mediate the quantum correlation.",
    },
    "clifford-polynomial": {
        "claim": "Clifford/stabilizer circuits are classically simulable in polynomial time",
        "simulate": phantom.clifford_scaling,  # live: Stim runs 1000 qubits in polynomial time
        "theorem": "QM.Stabilizer.clifford_normalizes_pauli",
        "falsifier": "a T-gate circuit blowing past 2^n",
        "oracle": ["kernel-checked (Lean)", "quantum-simulated (Phantom/Stim)"],
        "verdict": "FORCED",
        "why": "the Clifford group normalizes the Pauli group, so stabilizer states stay a closed "
               "class (the algebraic core of Gottesman–Knill); the T gate is the single thing that escapes it.",
    },
    "entanglement-area": {
        "claim": "entanglement across a cut is bounded by the cut area D^m",
        "theorem": "QM.MERA",
        "falsifier": "entanglement exceeding D^m",
        "oracle": ["kernel-checked (Lean)", "quantum-simulated (Phantom/Quimb)"],
        "verdict": "FORCED",
        "why": "a sum of r = D^m simple tensors has simple rank ≤ r (the area law, the algebraic "
               "core of Ryu–Takayanagi / MERA 'entanglement = geometry').",
    },
}

VERDICT_GLYPH = {"FORCED": "●", "FREE": "○", "IMPOSSIBLE": "✕"}


def classify(name: str) -> str:
    """Render the verdict + certificate for a named claim."""
    e = CATALOG[name]
    g = VERDICT_GLYPH[e["verdict"]]
    lines = [
        f"{g} {name}  →  {e['verdict']}",
        f"  claim:      {e['claim']}",
    ]
    if "simulate" in e:
        v = e["simulate"]()
        if isinstance(v, str):
            lines.append(f"  simulate:   {v}")
        else:
            lines.append(f"  simulate:   {v:.6f}  (Phantom, live)  — 2√2 = {2 * math.sqrt(2):.6f}")
    lines += [
        f"  theorem:    {e['theorem']}  (kernel-checked)",
        f"  falsifier:  {e['falsifier']}",
        f"  oracle:     {', '.join(e['oracle'])}",
        f"  why:        {e['why']}",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import sys

    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("--help", "-h"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        for name in CATALOG:
            e = CATALOG[name]
            print(f"{VERDICT_GLYPH[e['verdict']]} {name:<20} {e['verdict']:<11} {e['claim']}")
        return 0
    name = argv[0]
    if name not in CATALOG:
        print(f"unknown claim '{name}'. known: {', '.join(CATALOG)}", file=sys.stderr)
        return 2
    print(classify(name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
