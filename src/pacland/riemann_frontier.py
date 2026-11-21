"""riemann_frontier.py — the Riemann Hypothesis partial results, tiered, with the precise open lemma.

From Goldston & Suriajaya, "Zeta Zeros on the Critical Line" (arXiv:2511.20059, expository). The whole
'remove RH from Montgomery' question collapses to ONE falsifiable bound. This module records the tiered
claims and extracts that lemma so the machinery has a concrete target.
"""
from __future__ import annotations

# the tiered claims (name → (statement, tier, source)). tier: 1 established · 2 follows (conditional) ·
# 3 open · 4 numerical · 5 unknown.
CLAIMS: list[dict] = [
    {"name": "von-mangoldt-count", "tier": 1,
     "statement": "N(T) = (T/2π)log(T/2π) − T/2π + O(log T) (the zero count)",
     "source": "von Mangoldt 1905"},
    {"name": "fejer-kernel-identity", "tier": 1,
     "statement": "the Fejér-kernel double sum equals 2∫₀¹ |Σ T^{iαγ}|² (1−α) dα",
     "source": "elementary (note eq. 4.2–4.3)"},
    {"name": "montgomery-fejer-asymptotic", "tier": 2,
     "statement": "the Fejér-kernel sum is (4/3+o(1))·(T/2π)log T",
     "source": "Montgomery 1973, ASSUMING RH"},
    {"name": "montgomery-simple-zeros", "tier": 2,
     "statement": "≥2/3 of zeros are simple",
     "source": "Montgomery 1973, ASSUMING RH"},
    {"name": "goldston-suriajaya-reduction", "tier": 1,
     "statement": "if the horizontal count H(T) ≤ (C+o(1))·(T/2π)log T for some 1≤C<2 UNCONDITIONALLY, "
                  "then ≥(2−C) of the zeros are simple AND on the critical line",
     "source": "Goldston & Suriajaya, Theorem 2 (unconditional reduction)"},
    {"name": "horizontal-count-bound", "tier": 3,
     "statement": "H(T) := Σ_{ρ,ρ'∈Z(T), γ=γ'} 1 ≤ (C+o(1))·(T/2π)log T for some C<2, UNCONDITIONALLY",
     "source": "OPEN — this is the frontier"},
    {"name": "pratt-critical-line-41.7", "tier": 1,
     "statement": "≥41.7% of zeros are on the critical line; ≥40.7% are simple and on the line",
     "source": "Pratt–Robles–Zaharescu–Zeindler 2020 (Levinson's method)"},
    {"name": "platt-trudgian-computation", "tier": 4,
     "statement": "up to height 3·10¹², all 12.36 trillion zeros are on the line and simple",
     "source": "Platt & Trudgian 2021 (computation)"},
    {"name": "simple-zeros-67.92", "tier": 2,
     "statement": "≥67.92% of zeros are simple",
     "source": "Montgomery's method, ASSUMING RH (this is the figure the viral claim misread)"},
]


def frontier_lemma() -> dict:
    """The ONE precise, falsifiable step the whole 'remove RH' question reduces to."""
    return {
        "open_lemma": "Prove, WITHOUT assuming RH, that the horizontal zero-pair count is bounded by "
                      "a constant C < 2:  H(T) = Σ_{γ=γ'} 1  ≤  (C+o(1))·(T/2π)·log T.",
        "why_it_is_the_frontier": "Theorem 2 (the reduction) is UNCONDITIONAL and already proven: any "
                                  "such C<2 immediately yields ≥(2−C) of zeros simple AND on the line. "
                                  "Under RH the bound holds with C=4/3 (Montgomery). The entire gap is "
                                  "one analytic-number-theory estimate.",
        "the_obstacles_when_rh_is_dropped": [
            "the symmetric diagonal terms (pairs ρ, 1−ρ̄ on the same horizontal line, β≠1/2)",
            "the non-symmetric horizontal terms (≥3 zeros on one horizontal line)",
        ],
        "reduction_constant": "C=4/3 → 2/3 of zeros; C=1 → 100% (would prove RH)",
    }


def tiered_claims() -> list[dict]:
    return CLAIMS


def record() -> int:
    """Ingest the RH tiered claims into the registry (the five registries' Properties store)."""
    import time
    from pacland import registry
    n = 0
    for c in CLAIMS:
        registry.add(registry.Entry(
            id=f"rh-{c['name']}",
            kind="property",
            payload={"name": c["name"], "statement": c["statement"], "tier": c["tier"],
                     "domain": "mathematics", "source": c["source"]},
            provenance={"produced_by": "riemann-frontier", "method": "paper-ingest", "ts": time.time()}))
        n += 1
    return n
