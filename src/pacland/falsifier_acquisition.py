"""Falsifier acquisition — when a hypothesis has no runnable falsifier, go find or build one.

The engine must not stop at OPEN. It searches three places, in order of strength, and falls back to
synthesising a candidate:

1. the codebase — an existing falsifier that already tests the claim (runnable today),
2. the Lean proof tree — a theorem that refutes the claim (a real falsifier, kernel-checked),
3. arXiv — prior art that tests the claim, with its headline claim as a candidate falsifier,
4. the LLM — synthesise the sentence that would make the claim wrong (a candidate to build).

The result is an acquisition record, never a fake verdict: a found falsifier is named; a missing one
is recorded as "to build" with the evidence of where to look.
"""
from __future__ import annotations

import re
from pathlib import Path

from pacland import literature

_STOP = {"that", "with", "this", "from", "these", "their", "they", "have", "than", "will",
         "would", "been", "were", "such", "more", "also", "only", "very", "into", "over",
         "under", "where", "when", "which", "while", "there", "here", "about", "between",
         "through", "using", "does", "mass", "gap"}


def key_terms(statement: str, n: int = 6) -> list[str]:
    """The statement's key content terms (>= 4 chars, not stopwords) for matching."""
    words = re.findall(r"[a-z]{4,}", statement.lower())
    return [w for w in words if w not in _STOP][:n]


def search_arxiv(statement: str, max_results: int = 5) -> list[dict]:
    """Prior art: arXiv papers that test the claim, with their headline claim as a candidate falsifier."""
    try:
        records = literature.search_arxiv(statement, max_results)
    except Exception as e:  # noqa: BLE001 — arXiv unreachable is not fatal, it is reported
        return [{"error": f"arXiv unreachable: {type(e).__name__}"}]
    out = []
    for r in records:
        if r.get("claim"):
            out.append({"arxiv_id": r.get("arxiv_id", ""), "title": r.get("title", ""),
                        "claim": r["claim"]})
    return out


def search_proof_tree(statement: str, proof_dir: str | Path = "pacland-proof",
                      max_hits: int = 10) -> list[dict]:
    """The Lean proof tree: theorems whose statement shares the claim's key terms.

    A theorem that shares >= 2 key terms with the claim is a candidate refutation (or support) worth
    reading. This surfaces it; it does not assert it refutes the claim — the kernel decides.
    """
    terms = key_terms(statement)
    root = Path(proof_dir)
    if not root.exists() or not terms:
        return []
    hits: list[dict] = []
    for p in list(root.rglob("*.lean"))[:500]:
        try:
            txt = p.read_text(errors="ignore").lower()
        except OSError:
            continue
        if sum(1 for t in terms if t in txt) < 2:
            continue
        for m in re.finditer(r"theorem\s+([\w']+)", txt):
            hits.append({"file": str(p), "theorem": m.group(1)})
        if len(hits) >= max_hits:
            break
    return hits[:max_hits]


def search_code(statement: str) -> list[dict]:
    """An existing falsifier in the codebase that matches the claim (runnable today)."""
    from pacland import runner

    fn = runner._falsifier_for_statement(statement)
    return [{"falsifier": fn.__name__}] if fn is not None else []


def synthesize(statement: str, endpoint: str, key: str, model: str) -> str | None:
    """Synthesise the sentence that would make the claim wrong (a candidate falsifier to build)."""
    if not model:
        return None
    from pacland import runner

    prompt = (
        "You are a physics falsifier designer. Given the claim below, write the SINGLE most decisive "
        "measurement or theorem that would REFUTE it (the sentence that, if true, makes the claim "
        "wrong). One sentence only.\n\nClaim: " + statement
    )
    try:
        return runner._ask_llm(prompt, endpoint, key, model).strip()
    except Exception:  # noqa: BLE001
        return None


def acquire(statement: str, proof_dir: str | Path = "pacland-proof",
            endpoint: str = "", key: str = "", model: str = "") -> dict:
    """Find or note a falsifier for an OPEN hypothesis. Returns the acquisition record."""
    code = search_code(statement)
    proof = search_proof_tree(statement, proof_dir)
    arxiv = search_arxiv(statement)
    synthesized = None
    if not (code or proof):
        synthesized = synthesize(statement, endpoint, key, model)
    found = bool(code or proof)
    return {
        "statement": statement,
        "found": found,
        "code": code,
        "proof_tree": proof,
        "arxiv": arxiv,
        "synthesized_falsifier": synthesized,
        "verdict": ("falsifier found" if found else
                    ("candidate synthesized — build it" if synthesized else "no falsifier found")),
    }


def validate_falsifier(code: str, statement: str) -> list[str]:
    """A synthesized falsifier must ACTUALLY test the candidate, or it is rejected as vacuous.

    Three independent checks: it must branch (be able to reject — a constant ``return True`` is
    vacuous), it must reference the claim's key terms (test THAT claim, not something unrelated), and
    it must not be a bare constant return. Returns a list of violations (empty = acceptable).
    """
    low = code.lower()
    issues = []
    if "return true" in low and not any(k in low for k in ("if", "else", "elif", ">", "<", "==")):
        issues.append("returns True unconditionally (no branch)")
    if not any(k in low for k in ("if", "else", "elif", ">", "<", "==", "assert", "abs", "diff",
                                  "min", "max", "where", "all", "any", "compare", "tolerance")):
        issues.append("no comparison or branch — it cannot reject anything")
    terms = key_terms(statement, n=3)
    if terms and not any(t in low for t in terms):
        issues.append(f"does not reference the claim's key terms {terms}")
    return issues


def build_and_run_falsifier(statement: str, endpoint: str, key: str, model: str) -> dict:
    """Turn a synthesized falsifier into an EXECUTABLE test, validate it, run it, and retry.

    This closes the acquisition loop: acquire -> build (the LLM writes a Python ``falsifier()``
    returning ``(bool, str)``) -> VALIDATE it actually tests the candidate -> run it in a subprocess ->
    get a verdict. The verdict is honest — it is from a SYNTHESIZED falsifier (LLM-written, not a
    vetted lattice/Lean computation), so it is a candidate verdict, not a definitive one.
    """
    from pacland import runner

    if not model:
        return {"ran": False, "reason": "no LLM to write the falsifier"}
    prompt = (
        "Write a Python function `falsifier()` that tests the hypothesis below and returns "
        "(bool, str): True if the hypothesis SURVIVES (the test could not refute it), False if it is "
        "REFUTED, plus a one-line evidence string. Use only numpy / math / sympy — no files, no "
        "network, no prints except the return. Output ONLY the code.\n\nHypothesis: " + statement
    )
    try:
        code = runner._ask_llm(prompt, endpoint, key, model)
    except Exception as e:  # noqa: BLE001
        return {"ran": False, "reason": f"LLM failed: {type(e).__name__}"}
    code = code.strip().strip("`").replace("```python", "").replace("```", "").strip()

    issues = validate_falsifier(code, statement)
    if issues:
        return {"ran": False, "reason": "vacuous falsifier rejected: " + "; ".join(issues)}

    import json
    import subprocess
    import tempfile
    from pathlib import Path

    harness = ("import json\nimport numpy as np\nimport math\nimport sympy\n"
               + code + "\n_result = falsifier()\nprint(json.dumps(list(_result)))\n")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(harness)
        path = f.name
    try:
        r = subprocess.run(["python3", path], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return {"ran": False, "reason": "synthesized falsifier timed out"}
    finally:
        Path(path).unlink(missing_ok=True)
    if r.returncode != 0:
        return {"ran": False, "reason": f"falsifier code failed: {(r.stderr or r.stdout)[:200]}"}
    try:
        survived, evidence = json.loads(r.stdout.strip())
    except Exception:  # noqa: BLE001
        return {"ran": False, "reason": f"falsifier returned unparseable output: {r.stdout[:120]}"}
    return {"ran": True, "survived": bool(survived), "evidence": str(evidence), "code": code,
            "note": "synthesized falsifier (LLM-written, not a vetted lattice/Lean computation)"}
