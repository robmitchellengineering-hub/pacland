# The discovery engine — architecture and state

The engine is `src/pacland/runner.py` (the `DiscoveryEngine` class). It is an **automated frontier
discovery-and-proof machine**: propose → falsify → challenge → prove → record → acquire, runnable
unattended, with DeepSeek as the fallback for the harder steps.

## The loop (all wired, all on main)

| stage | mechanism |
|---|---|
| propose | `LlmSearch` (LLM proposes `HYPOTHESIS | FALSIFIER`) + six catalog strategies |
| falsify | SEXTANT falsifiers + keyword routing + **3-state** (survived / refuted / unresolved) |
| challenge | the eight-stage SEXTANT sequence (`challenges.run_sequence`) on every candidate |
| prove | `prove_and_record` — persist the survivor, formalise to Lean, kernel-check, repair |
| record | survivors → `runs/discoveries.jsonl`; every run → `runs/experiments.jsonl` (registry) |
| acquire | `falsifier_acquisition.acquire` — search codebase / Lean tree / arXiv, then synthesize |
| build | `build_and_run_falsifier` — turn the synthesized falsifier into an executable test, **validate it**, run it, retry |

## Honesty guards (the falsifier is the unit of honesty)

- `verify_mass_gap_scaling` no longer returns success unconditionally — the asymptotic-freedom
  candidate is the referee itself (`m(β)=25.28·e^{-1.182β}`), flagged **REFEREE IDENTITY**, not a survivor.
- Keyword routing is **APPROXIMATE** (`survived=None`) — a hypothesis routed to a *related* falsifier
  stays OPEN until a candidate-specific test is built.
- `validate_falsifier` rejects a synthesized falsifier that cannot branch or does not reference the
  claim — a constant `return True` is rejected before it runs.
- `_lean_matches_hypothesis` protects the Lean bridge — a proof of a different/weaker proposition is
  rejected, not recorded.
- `challenges` no longer passes vacuously: `known-results` is NOT_APPLICABLE without a catalog match,
  and `formal-verification` runs `lake env lean` (a comment cannot fake a kernel check).

## Measured performance (live, DeepSeek, 2026-11-18)

Independent decontaminated baselines (`measure_independent`, judged):

| suite | recall | baseline |
|---|---|---|
| synthetic (planted-law, seed 0) | **0.80** | 0.00 |
| disguised (isomorphic vocabulary) | **0.90** | 0.10 |
| post-cutoff (recent resolutions) | **0.67** | 0.00 |

These are problems the model cannot have memorised, so recall here is induction, not memorisation.

## The local-LLM path (PEFT)

The plan is to fine-tune the self-hosted LLM (qwen2.5:7b on `pacland-rog`) so it runs the loop without
DeepSeek. The pipeline is built:

- `scripts/build_peft_dataset.py` — benchmark pairs → Alpaca instruction dataset (223 examples).
- `scripts/fine_tune_peft.py` — QLoRA (PEFT + TRL) fine-tune script.

**Hardware finding:** `pacland-rog` is a GTX 960M (4 GB VRAM, Maxwell, no working NVIDIA driver) — it
**cannot** run a 7B QLoRA fine-tune (needs ≥ 8 GB CUDA, 16 GB comfortable). Options: a small (1–3B)
model on CPU (very slow), online GPU rental (the accepted exception), or keep DeepSeek for the hard
steps. The dataset + script make the fine-tune one command away once a GPU exists.
