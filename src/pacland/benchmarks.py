"""G3 — the benchmark harness (from PLAN-discovery-engine.md).

Four suites + five-arm comparison. This is the gate GPT-6's blueprint calls "non-negotiable": the engine
must beat an untyped baseline, blind, on withheld jumps before it may claim to help discovery. The metric
is recall + rank + cost, never candidate count.

Honesty: the harness is real and runnable. The ARMS are pluggable generators; the toy generators shipped
here are a straw-man to prove the harness executes — a real benchmark needs the real (LLM-backed)
generator, which does not have the answer baked in. The toy arms are structurally honest (they see only
the pre-state, never the withheld jump), but they cannot measure discovery quality; they measure that the
harness runs.

Run:
    python3 -m pacland.benchmarks self-test
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

SUITES = ("historical-rediscovery", "known-solution", "adversarial", "open")
ARMS = ("untyped-baseline", "five-jump", "plus-independent", "full-engine", "human")

# historical-rediscovery dataset: PRE-STATE is what the generator sees; JUMP is withheld from it.
DATASET = {
    "blackbody":      {"pre": "the blackbody spectrum diverges at short wavelength (Rayleigh-Jeans)", "jump": "energy is quantised, E = h nu"},
    "photoelectric":  {"pre": "the photoelectric threshold depends on frequency, not intensity", "jump": "light is made of quanta (photons)"},
    "perihelion":     {"pre": "Mercury's perihelion precesses 43 arcsec/century beyond Newton", "jump": "gravity is spacetime curvature (GR)"},
    "michelson":      {"pre": "no aether drift is detected at any velocity", "jump": "Lorentz invariance (special relativity)"},
    "atomic-spectra": {"pre": "atomic spectra are discrete, not continuous", "jump": "electron orbits are quantised (Bohr)"},
    "beta-decay":     {"pre": "beta decay appears to violate energy conservation", "jump": "a missing neutral particle (the neutrino)"},
    "zeeman":         {"pre": "the anomalous Zeeman effect shows half-integer splittings", "jump": "the electron has intrinsic spin"},
    "isospin":        {"pre": "strong interactions preserve isospin but not locality", "jump": "non-abelian gauge symmetry (Yang-Mills)"},
    "weak-em":        {"pre": "weak and electromagnetic couplings look unrelated at low energy", "jump": "electroweak unification"},
    "mercury-lines":  {"pre": "the discrete spectrum cannot be explained by classical orbits", "jump": "matrix mechanics / quantum jumps"},
}

# A generator maps the PRE-STATE (only) to a list of candidate hypotheses. It never sees the jump.
Generator = Callable[[str], list[str]]


@dataclass
class ArmResult:
    arm: str
    suite: str
    problems: int = 0
    found: int = 0                # recall: the withheld jump was among the candidates
    total_rank: int = 0           # sum of the jump's rank when found
    false_positives: int = 0      # candidates that are not the jump


def run_arm(arm: str, generator: Generator, suite: str, dataset: dict) -> ArmResult:
    r = ArmResult(arm=arm, suite=suite)
    for name, d in dataset.items():
        r.problems += 1
        cands = generator(d["pre"])          # blind: only the pre-state
        for i, c in enumerate(cands):
            if c == d["jump"]:
                r.found += 1
                r.total_rank += i + 1
            else:
                r.false_positives += 1
    return r


def compare(arms: dict[str, Generator], suite: str, dataset: dict) -> list[ArmResult]:
    return [run_arm(name, gen, suite, dataset) for name, gen in arms.items()]


def report(results: list[ArmResult]) -> str:
    out = [f"{r.arm:20s} recall={r.found}/{r.problems}  avg_rank={r.total_rank / max(r.found, 1):.1f}  false_pos={r.false_positives}"
           for r in results]
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Straw-man generators (prove the harness runs; NOT a real discovery test)
# ----------------------------------------------------------------------------

# The untyped baseline: produces distractors only, never the jump (a deliberately weak straw-man).
def untyped_generator(pre: str) -> list[str]:
    return [f"a granular medium explanation of: {pre[:30]}", "a new long-range force"]


# The five-jump arm: a knowledge-base generator that, for this toy, carries the jump mapping.
# HONESTY NOTE: this is a straw-man. A real five-jump generator (LLM) does not carry the answer; this
# one does, so its recall of 1.0 is an upper bound, not evidence the taxonomy works.
_TOY_JUMP = {d["pre"]: d["jump"] for d in DATASET.values()}


def five_jump_generator(pre: str) -> list[str]:
    return [_TOY_JUMP[pre], f"an alternative reading of: {pre[:30]}"]


# ----------------------------------------------------------------------------
# G3-real — the REAL generator: an LLM that sees only the pre-state, never the answer.
# ----------------------------------------------------------------------------

import json
import os
import urllib.request


def _llm_config() -> tuple[str, str, str]:
    """The OpenAI-compatible endpoint, key and model (Ollama on the ROG, or any compatible API)."""
    return (
        os.environ.get("SEXTANT_LLM_ENDPOINT", "http://localhost:11434/v1"),
        os.environ.get("SEXTANT_LLM_KEY", ""),
        os.environ.get("SEXTANT_LLM_MODEL", ""),
    )


def _ask_llm(prompt: str, endpoint: str, key: str, model: str) -> str:
    """One OpenAI-compatible ``/chat/completions`` call, returning the assistant text."""
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(endpoint.rstrip("/") + "/chat/completions", data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


_PROMPT = (
    "You are a scientific hypothesis generator. Given the state of knowledge BEFORE a famous discovery, "
    "generate candidate hypotheses that could explain the observation. Be specific and physics-literate. "
    "Output ONE candidate per line, no numbering, no bullet, no explanation.\n\n"
    "Pre-state: {pre}\n\nCandidates:"
)


def llm_generator(pre: str) -> list[str]:
    """The real generator (G3-real): an LLM that sees only the pre-state. It does NOT carry the answer."""
    endpoint, key, model = _llm_config()
    if not model:
        raise RuntimeError("SEXTANT_LLM_MODEL is not set — set SEXTANT_LLM_MODEL (and "
                           "SEXTANT_LLM_ENDPOINT if not localhost) to run the real generator")
    text = _ask_llm(_PROMPT.format(pre=pre), endpoint, key, model)
    return [line.strip().lstrip("-*•0123456789.) \t")
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith(("#", "//"))]


# ----------------------------------------------------------------------------
# G5 — campaigns: A (calibrate on known answers) -> B (validate on a dataset) -> C (frontier).
# ----------------------------------------------------------------------------

CAMPAIGNS = {
    "A": {"suite": "historical-rediscovery",
          "purpose": "calibrate on known answers, hidden — do this FIRST, never the YM mass gap"},
    "B": {"suite": "known-solution",
          "purpose": "validate on an established dataset with competing explanations (dataset TODO)"},
    "C": {"suite": "open",
          "purpose": "the frontier (YM mass gap) — only after A and B"},
}


def run_campaign(name: str, generator: Generator, dataset: dict | None = None) -> list[ArmResult]:
    """Run one campaign: the given generator against the untyped baseline, on that campaign's suite."""
    if name not in CAMPAIGNS:
        raise ValueError(f"unknown campaign {name!r}; known: {', '.join(CAMPAIGNS)}")
    data = dataset or DATASET
    arms = {"untyped-baseline": untyped_generator, "llm": generator}
    return compare(arms, CAMPAIGNS[name]["suite"], data)


if __name__ == "__main__":
    arms = {"untyped-baseline": untyped_generator, "five-jump": five_jump_generator}
    print("=== historical-rediscovery, blind (harness self-test, straw-man arms) ===")
    print(report(compare(arms, "historical-rediscovery", DATASET)))
    print("\nNOTE: the five-jump arm carries the jump (straw-man) — recall 1.0 is an upper bound, not")
    print("evidence. Run with the real generator via:")
    print("  SEXTANT_LLM_ENDPOINT=http://<rog-ip>:11434/v1 SEXTANT_LLM_MODEL=qwen2.5:7b \\")
    print("  python3 -c \"from pacland import benchmarks as b; print(b.report(b.run_campaign('A', b.llm_generator)))\"")
