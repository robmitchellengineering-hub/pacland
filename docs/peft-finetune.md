# Fine-tuning the local discovery model — the full path

The plan is to fine-tune the self-hosted LLM (`qwen2.5:7b` on `pacland-rog`) on the discovery skill, so
it runs the discovery loop unattended without DeepSeek. The front half (data → fine-tune) is built; this
documents the whole path including the back half (merge → GGUF → Ollama).

## 0. Hardware

A QLoRA fine-tune of a 7B needs a CUDA GPU with ≥ 8 GB VRAM (16–24 GB comfortable). The ROG's GTX 960M
(4 GB, Maxwell) cannot run it. Cheapest rental: **Vast.ai spot RTX 3090** (24 GB) at ~$0.10–0.15/hr; our
223-example, 3-epoch run is ~1–2 hours → well under $1.

## 1. Build the training data (local, no GPU)

```
python3 scripts/build_peft_dataset.py --out runs/peft-discovery.jsonl
```

223 examples (historical + disguised + post-cutoff + 200 planted-law).

## 2. Fine-tune (rented GPU)

```
pip install torch transformers peft trl bitsandbytes datasets accelerate
python3 scripts/fine_tune_peft.py --model Qwen/Qwen2.5-7B --data runs/peft-discovery.jsonl --out runs/peft-adapter
```

This produces a **LoRA adapter** (small), not a runnable model.

## 3. Merge the adapter back into the base (rented GPU)

```
python3 scripts/merge_lora.py --base Qwen/Qwen2.5-7B --adapter runs/peft-adapter --out runs/peft-merged
```

## 4. Convert to GGUF, quantize, import into Ollama (any machine with llama.cpp + ollama)

```
bash scripts/publish_ollama.sh runs/peft-merged qwen2.5-discovery
```

Then the ROG serves it:
```
ollama run qwen2.5-discovery
```

## 5. Point the discovery engine at it

```
SEXTANT_LLM_ENDPOINT=http://100.73.60.26:11434/v1 SEXTANT_LLM_MODEL=qwen2.5-discovery \
  python3 -m pacland.runner --autonomous "the mass gap"
```

## Honest status

- `build_peft_dataset.py` — **verified** (runs, 223 examples).
- `fine_tune_peft.py` — **verified on a rented 3090** (trains, saves, merges); the five API/version bugs found live are fixed.
- `merge_lora.py` + `publish_ollama.sh` — **verified** (full run produced `qwen2.5-discovery`, recall 1/1 on blackbody).

## Later — expand Mathlib with our physics Lean proofs (deferred)

Mathlib has only a thin `Physics/` dir (relativity + basic QM). Our `pacland-proof/` tree already formalises
real QM results (Born rule, Tsirelson, Gaussian-LSI) that Mathlib lacks. Two later steps, deliberately not
done now:

1. **Contribute our physics Lean proofs upstream to Mathlib** (or a physics sub-project), so the formalised
   physics corpus grows for everyone.
2. **Use them + Mathlib.Physics + ProofNet as physics-specific formalizer training data** — today the
   formalizer skill is only 25 generated examples; this is the real source for a serious formalizer tune.

For now the training stays **physics-specific**: discovery data is ours, the falsifier skill is generated
(there is no public physics-falsifier corpus), and the Lean skill is the small generated set until the
Mathlib-expansion step above.

