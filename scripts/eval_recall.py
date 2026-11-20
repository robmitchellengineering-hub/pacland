"""Evaluate a merged HF model's JUDGED recall on the full benchmark (the metric that matters).

Run on a GPU (fast generation); the judge is deepseek-reasoner (distinct from the generator).
Usage: python3 scripts/eval_recall.py <merged-model-path>
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from pacland import benchmarks as b  # noqa: E402

import torch  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402


def _gen(model, tok, pre: str) -> list[str]:
    prompt = b._PROMPT.format(pre=pre)
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=220, do_sample=True, temperature=0.7)
    text = tok.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return [ln.strip().lstrip("-*•0123456789.) \t")
            for ln in text.splitlines() if ln.strip() and not ln.strip().startswith(("#", "//"))]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: eval_recall.py <merged-model-path>")
        return 2
    path = sys.argv[1]

    os.environ["SEXTANT_JUDGE_ENDPOINT"] = "https://api.deepseek.com/v1"
    os.environ["SEXTANT_JUDGE_KEY"] = open(os.path.expanduser("~/.dsh/deepseek-api-key")).read().strip()
    os.environ["SEXTANT_JUDGE_MODEL"] = "deepseek-reasoner"

    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path, device_map="auto", torch_dtype=torch.float16)
    model.eval()

    hits = 0
    problems = list(b.DATASET.items())
    for name, d in problems:
        cands = _gen(model, tok, d["pre"])
        try:
            match = any(b.judge_matches(cands, d["jump"]))
        except Exception as e:
            match = False
            print(f"{name}: JUDGE ERROR {type(e).__name__}", flush=True)
        hits += int(match)
        print(f"{name}: {'HIT' if match else 'MISS'} ({len(cands)} cands)", flush=True)
    print(f"RECALL {hits}/{len(problems)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
