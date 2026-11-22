"""supervisor.py — the supervisory engine (P2): choose the next research frontier.

The supervisor closes the loop between what is known, what is missing, and what has FAILED:
  * identify_missing_lemmas — the proof-tree gaps (sorry/admit) that still need a proof,
  * failed_approaches     — every direction already tried and recorded as failed (the claims),
  * choose_next_frontier  — the top-EIG open problem whose next sub-lemma has NOT already failed,
                            so the engine compounds instead of re-trying a dead direction.

This is the "allocate resources / track failed approaches / choose the next frontier" layer the
autonomous loop was missing: it reads the unified claims (not a stale memory) and the proof tree.
"""
from __future__ import annotations

from pathlib import Path

from pacland import registry


def identify_missing_lemmas(proof_dir: Path | None = None) -> list[str]:
    """Every theorem/lemma in the proof tree still carrying ``sorry``/``admit`` — the missing lemmas.

    A file with a sorry is a named, provable gap — the next thing the prover should target.
    """
    if proof_dir is None:
        from pacland import runner
        proof_dir = runner.PROOF_DIR
    if not proof_dir.exists():
        return []
    import re
    gaps: list[str] = []
    for p in sorted(proof_dir.rglob("*.lean")):
        text = p.read_text(errors="ignore")
        if "sorry" not in text and "admit" not in text:
            continue
        for m in re.finditer(r"^\s*(?:theorem|lemma)\s+([a-zA-Z0-9_']+)", text, re.M):
            gaps.append(f"{m.group(1)} ({p.name})")
    return gaps


def failed_approaches() -> list[dict]:
    """Every research direction already recorded as failed — the claims the supervisor must NOT re-run."""
    return registry.failed_directions()


def _failed_statements() -> set[str]:
    return {c.get("payload", {}).get("statement", "") for c in registry.claims("failed")}


def choose_next_frontier() -> dict:
    """Choose what to investigate next: the top-EIG open problem whose next sub-lemma has NOT failed.

    Returns the problem, its next sub-lemma, and the count of already-failed directions it skipped —
    so the decision is auditable (why this frontier, and what was excluded).
    """
    from pacland import hypotheses, runner

    failed = _failed_statements()
    ranked = runner.rank_open_by_eig()
    skipped = 0
    for name, score in ranked:
        h = hypotheses.HYPOTHESES.get(name, {})
        # walk the decomposition, skipping already-failed sub-lemmas
        for cand in h.get("candidates", []):
            statement = cand.get("hypothesis", "")
            if statement in failed:
                skipped += 1
                continue
            return {
                "problem": name,
                "eig": score,
                "next_sublemma": statement,
                "falsifier": cand.get("falsifier", ""),
                "skipped_failed": skipped,
            }
    # every sub-lemma of every open problem has already failed — the frontier is a new decomposition
    return {"problem": ranked[0][0] if ranked else None, "eig": None, "next_sublemma": None,
            "falsifier": None, "skipped_failed": skipped, "note": "all known sub-lemmas failed — reframe"}


def supervisor_report() -> dict:
    """The consolidated decision record: missing lemmas, failed approaches, and the chosen frontier."""
    return {
        "missing_lemmas": identify_missing_lemmas(),
        "failed_approaches": failed_approaches(),
        "frontier": choose_next_frontier(),
    }
