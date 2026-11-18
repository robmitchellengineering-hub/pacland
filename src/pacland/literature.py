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

# Sentences that state a TEST or CONSTRAINT — the material a falsifier is built from.
_CONSTRAINT_VERBS = ("we rule out", "we exclude", "we find no evidence", "we bound", "we constrain",
                     "we place", "we measure", "we observe", "we search for")
_CONSTRAINT_WORDS = ("bound", "exclude", "excluded", "constrain", "rule out", "ruled out",
                     "tension with", "no evidence", "upper", "lower", "consistent with",
                     "limits", "limit on", "disfavors", "disfavoured")


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


def extract_method(abstract: str) -> list[str]:
    """Pull the sentences that state a TEST or CONSTRAINT — the falsifier material.

    These are the parts of an abstract that say what was measured/bounded/excluded, i.e. the
    evidence a falsifier can be built from, as opposed to the headline claim.
    """
    text = " ".join((abstract or "").split())
    if not text:
        return []
    out: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        low = sentence.lower()
        if low.startswith(_CONSTRAINT_VERBS) or any(k in low for k in _CONSTRAINT_WORDS):
            out.append(sentence.strip())
    return out


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


_NEGATION_MARKERS = ("refute", "disprove", "contradict", "no such", "does not", "cannot",
                     "fails", "absent", "vanishes", "incompatible", "impossible", "rule out")
_STOPWORDS = {
    "that", "with", "this", "from", "these", "their", "they", "have", "than", "will",
    "would", "been", "were", "such", "more", "also", "only", "very", "into", "over",
    "under", "where", "when", "which", "while", "there", "here", "about", "between",
    "through", "using", "other", "which", "their", "them", "this", "then",
}


def _subject_words(claim: str) -> set[str]:
    """Lowercased words of length >= 5 that are not stopwords — a rough 'what the claim is about'."""
    return {w for w in re.findall(r"[a-z]{4,}", (claim or "").lower()) if w not in _STOPWORDS}


def find_contradictions(records: list[dict]) -> list[dict]:
    """Surface candidate contradiction pairs — papers whose claims disagree on a shared subject.

    Conservative first pass: a pair is surfaced only when both records have a claim, the two claims
    share at least one subject word, and at least one claim carries an explicit negation marker.
    This SURFACES candidates; it does not judge which side is right — the falsifier does.
    """
    out = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            a, b = records[i], records[j]
            ca, cb = a.get("claim"), b.get("claim")
            if not ca or not cb:
                continue
            shared = _subject_words(ca) & _subject_words(cb)
            if not shared:
                continue
            if any(m in ca.lower() for m in _NEGATION_MARKERS) or \
               any(m in cb.lower() for m in _NEGATION_MARKERS):
                out.append({"a": a["arxiv_id"], "b": b["arxiv_id"], "on": sorted(shared)})
    return out


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
