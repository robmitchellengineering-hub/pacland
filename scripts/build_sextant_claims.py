#!/usr/bin/env python3
"""build_sextant_claims.py — generate web/sextant-claims.json from the live theorem registry.

The page fetches `sextant-claims.json`, so it is a live view of the discovery system, not an
embedded copy. The source of truth is `src/pacland/sextant.py`'s CATALOG (claim, theorem,
falsifier, oracle, verdict); the hand-maintained explanatory prose (plain, ev, dont) and the
category/field maps live in `web/sextant-prose.json`. This script merges the two into one data
file the page loads, and refuses to emit if the ids/verdicts drift or a claim is missing prose.

Exit 0 = generated · 1 = drift / missing prose · 2 = could not parse.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def catalog(path: Path) -> dict:
    """Parse the CATALOG (id -> claim/theorem/falsifier/oracle/verdict) from sextant.py."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"CATALOG: dict\[str, dict\] = \{(.*?)\n\}", text, re.S)
    if not m:
        print(f"build_sextant_claims: could not find CATALOG in {path}", file=sys.stderr)
        raise SystemExit(2)
    body = m.group(1)
    out = {}
    for idm in re.finditer(r'"([a-z0-9-]+)":\s*\{', body):
        cid = idm.group(1)
        tail = body[idm.end():]
        # a claim's block runs to the next top-level "key": { at the same indent
        nxt = re.search(r'\n    "[a-z0-9-]+":\s*\{|\n\}', tail)
        block = tail[:nxt.start()] if nxt else tail
        def field(name):
            fm = re.search(rf'"{name}":\s*"((?:[^"\\]|\\.)*)"', block, re.S)
            return fm.group(1) if fm else ""
        out[cid] = {
            "claim": field("claim"),
            "theorem": field("theorem"),
            "falsifier": field("falsifier"),
            "oracle": re.findall(r'"([^"]+)"', re.search(r'"oracle":\s*\[(.*?)\]', block, re.S).group(1)) if re.search(r'"oracle":\s*\[', block) else [],
            "verdict": field("verdict"),
        }
    return out


def main() -> int:
    reg = catalog(ROOT / "src" / "pacland" / "sextant.py")
    prose_path = ROOT / "web" / "sextant-prose.json"
    if not prose_path.exists():
        print("build_sextant_claims: web/sextant-prose.json is missing", file=sys.stderr)
        return 2
    prose = json.loads(prose_path.read_text(encoding="utf-8"))

    problems = []
    claims = []
    for cid in sorted(reg):
        c = reg[cid]
        p = prose.get("prose", {}).get(cid)
        if p is None or not p.get("plain") or not p.get("ev"):
            problems.append(f"claim {cid!r} has no prose (plain/ev) in sextant-prose.json")
            continue
        claims.append({
            "id": cid,
            "v": c["verdict"],
            "th": c["theorem"],
            "claim": c["claim"],
            "falsifier": c["falsifier"],
            "oracle": " + ".join(c["oracle"]) if c["oracle"] else "",
            "ev": p["ev"],
            "plain": p["plain"],
            "dont": p.get("dont", ""),
        })
    # a claim in the prose but not the registry is also drift
    for cid in sorted(prose.get("prose", {})):
        if cid not in reg:
            problems.append(f"prose has claim {cid!r} that is not in the registry")

    if problems:
        for p in problems:
            print(f"DRIFT  {p}")
        return 1

    import datetime
    out = {
        "generated": datetime.date.today().isoformat(),
        "claims": claims,
        "cat": prose.get("cat", {}),
        "cats": prose.get("cats", {}),
        "fields": prose.get("fields", []),
    }
    out_path = ROOT / "web" / "sextant-claims.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"build_sextant_claims: wrote web/sextant-claims.json — {len(claims)} claims, {len(out['cats'])} categories, {len(out['fields'])} fields (from the live CATALOG + prose)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
