"""lean_churn.py — the Lean proof churn loop: generate → kernel-check → iterate, offline.

The self-hosted model (DeepSeek-Prover-V1.5) writes a .lean proof attempt; the Lean kernel (`lake env lean`)
checks it for free; on failure the error is fed back to the model to fix. After N local attempts the loop
falls back to the frontier model (DeepSeek-Prover-V2, paid, once). The two tiers never run at the same time.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from pacland import proof_models
from pacland.runner import _ask_llm

PROOF_ROOT = Path(__file__).resolve().parent.parent.parent / "pacland-proof"

_PROMPT = (
    "You are a Lean 4 theorem prover using Mathlib. Write a COMPLETE, compiling Lean 4 theorem with its "
    "proof. Include the necessary imports. Output ONLY the Lean code, no prose.\n\n"
    "Theorem: {theorem}\n\n{failure}"
)


def generate_lean(theorem: str, tier: str, failure: str = "") -> str:
    """Ask the chosen model to write the Lean proof. Returns the code (fenced block extracted)."""
    endpoint, key, model = proof_models.model(tier)
    prompt = _PROMPT.format(theorem=theorem, failure=(f"Previous error:\n{failure}" if failure else ""))
    raw = _ask_llm(prompt, endpoint, key, model)
    m = re.search(r"```lean\s*\n(.*?)```", raw, re.DOTALL)
    return (m.group(1) if m else raw).strip()


def kernel_check(lean_code: str, name: str = "Churn") -> tuple[bool, str]:
    """Write the code into the proof project and run the Lean kernel. Returns (ok, error_tail)."""
    path = PROOF_ROOT / "PaclandProof" / f"{name}.lean"
    path.write_text(lean_code)
    try:
        r = subprocess.run(["lake", "env", "lean", str(path)], cwd=str(PROOF_ROOT),
                           capture_output=True, text=True, timeout=600)
        return r.returncode == 0, (r.stderr or r.stdout or "")[-2500:]
    except subprocess.TimeoutExpired:
        return False, "kernel check timed out"
    finally:
        path.unlink(missing_ok=True)


def churn(theorem: str, max_local: int = 5) -> dict:
    """The loop: generate with the LOCAL model, kernel-check, iterate on the error; on stall, fall back
    to the FRONTIER model once. Returns the verdict + the compiled proof on success."""
    last_err = ""
    for attempt in range(1, max_local + 1):
        code = generate_lean(theorem, "local", last_err)
        ok, err = kernel_check(code)
        if ok:
            return {"proved": True, "tier": "local", "attempts": attempt, "lean": code}
        last_err = err
    # frontier fallback (paid, once)
    code = generate_lean(theorem, "frontier", last_err)
    ok, err = kernel_check(code)
    return {"proved": ok, "tier": "frontier" if ok else "failed",
            "attempts": max_local + 1, "lean": code if ok else "", "error": "" if ok else err}
