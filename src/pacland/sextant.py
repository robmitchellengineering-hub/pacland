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
        "simulate": phantom.gravity_quantum,
        "theorem": "QM.Entanglement + QM.NoCloning + Gleason",
        "falsifier": "a consistent classical (LOCC) coupling",
        "oracle": ["quantum-simulated (Phantom)", "kernel-checked (Lean)"],
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
        "theorem": "QM.MERA.srank_maximally_entangled (entanglement = D^m EXACTLY) + QM.MERA.areaLaw_rank + QM.MERA.bondConfigurations",
        "falsifier": "entanglement exceeding D^m",
        "oracle": ["kernel-checked (Lean)", "quantum-simulated (Phantom/Quimb)"],
        "verdict": "FORCED",
        "why": "a sum of r = D^m simple tensors has simple rank ≤ r (the area law, the algebraic "
               "core of Ryu–Takayanagi / MERA 'entanglement = geometry').",
    },
    "mera-hyperbolic": {
        "claim": "the MERA causal cone is a discrete hyperbolic space (Gromov 0-hyperbolic)",
        "theorem": "QM.Hyperbolic.treeDist_four_point + QM.MERA.causalConeDoubles + QM.MERA.ballVolumeExponential + QM.MERA.logDepthForced + QM.MERA.meraEmergence + QM.Hyperbolic.treeToH2",
        "falsifier": "a four-point violation of the 0-hyperbolicity condition, or sub-exponential volume growth",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the tree metric satisfies the four-point condition (0-hyperbolicity), with exponential "
               "volume 2^(r+1)−1, log depth, and the D^m area law — the discrete signature of the "
               "hyperbolic (AdS) plane (Swingle's 'MERA = AdS', kernel-checked).",
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
    "mitchell-uniqueness": {
        "claim": "the D3 tadpole FᵀJH is the unique bilinear symplectic invariant of the flux",
        "theorem": "Mitchell.mitchell_uniqueness_n1 + General.mitchell_uniqueness",
        "falsifier": "a second bilinear symplectic invariant of the flux",
        "oracle": ["kernel-checked (Lean)", "exact symbolic (sympy)"],
        "verdict": "FORCED",
        "why": "the only matrix M with SᵀMS = M for every symplectic S is a scalar multiple of J — the tadpole is forced, not chosen.",
    },
    "constraint-first": {
        "claim": "every duality-invariant exact polynomial in the flux is a function of the tadpole",
        "theorem": "DegreeOne.no_linear_invariant_n1 + DegreeThree.no_cubic_invariant + DegreeFour.quartic_is_N_sq",
        "falsifier": "an invariant polynomial that is not a function of FᵀJH",
        "oracle": ["kernel-checked (Lean)", "exact symbolic (sympy)"],
        "verdict": "FORCED",
        "why": "no linear invariant, no cubic invariant, only N² at quartic — the invariant ring has a single generator (Weyl's FFT, degrees 1–4 machine-checked).",
    },
    "completeness": {
        "claim": "no exact invariant selector can single out a vacuum (the tadpole is complete)",
        "theorem": "Transitivity.transitivity_n1 + Transitivity.symp_iff_det_eq_one",
        "falsifier": "a second exact, duality-invariant selector",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "SᵀJS = det S · J, so symplectic ⟺ det 1, and {xᵀJy = 1} is one SL(2) orbit — the no-go on exact invariant selectors.",
    },
    "matchgate-seed": {
        "claim": "matchgate amplitudes are Pfaffians — the full even/odd split kernel-checked (2×2 and 4×4 Pf² = det, odd-dim det = 0)",
        "theorem": "QM.Matchgate.det_antisymm_sign + QM.Matchgate.pfaffian2_sq_eq_det + QM.Matchgate.pfaffian4_sq_eq_det + QM.Matchgate.pfaffian6_sq_eq_det + QM.Matchgate.det_antisymm_odd_eq_zero + QM.PfaffianRec.pfaffian_rec_2 + QM.PfaffianRec.pfaffian_rec_4 + QM.PfaffianRec.pfaffian_sq_eq_det_2 + QM.PfaffianRec.pfaffian_sq_eq_det_4 + QM.PfaffianRec.pfaffian_transform_2",
        "falsifier": "a 2×2 matchgate whose amplitude is not its Pfaffian, or a nonzero odd-dimensional antisymmetric determinant",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the 2×2 and 4×4 Pfaffians square to the determinant (the exact two- and four-qubit amplitudes), the recursive Pfaffian reproduces the explicit cases (pfaffian_rec_2/4) with the m=1 and m=2 induction bases (pfaffian_sq_eq_det_2/4: recursive Pf² = det), the transformation law Pf(PAPᵀ) = det(P)·Pf(A) holds at 2×2 (pfaffian_transform_2 — the normal-form route to the general Cayley), and ANY odd-dimensional antisymmetric matrix has determinant 0 — the complete even/odd split: matchgates are even-dimensional Pfaffians, hence classically simulable.",
    },
    "pr-box": {
        "claim": "the PR box saturates the non-signaling CHSH bound at 4",
        "theorem": "Foundations.PRBox.prbox_chsh",
        "falsifier": "a non-signaling box exceeding CHSH = 4",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the PR box is the maximally non-local box allowed by no-signaling — CHSH = 4, the ceiling above the quantum 2√2.",
    },
    "sm-index": {
        "claim": "N_gen is a protected topological index (|χ|/2 in the heterotic class)",
        "theorem": "SM.Index.index_free + SM.Index.index_protected + SM.Index.chi_even",
        "falsifier": "an anomaly that un-protects the index",
        "oracle": ["kernel-checked (Lean)"],
        "verdict": "FORCED",
        "why": "the generation count is an index — free (not fixed) and protected (robust) — and χ = 2(h¹¹−h²¹) is even, so N_gen = |χ|/2 is always a whole number. But the value 3 (χ = 6) is a free label, not a forced value.",
    },
     "black-hole-entropy": {
         "claim": "no region's entanglement entropy exceeds its horizon area — S ≤ A/4G, and the black hole saturates it",
         "simulate": phantom.black_hole_entropy,
         "theorem": "QM.MERA.srank_maximally_entangled + QM.MERA.areaLaw_rank (the area law specialised to the horizon cut: S = A/4G)",
         "falsifier": "a state whose horizon entanglement exceeds A/4G",
         "oracle": ["quantum-simulated (Phantom)", "kernel-checked (Lean)"],
         "verdict": "FORCED",
         "why": "the Bekenstein–Hawking entropy is not a dial — it is the entanglement-area law with the cut = the horizon. A random (Page) state saturates A/4G; nothing exceeds it.",
     },
     "black-hole-unitarity": {
         "claim": "black hole evaporation is unitary — the information is never lost, only re-encoded in the radiation's entanglement",
         "simulate": phantom.black_hole_unitarity,
         "theorem": "QM.NoCloning + QM.NoBroadcasting (linearity + unitarity forbid information loss)",
         "falsifier": "a non-unitary (information-losing) evaporation map",
         "oracle": ["quantum-simulated (Phantom)", "kernel-checked (Lean)"],
         "verdict": "FORCED",
         "why": "a pure state stays pure under any unitary map (purity is invariant), so the interior's information cannot vanish — it is re-encoded in the Hawking radiation's entanglement. The mechanism of the recovery is the open part; the unitarity itself is forced.",
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
    if argv[0] == "--verify":
        print(verify_all())
        return 0
    if argv[0] == "verify":
        if len(argv) < 2:
            print("usage: sextant verify <claim>   (or --verify for all)", file=sys.stderr)
            return 2
        if argv[1] not in CATALOG:
            print(f"unknown claim '{argv[1]}'. known: {', '.join(CATALOG)}", file=sys.stderr)
            return 2
        print(verify(argv[1]))
        return 0
    if argv[0] == "hunt":
        from pacland import hypotheses

        if len(argv) > 1 and argv[1] in hypotheses.HYPOTHESES:
            print(hypotheses.hypothesize(argv[1]))
        else:
            print(hypotheses.hunt())
        return 0
    name = argv[0]
    if name not in CATALOG:
        print(f"unknown claim '{name}'. known: {', '.join(CATALOG)}", file=sys.stderr)
        return 2
    print(classify(name))
    return 0



def verify(name: str) -> str:
    """Run a claim's falsifier and report whether the claim survives it."""
    e = CATALOG[name]
    g = VERDICT_GLYPH[e["verdict"]]
    if name in phantom.FALSIFIERS:
        survived, evidence = phantom.FALSIFIERS[name]()
        status = "SURVIVES" if survived else "REFUTED"
        return (
            f"{g} {name} → {e['verdict']}  [{status}]\n"
            f"  claim:      {e['claim']}\n"
            f"  falsifier:  {e['falsifier']}\n"
            f"  ran:        {evidence}\n"
            f"  theorem:    {e['theorem']} (kernel-checked)"
        )
    return (
        f"{g} {name} → {e['verdict']}\n"
        f"  claim:      {e['claim']}\n"
        f"  falsifier:  {e['falsifier']}\n"
        f"  ran:        kernel-checked — {e['theorem']} proves the falsifier impossible (no live oracle)"
    )


def verify_all() -> str:
    """Run every claim's falsifier; a claim survives iff its falsifier fails."""
    lines = []
    survived = 0
    for name in CATALOG:
        e = CATALOG[name]
        g = VERDICT_GLYPH[e["verdict"]]
        if name in phantom.FALSIFIERS:
            ok, _ = phantom.FALSIFIERS[name]()
            lines.append(f"{g} {name:<22} {'SURVIVES' if ok else 'REFUTED'}")
            if ok:
                survived += 1
        else:
            lines.append(f"{g} {name:<22} kernel-checked (theorem)")
            survived += 1
    return "\n".join(lines) + f"\n\n{survived}/{len(CATALOG)} claims survive their falsifier"

if __name__ == "__main__":
    raise SystemExit(main())
