"""SEXTANT — the yes/no engine (question -> simulate -> classify -> certificate).

Two layers, per PLAN-sextant-proof-engine.md:
  * **Phantom** (``phantom.py``) is the simulated-quantum substrate (Stim / Quimb /
    QuEST): it *computes* the number.
  * **SEXTANT** (``engine.py``) is the classifier: it reads the claim registry and
    emits FORCED / FREE / IMPOSSIBLE.

A claim's verdict comes from the registry, never from a guess; a claim that needs a
number is computed by Phantom and the number is quoted, never recalled.
"""
from .engine import run, classify
from .registry import Claim, CLAIMS, FORCED, FREE, IMPOSSIBLE

__all__ = ["run", "classify", "Claim", "CLAIMS", "FORCED", "FREE", "IMPOSSIBLE"]
