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
- `fine_tune_peft.py` — **guards verified** (refuses without CUDA); the training itself has **not** been
  run on a GPU.
- `merge_lora.py` + `publish_ollama.sh` — **written, not yet run** (need the GPU + llama.cpp).
