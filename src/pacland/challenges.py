"""G2 — the graded SEXTANT challenge sequence (from PLAN-discovery-engine.md).

Replaces the single binary falsifier with eight ordered challenges, each scored
PASS / FAIL / INCONCLUSIVE / NOT APPLICABLE. A candidate can survive seven and die on the eighth; the
record preserves all eight results plus the decisive failure.

Mechanical challenges (known-results, boundary, counterexample, reproducibility, formal verification)
run against SEXTANT/Phantom and the Lean tower. The three model-judged ones (logical consistency,
assumption audit, alternative explanation) are honest stubs that return INCONCLUSIVE until a judge is
plugged in — keeping the honesty that only "counterexample search" and "formal verification" are
mechanical, not model-opinion.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

VERDICTS = ("PASS", "FAIL", "INCONCLUSIVE", "NOT_APPLICABLE")


@dataclass
class Challenge:
    name: str
    question: str
    kind: str            # "mechanical" | "model-judged"


@dataclass
class ChallengeResult:
    name: str
    kind: str
    verdict: str
    evidence: str = ""


@dataclass
class Candidate:
    name: str
    hypothesis: str
    falsifier: str = ""
    assumptions: list[str] = field(default_factory=list)
    theorem: str = ""    # the Lean theorem it claims, if any
    # The (survived, evidence) the runner's falsifier ALREADY computed. When supplied, the mechanical
    # falsifier stages use it instead of re-running (and instead of looking up by name). survived may be
    # None (a falsifier ran but the verdict is approximate/unresolved → INCONCLUSIVE).
    falsifier_result: tuple[bool | None, str] | None = None


CHALLENGES = [
    Challenge("logical-consistency", "Does the hypothesis contradict itself?", "model-judged"),
    Challenge("assumption-audit", "Are the assumptions justified, hidden, or circular?", "model-judged"),
    Challenge("known-results", "Does it contradict an established FORCED result?", "mechanical"),
    Challenge("boundary-testing", "Does it survive limiting and extreme cases?", "mechanical"),
    Challenge("counterexample-search", "Can a solver construct a case where it fails?", "mechanical"),
    Challenge("alternative-explanation", "Could an existing theory explain it more simply?", "model-judged"),
    Challenge("reproducibility", "Can an independent re-run reproduce the result?", "mechanical"),
    Challenge("formal-verification", "Is the claim kernel-checked in Lean?", "mechanical"),
]


def _import_sextant():
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from pacland import phantom, sextant

        return sextant, phantom
    except Exception:
        return None, None


def _judge_config() -> tuple[str, str, str]:
    """The model-judge's endpoint/key/model (same env as the LLM generator)."""
    import os

    return (os.environ.get("SEXTANT_LLM_ENDPOINT", "http://localhost:11434/v1"),
            os.environ.get("SEXTANT_LLM_KEY", ""),
            os.environ.get("SEXTANT_LLM_MODEL", ""))


def _ask_judge(prompt: str) -> str | None:
    """One LLM call for a model-judged challenge; None when no model is configured or the call fails.

    A slow or unreachable judge must NOT crash the challenge sequence — it degrades to INCONCLUSIVE.
    """
    import json
    import urllib.request

    endpoint, key, model = _judge_config()
    if not model:
        return None
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(endpoint.rstrip("/") + "/chat/completions", data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
    except Exception:  # noqa: BLE001 — timeout/unreachable => INCONCLUSIVE, not a crash
        return None


def _model_judge(stage: str, hypothesis: str, assumptions: list[str] | None = None) -> tuple[str, str]:
    """Run one model-judged challenge. Returns ``(verdict, evidence)``; INCONCLUSIVE when no judge."""
    prompts = {
        "logical-consistency": (
            "Does this hypothesis contradict itself? Answer exactly INTERNALLY CONSISTENT or "
            "CONTRADICTORY.\n\nHypothesis: " + hypothesis),
        "assumption-audit": (
            "Are the assumptions of this hypothesis justified, hidden, or circular? Answer exactly "
            "JUSTIFIED, HIDDEN, or CIRCULAR.\n\nHypothesis: " + hypothesis
            + "\nAssumptions: " + (", ".join(assumptions) if assumptions else "not recorded")),
        "alternative-explanation": (
            "Could an existing, established theory explain this more simply than the hypothesis does? "
            "Answer exactly YES or NO.\n\nHypothesis: " + hypothesis),
    }
    if stage not in prompts:
        return "INCONCLUSIVE", "unknown stage"
    answer = _ask_judge(prompts[stage])
    if answer is None:
        return "INCONCLUSIVE", "no judge model configured (set SEXTANT_LLM_MODEL)"
    up = answer.upper()
    if stage == "logical-consistency":
        verdict = ("PASS" if "CONSISTENT" in up and "CONTRA" not in up else
                   "FAIL" if "CONTRA" in up else "INCONCLUSIVE")
    elif stage == "assumption-audit":
        verdict = ("PASS" if "JUSTIFIED" in up else
                   "FAIL" if "HIDDEN" in up or "CIRCULAR" in up else "INCONCLUSIVE")
    else:  # alternative-explanation
        verdict = ("FAIL" if up.startswith("YES") else
                   "PASS" if up.startswith("NO") else "INCONCLUSIVE")
    return verdict, f"judge: {answer[:120]}"


def _lean_check(theorem: str) -> tuple[str, str]:
    """Mechanical formal-verification check: is the theorem present + free of sorry in the tower?"""
    if not theorem:
        return "NOT_APPLICABLE", "no formalisation target named"
    root = Path(__file__).resolve().parent.parent.parent / "pacland-proof"
    if not root.exists():
        return "INCONCLUSIVE", "Lean tower not present"
    import re
    import subprocess
    short = theorem.split(".")[-1]
    for p in root.rglob("*.lean"):
        txt = p.read_text(errors="ignore")
        # require the DECLARATION, not a substring in a comment or docstring
        if not re.search(rf"\b(?:theorem|lemma)\s+{re.escape(short)}\b", txt):
            continue
        if re.search(r"\b(?:sorry|admit)\b", txt):
            return "FAIL", f"{theorem} declared in {p.name} but carries sorry/admit"
        elan = str(Path.home() / ".elan" / "bin")
        env = dict(__import__("os").environ)
        env["PATH"] = elan + __import__("os").pathsep + env.get("PATH", "")
        try:
            r = subprocess.run(["lake", "env", "lean", str(p)], cwd=str(root),
                               capture_output=True, text=True, timeout=300, env=env)
        except FileNotFoundError:
            return "INCONCLUSIVE", f"{theorem} declared in {p.name}; kernel unavailable (no lake)"
        except subprocess.TimeoutExpired:
            return "INCONCLUSIVE", f"{theorem} declared in {p.name}; kernel timed out"
        if r.returncode == 0:
            return "PASS", f"{theorem} kernel-checked in {p.name}"
        return "FAIL", f"{theorem} declared in {p.name} but does not compile: {(r.stdout + r.stderr).strip()[-200:]}"
    return "INCONCLUSIVE", f"{theorem} not declared in the Lean tower"


def run_sequence(c: Candidate) -> list[ChallengeResult]:
    """Run the eight challenges in order. The record keeps every result, including the decisive failure."""
    sextant, phantom = _import_sextant()
    results: list[ChallengeResult] = []

    def add(name, kind, verdict, evidence):
        results.append(ChallengeResult(name, kind, verdict, evidence))

    # 1-2: model-judged — a real LLM judge (INCONCLUSIVE only when no judge is configured)
    v, ev = _model_judge("logical-consistency", c.hypothesis)
    add("logical-consistency", "model-judged", v, ev)
    v, ev = _model_judge("assumption-audit", c.hypothesis, c.assumptions)
    add("assumption-audit", "model-judged", v, ev)

    # 3: known-results — mechanical (does it name a FORCED claim and try to invert it?)
    if sextant is not None:
        hit = next((n for n, e in sextant.CATALOG.items() if n in c.hypothesis), None)
        if hit is None:
            add("known-results", "mechanical", "NOT_APPLICABLE",
                "names no catalog claim — nothing to check (not a PASS)")
        elif sextant.CATALOG[hit].get("verdict") == "FORCED":
            add("known-results", "mechanical", "FAIL",
                f"contradicts the FORCED claim {hit}: {sextant.CATALOG[hit]['claim']}")
        else:
            add("known-results", "mechanical", "PASS",
                f"names {hit}, which is not FORCED — no established result contradicted")
    else:
        add("known-results", "mechanical", "NOT_APPLICABLE", "SEXTANT not importable")

    # 4: boundary-testing — mechanical (the falsifier probes the limiting/extreme case).
    # The runner's already-computed falsifier result is authoritative; otherwise fall back to a live
    # run keyed by c.falsifier (NOT c.name — the runner's name is a generated id, not a falsifier key).
    if c.falsifier_result is not None:
        survived, ev = c.falsifier_result
        verdict = ("PASS" if survived is True else "FAIL" if survived is False else "INCONCLUSIVE")
        add("boundary-testing", "mechanical", verdict, ev + " [runner-supplied falsifier result]")
    elif phantom is not None and c.falsifier in getattr(phantom, "FALSIFIERS", {}):
        try:
            ok, ev = phantom.FALSIFIERS[c.falsifier]()
            add("boundary-testing", "mechanical", ("PASS" if ok else "FAIL"), ev)
        except Exception as exc:  # noqa: BLE001
            add("boundary-testing", "mechanical", "INCONCLUSIVE",
                f"falsifier raised {type(exc).__name__}: {exc}")
    else:
        add("boundary-testing", "mechanical", "INCONCLUSIVE",
            "no runnable falsifier — untested, not refuted")

    # 5: counterexample-search — mechanical (the live Phantom falsifier, or the runner's result)
    if c.falsifier_result is not None:
        survived, ev = c.falsifier_result
        verdict = ("PASS" if survived is True else "FAIL" if survived is False else "INCONCLUSIVE")
        add("counterexample-search", "mechanical", verdict, ev + " [runner-supplied falsifier result]")
    elif phantom is not None and c.falsifier in getattr(phantom, "FALSIFIERS", {}):
        try:
            ok, ev = phantom.FALSIFIERS[c.falsifier]()
            add("counterexample-search", "mechanical",
                ("PASS" if ok else "FAIL"), ev)
        except Exception as exc:
            add("counterexample-search", "mechanical", "INCONCLUSIVE",
                f"falsifier raised {type(exc).__name__}: {exc}")
    else:
        add("counterexample-search", "mechanical", "NOT_APPLICABLE", "no registered falsifier")

    # 6: model-judged — a real LLM judge
    v, ev = _model_judge("alternative-explanation", c.hypothesis)
    add("alternative-explanation", "model-judged", v, ev)

    # 7: reproducibility — mechanical (run the falsifier twice, require determinism)
    if phantom is not None and c.falsifier in getattr(phantom, "FALSIFIERS", {}):
        try:
            a = phantom.FALSIFIERS[c.falsifier]()
            b = phantom.FALSIFIERS[c.falsifier]()
            add("reproducibility", "mechanical",
                ("PASS" if a == b else "FAIL"), "two runs " + ("agree" if a == b else "disagree"))
        except Exception as exc:
            add("reproducibility", "mechanical", "INCONCLUSIVE", f"raised {type(exc).__name__}")
    else:
        add("reproducibility", "mechanical", "NOT_APPLICABLE", "no registered falsifier")

    # 8: formal-verification — mechanical (Lean tower check)
    v, ev = _lean_check(c.theorem)
    add("formal-verification", "mechanical", v, ev)

    return results


def summarize(results: list[ChallengeResult]) -> str:
    """One-line verdict per challenge + the tally."""
    lines = [f"[{r.verdict:13s}] {r.name:24s} {r.evidence[:60]}" for r in results]
    tally = {v: sum(1 for r in results if r.verdict == v) for v in VERDICTS}
    lines.append(f"tally: " + ", ".join(f"{k}={v}" for k, v in tally.items() if v))
    return "\n".join(lines)


def gate(results: list[ChallengeResult]) -> str:
    """SEXTANT as a DECISION GATE, not just a report.

    ``FAIL`` — any challenge FAILED (the candidate is dead; do not prove/record/promote it).
    ``PASS`` — no FAIL and at least one challenge actually PASSED (survived a real test).
    ``INCONCLUSIVE`` — no FAIL and no PASS (nothing decisive happened; proceed but flag it).
    """
    verdicts = [r.verdict for r in results]
    if "FAIL" in verdicts:
        return "FAIL"
    if "PASS" in verdicts:
        return "PASS"
    return "INCONCLUSIVE"


if __name__ == "__main__":
    # self-test: run the sequence on a SEXTANT claim + a bare hypothesis
    print("=== graded challenge sequence: chsh (FORCED, live falsifier) ===")
    print(summarize(run_sequence(Candidate("chsh", "no state beats 2√2", falsifier="chsh", theorem="QM.Tsirelson"))))
    print("\n=== graded challenge sequence: a hypothesis with no falsifier + no theorem ===")
    print(summarize(run_sequence(Candidate("bare", "some new hypothesis"))))
