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
        "simulate": phantom.mera_entanglement,  # live: Quimb MPS entanglement ≤ log D
        "theorem": "QM.MERA",
        "falsifier": "entanglement exceeding D^m",
        "oracle": ["kernel-checked (Lean)", "quantum-simulated (Phantom/Quimb)"],
        "verdict": "FORCED",
        "why": "a sum of r = D^m simple tensors has simple rank ≤ r (the area law, the algebraic "
               "core of Ryu–Takayanagi / MERA 'entanglement = geometry').",
    },

    "bell-classical": {
        "claim": "no local-hidden-variable theory violates CHSH beyond 2",
        "simulate": phantom.bell_classical,
        "theorem": "QM.CHSH (Bell)",
        "falsifier": "a classical strategy exceeding 2",
        "oracle": ["quantum-simulated (Phantom)", "kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the classical wall is 2; quantum reaches 2√2, so the gap [2, 2√2] is the free column (entanglement).",
    },
    "no-broadcasting": {
        "claim": "no machine broadcasts an arbitrary mixed state (M ↦ M⊗M is not linear)",
        "theorem": "QM.NoBroadcasting",
        "falsifier": "a linear broadcasting map",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "IMPOSSIBLE",
        "why": "the mixed-state form of no-cloning.",
    },
    "pbr": {
        "claim": "distinct pure states cannot share a ψ-epistemic ontic overlap",
        "theorem": "QM.PBR (pbr_two_copy_independent)",
        "falsifier": "two distinct states with overlapping ontic support",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the two-copy states |ψi⟩⊗|ψj⟩ are linearly independent, so a measurement distinguishes them — excluding ψ-epistemic models.",
    },
    "mermin": {
        "claim": "no non-contextual ±1 assignment to the Mermin square exists",
        "simulate": phantom.mermin_product,
        "theorem": "QM.Mermin (mermin_no_value_assignment)",
        "falsifier": "a non-contextual ±1 assignment",
        "oracle": ["quantum-simulated (Phantom)", "kernel-checked (Lean)"],
        "verdict": "IMPOSSIBLE",
        "why": "row products +I, last column −I: the product of all nine is +1 (rows) and −1 (columns) — contradiction.",
    },
    "locc-no-entanglement": {
        "claim": "a classical (LOCC) channel cannot create entanglement",
        "theorem": "QM.Entanglement (local_channel_preserves_separable)",
        "falsifier": "a classical channel entangling two systems",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "IMPOSSIBLE",
        "why": "Φ⊗Ψ maps product states to product states, so separability is preserved — entanglement is non-classical.",
    },
    "lovelock": {
        "claim": "the Einstein equation is the unique divergence-free 2-tensor theory in 4D",
        "theorem": "Gravity.Lovelock.lovelock_divergence",
        "falsifier": "a second divergence-free gravity theory",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "∇·(αR + βRg) = (α/2+β)∇R vanishes identically iff β = −α/2 — the Einstein tensor.",
    },
    "bianchi": {
        "claim": "the Einstein tensor is divergence-free (∇·G = 0)",
        "theorem": "Gravity.QG.einstein_divergence_free",
        "falsifier": "a metric with ∇·G ≠ 0",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the contracted second Bianchi identity — the constraint that joins QM and GR.",
    },
    "wdw": {
        "claim": "physical states satisfy the Wheeler–DeWitt equation Ĥ|ψ⟩ = 0",
        "theorem": "Gravity.WheelerDeWitt.wdw_equation",
        "falsifier": "a physical state not in ker Ĥ",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "physical states = ker Ĥ; time is emergent (the 'problem of time').",
    },
    "dirac": {
        "claim": "the ADM constraints close under the Dirac (hypersurface-deformation) algebra",
        "theorem": "Gravity.Dirac.dirac_antisymmetric",
        "falsifier": "a constraint algebra that fails to close",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the structure function q^ab makes it a Lie algebroid — the signature of diffeomorphism invariance.",
    },
    "adm": {
        "claim": "QG's forced content is the constraint system {Ĥ = G·ππ − R, Ĥa = ∇·π}",
        "theorem": "Gravity.ADMConstraints.admConstraints",
        "falsifier": "a third independent constraint",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the Hamiltonian + momentum constraints, joined by the DeWitt supermetric G^abcd.",
    },
    "hypercharge-uniqueness": {
        "claim": "the SM anomaly conditions force the hypercharges uniquely (up to scale + u↔d)",
        "theorem": "SM.Hypercharge.hypercharge_uniqueness",
        "falsifier": "a second anomaly-free hypercharge assignment",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the anomaly conditions have a unique solution — the SM's gauge sector is forced.",
    },
    "anomaly-cancellation": {
        "claim": "the SM's five anomaly coefficients vanish",
        "theorem": "SM.Anomaly.anomaly_cancellation",
        "falsifier": "a nonzero anomaly coefficient",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the hypercharges cancel all five gauge/gravitational anomalies — the SM is consistent.",
    },
    "generation-free": {
        "claim": "the generation number N_gen is not fixed by anomaly cancellation",
        "theorem": "SM.Generation.anomaly_homogeneous",
        "falsifier": "an anomaly condition fixing N_gen",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FREE",
        "why": "the coefficients are homogeneous, so N_gen copies stay anomaly-free — N_gen = 3 is a label.",
    },
    "the-19": {
        "claim": "the SM has 19 free parameters (orbit-space dimension)",
        "theorem": "SM.ParameterCount",
        "falsifier": "a relation collapsing more than 2 of the 19 correctly",
        "oracle": ["kernel-checked (Lean)", "exact symbolic (sympy)"],
        "verdict": "FREE",
        "why": "the SM's own flavor symmetry leaves orbit-space rank 19; no completion derives more than 2 correctly.",
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
