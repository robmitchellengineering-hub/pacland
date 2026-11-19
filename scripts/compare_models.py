"""Compare two self-hosted models (ROG Ollama) on judged recall, judged by deepseek-reasoner.

The ROG is CPU-only, so generation is slow; the generator call uses a long timeout (10 min)
because deepseek-r1:7b emits chain-of-thought.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from pacland import benchmarks as b  # noqa: E402

ROG = "http://100.73.60.26:11434/v1"
PROBLEMS = ["blackbody", "photoelectric", "perihelion"]
MODELS = ["qwen2.5-discovery", "deepseek-r1:7b"]


def _gen(pre: str, model: str) -> list[str]:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": b._PROMPT.format(pre=pre)}]}).encode()
    req = urllib.request.Request(ROG + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        text = json.loads(resp.read())["choices"][0]["message"]["content"]
    return [ln.strip().lstrip("-*•0123456789.) \t")
            for ln in text.splitlines()
            if ln.strip() and not ln.strip().startswith(("#", "//"))]


def main() -> int:
    os.environ["SEXTANT_JUDGE_ENDPOINT"] = "https://api.deepseek.com/v1"
    os.environ["SEXTANT_JUDGE_KEY"] = open(os.path.expanduser("~/.dsh/deepseek-api-key")).read().strip()
    os.environ["SEXTANT_JUDGE_MODEL"] = "deepseek-reasoner"

    for model in MODELS:
        hits = 0
        for p in PROBLEMS:
            d = b.DATASET[p]
            cands = _gen(d["pre"], model)
            m = b.judge_matches(cands, d["jump"])
            hit = any(m)
            hits += int(hit)
            print(f"{model} {p}: {'HIT' if hit else 'MISS'} ({len(cands)} cands) top={cands[:2]!r}", flush=True)
        print(f"{model} RECALL {hits}/{len(PROBLEMS)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
