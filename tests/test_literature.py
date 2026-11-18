"""The literature searcher returns structured records and quotes the headline claim — no network in tests."""
import unittest

from pacland import literature as lit

SAMPLE_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>ArXiv Query: search_query=all:mass gap</title>
  <entry>
    <id>http://arxiv.org/abs/2501.00001v1</id>
    <title>A Sharp Lower Bound on the Yang-Mills Mass Gap</title>
    <summary>We prove a sharp lower bound on the mass gap for non-Abelian lattice gauge theory. We show the bound reaches the asymptotic-freedom scale.</summary>
    <author><name>Alice</name></author>
    <author><name>Bob</name></author>
    <published>2025-01-01T00:00:00Z</published>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2501.00002v1</id>
    <title>A Survey of Confinement Mechanisms</title>
    <summary>This survey reviews several confinement mechanisms. No new results are reported.</summary>
    <author><name>Carol</name></author>
    <published>2025-01-02T00:00:00Z</published>
  </entry>
</feed>
"""


class TestParseAtom(unittest.TestCase):
    def test_extracts_title_abstract_authors(self):
        records = lit.parse_atom(SAMPLE_FEED.encode())
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["title"], "A Sharp Lower Bound on the Yang-Mills Mass Gap")
        self.assertEqual(records[0]["authors"], ["Alice", "Bob"])
        self.assertIn("sharp lower bound", records[0]["abstract"])

    def test_collapses_whitespace_in_title(self):
        records = lit.parse_atom(SAMPLE_FEED.encode())
        self.assertNotIn("  ", records[0]["title"])


class TestExtractClaim(unittest.TestCase):
    def test_quotes_the_first_claim_sentence(self):
        claim = lit.extract_claim("We prove a sharp lower bound. We show the scale.")
        self.assertEqual(claim, "We prove a sharp lower bound.")

    def test_returns_none_when_no_claim_verb(self):
        claim = lit.extract_claim("This survey reviews several mechanisms.")
        self.assertIsNone(claim)

    def test_returns_none_for_empty_abstract(self):
        self.assertIsNone(lit.extract_claim(""))


class TestStructure(unittest.TestCase):
    def test_adds_claim_and_empty_falsifier_slot(self):
        records = lit.parse_atom(SAMPLE_FEED.encode())
        structured = lit.structure(records)
        self.assertEqual(structured[0]["claim"], "We prove a sharp lower bound on the mass gap for non-Abelian lattice gauge theory.")
        self.assertIsNone(structured[0]["falsifier"])
        # the survey asserts nothing, so no claim is quoted
        self.assertIsNone(structured[1]["claim"])


class TestFindContradictions(unittest.TestCase):
    def _records(self, claims):
        return [{"arxiv_id": f"id-{i}", "claim": c} for i, c in enumerate(claims)]

    def test_surfaces_a_pair_when_one_claim_negates_on_a_shared_subject(self):
        records = self._records([
            "We prove the mass gap is positive for the Yang-Mills theory.",
            "We refute the mass gap claim: the gap vanishes in the Yang-Mills theory.",
        ])
        pairs = lit.find_contradictions(records)
        self.assertEqual(len(pairs), 1)
        self.assertIn("mass", pairs[0]["on"])

    def test_no_pair_when_claims_agree(self):
        records = self._records([
            "We prove the mass gap is positive for the Yang-Mills theory.",
            "We strengthen the mass gap bound for the Yang-Mills theory.",
        ])
        self.assertEqual(lit.find_contradictions(records), [])

    def test_no_pair_without_a_shared_subject(self):
        records = self._records([
            "We refute the positive mass gap.",
            "We prove the photon is massless.",
        ])
        self.assertEqual(lit.find_contradictions(records), [])


if __name__ == "__main__":
    unittest.main()
