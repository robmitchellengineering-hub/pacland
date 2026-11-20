"""known_unifications.py — the harvested, sourced known-unifications library.

The fan-out web search compiled the KNOWN economics↔hard-science (and other soft↔hard) unifications from
the published literature, each with its source. These are RECOGNITIONS — established links, not discoveries
(plan §2). They seed the known-unifications library so the engine does not re-derive or "rediscover" them.
"""
from __future__ import annotations

import time

from pacland import registry

# (economics/field A, hard science, exact form, source)
UNIFICATIONS: list[tuple[str, str, str, str]] = [
    # econophysics
    ("wealth-distribution", "boltzmann", "P(w) = (1/T)e^{−w/T}", "Dragulescu-Yakovenko 2000"),
    ("income-tail", "pareto", "P(x) ∝ x^{−(α+1)}", "Pareto 1897; Mantegna-Stanley"),
    ("price", "brownian-motion", "dS = μS dt + σS dW", "Bachelier 1900"),
    ("stock-returns", "levy-stable", "ln φ(t) = iδt − γ|t|^α", "Mandelbrot 1963"),
    ("gravity-trade", "newton-gravity", "F = G·M₁M₂/D²", "Tinbergen 1962"),
    ("quantity-theory", "ideal-gas", "MV = PY ⟺ PV = nRT", "Fisher 1911; Saslow 1999"),
    ("fx-volatility", "turbulence", "P(Δx) ∝ |Δx|^{−3}", "Ghashghaie 1996"),
    ("option-pricing", "heat-equation", "∂V/∂t + ½σ²S²∂²V/∂S² = rV", "Black-Scholes 1973"),
    ("herding", "percolation", "return PDF from cluster-size power law", "Cont-Bouchaud 2000"),
    ("financial-crash", "critical-point", "p(t) = A + B(t_c−t)^m (log-periodic)", "Sornette 2003"),
    ("volatility-clustering", "omori-law", "n(t) ∝ t^{−p}", "Sornette; Omori 1894"),
    ("market-dynamics", "spin-glass", "phase transition at α_c ≈ 0.337", "Challet-Zhang 1997"),
    # economics ↔ biology
    ("goodwin-cycle", "lotka-volterra", "ẇ=w(ρu−a), u̇=u(b−cw)", "Goodwin 1967"),
    ("evolutionary-game", "evolution", "ESS: E(I,I) ≥ E(J,I)", "Maynard Smith-Price 1973"),
    ("market-selection", "replicator", "dxᵢ/dt = xᵢ(fᵢ−f̄)", "Metcalfe"),
    ("technology-diffusion", "logistic", "f/(1−f) = e^{2α(t−t₀)}", "Fisher-Pry 1971"),
    ("competition", "niche-exclusion", "Gause's law", "Hannan-Freeman 1977"),
    ("leontief-multiplier", "trophic-cascade", "(I−A)^{−1} = total-throughput multiplier", "Hannon 1973"),
    ("innovation-diffusion", "sir", "dF/dt = (p+qF)(1−F)", "Bass 1969"),
    ("firm-scaling", "kleiber-law", "sales ∝ size^{3/4}", "West 2017"),
    # economics ↔ math
    ("nash-equilibrium", "fixed-point", "x* ∈ BR(x*)", "Nash 1950-51"),
    ("utility", "lagrangian", "∂u/∂xᵢ = λpᵢ (MRS = pᵢ/pⱼ)", "Ramsey 1928"),
    ("efficient-frontier", "pareto-frontier", "min σ² s.t. E[r] = μ", "Markowitz 1952"),
    ("capm", "projection", "E[rᵢ] = r_f + βᵢ(E[r_m]−r_f)", "Sharpe 1964"),
    ("keynesian-multiplier", "geometric-series", "1/(1−c)", "Kahn 1931; Keynes 1936"),
    ("comparative-advantage", "lp-duality", "equilibrium prices = dual variables", "Dorfman-Samuelson-Solow 1958"),
    ("arrow-debreu", "kakutani-fixed-point", "p* ∈ Z(p*)", "Arrow-Debreu 1954"),
    # economics ↔ thermodynamics
    ("theil-index", "shannon-entropy", "T = ln N − H", "Theil; Shannon"),
    ("gini", "entropy", "gintropy σ = F̄−C̄", "Biró-Néda 2020"),
    ("arrow-debreu", "maximum-entropy", "nᵢ ∝ e^{−βaᵢ}/Z", "Foley 1994"),
    ("production-function", "thermodynamic-potential", "Cobb-Douglas ↔ equation of state", "Saslow 1999"),
    # other soft ↔ hard fields (the playbook generalises)
    ("opinion-dynamics", "ising", "±spins, order/disorder transition", "Galam 2012"),
    ("associative-memory", "spin-glass", "Hopfield, capacity 0.14N", "Hopfield 1982"),
    ("word-frequency", "zipf-power-law", "freq ∝ 1/rank", "Zipf 1949"),
    ("signal-detection", "information-theory", "d′ = signal/noise separation", "Green-Swets 1966"),
    ("epidemic", "chemical-kinetics", "dS/dt = −βSI", "Kermack-McKendrick 1927"),
    ("scale-free-network", "preferential-attachment", "P(k) ∝ k^{−γ}", "Barabási-Albert 1999"),
    ("replicator", "gradient-dynamics", "dx/dt = x(f−f̄) on a fitness landscape", "Taylor-Jonker 1978"),
]


def record() -> int:
    """Ingest every harvested unification as a known (recognition) mapping with its source. Returns count."""
    n = 0
    for frm, to, form, source in UNIFICATIONS:
        registry.add(registry.Entry(
            id=f"known-{frm}-{to}",
            kind="mapping",
            payload={"from": frm, "to": to, "exact_form": form, "source": source,
                     "kind_of_yield": "recognition",
                     "novel": False, "known": True},
            provenance={"produced_by": "known-unifications-harvest", "method": "web-search",
                        "ts": time.time()}))
        n += 1
    return n
