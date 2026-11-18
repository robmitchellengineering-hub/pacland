# The discovery engine — architecture (first-class component)

The engine is `src/pacland/discovery_engine.py`. It is NOT the five jump types; those are ONE search
strategy inside it.

## Design principles

- **Optimize verified discoveries per unit of research effort**, not hypotheses generated. The score is
  `discoveries / total_falsifier_effort`, per strategy and global — a strategy that churns candidates
  with no survivor costs effort and earns nothing.
- **The five jump types do not bound discovery.** They are `conceptual-jump`, one of six strategies. A
  discovery may equally come from an invariant search, a counterexample, a dataset relationship, a
  theory combination, or a missing assumption. The taxonomy *helps generate ideas*; it never dictates
  what is permitted.

## Components

- **Data model** — `Candidate` (hypothesis + strategy + falsifier + cost + prior + status), `Discovery`
  (a candidate that *survived* falsification), `Experiment` (one strategy run on one problem), and the
  `Ledger` (persistent store).
- **Search strategies** (pluggable `Strategy` interface):
  - `conceptual-jump` — the five typed questions (one strategy).
  - `mathematical-search` — surface a proven invariant and test its transfer.
  - `computational-search` — run the live SEXTANT/Phantom falsifiers for a counterexample.
  - `dataset-mining` — correlate ledger candidates by shared falsifier.
  - `theory-combination` — pairwise-combine the catalog's theorems.
  - `proof-gap` — scan the Lean tree for `sorry`/`admit` (real: reads `pacland-proof/`).
- **Falsifier** — SEXTANT (`src/pacland/phantom.py` falsifiers), wired; unknown candidates return `open`
  with a *proposed* falsifier.
- **Scoring** — `score(experiments)` returns `discoveries_per_effort` per strategy and globally.
- **Lifecycle** — `lifecycle(problem, budget)` = plan (all strategies) → run → falsify → score → kill
  (stop-and-reframe when budget exhausts with no survivor).

## Honest status

The architecture, data model, scoring and lifecycle are real and executable (self-test passes; SEXTANT is
wired and the computational + proof-gap strategies run against live artifacts). The strategies are a mix
of real (computational, proof-gap, conceptual-jump) and thin recombinations (mathematical, dataset,
combination) — those are the surfaces to deepen, not the architecture to redo. The LLM-backed generator is
the pluggable next step behind the `Strategy.generate` interface.

## The retrodiction gate (unchanged)

`docs/RETRODICTION-TEST.md` still gates the whole engine: a strategy (or the engine) earns a claim to
"help" only by beating an untyped baseline blind on withheld historical jumps. That is now a test of
**discoveries per effort**, not candidate count.
