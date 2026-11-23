"""The churn-loop driver: feed each sorry-target to the LLM prover + kernel-check, up to `attempts`.

Run on the ROG where the model and the cached lake build both live:

    SEXTANT_LLM_MODEL=hf.co/neopolita/deepseek-prover-v1.5-rl-gguf:latest \
    SEXTANT_LLM_ENDPOINT=http://localhost:11434/v1 \
    python3 scripts/churn_driver.py scripts/churn_targets.lean

For each `theorem … := by sorry` in the file, it calls `runner.prove` (propose → `lake env lean` →
refuse `sorry` → repair) and reports the result. A proven theorem is saved into the proof tower.
"""
import json
import os
import re
import sys

sys.path.insert(0, "src")
from pacland import runner  # noqa: E402


def split_theorems(text: str) -> list[str]:
    """Split a Lean file into (header, theorem blocks) so each `theorem` is a complete file."""
    blocks = []
    header_lines = []
    theorem_lines = []
    in_theorem = False
    for line in text.splitlines():
        if re.match(r"^(theorem|lemma)\s", line):
            if theorem_lines:
                blocks.append("\n".join(header_lines + theorem_lines))
                theorem_lines = []
            in_theorem = True
        elif line.strip() == "end ChurnTargets" and in_theorem:
            theorem_lines.append(line)
            blocks.append("\n".join(header_lines + theorem_lines))
            theorem_lines = []
            in_theorem = False
            continue
        if in_theorem:
            theorem_lines.append(line)
        else:
            header_lines.append(line)
    return blocks


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "scripts/churn_targets.lean"
    attempts = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    text = open(path, encoding="utf-8").read()
    blocks = split_theorems(text)
    print(f"== {len(blocks)} target(s) from {path} — model={os.environ.get('SEXTANT_LLM_MODEL', '(unset)')} ==\n")
    for i, block in enumerate(blocks, 1):
        name = re.search(r"^(?:theorem|lemma)\s+(\w+)", block, re.M)
        label = name.group(1) if name else f"block-{i}"
        r = runner.prove(block, attempts=attempts, save=f"pacland-proof/PaclandProof/QM/Churn_{label}.lean")
        if r.get("ok"):
            print(f"[{label}] PROVED in {r['attempts']} attempt(s) — saved to {r.get('saved')}")
        else:
            err = r.get("last_error") or r.get("error") or "?"
            print(f"[{label}] NOT proved in {r.get('attempts', attempts)} attempt(s): {str(err)[:600]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
