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


class TestTheClaimsRegistryRule(unittest.TestCase):
    """A decided hypothesis must name a script that exists; open may say "no executable test"."""

    def test_the_rule_passes(self):
        art = H.check_artefacts()
        self.assertTrue(art["ok"], art)

    def test_every_decided_hypothesis_has_a_script_on_disk(self):
        for hid, title, cited, claim, predicts, test, status, script in H.HYPOTHESES:
            if status in H.DECIDED:
                self.assertTrue(script, hid)
                self.assertTrue((ROOT / "scripts" / script).is_file(), f"{hid}: {script}")

    def test_an_open_hypothesis_may_have_none(self):
        open_ones = [h for h in H.HYPOTHESES if h[6] == "open"]
        self.assertTrue(open_ones, "expected at least one open hypothesis")
        self.assertTrue(any(h[7] is None for h in open_ones))

    def test_the_rule_text_is_in_the_page(self):
        self.assertIn("claims-registry rule", H.render())
        self.assertIn("no executable test", H.render())
