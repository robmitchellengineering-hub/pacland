# SEXTANT — User Manual

This manual is written so **any session (human or harness) can operate SEXTANT correctly**. Read it
before driving the engine; it is self-contained and gives the exact commands, function signatures,
environment, and conventions.

---

## 1. What SEXTANT is

A **verified-discovery engine**, not a hypothesis generator. It searches knowledge, proposes
cross-discipline hypotheses, falsifies them, attempts formal proofs, and keeps an auditable record of
what is known, unknown, and disproven.

The guiding north star is **Milestone 3**: a *new, independently-verified analytic bound* (or a new
cross-structure connection) — more significant than another thousand simulations.

---

## 2. Architecture

**The data model** — five registries + a claim store, all append/upsert JSONL under
`~/.dsh/sextant-registry/`:

| kind | what it holds |
|---|---|
| `structure` | typed structures (`heat-equation`, `markov-chain-monte-carlo`, …) |
| `domain` | disciplines |
| `property` | claims/lemmas with an epistemic **tier** (1–5) |
| `evidence` | tests / datasets |
| `mapping` | cross-field links (`from → to` + `kind_of_yield`) |
| `claim` | a research claim with a **status**: `survived` / `failed` / `gated-out` / `open` / `manual` |

**The loop** — `generate → falsify → 8-stage challenge gate → prove → record → learn`, with a
supervisor that decomposes a goal, allocates budget, retries, and stops on criteria.

**The five engines** — mathematical (search+prove) · computational (simulate+test) · empirical (real
datasets) · knowledge (the record) · supervisory (choose the frontier) — all through **one
evidence-and-claim architecture**.

---

## 3. Quick start — the CLI

The single entry point is `python -m pacland.tool <command>` (alias `sextant`).

```sh
sextant ingest                        # populate the registries from the built-in assets
sextant search <keyword>              # search every registry
sextant cross <type> <domain>         # cross-field search: match a structure type in other fields
sextant verify <mapping>              # run the transfer encoding-check
sextant synthesize <domain> <type>    # cross-field match + rank by linked knowledge
sextant run [problem]                 # one autonomous loop pass (propose -> falsify -> prove)
sextant prove-lean <theorem>          # churn a Lean proof (local model + kernel check)
sextant benchmark [--live] [--judged] # the G3 discovery benchmark
```

**External data in** (other people's data and libraries):

```sh
sextant ingest-external <file>.json   # structures/properties/evidence/mappings
sextant ingest-library  <file>.py     # the above + executable FALSIFIERS
sextant ingest-lean     <path>        # a Lean repo's theorems -> tier-1 properties
sextant ingest-csv      <file>.csv    # rows -> entries (default evidence)
```

**Lean truths in** (the "bigger library of empirical truths"):

```sh
sextant search-lean  <keyword> [--ingest]   # search local Mathlib (~173k theorems)
sextant harvest-lean "spectral gap,mixing"  # batch-ingest by concept (uses KEYWORD_ALIASES)
sextant scrape-lean  <repo-url>             # clone + scan one Lean repo
sextant scrape-github <query>               # search GitHub for Lean repos + scrape them
```

---

## 4. Environment

The LLM generator and the judge are configured by environment variables (no hardcoded default — an
unset model is a detectable "no model" state, never a silent guess):

```sh
SEXTANT_LLM_ENDPOINT=https://api.deepseek.com/v1   # default http://localhost:11434/v1
SEXTANT_LLM_MODEL=deepseek-chat
SEXTANT_LLM_KEY="$(cat ~/.dsh/deepseek-api-key)"

# the JUDGE must be DISTINCT from the generator (otherwise it grades its own homework):
SEXTANT_JUDGE_ENDPOINT=…  SEXTANT_JUDGE_KEY=…  SEXTANT_JUDGE_MODEL=…
```

The Lean churn loop's model is in `src/pacland/proof_models.py`
(`LEAN_LOCAL_MODEL` / `LEAN_LOCAL_ENDPOINT` — the ROG's Ollama, default the pulled
`hf.co/neopolita/deepseek-prover-v1.5-rl-gguf`).

---

## 5. The Python API

Import with `PYTHONPATH=src` and `from pacland import <module>`.

**`registry`** — the store.
```python
registry.add(Entry(id, kind, payload, provenance, links))   # UPSERT by id (bumps version)
registry.get(kind, id) · registry.query(kind, predicate) · registry.link(a, b)
registry.record_claim(id, statement, status, problem=, assumptions=, test=, reason=)
registry.claims(status) · registry.failed_directions() · registry.known_unknown_disproven()
```

**`ingest`** — population.
```python
ingest.ingest_all()                       # refresh the built-in assets (idempotent, never wipes)
ingest.ingest_external(dict)              # namespaced ext:<source>:<id>, provenance-tracked
ingest.ingest_library(module)             # CONTRIBUTION + FALSIFIERS -> runner.FALSIFIERS
ingest.ingest_lean_repo(path, source)     # theorems -> tier-1 properties
ingest.ingest_csv(path, source, kind)
```

**`runner`** — the loop.
```python
runner.generate(fact_ids, strategy) · runner.run(candidate) · runner.advance(facts, strategy)
runner.run_autonomous(problem, rounds, budget)   # the full propose->falsify->prove pass
runner.prove(lean_code, attempts)                # LLM propose -> kernel check -> repair
runner.FALSIFIERS · runner.FACTS · runner.radar() · runner.rank_open_by_eig()
```

**`challenges`** — the eight-stage gate.
```python
challenges.run_sequence(challenges.Candidate(name=, hypothesis=, falsifier=, assumptions=,
                                             falsifier_result=(survived, evidence)))
challenges.gate(results)   # FAIL / PASS / INCONCLUSIVE
```

**`transfer_verify`** — cross-field verification (specific checker → shared-type checker → honest
"unverified").
```python
transfer_verify.verify_transfer(mapping_id) · transfer_verify.verifiable_mappings()
```

**`novelty`** — the novelty verdict (ends in a WEB SEARCH by us, never a handoff).
```python
novelty.novelty_verdict(frm, to, claim)   # 'known' / 'published' / 'candidate-novel'
novelty.benchmark_novelty(candidates)     # recall vs published vs novel split
```

**`bound_search` + `derived_bounds` + `synthesis_bounds`** — the M3 machinery.
```python
bound_search.referee(beta)                # m(β) = 25.28·e^(−1.182β)
bound_search.check_bound(c)               # positivity/validity/sharpness/reaches_scale
bound_search.search_family(name, make_bound, param_grids)
derived_bounds.evaluate_derived()         # cluster expansion / Dobrushin / asymptotic freedom
synthesis_bounds.run_synthesis()          # lemma -> bound shape -> referee
```

**`supervisor` + `research_state`** — autonomous operation.
```python
supervisor.identify_missing_lemmas() · supervisor.choose_next_frontier() · supervisor.supervisor_report()
rs = research_state.ResearchState(problem).decompose([(id, desc, budget)])
rs.next_task() · rs.record_attempt(id, succeeded, evidence) · rs.should_stop() · rs.save(path) · rs.load(path)
```

**`lean_scrape`** — the truth library.
```python
lean_scrape.count_mathlib_theorems() · lean_scrape.search_mathlib(keyword)
lean_scrape.harvest_mathlib(concepts) · lean_scrape.scrape_github_lean(url)
lean_scrape.search_github_lean_repos(query) · lean_scrape.ingest_mathlib_hits(keyword)
```

**`benchmarks`** — the G3 gate.
```python
benchmarks.run_campaign(campaign, generator) · benchmarks.run_blinded(arms, suite, dataset)
benchmarks.run_paired(generator, dataset)  · benchmarks.run_llm_benchmark(campaign)
benchmarks.gate(results) · benchmarks.falsify_law(expr, points) · benchmarks.run_induction(generator)
```

---

## 6. Conventions a harness MUST follow

1. **IDs are namespaced.** Internal entries use bare slugs (`lean-<name>`, `domain-<x>`); external
   contributions are `ext:<source>:<id>` — an external `darcy-flow` can never overwrite an internal one.
2. **The tier is epistemic, not a score.** 1 established · 2 follows-from-established · 3 conjecture ·
   4 tested-numerically · 5 unknown. A claim is promoted only by a check, never by assertion.
3. **Provenance is mandatory.** Every entry carries `{produced_by, method, ts}` (external ones also
   `source`), so the record is auditable.
4. **A failed direction is a claim, not a dropped log.** Use `registry.record_claim(..., status="failed",
   reason=...)` — SEXTANT must be able to say a direction failed.
5. **The registry is the substrate.** Re-ingesting is idempotent (`add` upserts); never wipe it to
   reseed (that loses accumulated evidence).
6. **A "no model" state is detectable.** Set `SEXTANT_LLM_MODEL` to run the real generator; leave it
   unset and the deterministic/stub paths run instead — never a silent wrong answer.
7. **The novelty verdict ends in a web search by us** (`novelty.novelty_verdict`), not a handoff to
   outside experts.

---

## 7. Workflows

**Give SEXTANT a project's data** (so it's useful on *their* problem):
```sh
sextant ingest-library path/to/project.py     # CONTRIBUTION + FALSIFIERS
```

**Grow the truth library**:
```sh
sextant harvest-lean "spectral gap,mass gap,mixing,decay,entropy"
sextant scrape-github "yang-mills"
```

**Run a discovery pass**:
```sh
sextant run "does lattice Yang-Mills have a mass gap"
```

**Test a candidate mass-gap bound** (the M3 referee):
```python
from pacland import bound_search as bs
bs.check_bound(lambda beta: 25.28 * math.exp(-1.182 * beta))   # the referee survives
bs.check_bound(lambda beta: 1.0)                                # constant -> too big (invalid)
bs.check_bound(lambda beta: math.exp(-beta))                    # generic decay -> too fast
```

**Measure the engine honestly** (cost-aware, blinded, capable baseline):
```sh
SEXTANT_LLM_MODEL=deepseek-chat SEXTANT_LLM_KEY=… sextant benchmark --live
```

**Run autonomously and survive a crash** (durable state):
```python
rs = research_state.ResearchState("ym-mass-gap").decompose([("a", "bound the string tension", 1.0)])
rs.next_task(); rs.record_attempt("a", False, "too weak"); rs.save("state.json")
# later session: rs = research_state.ResearchState.load("state.json")
```

---

## 8. The current M3 frontier (what a mass-gap session should know)

The referee is `m(β) = 25.28·e^(−1.182β)`. The known mechanisms **fail**: cluster expansion (`~ log β`)
is too weak; Dobrushin dies at its ceiling; asymptotic freedom *is* the referee. The synthesis over the
harvested library found the target sits **between** the constant (too big) and `e^(−β)` (too fast) — a
new bound must **track `e^(−1.182β)`**. Test every candidate with `bound_search.check_bound` and record
the outcome with `registry.record_claim`.

---

## 9. Tests

```sh
python3 -m pytest tests -q          # full suite (~1800+ tests)
python3 -m unittest discover -s tests
```

The doc-drift gate (`test_doc_claims`) requires the README/docs test count to match the collected count
— after adding tests, run `scripts/build_site_index.py` and update the quoted count.
