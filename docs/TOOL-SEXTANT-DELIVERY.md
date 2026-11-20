# Tool Sextant — the delivery plan (both forms)

The thing being shipped is the **discovery engine** — the whole autonomous loop — as one self-contained
tool, in two delivery forms. This is the plan Rob confirmed ("both is the answer").

## What ships (the bundle, identical in both forms)

| component | what | status |
|---|---|---|
| discovery loop | `runner` / `hypotheses` / `belief` / `challenges` / `benchmarks` (Python) | built |
| falsifiers | SEXTANT + Phantom (`numpy`/`stim`/`quimb`) | built |
| proof engine | Elan + Mathlib + the 107 `.lean` proofs | built (toolchain to bundle) |
| trained LLM | `qwen2.5-discovery` GGUF + llama.cpp/Ollama | **training not finished** — the gate |
| supervisor | a daemon that runs the loop autonomously (radar→generate→falsify→prove→record→learn→repeat) | **to build** |

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
| 4 | the **model** — drop the trained GGUF in when training finishes | discovery uses the bundled model, no remote call |

## The two hard parts, named

- **Bundling the Lean toolchain** (Elan + Mathlib) into a reproducible image is the heaviest piece — it
  is not pip-installable and Mathlib is large.
- **The trained model** is the schedule gate: until training finishes, the bundle ships with the loop +
  falsifiers + prover, and the generator runs on whatever model is present; the trained GGUF drops in at
  phase 4 without a rebuild.

## The honest dependency

The whole thing can be built *except* the trained model, which is still training. Phases 1–3 do not wait
on it; phase 4 is a drop-in. So the build can start now and the model lands when it lands.
