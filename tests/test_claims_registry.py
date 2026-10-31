"""The claims registry: every published number has a status, a script, and a falsifier.

This is the enforcement leg of the goal. It makes PASS-1 and PASS-2 mechanical instead of a habit: a claim
marked PASS-2 must cite at least two independent evidence lines, and a withdrawn claim must say why.
"""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "docs" / "claims.json").read_text())
VALID = {"PASS-1", "PASS-2", "withdrawn"}


class TestRegistryShape(unittest.TestCase):
    def test_every_claim_has_the_required_fields(self):
        for c in REG["claims"]:
            required = ("id", "claim", "status", "script", "doc")
            for field in required:
                self.assertIn(field, c, f"{c.get('id')} missing {field}")
            # a live claim must name what would break it; a withdrawn one must say why it broke
            if c["status"] == "withdrawn":
                self.assertIn("reason", c, f"{c['id']} withdrawn without a reason")
            else:
                self.assertIn("falsifier", c, f"{c['id']} has no falsifier")

    def test_status_is_one_of_three(self):
        for c in REG["claims"]:
            self.assertIn(c["status"], VALID, c["id"])

    def test_ids_are_unique(self):
        ids = [c["id"] for c in REG["claims"]]
        self.assertEqual(len(ids), len(set(ids)))


class TestEveryClaimIsBacked(unittest.TestCase):
    def test_the_script_exists(self):
        for c in REG["claims"]:
            self.assertTrue((ROOT / c["script"]).exists(), f"{c['id']}: missing {c['script']}")

    def test_the_doc_exists(self):
        for c in REG["claims"]:
            self.assertTrue((ROOT / c["doc"]).exists(), f"{c['id']}: missing {c['doc']}")

    def test_a_withdrawn_claim_says_why(self):
        for c in REG["claims"]:
            if c["status"] == "withdrawn":
                self.assertTrue(c.get("reason"), f"{c['id']} is withdrawn with no reason")


class TestPass2MeansReproduced(unittest.TestCase):
    def test_pass2_cites_at_least_two_evidence_lines(self):
        for c in REG["claims"]:
            if c["status"] == "PASS-2":
                self.assertGreaterEqual(len(c.get("evidence", [])), 2,
                                        f"{c['id']} is PASS-2 with fewer than two evidence lines")

    def test_pass1_does_not_claim_reproduction(self):
        for c in REG["claims"]:
            if c["status"] == "PASS-1":
                ev = c.get("evidence", [])
                self.assertTrue(all("not measured" in e or "one parameterisation" in e or "computed, never" in e
                                    or "converged in cap" in e for e in ev) or len(ev) <= 2,
                                f"{c['id']} is PASS-1 but claims more evidence than a single run")


if __name__ == "__main__":
    unittest.main()
