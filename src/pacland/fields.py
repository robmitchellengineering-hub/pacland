"""fields.py — the built-out field catalog: the seed material for cross-field reference.

Each structure carries the full typed-knowledge-model shape (plan §3): definition, type (its
isomorphism class — the cross-field match key), domain, assumptions, the non-trivial property it
reproduces, its five-tier epistemic status, limitations, and permitted mappings. Every entry here is
ESTABLISHED science (tier 1–2) — these are RECOGNITIONS, not discoveries.

The catalog is organised so each TYPE spans several fields — that is what makes cross-reference
searches yield real matches.
"""
from __future__ import annotations

from pacland import registry


# tier: 1 = mathematically established · 2 = follows from established · 3 = conjecture ·
#       4 = tested numerically · 5 = genuinely unknown
FIELDS: list[dict] = [
    # ---- diffusion / parabolic-pde ----
    {"id": "heat-equation", "type": "parabolic-pde", "domain": "physics",
     "definition": "∂_t u = α ∇² u", "assumptions": ["linear conduction", "Fourier's law"],
     "reproduces": "linear-in-time mean-squared displacement ⟨x²⟩ = 2αt", "tier": 1,
     "limitations": ["breaks at microscopic/relativistic scales"],
     "maps": ["fick-diffusion", "brownian-motion", "black-scholes"]},
    {"id": "fick-diffusion", "type": "parabolic-pde", "domain": "chemistry",
     "definition": "∂_t c = D ∇² c", "assumptions": ["dilute solute", "no drift"],
     "reproduces": "Fick's second law; concentration spreads as √(Dt)", "tier": 1,
     "limitations": ["no reaction term (see reaction-diffusion)"],
     "maps": ["heat-equation", "reaction-diffusion"]},
    {"id": "brownian-motion", "type": "parabolic-pde", "domain": "probability",
     "definition": "a continuous Markov process with Gaussian increments, ⟨Δx²⟩ ∝ Δt",
     "assumptions": ["independent increments", "continuous paths"],
     "reproduces": "the heat kernel is the transition density; ⟨x²⟩ = 2Dt", "tier": 1,
     "limitations": ["no jumps (see Lévy processes)"],
     "maps": ["heat-equation", "ou-process"]},
    {"id": "black-scholes", "type": "parabolic-pde", "domain": "economics",
     "definition": "∂_t V + ½σ²S²∂²V/∂S² + rS∂V/∂S − rV = 0",
     "assumptions": ["geometric Brownian motion", "no arbitrage"],
     "reproduces": "the option price is a heat equation under a log-change of variables", "tier": 2,
     "limitations": ["constant volatility is false in practice"],
     "maps": ["heat-equation"]},
    {"id": "diffusion-mri", "type": "parabolic-pde", "domain": "neuroscience",
     "definition": "signal attenuation exp(−b·ADC) from water self-diffusion in tissue",
     "assumptions": ["Gaussian displacement", "single compartment"],
     "reproduces": "the Einstein relation maps measured ADC to mean-squared displacement", "tier": 4,
     "limitations": ["crossing fibres need multi-tensor models"],
     "maps": ["heat-equation"]},

    # ---- markov ----
    {"id": "ou-process", "type": "markov", "domain": "economics",
     "definition": "dX = −θ(X−μ)dt + σ dW (mean-reversion)",
     "assumptions": ["linear drift", "Gaussian noise"],
     "reproduces": "stationary distribution N(μ, σ²/2θ); autocorrelation decays at rate θ", "tier": 1,
     "limitations": ["linear mean-reversion"],
     "maps": ["brownian-motion", "sir-model"]},
    {"id": "sir-model", "type": "markov", "domain": "epidemiology",
     "definition": "S→I→R compartmental flow with rate βSI and recovery γ",
     "assumptions": ["well-mixed population", "no births/deaths"],
     "reproduces": "R₀ = β/γ threshold; epidemic dies out iff R₀ < 1", "tier": 1,
     "limitations": ["no network structure"],
     "maps": ["ou-process", "logistic-growth"]},
    {"id": "wright-fisher", "type": "markov", "domain": "biology",
     "definition": "a Markov chain on allele frequencies with binomial resampling",
     "assumptions": ["fixed population size", "neutral drift"],
     "reproduces": "fixation probability equals initial frequency; heterozygosity decays at 1/N", "tier": 1,
     "limitations": ["neutrality (no selection)"],
     "maps": ["markov-chain-monte-carlo"]},
    {"id": "markov-chain-monte-carlo", "type": "markov", "domain": "physics",
     "definition": "a reversible Markov chain with the target distribution as its stationary measure",
     "assumptions": ["detailed balance", "aperiodic + irreducible"],
     "reproduces": "the spectral gap of the chain bounds the mixing time (1/gap)", "tier": 1,
     "limitations": ["slow mixing in multimodal targets"],
     "maps": ["wright-fisher", "spectral-gap"]},

    # ---- conservation ----
    {"id": "energy-budget", "type": "conservation", "domain": "climate",
     "definition": "dE/dt = absorbed solar − emitted longwave (the TOA energy balance)",
     "assumptions": ["global average", "grey atmosphere"],
     "reproduces": "the equilibrium sensitivity ∝ 1/(climate feedback parameter)", "tier": 2,
     "limitations": ["aggregates spatial/spectral detail"],
     "maps": ["noether-conservation", "carbon-cycle"]},
    {"id": "carbon-cycle", "type": "conservation", "domain": "climate",
     "definition": "dC/dt = emissions − uptake (a conservation of carbon across reservoirs)",
     "assumptions": ["reservoir linearity"],
     "reproduces": "the airborne fraction ≈ constant under constant emissions", "tier": 2,
     "limitations": ["nonlinear sink saturation"],
     "maps": ["energy-budget", "stoichiometry"]},
    {"id": "stoichiometry", "type": "conservation", "domain": "chemistry",
     "definition": "mass is conserved across a reaction: Σ νᵢ Mᵢ = 0",
     "assumptions": ["closed system", "no nuclear reactions"],
     "reproduces": "balanced equations give exact product ratios", "tier": 1,
     "limitations": ["kinetics may limit yield (thermodynamics ≠ rate)"],
     "maps": ["carbon-cycle", "noether-conservation"]},
    {"id": "noether-conservation", "type": "conservation", "domain": "physics",
     "definition": "every continuous symmetry has a conserved charge (Noether's theorem)",
     "assumptions": ["Lagrangian formulation", "continuous symmetry"],
     "reproduces": "time-translation → energy; rotation → angular momentum", "tier": 1,
     "limitations": ["discrete symmetries (no conserved charge)"],
     "maps": ["energy-budget", "gauge-symmetry"]},

    # ---- symmetry ----
    {"id": "gauge-symmetry", "type": "symmetry", "domain": "physics",
     "definition": "a local symmetry group acting on a fiber bundle",
     "assumptions": ["principal bundle", "local invariance"],
     "reproduces": "the field strength F = dA + A∧A is the curvature of the connection", "tier": 1,
     "limitations": ["non-compact / anomalous cases"],
     "maps": ["noether-conservation", "crystal-space-group"]},
    {"id": "molecular-point-group", "type": "symmetry", "domain": "chemistry",
     "definition": "the finite group of symmetry operations of a molecule",
     "assumptions": ["rigid geometry"],
     "reproduces": "selection rules: a transition is allowed iff the irrep product contains the totally symmetric irrep", "tier": 1,
     "limitations": ["fluxional / non-rigid molecules"],
     "maps": ["crystal-space-group"]},
    {"id": "crystal-space-group", "type": "symmetry", "domain": "materials",
     "definition": "the 230 crystallographic space groups (symmetry of a lattice)",
     "assumptions": ["perfect crystal", "infinite lattice"],
     "reproduces": "Bragg peaks are the reciprocal lattice (the group's dual)", "tier": 1,
     "limitations": ["defects break the symmetry"],
     "maps": ["molecular-point-group", "gauge-symmetry"]},

    # ---- oscillator ----
    {"id": "harmonic-oscillator", "type": "oscillator", "domain": "physics",
     "definition": "m ẍ + kx = 0 (or the quantum version with spectrum ℏω(n+½))",
     "assumptions": ["quadratic potential", "no damping"],
     "reproduces": "period 2π√(m/k) independent of amplitude", "tier": 1,
     "limitations": ["anharmonic corrections at large amplitude"],
     "maps": ["integrate-and-fire", "business-cycle"]},
    {"id": "integrate-and-fire", "type": "oscillator", "domain": "neuroscience",
     "definition": "dV/dt = (I − V)/τ, reset V→Vr at threshold (relaxation oscillation)",
     "assumptions": ["point neuron", "constant input"],
     "reproduces": "firing rate ∝ 1/ln(I/(I−V_th)) — a soft-threshold rate curve", "tier": 2,
     "limitations": ["no spikes dynamics, no adaptation"],
     "maps": ["harmonic-oscillator"]},
    {"id": "business-cycle", "type": "oscillator", "domain": "economics",
     "definition": "second-order dynamics in output (the multiplier-accelerator model)",
     "assumptions": ["lagged investment response"],
     "reproduces": "damped or growing oscillations set by the accelerator coefficient", "tier": 3,
     "limitations": ["reduced-form, no microfoundations"],
     "maps": ["harmonic-oscillator"]},

    # ---- growth / logistic ----
    {"id": "logistic-growth", "type": "logistic", "domain": "biology",
     "definition": "dN/dt = rN(1 − N/K)",
     "assumptions": ["single species", "constant carrying capacity"],
     "reproduces": "S-shaped saturation to K; the sigmoid is the solution", "tier": 1,
     "limitations": ["no age structure, no stochasticity"],
     "maps": ["sir-model", "adoption-curve"]},
    {"id": "adoption-curve", "type": "logistic", "domain": "economics",
     "definition": "technology adoption follows the logistic (Bass) diffusion",
     "assumptions": ["imitation + innovation"],
     "reproduces": "the S-curve of cumulative adoption", "tier": 4,
     "limitations": ["network effects can break the S-shape"],
     "maps": ["logistic-growth"]},

    # ---- spectral gap ----
    {"id": "spectral-gap", "type": "spectral-gap", "domain": "mathematics",
     "definition": "the gap λ₂ − λ₁ between the two largest eigenvalues of a self-adjoint operator",
     "assumptions": ["self-adjoint", "compact/normal"],
     "reproduces": "mixing time ≤ (1/gap) log(1/ε) for a reversible chain", "tier": 1,
     "limitations": ["non-reversible chains need a different bound"],
     "maps": ["markov-chain-monte-carlo", "ou-process"]},
]


def seed_fields() -> int:
    """Load every field structure into the registry. Returns the number seeded."""
    n = 0
    for s in FIELDS:
        payload = {
            "definition": s["definition"],
            "type": s["type"],
            "domain": s["domain"],
            "assumptions": s.get("assumptions", []),
            "reproduces": s["reproduces"],
            "tier": s["tier"],
            "limitations": s.get("limitations", []),
            "permitted_mappings": s.get("maps", []),
        }
        registry.add(registry.Entry(
            id=s["id"], kind="structure", payload=payload,
            provenance={"produced_by": "fields-seed", "method": "established-science"}))
        n += 1
    return n
