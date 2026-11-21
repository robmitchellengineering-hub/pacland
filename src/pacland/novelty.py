"""novelty.py — the blind-benchmark verdict: is a candidate genuinely NEW, or just recall?

The line SEXTANT must not cross is claiming "discovery" for something already published. The novelty
verdict is settled by a WEB SEARCH done here (not handed off to outside experts):

  1. RECALL check — is the mapping already in the known-unifications library (or the registry)? → 'known'
  2. PUBLISHED check — a web search (arXiv) for the claim's terms → 'published' when it matches, else
     'candidate-novel' (not-found is weak evidence for novelty, never a proof of it).

This is the benchmark that tells the difference between reproducing famous discoveries and finding
something not already in the literature.
"""
from __future__ import annotations

import re
import urllib.parse
import urllib.request

from pacland import registry


def _key_terms(claim: str, keep: int = 4) -> str:
    """The significant terms to search — drop stopwords, keep the distinctive content words."""
    stop = {"the", "a", "an", "of", "and", "or", "in", "on", "for", "with", "that", "is", "are",
            "to", "from", "by", "at", "as", "this", "does", "not", "no"}
    words = re.findall(r"[a-z]{3,}", claim.lower())
    terms = [w for w in words if w not in stop]
    return " ".join(terms[:keep])


def _arxiv_search(terms: str, max_results: int = 5) -> list[str]:
    """Query arXiv for the terms; return the matching paper titles (the 'already published?' check)."""
    q = urllib.parse.quote(f'all:"{terms}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results={max_results}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            xml = r.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — a network failure means UNKNOWN, not a verdict
        return []
    titles = re.findall(r"<title>(.*?)</title>", xml, re.DOTALL)
    return [t.strip() for t in titles[1:]]  # titles[0] is the feed title


def is_known(frm: str, to: str) -> bool:
    """RECALL check: is the (frm, to) mapping already in the known-unifications library or registry?"""
    try:
        from pacland import known_unifications
        pairs = {(a, b) for a, b, _f, _s in known_unifications.UNIFICATIONS}
        if (frm, to) in pairs or (to, frm) in pairs:
            return True
    except Exception:  # noqa: BLE001
        pass
    for m in registry.query("mapping", lambda d: True):
        p = m.get("payload", {})
        if {p.get("from"), p.get("to")} == {frm, to}:
            return True
    return False


def web_check(claim: str, _search=None) -> dict:
    """The PUBLISHED check — a web search done here, not a handoff.

    Returns a verdict + evidence. 'published' when arXiv has a match; 'not-found' when it does not
    (weak evidence for novelty); 'unsettled' when the search could not run.
    """
    searcher = _search or _arxiv_search
    terms = _key_terms(claim)
    if not terms:
        return {"verdict": "unsettled", "evidence": "no searchable terms"}
    titles = searcher(terms)
    if titles:
        return {"verdict": "published", "evidence": titles[:3]}
    return {"verdict": "not-found", "evidence": [], "terms": terms}


def novelty_verdict(frm: str, to: str, claim: str, _search=None) -> dict:
    """The three-way verdict: 'known' (recall), 'published' (web), 'candidate-novel' (neither).

    A 'candidate-novel' result is a CANDIDATE for genuine novelty — it has passed the recall check and
    a web search did not surface it — but it is not yet a proof of novelty (the search is arXiv-only
    and 'not-found' is weak evidence).
    """
    if is_known(frm, to):
        return {"verdict": "known", "mapping": (frm, to), "evidence": "in the known-unifications library"}
    wc = web_check(claim, _search=_search)
    if wc["verdict"] == "published":
        return {"verdict": "published", "mapping": (frm, to), "evidence": wc["evidence"]}
    if wc["verdict"] == "unsettled":
        return {"verdict": "unsettled", "mapping": (frm, to), "evidence": wc["evidence"]}
    return {"verdict": "candidate-novel", "mapping": (frm, to), "evidence": wc}


def benchmark_novelty(candidates: list[tuple[str, str, str]], _search=None) -> dict:
    """The blind benchmark: classify each (frm, to, claim) and report the recall vs novel split.

    The number that matters is the CANDIDATE-NOVEL rate — the fraction that is neither already in the
    library nor already on arXiv. That, not the raw candidate count, is the measure of genuine novelty.
    """
    verdicts = [novelty_verdict(f, t, c, _search=_search) for f, t, c in candidates]
    tally: dict[str, int] = {}
    for v in verdicts:
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
    n = max(1, len(verdicts))
    return {
        "total": len(verdicts),
        "tally": tally,
        "recall_rate": tally.get("known", 0) / n,
        "published_rate": tally.get("published", 0) / n,
        "candidate_novel_rate": tally.get("candidate-novel", 0) / n,
        "verdicts": verdicts,
    }
