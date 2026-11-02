"""The wall register must classify every wall, and the classes must be honest."""
import subprocess
import sys
import unittest
from pathlib import Path

from pacland.exactness import walls as W

ROOT = Path(__file__).resolve().parents[1]


class TestTheRegister(unittest.TestCase):
    def test_all_four_classes_are_used(self):
        c = W.counts()
        for k in ("dissolves", "provable", "infrastructure", "bounded"):
            self.assertGreaterEqual(c[k], 1, k)

    def test_every_wall_has_evidence_and_a_contrast(self):
        for name, cls, looked, actually, evidence in W.REGISTER:
            self.assertGreater(len(looked), 10, name)
            self.assertGreater(len(actually), 30, name)
            self.assertGreater(len(evidence), 5, name)

    def test_the_rate_wall_is_classed_as_ours_not_natures(self):
        # this is the whole point: it looked like a law and was a budget
        r = {x["name"]: x for x in W.by_class()["DISSOLVES"]}
        self.assertTrue(any("rate wall" in n for n in r))

    def test_the_measure_wall_is_classed_as_provable(self):
        p = {x["name"]: x for x in W.by_class()["PROVABLE"]}
        self.assertTrue(any("measure wall" in n for n in p))

    def test_the_page_says_only_provable_walls_constrain(self):
        self.assertIn("Only PROVABLE walls constrain", W.render())


class TestThePageDoesNotDrift(unittest.TestCase):
    def test_check_passes(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "walls.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
