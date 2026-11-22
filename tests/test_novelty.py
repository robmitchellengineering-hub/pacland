"""P1 — blind benchmark: the novelty verdict ends in a web search done by us (recall vs novel)."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, novelty


def _no_hits(terms):
    return []


def _one_hit(terms):
    return ["A paper on " + terms]


class TestNovelty(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_recall_is_known(self):
        # wealth-distribution ↔ boltzmann is a harvested known unification
        self.assertTrue(novelty.is_known("wealth-distribution", "boltzmann"))

    def test_unknown_pair_is_not_known(self):
        self.assertFalse(novelty.is_known("xyzzy", "plugh"))

    def test_published_verdict(self):
        v = novelty.novelty_verdict("xyzzy", "plugh", "a new link between xyzzy and plugh", _search=_one_hit)
        self.assertEqual(v["verdict"], "published")

    def test_candidate_novel_verdict(self):
        v = novelty.novelty_verdict("xyzzy", "plugh", "a new link between xyzzy and plugh", _search=_no_hits)
        self.assertEqual(v["verdict"], "candidate-novel")

    def test_benchmark_reports_split(self):
        b = novelty.benchmark_novelty([
            ("wealth-distribution", "boltzmann", "wealth is a Boltzmann gas"),
            ("xyzzy", "plugh", "a new link between xyzzy and plugh"),
        ], _search=_no_hits)
        self.assertEqual(b["tally"].get("known"), 1)
        self.assertEqual(b["tally"].get("candidate-novel"), 1)
        self.assertIn("candidate_novel_rate", b)


if __name__ == "__main__":
    unittest.main()
