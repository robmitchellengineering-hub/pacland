"""The discovery engine — generate, construct, validate, and record over the guarded frontier.

The loop reads the open obligations from `web/research-frontier.json`, runs the cross-field search,
proposes approaches (the LLM), runs the Lean kernel to construct proofs, and records reproducible
evidence. Every LLM step is wireable: set `SEXTANT_LLM_ENDPOINT`, `SEXTANT_LLM_MODEL` and
`SEXTANT_LLM_KEY` to any OpenAI-compatible endpoint — the default is `deepseek-v4-pro` (the frontier
model), a self-hosted Ollama works at `http://100.73.60.26:11434/v1`, and anyone can point it at their
own model the same way.

Usage:
    python -m pacland.discovery --list           # identify the open obligations
    python -m pacland.discovery --search         # cross-field candidates
    python -m pacland.discovery --generate       # the LLM proposes a novel approach
    python -m pacland.discovery --prove          # run the Lean kernel + read the goal state
    python -m pacland.discovery --refine         # the LLM proposes a Lean attempt
    python -m pacland.discovery --tactic         # the kernel's goal → the LLM's next tactic
    python -m pacland.discovery --beam           # N candidate tactics (the search's proposal half)
    python -m pacland.discovery --beam-filter    # N fixes, ranked by the kernel's error count
    python -m pacland.discovery --validate       # the full tower + guarded tests
    python -m pacland.discovery --record         # run the falsifiers + write reproducible evidence
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FRONTIER = ROOT / "web" / "research-frontier.json"


def _frontier() -> dict:
    return json.loads(FRONTIER.read_text())


def open_obligations() -> list[dict]:
    """The open obligations (state == 'open') from the guarded frontier."""
    return [o for o in _frontier()["obligations"] if o.get("state") == "open"]


def _catalog():
    sys.path.insert(0, str(ROOT / "src"))
    from pacland import sextant
    return sextant.CATALOG


def list_open() -> str:
    lines = []
    for o in open_obligations():
        e = _catalog().get(o["name"], {})
        falsifier = e.get("falsifier") or "(no falsifier wired)"
        tier = e.get("tier", "-")
        lines.append(f"◐ {o['name']}  [tier {tier}]")
        lines.append(f"    rung:      {o['rung']}")
        lines.append(f"    falsifier: {falsifier}")
    return "\n".join(lines)


def run_falsifiers() -> str:
    lines = []
    for o in open_obligations():
        e = _catalog().get(o["name"])
        simulate = e.get("simulate") if e else None
        if simulate is None:
            lines.append(f"◐ {o['name']:<32} NO-FALSIFIER  ({e.get('falsifier','') if e else ''})")
            continue
        try:
            survived, evidence = simulate()
            status = "SURVIVES" if survived else "REFUTED"
        except Exception as exc:  # a falsifier that errors is information too
            status, evidence = "ERROR", f"{type(exc).__name__}: {exc}"
        lines.append(f"◐ {o['name']:<32} {status}  {evidence}")
    return "\n".join(lines)


def record_results() -> list[dict]:
    """Run the falsifiers and record REPRODUCIBLE evidence (the 'learn' stage of the loop).

    Each run records the falsifier's name, the exact command that re-runs it, the commit the code
    was at, and the timestamp — so a recorded result can be re-produced, not just read.
    """
    import datetime
    import subprocess
    at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                            cwd=ROOT).stdout.strip() or "unknown"
    results = []
    for o in open_obligations():
        e = _catalog().get(o["name"])
        simulate = e.get("simulate") if e else None
        if simulate is None:
            results.append({
                "name": o["name"], "status": "NO-FALSIFIER",
                "evidence": e.get("falsifier", "") if e else "",
                "falsifier": None,
                "command": "python -m pacland.discovery --record",
                "commit": commit, "at": at,
            })
            continue
        try:
            survived, evidence = simulate()
            status = "SURVIVES" if survived else "REFUTED"
        except Exception as exc:
            status, evidence = "ERROR", f"{type(exc).__name__}: {exc}"
        results.append({
            "name": o["name"], "status": status, "evidence": str(evidence),
            "falsifier": getattr(simulate, "__name__", str(simulate)),
            "command": f"python -c 'from pacland import mass_gap_falsifiers; print(mass_gap_falsifiers.{getattr(simulate, '__name__', '')}())'",
            "commit": commit, "at": at,
        })
    out = ROOT / "web" / "evidence.json"
    out.write_text(json.dumps({"schema": "sextant-evidence", "commit": commit, "runs": results}, indent=2))
    return results


def approaches() -> str:
    """List the known routes + the next step for each open obligation (the 'generate' stage)."""
    data = json.loads((ROOT / "web" / "approaches.json").read_text())
    lines = []
    for o in data["obligations"]:
        lines.append(f"◐ {o['name']}")
        for r in o["routes"]:
            mark = "●" if r["state"] == "attempted" else "○"
            lines.append(f"    {mark} {r['name']} — next: {r['next']}")
            if r.get("note"):
                lines.append(f"        ({r['note']})")
    return "\n".join(lines)


SEARCH_TYPES = {
    "ym-linked-cluster-contraction": ("spectral-gap", "gauge-theory"),
    "ym-log-sobolev": ("markov", "gauge-theory"),
    "ym-volume-uniform-su2": ("spectral-gap", "gauge-theory"),
}


def search() -> str:
    """The 'search across fields' stage: for each open obligation, list same-type structures in other
    fields (candidate transfers — a match is a correspondence, NOT a verified transfer)."""
    from pacland import cross_reference
    lines = []
    for o in open_obligations():
        tt = SEARCH_TYPES.get(o["name"])
        lines.append(f"◐ {o['name']}")
        if tt is None:
            lines.append("    (no cross-field type mapped)")
            continue
        typ, dom = tt
        cands = cross_reference.cross_field(typ, dom)
        if not cands:
            lines.append(f"    no {typ} structures outside {dom}")
        for c in cands[:5]:
            p = c["payload"]
            d = p.get("domain") or p.get("domains") or []
            d = d if isinstance(d, str) else ", ".join(d)
            reproduces = p.get("reproduces", "")
            lines.append(f"    → [{p.get('type', '')}] in {d} — reproduces: {reproduces}")
    return "\n".join(lines)


ATTEMPT_TARGETS = {
    "ym-linked-cluster-contraction": ("animals bound", "#{connected clusters of size n} ≤ Δ^(2(n−1)) — the spanning-tree / Euler-tour injection on top of walk_count_bound (proved)"),
    "ym-log-sobolev": ("log-Sobolev → mixing bridge", "the log-Sobolev constant → the mixing time, chaining clustering_iff_gap (proved)"),
    "ym-volume-uniform-su2": ("non-Abelian FSS", "the SU(2) character two-point function dominated by the free propagator"),
}


def attempt() -> str:
    """The 'attempt proofs' stage: for each open obligation, name the Lean theorem that is the next rung.
    The kernel status is NOT asserted here — `--prove` / `--validate` run the build and report the real
    result, so a claim of green must come from an actual build, not a hard-coded string."""
    lines = []
    for o in open_obligations():
        target = ATTEMPT_TARGETS.get(o["name"])
        lines.append(f"◐ {o['name']}")
        if target is None:
            lines.append("    (no Lean target mapped)")
            continue
        name, desc = target
        lines.append(f"    next theorem: {name} — {desc}")
        lines.append("    kernel status: run --prove or --validate (the build is executed there, not asserted here)")
    return "\n".join(lines)


KERNEL = "rob@100.73.60.26"


def _kernel_build(target: str, timeout: int = 300):
    """Run `lake build <target>` — the SINGLE configurable execution mechanism. By default it builds in
    the LOCAL checkout (`ROOT/pacland-proof`); set `SEXTANT_KERNEL` to an SSH host to build remotely
    instead. Returns the CompletedProcess; callers inspect `.returncode` / `.stdout` / `.stderr`."""
    import subprocess
    cmd = ('export PATH="$HOME/.elan/bin:$PATH"; cd ' + str(ROOT / "pacland-proof") +
           f' && lake build {target} 2>&1')
    host = os.environ.get("SEXTANT_KERNEL", "")
    if host:
        return subprocess.run(
            ['ssh', '-i', os.path.expanduser('~/.ssh/pacland-rog-agent'), host, cmd],
            capture_output=True, text=True, timeout=timeout)
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)


def _goal_lines(stdout: str, limit: int = 40) -> str:
    """The error / goal-state lines from a build log (the part the retry loop reads). Slices LINES,
    not characters."""
    lines = [l for l in stdout.splitlines() if "error" in l or "⊢" in l]
    return "\n".join(lines[: limit])


def prove() -> str:
    """The 'construct proofs' stage: run the Lean kernel on the target file and read back the actual
    goal state, so the engine retries from the kernel's error rather than guessing."""
    try:
        proc = _kernel_build("PaclandProof.QM.AnimalsBound")
    except Exception as exc:  # noqa: BLE001 — the kernel is one of several executors
        return f"the kernel raised {type(exc).__name__}: {exc}"
    out = _goal_lines(proc.stdout)
    if proc.returncode != 0 and not out:
        return f"the kernel failed (exit {proc.returncode}):\n" + proc.stdout[-500:]
    if not out:
        return "the kernel reports: AnimalsBound builds clean — no goal remaining"
    return "the kernel reports:\n" + out


def generate() -> str:
    """The 'generate approaches' stage: ask the LLM (deepseek-v4-pro) to propose a NOVEL candidate
    approach for the root obligation, different from the known and rejected routes. The proposal is a
    candidate only — the encoding-check gate and the kernel decide whether it is worth anything."""
    import urllib.request
    fr = json.loads((ROOT / "web" / "research-frontier.json").read_text())
    ap = json.loads((ROOT / "web" / "approaches.json").read_text())
    rej = json.loads((ROOT / "web" / "rejections.json").read_text())
    known = "; ".join(r["name"] + " → " + r.get("next", "") for o in ap["obligations"] for r in o.get("routes", []))
    rejected = "; ".join(r["name"] + " (" + r["why_failed"] + ")" for r in rej["rejections"])
    prompt = (
        "You are a mathematical discovery engine. Propose ONE novel approach to this open obligation:\n"
        f"{fr['root_obligation']}\n\n"
        f"Known routes (do NOT repeat): {known}\n"
        f"Rejected routes (do NOT repeat): {rejected}\n\n"
        "Give the candidate approach as: (1) the mechanism, (2) the first lemma to prove, (3) why it is "
        "different from the known routes. Be concrete and short."
    )
    key = _llm_key()
    req = urllib.request.Request(
        os.environ.get("SEXTANT_LLM_ENDPOINT", "https://api.deepseek.com/v1") + "/chat/completions",
        data=json.dumps({
            "model": os.environ.get("SEXTANT_LLM_MODEL", "deepseek-v4-pro"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
        return "the LLM proposes:\n" + data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return f"the LLM call failed: {type(exc).__name__}: {exc}"


def _llm_key() -> str:
    """The API key: `SEXTANT_LLM_KEY` if set, else the DeepSeek key file. The env var is the documented
    wire; the file is the local fallback so a checkout without the env still works."""
    env = os.environ.get("SEXTANT_LLM_KEY")
    if env:
        return env
    return open(os.path.expanduser("~/.dsh/deepseek-api-key")).read().strip()


def _llm(prompt: str, temperature: float = 0.3) -> str:
    """One deepseek-v4-pro completion; returns the raw content text (raises on failure)."""
    import urllib.request
    key = _llm_key()
    req = urllib.request.Request(
        os.environ.get("SEXTANT_LLM_ENDPOINT", "https://api.deepseek.com/v1") + "/chat/completions",
        data=json.dumps({
            "model": os.environ.get("SEXTANT_LLM_MODEL", "deepseek-v4-pro"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def _refine_prompt() -> str:
    target = ("tree_euler_tour_length : a tree (SimpleGraph.IsTree) on a finite nonempty type V has a walk "
              "of length ≤ 2 * (Fintype.card V - 1) visiting every vertex (each of the n-1 edges walked twice).")
    known = (
        "Already proved and available: connected_exists_visiting_walk (a connected graph has a walk visiting "
        "every vertex); walk_count_bound; SimpleGraph.IsTree.exists_vert_degree_one_of_nontrivial (a nontrivial "
        "tree has a degree-1 leaf); SimpleGraph.Connected.induce_compl_singleton_of_degree_eq_one (removing a "
        "degree-1 vertex keeps the induced subgraph connected); SimpleGraph.IsTree.card_edgeFinset (a tree has "
        "n-1 edges); Walk.support / append / reverse / length_append / support_append.\n\n"
        "A WORKING example of this exact machinery, already proved in the tower (mimic its style):\n"
        "connected_exists_visiting_walk does `Finset.induction_on` over the vertex set, `by_cases a = v₀`, "
        "obtains the path via `hG.exists_isPath v₀ a`, builds `w.append (p₁.append p₁.reverse)`, and shows "
        "membership with `SimpleGraph.Walk.support_append` + `List.mem_append` + `SimpleGraph.Walk.end_mem_support`."
    )
    return (
        f"Write Lean 4 (Mathlib) code that proves: {target}\n\n{known}\n\n"
        "Use the leaf induction: pick the degree-1 leaf, remove it (the induced subgraph on the other vertices "
        "is a smaller tree), recurse by strong induction on Fintype.card V, and append the leaf edge twice. "
        "For the MECHANICAL subgoals (arithmetic, list/set membership, the length bound), use the deterministic "
        "hammer first: `aesop`, `grind`, `simp`, `omega`, `ring` — do not hand-write these. "
        "No sorry/admit/axiom. Output only the complete theorem with its proof."
    )


def refine() -> str:
    """The 'learn' stage (retry-on-goal-state): feed the open rung + the proved lemmas to the LLM and
    get a proposed Lean proof attempt, which `--prove` then checks. The LLM proposes; the kernel decides."""
    return "the LLM proposes this Lean attempt (check it with --prove):\n\n" + _llm(_refine_prompt())


def construct() -> str:
    """One iteration of the closed loop: LLM-propose → write to a scratch file → kernel-check → report
    the goal state. The scratch file is separate from the green tower, so a bad attempt cannot corrupt it."""
    import re
    import subprocess
    code = _llm(_refine_prompt())
    m = re.search(r'```(?:lean4|lean)?\n(.*?)```', code, re.S)
    code = (m.group(1) if m else code).strip()
    code = code.replace("import Mathlib", "").replace("open SimpleGraph", "").strip()
    scratch = ROOT / "pacland-proof" / "PaclandProof" / "QM" / "AnimalsBoundAttempt.lean"
    scratch.write_text(
        "import Mathlib\nimport PaclandProof.QM.FullLattice\n\nnamespace QM\n"
        + code + "\n\nend QM\n"
    )
    try:
        proc = _kernel_build("PaclandProof.QM.AnimalsBoundAttempt")
    except Exception as exc:  # noqa: BLE001
        return f"the kernel raised {type(exc).__name__}: {exc}"
    out = _goal_lines(proc.stdout)
    # record the attempt (the "attempted proofs" data the interface renders), success or failure
    import datetime
    attempts_path = ROOT / "web" / "attempts.json"
    attempts = json.loads(attempts_path.read_text()).get("attempts", []) if attempts_path.exists() else []
    attempts.append({
        "theorem": "tree_euler_tour_length",
        "code": code,
        "result": out or "builds clean",
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    })
    attempts_path.write_text(json.dumps({"schema": "sextant-attempts", "attempts": attempts[-20:]}, indent=2))
    if not out:
        return "the kernel reports: the LLM's attempt builds clean — the length bound may be closed"
    return "wrote AnimalsBoundAttempt.lean + recorded the attempt in web/attempts.json; the kernel reports:\n" + out


def tactic() -> str:
    """The tactic-level retry (AlphaProof/LeanDojo shape): read the kernel's first goal state from the
    scratch attempt and ask the LLM for the NEXT tactic that closes it, rather than a whole-file rewrite."""
    import subprocess
    try:
        proc = _kernel_build("PaclandProof.QM.AnimalsBoundAttempt")
    except Exception as exc:  # noqa: BLE001
        return f"the kernel raised {type(exc).__name__}: {exc}"
    goal = _goal_lines(proc.stdout, 30)
    if not goal:
        return "no goal state — the scratch attempt builds clean"
    # simple retrieval (LeanDojo-style): for each unknown identifier in the error, grep the tower +
    # Mathlib for the qualified name, so the LLM uses the right namespace instead of guessing.
    import re
    hits = []
    for m in re.finditer(r"Unknown (?:identifier|constant) `([^`]+)`", goal):
        name = m.group(1)
        r = subprocess.run(
            f"grep -rn '{name}' pacland-proof/PaclandProof pacland-proof/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph 2>/dev/null | head -3",
            shell=True, capture_output=True, text=True, cwd=ROOT)
        if r.stdout.strip():
            hits.append(r.stdout.strip())
    context = "\n".join(hits)
    prompt = (
        "The Lean kernel reports this goal/error on the tree-length-bound attempt:\n\n" + goal + "\n\n"
        + (f"Qualified names in the codebase (use these exact names):\n{context}\n\n" if context else "")
        + "Propose the NEXT single Lean tactic (or the minimal fix) that closes the FIRST goal or error. "
        "Give only the tactic(s), no prose."
    )
    return "the kernel's goal:\n" + goal + ("\n\nretrieved names:\n" + context if context else "") + \
        "\n\nthe LLM proposes:\n" + _llm(prompt, temperature=0.1)


def build_evidence() -> dict:
    """The AUTHORITATIVE verification evidence: run the actual build and capture the commit SHA, the dirty
    state, the Lean version, the EXACT command, the FULL build log (stdout + stderr), the exit code, and the
    full theorem list — never inferred from a previous run."""
    import subprocess
    commit = subprocess.run("git rev-parse HEAD", shell=True, capture_output=True, text=True,
                            cwd=ROOT).stdout.strip()
    dirty = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True,
                           cwd=ROOT).stdout.strip()
    lean = subprocess.run('export PATH="$HOME/.elan/bin:$PATH"; cd pacland-proof && lake env lean --version',
                          shell=True, capture_output=True, text=True, cwd=ROOT).stdout.strip()
    build_cmd = 'export PATH="$HOME/.elan/bin:$PATH"; cd pacland-proof && lake build PaclandProof 2>&1'
    build = subprocess.run(build_cmd, shell=True, capture_output=True, text=True, cwd=ROOT, timeout=900)
    theorems = subprocess.run(
        "grep -rhoE 'theorem [a-zA-Z0-9_]+' pacland-proof/PaclandProof/QM/*.lean | sed 's/theorem //' | sort -u",
        shell=True, capture_output=True, text=True, cwd=ROOT).stdout.strip()
    return {
        "commit": commit,
        "dirty": dirty.split("\n") if dirty else [],
        "lean_version": lean.strip(),
        "command": build_cmd,
        "build_log": build.stdout,
        "build_stderr": build.stderr,
        "build_exit": build.returncode,
        "theorems": theorems.split("\n") if theorems else [],
    }


def validate() -> str:
    """The 'independently validate' stage: a SEPARATE check distinct from the construction's single-file
    kernel run — the whole tower build plus the guarded test suite, with the FULL authoritative evidence
    (commit, dirty state, Lean version, exact command, full build log, exit code, theorem list, test
    output) written to web/build-evidence.json. `ok` is false unless both the build and tests exit 0, so
    a failed validation cannot be reported as successful."""
    import subprocess
    ev = build_evidence()
    tests = subprocess.run(
        'PYTHONPATH=src python3 -m pytest tests/test_site_index.py tests/test_research_frontier.py -q 2>&1',
        shell=True, capture_output=True, text=True, cwd=ROOT, timeout=300)
    ok = ev["build_exit"] == 0 and tests.returncode == 0
    (ROOT / "web" / "build-evidence.json").write_text(json.dumps({
        "schema": "sextant-build-evidence",
        "commit": ev["commit"],
        "dirty": ev["dirty"],
        "lean_version": ev["lean_version"],
        "command": ev["command"],
        "build_log": ev["build_log"],
        "build_stderr": ev["build_stderr"],
        "build_exit": ev["build_exit"],
        "theorems": ev["theorems"],
        "tests": tests.stdout,
        "tests_exit": tests.returncode,
        "ok": ok,
    }, indent=2))
    # regenerate the canonical view so the site never shows stale verification data
    import subprocess as _sp
    _sp.run([sys.executable, str(ROOT / "scripts" / "build_frontier_view.py")],
            capture_output=True, text=True, cwd=ROOT, timeout=120)
    return ("independent validation (executed, not inferred):\n"
            f"  commit:       {ev['commit']}\n"
            f"  dirty:        {len(ev['dirty'])} uncommitted path(s)\n"
            f"  lean:         {ev['lean_version']}\n"
            f"  build exit:   {ev['build_exit']} (log {len(ev['build_log'])} chars, {len(ev['theorems'])} theorems)\n"
            f"  tests exit:   {tests.returncode}\n"
            f"  OK:           {ok}\n"
            "  → web/build-evidence.json + regenerated web/frontier-view.json")


def beam(n: int = 3) -> str:
    """The beam-search proposal half: propose N different candidate tactics for the current goal, so the
    engine (or a human) picks the one the kernel accepts instead of trusting a single sample."""
    import subprocess
    try:
        proc = _kernel_build("PaclandProof.QM.AnimalsBoundAttempt")
    except Exception as exc:  # noqa: BLE001
        return f"the kernel raised {type(exc).__name__}: {exc}"
    goal = _goal_lines(proc.stdout, 30)
    if not goal:
        return "no goal state — the scratch attempt builds clean"
    import re
    hits = []
    for m in re.finditer(r"Unknown (?:identifier|constant) `([^`]+)`", goal):
        name = m.group(1)
        r = subprocess.run(
            f"grep -rn '{name}' pacland-proof/PaclandProof pacland-proof/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph 2>/dev/null | head -3",
            shell=True, capture_output=True, text=True, cwd=ROOT)
        if r.stdout.strip():
            hits.append(r.stdout.strip())
    context = "\n".join(hits)
    base = (
        "The Lean kernel reports this goal/error on the tree-length-bound attempt:\n\n" + goal + "\n\n"
        + (f"Qualified names in the codebase:\n{context}\n\n" if context else "")
        + "Propose the NEXT single Lean tactic that closes the FIRST goal or error. Only the tactic(s)."
    )
    out = ["the kernel's goal:\n" + goal]
    for i in range(n):
        p = _llm(base + f"\n(Sample {i+1}/{n}: give a DIFFERENT tactic.)", temperature=0.5)
        out.append(f"candidate {i+1}:\n{p.strip()}")
    return "\n\n".join(out)


def beam_filter(n: int = 3) -> str:
    """The beam filter (the search's accept/reject half): propose N candidate fixes, apply each to the
    scratch attempt, and let the kernel count the remaining errors — mechanically ranking the candidates
    the kernel prefers. The scratch is restored afterwards, so the green tower is never touched."""
    import subprocess
    import re
    scratch = ROOT / "pacland-proof" / "PaclandProof" / "QM" / "AnimalsBoundAttempt.lean"
    base = scratch.read_text()
    candidates = []
    try:
        for i in range(n):
            goal = _goal_lines(_kernel_build("PaclandProof.QM.AnimalsBoundAttempt").stdout, 12)
            prompt = (
                "The Lean kernel reports these errors on the tree-length-bound attempt:\n\n" + goal + "\n\n"
                "Give a MINIMAL fix as ONE line to insert at the top of the file (e.g. an `open SimpleGraph`, "
                f"a namespace qualifier, or a `set_option`). Only the line, no prose. (Sample {i+1}/{n}, different.)"
            )
            candidates.append(_llm(prompt, temperature=0.6).strip().split("\n")[0])
        results = []
        for cand in candidates:
            scratch.write_text(base.replace("namespace QM\n", "namespace QM\n" + cand + "\n", 1))
            r = _kernel_build("PaclandProof.QM.AnimalsBoundAttempt")
            errs = r.stdout.count("error:")
            results.append((cand[:70], errs))
        results.sort(key=lambda x: x[1])
        return "candidate fixes, ranked by the kernel's error count (fewer is better):\n" + \
            "\n".join(f"  {errs} errors — {cand}" for cand, errs in results)
    finally:
        scratch.write_text(base)


def hammer() -> str:
    """The ATP hammer: try the deterministic tactics (aesop / grind / simp / omega) on a mechanical goal
    and report which closes it — the sound tactic engine that needs no LLM for the easy subgoals."""
    scratch = ROOT / "pacland-proof" / "PaclandProof" / "QM" / "Hammer.lean"
    results = []
    try:
        for tactic in ["aesop", "grind", "simp", "omega"]:
            scratch.write_text(
                "import Mathlib\nnamespace QM\n"
                f"example (n : ℕ) : 1 ≤ n + 1 := by {tactic}\n"
                "end QM\n"
            )
            r = _kernel_build("PaclandProof.QM.Hammer")
            results.append((tactic, r.stdout.count("error:") == 0))
    finally:
        scratch.unlink(missing_ok=True)
    return "the hammer on `1 ≤ n + 1` (a mechanical goal):\n" + \
        "\n".join(f"  {t}: {'closed ✓' if ok else 'failed'}" for t, ok in results)


def loop(n: int = 3) -> str:
    """The CLOSED retry loop: propose → compile → capture the errors → feed them back → retry, up to N
    iterations. The kernel, not the LLM, decides whether an attempt is accepted; a clean build stops the
    loop. This is the 'construct proofs' stage Rob's #3 asks for — generate, compile, capture, iterate."""
    import re
    import subprocess
    code = _llm(_refine_prompt())
    last_errs = ""
    for i in range(n):
        m = re.search(r'```(?:lean4|lean)?\n(.*?)```', code, re.S)
        body = (m.group(1) if m else code).strip()
        body = body.replace("import Mathlib", "").replace("open SimpleGraph", "").strip()
        scratch = ROOT / "pacland-proof" / "PaclandProof" / "QM" / "AnimalsBoundAttempt.lean"
        scratch.write_text(
            "import Mathlib\nimport PaclandProof.QM.FullLattice\n\nnamespace QM\n"
            + body + "\n\nend QM\n")
        try:
            r = _kernel_build("PaclandProof.QM.AnimalsBoundAttempt")
        except Exception as exc:  # noqa: BLE001
            return f"iteration {i+1}: the kernel raised {type(exc).__name__}: {exc}"
        last_errs = _goal_lines(r.stdout, 20)
        if r.returncode != 0 and not last_errs:
            last_errs = r.stdout[-500:]
        if not last_errs:
            return f"iteration {i+1}: the kernel ACCEPTS — builds clean (no error)"
        code = _llm(
            "The Lean kernel REJECTED this attempt with these errors:\n" + last_errs +
            "\n\nFix the attempt and output the corrected complete theorem (no sorry/admit/axiom).\n\n"
            "Previous attempt:\n" + body, temperature=0.2)
    return f"no proof after {n} iterations; the last errors were:\n" + last_errs


def main() -> int:
    ap = argparse.ArgumentParser(description="the discovery loop over the open obligations")
    ap.add_argument("--list", action="store_true", help="list the open obligations")
    ap.add_argument("--run", action="store_true", help="run each obligation's falsifier")
    ap.add_argument("--record", action="store_true", help="run the falsifiers and write the evidence")
    ap.add_argument("--approaches", action="store_true", help="list the known routes + next steps")
    ap.add_argument("--search", action="store_true", help="search other fields for same-type structures")
    ap.add_argument("--attempt", action="store_true", help="name the next Lean theorem to prove")
    ap.add_argument("--prove", action="store_true", help="run the Lean kernel on the target and read the goal state")
    ap.add_argument("--generate", action="store_true", help="ask the LLM to propose a novel candidate approach")
    ap.add_argument("--refine", action="store_true", help="ask the LLM for a Lean proof attempt of the open rung")
    ap.add_argument("--construct", action="store_true", help="LLM-propose → write → kernel-check → report (one loop iteration)")
    ap.add_argument("--tactic", action="store_true", help="read the kernel's goal state and ask the LLM for the next tactic")
    ap.add_argument("--validate", action="store_true", help="run the full tower build + guarded tests as an independent check")
    ap.add_argument("--beam", action="store_true", help="propose N candidate tactics for the current goal (the search's proposal half)")
    ap.add_argument("--beam-filter", action="store_true", help="propose N fixes, apply each, and rank them by the kernel's error count")
    ap.add_argument("--hammer", action="store_true", help="try the deterministic tactics (aesop/grind/simp/omega) on a mechanical goal")
    ap.add_argument("--loop", action="store_true", help="the closed retry loop: propose → compile → capture → feed back → retry (up to 3 iterations)")
    args = ap.parse_args()
    if args.loop:
        print(loop())
    elif args.hammer:
        print(hammer())
    elif args.beam_filter:
        print(beam_filter())
    elif args.beam:
        print(beam())
    elif args.validate:
        print(validate())
    elif args.tactic:
        print(tactic())
    elif args.construct:
        print(construct())
    elif args.refine:
        print(refine())
    elif args.generate:
        print(generate())
    elif args.prove:
        print(prove())
    elif args.attempt:
        print(attempt())
    elif args.search:
        print(search())
    elif args.approaches:
        print(approaches())
    elif args.record:
        results = record_results()
        for r in results:
            print(f"◐ {r['name']:<32} {r['status']}  {r['evidence']}")
        print(f"\nwrote web/evidence.json ({len(results)} runs)")
    elif args.run:
        print(run_falsifiers())
    else:
        print(list_open())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
