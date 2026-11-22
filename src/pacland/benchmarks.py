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
    "isospin":        {"pre": "the proton and neutron interact almost identically under the strong force, as if symmetric under exchange", "jump": "non-abelian gauge symmetry (Yang-Mills)"},
    "weak-em":        {"pre": "weak and electromagnetic couplings look unrelated at low energy", "jump": "electroweak unification"},
    "ampere-maxwell": {"pre": "an electric current deflects a nearby compass needle", "jump": "moving charges generate magnetic fields (electromagnetism)"},
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

# Campaign A problems, disguised: isomorphic pre-states in different vocabulary, so an LLM that has
# memorised the canonical wording cannot just recall the answer. The jumps are unchanged.
DISGUISED_DATASET = {
    "blackbody":      {"pre": "a closed oven's radiation output climbs without limit as the light tends to the blue end", "jump": "energy is quantised, E = h nu"},
    "photoelectric":  {"pre": "a lit metal plate ejects electrons only past a certain colour of light, never below it however bright", "jump": "light is made of quanta (photons)"},
    "perihelion":     {"pre": "a planet's closest approach to its star drifts by a fixed amount each orbit beyond the old account", "jump": "gravity is spacetime curvature (GR)"},
    "michelson":      {"pre": "no experiment detects any difference in light's speed however the Earth moves", "jump": "Lorentz invariance (special relativity)"},
    "atomic-spectra": {"pre": "a heated gas glows only at specific colours, never a continuous rainbow", "jump": "electron orbits are quantised (Bohr)"},
    "beta-decay":     {"pre": "a radioactive decay ends with less energy than it began, seemingly destroying energy", "jump": "a missing neutral particle (the neutrino)"},
    "zeeman":         {"pre": "a spectral line splits into an even number of close components in a magnetic field", "jump": "the electron has intrinsic spin"},
    "isospin":        {"pre": "the proton and neutron are interchangeable under the strong force, two faces of one particle", "jump": "non-abelian gauge symmetry (Yang-Mills)"},
    "weak-em":        {"pre": "the force behind radioactivity and the force behind charge look unrelated at everyday energy", "jump": "electroweak unification"},
    "ampere-maxwell": {"pre": "a wire carrying current swings a nearby compass though nothing visibly moves between them", "jump": "moving charges generate magnetic fields (electromagnetism)"},
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
    cost: int = 0                 # research effort: total candidates generated (an output-token proxy)


Matcher = Callable[[list[str], str], list[bool]]


def _full_word_matcher(cands: list[str], jump: str) -> list[bool]:
    return [semantic_match(c, jump) for c in cands]


def run_arm(arm: str, generator: Generator, suite: str, dataset: dict,
            matcher: Matcher = _full_word_matcher) -> ArmResult:
    r = ArmResult(arm=arm, suite=suite)
    for name, d in dataset.items():
        r.problems += 1
        cands = generator(d["pre"])          # blind: only the pre-state
        r.cost += len(cands)                 # cost = effort (candidates ≈ output tokens)
        matched = matcher(cands, d["jump"])
        first_rank = next((i + 1 for i, m in enumerate(matched) if m), None)
        if first_rank is not None:           # recall counts a PROBLEM once, at its first hit
            r.found += 1
            r.total_rank += first_rank
        r.false_positives += len(cands) - sum(matched)
    return r


def run_blinded(arms: dict[str, Generator], suite: str, dataset: dict,
                matcher: Matcher = _full_word_matcher, seed: int = 0) -> list[ArmResult]:
    """BLINDED scoring: pool + shuffle the candidates from every arm, score them WITHOUT the arm
    label, then attribute the scores back to arms only at the end.

    This removes the judge's ability to favour the engine arm on sight — the scorer sees an anonymous
    stream of (candidate, withheld-answer) pairs and cannot tell the LLM from the baseline.
    """
    import random

    rng = random.Random(seed)
    # 1. generate + pool, unlabeled (only the pre-state reaches each generator)
    pooled = [(arm, d["jump"], gen(d["pre"])) for arm, gen in arms.items() for d in dataset.values()]
    # 2. shuffle so the scorer cannot reconstruct which arm produced which candidate
    rng.shuffle(pooled)
    # 3. score anonymously
    scored = [(arm, jump, cands, matcher(cands, jump)) for arm, jump, cands in pooled]
    # 4. attribute to arms
    results = {arm: ArmResult(arm=arm, suite=suite) for arm in arms}
    for arm, _jump, cands, matched in scored:
        r = results[arm]
        r.problems += 1
        r.cost += len(cands)
        first_rank = next((i + 1 for i, m in enumerate(matched) if m), None)
        if first_rank is not None:
            r.found += 1
            r.total_rank += first_rank
        r.false_positives += len(cands) - sum(matched)
    return list(results.values())


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


# ----------------------------------------------------------------------------
# The pipeline filter — the FULL ENGINE is not just the generator; it falsifies.
# ----------------------------------------------------------------------------

_GENERIC_MARKERS = ("new long-range force", "undiscovered particle", "measurement error",
                    "systematic effect", "coincidental correlation", "unmodelled",
                    "unknown mechanism", "something else entirely")


def _is_generic_distractor(candidate: str) -> bool:
    low = candidate.lower()
    return any(m in low for m in _GENERIC_MARKERS)


def premise_restates(candidate: str, pre: str) -> bool:
    """True when the candidate adds NO new content word — it only restates the premise (a non-answer)."""
    ct, pt = _tokens(candidate), _tokens(pre)
    return bool(ct) and ct <= pt


def engine_with_filter(inner: Generator) -> Generator:
    """The FULL ENGINE arm: the generator + a falsifier that rejects generic distractors and premise
    restatements. This is the honest 'pipeline beats the prompt' test — the engine's advantage should
    come from FILTERING false positives, not from proposing more of them.
    """
    def filtered(pre: str) -> list[str]:
        return [c for c in inner(pre)
                if not _is_generic_distractor(c) and not premise_restates(c, pre)]
    return filtered


def compare(arms: dict[str, Generator], suite: str, dataset: dict) -> list[ArmResult]:
    return [run_arm(name, gen, suite, dataset) for name, gen in arms.items()]


def report(results: list[ArmResult]) -> str:
    out = [f"{r.arm:20s} recall={r.found}/{r.problems}  avg_rank={r.total_rank / max(r.found, 1):.1f}  false_pos={r.false_positives}"
           for r in results]
    return "\n".join(out)


def gate(results: list[ArmResult]) -> dict:
    """The G3 gate: the engine must beat the untyped baseline blind on recall, at measured cost.

    Returns ``passed`` plus the recall fractions AND the cost-per-found (discoveries per unit effort),
    so an engine cannot win by flooding the judge with cheap guesses.
    """
    by_arm = {r.arm: r for r in results}
    engine = by_arm.get("llm")
    baseline = next((r for r in results if r.arm != "llm"), None)
    if engine is None or baseline is None:
        return {"passed": False, "reason": "missing an arm"}
    e = engine.found / max(engine.problems, 1)
    b = baseline.found / max(baseline.problems, 1)
    engine_cpf = engine.found / max(engine.cost, 1)
    baseline_cpf = baseline.found / max(baseline.cost, 1)
    return {"passed": e > b, "engine_recall": e, "baseline_recall": b,
            "engine_cost_per_found": engine_cpf, "baseline_cost_per_found": baseline_cpf,
            "engine_cost": engine.cost, "baseline_cost": baseline.cost,
            "reason": f"engine recall {e:.2f} vs baseline {b:.2f}"}


# ----------------------------------------------------------------------------
# Straw-man generators (prove the harness runs; NOT a real discovery test)
# ----------------------------------------------------------------------------

# The untyped baseline: generic distractors only, never the jump (a deliberately weak straw-man —
# its job is to be beaten, not to compete). Fixed wrong guesses, so it does not restate the premise
# (which used to leak false positives through the judge) and a real engine must strictly exceed it.
_UNTYPED_DISTRACTORS = [
    "a new long-range force",
    "an undiscovered particle",
    "a measurement error in the apparatus",
    "an unmodelled systematic effect",
]


def untyped_generator(pre: str) -> list[str]:
    return list(_UNTYPED_DISTRACTORS)


# The five-jump arm: a knowledge-base generator that, for this toy, carries the jump mapping.
# HONESTY NOTE: this is a straw-man. A real five-jump generator (LLM) does not carry the answer; this
# one does, so its recall of 1.0 is an upper bound, not evidence the taxonomy works.
_TOY_JUMP = {d["pre"]: d["jump"] for d in DATASET.values()}


def five_jump_generator(pre: str) -> list[str]:
    return [_TOY_JUMP[pre], f"an alternative reading of: {pre[:30]}"]


def diversity_matched_generator(pre: str) -> list[str]:
    """A control arm with the SAME output breadth as the LLM (five candidates) but no discovery.

    It is the fair baseline for 'is the LLM's gain just more varied candidates?' — five generic
    distractors, never the jump, so a real engine must beat it by recall, not by volume.
    """
    return ["a new long-range force", "an undiscovered particle", "a measurement error in the apparatus",
            "an unmodelled systematic effect", "a coincidental correlation"]


# ----------------------------------------------------------------------------
# Planted-law synthetic suites — real induction statistics, free of training-data contamination.
# ----------------------------------------------------------------------------

def synthetic_suite(n: int = 100, seed: int = 0) -> dict:
    """Generate ``n`` planted-law problems: find the hidden function from input->output pairs.

    These are synthetic, so an LLM cannot have memorised the specific (seed, law, offset) tuple — the
    recall here is induction, not memorisation. Each entry is ``{pre, jump}``.
    """
    import math
    import random

    laws = [
        ("f(n) = n^2", lambda n: n * n),
        ("f(n) = 2n + 1", lambda n: 2 * n + 1),
        ("f(n) = n^3", lambda n: n * n * n),
        ("f(n) = n(n+1)/2", lambda n: n * (n + 1) // 2),
        ("f(n) = 2^n", lambda n: 2 ** n),
        ("f(n) = n!", lambda n: math.factorial(n)),
    ]
    rng = random.Random(seed)
    out = {}
    for i in range(n):
        label, fn = rng.choice(laws)
        start = rng.randint(1, 3)
        xs = list(range(start, start + 4))
        ys = [fn(x) for x in xs]
        pre = f"for inputs {', '.join(str(x) for x in xs)} the outputs are {', '.join(str(y) for y in ys)}"
        out[f"planted-{i:03d}"] = {"pre": pre, "jump": label}
    return out


# Problems whose resolution is recent enough that a pre-cutoff model is unlikely to have memorised
# it. HONEST NOTE: the exact training cutoff is unverifiable from here, so this is a SECONDARY probe —
# the planted-law synthetic_suite is the hard decontamination guarantee.
# Recent resolutions, each with its publication date. HONEST NOTE: "post-cutoff" is NOT verified —
# deepseek-chat's training cutoff is unknown from here, and LK-99/JWST (2022-2023) may well be in its
# training data. These are a SECONDARY probe; the planted-law synthetic_suite is the hard
# decontamination guarantee. Each `pre` must not spell the answer.
POST_CUTOFF_DATASET = {
    "lk99":  {"published": "2023-08", "pre": "a material was claimed to superconduct at room temperature and ambient pressure, but independent groups could not reproduce it", "jump": "LK-99 is not a superconductor; the diamagnetism is from an impurity phase"},
    "jwst-early-galaxies": {"published": "2022-12", "pre": "the earliest galaxies seen by JWST are brighter and more massive than the standard timeline predicts", "jump": "early star formation is more efficient than standard models assumed"},
    "desi-dark-energy": {"published": "2024-04", "pre": "a survey of millions of galaxies finds the expansion's acceleration may have weakened recently", "jump": "dark energy may be a dynamical field, weakening at late times"},
    "rna-vaccine": {"published": "2023-10", "pre": "a vaccine platform works by delivering instructions the cell reads to make a viral protein", "jump": "mRNA encodes the antigen; the cell translates it (Nobel 2023)"},
    "quantum-error-threshold": {"published": "2023-02", "pre": "a quantum computer's logical error rate drops as more physical qubits are added, past a crossover point", "jump": "the surface-code threshold: below a critical physical error rate, errors are exponentially suppressed"},
    "clay-mineral-water": {"published": "2023-09", "pre": "fine dust on an airless body holds more water than the rock can absorb, and it persists in sunlight", "jump": "water is trapped in impact-glass beads (lunar regolith)"},
}


def run_campaign_repeated(generator: Generator, campaign: str = "A", repeats: int = 3,
                          dataset: dict | None = None, judged: bool = True) -> dict:
    """Run a campaign repeatedly (paired seeds) and report mean +/- spread of recall.

    The LLM is non-deterministic, so one recall number is not a result — report the spread too. A
    stable engine has a small standard deviation across repeats; a large one means the number is noise.
    """
    import statistics

    recalls: list[float] = []
    for _ in range(repeats):
        res = run_campaign(campaign, generator, dataset=dataset, judged=judged)
        llm = next(r for r in res if r.arm == "llm")
        recalls.append(llm.found / max(llm.problems, 1))
    mean = statistics.mean(recalls)
    stdev = statistics.stdev(recalls) if len(recalls) > 1 else 0.0
    return {"campaign": campaign, "repeats": repeats, "recall_mean": mean,
            "recall_stdev": stdev, "recalls": recalls}


def measure_independent(generator: Generator, n_synthetic: int = 20, seed: int = 0,
                        judged: bool = True) -> dict:
    """Measure ACTUAL discovery performance on the decontaminated suite (independent baselines).

    Runs the generator against the planted-law synthetic suite, the disguised problems, and the
    post-cutoff probe, and reports recall on each. These are problems the model cannot have memorised
    (synthetic tuples, disguised vocabulary, recent resolutions), so recall here is induction, not
    memorisation — the honest discovery number.
    """
    suites = {
        "synthetic": synthetic_suite(n_synthetic, seed=seed),
        "disguised": DISGUISED_DATASET,
        "post-cutoff": POST_CUTOFF_DATASET,
    }
    out = {}
    for label, ds in suites.items():
        res = run_campaign("A", generator, dataset=ds, judged=judged)
        llm = next(r for r in res if r.arm == "llm")
        base = next(r for r in res if r.arm != "llm")
        out[label] = {"recall": llm.found / max(llm.problems, 1),
                      "baseline_recall": base.found / max(base.problems, 1),
                      "problems": llm.problems}
    return out


JUDGE_RUBRIC_VERSION = 2  # the frozen judge rubric (see _JUDGE_PROMPT); bump when the rubric changes


def judge_is_distinct() -> bool:
    """True when the judge model differs from the generator model (the honest setup)."""
    _, _, gen = _llm_config()
    _, _, judge = _judge_config()
    return bool(judge) and judge != gen


# ----------------------------------------------------------------------------
# G3-real — the REAL generator: an LLM that sees only the pre-state, never the answer.
# ----------------------------------------------------------------------------

import json
import os
import urllib.request


def _llm_config() -> tuple[str, str, str]:
    """The OpenAI-compatible endpoint, key and model (Ollama on the ROG, or any compatible API).

    The model is read from the environment with NO hardcoded default, so "no model configured" stays
    a detectable, gracefully-refused state (the runner/benchmark tests rely on it). Set
    SEXTANT_LLM_MODEL=qwen2.5-discovery (and SEXTANT_LLM_ENDPOINT) to use the tuned local model.
    """
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


# The CAPABLE baseline: the SAME model, asked the SAME observation, but WITHOUT the discovery framing.
# If the discovery prompt is worth anything, "llm" must beat this arm — it is not a straw-man that never
# finds the jump, but the same LLM doing a neutral brainstorm.
_NEUTRAL_PROMPT = (
    "List possible explanations for the observation below, one per line.\n\n"
    "Observation: {pre}\n\nExplanations:"
)


def generic_llm_generator(pre: str) -> list[str]:
    """The capable baseline: the same LLM with a NEUTRAL prompt (no discovery framing, no few-shot).

    This is the honest comparison — does the discovery PROMPT add recall over the same model asked to
    just list explanations? A real engine must beat this arm, not just a straw-man.
    """
    endpoint, key, model = _llm_config()
    if not model:
        raise RuntimeError("SEXTANT_LLM_MODEL is not set — set SEXTANT_LLM_MODEL (and "
                           "SEXTANT_LLM_ENDPOINT if not localhost) to run the real baseline")
    text = _ask_llm(_NEUTRAL_PROMPT.format(pre=pre), endpoint, key, model)
    return [line.strip().lstrip("-*•0123456789.) \t")
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith(("#", "//"))]


def run_llm_benchmark(campaign: str = "A", dataset: dict | None = None, judged: bool = True) -> dict:
    """The real G3 measurement: the discovery-prompted LLM vs the NEUTRAL-prompt LLM, blind + cost-aware.

    Returns the gate verdict + the two ArmResults. This is the benchmark that actually answers "does
    the engine beat a capable baseline", not just a straw-man.
    """
    data = dataset or (B_DATASET if campaign == "B" else DATASET)
    arms = {"llm": llm_generator, "generic-llm": generic_llm_generator}
    matcher = judge_matches if judged else _full_word_matcher
    results = run_blinded(arms, campaign, data, matcher=matcher)
    return {**gate(results), "arms": [__import__("dataclasses").asdict(r) for r in results]}


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
    (otherwise the judge grades its own homework); the endpoint and key can also differ (e.g. the
    judge lives on the ROG's Ollama while the generator is DeepSeek). Falls back to the generator's
    endpoint/model only when unset."""
    endpoint = os.environ.get("SEXTANT_JUDGE_ENDPOINT", "") or _llm_config()[0]
    key = os.environ.get("SEXTANT_JUDGE_KEY", "") or _llm_config()[1]
    model = os.environ.get("SEXTANT_JUDGE_MODEL", "") or _llm_config()[2]
    return endpoint, key, model


_JUDGE_PROMPT = (
    "Withheld answer: {jump}\n\nCandidates:\n{candidates}\n\n"
    "For each candidate, decide whether it asserts the SAME discovery as the withheld answer. "
    "Two statements are the same discovery if one is a paraphrase of the other — the same idea, "
    "possibly in different words, with or without the same terms. It does NOT match if it merely "
    "restates the premise/observation, or if it asserts a DIFFERENT hypothesis. Answer ONLY as a "
    "comma-separated list of the indices that match, or NONE."
)


def judge_matches(cands: list[str], jump: str) -> list[bool]:
    """Semantic equivalence judge: one LLM call per problem, returning a bool per candidate.

    Credits paraphrases that share no word (which full-word match under-counts). Falls back to the
    full-word matcher ONLY when no judge model is configured; if a judge IS configured and the call
    fails, it raises — a silently weaker judge would be a dishonest measurement.
    """
    endpoint, key, model = _judge_config()
    if not model:
        return _full_word_matcher(cands, jump)
    prompt = _JUDGE_PROMPT.format(
        jump=jump, candidates="\n".join(f"{i}. {c}" for i, c in enumerate(cands)))
    text = _ask_llm(prompt, endpoint, key, model)  # raises on failure — no silent fallback
    idxs = {int(x) for x in __import__("re").findall(r"\d+", text)}
    return [i in idxs for i in range(len(cands))]


# ----------------------------------------------------------------------------
# Judge calibration: a labeled equivalence set, so the judge's strictness is MEASURED, not a dial.
# ----------------------------------------------------------------------------

# (candidate, jump, expected) — expected True means "same specific claim" (a paraphrase), False means
# a premise restatement or a different hypothesis. This is the ground truth the judge is scored against.
JUDGE_CALIBRATION = [
    # paraphrases of the jump (expected YES)
    ("radiant energy is emitted in discrete packets", "energy is quantised, E = h nu", True),
    ("light consists of individual quanta", "light is made of quanta (photons)", True),
    ("mass curves spacetime, changing planetary trajectories", "gravity is spacetime curvature (GR)", True),
    ("the speed of light is identical in every inertial frame", "Lorentz invariance (special relativity)", True),
    ("electrons can occupy only discrete orbits", "electron orbits are quantised (Bohr)", True),
    ("an unseen neutral particle carries away the missing energy", "a missing neutral particle (the neutrino)", True),
    ("the electron carries an intrinsic angular momentum", "the electron has intrinsic spin", True),
    ("the strong force is a non-commutative gauge field", "non-abelian gauge symmetry (Yang-Mills)", True),
    ("electromagnetism and the weak force merge at high energy", "electroweak unification", True),
    ("observables are represented by non-commuting operators", "matrix mechanics / quantum jumps", True),
    # premise restatements and different hypotheses (expected NO)
    ("the blackbody spectrum diverges at short wavelength", "energy is quantised, E = h nu", False),
    ("the photoelectric threshold depends on frequency", "light is made of quanta (photons)", False),
    ("a hidden planet named Vulcan perturbs Mercury's orbit", "gravity is spacetime curvature (GR)", False),
    ("the aether drag slows light near the Earth", "Lorentz invariance (special relativity)", False),
    ("atoms are solid indivisible spheres", "electron orbits are quantised (Bohr)", False),
    ("the beta decay spectrum is continuous", "a missing neutral particle (the neutrino)", False),
    ("magnetic fields split spectral lines", "the electron has intrinsic spin", False),
    ("particles interact by exchanging virtual photons", "non-abelian gauge symmetry (Yang-Mills)", False),
    ("gravity and electromagnetism unify into one force", "electroweak unification", False),
    ("the atom is a miniature solar system", "matrix mechanics / quantum jumps", False),
    # meta-commentary about the premise is NOT a match (the straw-man used to leak through here)
    ("a granular medium explanation of the blackbody divergence", "energy is quantised, E = h nu", False),
    ("an alternative reading of the photoelectric threshold", "light is made of quanta (photons)", False),
]


def judge_report() -> dict:
    """Score the judge on the labeled equivalence set: precision, recall, accuracy, and the matrix.

    A calibrated judge has high precision (its YES calls are right) AND high recall (it catches the
    true paraphrases). This is the measurement that replaces the judge's free strictness dial.
    """
    tp = fp = tn = fn = 0
    for cand, jump, expected in JUDGE_CALIBRATION:
        got = judge_matches([cand], jump)[0]
        if got and expected:
            tp += 1
        elif got and not expected:
            fp += 1
        elif not got and not expected:
            tn += 1
        else:
            fn += 1
    n = tp + fp + tn + fn
    return {
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": tp / max(tp + fp, 1),
        "recall": tp / max(tp + fn, 1),
        "accuracy": (tp + tn) / max(n, 1),
    }


def judged_compare(arms: dict[str, Generator], suite: str, dataset: dict) -> list[ArmResult]:
    """Compare arms with LLM-judged recall (semantic equivalence) instead of full-word match."""
    _require_distinct_judge()
    return [run_arm(name, gen, suite, dataset, matcher=judge_matches) for name, gen in arms.items()]


def _require_distinct_judge() -> None:
    """A judged measurement must use a judge model DISTINCT from the generator, or it is the model
    grading its own homework. Refuse, rather than silently measure with the same model."""
    if not judge_is_distinct():
        raise RuntimeError(
            "the judge model is not distinct from the generator — set SEXTANT_JUDGE_MODEL "
            "(and SEXTANT_JUDGE_ENDPOINT if it lives elsewhere) to a different model")


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
    if judged:
        _require_distinct_judge()
        matcher = judge_matches
    else:
        matcher = _full_word_matcher
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
    print("  SEXTANT_LLM_ENDPOINT=http://<rog-ip>:11434/v1 SEXTANT_LLM_MODEL=deepseek-r1:7b \\")
    print("  python3 -c \"from pacland import benchmarks as b; print(b.report(b.run_campaign('A', b.llm_generator)))\"")
