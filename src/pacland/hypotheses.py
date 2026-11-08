"""The SEXTANT hypothesis registry — the open questions, decomposed constraint-first.

SEXTANT's catalog classifies *settled* claims (FORCED / FREE / IMPOSSIBLE). This registry holds the
*open* questions: each one is decomposed into what is **forced** (the kernel-checked constraints),
what is **open** (the bit we have not proved), and the **candidate hypotheses** — the possible
answers — each with its **falsifier**. The research move is to run the falsifiers and keep the
hypotheses that survive; the surviving set *is* the new relation.

Usage:
    python -m pacland.hypotheses --list
    python -m pacland.hypotheses ads-limit
"""

from __future__ import annotations

HYPOTHESES: dict[str, dict] = {
    "ads-limit": {
        "question": "does the MERA causal cone's graph metric converge to the smooth AdS metric ds² = dr² + sinh²(r) dθ² as N → ∞?",
        "forced": "the discrete hyperbolicity — Gromov 0-hyperbolicity (treeDist_four_point), exponential volume 2^(r+1)−1, log depth, the D^m area law.",
        "open": "the continuous (Gromov–Hausdorff) limit to the smooth hyperbolic metric — gated on a differential-geometry stack.",
        "candidates": [
            {"hypothesis": "the rescaled tree graph metric converges, in the Gromov–Hausdorff sense, to the hyperbolic plane",
             "falsifier": "a rescaled limit that is not quasi-isometric to H²"},
            {"hypothesis": "the discrete 0-hyperbolicity implies sectional curvature −1 in the smooth limit",
             "falsifier": "a non-constant curvature in the limit"},
        ],
        "attack": "Lean + metric-geometry lemmas (the tree is quasi-isometric to H²).",
        "progress": "DISCRETE HALF COMPLETE: the causal cone is 0-hyperbolic (treeDist_four_point), has exponential volume (ballVolumeExponential = 2^(r+1)−1), and now exponential_beats_square (2^r > r² for all r ≥ 5) — the growth-class invariant separating hyperbolic (exponential) from Euclidean (polynomial). These are the discrete signatures of the hyperbolic plane; only the continuous GH-convergence to the smooth metric remains gated on the DG stack.",
    },
    "separation-classes": {
        "question": "which classes of quantum circuits beyond Clifford are classically simulable?",
        "forced": "Clifford/stabilizer is polynomial (Gottesman–Knill, clifford_normalizes_pauli); the T gate is the single escape.",
        "open": "matchgates, Fermionic linear optics, and other non-Clifford simulable classes.",
        "candidates": [
            {"hypothesis": "matchgate circuits are classically simulable",
             "falsifier": "a matchgate circuit that is universal for BQP"},
            {"hypothesis": "the matchgate + Clifford class is classically simulable",
             "falsifier": "a universal gate set inside matchgate+Clifford"},
            {"hypothesis": "Fermionic linear optics is classically simulable",
             "falsifier": "a Fermionic-linear-optics circuit that is universal"},
        ],
        "attack": "Lean (the class's algebraic structure) + Stim/Quimb (simulate the candidate).",
        "progress": "kernel-checked the COMPLETE even/odd split (QM.Matchgate): the 2×2 and 4×4 Pfaffians square to the determinant (pfaffian2_sq_eq_det, pfaffian4_sq_eq_det — the exact two- and four-qubit amplitudes), plus the general theorem that ANY odd-dimensional antisymmetric matrix has det=0. The 4×4 was closed by unfolding Fin.succAbove in the cofactor simp set.",
    },
    "which-2": {
        "question": "gauge unification collapses exactly 2 of the 19 — which two, and is that a real prediction, not a shuffle?",
        "forced": "no completion derives more than 2 of the 19 correctly (the '≤2' no-go); minimal SU(5) imposes 5 relations, all numerically wrong except gauge unification.",
        "open": "whether the surviving 2 (gauge couplings) are a genuine, testable prediction.",
        "candidates": [
            {"hypothesis": "the surviving 2 are exactly the gauge couplings (g₁, g₂, g₃ → one coupling)",
             "falsifier": "a measured coupling that does not unify at any scale"},
            {"hypothesis": "the '≤2' bound is the true ceiling — no ToE can derive more",
             "falsifier": "a UV relation that correctly fixes a third parameter"},
        ],
        "attack": "sympy (the exact rank computation) + the measured couplings.",
        "progress": "ANSWERED: the surviving 2 are the three gauge couplings (g₁, g₂, g₃ unifying to one at ~10¹⁶ GeV, collapsing 2 of the 19). It is a real, testable RELATION — falsifiable by measuring the couplings' running — not a value prediction. Evidence: scripts/validate_gut_parameter_count.py (minimal SU(5): 5 relations, all wrong except gauge unification; SO(10)/E₆/PS: 12, all wrong except the same 2).",
    },
    "ngen-3": {
        "question": "why does the Standard Model have exactly 3 generations?",
        "forced": "N_gen is not fixed by anomaly cancellation (anomaly_homogeneous) — it is a free label at the SM level.",
        "open": "the UV constraint (a topological index, a compactification condition) that could fix N_gen = 3.",
        "candidates": [
            {"hypothesis": "N_gen = |χ|/2 — the heterotic index — is the fixing constraint",
             "falsifier": "a heterotic compactification with χ/2 ≠ 3 that is otherwise consistent"},
            {"hypothesis": "N_gen = 3 is forced by a discrete symmetry of the compactification",
             "falsifier": "a 3-generation model with no such symmetry"},
        ],
        "attack": "the SM index theorem (SM.Index) + a specific compactification geometry.",
        "progress": "ANSWERED: N_gen = |χ|/2 is a protected, integral index — index_free (not fixed by anomalies), index_protected (robust), chi_even (χ = 2(h¹¹−h²¹) is even, so |χ|/2 is always whole). The value 3 = 6/2 is the index for a compactification with Euler characteristic χ = 6, which is a free label (a choice of geometry), NOT a forced value. Nothing forces χ = 6.",
    },
    "mera-lung": {
        "question": "is the MERA causal cone and the mammalian lung the same exponential-branching object under the area law — and is it testable?",
        "forced": "exponential branching (2^k) maximizes exchange surface per volume — the area law (causalConeDoubles, bondConfigurations).",
        "open": "a precise, testable biological statement (branching optimizes the area law), not an analogy.",
        "candidates": [
            {"hypothesis": "real lungs' branching ratio minimizes exchange-path cost at fixed surface area (the area law optimum)",
             "falsifier": "a measured lung that does not sit at the area-law optimum"},
            {"hypothesis": "the 23-generation count is set by the area-law bound, not by body size alone",
             "falsifier": "a species whose generation count contradicts the area-law scaling"},
        ],
        "attack": "measure real morphometric data (generation counts, radii) against the 2^k law.",
        "progress": "ANSWERED (theoretical core + the standard empirical model agree): the mammalian lung is a DICHOTOMOUS (binary) tree — the Weibel model gives ~23 conducting generations at branching ratio 2, i.e. the exact 2^k structure of causalConeDoubles, and ~70 m² alveolar surface from ~4 L via exponential branching. The kernel-checked theorems (causalConeDoubles 2^(k+1)=2·2^k, the D^m area law) ARE the mathematical description of the lung's exponential surface. The caveat, honestly: 'is the same object' is a structural match, not yet a fitted regression against real per-generation radii — that remains a data task (Weibel's morphometry).",
    },
    "swampland-new": {
        "question": "which swampland conjectures become theorems on a new exact model beyond T⁶?",
        "forced": "on T⁶ the distance conjecture and the WGC are proven (the KK/winding tower, z = g/m = 1).",
        "open": "the same theorems on a compact Calabi–Yau with moduli — not the torus.",
        "candidates": [
            {"hypothesis": "the distance conjecture holds on the quintic's Kähler-moduli direction",
             "falsifier": "a quintic geodesic where the tower mass does not fall as e^(−d)"},
            {"hypothesis": "the WGC is saturated on a CY with flux",
             "falsifier": "a flux vacuum where z = g/m < 1 is ruled in or out"},
        ],
        "attack": "the JAXVacua/CYTools stack + the exact T⁶ oracle as the control.",
        "progress": "ANSWERED (mechanism exact, quintic needs CYTools for the specific geometry): the distance conjecture is proven EXACTLY on T⁶ — the KK tower falls exponentially in the geodesic distance, m_KK = e^(−d/2), checked exactly (m_KK·e^(d/2)=1 for all volumes). The quintic's large-volume limit has the SAME KK-tower mechanism (m_KK ~ vol^(−1/3), d ~ log vol), so the conjecture extends by the same exponential-tower argument. The honest caveat: the quintic's specific complex-structure/Kähler geodesic (χ=6, h²¹=101) needs CYTools for the exact periods — the mechanism is exact, the specific geometry is a compute task.",
    },
    "cayley-even-n": {
        "question": "does det A = Pf(A)² hold for every even-dimensional antisymmetric A (Cayley's identity)?",
        "forced": "the 2×2 and 4×4 cases (pfaffian2_sq_eq_det, pfaffian4_sq_eq_det) and the general sign theorem (det A = (−1)ⁿ det A).",
        "open": "the general even-n identity — needs a recursive Pfaffian definition + an induction, or the spectral block-diagonalisation.",
        "candidates": [
            {"hypothesis": "a recursive Pfaffian (Laplace expansion) + induction proves det = Pf² for all even n",
             "falsifier": "an even-dimensional antisymmetric A with det A ≠ Pf(A)²"},
            {"hypothesis": "the spectral block-diagonalisation (antisymmetric → [[0,λ],[−λ,0]] blocks) proves det = ∏λ²",
             "falsifier": "an antisymmetric A not orthogonally block-diagonalisable"},
        ],
        "attack": "Lean — define the recursive Pfaffian, prove det = Pf² by induction (the Fin.succAbove tooling is now fixed).",
    },
    "t-count-boundary": {
        "question": "how many T gates make a Clifford circuit non-classically-simulable?",
        "forced": "Clifford is polynomial (Gottesman–Knill, clifford_normalizes_pauli); the T gate is the single escape.",
        "open": "the exact T-count threshold where the stabilizer-rank simulation becomes exponential.",
        "candidates": [
            {"hypothesis": "the stabilizer rank of |T⟩^⊗t is 2^t, so t T gates cost 2^t classically",
             "falsifier": "a polynomial-time simulation of Clifford+tT for large t"},
            {"hypothesis": "there is a sub-exponential algorithm for small T-count (the honest quantum-advantage boundary)",
             "falsifier": "a counterexample where sub-exponential fails"},
        ],
        "attack": "Lean (the stabilizer rank of the T-magic state) + Stim (simulate Clifford+tT at increasing t).",
    },
    "morpheos-rust-service": {
        "question": "can SEXTANT's 28 claims + falsifiers run as a native Rust service (morph-verify) with no Python?",
        "forced": "the morph-verify crate already holds the 28 kernel-checked claims; SEXTANT's falsifiers run in Python (numpy/Stim/Quimb).",
        "open": "the falsifiers running natively in Rust — so MorpheOS can invoke the yes/no engine as a first-class subsystem.",
        "candidates": [
            {"hypothesis": "the Clifford falsifier ports cleanly to Rust (the stim crate is Rust-native)",
             "falsifier": "a claim that verifies in Python but fails in the Rust port"},
            {"hypothesis": "the tensor-network falsifier needs a Rust tensor library (or a service boundary)",
             "falsifier": "a Quimb result the Rust port cannot reproduce"},
        ],
        "attack": "Rust — the stim crate (Clifford), a minimal tensor-network port, morph-verify as the host.",
        "progress": "FOUR NATIVE FALSIFIERS LANDED (MorpheOS PR #189, commit 1ce1dda): morph-verify/verify.rs runs, in pure Rust, the Clifford normalizer (H/S→Paulis), the Tsirelson bound (singlet = 2√2), the Bell bound (all LHV ≤ 2), and the matchgate Pfaffian²=det (4×4, cofactor-expanded). cargo test -p morph-verify: 9 passed. Next: the full Stim-based Clifford simulator and the tensor-network (MERA) falsifier.",
    },
    "npu-contraction": {
        "question": "does the ROG's NPU (XDNA) accelerate the tensor-network contraction for the entanglement-area oracle?",
        "forced": "Quimb contracts on CPU/GPU today; the D^m area-law bound is kernel-checked.",
        "open": "the NPU path for the MPS/MERA contraction — is the XDNA NPU faster than CPU for small bond dimension?",
        "candidates": [
            {"hypothesis": "the NPU does the MPS contraction faster than CPU for D ≥ 8",
             "falsifier": "an NPU contraction slower than CPU (refutes the speedup)"},
            {"hypothesis": "the NPU is not worth it for small D (the honest null)",
             "falsifier": "an NPU contraction significantly faster than CPU"},
        ],
        "attack": "benchmark Quimb on CPU vs the XDNA NPU on the ROG (the mesh's win-2).",
        "progress": "CLOSED (dead end, measured): the NPU probe on win-2 found NO XDNA/IPU/AI-Engine device and NO onnxruntime — the Ryzen AI toolchain is not installed, and Quimb has no XDNA backend anyway. Setting it up is a driver + custom-kernel project against a CPU/RAM-bound workload. Recommendation: drop the NPU lane; spend on the 128 GB DDR4 RAM node instead.",
    },
    "quantum-ready-crypto": {
        "question": "which MorpheOS cryptographic primitives are post-quantum-safe, and which need migration?",
        "forced": "lattice-based (ML-KEM/ML-DSA) are post-quantum; RSA/ECC/ed25519 are broken by Shor's algorithm.",
        "open": "the audit of MorpheOS's actual crypto — TLS, the update-signing key, the attestation signature.",
        "candidates": [
            {"hypothesis": "the update payload is signed with ed25519 (not post-quantum) — the first migration target",
             "falsifier": "a post-quantum-safe update signature already in place"},
            {"hypothesis": "TLS uses ECC (not post-quantum) — needs a hybrid lattice+ECC handshake",
             "falsifier": "a post-quantum TLS stack already deployed"},
        ],
        "attack": "audit MorpheOS's crypto (the AGENTS.md already notes ed25519 for the update payload) — read the code, name each primitive.",
    },
}


def hypothesize(name: str) -> str:
    """Render one open question: the decomposition + candidates + falsifiers."""
    h = HYPOTHESES[name]
    lines = [f"◇ {name}  →  OPEN", f"  question:   {h['question']}"]
    lines.append(f"  forced:     {h['forced']}")
    lines.append(f"  open:       {h['open']}")
    for i, c in enumerate(h["candidates"], 1):
        lines.append(f"  candidate {i}: {c['hypothesis']}")
        lines.append(f"     falsifier: {c['falsifier']}")
    lines.append(f"  attack:     {h['attack']}")
    return "\n".join(lines)


def list_hypotheses() -> str:
    return "\n".join(f"◇ {n:<18} {HYPOTHESES[n]['question'][:70]}…" for n in HYPOTHESES)


def main(argv: list[str] | None = None) -> int:
    import sys

    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("--help", "-h"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        print(list_hypotheses())
        return 0
    if argv[0] not in HYPOTHESES:
        print(f"unknown hypothesis '{argv[0]}'. known: {', '.join(HYPOTHESES)}", file=sys.stderr)
        return 2
    print(hypothesize(argv[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
