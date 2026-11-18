"""Merge a LoRA/QLoRA adapter back into its base model (full fine-tuned checkpoint).

The fine-tune (``fine_tune_peft.py``) produces an adapter, not a runnable model. This merges it with
the base weights so the result is a self-contained HF model, ready for GGUF conversion.

Run on the rented GPU, after fine_tune_peft.py:
    python3 scripts/merge_lora.py --base Qwen/Qwen2.5-7B --adapter runs/peft-adapter --out runs/peft-merged
"""
from __future__ import annotations

import argparse


def main() -> int:
    ap = argparse.ArgumentParser(description="Merge a LoRA adapter into its base model")
    ap.add_argument("--base", default="Qwen/Qwen2.5-7B")
    ap.add_argument("--adapter", default="runs/peft-adapter")
    ap.add_argument("--out", default="runs/peft-merged")
    args = ap.parse_args()

    try:
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as e:
        print(f"missing dependency: {e.name if hasattr(e, 'name') else e}")
        print("install: pip install peft transformers torch")
        return 2

    base = AutoModelForCausalLM.from_pretrained(args.base)
    model = PeftModel.from_pretrained(base, args.adapter)
    model = model.merge_and_unload()
    model.save_pretrained(args.out)
    tokenizer = AutoTokenizer.from_pretrained(args.base)
    tokenizer.save_pretrained(args.out)
    print(f"merged model saved to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
