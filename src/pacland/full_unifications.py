"""full_unifications.py — the comprehensive harvested catalog of known soft↔hard-science unifications.

A 16-agent fan-out across every major sub-field (econophysics market/distribution, finance, macro, micro/
game theory, psychology, sociology, linguistics, urban, politics, anthropology, history, neuroscience,
epidemiology/health, climate/ecology, AI/ML). Each entry: (soft concept, hard science, source).
"""
from __future__ import annotations

import time

from pacland import registry

UNIFICATIONS: list[tuple[str, str, str]] = [
    # econophysics — market microstructure / price dynamics
    ("price-impact", "elasticity", "Kyle 1985"), ("temporary-impact", "friction", "Almgren-Chriss 2001"),
    ("square-root-impact", "diffusion", "Toth-Bouchaud 2011"), ("order-flow", "point-process", "Bouchaud-Farmer-Lillo 2004"),
    ("bid-ask-spread", "adverse-selection", "Roll 1984"), ("volatility-clustering", "autoregressive-diffusion", "Engle 1982"),
    ("multifractal-volatility", "turbulence", "Mandelbrot-Calvet-Fisher 1997"), ("epps-effect", "asynchronous-sampling", "Epps 1979"),
    ("market-efficiency", "random-walk", "Fama 1970"), ("leverage-effect", "asymmetric-feedback", "Black 1976"),
    ("herding", "ising", "Bornholdt 2001"), ("herding-clusters", "percolation", "Cont-Bouchaud 2000"),
    ("crashes", "criticality", "Sornette 2003"), ("minority-game", "spin-glass", "Challet-Zhang 1997"),
    ("fat-tails", "levy-flight", "Mandelbrot 1963"), ("return-correlations", "random-matrix", "Laloux 1999"),
    ("fx-intermittency", "turbulence", "Ghashghaie 1996"), ("order-book", "self-organised-criticality", "Bak-Paczuski-Shubik 1997"),
    ("stochastic-volatility", "ou-process", "Heston 1993"), ("price-discovery", "information-entropy", "Grossman-Stiglitz 1980"),
    # econophysics — distributions
    ("wealth-bulk", "boltzmann", "Dragulescu-Yakovenko 2000"), ("money-equilibrium", "thermal", "Yakovenko 2001"),
    ("income-tail", "pareto", "Pareto 1897"), ("firm-size", "lognormal", "Gibrat 1931"),
    ("firm-growth", "multiplicative-random-walk", "Gibrat 1931"), ("firm-tail", "zipf", "Axtell 2001"),
    ("firm-growth-spread", "laplace", "Stanley 1996"), ("city-size", "zipf", "Gabaix 1999"),
    ("money-max-entropy", "maximum-entropy", "Jaynes 1957"), ("saving-propensity", "gamma", "Chakraborti-Chakrabarti 2000"),
    ("power-law-exponent", "proportionate-growth", "Gabaix 2009"), ("wealth-composite", "boltzmann+pareto", "Yakovenko-Rosser 2009"),
    # financial economics
    ("black-scholes", "heat-equation", "Black-Scholes 1973"), ("option-greeks", "taylor-expansion", "Hull"),
    ("portfolio-theory", "quadratic-optimisation", "Markowitz 1952"), ("capm", "projection", "Sharpe 1964"),
    ("arbitrage-pricing", "no-arbitrage", "Ross 1976"), ("binomial-model", "random-walk", "Cox-Ross-Rubinstein 1979"),
    ("risk-neutral-pricing", "change-of-measure", "Girsanov 1960"), ("yield-curve", "mean-reverting-diffusion", "Vasicek 1977"),
    ("duration-convexity", "taylor-series", "Macaulay 1938"), ("risk-aversion", "concavity", "Arrow-Pratt 1964"),
    ("no-arbitrage-pde", "feynman-kac", "Feynman-Kac"), ("complete-markets", "linear-algebra", "Arrow-Debreu 1954"),
    ("stochastic-calculus", "ito-chain-rule", "Ito 1944"),
    # macroeconomics
    ("quantity-theory", "ideal-gas", "Fisher 1911"), ("solow-growth", "relaxation", "Solow 1956"),
    ("business-cycle", "oscillator", "Samuelson 1939"), ("goodwin-cycle", "lotka-volterra", "Goodwin 1967"),
    ("inflation", "temperature", "Saslow 2024"), ("adaptive-expectations", "low-pass-filter", "Cagan 1956"),
    ("rational-expectations", "kalman-filter", "Muth 1961"), ("multiplier", "geometric-series", "Kahn 1931"),
    ("phillips-curve", "hyperbola", "Phillips 1958"), ("kondratiev-wave", "oscillator", "Kondratiev 1925"),
    ("dsge", "dynamical-systems", "Blanchard-Kahn 1980"), ("monetary-policy", "pid-control", "Taylor 1993"),
    # microeconomics / game theory
    ("nash-equilibrium", "fixed-point", "Nash 1950"), ("utility", "lagrangian", "Samuelson"),
    ("arrow-debreu", "kakutani", "Arrow-Debreu 1954"), ("comparative-advantage", "lp-duality", "McKenzie"),
    ("core", "cooperative-game", "Bondareva-Shapley"), ("auction", "mechanism-design", "Vickrey 1961"),
    ("median-voter", "fixed-point", "Black 1948"), ("matching", "stable-marriage", "Gale-Shapley 1962"),
    ("bargaining", "nash-solution", "Nash 1950"), ("perfect-competition", "walrasian-equilibrium", "Arrow-Debreu"),
    ("envelope-theorem", "calculus", "Hotelling"), ("mechanism-design", "revelation-principle", "Myerson 1979"),
    ("social-choice", "arrow-impossibility", "Arrow 1951"), ("cooperative-value", "shapley-value", "Shapley 1953"),
    ("public-goods", "vickrey-clarke-groves", "Vickrey 1961"),
    # psychology
    ("signal-detection", "information-theory", "Green-Swets 1966"), ("weber-fechner", "log-response", "Fechner 1860"),
    ("hick-law", "information-theory", "Hick 1952"), ("fitts-law", "information-theory", "Fitts 1954"),
    ("memory-forgetting", "power-law", "Wickelgren 1974"), ("skill-learning", "power-law", "Newell-Rosenbloom 1981"),
    ("perception", "bayesian", "Knill-Pouget 2004"), ("perception-action", "free-energy", "Friston 2010"),
    ("decision-time", "drift-diffusion", "Ratcliff 1978"), ("mental-rotation", "rotation-group", "Shepard-Metzler 1971"),
    ("emotion", "dynamical-systems", "Lewis 2005"), ("personality", "factor-analysis", "Costa-McCrae 1992"),
    ("neural-coding", "efficient-coding", "Barlow 1961"), ("conditioning", "gradient-descent", "Rescorla-Wagner 1972"),
    ("motor-control", "optimal-control", "Todorov-Jordan 2002"), ("spatial-vision", "fourier", "Campbell-Robson 1968"),
    # sociology
    ("opinion", "ising", "Galam 1990"), ("segregation", "phase-separation", "Schelling 1971"),
    ("social-network", "scale-free", "Barabasi-Albert 1999"), ("polarisation", "ferromagnetic", "Galam"),
    ("crowd", "percolation", "Helbing"), ("collective-behaviour", "self-organised-criticality", "Bak 1987"),
    ("rumour", "sir", "Daley-Kendall 1965"), ("cooperation", "evolutionary-game", "Szabo-Fath 2007"),
    ("social-mobility", "markov-chain", "Prais 1955"), ("small-world", "clustering", "Watts-Strogatz 1998"),
    ("inequality", "entropy", "Dragulescu-Yakovenko 2000"), ("social-influence", "mean-field", "Castellano 2009"),
    ("cultural-fragmentation", "potts", "Axelrod 1997"), ("language-competition", "voter-model", "Castellano 2009"),
    # linguistics
    ("zipf", "power-law", "Zipf 1949"), ("heaps", "sublinear-growth", "Heaps 1978"),
    ("menzerath-altmann", "allometric", "Altmann 1980"), ("glottochronology", "radioactive-decay", "Swadesh 1952"),
    ("information-density", "shannon-entropy", "Shannon 1948"), ("grammar", "formal-language", "Chomsky 1956"),
    ("semantic-space", "vector-geometry", "Mikolov 2013"), ("language-change", "diffusion", "Wang 1969"),
    ("chomsky-hierarchy", "automata", "Chomsky 1956"), ("phoneme-frequency", "entropy", "Shannon 1951"),
    ("language-complexity", "kolmogorov", "Kolmogorov 1965"), ("semantic-drift", "random-walk", "Hamilton 2016"),
    ("lexical-diversity", "type-token", "Johnson 1944"), ("text-redundancy", "entropy-rate", "Shannon 1951"),
    # urban / geography
    ("city-size", "zipf", "Gabaix 1999"), ("urban-scaling", "allometric", "Bettencourt 2007"),
    ("gravity-migration", "newton-gravity", "Tinbergen 1962"), ("traffic", "fluid-dynamics", "Lighthill-Whitham 1955"),
    ("urban-growth", "dla", "Makse 1995"), ("central-place", "voronoi", "Christaller 1933"),
    ("land-use", "entropy-maximisation", "Wilson 1967"), ("commuting", "potential-flow", "Stewart 1947"),
    ("urban-fractal", "fractal", "Batty-Longley 1994"), ("road-network", "planar-graph", "Barthelemy 2011"),
    ("urban-heat", "thermodynamics", "Oke 1982"), ("accessibility", "gravity", "Hansen 1959"),
    # political science
    ("voting", "ising-potts", "Galam 2002"), ("polarisation", "phase-transition", "Sznajd"),
    ("median-voter", "fixed-point", "Black 1948"), ("war-frequency", "power-law", "Richardson 1960"),
    ("coalition", "cooperative-game", "Shapley 1953"), ("gerrymandering", "optimal-transport", "MIT"),
    ("electoral-volatility", "ou-process", "Pedersen 1979"), ("arms-race", "lotka-volterra", "Richardson 1935"),
    ("opinion", "mean-field", "Galam"), ("social-choice", "geometry", "Arrow 1951; Saari 1994"),
    ("rumour", "epidemiology", "Daley-Kendall 1964"), ("collective-action", "percolation", "Granovetter 1978"),
    # anthropology / archaeology
    ("cultural-evolution", "replicator", "Price 1970"), ("kinship", "group-theory", "Weil 1949"),
    ("language-drift", "genetic-drift", "Kimura 1968"), ("population-genetics", "coalescent", "Kingman 1982"),
    ("technology-adoption", "logistic", "Rogers 1962"), ("radiocarbon", "radioactive-decay", "Libby 1949"),
    ("stratigraphy", "superposition", "Steno 1669"), ("artefact-frequency", "seriation", "Petrie 1899"),
    ("demography", "population-dynamics", "Hassan 1981"), ("cultural-transmission", "epidemiology", "Cavalli-Sforza 1981"),
    ("language-phylogeny", "cladistics", "Gray-Atkinson 2003"), ("niche-construction", "ecosystem-engineering", "Odling-Smee 2003"),
    # history / cliodynamics
    ("political-instability", "demographic-cycle", "Turchin 2009"), ("empire-size", "power-law", "Taagepera 1997"),
    ("empire-rise-fall", "logistic", "Taagepera 1978"), ("agrarian-state", "predator-prey", "Turchin 2003"),
    ("war", "power-law", "Richardson 1960"), ("kondratiev", "oscillator", "Kondratiev 1925"),
    ("state-formation", "phase-transition", "Galam 2012"), ("elite-overproduction", "malthusian", "Turchin 2016"),
    ("collapse", "tipping-point", "Scheffer 2009"), ("long-term-growth", "exponential", "Maddison 2001"),
    # neuroscience / cognition
    ("associative-memory", "hopfield-spin-glass", "Hopfield 1982"), ("perception", "free-energy", "Friston 2010"),
    ("neural-firing", "integrate-and-fire", "Lapicque 1907"), ("brain-network", "small-world", "Watts-Strogatz 1998"),
    ("neural-dynamics", "attractor", "Amit 1985"), ("decision", "drift-diffusion", "Ratcliff 1978"),
    ("neural-coding", "information-theory", "Barlow 1961"), ("synaptic-plasticity", "hebbian", "Hebb 1949"),
    ("consciousness", "integrated-information", "Tononi 2004"), ("brain-criticality", "self-organised-criticality", "Beggs-Plenz 2003"),
    ("neural-avalanche", "power-law", "Beggs-Plenz 2003"), ("brain", "bayesian", "Knill-Pouget 2004"),
    ("oscillation", "kuramoto", "Kuramoto 1975"), ("signal-spread", "cable-equation", "Rall 1959"),
    # epidemiology / health
    ("sir", "chemical-kinetics", "Kermack-McKendrick 1927"), ("epidemic-threshold", "percolation", "Newman 2002"),
    ("disease-spread", "reaction-diffusion", "Fisher 1937"), ("network-epidemic", "scale-free", "Pastor-Satorras 2001"),
    ("healthcare-queueing", "erlang", "Erlang 1917"), ("pharmacodynamics", "hill-equation", "Hill 1910"),
    ("radiation-dose", "poisson", "Lea 1946"), ("cancer-growth", "gompertz", "Gompertz 1825"),
    ("drug-delivery", "diffusion", "Higuchi 1961"), ("ecg-heart", "oscillator", "van-der-Pol 1926"),
    ("blood-flow", "fluid-dynamics", "Poiseuille 1840"), ("imaging", "fourier-radon", "Cormack 1963"),
    ("pharmacokinetics", "first-order-kinetics", "Teorell 1937"), ("mri", "bloch-equations", "Bloch 1946"),
    # climate / ecology
    ("energy-balance", "stefan-boltzmann", "Budyko 1969"), ("greenhouse", "radiative-transfer", "Arrhenius 1896"),
    ("weather", "chaos", "Lorenz 1963"), ("climate-model", "navier-stokes", "Phillips 1956"),
    ("ocean-circulation", "fluid-dynamics", "Stommel 1961"), ("carbon-cycle", "box-model", "Keeling"),
    ("population", "logistic", "Verhulst 1838"), ("predator-prey", "lotka-volterra", "Lotka 1925"),
    ("ecosystem", "food-web", "May 1972"), ("tipping-point", "bifurcation", "Scheffer 2001"),
    ("biodiversity", "entropy", "MacArthur 1955"), ("species-area", "power-law", "Arrhenius 1921"),
    ("island-richness", "equilibrium", "MacArthur-Wilson 1967"), ("metabolic-rate", "allometric", "Kleiber 1932"),
    # AI / ML ↔ physics
    ("hopfield-memory", "ising", "Hopfield 1982"), ("neural-net", "spin-glass", "Gardner 1988"),
    ("statistical-learning", "order-parameter", "Gardner 1988"), ("gradient-descent", "langevin", "Welling-Teh 2011"),
    ("boltzmann-machine", "ising", "Ackley-Hinton 1985"), ("overfitting", "phase-transition", "Spigler 2019"),
    ("loss-landscape", "spin-glass", "Choromanska 2015"), ("simulated-annealing", "optimisation", "Kirkpatrick 1983"),
    ("diffusion-model", "nonequilibrium-thermodynamics", "Sohl-Dickstein 2015"), ("deep-learning", "renormalisation", "Mehta-Schwab 2014"),
    ("pac-learning", "information-theory", "Xu-Raginsky 2017"), ("variational-inference", "free-energy", "Dayan 1995"),
    ("attention", "hopfield", "Ramsauer 2021"), ("infinite-width", "gaussian-process", "Jacot 2018"),
    ("deep-learning", "information-bottleneck", "Tishby-Zaslavsky 2015"),
]


def record() -> int:
    """Ingest every harvested unification (dedupe by 'from'), each flagged known with its source."""
    from pacland import registry as rg
    existing = {m["payload"].get("from", "") for m in rg.query("mapping", lambda d: True)}
    n = 0
    for frm, to, source in UNIFICATIONS:
        if frm in existing:
            continue  # dedupe
        rg.add(rg.Entry(
            id=f"full-{frm}-{to}",
            kind="mapping",
            payload={"from": frm, "to": to, "source": source, "kind_of_yield": "recognition",
                     "novel": False, "known": True},
            provenance={"produced_by": "full-unifications-harvest", "method": "web-search",
                        "ts": time.time()}))
        existing.add(frm)
        n += 1
    return n
