# Tool Sextant — the strategic plan to make it the FULL tool

**The big think:** the full tool is not "more code". It is the **loop closing** — every piece we have
(generator, falsifier, belief, benchmark) is currently a *part*, and the full tool is when they connect
end-to-end and *measure themselves improving*. That is the one thing to build toward.

## What "the full tool" is

A self-contained, autonomous discovery engine that closes this loop, measured by **verified discoveries
per unit of research effort**:

```
radar (find a problem) → generate (hypotheses) → falsify (SEXTANT challenges)
   → promote/record (ledger) → believe (calibration) → learn (memory) → repeat, better
```

The gate is the benchmark (`benchmarks.py`): each addition must **beat the untyped baseline** before the
next is built. Anything that does not improve discoveries-per-effort is not part of the tool.

## Current state (honest)

| Piece | Status |
|---|---|
| SEXTANT (yes/no) + Phantom (falsifiers) | **full** (Python + Rust registry) |
| Discovery loop (runner) + hypothesis registry | **full** (Python) |
| Belief layer (prior → Bayes → EIG → calibration) | **full** (Python) |
| Graded challenge sequence + benchmark harness | **built** (Python) |
| **LLM generator** | **missing** — the "once trained" gate |
| **Radar** (problem discovery) | **missing** |
| **Knowledge graph / discovery memory** | **missing** |
| **Control plane** (budget + orchestration) | **missing** |
| Rust `morph-verify` + `rob-quantum` | **partial** (registry + compute only) — being consolidated |

## The three strategic decisions

1. **Python is the canonical full tool.** The loop lives in Python; do **not** port the discovery engine,
   belief layer, challenges, or benchmarks to Rust until the Python loop *beats a baseline*. Porting now
   is premature (we would be polishing a loop that has not proven itself).

2. **Rust is the embedded OS subset.** `morph-verify` (the yes/no registry) + `rob-quantum` (the compute)
   stay as the OS-baked spine; the full loop runs on top. One spine, two delivery forms — not two engines.

3. **Benchmark-first, vertical slices.** Build one slice, measure it, beat the baseline, then the next.
   Never the 10-subsystem grand design at once.

## The build order

| Phase | What | Gate |
|---|---|---|
| **0 — consolidate (running now)** | unify the 3 Rust worktrees → one `morph-verify` + one `rob-quantum` | no duplicate crates |
| **1 — LLM generator** | plug DeepSeek (`~/.dsh/deepseek-api-key`) or Ollama (`pacland-rog`) into `hypotheses.py`/`runner.py` | the generator produces *novel* candidates, not the knowledge-base recombinations |
| **2 — measure** | run `benchmarks.py` (blind rediscovery) with the LLM generator vs the untyped baseline | beats baseline on recall-per-effort |
| **3 — close the loop** | radar + knowledge graph + discovery memory + control plane, as vertical slices | each slice improves discoveries-per-effort |
| **4 — ship** | the full tool: `sextant-node` downloadable + the Rust spine in MorpheOS | one Tool Sextant, two delivery forms |

## The honest bottom line

We have the *parts* of the full tool; we lack the **closed loop** and the **LLM generator** that would
make it run. The plan is: consolidate (now) → generator → measure → close the loop → ship — each step
gated by the benchmark, so we never claim a discovery engine we have not measured.
