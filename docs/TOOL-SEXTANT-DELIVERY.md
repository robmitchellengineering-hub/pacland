# Tool Sextant — the delivery plan (both forms)

> **Live-state note (last verified 2026-11-25).** This file is a snapshot; the two status cells that
> used to read "to build" / "still training" are stale. The truth now:
> - the **supervisor** is built — `src/pacland/supervisor.py` (P2): `identify_missing_lemmas`,
>   `failed_approaches`, `choose_next_frontier`, `supervisor_report`. What remains is the thin daemon
>   wrapper that calls it in a loop, not the decision logic.
> - the **model** is trained and in use — `qwen2.5-discovery`; see `docs/SEXTANT-ASSESSMENT-LOG.md`
>   R1.12 ("the small trained model"). It is small and does not yet propose genuine cross-field links,
>   which is a *limitation*, not a training gate.
> Before trusting any status cell below, read the code / the assessment log — not this table.

The thing being shipped is the **discovery engine** — the whole autonomous loop — as one self-contained
tool, in two delivery forms. This is the plan Rob confirmed ("both is the answer").

## What ships (the bundle, identical in both forms)

| component | what | status |
|---|---|---|
| discovery loop | `runner` / `hypotheses` / `belief` / `challenges` / `benchmarks` (Python) | built |
| falsifiers | SEXTANT + Phantom (`numpy`/`stim`/`quimb`) | built |
| proof engine | Elan + Mathlib + the `.lean` proofs | built (toolchain to bundle) |
| trained LLM | `qwen2.5-discovery` GGUF + llama.cpp/Ollama | **trained + in use** (small — R1.12) |
| supervisor | `supervisor.py` (P2) — the decision layer; the daemon wrapper is the thin remaining piece | **built** |

## The two forms

1. **Container image** — Docker: Python + Lean + Mathlib + llama.cpp + the GGUF + the supervisor, one
   `pull && run` that keeps the loop going and writes discoveries/proofs to a mounted volume.
2. **MorpheOS image** — the same system baked into the OS (`morph-verify` + `rob-quantum` Rust spine +
   the Python loop + the model + Lean), boot-and-run as an appliance.

## Build order

| phase | what | gate |
|---|---|---|
| 1 | the **supervisor daemon** — close the loop end-to-end, one run | it generates, falsifies, and kernel-checks a survivor without a human |
| 2 | the **container** — bundle Python + Lean + Mathlib + llama.cpp + the model | `pull && run` reproduces phase 1 on a clean machine |
| 3 | the **MorpheOS** form — bake the same system into the OS image | boot-and-run reproduces phase 1 |
| 4 | the **model** — ship the trained GGUF | discovery uses the bundled model, no remote call |

## The two hard parts, named

- **Bundling the Lean toolchain** (Elan + Mathlib) into a reproducible image is the heaviest piece — it
  is not pip-installable and Mathlib is large.
- **The thin daemon wrapper** is the remaining code piece: a loop that calls `supervisor.choose_next_frontier`
  → `runner` (generate/falsify/record) → repeat, writing to the knowledge graph. The decision logic is
  built; the wrapper that runs it continuously is not yet.

## The honest dependency

The decision layer (supervisor) and the generator model both exist. What is left is packaging (Lean +
Mathlib into a reproducible image) and the daemon wrapper. The model is small and proposes weak
cross-field links today, but that is a quality issue, not a missing dependency.
