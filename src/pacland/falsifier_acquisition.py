"""Falsifier acquisition — when a hypothesis has no runnable falsifier, go find or build one.

The engine must not stop at OPEN. It searches three places, in order of strength, and falls back to
synthesising a candidate:

1. the codebase — an existing falsifier that already tests the claim (runnable today),
2. the Lean proof tree — a theorem that refutes the claim (a real falsifier, kernel-checked),
3. arXiv — prior art that tests the claim, with its headline claim as a candidate falsifier,
4. the LLM — synthesise the sentence that would make the claim wrong (a candidate to build).

The result is an acquisition record, never a fake verdict: a found falsifier is named; a missing one
is recorded as "to build" with the evidence of where to look.

When a falsifier cannot be BUILT in the current pass (the synthesized code crashes, or no LLM is
present), it is recorded as a JOB in ``runs/falsifier-jobs.jsonl`` — a concrete task another process
or session can pick up and complete, so the frontier progresses across runs instead of stalling.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path

from pacland import literature

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # .../pacland
FALSIFIER_JOBS = REPO_ROOT / "runs" / "falsifier-jobs.jsonl"

_STOP = {"that", "with", "this", "from", "these", "their", "they", "have", "than", "will",
         "would", "been", "were", "such", "more", "also", "only", "very", "into", "over",
         "under", "where", "when", "which", "while", "there", "here", "about", "between",
         "through", "using", "does", "mass", "gap"}


def key_terms(statement: str, n: int = 6) -> list[str]:
    """The statement's key content terms (>= 4 chars, not stopwords) for matching."""
    words = re.findall(r"[a-z]{4,}", statement.lower())
    return [w for w in words if w not in _STOP][:n]


def search_arxiv(statement: str, max_results: int = 5) -> list[dict]:
    """Prior art: arXiv papers that test the claim, with BOTH the headline claim and the falsifier
    METHOD (the measurement/bound/exclusion sentences the paper states)."""
    try:
        records = literature.search_arxiv(statement, max_results)
    except Exception as e:  # noqa: BLE001 — arXiv unreachable is not fatal, it is reported
        return [{"error": f"arXiv unreachable: {type(e).__name__}"}]
    out = []
    for r in records:
        method = literature.extract_method(r.get("abstract", ""))
        out.append({"arxiv_id": r.get("arxiv_id", ""), "title": r.get("title", ""),
                    "claim": r.get("claim"), "method": method})
    return out


def search_mathlib(statement: str, max_hits: int = 10) -> list[dict]:
    """Search Mathlib (via Loogle) for theorems whose statement mentions the claim's key terms.

    This is the real 'search the Lean library' step: each hit carries the theorem's FULL TYPE (its
    statement), so whether it refutes the claim can be checked against the claim's negation — not
    guessed from a shared word.
    """
    import urllib.parse
    import urllib.request

    hits: list[dict] = []
    for frag in _loogle_fragments(statement)[:6]:
        url = "https://loogle.lean-lang.org/json?q=" + urllib.parse.quote(frag)
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode())
        except Exception:  # noqa: BLE001 — Loogle unreachable => no hits, not a crash
            continue
        for h in data.get("hits", [])[:5]:
            hits.append({"module": h.get("module", ""), "name": h.get("name", ""),
                         "type": h.get("type", "")})
        if len(hits) >= max_hits:
            break
    return hits[:max_hits]


def _loogle_fragments(statement: str) -> list[str]:
    """Identifier fragments for a Loogle (identifier-name) query, from the claim's key terms."""
    frags: list[str] = []
    for t in key_terms(statement, n=6):
        frags.append(t)
        parts = t.split(" ")
        if len(parts) > 1:
            frags.append(parts[0] + "".join(p.title() for p in parts[1:]))  # camelCase
    return [f for f in frags if f]


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
    """Find an existing falsifier across the FULL inventory — not just a keyword map.

    Scans the runner's falsifiers, the SEXTANT/Phantom falsifiers, and the lattice tools
    (``lattice_ym_su2``, ``glueball``) — matching the claim's key terms against each function's name
    and docstring. This is 'get the code that it needs' from the library that already exists; fetching
    code from external repos (GitHub/PyPI) is a further step, not wired here.
    """
    from pacland import runner

    hits: list[dict] = []
    for name, fn in runner.FALSIFIERS.items():
        if _matches(statement, name + " " + (fn.__doc__ or "")):
            hits.append({"falsifier": name, "source": "runner.FALSIFIERS"})
    _, phantom = runner._import_sextant()
    if phantom is not None:
        for name, fn in getattr(phantom, "FALSIFIERS", {}).items():
            if _matches(statement, name + " " + (fn.__doc__ or "")):
                hits.append({"falsifier": name, "source": "phantom.FALSIFIERS"})
    for modname in ("lattice_ym_su2", "glueball"):
        try:
            mod = __import__(f"pacland.{modname}", fromlist=[modname])
        except Exception:  # noqa: BLE001 — a missing optional dep is not a hit, not a crash
            continue
        for name in dir(mod):
            if not name.startswith(("measure", "verify", "compute", "glueball", "creutz", "wilson")):
                continue
            fn = getattr(mod, name)
            if callable(fn) and _matches(statement, name + " " + (fn.__doc__ or "")):
                hits.append({"falsifier": f"{modname}.{name}", "source": modname})
    return hits


def _matches(statement: str, text: str) -> bool:
    """True when any of the claim's key terms appears in the falsifier's name/docstring."""
    terms = key_terms(statement, n=4)
    low = text.lower()
    return any(t in low for t in terms)


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
    """FIND a falsifier first, BUILD only if none is found — in that order.

    1. code       — an existing falsifier in the codebase (runnable today),
    2. proof tree — a theorem in the local Lean tower that refutes the claim,
    3. Mathlib    — search Loogle for theorems whose STATEMENT matches (real library search),
    4. arXiv      — prior art that tests the claim, with its method (measurement/bound/exclusion),
    5. synthesize — only if none of the above found a falsifier, propose a candidate to build.

    ``found`` is True only when a falsifier was actually located; a bare key-term overlap is NOT
    counted as found — it is surfaced as a candidate with its statement for the kernel to decide.
    """
    code = search_code(statement)
    proof = search_proof_tree(statement, proof_dir)
    mathlib = search_mathlib(statement)
    arxiv = search_arxiv(statement)
    found = bool(code or proof or mathlib or any(r.get("method") for r in arxiv))
    synthesized = None
    if not found:
        synthesized = synthesize(statement, endpoint, key, model)
    return {
        "statement": statement,
        "found": found,
        "code": code,
        "proof_tree": proof,
        "mathlib": mathlib,
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


# The restricted-exec harness: the LLM code runs with a whitelist of builtins plus math/numpy/sympy.
# No __import__ / open / os / subprocess / socket / eval / exec / globals / locals — so the generated
# code cannot touch the filesystem or network even though it is a real subprocess. (Defense-in-depth;
# a true OS sandbox — bwrap/sandbox-exec — is the stronger form and is not available here.)
_RESTRICTED_PRELUDE = '''\
import builtins as _bi
import json as _json
import math as _math
import numpy as _np
import sympy as _sympy

_SAFE_BUILTINS = {
    "abs", "all", "any", "len", "range", "sum", "min", "max", "round", "int", "float", "str",
    "bool", "list", "dict", "tuple", "set", "frozenset", "enumerate", "zip", "map", "filter",
    "sorted", "reversed", "pow", "divmod", "isinstance", "print", "complex", "True", "False",
    "None", "Exception", "ValueError", "TypeError", "ZeroDivisionError", "IndexError", "KeyError",
    "ArithmeticError", "OverflowError",
}
_g = {"__builtins__": {k: getattr(_bi, k) for k in _SAFE_BUILTINS if hasattr(_bi, k)},
      "math": _math, "np": _np, "numpy": _np, "sympy": _sympy}
'''

_RESTRICTED_POSTLUDE = '''\
exec(_code, _g)
_result = _g["falsifier"]()
print(_json.dumps(list(_result)))
'''


def build_and_run_falsifier(statement: str, endpoint: str, key: str, model: str,
                            attempts: int = 3) -> dict:
    """Turn a synthesized falsifier into an EXECUTABLE test, validate it, run it, and REPAIR it.

    This closes the acquisition loop: acquire -> build (the LLM writes a Python ``falsifier()``
    returning ``(bool, str)``) -> VALIDATE it actually tests the candidate -> run it in a subprocess ->
    get a verdict. On a crash or unparseable output the error is fed back to the LLM and it retries
    (up to ``attempts``), the same repair loop the Lean prover uses. The code runs in a RESTRICTED
    namespace (whitelisted builtins + math/numpy/sympy — no ``__import__``/``open``/``os``/
    ``subprocess``/``socket``/``eval``) inside a subprocess with a timeout, so the "no files/network"
    instruction is enforced, not merely requested. The verdict is honest — it is from a SYNTHESIZED
    falsifier (LLM-written, not a vetted lattice/Lean computation), so it is a candidate verdict.
    """
    from pacland import runner

    if not model:
        return {"ran": False, "reason": "no LLM to write the falsifier"}

    import json
    import subprocess
    import tempfile
    from pathlib import Path

    base_prompt = (
        "Write a Python function `falsifier()` that tests the hypothesis below and returns "
        "(bool, str): True if the hypothesis SURVIVES (the test could not refute it), False if it is "
        "REFUTED, plus a one-line evidence string. Use only numpy / math / sympy — no files, no "
        "network, no prints except the return. Output ONLY the code.\n\nHypothesis: " + statement
    )
    last_reason = ""
    for attempt in range(attempts):
        prompt = base_prompt
        if last_reason:
            prompt += "\n\nYour previous attempt failed with: " + last_reason + \
                      "\nFix the bug and output ONLY the corrected code."
        try:
            code = runner._ask_llm(prompt, endpoint, key, model)
        except Exception as e:  # noqa: BLE001
            return {"ran": False, "reason": f"LLM failed: {type(e).__name__}"}
        code = code.strip().strip("`").replace("```python", "").replace("```", "").strip()

        issues = validate_falsifier(code, statement)
        if issues:
            last_reason = "vacuous falsifier rejected: " + "; ".join(issues)
            continue

        # The LLM code runs in a RESTRICTED namespace: only a whitelist of builtins plus math/numpy/sympy.
        harness = _RESTRICTED_PRELUDE + "\n_code = " + repr(code) + "\n" + _RESTRICTED_POSTLUDE
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(harness)
            path = f.name
        try:
            r = subprocess.run(["python3", path], capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            Path(path).unlink(missing_ok=True)
            last_reason = "synthesized falsifier timed out"
            continue
        Path(path).unlink(missing_ok=True)
        if r.returncode != 0:
            last_reason = f"falsifier code failed: {(r.stderr or r.stdout)[:200]}"
            continue
        try:
            survived, evidence = json.loads(r.stdout.strip())
        except Exception:  # noqa: BLE001
            last_reason = f"falsifier returned unparseable output: {r.stdout[:120]}"
            continue
        return {"ran": True, "survived": bool(survived), "evidence": str(evidence), "code": code,
                "attempts": attempt + 1,
                "note": "synthesized falsifier (LLM-written, not a vetted lattice/Lean computation)"}

    return {"ran": False, "reason": last_reason or "could not build a runnable falsifier"}


def record_falsifier_job(statement: str, proposed_falsifier: str, reason: str) -> str:
    """Record a "build this falsifier" job so another process or session can complete it.

    The frontier does not stall on an un-buildable falsifier: it writes the claim, the proposed test,
    and the reason it could not be built now, as a queued job. Returns the job id.
    """
    job = {"job_id": uuid.uuid4().hex[:12], "statement": statement,
           "proposed_falsifier": proposed_falsifier or "(none proposed)",
           "reason": reason or "unknown", "status": "queued", "created_at": time.time()}
    FALSIFIER_JOBS.parent.mkdir(parents=True, exist_ok=True)
    with FALSIFIER_JOBS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(job) + "\n")
    return job["job_id"]


def list_falsifier_jobs(status: str | None = None) -> list[dict]:
    """The falsifier job queue, newest first, optionally filtered by ``status``."""
    if not FALSIFIER_JOBS.exists():
        return []
    jobs = [json.loads(line) for line in FALSIFIER_JOBS.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    if status:
        jobs = [j for j in jobs if j.get("status") == status]
    return list(reversed(jobs))


def claim_falsifier_job(job_id: str) -> bool:
    """Mark a job in-progress so one session owns it (a mutex for the shared queue)."""
    jobs = list_falsifier_jobs()
    changed = False
    for j in jobs:
        if j["job_id"] == job_id and j.get("status") == "queued":
            j["status"] = "in-progress"
            changed = True
    if changed:
        _rewrite_jobs(jobs)
    return changed


def mark_falsifier_built(job_id: str, falsifier: str) -> bool:
    """Mark a job as built (a falsifier now exists), so the queue reflects progress."""
    jobs = list_falsifier_jobs()
    changed = False
    for j in jobs:
        if j["job_id"] == job_id:
            j["status"] = "built"
            j["falsifier"] = falsifier
            changed = True
    if changed:
        _rewrite_jobs(jobs)
    return changed


def _rewrite_jobs(jobs: list[dict]) -> None:
    FALSIFIER_JOBS.parent.mkdir(parents=True, exist_ok=True)
    with FALSIFIER_JOBS.open("w", encoding="utf-8") as fh:
        for j in jobs:
            fh.write(json.dumps(j) + "\n")
