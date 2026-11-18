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

# Campaign B — known-solution problems across other disciplines (validate, not just physics).
B_DATASET = {
    "continental-drift":  {"pre": "matching coastlines, fossils, and rock strata span now-separated continents", "jump": "plate tectonics: continents drift on moving plates"},
    "stomach-ulcers":     {"pre": "peptic ulcers recur after acid suppression, and the stomach was thought sterile", "jump": "H. pylori bacteria cause most ulcers"},
    "k-pg-extinction":    {"pre": "a global iridium spike marks the Cretaceous-Paleogene boundary", "jump": "an asteroid impact caused the mass extinction"},
    "childbed-fever":     {"pre": "childbed fever deaths are far higher in the doctor clinic than home births", "jump": "hand disinfection prevents sepsis (germ theory)"},
    "ozone-hole":         {"pre": "stratospheric ozone collapses over Antarctica every austral spring", "jump": "CFC chlorine catalytically destroys ozone"},
    "beriberi":           {"pre": "sailors on polished white rice develop paralysis and heart failure; brown rice prevents it", "jump": "a vitamin B1 (thiamine) deficiency causes beriberi"},
    "prions":             {"pre": "a transmissible spongiform brain disease resists treatments that destroy nucleic acids", "jump": "a misfolded protein (prion) transmits the disease"},
    "sickle-cell":        {"pre": "the sickle-cell allele persists at high frequency only where malaria is endemic", "jump": "heterozygote advantage protects carriers against malaria"},
    "great-oxidation":    {"pre": "banded iron formations and red beds mark a shift in the atmosphere about 2.4 billion years ago", "jump": "oxygenic photosynthesis oxygenated the atmosphere"},
    "endosymbiosis":      {"pre": "mitochondria and chloroplasts have their own DNA, ribosomes, and double membranes", "jump": "they arose from engulfed bacteria (endosymbiosis)"},
}

# Campaign C — the open frontier: no withheld answer, so no recall is possible. The engine proposes;
# SEXTANT falsifies. This is the YM mass gap, the Clay problem.
FRONTIER = ("does non-Abelian lattice Yang-Mills have a mass gap (exponential clustering) in the "
            "continuum limit at weak coupling in d >= 4")

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


Matcher = Callable[[list[str], str], list[bool]]


def _full_word_matcher(cands: list[str], jump: str) -> list[bool]:
    return [semantic_match(c, jump) for c in cands]


def run_arm(arm: str, generator: Generator, suite: str, dataset: dict,
            matcher: Matcher = _full_word_matcher) -> ArmResult:
    r = ArmResult(arm=arm, suite=suite)
    for name, d in dataset.items():
        r.problems += 1
        cands = generator(d["pre"])          # blind: only the pre-state
        matched = matcher(cands, d["jump"])
        first_rank = next((i + 1 for i, m in enumerate(matched) if m), None)
        if first_rank is not None:           # recall counts a PROBLEM once, at its first hit
            r.found += 1
            r.total_rank += first_rank
        r.false_positives += len(cands) - sum(matched)
    return r


_STOP = {"the", "and", "for", "that", "this", "with", "from", "are", "was", "has", "have",
         "its", "not", "but", "can", "could", "would", "should", "their", "they", "then",
         "than", "there", "here", "what", "when", "where", "which", "while", "into", "such",
         "more", "also", "only", "very", "over", "under", "these", "those"}


def _tokens(s: str) -> set[str]:
    return {w for w in __import__("re").findall(r"[a-z]+", s.lower()) if len(w) >= 4 and w not in _STOP}


def semantic_match(candidate: str, jump: str) -> bool:
    """Does the candidate recall the jump's key term? A shared FULL content word.

    A real generator paraphrases, so exact string equality under-measures it. But prefix stemming
    over-matches ("photoelectric" vs "photons"). A shared full word (>= 4 chars, not a stopword) is
    the honest middle: it credits the recall of a key term without the false positives of stemming.
    This is a LOWER bound on discovery; paraphrases that share no word still under-count.
    """
    jt, ct = _tokens(jump), _tokens(candidate)
    if not jt or not ct:
        return candidate.strip().lower() == jump.strip().lower()
    return any(j in ct for j in jt)


def compare(arms: dict[str, Generator], suite: str, dataset: dict) -> list[ArmResult]:
    return [run_arm(name, gen, suite, dataset) for name, gen in arms.items()]


def report(results: list[ArmResult]) -> str:
    out = [f"{r.arm:20s} recall={r.found}/{r.problems}  avg_rank={r.total_rank / max(r.found, 1):.1f}  false_pos={r.false_positives}"
           for r in results]
    return "\n".join(out)


def gate(results: list[ArmResult]) -> dict:
    """The G3 gate: the engine must beat the untyped baseline blind on recall.

    Returns ``passed`` plus the two recall fractions and a one-line reason. This is the honest
    PASS/FAIL before the engine may claim to help discovery; the baseline is a straw-man that
    never finds the jump, so a real engine must strictly exceed it.
    """
    by_arm = {r.arm: r for r in results}
    engine, baseline = by_arm.get("llm"), by_arm.get("untyped-baseline")
    if engine is None or baseline is None:
        return {"passed": False, "reason": "missing an arm"}
    e = engine.found / max(engine.problems, 1)
    b = baseline.found / max(baseline.problems, 1)
    return {"passed": e > b, "engine_recall": e, "baseline_recall": b,
            "reason": f"engine recall {e:.2f} vs baseline {b:.2f}"}


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
# The semantic judge — LLM-judged recall, so paraphrases are credited, not only shared words.
# ----------------------------------------------------------------------------

def _judge_config() -> tuple[str, str, str]:
    """The judge's endpoint/key/model. A model DISTINCT from the generator is the honest choice
    (otherwise the judge grades its own homework); fall back to the generator's model if unset."""
    endpoint, key, gen_model = _llm_config()
    model = os.environ.get("SEXTANT_JUDGE_MODEL", "") or gen_model
    return endpoint, key, model


_JUDGE_PROMPT = (
    "Withheld answer: {jump}\n\nCandidates:\n{candidates}\n\n"
    "Which candidates state the SAME specific claim as the withheld answer? The answer is a NOVEL "
    "discovery; a candidate that merely restates the premise or describes the observation does NOT "
    "match. Only mark a candidate that expresses the same new idea. Answer ONLY as a comma-separated "
    "list of the indices that match, or NONE."
)


def judge_matches(cands: list[str], jump: str) -> list[bool]:
    """Semantic equivalence judge: one LLM call per problem, returning a bool per candidate.

    Credits paraphrases that share no word (which full-word match under-counts). Falls back to the
    full-word matcher when no judge model is configured or the call fails.
    """
    endpoint, key, model = _judge_config()
    if not model:
        return _full_word_matcher(cands, jump)
    prompt = _JUDGE_PROMPT.format(
        jump=jump, candidates="\n".join(f"{i}. {c}" for i, c in enumerate(cands)))
    try:
        text = _ask_llm(prompt, endpoint, key, model)
    except Exception:
        return _full_word_matcher(cands, jump)
    idxs = {int(x) for x in __import__("re").findall(r"\d+", text)}
    return [i in idxs for i in range(len(cands))]


def judged_compare(arms: dict[str, Generator], suite: str, dataset: dict) -> list[ArmResult]:
    """Compare arms with LLM-judged recall (semantic equivalence) instead of full-word match."""
    return [run_arm(name, gen, suite, dataset, matcher=judge_matches) for name, gen in arms.items()]


# ----------------------------------------------------------------------------
# G5 — campaigns: A (calibrate on known answers) -> B (validate on a dataset) -> C (frontier).
# ----------------------------------------------------------------------------

CAMPAIGNS = {
    "A": {"suite": "historical-rediscovery", "dataset": DATASET,
          "purpose": "calibrate on known answers, hidden — do this FIRST, never the YM mass gap"},
    "B": {"suite": "known-solution", "dataset": B_DATASET,
          "purpose": "validate on an established cross-discipline dataset"},
    "C": {"suite": "open", "dataset": None,
          "purpose": "the frontier (YM mass gap) — proposals only, no withheld answer to recall"},
}


def run_campaign(name: str, generator: Generator, dataset: dict | None = None,
                 judged: bool = True) -> list[ArmResult]:
    """Run one campaign: the given generator against the untyped baseline, on that campaign's suite.

    The default metric is the LLM semantic judge (honest recall of paraphrases); pass ``judged=False``
    for the deterministic full-word lower bound. Set ``SEXTANT_JUDGE_MODEL`` to a model DISTINCT from
    the generator so the judge does not grade its own homework (falls back to the generator's model
    if unset). Campaign C has no withheld answer, so use ``run_frontier`` instead.
    """
    if name not in CAMPAIGNS:
        raise ValueError(f"unknown campaign {name!r}; known: {', '.join(CAMPAIGNS)}")
    if name == "C":
        raise ValueError("campaign C is the open frontier — use run_frontier (no recall)")
    camp = CAMPAIGNS[name]
    data = dataset or camp["dataset"]
    arms = {"untyped-baseline": untyped_generator, "llm": generator}
    matcher = judge_matches if judged else _full_word_matcher
    return [run_arm(n, g, camp["suite"], data, matcher=matcher) for n, g in arms.items()]


def run_frontier(generator: Generator) -> list[str]:
    """Campaign C: the open frontier. No withheld answer, so no recall — return the proposals."""
    return generator(FRONTIER)


if __name__ == "__main__":
    arms = {"untyped-baseline": untyped_generator, "five-jump": five_jump_generator}
    print("=== historical-rediscovery, blind (harness self-test, straw-man arms) ===")
    print(report(compare(arms, "historical-rediscovery", DATASET)))
    print("\nNOTE: the five-jump arm carries the jump (straw-man) — recall 1.0 is an upper bound, not")
    print("evidence. Run with the real generator via:")
    print("  SEXTANT_LLM_ENDPOINT=http://<rog-ip>:11434/v1 SEXTANT_LLM_MODEL=qwen2.5:7b \\")
    print("  python3 -c \"from pacland import benchmarks as b; print(b.report(b.run_campaign('A', b.llm_generator)))\"")
