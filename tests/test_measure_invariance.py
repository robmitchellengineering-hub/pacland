"""The audit must have two populated classes, cite real modules, and stay in sync with its generated page."""
import subprocess
import sys
import unittest
from pathlib import Path

from pacland.exactness import measure_invariance as M

ROOT = Path(__file__).resolve().parents[1]


class TestTheRegister(unittest.TestCase):
    def test_both_classes_are_populated(self):
        c = M.counts()
        self.assertGreaterEqual(c["invariant"], 5)
        self.assertGreaterEqual(c["dependent"], 5)

    def test_every_cited_module_exists(self):
        for name, cls, why, module in M.REGISTER:
            self.assertTrue((ROOT / "src" / "pacland" / module).is_file(), f"{name}: {module}")

    def test_every_entry_has_a_reason(self):
        for name, cls, why, module in M.REGISTER:
            self.assertGreater(len(why), 20, name)

    def test_the_theorem_is_invariant_and_the_sampler_is_not(self):
        inv = {r["name"] for r in M.by_class()["INVARIANT"]}
        dep = {r["name"] for r in M.by_class()["DEPENDENT"]}
        self.assertTrue(any("max |N| = b3" in n for n in inv))
        self.assertTrue(any("accessibility" in n for n in dep))


class TestTheGeneratedPageDoesNotDrift(unittest.TestCase):
    def test_check_passes(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "measure_audit.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
