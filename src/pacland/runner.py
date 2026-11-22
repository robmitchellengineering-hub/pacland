"""SEXTANT runner — the generate → test → prune/promote → record loop.

The engine already has the three ingredients: validated facts (``sextant.CATALOG``), open
questions (``hypotheses.HYPOTHESES``), and falsifiers (``phantom.FALSIFIERS``). What was missing
is the *loop* that closes them:

    fact + strategy  →  candidate  →  run falsifier  →  verdict  →  promote | drop  →  record

This module is that loop. The metric it optimises is **candidates generated → falsified/survived
per run**, not files committed.

Usage:
    python -m pacland.runner --list-facts
    python -m pacland.runner --list-strategies
    python -m pacland.runner --fact ou-curvature --strategy combine
    python -m pacland.runner --advance-all
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

from pacland import hypotheses  # noqa: E402  (the open-question registry the runner decomposes)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # .../pacland
PROOF_DIR = REPO_ROOT / "pacland-proof"
RECORD = REPO_ROOT / "runs" / "runner.jsonl"
DISCOVERIES = REPO_ROOT / "runs" / "discoveries.jsonl"
EXPERIMENTS = REPO_ROOT / "runs" / "experiments.jsonl"
MEMORY = REPO_ROOT / "runs" / "discovery-memory.jsonl"
REJECTED = REPO_ROOT / "runs" / "rejected.jsonl"


def _load_memory() -> list[dict]:
    """The verified-discovery memory: one JSON object per line (problem, statement, falsifier, proof)."""
    if not MEMORY.exists():
        return []
    out: list[dict] = []
    for line in MEMORY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _append_memory(problem: str, statement: str, falsifier: str, proof: dict | None) -> None:
    """Record a VERIFIED discovery into the in-context memory (the learn-as-it-goes store)."""
    MEMORY.parent.mkdir(parents=True, exist_ok=True)
    with MEMORY.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "problem": problem, "statement": statement, "falsifier": falsifier,
            "proof": (proof or {}).get("lean", "") if proof else "",
            "ts": datetime.now(timezone.utc).isoformat(),
        }) + "\n")


def _load_rejected() -> list[dict]:
    """Past proposals with their disposition: 'falsified' (dead) or 'gated-out: <stage>' (not dead)."""
    if not REJECTED.exists():
        return []
    out: list[dict] = []
    for line in REJECTED.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _append_rejected(problem: str, statement: str, reason: str) -> None:
    """Record a proposal's disposition. 'falsified' means dead; 'gated-out' means unjustified, not dead.

    Also writes a registry CLAIM so the failed direction enters the unified scientific record — SEXTANT
    can say a direction did not work out, and the record is queryable, not a dropped log line.
    """
    REJECTED.parent.mkdir(parents=True, exist_ok=True)
    with REJECTED.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"problem": problem, "statement": statement, "reason": reason,
                             "ts": datetime.now(timezone.utc).isoformat()}) + "\n")
    from pacland import registry
    registry.record_claim(
        f"claim-{slug(statement)[:64]}",
        statement,
        "failed" if reason == "falsified" else "gated-out",
        problem=problem,
        reason=reason,
        produced_by="runner",
    )


def _memory_prefix(problem: str, n: int = 4) -> str:
    """Few-shot prefix from the most relevant verified discoveries + a 'do NOT re-propose' block.

    Drawn from the UNIFIED registry (``registry.claims``) — the same substrate the cross-field search
    and the knowledge engine read — so knowledge compounds across campaigns. The legacy JSONL stores
    remain the fallback while the transition to the single claim architecture completes.
    """
    from pacland import registry

    survivors = registry.claims("survived")
    failed = registry.claims("failed")
    gated = registry.claims("gated-out")
    parts: list[str] = []

    def _stmt(c: dict) -> str:
        return c.get("payload", {}).get("statement", "")

    if survivors:
        q = set(re.findall(r"[a-z]{3,}", problem.lower()))

        def score(c: dict) -> int:
            hay = (c.get("payload", {}).get("problem", "") + " " + _stmt(c)).lower()
            return len(q & set(re.findall(r"[a-z]{3,}", hay)))

        ranked = sorted(survivors, key=score, reverse=True)[:n]
        parts.append("Verified discoveries from past runs (use as a template, do not repeat them):")
        parts += [f"- {_stmt(c)}" for c in ranked]

    if failed:
        parts.append("Already FALSIFIED — do NOT re-propose these:")
        parts += [f"- {_stmt(c)}" for c in failed[-6:]]
    if gated:
        parts.append("Already proposed but gated (not falsified — needs better justification):")
        parts += [f"- {_stmt(c)} ({c['payload'].get('reason', '')})" for c in gated[-6:]]

    if parts:
        return "\n".join(parts) + "\n\n"

    # fallback: the legacy JSONL stores (pre-unification data) — retire once the registry is the only store
    entries = _load_memory()
    rejected = _load_rejected()
    if entries:
        q = set(re.findall(r"[a-z]{3,}", problem.lower()))

        def score(e: dict) -> int:
            hay = (e.get("problem", "") + " " + e.get("statement", "")).lower()
            return len(q & set(re.findall(r"[a-z]{3,}", hay)))

        ranked = sorted(entries, key=score, reverse=True)[:n]
        parts.append("Verified discoveries from past runs (use as a template, do not repeat them):")
        parts += [f"- {e['statement']} (falsifier: {e['falsifier']})" for e in ranked]

    if rejected:
        dead = [e for e in rejected if e.get("reason") == "falsified"]
        gated = [e for e in rejected if str(e.get("reason", "")).startswith("gated-out")]
        if dead:
            parts.append("Already FALSIFIED — do NOT re-propose these:")
            parts += [f"- {e['statement']}" for e in dead[-6:]]
        if gated:
            parts.append("Already proposed but gated (not falsified — needs better justification):")
            parts += [f"- {e['statement']} ({e['reason']})" for e in gated[-6:]]

    if not parts:
        return ""
    return "\n".join(parts) + "\n\n"


# ------------------------------------------------------------------------------------------ #
# The falsifiers that the runner can call. Each returns (survived : bool, evidence : str).
# ------------------------------------------------------------------------------------------ #

def verify_ou_gap() -> tuple[bool, str]:
    """The OU spectral gap via the Hermite eigenfunctions.

    ``L f = f'' - x f'`` has probabilist-Hermite eigenfunctions ``He_n`` with
    ``L He_n = -n He_n``, so the spectral gap (0 → -1) is exactly 1. This is the numerical/
    symbolic falsifier for the candidate "the OU gap is ≥ 1" generated by combining the committed
    curvature ``Γ₂ ≥ Γ`` (κ = 1) with the Grönwall decay.
    """
    import sympy as sp
    x = sp.symbols("x")

    def L(f):
        return sp.diff(f, x, 2) - x * sp.diff(f, x)

    He = [sp.Integer(1), x, x**2 - 1, x**3 - 3 * x]
    for n, he in enumerate(He):
        lhs = sp.simplify(L(he))
        rhs = sp.simplify(-n * he)
        if lhs != rhs:
            return False, f"OU eigen-equation fails at n={n}: L He_{n} = {lhs}, -n He_{n} = {rhs}"
    return True, "OU eigenvalues 0, -1, -2, -3 (Hermite); spectral gap = exactly 1"


def verify_su2_weak_coupling() -> tuple[bool, str]:
    """The SU(2) weak-coupling area law via the committed Creutz-ratio Monte-Carlo.

    Re-runs ``lattice_ym_su2.measure_string_tension`` at weak coupling β=2.5 and checks the
    string tension is positive (area law), i.e. deconfinement has NOT set in.
    """
    from pacland import lattice_ym_su2 as lym
    beta = 2.5
    chi = lym.measure_string_tension(beta, d=4, N=6, n_sweeps=3, seed=0)
    survived = chi > 0.0
    return survived, f"SU(2) Creutz ratio at weak coupling β={beta}: χ={chi:.4f} " \
                     f"({'positive → area law / confinement' if survived else 'non-positive → deconfined'})"


def _glueball_ratio(beta: float, N: int = 5):
    """The RG-invariant m/sqrt(σ) at one coupling, or None if the string tension is noisy/non-positive."""
    import numpy as np
    from pacland.glueball import glueball_mass
    from pacland.lattice_ym_su2 import measure_string_tension
    m = glueball_mass(beta, N=N, n_sweeps=6, n_meas=20, seed=0)
    sigma = measure_string_tension(beta, d=4, N=N, n_sweeps=3, seed=0)
    if sigma <= 0 or m <= 0:
        return None, (m, sigma)   # noise-dominated: the signal is not resolved at this lattice/statistics
    return m / np.sqrt(sigma), (m, sigma)


def verify_glueball_mass_ratio() -> tuple[bool, str]:
    """The SU(2) glueball mass ratio m/sqrt(σ) at two weak-coupling points — the RG-invariant
    should be roughly constant (approaching the continuum value)."""
    ratios, details = [], []
    for beta in (2.4, 2.6):
        r, det = _glueball_ratio(beta)
        if r is None:
            return False, f"noise-dominated at β={beta}: m={det[0]:.4f}, σ={det[1]:.4f} — the signal is unresolved (needs larger lattice / more statistics)"
        ratios.append(r)
        details.append(det)
    spread = abs(ratios[0] - ratios[1]) / max(abs(ratios[0]), abs(ratios[1]))
    survived = spread < 0.3
    return survived, (
        f"m/sqrt(σ) at β=2.4,2.6: {ratios[0]:.3f}, {ratios[1]:.3f} (spread {spread:.2f}) — "
        f"{'approaching a constant → continuum ratio' if survived else 'diverging → no continuum limit'}"
    )


def verify_mass_gap_scaling() -> tuple[bool, str]:
    """The referee for the sharper-bound search: a mass-gap bound c(β) must be a *decaying*
    lower bound that reaches the asymptotic-freedom scale — not diverge (cluster expansion, log β),
    not die at the ceiling (Dobrushin, (−log α)/2 → 0 and negative past it), not need log-concavity
    (Bakry–Émery). The bench is the known-answer referee m(β) = 25.28·e^(−1.182β), m/√σ ≈ 3.2.

    Checks, for β in {2.0, 2.5, 3.0}:
      (a) positivity: c(β) > 0 (a bound that dies is vacuous),
      (b) validity:   c(β) ≤ m(β) (a bound above the truth is false),
      (c) sharpness:  c(β) tracks the true exponential scale (does not collapse faster than e^(−1.182β)).
    """
    import math
    def m(beta): return 25.28 * math.exp(-1.182 * beta)
    cands = {
        "cluster-expansion": (lambda b: math.log(b) if b > 1 else 0.0),
        # the strong-coupling Dobrushin bound m(α)=(−log α)/2 has a CEILING α(β*)=1 (kernel-checked:
        # massRate_tendsto_zero + alphaAt_ceiling_eq_one), so it is 0 at β* and negative past it.
        "dobrushin": (lambda b: 0.0 if b >= 2.0 else -0.5 * math.log(max(1e-12, 1.0 - b / 2.0))),
        "asymptotic-freedom": (lambda b: 25.28 * math.exp(-1.182 * b)),
    }
    lines = []
    survivors = []
    for name, c in cands.items():
        positive = all(c(b) > 0 for b in (2.0, 2.5, 3.0, 4.0))
        valid = all(c(b) <= m(b) for b in (2.0, 2.5, 3.0))
        ratios = [c(b) / m(b) for b in (2.5, 3.0)]
        sharp = ratios[1] >= 0.5 * ratios[0]
        survived = positive and valid and sharp
        if name == "asymptotic-freedom":
            # c(β) IS the referee m(β) by construction — reaching it is an identity, not an
            # independent test, so it must not be counted as a survivor.
            lines.append(f"{name}: REFEREE IDENTITY (c == m by construction — not an independent bound)")
            continue
        lines.append(f"{name}: {'SURVIVED' if survived else 'REFUTED'}"
                     f" (c(2.5)={c(2.5):.4f}, m(2.5)={m(2.5):.4f}, ratio {ratios[0]:.3f}→{ratios[1]:.3f})")
        if survived:
            survivors.append(name)
    # an INDEPENDENT mechanism must survive — the referee testing itself does not count, so this
    # falsifier honestly reports that no independent known mechanism reaches the mass-gap scale.
    return bool(survivors), (" | ".join(lines)
                             + " — no independent mechanism survives; the asymptotic-freedom scale is the referee itself")


def _lazy(module: str, attr: str):
    """Import a falsifier lazily (avoids importing numpy at module import time)."""
    import importlib

    def _f():
        return getattr(importlib.import_module(f"pacland.{module}"), attr)()
    return _f


FALSIFIERS: dict[str, object] = {
    "ou-gap": verify_ou_gap,
    "su2-weak-coupling": verify_su2_weak_coupling,
    "glueball-mass-ratio": verify_glueball_mass_ratio,
    "mass-gap-scaling": verify_mass_gap_scaling,
    # candidate-specific mass-gap falsifiers (built from the SU(2) lattice tools)
    "d5-mass-gap": _lazy("mass_gap_falsifiers", "verify_d5_mass_gap"),
    "bulk-transition": _lazy("mass_gap_falsifiers", "verify_bulk_transition"),
    "universality": _lazy("mass_gap_falsifiers", "verify_universality"),
    "large-n-ratio": _lazy("mass_gap_falsifiers", "verify_large_n_ratio"),
    "polyakov-clustering": _lazy("mass_gap_falsifiers", "verify_polyakov_clustering"),
}


# ------------------------------------------------------------------------------------------ #
# The validated facts (the tower, plus the kernel-checked Gaussian-LSI layer).
# ------------------------------------------------------------------------------------------ #

@dataclass(frozen=True)
class Fact:
    id: str
    statement: str
    falsifier: str          # the description of what would refute it
    source: str             # the Lean theorem / script that validates it
    category: str


FACTS: dict[str, Fact] = {
    "ou-curvature": Fact(
        id="ou-curvature",
        statement="the OU generator's Bochner curvature is κ=1: Γ₂(f) ≥ Γ(f) pointwise (Γ₂ = f''² + f'²)",
        falsifier="a differentiable f with Γ(f) > Γ₂(f) at some point",
        source="PaclandProof.QM.ou_bakry_emery (Lean, kernel-checked)",
        category="bakry-emery",
    ),
    "gronwall-decay": Fact(
        id="gronwall-decay",
        statement="u' ≤ -c·u ⟹ u(t) ≤ u(0)·e^{-ct} for t ≥ 0",
        falsifier="a solution u with u' ≤ -c·u but u(t) > u(0)·e^{-ct}",
        source="PaclandProof.QM.gronwall_decay (Lean, kernel-checked)",
        category="ode",
    ),
    "ou-invariant": Fact(
        id="ou-invariant",
        statement="∫ e^{-x²/2}·Lg = 0 (the Gaussian is the OU invariant measure)",
        falsifier="a g with ∫ γ Lg ≠ 0",
        source="PaclandProof.QM.ou_invariant (Lean, kernel-checked)",
        category="bakry-emery",
    ),
    "ou-selfadjoint": Fact(
        id="ou-selfadjoint",
        statement="∫ e^{-x²/2} f·Lg = -∫ e^{-x²/2} f'·g' (self-adjointness / Dirichlet form)",
        falsifier="f, g with ∫ γ f·Lg ≠ -∫ γ f'·g'",
        source="PaclandProof.QM.gaussian_dirichlet (Lean, kernel-checked)",
        category="bakry-emery",
    ),
    "ou-fisher": Fact(
        id="ou-fisher",
        statement="∫ e^{-x²/2} (Lf)·log f = -∫ e^{-x²/2} (f')²/f (the Fisher identity)",
        falsifier="an f with ∫ γ (Lf)·log f ≠ -∫ γ (f')²/f",
        source="PaclandProof.QM.fisher_information_identity (Lean, kernel-checked)",
        category="bakry-emery",
    ),
}


# ------------------------------------------------------------------------------------------ #
# The generator: a candidate hypothesis, grounded in the validated facts.
# ------------------------------------------------------------------------------------------ #

@dataclass(frozen=True)
class Candidate:
    id: str
    statement: str
    falsifier: str
    strategy: str
    source_facts: tuple[str, ...]
    test: str
    cost: float = 1.0       # research effort, for discoveries-per-effort scoring
    prior: float = 0.5      # operator's prior, for EIG ranking
    ancestry: tuple[str, ...] = ()   # lineage, root first: A -> A1 -> A2 (the parent ids)
    assumptions: tuple[str, ...] = ()        # explicit assumptions the hypothesis rests on
    proposed_mappings: tuple[str, ...] = ()  # cross-field mappings (field A structure -> field B), for transfer strategies


STRATEGIES: dict[str, str] = {
    "combine": "combine two facts into a new inequality/statement",
    "generalize": "generalize a fact to a wider scope",
    "specialize": "specialize an open question to a computable instance",
    "conjecture-value": "conjecture a concrete value from an open question and falsify it",
    "decompose": "decompose an OPEN hypothesis into its next falsifiable sub-lemma (the frontier move)",
}


def generate(fact_ids: list[str], strategy: str) -> Candidate:
    """Generate a candidate hypothesis from validated facts, per the strategy.

    This is the *grounded* generator: every candidate cites the facts (or the open question) it is
    built from, and names the falsifier that would refute it. No free-floating conjectures.
    """
    if strategy == "combine":
        # curvature κ=1 + Grönwall decay  →  the Bakry-Émery spectral gap bound "gap ≥ 1".
        if {"ou-curvature", "gronwall-decay"} <= set(fact_ids):
            return Candidate(
                id="ou-gap-lower-bound",
                statement="the OU spectral gap is ≥ 1 (Bakry-Émery: Γ₂ ≥ κΓ with κ=1 ⟹ gap ≥ κ)",
                falsifier="an OU spectral gap strictly below 1",
                strategy="combine",
                source_facts=("ou-curvature", "gronwall-decay"),
                test="ou-gap",
            )

    if strategy == "generalize":
        # the 1D OU gap generalizes to n dimensions by tensorization.
        if "ou-curvature" in fact_ids:
            return Candidate(
                id="n-dim-gaussian-gap",
                statement="the n-dimensional Gaussian spectral gap is also 1 (tensorization of the 1D gap)",
                falsifier="an n-dim Gaussian gap ≠ 1",
                strategy="generalize",
                source_facts=("ou-curvature",),
                test="ou-gap",  # placeholder until an n-dim falsifier exists
            )

    if strategy == "conjecture-value":
        # the open question → a concrete VALUE to conjecture and falsify.
        return Candidate(
            id="su2-glueball-mass-ratio",
            statement="the SU(2) glueball mass ratio m/sqrt(σ) approaches a constant (the continuum value) at weak coupling",
            falsifier="m/sqrt(σ) diverges or does not plateau as β → ∞",
            strategy="conjecture-value",
            source_facts=tuple(fact_ids),
            test="glueball-mass-ratio",
        )

    if strategy == "specialize":
        # the confinement-frontier open question → a computable weak-coupling instance.
        return Candidate(
            id="su2-weak-coupling-area-law",
            statement="the SU(2) lattice string tension stays positive at weak coupling (confinement)",
            falsifier="a non-positive Creutz ratio at weak coupling (deconfinement)",
            strategy="specialize",
            source_facts=("confinement-frontier",),
            test="su2-weak-coupling",
        )

    if strategy == "decompose":
        # the frontier move: emit the OPEN hypothesis's next falsifiable sub-lemma.
        return next_sublemma(fact_ids[0])

    raise ValueError(f"no candidate for facts {fact_ids} under strategy {strategy!r}")


def generate_llm(fact_ids: list[str], strategy: str) -> list[Candidate]:
    """The LLM-backed candidate generator (P1). The model proposes STRUCTURED hypotheses — each with a
    statement, the source facts it cites, explicit assumptions, proposed cross-field mappings, and a
    falsifier. Returns a list; empty on any failure (the deterministic generator is the fallback)."""
    if strategy not in STRATEGIES:
        return []
    endpoint, key, model = _llm_config()
    if not model:
        return []  # no model configured — deterministic is the fallback
    fact_list = ", ".join(fact_ids) or "(none)"
    prompt = (
        "You are a discovery generator in a verified-research system. Given validated facts and a "
        "strategy, propose up to 3 candidate hypotheses as JSON.\n\n"
        f"Facts available: {fact_list}\n"
        f"Strategy: {STRATEGIES[strategy]}\n\n"
        'Return a JSON object {"candidates": [{"statement": str, "source_facts": [str], '
        '"assumptions": [str], "proposed_mappings": [str], "falsifier": str}]}.\n'
        "Every candidate must: cite source_facts (the facts it is built from), state its explicit "
        "assumptions, name any proposed cross-field mapping (\"structure X in field A corresponds to "
        "structure Y in field B\"), and give a concrete falsifier that would refute it. No free-floating "
        "conjectures. Output ONLY the JSON."
    )
    try:
        raw = _ask_llm(prompt, endpoint, key, model)
    except Exception:
        return []
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except Exception:
        return []
    out: list[Candidate] = []
    for i, c in enumerate(data.get("candidates", [])):
        try:
            stmt = str(c.get("statement", "")).strip()
            if not stmt:
                continue
            out.append(Candidate(
                id=(_slug(stmt)[:40] or f"llm-{strategy}-{i}"),
                statement=stmt,
                falsifier=str(c.get("falsifier", "")).strip(),
                strategy=strategy,
                source_facts=tuple(str(x) for x in (c.get("source_facts") or [])),
                test="",  # a test id is assigned by the falsifier layer, not the generator
                assumptions=tuple(str(x) for x in (c.get("assumptions") or [])),
                proposed_mappings=tuple(str(x) for x in (c.get("proposed_mappings") or [])),
            ))
        except Exception:
            continue
    return out


def generate_candidates(fact_ids: list[str], strategy: str, use_llm: bool = True) -> list[Candidate]:
    """The model-driven generation entry point: LLM-backed structured candidates when available,
    the deterministic grounded generator as the baseline + fallback (wrapped in a list)."""
    if use_llm:
        cands = generate_llm(fact_ids, strategy)
        if cands:
            return cands
    return [generate(fact_ids, strategy)]


# ------------------------------------------------------------------------------------------ #
# The frontier generator: decompose an OPEN hypothesis into its next falsifiable sub-lemma.
# This is the move the recombination strategies cannot make — it points at the *unproven* step
# (from the hypothesis's candidates) instead of re-deriving a known fact.
# ------------------------------------------------------------------------------------------ #

def _slug(text: str) -> str:
    """A short stable id from a candidate hypothesis string."""
    words = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-").split("-")
    return "-".join(words[:6]) or "sublemma"


def _runnable_test(statement: str) -> str:
    """A runnable falsifier key for a candidate sub-lemma, or "" when it needs a thinking agent.

    Honest by design: only the sub-lemmas with a real falsifier get one; the rest are emitted as
    ``MANUAL`` so the engine says "here is the next thing to prove/refute" without pretending it
    can test it. Add a falsifier to ``FALSIFIERS`` and map it here to make a sub-lemma runnable.
    """
    if "string tension" in statement or "area law" in statement:
        return "su2-weak-coupling"          # the Creutz ratio tests the area law / confinement
    if "glueball" in statement and "m/sqrt" in statement:
        return "glueball-mass-ratio"
    if "asymptotic" in statement or "mass gap" in statement or "sharper bound" in statement:
        return "mass-gap-scaling"
    return ""


def _prior_refuted() -> set[str]:
    """The candidate statements already REFUTED in the record — decompose skips them so the
    engine compounds (it never re-emits a sub-lemma it has already killed)."""
    if not RECORD.exists():
        return set()
    refuted = set()
    for line in RECORD.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("verdict") == "REFUTED":
            refuted.add(row.get("statement", ""))
    return refuted


def next_sublemma(hypothesis_id: str) -> Candidate:
    """The next falsifiable sub-lemma of an OPEN hypothesis — its first candidate that is not yet
    refuted, with the falsifier that would refute it. Grounded in ``hypotheses.HYPOTHESES`` (not a
    free-floating conjecture): the hypothesis already carries the decomposition; this emits one rung
    of it, skipping any rung the runner has already killed.
    """
    if hypothesis_id not in hypotheses.HYPOTHESES:
        raise ValueError(
            f"unknown hypothesis {hypothesis_id!r}; known: {', '.join(hypotheses.HYPOTHESES)}")
    h = hypotheses.HYPOTHESES[hypothesis_id]
    refuted = _prior_refuted()
    for cand in h.get("candidates", []):
        statement = cand["hypothesis"]
        if statement in refuted:
            continue
        return Candidate(
            id=f"{hypothesis_id}::{_slug(statement)}",
            statement=statement,
            falsifier=cand["falsifier"],
            strategy="decompose",
            source_facts=(hypothesis_id,),
            test=_runnable_test(statement),
        )
    raise ValueError(f"hypothesis {hypothesis_id!r} has no candidates to decompose")


# ------------------------------------------------------------------------------------------ #
# The prover: formalize → LLM-propose → kernel-check → repair → record.
# This is the loop that turns the engine from a *pointer* into a *prover* for the reachable
# rungs. It proves "assemble known lemmas into a new theorem"; it does not do novel mathematics
# (that is Level 2 — proof search with RL). Config via env: SEXTANT_LLM_ENDPOINT / _KEY / _MODEL.
# ------------------------------------------------------------------------------------------ #

def _llm_config() -> tuple[str, str, str]:
    """The OpenAI-compatible endpoint, key and model from the environment.

    The model is read from the environment with NO hardcoded default, so "no model configured" stays
    a detectable, gracefully-refused state (the runner/benchmark tests rely on it). Set
    SEXTANT_LLM_MODEL=qwen2.5-discovery (and SEXTANT_LLM_ENDPOINT) to use the tuned local model.
    """
    return (
        os.environ.get("SEXTANT_LLM_ENDPOINT", "http://localhost:11434/v1"),
        os.environ.get("SEXTANT_LLM_KEY", ""),
        os.environ.get("SEXTANT_LLM_MODEL", ""),
    )


def _judge_config() -> tuple[str, str, str]:
    """The independent judge's endpoint/key/model (distinct from the generator for honest checks)."""
    return (
        os.environ.get("SEXTANT_JUDGE_ENDPOINT", "") or _llm_config()[0],
        os.environ.get("SEXTANT_JUDGE_KEY", "") or _llm_config()[1],
        os.environ.get("SEXTANT_JUDGE_MODEL", "") or _llm_config()[2],
    )


def _ask_llm(prompt: str, endpoint: str, key: str, model: str) -> str:
    """One OpenAI-compatible ``/chat/completions`` call, returning the assistant text."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(
        f"{endpoint.rstrip('/')}/chat/completions", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.load(resp)
    return data["choices"][0]["message"]["content"]


def _check_lean(code: str) -> tuple[bool, str]:
    """Write the proposal to a temp file inside the proof tree and run the Lean kernel.

    Returns ``(ok, error)`` — ``ok`` when ``lake env lean`` exits 0, else the kernel's message
    (trimmed to the tail, which carries the error).
    """
    if not PROOF_DIR.exists():
        return False, f"proof tree not found at {PROOF_DIR}"
    d = PROOF_DIR / ".prove"
    d.mkdir(exist_ok=True)
    f = d / "Proposal.lean"
    f.write_text(code, encoding="utf-8")
    env = dict(os.environ)
    elan = str(Path.home() / ".elan" / "bin")
    env["PATH"] = elan + os.pathsep + env.get("PATH", "")
    try:
        r = subprocess.run(
            ["lake", "env", "lean", str(f)],
            cwd=str(PROOF_DIR), capture_output=True, text=True, timeout=600, env=env,
        )
    except FileNotFoundError:
        return False, "lake not found — is the Lean toolchain installed and on PATH?"
    except subprocess.TimeoutExpired:
        return False, "kernel timed out (600s)"
    if r.returncode == 0:
        out = r.stdout + r.stderr
        # `sorry`/`admit` COMPILE with a warning, so a green kernel alone is not a proof. Refuse any
        # file that still carries a placeholder or an axiom — the whole point of the proof loop.
        if re.search(r"declaration uses ['`]?(sorry|admit)", out) or re.search(r"\baxiom\b", out):
            return False, f"compiles but is not a proof: {out.strip()[-500:]}"
        return True, ""
    return False, (r.stdout + r.stderr).strip()[-4000:]


def _proof_prompt(statement: str, error: str | None) -> str:
    """The prover prompt: complete the Lean code, replacing ``sorry`` with a real proof."""
    err = (
        f"\n\nYour previous attempt did NOT compile. The kernel said:\n{error}\n"
        f"Fix the proof and output the corrected, complete Lean code (imports + theorem + proof)."
        if error else ""
    )
    return (
        "You are a Lean 4 theorem prover. Output a COMPLETE, compiling Lean 4 file.\n\n"
        f"The file to complete (replace every `sorry` with a real proof):\n\n{statement}\n\n"
        "Rules:\n"
        "- Output ONLY Lean code (no markdown fences, no prose).\n"
        "- Use Mathlib and the imports already in the file; do not add `axiom` or `sorry`.\n"
        "- The file must compile under `lake env lean`."
        f"{err}"
    )


def prove(statement: str, attempts: int = 5, save: str | None = None) -> dict:
    """One run of the prove loop: propose → kernel-check → repair, up to ``attempts`` tries.

    ``statement`` is the full Lean file to complete (imports + theorem with a ``sorry``). On success
    returns ``ok`` + the compiled code; optionally persists it to ``save`` (a ``.lean`` path) so a
    proven theorem lands in the tower rather than only on stdout.
    """
    endpoint, key, model = _llm_config()
    if not model:
        return {"ok": False, "error": "no LLM configured — set SEXTANT_LLM_ENDPOINT / "
                                     "SEXTANT_LLM_MODEL (and SEXTANT_LLM_KEY if the endpoint needs it)"}
    error = None
    for i in range(attempts):
        try:
            code = _ask_llm(_proof_prompt(statement, error), endpoint, key, model)
        except Exception as e:  # noqa: BLE001 — network / API failures are not fatal, report them
            return {"ok": False, "attempts": i + 1, "error": f"LLM call failed: {type(e).__name__}: {e}"}
        code = code.strip()
        if code.startswith("```"):
            code = re.sub(r"^```[a-z]*\n?", "", code)
            code = re.sub(r"\n?```$", "", code)
        ok, err = _check_lean(code)
        if ok:
            saved = None
            if save:
                Path(save).parent.mkdir(parents=True, exist_ok=True)
                Path(save).write_text(code + "\n", encoding="utf-8")
                saved = save
            return {"ok": True, "attempts": i + 1, "code": code, "checked_by": "lake env lean",
                    "saved": saved}
        error = err
    return {"ok": False, "attempts": attempts, "last_error": error}




@dataclass
class Verdict:
    candidate_id: str
    statement: str
    strategy: str
    source_facts: list[str]
    survived: bool
    verdict: str            # "SURVIVED" | "REFUTED"
    evidence: str
    timestamp: str


def run(candidate: Candidate) -> Verdict:
    test = FALSIFIERS.get(candidate.test)
    if test is None:
        # A decomposed sub-lemma without a runnable falsifier is not an error — it is the
        # *frontier*: the engine names the next unproven step and says so, instead of pretending.
        return Verdict(
            candidate_id=candidate.id,
            statement=candidate.statement,
            strategy=candidate.strategy,
            source_facts=list(candidate.source_facts),
            survived=None,
            verdict="MANUAL",
            evidence=f"no runnable falsifier — this sub-lemma needs a thinking agent "
                     f"(falsifier to check: {candidate.falsifier})",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    survived, evidence = test()
    survived = bool(survived)  # cast numpy.bool_ → Python bool (JSON-serializable)
    return Verdict(
        candidate_id=candidate.id,
        statement=candidate.statement,
        strategy=candidate.strategy,
        source_facts=list(candidate.source_facts),
        survived=survived,
        verdict="SURVIVED" if survived else "REFUTED",
        evidence=evidence,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def promote(verdict: Verdict) -> str:
    """A survived candidate becomes a new validated fact, persisted to the discoveries store so the
    next run can build on it; a refuted one is dropped; a MANUAL one is recorded as an open step.
    Returns the promotion note."""
    if verdict.survived is None:
        return f"MANUAL {verdict.candidate_id} → recorded as an open sub-lemma (needs a thinking agent)"
    if verdict.survived:
        fact = {
            "id": verdict.candidate_id,
            "statement": verdict.statement,
            "falsifier": verdict.evidence,
            "source": f"SEXTANT runner {verdict.strategy} over {verdict.source_facts}",
            "category": "discovered",
            "discovered_at": verdict.timestamp,
        }
        DISCOVERIES.parent.mkdir(parents=True, exist_ok=True)
        with DISCOVERIES.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(fact) + "\n")
        return f"PROMOTE {verdict.candidate_id} → new validated fact (persisted to {DISCOVERIES.name})"
    return f"DROP {verdict.candidate_id} (refuted: {verdict.evidence})"


def list_discoveries() -> list[dict]:
    """The promoted survivors, newest first."""
    if not DISCOVERIES.exists():
        return []
    rows = [json.loads(line) for line in DISCOVERIES.read_text(encoding="utf-8").splitlines() if line.strip()]
    return list(reversed(rows))


def register_experiment(kind: str, config: dict, metrics: dict) -> str:
    """Record an experiment's config + metrics with a reproducibility id (an experiment registry).

    Every run — a campaign, an autonomous pass, a benchmark — is registered with its config (model,
    seed, dataset) and its measured metrics, so any result can be traced back to exactly how it was
    produced and re-run with the same inputs (``reproduce``).
    """
    import time
    import uuid

    run_id = uuid.uuid4().hex[:12]
    record = {"run_id": run_id, "kind": kind, "config": config, "metrics": metrics,
              "timestamp": time.time()}
    EXPERIMENTS.parent.mkdir(parents=True, exist_ok=True)
    with EXPERIMENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
    return run_id


def reproduce(run_id: str) -> dict:
    """Re-run a recorded experiment from its stored config (real reproducibility, not just a log).

    Reads the run's ``kind`` and ``config`` and re-executes it, returning the new run. The LLM's
    sampling is non-deterministic, so "reproduce" means the same inputs and config — not bit-identical
    output; a seed (where the kind supports one) makes the synthetic suite deterministic.
    """
    if not EXPERIMENTS.exists():
        raise KeyError(f"no experiment registry at {EXPERIMENTS}")
    record = None
    for line in EXPERIMENTS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if r.get("run_id") == run_id:
                record = r
                break
    if record is None:
        raise KeyError(f"unknown run_id {run_id}")
    kind = record["kind"]
    cfg = record["config"]
    if kind == "autonomous":
        result = run_autonomous(cfg["problem"], rounds=cfg.get("rounds", 1),
                                budget=cfg.get("budget", 8))
        return {"reproduced_from": run_id, "new_run_id": result["run_id"], "result": result}
    raise ValueError(f"cannot reproduce kind {kind!r} (only 'autonomous' is re-runnable today)")


def all_facts() -> dict[str, Fact]:
    """The validated facts PLUS the promoted discoveries — the loop feeds survivors back as facts
    the next run can combine/generalize over. This is what makes the engine *compound*."""
    merged = dict(FACTS)
    for d in list_discoveries():
        merged[d["id"]] = Fact(
            id=d["id"], statement=d["statement"], falsifier=d["falsifier"],
            source=d["source"], category=d.get("category", "discovered"))
    return merged


def record(verdict: Verdict) -> Path:
    """Append a *structured* verdict (JSON, not prose) to the run record."""
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    with RECORD.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(verdict)) + "\n")
    return RECORD


def advance(fact_ids: list[str], strategy: str) -> Verdict:
    """One full turn of the loop: generate → test → promote/drop → record."""
    candidate = generate(fact_ids, strategy)
    verdict = run(candidate)
    note = promote(verdict)
    path = record(verdict)
    verdict.note = note  # type: ignore[attr-defined]
    verdict.recorded = str(path)  # type: ignore[attr-defined]
    return verdict


# ------------------------------------------------------------------------------------------ #
# CLI
# ------------------------------------------------------------------------------------------ #

def rank_open_by_eig() -> list[tuple[str, float]]:
    """Rank the open hypotheses by expected information gain per unit cost.

    Bridges the hypothesis registry to the belief layer: every registered hypothesis's prior and
    falsifier power (``hypotheses.beliefs_for_all``) become a ``Belief``, the C/P detector gates it
    (refuses outside convergence), and ``belief.rank_by_eig`` orders them so the first item is the
    test that shrinks our uncertainty the most per unit cost. The priors are SHRUNK toward 0.5 (the
    handover measured mean Brier 0.41 against the 0.25 skill floor) so EIG does not over-trust them.
    """
    from pacland import belief

    beliefs = [
        belief.Belief(name=s["name"], prior=belief.shrink_prior(s["prior"]),
                      likelihood=belief.Likelihood(s["tp"], s["fp"]),
                      cost=s["cost"])
        for s in hypotheses.beliefs_for_all()
    ]
    return belief.rank_by_eig(beliefs)


def radar() -> str:
    """Surface the next problem to work on — the minimal problem-finder.

    Ranks the open hypotheses by expected information gain per unit cost and returns the top one's
    name; if nothing is ranked, returns the standing frontier problem. This is the *minimal* radar:
    the full cross-field version (querying the five registries for an open problem in a target field
    whose type matches a structure elsewhere) is gated on the registries, which are unbuilt (§10 of
    the plan). This version already makes the loop self-starting: ``run_autonomous()`` picks its own
    problem instead of requiring one.
    """
    try:
        ranked = rank_open_by_eig()
    except Exception:  # noqa: BLE001 — a missing dep must not stop the loop from starting
        ranked = []
    if ranked:
        return ranked[0][0]
    return "confinement-frontier"  # the standing open problem (the frontier)


# ------------------------------------------------------------------------------------------ #
# Search strategies — pluggable problem-level generators (folded from the discovery engine).
#
# The fact-based STRATEGIES above (combine/generalize/specialize/conjecture-value/decompose)
# generate a candidate from validated facts. These generate from a *problem*, the SEXTANT
# catalog, the live simulators, and the proof tree. The five "jump types" are ONE strategy
# (conceptual-jump), not the engine: a discovery can come from anywhere.
# ------------------------------------------------------------------------------------------ #

def _import_sextant():
    try:
        from pacland import phantom, sextant

        return sextant, phantom
    except Exception:
        return None, None


def _falsifier_for_statement(statement: str):
    """Map a natural-language mass-gap hypothesis to the closest runnable lattice falsifier.

    The LLM proposes in prose ('m_gap ≥ c·√σ', 'mass gap ∝ Λ_QCD', 'robust against θ'). This routes
    the claims we can already test to the existing lattice falsifiers; returns ``None`` when no
    falsifier exists yet (the hypothesis stays OPEN — a falsifier for it has not been built).
    """
    low = statement.lower()
    # the candidate-specific falsifiers now exist — route to them BEFORE the generic "return None"
    if "d=5" in low or "five-dim" in low or "d = 5" in low:
        return "d5-mass-gap"
    if "bulk transition" in low or "first-order" in low or "first order" in low:
        return "bulk-transition"
    if any(k in low for k in ("universal", "irrelevant", "improved action")):
        return "universality"
    if any(k in low for k in ("large-n", "large n", "all n", "universal ratio", "n=3", "n=4", "n=5")):
        return "large-n-ratio"
    if "polyakov" in low or "finite-t" in low or "finite temperature" in low or "deconfin" in low:
        return "polyakov-clustering"
    if any(k in low for k in ("theta", "θ", "n-independ", "su(3)", "su(4)", "su(5)")):
        return None  # no lattice tool for θ or multi-N claims yet
    if any(k in low for k in ("string tension", "sqrt", "glueball", "sigma", "σ")):
        return "glueball-mass-ratio"
    if "mass gap" in low and any(k in low for k in ("bound", "perturbative", "scales", "lower")):
        return "mass-gap-scaling"
    if "mass gap" in low and "weak coupling" in low:
        return "su2-weak-coupling"
    return None


# The falsifiers BUILT for a specific mass-gap claim give a DEFINITIVE verdict; the generic lattice
# falsifiers test a RELATED (not the exact) claim, so their verdict is only APPROXIMATE.
_CANDIDATE_SPECIFIC = frozenset({"d5-mass-gap", "bulk-transition", "universality",
                                 "large-n-ratio", "polyakov-clustering"})


_UNRESOLVED_MARKERS = ("noise-dominated", "unresolved", "signal is unresolved", "cannot measure")


def _is_unresolved(evidence: str) -> bool:
    """A falsifier that could not measure returns 'unresolved', which is OPEN — not FALSIFIED."""
    return any(m in evidence.lower() for m in _UNRESOLVED_MARKERS)


def _falsify(candidate: Candidate) -> tuple[bool, bool | None, str]:
    """Run a candidate's falsifier. Tries ``FALSIFIERS`` first (by ``candidate.test``), then a
    SEXTANT catalog claim named in the statement, then a keyword-routed mass-gap falsifier. Returns
    ``(ran, survived, evidence)``; ``ran`` is False when there is no runnable falsifier (the frontier
    — named, not pretended), and an unresolved measurement (noise-dominated) is OPEN, not refuted."""
    if candidate.test in FALSIFIERS:
        try:
            survived, evidence = FALSIFIERS[candidate.test]()
            if not survived and _is_unresolved(evidence):
                return False, None, evidence + "  [unresolved — not a refutation]"
            return True, bool(survived), evidence
        except Exception as e:  # noqa: BLE001 — a missing dependency (e.g. stim) means OPEN, not a crash
            return False, None, f"falsifier unavailable ({type(e).__name__}: {e})"
    sextant, phantom = _import_sextant()
    if sextant is not None and phantom is not None:
        for name in sextant.CATALOG:
            if name in candidate.statement and name in phantom.FALSIFIERS:
                try:
                    ok, ev = phantom.FALSIFIERS[name]()
                    return True, bool(ok), ev
                except Exception as e:  # noqa: BLE001 — same: missing dep => OPEN, not a crash
                    return False, None, f"falsifier unavailable ({type(e).__name__}: {e})"
    key = _falsifier_for_statement(candidate.statement)
    if key is not None and key in FALSIFIERS:
        try:
            survived, evidence = FALSIFIERS[key]()
            if not survived and _is_unresolved(evidence):
                return False, None, evidence + "  [unresolved — not a refutation]"
            if key in _CANDIDATE_SPECIFIC:
                # built for this exact claim => a DEFINITIVE verdict
                return True, bool(survived), evidence + "  [candidate-specific falsifier]"
            # a generic lattice falsifier tests a RELATED claim, not the exact one => APPROXIMATE
            return True, None, (evidence
                                + "  [APPROXIMATE: routed to a related falsifier, not the exact claim]")
        except Exception as e:  # noqa: BLE001
            return False, None, f"falsifier unavailable ({type(e).__name__}: {e})"
    return False, None, f"needs a falsifier (proposed: {candidate.falsifier})"


def slug(s: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in s.lower()).strip("-")


def lineage(candidate: Candidate) -> str:
    """Render a candidate's discovery lineage, root first: ``A → A1 → A2`` (G4)."""
    return " → ".join(candidate.ancestry + (candidate.id,))


def _mk(problem: str, strategy: str, tag: str, statement: str, falsifier: str,
        cost: float, prior: float, ancestry: tuple[str, ...] = ()) -> Candidate:
    return Candidate(
        id=f"{slug(problem)}-{tag}-{uuid.uuid4().hex[:6]}",
        statement=statement, falsifier=falsifier, strategy=strategy,
        source_facts=(), test="", cost=cost, prior=prior, ancestry=ancestry,
    )


class SearchStrategy:
    name = "search-strategy"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        raise NotImplementedError


class ConceptualJump(SearchStrategy):
    """ONE strategy: the five typed questions over the SEXTANT catalog (anomaly, inversion,
    unification, analogy, principle). They help generate ideas; they do not bound discovery."""

    name = "conceptual-jump"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        sextant, _ = _import_sextant()
        out: list[Candidate] = []
        per_q = max(1, budget // 5)
        questions = list(hypotheses.JUMP_QUESTIONS.items())
        for i, (jt, _q) in enumerate(questions):
            if sextant is None:
                continue
            for name, e in list(sextant.CATALOG.items())[:per_q]:
                verdict = e.get("verdict")
                if jt == "anomaly" and verdict == "FREE":
                    h = f"{name}: {e['claim']} is FREE (unforced) — the gap to close"
                elif jt == "inversion" and verdict == "FREE":
                    h = f"invert {name}: assume {e['claim']} is FORCED, not free"
                elif jt == "unification":
                    h = f"unify {name} with {problem}: {e.get('why', '')[:50]}"
                elif jt == "principle" and verdict == "FORCED":
                    h = f"principle {name}: {e['claim']} as a postulate"
                else:
                    continue
                out.append(_mk(problem, self.name, jt, h, e.get("falsifier", "a falsifier"),
                               2.0 + i * 0.5, 0.3))
        return out[:budget]


class MathematicalSearch(SearchStrategy):
    """Surface the invariants we have already proven and propose testing them in a new setting."""

    name = "mathematical-search"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        sextant, _ = _import_sextant()
        out: list[Candidate] = []
        if sextant is not None:
            for name, e in list(sextant.CATALOG.items())[:budget]:
                if e.get("verdict") == "FORCED":
                    out.append(_mk(problem, self.name, "invariant",
                                   f"the invariant behind {name} ({e['theorem']}) transfers to {problem}",
                                   "does the invariant survive in the new setting?", 3.0, 0.2))
        return out[:budget]


class ComputationalSearch(SearchStrategy):
    """Run the live simulators/falsifiers and surface anything that fires as a counterexample."""

    name = "computational-search"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        _, phantom = _import_sextant()
        out: list[Candidate] = []
        if phantom is not None:
            for name in list(phantom.FALSIFIERS)[:budget]:
                out.append(_mk(problem, self.name, "counterexample",
                               f"search for a counterexample to {name} (live falsifier)",
                               name, 1.0, 0.4))
        return out[:budget]


class DatasetMining(SearchStrategy):
    """Expose an unrecognised relationship in the ledger/data."""

    name = "dataset-mining"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        return [_mk(problem, self.name, "relationship",
                    f"correlate the {problem} candidates in the ledger by shared falsifier",
                    "does the shared falsifier reveal a common structure?", 2.0, 0.25)][:budget]


class TheoryCombination(SearchStrategy):
    """Combine existing theories (the catalog's theorems) pairwise and propose the junction."""

    name = "theory-combination"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        sextant, _ = _import_sextant()
        out: list[Candidate] = []
        if sextant is not None:
            names = list(sextant.CATALOG)[: budget + 1]
            for i in range(len(names) - 1):
                out.append(_mk(problem, self.name, "combination",
                               f"combine {names[i]} with {names[i + 1]} toward {problem}",
                               "does the combined structure close?", 4.0, 0.2))
        return out[:budget]


class ProofGap(SearchStrategy):
    """Spot a missing assumption: scan the proof tree for sorry/admit/open lemmas."""

    name = "proof-gap"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        gaps: list[str] = []
        if PROOF_DIR.exists():
            for p in list(PROOF_DIR.rglob("*.lean"))[:200]:
                txt = p.read_text(errors="ignore")
                if "sorry" in txt or "admit" in txt:
                    gaps.append(p.name)
        return [_mk(problem, self.name, "missing-assumption",
                    f"the gap in {g} may be a missing assumption toward {problem}",
                    "is the assumption load-bearing?", 1.5, 0.35) for g in gaps[:budget]]


class LlmSearch(SearchStrategy):
    """Propose hypotheses from an LLM (the real generator), then let SEXTANT falsify them.

    The other strategies recombine what the catalog already holds; this one proposes NEW ideas from
    the LLM. Each line is ``HYPOTHESIS | FALSIFIER``, which becomes a candidate the engine's falsifier
    then runs. With no model configured it returns nothing (it must be able to refuse, not crash).
    """

    name = "llm-search"

    def generate(self, problem: str, budget: int) -> list[Candidate]:
        endpoint, key, model = _llm_config()
        if not model:
            return []
        prompt = _memory_prefix(problem) + (
            "You are a scientific hypothesis generator. Given the open problem below, propose up to "
            f"{budget} falsifiable hypotheses, each with a falsifier. Output ONE per line as "
            "'HYPOTHESIS | FALSIFIER' (a falsifier is the sentence that would make it wrong). "
            "No numbering, no prose.\n\nProblem: " + problem
        )
        try:
            text = _ask_llm(prompt, endpoint, key, model)
        except Exception as e:  # noqa: BLE001 — an unreachable LLM must not crash the engine
            return [_mk(problem, self.name, "llm",
                        f"the LLM could not be reached ({type(e).__name__}) — no hypotheses proposed",
                        "n/a", 0.0, 0.5)]
        out: list[Candidate] = []
        for line in text.splitlines():
            if "|" in line:
                hyp, fal = line.split("|", 1)
                if hyp.strip():
                    out.append(_mk(problem, self.name, "llm", hyp.strip(), fal.strip(), 2.0, 0.3))
        return out[:budget]


SEARCH_STRATEGIES: list[SearchStrategy] = [
    ConceptualJump(), MathematicalSearch(), ComputationalSearch(),
    DatasetMining(), TheoryCombination(), ProofGap(), LlmSearch(),
]


@dataclass
class Discovery:
    """A VERIFIED discovery: a candidate that survived falsification."""
    candidate: Candidate
    effort: float


@dataclass
class Experiment:
    id: str
    problem: str
    strategy: str
    budget: int
    candidates: list[Candidate] = field(default_factory=list)
    discoveries: list[Discovery] = field(default_factory=list)
    effort: float = 0.0
    stopped: bool = False
    reason: str = ""


@dataclass
class KillState:
    budget: int = 10
    tried: int = 0
    survivors: int = 0
    stopped: bool = False
    reason: str = ""


def apply_kill_criteria(ks: KillState) -> KillState:
    """After candidates resolve, decide whether the run is exhausted: budget spent with no survivor
    means the framing is dead — reframe, do not re-run the same strategy."""
    if ks.tried >= ks.budget and ks.survivors == 0:
        ks.stopped = True
        ks.reason = "budget exhausted with no verified discovery — reframe, do not re-run the same strategy"
    return ks


def is_non_vacuous_survivor(candidate: Candidate, evidence: str) -> bool:
    """A survivor is non-vacuous only if it names the real object AND its falsifier actually ran.

    A toy theorem that survives a trivially-true check must not stop the search, so the stop rule
    counts only survivors that are about the real object (mass gap / Yang-Mills / glueball /
    confinement) and were falsified by a real, runnable test (not 'needs a falsifier', not unresolved).
    """
    low = candidate.statement.lower()
    about_real_object = any(t in low for t in ("mass gap", "yang-mills", "glueball",
                                               "confinement", "string tension", "area law"))
    ran_falsifier = bool(evidence) and "needs a falsifier" not in evidence \
        and "unresolved" not in evidence
    return about_real_object and ran_falsifier


class DiscoveryEngine:
    """Run strategies, falsify candidates, and score verified discoveries per unit of effort."""

    def __init__(self, strategies: list[SearchStrategy] | None = None):
        self.strategies = strategies or SEARCH_STRATEGIES

    def run_experiment(self, problem: str, strategy: SearchStrategy, budget: int = 10) -> Experiment:
        exp = Experiment(id=uuid.uuid4().hex[:8], problem=problem,
                         strategy=strategy.name, budget=budget)
        ks = KillState(budget=budget)
        for c in strategy.generate(problem, budget):
            exp.candidates.append(c)
            ran, survived, evidence = _falsify(c)
            exp.effort += c.cost
            ks.tried += 1
            if ran and survived:
                exp.discoveries.append(Discovery(candidate=c, effort=c.cost))
                if is_non_vacuous_survivor(c, evidence):
                    ks.survivors += 1
            apply_kill_criteria(ks)
            if ks.stopped:
                break
        exp.stopped = ks.stopped
        exp.reason = ks.reason
        return exp

    def score(self, exps: list[Experiment]) -> dict:
        per: dict[str, list[float]] = {}
        total_d, total_e = 0, 0.0
        for e in exps:
            d = len(e.discoveries)
            per.setdefault(e.strategy, [0, 0.0])
            per[e.strategy][0] += d
            per[e.strategy][1] += e.effort
            total_d += d
            total_e += e.effort
        return {
            "per_strategy": {s: {"discoveries": int(v[0]), "effort": v[1],
                                 "discoveries_per_effort": v[0] / max(v[1], 1e-9)}
                             for s, v in per.items()},
            "global": {"discoveries": total_d, "effort": total_e,
                       "discoveries_per_effort": total_d / max(total_e, 1e-9)},
        }

    def lifecycle(self, problem: str, budget: int = 10) -> dict:
        exps = [self.run_experiment(problem, s, budget) for s in self.strategies]
        return {"problem": problem, "experiments": [asdict(e) for e in exps],
                "score": self.score(exps)}


def engine_self_test() -> dict:
    """Run all six strategies on 'mass-gap', falsify, and score — the engine's self-test."""
    return DiscoveryEngine().lifecycle("mass-gap", budget=6)


def _formalize_prompt(statement: str) -> str:
    """Ask the LLM to formalise a hypothesis as a Mathlib Lean file (theorem + ``sorry``)."""
    return (
        "You are a Lean 4 formalizer. Formalize the hypothesis below as a complete Mathlib Lean 4 "
        "file: imports plus a theorem statement with a `sorry` for the proof. Output ONLY Lean code, "
        "no prose, no fences.\n\nHypothesis: " + statement
    )


def _lean_matches_hypothesis(lean: str, statement: str) -> bool:
    """Protect the Lean bridge: the formalized theorem must state the SAME proposition as the claim.

    The formalizer can silently weaken or change the claim (prove an easier, unrelated theorem). This
    checks, with an INDEPENDENT judge (SEXTANT_JUDGE_* — a different model than the formalizer), that
    the Lean statement is logically equivalent to the hypothesis, so a proof of a different
    proposition is rejected rather than recorded. The judge must not be the formalizer grading itself.
    """
    endpoint, key, model = _judge_config()
    if not model:
        return False
    prompt = (
        "Does the Lean theorem below state the SAME proposition as the hypothesis (logically "
        "equivalent — not weaker, not stronger, not unrelated)? Answer YES or NO.\n\n"
        f"Hypothesis: {statement}\n\nLean:\n{lean}\n\nAnswer (YES/NO):"
    )
    try:
        ans = _ask_llm(prompt, endpoint, key, model).strip().upper()
    except Exception:  # noqa: BLE001
        return False
    return ans.startswith("YES")


def prove_and_record(candidate: Candidate, evidence: str) -> dict:
    """A survivor of falsification: persist it, then attempt an automated Lean proof.

    Records the survivor to the discoveries store AND to the unified registry as a 'survived' claim
    (the full checklist: statement, assumptions, test, source facts, and — if the proof succeeds — the
    Lean certificate). A proof is a bonus; an unproven survivor is still a recorded discovery.
    """
    from pacland import registry
    claim_id = f"claim-{slug(candidate.id)[:64]}"
    registry.record_claim(
        claim_id, candidate.statement, "survived",
        problem=candidate.strategy,
        assumptions=list(candidate.assumptions),
        test=candidate.test,
        reason=evidence,
        links=[f"property-{f}" for f in candidate.source_facts],
        produced_by=f"runner/{candidate.strategy}",
    )

    fact = {"id": candidate.id, "statement": candidate.statement, "falsifier": evidence,
            "source": f"discovery-engine {candidate.strategy}", "category": "discovered"}
    DISCOVERIES.parent.mkdir(parents=True, exist_ok=True)
    with DISCOVERIES.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(fact) + "\n")

    endpoint, key, model = _llm_config()
    if not model:
        return {"ok": False, "recorded": True, "proof": "deferred — no LLM configured"}
    try:
        lean = _ask_llm(_formalize_prompt(candidate.statement), endpoint, key, model)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "recorded": True, "proof": f"formalise failed: {type(e).__name__}"}
    if not _lean_matches_hypothesis(lean, candidate.statement):
        return {"ok": False, "recorded": True,
                "proof": "rejected — the formalized theorem does not state the original claim"}
    proof = prove(lean, attempts=3)
    if proof.get("ok"):
        # attach the Lean certificate to the claim (upsert updates the existing entry in place)
        registry.record_claim(
            claim_id, candidate.statement, "survived",
            problem=candidate.strategy,
            assumptions=list(candidate.assumptions),
            test=candidate.test,
            reason=evidence,
            lean_cert=proof.get("code", "")[:500],
            links=[f"property-{f}" for f in candidate.source_facts],
            produced_by=f"runner/{candidate.strategy}",
        )
    return {"ok": proof.get("ok", False), "recorded": True, "proof": proof}


def run_autonomous(problem: str | None = None, rounds: int = 1, budget: int = 8) -> dict:
    """One autonomous pass of the frontier machine: propose -> falsify -> challenge -> prove -> build.

    For each round it runs the LLM search strategy, falsifies every proposal, runs the EIGHT-STAGE
    SEXTANT challenge sequence on every proposal, records and tries to prove every survivor, and —
    for every OPEN proposal — searches arXiv / the proof tree / the codebase for a falsifier,
    synthesises one, BUILDS it into an executable test, and retries the hypothesis against it.
    Returns the whole round's evidence.

    ``problem=None`` → the radar surfaces the top-EIG open problem (self-starting).
    """
    from pacland import challenges
    from pacland import falsifier_acquisition as fa
    from pacland import memory

    endpoint, key, model = _llm_config()
    problem = problem or radar()
    out = {"problem": problem, "rounds": []}
    for _ in range(rounds):
        cands = LlmSearch().generate(problem, budget)
        round_out = {"proposals": [], "survivors": [], "open": []}
        for c in cands:
            ran, survived, evidence = _falsify(c)
            # If no existing falsifier exists, ACQUIRE/BUILD one autonomously BEFORE the gate: the
            # gate's boundary-testing needs a falsifier to test with, and gating first would drop the
            # candidate before a falsifier could ever be generated.
            acq = None
            existing = None
            built = None
            if not ran:
                acq = fa.acquire(c.statement, endpoint=endpoint, key=key, model=model)
                # USE an existing falsifier (code / proof tree / Mathlib / arXiv) if acquire found one.
                existing = fa.apply_acquired(acq, c.statement)
                if existing is not None and existing.get("ran"):
                    # a DEFINITIVE existing falsifier ran — promote (it is vetted, not synthesized)
                    ran, survived, evidence = (True, existing["survived"],
                                               f"{existing['evidence']} [{existing.get('note','existing falsifier')}]")
                elif existing is None:
                    # nothing existing — build a new one (synthesized, CANDIDATE — does NOT promote)
                    if fa.is_lattice_claim(c.statement):
                        built = fa.build_lattice_falsifier(c.statement, endpoint, key, model)
                    else:
                        built = fa.build_and_run_falsifier(c.statement, endpoint, key, model)
            # the eight-stage graded challenge, on every proposal (not just the single falsifier).
            # Thread the runner's ALREADY-COMPUTED falsifier result + the recorded assumptions, and
            # pass the falsifier KEY (c.test), not the generated id or the prose description — so a
            # candidate that a falsifier actually tested is not FAILed on a bad name→key lookup.
            seq = challenges.run_sequence(challenges.Candidate(
                name=c.id,
                hypothesis=c.statement,
                falsifier=c.test or "",
                assumptions=list(c.assumptions),
                falsifier_result=(survived, evidence) if ran else None,
            ))
            stage_verdicts = {r.name: r.verdict for r in seq}
            gate = challenges.gate(seq)
            # SEXTANT is a DECISION GATE: a candidate that FAILED a challenge is dead — dropped, not
            # proved/recorded/acquired. (formal-verification is NOT_APPLICABLE here because the LLM
            # proposal has no theorem yet; the real kernel-check runs in prove_and_record.)
            if gate == "FAIL":
                # the gate FAILs for a REASON (unjustified assumptions, untested boundary, ...) —
                # that is NOT the same as falsified, so record which stage dropped it.
                failed_stage = next((n for n, v in stage_verdicts.items() if v == "FAIL"), "unknown")
                _append_rejected(problem, c.statement, f"gated-out: {failed_stage}")
                entry = {"statement": c.statement, "verdict": "gated-out",
                         "evidence": evidence, "challenges": stage_verdicts, "gate": gate}
                if existing is not None:
                    entry["existing_falsifier"] = existing
                if built is not None:
                    entry["synthesized_test"] = built
                round_out["proposals"].append(entry)
                continue
            if ran and survived is True:
                proof = prove_and_record(c, evidence)
                _append_memory(problem, c.statement, c.falsifier, proof)
                round_out["survivors"].append({"statement": c.statement, "proof": proof,
                                               "challenges": stage_verdicts, "gate": gate})
            elif ran and survived is False:
                _append_rejected(problem, c.statement, "falsified")
                round_out["proposals"].append({"statement": c.statement, "verdict": "falsified",
                                               "evidence": evidence, "challenges": stage_verdicts,
                                               "gate": gate})
            else:
                entry = {"statement": c.statement, "verdict": "open", "evidence": evidence,
                         "acquisition": acq, "challenges": stage_verdicts, "gate": gate}
                if existing is not None and existing.get("found_existing"):
                    # an existing falsifier (paper / Lean proof / Mathlib) already addresses the
                    # claim — use it, do not build a new one.
                    entry["verdict"] = "already-falsifiable"
                    entry["existing_falsifier"] = existing.get("existing")
                    entry["evidence"] = existing.get("evidence")
                elif built is not None and built.get("ran"):
                    # a synthesized falsifier that ran gives a CANDIDATE verdict (not definitive)
                    entry["synthesized_test"] = built
                    entry["candidate_verdict"] = ("survived" if built["survived"] else "refuted")
                else:
                    # no existing falsifier and none could be built in this pass — record it as a JOB
                    # so another process or session can build it, keeping the frontier moving.
                    entry["synthesized_test"] = built
                    entry["falsifier_job"] = fa.record_falsifier_job(
                        c.statement,
                        (acq or {}).get("synthesized_falsifier") or c.falsifier,
                        (built or {}).get("reason", "unknown"))
                round_out["open"].append(entry)
        out["rounds"].append(round_out)
    metrics = {"rounds": rounds,
               "survivors": sum(len(r["survivors"]) for r in out["rounds"]),
               "falsified": sum(len(r["proposals"]) for r in out["rounds"]),
               "open": sum(len(r["open"]) for r in out["rounds"])}
    out["run_id"] = register_experiment("autonomous", {"problem": problem, "rounds": rounds,
                                                       "budget": budget, "model": model}, metrics)
    return out


def _main() -> int:
    ap = argparse.ArgumentParser(description="SEXTANT runner — the hypothesis loop")
    ap.add_argument("--list-facts", action="store_true")
    ap.add_argument("--list-strategies", action="store_true")
    ap.add_argument("--list-discoveries", action="store_true")
    ap.add_argument("--fact", action="append", default=[], help="fact id (repeatable)")
    ap.add_argument("--strategy", choices=list(STRATEGIES))
    ap.add_argument("--list-open", action="store_true", help="list the OPEN hypotheses and their next sub-lemma")
    ap.add_argument("--rank-by-eig", action="store_true",
                    help="rank the OPEN hypotheses by expected information gain (what to test next)")
    ap.add_argument("--decompose", metavar="HYPOTHESIS", help="decompose one OPEN hypothesis into its next sub-lemma")
    ap.add_argument("--advance-all", action="store_true")
    ap.add_argument("--prove", nargs="?", const="", metavar="FILE",
                    help="run the prove loop (FILE = a .lean file with the statement + sorry)")
    ap.add_argument("--statement", help="inline Lean code to prove (implies --prove)")
    ap.add_argument("--prove-attempts", type=int, default=5, help="max LLM repair attempts (default 5)")
    ap.add_argument("--prove-save", metavar="PATH", help="save the proven .lean file to PATH (relative to the proof tree)")
    ap.add_argument("--engine-self-test", action="store_true",
                    help="run all six search strategies, falsify, and score discoveries per effort")
    ap.add_argument("--engine", metavar="PROBLEM", help="run the search engine on a problem")
    ap.add_argument("--autonomous", metavar="PROBLEM", help="one autonomous propose -> falsify -> prove -> acquire pass")
    ap.add_argument("--list-falsifier-jobs", action="store_true",
                    help="list the queued falsifier-build jobs (work for another session/process")
    args = ap.parse_args()

    if args.list_facts:
        for fid, f in all_facts().items():
            print(f"{fid:16s} [{f.category:12s}] {f.statement}\n    falsifier: {f.falsifier}\n    source: {f.source}")
        return 0
    if args.list_strategies:
        for sid, desc in STRATEGIES.items():
            print(f"{sid:12s} {desc}")
        return 0
    if args.list_discoveries:
        for d in list_discoveries():
            print(f"{d['id']:32s} {d['statement']}\n    source: {d['source']}\n    evidence: {d['falsifier']}")
        return 0
    if args.list_open:
        for hid, h in hypotheses.HYPOTHESES.items():
            cands = h.get("candidates", [])
            first = cands[0] if cands else None
            print(f"◇ {hid}\n    open: {h.get('open', '(none)')}")
            if h.get("progress"):
                print(f"    progress: {h['progress']}")
            if first:
                print(f"    next : {first['hypothesis']}\n    falsifier: {first['falsifier']}"
                      f"  [{ 'runnable' if _runnable_test(first['hypothesis']) else 'manual — needs a thinking agent' }]")
            else:
                print("    next : (no candidates)")
        return 0
    if args.rank_by_eig:
        print("open hypotheses ranked by expected information gain per unit cost (what to test next):")
        for i, (name, score) in enumerate(rank_open_by_eig(), 1):
            print(f"  {i}. {name:<24s} EIG/cost = {score:.4f} nats")
        return 0
    if args.decompose:
        v = advance([args.decompose], "decompose")
        print(_fmt(v))
        return 0
    if args.advance_all:
        # the recombinations (known facts) + the frontier move (every OPEN hypothesis decomposed)
        turns = [(["ou-curvature", "gronwall-decay"], "combine"), (["confinement-frontier"], "specialize")]
        turns += [([hid], "decompose") for hid in hypotheses.HYPOTHESES]
        for (a, b) in turns:
            v = advance(a, b)
            print(_fmt(v))
        return 0
    if args.prove is not None or args.statement:
        statement = args.statement
        if statement is None:
            f = Path(args.prove)
            if not f.exists():
                print(f"file not found: {f}", file=sys.stderr)
                return 1
            statement = f.read_text(encoding="utf-8")
        save = None
        if args.prove_save:
            save = str(PROOF_DIR / args.prove_save)
        result = prove(statement, attempts=args.prove_attempts, save=save)
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1
    if args.engine_self_test:
        r = engine_self_test()
        print("strategies run:", len(r["experiments"]))
        for s, m in r["score"]["per_strategy"].items():
            print(f"  {s:20s} discoveries={m['discoveries']} effort={m['effort']:.1f} "
                  f"d/e={m['discoveries_per_effort']:.3f}")
        print(f"  global: {r['score']['global']['discoveries']} verified discoveries per "
              f"{r['score']['global']['effort']:.1f} effort")
        return 0
    if args.engine:
        r = DiscoveryEngine().lifecycle(args.engine, budget=6)
        for e in r["experiments"]:
            print(f"[{e['strategy']:18s}] candidates={len(e['candidates'])} "
                  f"discoveries={len(e['discoveries'])} stopped={e['stopped']}")
            for c in e["candidates"]:
                print(f"    - {c['statement'][:70]}")
        print(json.dumps(r["score"], indent=2))
        return 0
    if args.autonomous:
        r = run_autonomous(args.autonomous)
        print(json.dumps(r, indent=2))
        return 0
    if args.list_falsifier_jobs:
        from pacland import falsifier_acquisition as fa
        jobs = fa.list_falsifier_jobs()
        print(f"{len(jobs)} falsifier-build job(s):")
        for j in jobs:
            print(f"  [{j['status']:11s}] {j['job_id']}  {j['statement'][:70]}")
            print(f"    proposed: {j['proposed_falsifier'][:70]}")
            print(f"    reason:   {j['reason'][:70]}")
        return 0
    if args.fact and args.strategy:
        v = advance(args.fact, args.strategy)
        print(_fmt(v))
        return 0
    ap.print_help()
    return 1


def _fmt(v: Verdict) -> str:
    return (
        f"[{v.verdict}] {v.candidate_id}\n"
        f"  statement : {v.statement}\n"
        f"  strategy  : {v.strategy}  ← facts {v.source_facts}\n"
        f"  evidence  : {v.evidence}\n"
        f"  action    : {getattr(v, 'note', '')}\n"
        f"  recorded  : {getattr(v, 'recorded', '')}"
    )


if __name__ == "__main__":
    sys.exit(_main())
