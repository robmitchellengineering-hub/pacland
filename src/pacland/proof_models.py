"""proof_models.py — the two Lean-proof models in Sextant (run at different times, never together).

The churn loop uses LOCAL by default (free, self-hosted). On a proof that stalls, it calls FRONTIER once
(paid, the DeepSeek API). They are time-shared, so there is no resource conflict.
"""
from __future__ import annotations

import os
from pathlib import Path

# LOCAL: the self-hosted Lean prover on the ROG's Ollama (free). The GGUF is the only distributable
# form — the raw HF repo is safetensors, not a GGUF. Pulled via:
#   curl http://100.73.60.26:11434/api/pull -d '{"name":"hf.co/neopolita/deepseek-prover-v1.5-rl-gguf"}'
LOCAL = {
    "endpoint": os.environ.get("LEAN_LOCAL_ENDPOINT", "http://100.73.60.26:11434/v1"),
    "model": os.environ.get("LEAN_LOCAL_MODEL", "hf.co/neopolita/deepseek-prover-v1.5-rl-gguf"),
    "key": "",
}

# FRONTIER: DeepSeek-Prover-V2 (671B) via the DeepSeek API — SOTA, paid, on-demand only.
FRONTIER = {
    "endpoint": os.environ.get("LEAN_FRONTIER_ENDPOINT", "https://api.deepseek.com/v1"),
    "model": os.environ.get("LEAN_FRONTIER_MODEL", "deepseek-prover-v2"),
    "key": os.environ.get("LEAN_FRONTIER_KEY", ""),
}


def frontier_key() -> str:
    """The DeepSeek API key (for the paid fallback), read at runtime — never hard-coded."""
    if FRONTIER["key"]:
        return FRONTIER["key"]
    p = Path.home() / ".dsh" / "deepseek-api-key"
    if p.exists():
        return p.read_text().strip()
    return ""


def model(tier: str) -> tuple[str, str, str]:
    """Return (endpoint, key, model) for the chosen tier: 'local' (free) or 'frontier' (paid)."""
    if tier == "frontier":
        return FRONTIER["endpoint"], frontier_key(), FRONTIER["model"]
    return LOCAL["endpoint"], LOCAL["key"], LOCAL["model"]
