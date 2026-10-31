import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    """Load a script module WITHOUT putting scripts/ on sys.path.

    `scripts/` contains test-named files from another session (test_swampland, test_orbit_injectivity, ...).
    Appending it to sys.path makes unittest discovery import THOSE instead of tests/*, which surfaces as
    "module incorrectly imported from .../scripts". Load by explicit path and keep sys.path clean.
    """
    spec = importlib.util.spec_from_file_location(f"_script_{name}", ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

C = _load("cycles")


class TestTheLog(unittest.TestCase):
    def test_the_file_is_current(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "cycles.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_turn_has_the_four_parts(self):
        for c in C.LOOPS:
            for key in ("negative", "question", "object", "excluded", "command"):
                self.assertTrue(c[key].strip(), f"{c['id']} missing {key}")

    def test_every_turn_states_what_it_excluded(self):
        # the discipline: no exclusion, no entry
        for c in C.LOOPS:
            self.assertGreater(len(c["excluded"]), 30, c["id"])

    def test_the_loop_has_both_kinds_of_outcome(self):
        # at least one entry where the answer was a definition, and one where it was a correction
        text = (ROOT / "docs" / "cycles.md").read_text()
        self.assertIn("exactly", text)
        self.assertIn("invalid", text)

    def test_the_count_in_the_header_matches(self):
        text = (ROOT / "docs" / "cycles.md").read_text()
        self.assertIn(f"{len(C.LOOPS)} closed loops", text)


if __name__ == "__main__":
    unittest.main()
