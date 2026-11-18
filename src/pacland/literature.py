"""Capability 2 — literature and dataset search.

Given an open question, search arXiv and return the state of the art as *structured* records
(title / claim / empty falsifier slot), not prose. This is retrieval and structuring, not
judgement: the searcher surfaces what is on record; it does not decide which hypothesis is right —
the falsifier does. The discovery engine consumes ``search_arxiv``; the searcher never reaches into
the engine.

The claim extraction is a rule-based first pass on purpose: a model replaces it later, and the
test pins the rule so a later swap is measurable.
"""
from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

_ARXIV_API = "https://export.arxiv.org/api/query"
_ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
_CLAIM_VERBS = ("we show", "we prove", "we establish", "we demonstrate", "we find",
                "we derive", "we obtain", "we present", "we construct", "we provide",
                "we introduce", "we give")


def parse_atom(xml_bytes: bytes) -> list[dict]:
    """Parse an arXiv Atom response into structured records."""
    root = ET.fromstring(xml_bytes)
    records = []
    for entry in root.findall("atom:entry", _ATOM_NS):
        title = " ".join((entry.findtext("atom:title", "", _ATOM_NS) or "").split())
        abstract = " ".join((entry.findtext("atom:summary", "", _ATOM_NS) or "").split())
        authors = [a.findtext("atom:name", "", _ATOM_NS) or ""
                   for a in entry.findall("atom:author", _ATOM_NS)]
        records.append({
            "arxiv_id": (entry.findtext("atom:id", "", _ATOM_NS) or "").strip(),
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "published": entry.findtext("atom:published", "", _ATOM_NS) or "",
        })
    return records


def extract_claim(abstract: str) -> str | None:
    """Pull the headline claim out of an abstract.

    Returns the first sentence that reads like an assertion the paper is making — one a falsifier
    could be written against — or ``None`` when there is nothing to quote. Rule-based first pass:
    a sentence beginning with a claim verb (``we show``, ``we prove``, …).
    """
    text = " ".join((abstract or "").split())
    if not text:
        return None
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sentence in sentences:
        low = sentence.lower()
        if low.startswith(_CLAIM_VERBS):
            return sentence.strip()
    return None


def structure(records: list[dict]) -> list[dict]:
    """Add the extracted claim and an empty falsifier slot (the engine fills it)."""
    return [{**r, "claim": extract_claim(r.get("abstract", "")), "falsifier": None}
            for r in records]


def search_arxiv(query: str, max_results: int = 10) -> list[dict]:
    """Search arXiv and return structured records (with ``claim`` and an empty ``falsifier``)."""
    url = _ARXIV_API + "?" + urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    })
    with urllib.request.urlopen(url, timeout=30) as resp:
        return structure(parse_atom(resp.read()))


def main(argv: list[str] | None = None) -> int:
    import sys

    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("--help", "-h"):
        print(__doc__)
        return 0
    if argv[0] != "search":
        print("usage: python -m pacland.literature search <query> [max_results]", file=sys.stderr)
        return 2
    query = argv[1]
    max_results = int(argv[2]) if len(argv) > 2 else 10
    for r in search_arxiv(query, max_results):
        print(f"* {r['title']}")
        print(f"  {r['arxiv_id']}")
        if r["claim"]:
            print(f"  claim: {r['claim']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
