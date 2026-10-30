"""The compression engine — structure is a prediction that survives held-out families."""
import json
import tempfile
import unittest
from pathlib import Path

from pacland.exactness import compression as X


def _write(d, name, rows):
    Path(d, name).write_text(json.dumps({"vacua": rows}))


class TestTheCorpus(unittest.TestCase):
    """The named customer: does the corpus compress on (log N, degree, h12)?"""

    @classmethod
    def setUpClass(cls):
        cls.r = X.compression()

    def test_the_verdict_is_reported(self):
        self.assertIn(self.r["verdict"], ("structure", "no structure",
                                          "no structure (the model is worse than the marginal)"))

    def test_the_baseline_and_the_model_are_both_scored(self):
        self.assertGreater(self.r["logloss_marginal"], 0)
        self.assertGreater(self.r["logloss_model"], 0)
        self.assertEqual(self.r["folds"], 16)

    def test_the_boundary_is_stated(self):
        self.assertIn("extrapolation", self.r["boundary"])
        self.assertIn("fixed before the score was seen", self.r["boundary"])


class TestStructureIsDetectable(unittest.TestCase):
    """Fail-ability: a dataset with a real, generalising dependence must come out `structure`."""

    def test_a_planted_dependence_is_found(self):
        with tempfile.TemporaryDirectory() as d:
            for h12 in (2, 3, 4):
                for m in (1, 2):
                    rows = []
                    for i in range(1, 60):
                        n = i
                        # label determined by N, identically in every family
                        rows.append({"flux": [1, 0, 0, 0, 1, 0, 0, 0], "Nflux": n,
                                     "is_susy": n < 30})
                    _write(d, f"h{h12}_{m}_stats.json", rows)
            r = X.compression(data_dir=d)
            self.assertEqual(r["verdict"], "structure", r)
            self.assertGreater(r["improvement"], 0.02)

    def test_no_dependence_reads_as_no_structure(self):
        with tempfile.TemporaryDirectory() as d:
            for h12 in (2, 3, 4):
                for m in (1, 2):
                    rows = [{"flux": [1, 0, 0, 0, 1, 0, 0, 0], "Nflux": i,
                             "is_susy": ((i * 7) % 13 == 0)} for i in range(1, 60)]
                    _write(d, f"h{h12}_{m}_stats.json", rows)
            r = X.compression(data_dir=d)
            self.assertIn("no structure", r["verdict"])


if __name__ == "__main__":
    unittest.main()
