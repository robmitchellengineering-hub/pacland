"""The theorem registry — the "yes/no catalog".

Each claim is data, not logic: a natural-language question, the value it asserts,
the oracle class that checks it, the falsifier written *before* the run, the theorem
that supplies the verdict, and the verdict itself.

Verdict alphabet (PLAN-sextant-proof-engine.md):
  FORCED     the value is fixed by the theory (a theorem / a bound)
  FREE       the value is not fixed (a free parameter, an open column)
  IMPOSSIBLE the thing cannot be done (a no-go)

This is the seed. The full catalog is the ~21 claims across QM foundations and the
SM exact structure; new claims are added here, never invented in the engine.
"""
from __future__ import annotations

from dataclasses import dataclass

FORCED = "FORCED"
FREE = "FREE"
IMPOSSIBLE = "IMPOSSIBLE"


@dataclass(frozen=True)
class Claim:
    id: str
    question: str
    value: str
    oracle_class: str
    falsifier: str
    remedy: str
    verdict: str
    keywords: tuple[str, ...] = ()


CLAIMS: tuple[Claim, ...] = (
    Claim(
        id="bell",
        question="What is the classical (local hidden-variable) CHSH bound?",
        value="2",
        oracle_class="exact-symbolic",
        falsifier="a local hidden-variable strategy that exceeds 2",
        remedy="QM.Bell",
        verdict=FORCED,
        keywords=("bell", "classical chsh"),
    ),
    Claim(
        id="chsh",
        question="What is the maximum CHSH violation a quantum strategy can reach?",
        value="2*sqrt(2) ≈ 2.8284271",
        oracle_class="simulated (Phantom/Stim) + kernel-checked (Tsirelson)",
        falsifier="a quantum state whose CHSH value exceeds 2*sqrt(2)",
        remedy="QM.Tsirelson",
        verdict=FORCED,
        keywords=("chsh", "tsirelson"),
    ),
    Claim(
        id="no-cloning",
        question="Can an arbitrary unknown quantum state be copied?",
        value="no",
        oracle_class="kernel-checked (Lean)",
        falsifier="a universal quantum cloning machine",
        remedy="QM.NoCloning",
        verdict=IMPOSSIBLE,
        keywords=("clone", "no-cloning"),
    ),
    Claim(
        id="hypercharge-uniqueness",
        question="Do the SM anomaly conditions fix the hypercharges uniquely?",
        value="yes, up to normalisation and u<->d swap",
        oracle_class="kernel-checked (Lean) + exact-symbolic",
        falsifier="a second anomaly-free hypercharge assignment",
        remedy="SM.Hypercharge",
        verdict=FORCED,
        keywords=("hypercharge",),
    ),
    Claim(
        id="generation-free",
        question="Is the generation number N_gen fixed by anomaly cancellation?",
        value="no (free)",
        oracle_class="kernel-checked (Lean)",
        falsifier="an anomaly condition that fixes N_gen",
        remedy="SM.Generation",
        verdict=FREE,
        keywords=("generation", "n_gen"),
    ),
    Claim(
        id="the-19",
        question="How many free parameters does the Standard Model have?",
        value="19 (the orbit-space dimension)",
        oracle_class="exact-symbolic",
        falsifier="a relation that collapses more than 2 of the 19 correctly",
        remedy="SM.ParameterCount",
        verdict=FREE,
        keywords=("19", "free parameters", "parameter count"),
    ),
)
