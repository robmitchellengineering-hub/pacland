"""soft_unifications.py — the harvested soft-field↔hard-science unifications (psychology, sociology,
linguistics, urban science, political science, anthropology, history, education/law/health).

Fan-out web research, each with its source. These are KNOWN unifications (recognitions) — they seed the
known-unifications library so the engine's cross-field search has a full baseline of established links.
"""
from __future__ import annotations

import time

from pacland import registry

UNIFICATIONS: list[tuple[str, str, str, str]] = [
    # psychology
    ("signal-detection", "information-theory", "d′ = z(H) − z(FA)", "Green-Swets 1966"),
    ("weber-fechner", "log-response", "S = k·ln(I/I₀)", "Fechner 1860"),
    ("decision-making", "bayesian-inference", "P(H|D) = P(D|H)P(H)/P(D)", "Wald 1950"),
    ("reaction-time", "information-theory", "RT = a + b·log₂(n+1) (Hick's law)", "Hick 1952"),
    ("memory-decay", "exponential-decay", "R = e^{−t/S}; power law", "Ebbinghaus 1885"),
    ("learning-curve", "power-law", "T = a·P^{−b} (power law of practice)", "Newell-Rosenbloom 1981"),
    ("perception", "free-energy", "F = −ln p(s̃) = complexity − accuracy", "Friston 2010"),
    # sociology / sociophysics
    ("opinion-dynamics", "ising", "H = −J·Σ sᵢsⱼ", "Castellano 2009; Galam 2012"),
    ("social-phase-transition", "critical-phenomena", "order parameter m → 0/±1", "Galam 1997"),
    ("schelling-segregation", "phase-separation", "tolerance → Cahn-Hilliard", "Vinković-Kirman 2006"),
    ("crowd-behaviour", "percolation", "info spread above p_c", "Helbing 2000"),
    ("social-networks", "scale-free", "P(k) ∝ k^{−γ}", "Barabási-Albert 1999"),
    ("group-polarisation", "ferromagnetic", "magnetisation below T_c", "Galam 2012"),
    ("collective-behaviour", "self-organised-criticality", "P(s) ∝ s^{−τ}", "Bak-Tang-Wiesenfeld 1987"),
    # linguistics
    ("word-frequency", "zipf-power-law", "f(r) ∝ r^{−a}", "Zipf 1949"),
    ("language-change", "diffusion", "sigmoid S-curve spread", "Schmidt 1872"),
    ("information-density", "shannon-entropy", "H = −Σ pᵢ log pᵢ", "Shannon 1948"),
    ("grammar", "formal-language", "Chomsky hierarchy", "Chomsky 1956"),
    ("menzerath-altmann", "allometric-scaling", "y = a·x^{−b}", "Menzerath 1954"),
    ("semantic-space", "vector-geometry", "similarity = cosine distance", "Mikolov 2013"),
    ("glottochronology", "radioactive-decay", "N(t) = N₀e^{−λt}, half-life ≈ 1000yr", "Swadesh 1952"),
    ("heaps-law", "sublinear-growth", "V(n) ∝ n^β", "Heaps 1978"),
    # urban science / geography
    ("city-size", "zipf", "P(size>S) ∝ S^{−ζ}", "Gabaix 1999"),
    ("urban-scaling", "allometric", "Y = Y₀N^β (β≈1.15)", "Bettencourt 2007"),
    ("migration-gravity", "newton-gravity", "T = G·PᵢPⱼ/d^γ", "Zipf 1946"),
    ("traffic-flow", "fluid-dynamics", "∂ρ/∂t + ∂q/∂x = 0 (LWR)", "Lighthill-Whitham 1955"),
    ("urban-growth", "diffusion-limited-aggregation", "fractal D ≈ 1.7", "Makse-Havlin-Stanley 1995"),
    ("central-place", "voronoi", "hexagonal market areas", "Christaller 1933"),
    ("commuting", "potential-flow", "gradient of a population potential", "Wilson 1967"),
    ("land-use", "entropy-maximisation", "S = −Σ Tᵢⱼ ln Tᵢⱼ", "Wilson 1967"),
    # political science
    ("voting", "ising-potts", "voters as spins", "Galam 2008"),
    ("polarisation", "ferromagnetic-transition", "consensus = magnetisation", "Galam 2008"),
    ("electoral-volatility", "stochastic-dynamics", "voter model / master equation", "Fernández-Gracia 2014"),
    ("coalition-formation", "cooperative-game-theory", "Shapley value, the core", "Shapley-Shubik 1954"),
    ("median-voter", "fixed-point", "median = best-response fixed point", "Black 1948; Downs 1957"),
    ("war-frequency", "power-law", "wars ∝ casualties^{−α}", "Richardson 1948"),
    ("gerrymandering", "optimal-transport", "Wasserstein distance of votes", "Abrishami 2020"),
    # anthropology / cultural evolution
    ("cultural-evolution", "replicator", "Price equation Δz̄ = Cov(w,z)/w̄", "Boyd-Richerson 1985"),
    ("cumulative-culture", "cumulative-process", "ratchet effect", "Tomasello 1999"),
    ("kinship", "group-theory", "marriage rules = finite group", "Lévi-Strauss 1949; Weil"),
    ("population-structure", "coalescent", "Kingman coalescent", "Kingman 1982"),
    ("technology-growth", "logistic", "S-curve / accelerating returns", "Kurzweil 2001"),
    ("language-drift", "genetic-drift", "Wright-Fisher analogue", "Bentley-Hahn-Shennan 2004"),
    # history / cliodynamics
    ("political-instability", "demographic-structural-cycle", "population → elite → breakdown", "Turchin-Nefedov 2009"),
    ("empire-size", "power-law", "heavy-tailed polity sizes", "Cederman 2003"),
    ("empire-rise-fall", "logistic", "S-shaped growth-decline", "Taagepera 1978"),
    ("agrarian-state", "predator-prey", "elites=predator, commoners=prey", "Turchin 2003"),
    ("kondratiev-wave", "oscillator", "~50yr harmonic waves", "Turchin cycles"),
    # education / law / health
    ("school-performance", "normal-lognormal", "grades ~ N(μ,σ²)", "Galton 1889"),
    ("citation-impact", "power-law", "Lotka n^{−2}; Price √N", "Lotka 1926; Price 1963"),
    ("legal-precedent", "network", "citation indegree = authority", "Fowler 2007"),
    ("crime-spread", "sir", "dS/dt = −βSI", "Kermack-McKendrick 1927"),
    ("disease-spread", "reaction-diffusion", "∂u/∂t = D∇²u + ru(1−u) (Fisher-KPP)", "Fisher 1937"),
    ("healthcare-demand", "queueing", "M/M/c / Erlang C", "Erlang 1917"),
]


def record() -> int:
    """Ingest every soft-field unification as a known (recognition) mapping with its source."""
    n = 0
    for frm, to, form, source in UNIFICATIONS:
        registry.add(registry.Entry(
            id=f"soft-{frm}-{to}",
            kind="mapping",
            payload={"from": frm, "to": to, "exact_form": form, "source": source,
                     "kind_of_yield": "recognition", "novel": False, "known": True},
            provenance={"produced_by": "soft-unifications-harvest", "method": "web-search",
                        "ts": time.time()}))
        n += 1
    return n
