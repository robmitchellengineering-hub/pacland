#!/usr/bin/env python3
"""build_sextant_claims.py — keep web/sextant.html in sync with the theorem registry.

The page's claim list is a hard-coded JS snapshot of `src/pacland/sextant.py`'s CATALOG
(the theorem registry). This guard parses BOTH and reports drift: a claim id that is in the
registry but missing from the page (or vice-versa), or a verdict that has changed. It is the
mechanical half of "the page reflects the live registry" — the plain-language prose is still
hand-maintained, but the ids and verdicts must match.

Exit 0 = in sync · 1 = drift · 2 = could not parse.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def catalog_ids(path: Path) -> dict:
    """Parse the CATALOG keys + verdicts from src/pacland/sextant.py (regex, no import)."""
    text = path.read_text(encoding="utf-8")
    catalog = {}
    # the CATALOG starts at 'CATALOG: dict[str, dict] = {' and runs to the matching '}'
    m = re.search(r"CATALOG: dict\[str, dict\] = \{(.*?)\n\}", text, re.S)
    if not m:
        raise SystemExit(f"could not find CATALOG in {path}")
    body = m.group(1)
    for idm in re.finditer(r'"([a-z0-9-]+)":\s*\{', body):
        cid = idm.group(1)
        # the verdict is the first '"verdict": "..."' after this id's block
        tail = body[idm.end():]
        vm = re.search(r'"verdict":\s*"([A-Z]+)"', tail)
        catalog[cid] = vm.group(1) if vm else "?"
    return catalog


def page_ids(path: Path) -> dict:
    """Parse the CLAIMS ids + verdicts from web/sextant.html (regex, no JS eval)."""
    text = path.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"\{ id:'([a-z0-9-]+)', v:'([A-Z]+)'", text):
        out[m.group(1)] = m.group(2)
    return out


def main() -> int:
    reg = catalog_ids(ROOT / "src" / "pacland" / "sextant.py")
    page = page_ids(ROOT / "web" / "sextant.html")
    problems = []
    for cid in sorted(reg):
        if cid not in page:
            problems.append(f"registry claim {cid!r} is missing from the page")
        elif reg[cid] != page[cid]:
            problems.append(f"claim {cid!r}: registry verdict {reg[cid]!r} vs page {page[cid]!r}")
    for cid in sorted(page):
        if cid not in reg:
            problems.append(f"page claim {cid!r} is not in the registry")
    if problems:
        for p in problems:
            print(f"DRIFT  {p}")
        print(f"build_sextant_claims: {len(reg)} registry claims vs {len(page)} on the page — {len(problems)} drift(s)")
        return 1
    print(f"build_sextant_claims: {len(reg)} registry claims, all on the page with matching verdicts — in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
