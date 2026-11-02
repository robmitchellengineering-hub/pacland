"""Hypotheses must cross-reference real walls, and the page must not drift."""
import subprocess
import sys
import unittest
from pathlib import Path

from pacland.exactness import hypotheses as H
from pacland.exactness import walls as W

ROOT = Path(__file__).resolve().parents[1]


class TestTheLinks(unittest.TestCase):
    def test_every_cited_wall_exists(self):
        link = H.check_links()
        self.assertTrue(link["ok"], link)

    def test_every_hypothesis_pairs_at_least_two_walls(self):
        for hid, title, cited, *rest in H.HYPOTHESES:
            self.assertGreaterEqual(len(set(cited)), 2, hid)

    def test_no_orphan_hypothesis(self):
        # a hypothesis must trace back to the register, not to our enthusiasm
        known = {n for n, *_ in W.REGISTER}
        for hid, title, cited, *rest in H.HYPOTHESES:
            self.assertTrue(set(cited) <= known, hid)


class TestTheRecords(unittest.TestCase):
    def test_every_hypothesis_has_a_test_and_a_prediction(self):
        for hid, title, cited, claim, predicts, test, status in H.HYPOTHESES:
            self.assertGreater(len(predicts), 15, hid)
            self.assertGreater(len(test), 30, hid)
            self.assertIn(status, H.STATUSES)

    def test_the_seeded_three_are_present(self):
        ids = {h[0] for h in H.HYPOTHESES}
        self.assertTrue({"H-A", "H-B", "H-C"} <= ids)


class TestThePageDoesNotDrift(unittest.TestCase):
    def test_check_passes(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "hypotheses.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
