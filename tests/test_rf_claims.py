"""The RF claims registry, enforced the way the physics one is.

Every number the RF work quotes must name a script that exists, a document that exists, and the check that could make it
wrong. A PASS-2 must carry at least two independent evidence lines, so the status cannot be typed on.

The first run of the physics guard found a script cited in a merged document that had never been merged. This exists so the
RF numbers cannot do the same.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "rf-claims.json"
STATUSES = {"PASS-1", "PASS-2", "withdrawn"}


def claims() -> list[dict]:
    return json.loads(REGISTRY.read_text())["claims"]


class TestRfClaims(unittest.TestCase):

    def test_the_registry_parses_and_is_not_empty(self):
        self.assertGreater(len(claims()), 0)

    def test_every_claim_has_the_required_fields(self):
        for c in claims():
            for field in ("id", "claim", "status", "script", "doc", "evidence", "falsifier"):
                self.assertIn(field, c, f"{c.get('id')} has no {field}")

    def test_every_id_is_unique(self):
        ids = [c["id"] for c in claims()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_status_is_one_of_the_three(self):
        for c in claims():
            self.assertIn(c["status"], STATUSES, f"{c['id']} has status {c['status']}")

    def test_every_script_exists(self):
        missing = [c["script"] for c in claims() if not (ROOT / c["script"]).exists()]
        self.assertEqual(missing, [], f"scripts cited but absent: {missing}")

    def test_every_doc_exists(self):
        missing = [c["doc"] for c in claims() if not (ROOT / c["doc"]).exists()]
        self.assertEqual(missing, [], f"documents cited but absent: {missing}")

    def test_a_pass_two_carries_two_independent_evidence_lines(self):
        for c in claims():
            if c["status"] == "PASS-2":
                self.assertGreaterEqual(len(c["evidence"]), 2, f"{c['id']} claims PASS-2 on one line")

    def test_every_claim_has_a_falsifier(self):
        for c in claims():
            self.assertGreater(len(c["falsifier"].strip()), 20, f"{c['id']} falsifier is not a check")

    def test_a_withdrawn_claim_says_why(self):
        withdrawn = [c for c in claims() if c["status"] == "withdrawn"]
        for c in withdrawn:
            self.assertIn("reason", c, f"{c['id']} is withdrawn with no reason recorded")


if __name__ == "__main__":
    unittest.main()
