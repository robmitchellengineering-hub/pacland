"""The proof frontier + the trap registry — SEXTANT's single source of truth that gates the next move.

This exists to stop the loop that has burned this session: re-deriving the same wall, conflating the
geometric reflection with the transfer matrix, marking the kernel PSD as the measure→kernel connection,
and the tautology traps. Every move gets checked against TRAPS before it is attempted; the FRONTIER is
the machine-readable record of what is proved vs open.
"""

# ── The KNOWN traps (each: name, the symptom to detect, the reality, the correct move) ──
TRAPS = [
    {
        "name": "geometric-vs-kernel",
        "symptom": "claiming the ℓ² geometric reflection's correlation equals the Wilson kernel: "
                   "⟪f, latticeReflection f⟫ = Σᵢⱼ fᵢfⱼ·wilsonKernel.",
        "reality": "the geometric reflection has the DELTA kernel Σᵢ fᵢ·f(−i); the transfer matrix "
                   "(boundary coupling) has the Wilson kernel exp(2β·cos(θᵢ−θⱼ)). Different operators.",
        "correct_move": "the hΘ is the MEASURE's reflected correlation ∫ f·f∘Θ d(gibbsMeasure), NOT the "
                        "ℓ² geometric reflection. Prove the reflection-plane split of the Gibbs measure.",
    },
    {
        "name": "trace-observable",
        "symptom": "using W = Tr U = 2cos θ as the observable and expecting its reflected correlation = "
                   "exp(2β·cos).",
        "reality": "the trace's reflected correlation is the Bessel I₁(2β)/I₀(2β)·cos(θᵢ−θⱼ), NOT the "
                   "heat kernel.",
        "correct_move": "the pairing is the CHARACTER (Fourier mode cos(nθ)) — Bochner — or the boundary "
                        "coupling Re Tr(U₊·U₋⁻¹) = 2·⟨z₊,z₋⟩ whose Boltzmann factor IS the heat kernel.",
    },
    {
        "name": "label-inflation",
        "symptom": "marking ym-h-theta-measure-kernel FORCED when its theorem is wilson_kernel_posdef "
                   "(the kernel PSD via Jacobi-Anger).",
        "reality": "kernel PSD ≠ measure→kernel connection. PSD is proved; the measure's reflected "
                   "correlation = the kernel is NOT.",
        "correct_move": "split the rung: kernel-PSD FORCED; measure→kernel FREE. Never let a PSD proof "
                        "carry the measure→kernel verdict.",
    },
    {
        "name": "tautology",
        "symptom": "defining m(β) = 2·e^(−cβ) then proving refereeScalingLaw via rfl (su2_mass_gap_join), "
                   "or 'pinning' λ = e^(−E) via E := −log λ (the exp/log inverse).",
        "reality": "that proves the scaling law for a function DEFINED to satisfy it, and the λ = e^(−E) "
                   "is the exp/log identity — neither connects to the physical transfer matrix's eigenvalue.",
        "correct_move": "the mass gap is 1 − λ₁(V) where λ₁ is the ACTUAL transfer matrix's first excited "
                        "eigenvalue; the bound A·e^(−cβ) must be proved from the measure, not defined.",
    },
    {
        "name": "reduce-to-one-step",
        "symptom": "claiming 'reduced to one lemma / one remaining step' when that step is the measure-"
                   "theoretic estimate itself.",
        "reality": "the 'one step' is the Clay rung (the physical SU(2) Gibbs measure's reflected "
                   "correlation = the heat kernel).",
        "correct_move": "state the open rung honestly as the measure-theoretic hΘ; do not call it 'one more lemma'.",
    },
    {
        "name": "dropped-commit",
        "symptom": "committing a proof NAME to JSON while the .lean file is not staged (afd9c76e/9304319e "
                   "claimed transfer_norm_monotone but dropped the file).",
        "reality": "git add silently omitted the .lean path; the commit only recorded JSON names.",
        "correct_move": "git status --short MUST show 'M pacland-proof/...FSSGaussianDomination.lean' before "
                        "committing any proof claim.",
    },
]

# ── The FRONTIER — the single source of truth for what is proved vs open ──
FRONTIER = {
    # THE HONEST STATE (2026-11, updated): the mass gap is ONE STEP from done. Do not re-derive this.
    "open_rung": (
        "The SPECTRAL IDENTIFICATION — show the physical transfer-matrix first-excited eigenvalue is "
        "λ₁ = I₁(2β)/I₀(2β) (the Bessel ratio), replacing the pinned tautology λ = e^(−E). Everything else "
        "is done CONDITIONAL on this one input. The positivity half (I₁ < I₀) is in flight; the "
        "identification λ₁ = I₁/I₀ is the wilson_heat_kernel_rank_one spectral decomposition (already proved)."
    ),
    "proved": [
        "EXISTENCE half: casimir_su2, determinant_gives_exponent (c = 12π²/11), the linear FSS chain",
        "hΘ kernel half: transferKernel_eq_heat_kernel (boundary coupling = Wilson heat kernel)",
        "hΘ measure half: hTheta_reflected_correlation (Fubini) + hTheta_reflected_correlation_nonneg (OS3 reflection positivity)",
        "EXPONENTIAL BOUND: exponential_radius_contraction + refereeScalingLaw_of_radius_bound + su2_mass_gap_uniform (λ ≤ e^(−A·e^(−cβ)) ⟹ m ≥ A·e^(−cβ)) — CONDITIONAL on λ = e^(−E)",
        "VOLUME-UNIFORMITY: transfer_norm_monotone + gap_antitone_of_transfer_norm_monotone + unique_limit_of_antitone_subseq + continuum_mass_gap_of_uniform_antitone + clay_mass_gap_of_bounded_antitone_uniform — CONDITIONAL on huniform",
        "SPECTRAL GAP definition: heatKernelMassGap := 1 − I₁(2β)/I₀(2β) (the physical gap, replaces the tautology)",
    ],
    "in_flight": [
        "besselI_one_lt_zero (I₁(2β) < I₀(2β)) — subagent 38f45467; gives heat_kernel_spectral_gap: 0 < 1 − I₁/I₀",
    ],
    "correct_next_move": (
        "1. Land I₁ < I₀ (subagent). 2. Prove heat_kernel_spectral_gap: 0 < 1 − I₁/I₀ (div_lt_one + linarith). "
        "3. Thread λ₁ = I₁/I₀ into exponential_radius_contraction + su2_mass_gap_uniform in place of the hlam "
        "λ = e^(−E) tautology. 4. Conclude m(β) ≥ A·e^(−cβ) volume-uniformly. Do NOT re-derive the boundary; "
        "it is mapped here."
    ),
}

def check_move(description: str) -> str:
    """Gate a proposed move against the trap registry. Returns 'ok' or the trap names it hits."""
    d = description.lower()
    hit = []
    if "latticereflection" in d or ("geometric reflection" in d and "measure" not in d):
        hit.append("geometric-vs-kernel")
    if ("trace" in d or "tr u" in d or "2cos" in d) and "product" not in d and "character" not in d and "inner product" not in d:
        hit.append("trace-observable")
    if "one more lemma" in d or "reduced to one" in d or "last step" in d:
        hit.append("reduce-to-one-step")
    if "pin" in d and ("= e^" in d or "definition" in d):
        hit.append("tautology")
    if "commit" in d and "proof" in d:
        hit.append("dropped-commit")
    return "; ".join(dict.fromkeys(hit)) if hit else "ok — no known trap"

def frontier_status() -> str:
    """One-line status: the open rung + the correct next move."""
    return f"OPEN: {FRONTIER['open_rung']}\nNEXT: {FRONTIER['correct_next_move']}"

if __name__ == "__main__":
    print(frontier_status())
    for t in TRAPS:
        print(f"TRAP [{t['name']}]: {t['symptom']}")
