"""Generate the falsifier-skill and Lean-skill training examples with DeepSeek.

The first fine-tune only taught "pre-state -> hypothesis + generic falsifier". The loop also needs
"hypothesis -> SPECIFIC falsifier" and "-> Lean theorem", so this adds those skills to the training set.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pacland import benchmarks as b  # noqa: E402

FALSIFIER_INSTRUCTION = (
    "You are a physics falsifier designer. Given a hypothesis, write the SINGLE most decisive "
    "measurement or theorem that would REFUTE it (the sentence that, if true, makes the hypothesis "
    "wrong). One sentence only."
)
LEAN_INSTRUCTION = (
    "You are a Lean 4 formalizer. Formalize the hypothesis below as a Mathlib Lean 4 theorem "
    "declaration (imports + theorem statement with a `sorry` for the proof). Output ONLY Lean code."
)


def _hypotheses() -> list[str]:
    hs = []
    for src in (b.DATASET, b.DISGUISED_DATASET, b.POST_CUTOFF_DATASET):
        hs += [d["jump"] for d in src.values()]
    hs += [d["jump"] for d in b.synthetic_suite(60).values()]
    return hs


def main() -> int:
    endpoint = os.environ.get("SEXTANT_LLM_ENDPOINT", "https://api.deepseek.com/v1")
    key = os.environ.get("SEXTANT_LLM_KEY", "")
    model = os.environ.get("SEXTANT_LLM_MODEL", "deepseek-chat")
    if not model:
        print("set SEXTANT_LLM_MODEL (and SEXTANT_LLM_KEY) to generate the skill data")
        return 1

    hs = _hypotheses()
    rows = []
    # falsifier skill (the loop's falsify step)
    for h in hs[:70]:
        out = b._ask_llm(FALSIFIER_INSTRUCTION + "\n\nHypothesis: " + h, endpoint, key, model)
        rows.append({"instruction": FALSIFIER_INSTRUCTION, "input": h,
                     "output": out.strip(), "source": "falsifier-skill"})
    # Lean formalizer skill (the loop's prove step)
    for h in hs[:25]:
        out = b._ask_llm(LEAN_INSTRUCTION + "\n\nHypothesis: " + h, endpoint, key, model)
        rows.append({"instruction": LEAN_INSTRUCTION, "input": h,
                     "output": out.strip(), "source": "lean-skill"})

    Path("runs/peft-skills.jsonl").parent.mkdir(parents=True, exist_ok=True)
    with open("runs/peft-skills.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} skill examples to runs/peft-skills.jsonl "
          f"({sum(1 for r in rows if r['source']=='falsifier-skill')} falsifier, "
          f"{sum(1 for r in rows if r['source']=='lean-skill')} lean)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
