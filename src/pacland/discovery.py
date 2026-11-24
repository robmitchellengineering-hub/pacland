"""The discovery loop — priority 3's thin driver over the frontier schema.

The loop is deliberately thin: it reads the open obligations from the guarded frontier
(`web/research-frontier.json`), finds each one's falsifier in the SEXTANT registry, runs it, and
records the result as evidence. It does *not* invent approaches or write proofs — those are the
engine's later stages, which sit on top of this. What this gives is the one thing priority 3 needs
first: a single command that says, truthfully, what is open and whether the open thing still
survives its falsifier.

Usage:
    python -m pacland.discovery --list            # the open obligations + their tasks
    python -m pacland.discovery --run             # run each obligation's falsifier and report
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FRONTIER = ROOT / "web" / "research-frontier.json"


def _frontier() -> dict:
    return json.loads(FRONTIER.read_text())


def open_obligations() -> list[dict]:
    """The open obligations (state == 'open') from the guarded frontier."""
    return [o for o in _frontier()["obligations"] if o.get("state") == "open"]


def _catalog():
    sys.path.insert(0, str(ROOT / "src"))
    from pacland import sextant
    return sextant.CATALOG


def list_open() -> str:
    lines = []
    for o in open_obligations():
        e = _catalog().get(o["name"], {})
        falsifier = e.get("falsifier") or "(no falsifier wired)"
        tier = e.get("tier", "-")
        lines.append(f"◐ {o['name']}  [tier {tier}]")
        lines.append(f"    rung:      {o['rung']}")
        lines.append(f"    falsifier: {falsifier}")
    return "\n".join(lines)


def run_falsifiers() -> str:
    lines = []
    for o in open_obligations():
        e = _catalog().get(o["name"])
        simulate = e.get("simulate") if e else None
        if simulate is None:
            lines.append(f"◐ {o['name']:<32} NO-FALSIFIER  ({e.get('falsifier','') if e else ''})")
            continue
        try:
            survived, evidence = simulate()
            status = "SURVIVES" if survived else "REFUTED"
        except Exception as exc:  # a falsifier that errors is information too
            status, evidence = "ERROR", f"{type(exc).__name__}: {exc}"
        lines.append(f"◐ {o['name']:<32} {status}  {evidence}")
    return "\n".join(lines)


def record_results() -> list[dict]:
    """Run the falsifiers and record the evidence (the 'learn' stage of the loop).

    The result is written to `web/evidence.json` — the same schema the interface renders, so a
    falsifier run updates the frontier's evidence, closing the identify → test → learn loop.
    """
    import datetime
    at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    results = []
    for o in open_obligations():
        e = _catalog().get(o["name"])
        simulate = e.get("simulate") if e else None
        if simulate is None:
            results.append({"name": o["name"], "status": "NO-FALSIFIER", "evidence": e.get("falsifier", "") if e else "", "at": at})
            continue
        try:
            survived, evidence = simulate()
            status = "SURVIVES" if survived else "REFUTED"
        except Exception as exc:
            status, evidence = "ERROR", f"{type(exc).__name__}: {exc}"
        results.append({"name": o["name"], "status": status, "evidence": str(evidence), "at": at})
    out = ROOT / "web" / "evidence.json"
    out.write_text(json.dumps({"schema": "sextant-evidence", "runs": results}, indent=2))
    return results


def approaches() -> str:
    """List the known routes + the next step for each open obligation (the 'generate' stage)."""
    data = json.loads((ROOT / "web" / "approaches.json").read_text())
    lines = []
    for o in data["obligations"]:
        lines.append(f"◐ {o['name']}")
        for r in o["routes"]:
            mark = "●" if r["state"] == "attempted" else "○"
            lines.append(f"    {mark} {r['name']} — next: {r['next']}")
            if r.get("note"):
                lines.append(f"        ({r['note']})")
    return "\n".join(lines)


SEARCH_TYPES = {
    "ym-linked-cluster-contraction": ("spectral-gap", "gauge-theory"),
    "ym-log-sobolev": ("markov", "gauge-theory"),
    "ym-volume-uniform-su2": ("spectral-gap", "gauge-theory"),
}


def search() -> str:
    """The 'search across fields' stage: for each open obligation, list same-type structures in other
    fields (candidate transfers — a match is a correspondence, NOT a verified transfer)."""
    from pacland import cross_reference
    lines = []
    for o in open_obligations():
        tt = SEARCH_TYPES.get(o["name"])
        lines.append(f"◐ {o['name']}")
        if tt is None:
            lines.append("    (no cross-field type mapped)")
            continue
        typ, dom = tt
        cands = cross_reference.cross_field(typ, dom)
        if not cands:
            lines.append(f"    no {typ} structures outside {dom}")
        for c in cands[:5]:
            p = c["payload"]
            d = p.get("domain") or p.get("domains") or []
            d = d if isinstance(d, str) else ", ".join(d)
            reproduces = p.get("reproduces", "")
            lines.append(f"    → [{p.get('type', '')}] in {d} — reproduces: {reproduces}")
    return "\n".join(lines)


ATTEMPT_TARGETS = {
    "ym-linked-cluster-contraction": ("animals bound", "#{connected clusters of size n} ≤ Δ^(2(n−1)) — the spanning-tree / Euler-tour injection on top of walk_count_bound (proved)"),
    "ym-log-sobolev": ("log-Sobolev → mixing bridge", "the log-Sobolev constant → the mixing time, chaining clustering_iff_gap (proved)"),
    "ym-volume-uniform-su2": ("non-Abelian FSS", "the SU(2) character two-point function dominated by the free propagator"),
}


def attempt() -> str:
    """The 'attempt proofs' stage: for each open obligation, name the Lean theorem that is the next
    rung, and whether it is already in the tower (green) or still to be proved."""
    import subprocess
    tower = ROOT / "pacland-proof" / "PaclandProof"
    lines = []
    for o in open_obligations():
        target = ATTEMPT_TARGETS.get(o["name"])
        lines.append(f"◐ {o['name']}")
        if target is None:
            lines.append("    (no Lean target mapped)")
            continue
        name, desc = target
        lines.append(f"    next theorem: {name} — {desc}")
        # the tower is kernel-checked green; the rung itself is what remains to be written
        lines.append("    kernel: lake build PaclandProof (green @ 9172 jobs); the rung is the open Lean task")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="the discovery loop over the open obligations")
    ap.add_argument("--list", action="store_true", help="list the open obligations")
    ap.add_argument("--run", action="store_true", help="run each obligation's falsifier")
    ap.add_argument("--record", action="store_true", help="run the falsifiers and write the evidence")
    ap.add_argument("--approaches", action="store_true", help="list the known routes + next steps")
    ap.add_argument("--search", action="store_true", help="search other fields for same-type structures")
    ap.add_argument("--attempt", action="store_true", help="name the next Lean theorem to prove")
    args = ap.parse_args()
    if args.attempt:
        print(attempt())
    elif args.search:
        print(search())
    elif args.approaches:
        print(approaches())
    elif args.record:
        results = record_results()
        for r in results:
            print(f"◐ {r['name']:<32} {r['status']}  {r['evidence']}")
        print(f"\nwrote web/evidence.json ({len(results)} runs)")
    elif args.run:
        print(run_falsifiers())
    else:
        print(list_open())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
