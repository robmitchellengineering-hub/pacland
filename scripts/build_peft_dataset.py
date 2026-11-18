"""Build the PEFT instruction dataset from the benchmark's (pre-state -> jump) pairs.

Converts DATASET + DISGUISED_DATASET + POST_CUTOFF_DATASET + synthetic_suite into an Alpaca-style
instruction dataset that teaches a local LLM the DISCOVERY skill: given a pre-state, propose the
underlying principle/entity and how to falsify it. Output is JSONL, ready for HF TRL ``SFTTrainer``.

This is hardware-independent — it runs now and makes the fine-tune one command away once a GPU exists.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pacland import benchmarks as b  # noqa: E402

INSTRUCTION = (
    "You are a physics discovery engine. Given a pre-state — an observation or anomaly that "
    "existing theory cannot explain — propose the underlying discovery (the new principle or "
    "entity) that resolves it, and state one way your proposal could be falsified."
)


def falsifier_for(jump: str) -> str:
    """A one-line falsifier per jump (the honest 'how would you show this is wrong')."""
    return f"an independent test contradicts {jump}, or {jump} fails to account for the pre-state"


def build(out_path: str = "runs/peft-discovery.jsonl", n_synthetic: int = 200, seed: int = 0) -> int:
    rows: list[dict] = []

    def add(pre: str, jump: str, source: str) -> None:
        rows.append({
            "instruction": INSTRUCTION,
            "input": pre,
            "output": f"Hypothesis: {jump}\nFalsifier: {falsifier_for(jump)}",
            "source": source,
        })

    for d in b.DATASET.values():
        add(d["pre"], d["jump"], "historical")
    for d in b.DISGUISED_DATASET.values():
        add(d["pre"], d["jump"], "disguised")
    for d in b.POST_CUTOFF_DATASET.values():
        add(d["pre"], d["jump"], "post-cutoff")
    for d in b.synthetic_suite(n_synthetic, seed).values():
        add(d["pre"], d["jump"], "synthetic")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} training examples to {out_path}")
    return len(rows)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Build the PEFT discovery instruction dataset")
    ap.add_argument("--out", default="runs/peft-discovery.jsonl")
    ap.add_argument("--n-synthetic", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    n = build(args.out, args.n_synthetic, args.seed)
    print(f"({n} examples)")
