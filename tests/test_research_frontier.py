"""The research frontier must not silently drift from the SEXTANT registry.

Priority 2 (unify the infrastructure): the accounting (`web/research-frontier.json`) and the
claim registry (`sextant.CATALOG`) are two views of one graph. This test makes the drift fail
loudly, the way `test_site_index.py` makes the site index fail.

The invariants:
- every `ym-*` claim carries a proof tier (no `tier` left unset);
- the frontier's `obligations` are exactly the claims whose hypothesis is still open
  (an `IRREDUCIBLE` verdict, or a `FORCED` transport whose hypothesis is named-but-unproved).
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FRONTIER = ROOT / "web" / "research-frontier.json"
VALID_TIERS = {"identity", "lemma", "chain", "conditional", "result"}


def _frontier() -> dict:
    return json.loads(FRONTIER.read_text())


def _catalog():
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from pacland import sextant
    return sextant.CATALOG


def test_frontier_schema_valid():
    d = _frontier()
    assert d["schema"] == "sextant-research-frontier"
    assert d["root_obligation"]
    assert isinstance(d["transports"], list) and isinstance(d["obligations"], list)


def test_every_ym_claim_has_a_tier():
    cat = _catalog()
    missing = [n for n, e in cat.items() if n.startswith("ym-") and e.get("tier") not in VALID_TIERS]
    assert not missing, f"ym-* claims without a tier: {missing}"


def test_frontier_obligations_match_open_claims():
    cat = _catalog()
    frontier_obligations = {o["name"] for o in _frontier()["obligations"]}
    claims = {n for n in cat if n.startswith("ym-")}
    orphans = frontier_obligations - claims
    assert not orphans, f"frontier obligations that are not ym-* claims: {orphans}"
    for o in _frontier()["obligations"]:
        assert o["state"] == "open", f"obligation {o['name']} must be state 'open'"
    # the IRREDUCIBLE (open) claims must all be accounted for somewhere in the frontier
    irreducible = {n for n, e in cat.items() if n.startswith("ym-") and e["verdict"] == "IRREDUCIBLE"}
    assert irreducible <= frontier_obligations, f"open claims missing from the frontier: {irreducible - frontier_obligations}"
