"""The live SEXTANT delivery status — each bundle component checked against the code.

The status table in ``docs/TOOL-SEXTANT-DELIVERY.md`` is a *snapshot*; this module is the live truth.
``live_status()`` checks whether each component's module actually exists on disk, and
``tests/test_delivery_status.py`` fails if the doc asserts a component is "to build" / "still training"
while its code is present — so a stale status cell cannot sit unnoticed.

Regenerate the committed snapshot with ``python3 scripts/build_delivery_status.py``.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

#: component -> the paths whose presence marks it "built". A component is built when ALL its
#: marker paths exist (so a missing half-finished module is reported, not silently passed).
COMPONENTS: dict[str, list[str]] = {
    "discovery-loop": [
        "src/pacland/runner.py",
        "src/pacland/hypotheses.py",
        "src/pacland/belief.py",
        "src/pacland/challenges.py",
        "src/pacland/benchmarks.py",
    ],
    "falsifiers": [
        "src/pacland/sextant.py",
        "src/pacland/phantom.py",
    ],
    "proof-engine": [
        "pacland-proof/PaclandProof/QM/BakryEmery.lean",
    ],
    "knowledge-graph": [
        "src/pacland/discovery_graph.py",
    ],
    "supervisor": [
        "src/pacland/supervisor.py",
    ],
    "model-wired": [
        "src/pacland/benchmarks.py",  # _llm_config reads SEXTANT_LLM_MODEL (qwen2.5-discovery)
    ],
}


def live_status() -> dict:
    """The live status: component -> {built, present, missing}."""
    out: dict = {}
    for component, paths in COMPONENTS.items():
        present = [p for p in paths if (REPO / p).exists()]
        missing = [p for p in paths if p not in present]
        out[component] = {
            "built": not missing,
            "present": present,
            "missing": missing,
        }
    return out
