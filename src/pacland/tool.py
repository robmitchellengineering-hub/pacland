"""tool.py — the unified Sextant CLI: ingest, search, cross-reference, verify, run.

One entry point for the whole discovery engine:

    python -m pacland.tool ingest                  # populate the registries from the real assets
    python -m pacland.tool cross <type> <domain>   # cross-field search (type match in OTHER fields)
    python -m pacland.tool verify <mapping>        # run the transfer encoding-check
    python -m pacland.tool search <keyword>        # search every registry
    python -m pacland.tool run [problem]           # one autonomous loop pass
"""
from __future__ import annotations

import argparse
import json
import sys


def _cmd_ingest(_: argparse.Namespace) -> int:
    from pacland import ingest, registry
    counts = ingest.ingest_all()
    print(json.dumps({**counts, "totals": {k: len(registry.query(k, lambda d: True))
                                           for k in registry.KINDS}}, indent=2))
    return 0


def _cmd_cross(a: argparse.Namespace) -> int:
    from pacland import ingest, cross_reference
    ingest.ingest_all()
    for t in cross_reference.propose_transfers({"type": a.type, "domain": a.domain}):
        print(f"{t['from_structure']:24s} ({t['from_domain']:12s}) → {t['reproduces'][:60]}")
    return 0


def _cmd_verify(a: argparse.Namespace) -> int:
    from pacland import ingest, transfer_verify
    ingest.ingest_all()
    v = transfer_verify.verify_transfer(a.mapping)
    print(json.dumps(v, indent=2))
    return 0


def _cmd_synthesize(a: argparse.Namespace) -> int:
    from pacland import ingest, synthesize
    ingest.ingest_all()
    for s in synthesize.synthesize(a.domain, a.type):
        print(f"{s['from_structure']:24s} ({s['from_domain']:12s}) | {s['linked_theorems']:3d} thms "
              f"| {s['candidate_yield']}")
    return 0


def _cmd_prove_lean(a: argparse.Namespace) -> int:
    from pacland import lean_churn
    r = lean_churn.churn(a.theorem, max_local=a.max_local)
    print(json.dumps(r, indent=2))
    return 0


def _cmd_search(a: argparse.Namespace) -> int:
    from pacland import registry
    kw = a.keyword.lower()
    for kind in registry.KINDS:
        hits = registry.query(kind, lambda d, kw=kw: kw in json.dumps(d).lower())
        if hits:
            print(f"--- {kind} ({len(hits)}) ---")
            for h in hits[:a.limit]:
                print(" ", h["id"], "|", json.dumps(h["payload"])[:100])
    return 0


def _cmd_run(a: argparse.Namespace) -> int:
    from pacland.runner import run_autonomous
    out = run_autonomous(problem=a.problem, rounds=a.rounds, budget=a.budget)
    print(json.dumps({"problem": out["problem"], "run_id": out["run_id"],
                      "survivors": sum(len(r["survivors"]) for r in out["rounds"]),
                      "falsified": sum(len(r["proposals"]) for r in out["rounds"]),
                      "open": sum(len(r["open"]) for r in out["rounds"])}, indent=2))
    return 0


def _cmd_ingest_external(a: argparse.Namespace) -> int:
    from pacland import ingest
    from pathlib import Path
    p = Path(a.file)
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 1
    data = json.loads(p.read_text(encoding="utf-8"))
    counts = ingest.ingest_external(data)
    print(json.dumps({"source": data.get("source"), **counts}, indent=2))
    return 0


def _cmd_ingest_library(a: argparse.Namespace) -> int:
    from pacland import ingest
    mod = ingest.load_module_from_path(a.path)
    out = ingest.ingest_library(mod)
    print(json.dumps(out, indent=2, default=str))
    return 0


def _cmd_ingest_lean(a: argparse.Namespace) -> int:
    from pacland import ingest
    out = ingest.ingest_lean_repo(a.path, source=a.source)
    print(json.dumps(out, indent=2))
    return 0


def _cmd_ingest_csv(a: argparse.Namespace) -> int:
    from pacland import ingest
    out = ingest.ingest_csv(a.path, source=a.source, kind=a.kind)
    print(json.dumps(out, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="sextant", description="the Sextant discovery engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ingest", help="populate the registries from the real assets")
    p.set_defaults(fn=_cmd_ingest)

    p = sub.add_parser("cross", help="cross-field search: match a type in other fields")
    p.add_argument("type")
    p.add_argument("domain")
    p.set_defaults(fn=_cmd_cross)

    p = sub.add_parser("verify", help="run the transfer encoding-check")
    p.add_argument("mapping", nargs="?", default="heat-diffusion-walk")
    p.set_defaults(fn=_cmd_verify)

    p = sub.add_parser("synthesize", help="cross-field discovery: match a type + rank by linked knowledge")
    p.add_argument("domain")
    p.add_argument("type")
    p.set_defaults(fn=_cmd_synthesize)

    p = sub.add_parser("prove-lean", help="churn a Lean proof: local model + kernel check, frontier fallback")
    p.add_argument("theorem")
    p.add_argument("--max-local", type=int, default=5)
    p.set_defaults(fn=_cmd_prove_lean)

    p = sub.add_parser("search", help="search every registry for a keyword")
    p.add_argument("keyword")
    p.add_argument("--limit", type=int, default=5)
    p.set_defaults(fn=_cmd_search)

    p = sub.add_parser("run", help="one autonomous loop pass")
    p.add_argument("problem", nargs="?")
    p.add_argument("--rounds", type=int, default=1)
    p.add_argument("--budget", type=int, default=4)
    p.set_defaults(fn=_cmd_run)

    p = sub.add_parser("ingest-external", help="ingest another project's data (structures/properties/evidence/mappings) from a JSON file")
    p.add_argument("file", help="path to the contribution JSON (see examples/external-contribution.json)")
    p.set_defaults(fn=_cmd_ingest_external)

    p = sub.add_parser("ingest-library", help="register an external Python library (its CONTRIBUTION data + FALSIFIERS)")
    p.add_argument("path", help="path to the .py library module")
    p.set_defaults(fn=_cmd_ingest_library)

    p = sub.add_parser("ingest-lean", help="ingest an external Lean repo's theorems as tier-1 properties")
    p.add_argument("path", help="path to the Lean repo / directory of .lean files")
    p.add_argument("--source", default="", help="the contributor slug (defaults to the directory name)")
    p.set_defaults(fn=_cmd_ingest_lean)

    p = sub.add_parser("ingest-csv", help="ingest a CSV — each row becomes an entry (default evidence)")
    p.add_argument("path", help="path to the .csv file")
    p.add_argument("--source", default="", help="the contributor slug (defaults to the filename)")
    p.add_argument("--kind", default="evidence", help="the registry kind for each row (default evidence)")
    p.set_defaults(fn=_cmd_ingest_csv)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
