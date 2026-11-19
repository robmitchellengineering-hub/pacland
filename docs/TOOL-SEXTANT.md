# Tool Sextant — the unified verification + discovery system

**One name for the whole system**: the yes/no proof engine + the hypothesis loop + the belief layer.

## The whole system (what exists, one map)

| Layer | What it is | Location |
|---|---|---|
| SEXTANT — the yes/no engine | 33 claims FORCED/FREE/IMPOSSIBLE, each with a falsifier | `src/pacland/sextant.py` |
| Phantom — the falsifiers | live oracles (CHSH=2√2, no-cloning, Clifford scaling) | `src/pacland/phantom.py` |
| Discovery loop | generate → test → promote → record | `src/pacland/runner.py` |
| Hypothesis registry | open questions, constraint-first, each with a falsifier | `src/pacland/hypotheses.py` |
| Belief layer | prior → Bayes → posterior → EIG → calibration | `src/pacland/belief.py` |
| Graded challenge sequence (G2) | 8 ordered challenges PASS/FAIL/INCONCLUSIVE/NA | `src/pacland/challenges.py` |
| Benchmark harness (G3) | 4 suites + 5 arms, blind, discoveries-per-effort | `src/pacland/benchmarks.py` |
| Rust ports | `morph-verify` (registry) + `rob-quantum` (compute) | MorpheOS / MorpheOS-Secure |
| Site node | proof-engine UI + global quest | `web/sextant.html`, `web/node.html` |

## The two directives (Rob, 2026-11-18)

1. **Unify all of it under the name "Tool Sextant".**
2. **Once the LLM is trained**, add the WHOLE system (not just the 33-claim catalog) to the sextant node
   on the site — `web/sextant.html` + `web/node.html` — and make it **downloadable**.

## Delivery forms — the answer is BOTH (they already exist, split)

- **Installable on a computer (runnable):** `pip install pacland` → `sextant-node` (`pacland.sextant_node`)
  serves the whole system locally at `http://127.0.0.1:8090` — the GUI, the yes/no engine, the global
  quest, the falsifier button, the "contribute a discovery" flow, and a "point at your own AI" hook.
  Entry points in `pyproject.toml`: `pacland`, `sextant`, `sextant-node`.
- **As the computer (the OS):** the Rust ports `morph-verify` (SEXTANT registry) and `rob-quantum`
  (quantum compute) compile into MorpheOS, booted via `images/x86-qemu/build.sh`.

**Consolidation needed:** the Rust ports currently live in THREE worktrees with duplicate `morph-verify`
copies (`MorpheOS-sextant-cli`, `MorpheOS-Secure-quantum`, `MorpheOS-morphverify-fix`). Unify them under
Tool Sextant so there is ONE `morph-verify`, ONE `rob-quantum`, and ONE node — not three.

## Current honest gap

The site node today shows only the yes/no engine (the catalog). The discovery loop, belief layer,
challenges, and benchmarks are in code but not on the site and not packaged for download. That is the
gap directive 2 closes.

## What "once the LLM is trained" gates

- The generator behind `hypotheses.py`/`runner.py` is still the knowledge-base version; the LLM-backed
  generator (DeepSeek API key in `~/.dsh/deepseek-api-key`, or Ollama on `pacland-rog`) is the pluggable
  next step recorded in `PLANS/HANDOVER-discovery-engine.md`.
- The real benchmark (`benchmarks.py`) needs that LLM generator before it measures anything.
- Downloadability = a packaged release (the Python package + the Rust ports) that ships the whole system,
  not just the catalog.
