"""Fine-tune a local LLM on the discovery skill with QLoRA (HuggingFace PEFT + TRL).

HONEST NOTE: the ROG (GTX 960M, 4GB VRAM, Maxwell, no working NVIDIA driver) CANNOT run this — it
needs a CUDA GPU with >= 8GB VRAM (16GB is comfortable for a 7B). Run it on a rented GPU (the accepted
exception) or future hardware:

    pip install torch transformers peft trl bitsandbytes datasets accelerate
    python3 scripts/build_peft_dataset.py                # produces runs/peft-discovery.jsonl
    python3 scripts/fine_tune_peft.py --model Qwen/Qwen2.5-7B --data runs/peft-discovery.jsonl

The fine-tuned adapter is then loaded by the local Ollama/transformers as the discovery specialist.
"""
from __future__ import annotations

import argparse


def main() -> int:
    ap = argparse.ArgumentParser(description="QLoRA fine-tune of a local LLM on the discovery skill")
    ap.add_argument("--model", default="Qwen/Qwen2.5-7B")
    ap.add_argument("--data", default="runs/peft-discovery.jsonl")
    ap.add_argument("--out", default="runs/peft-adapter")
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--lora-r", type=int, default=16)
    args = ap.parse_args()

    try:
        import torch
        from datasets import load_dataset
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
        from trl import SFTTrainer
    except ImportError as e:
        print(f"missing dependency: {e.name if hasattr(e, 'name') else e}")
        print("install: pip install torch transformers peft trl bitsandbytes datasets accelerate")
        return 2

    if not torch.cuda.is_available():
        print("no CUDA GPU — this fine-tune needs a CUDA GPU (>= 8GB VRAM); see the header note")
        return 1

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForCausalLM.from_pretrained(args.model, quantization_config=bnb,
                                                 device_map="auto")
    model = prepare_model_for_kbit_training(model)
    peft_cfg = LoraConfig(r=args.lora_r, lora_alpha=32, lora_dropout=0.05, bias="none",
                          task_type="CAUSAL_LM")
    model = get_peft_model(model, peft_cfg)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    data = load_dataset("json", data_files=args.data)["train"]

    def fmt(example):
        return {"text": f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}"
                        f"\n\n### Response:\n{example['output']}"}

    data = data.map(fmt)

    train_args = TrainingArguments(
        output_dir=args.out, per_device_train_batch_size=2, gradient_accumulation_steps=8,
        num_train_epochs=args.epochs, learning_rate=2e-4, fp16=True, logging_steps=10,
        save_strategy="epoch", report_to="none",
    )
    # Newer TRL: max_seq_length is not a SFTTrainer kwarg — it is dropped (the prompt+output fit the
    # default window); set it via SFTConfig if a longer sequence is ever needed.
    trainer = SFTTrainer(model=model, train_dataset=data, args=train_args,
                         processing_class=tokenizer)
    trainer.train()
    model.save_pretrained(args.out)
    tokenizer.save_pretrained(args.out)
    print(f"adapter saved to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
