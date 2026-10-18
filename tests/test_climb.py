import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.deficit import deficit_report
from pacland.observables import TOPOLOGY_OBSERVABLES

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "cy_corpus.json"


def _load_climber():
    spec = importlib.util.spec_from_file_location(
        "climb_deficit", ROOT / "scripts" / "climb_deficit.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestClimbCorpus(unittest.TestCase):
    def test_corpus_is_well_formed(self):
        with open(CORPUS) as f:
            corpus = json.load(f)
        self.assertIn("manifolds", corpus)
        quintic = corpus["manifolds"][0]
        self.assertEqual(quintic["name"], "quintic P4[5]")
        self.assertEqual(quintic["known"]["h11"], 1)
        self.assertEqual(quintic["known"]["h21"], 101)
        self.assertEqual(quintic["known"]["c2"], [-250, 50, 50, 50, 50, 50])
        self.assertEqual(quintic["known"]["kappa"], [5])
        # only the independent invariants count toward m
        self.assertEqual(quintic["counted"], ["h11", "h21", "c2", "kappa"])

    def test_corpus_matches_validated_observables(self):
        with open(CORPUS) as f:
            corpus = json.load(f)
        counted = set()
        for m in corpus["manifolds"]:
            counted.update(m["counted"])
        # the deficit's topology sector (m=4) and the corpus agree
        self.assertEqual(counted, {"h11", "h21", "c2", "kappa"})
        r = deficit_report(TOPOLOGY_OBSERVABLES)
        self.assertEqual(r.n_validation, len(counted))

    def test_climber_radius_matches_deficit(self):
        climber = _load_climber()
        delta = 0.025
        self.assertAlmostEqual(climber.hoefding(4, delta), 0.6791, places=4)
        self.assertEqual(climber.hoefding(0, delta), float("inf"))


if __name__ == "__main__":
    unittest.main()
