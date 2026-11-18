#!/usr/bin/env bash
# One-shot smoke run on the rented GPU: prove the whole path trains and merges before the full run.
# Usage: bash scripts/smoke_finetune.sh
set -euo pipefail

echo "== install deps =="
pip install -q torch transformers peft trl bitsandbytes datasets accelerate

echo "== build the dataset =="
python3 scripts/build_peft_dataset.py --out runs/peft-discovery.jsonl --n-synthetic 50

echo "== smoke fine-tune (a few steps) =="
python3 scripts/fine_tune_peft.py --model Qwen/Qwen2.5-7B --data runs/peft-discovery.jsonl \
  --out runs/peft-adapter-smoke --epochs 0.05 --lora-r 8

echo "== merge =="
python3 scripts/merge_lora.py --base Qwen/Qwen2.5-7B --adapter runs/peft-adapter-smoke --out runs/peft-merged-smoke

echo "SMOKE RUN OK — the fine-tune + merge path works end-to-end."
echo "Next: the full run is the same commands with --epochs 3 and --lora-r 16."
