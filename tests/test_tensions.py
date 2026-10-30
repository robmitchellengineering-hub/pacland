"""The tension register — generated, drift-guarded, and every open tension has a discriminator."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import tensions as T  # noqa: E402


class TestTheRegister(unittest.TestCase):
    def test_the_file_is_current(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "tensions.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_the_required_tensions_are_present(self):
        ids = {t["id"] for t in T.TENSIONS}
        self.assertTrue({"T1", "T2", "T3"} <= ids)
        text = (ROOT / "docs" / "tensions.md").read_text()
        for needle in ("degree 2 fixes it", "21.17%", "5.05x"):
            self.assertIn(needle, text)

    def test_every_tension_has_two_facts_and_a_discriminator(self):
        for t in T.TENSIONS:
            self.assertEqual(len(t["facts"]), 2, t["id"])
            self.assertGreater(len(t["discriminator"]), 40, t["id"])

    def test_every_tension_has_a_state(self):
        for t in T.TENSIONS:
            self.assertIn(t["state"], ("open", "resolved"), t["id"])

    def test_a_resolved_tension_carries_its_resolution(self):
        for t in T.TENSIONS:
            if t["state"] == "resolved":
                self.assertGreater(len(t["resolution"]), 60, t["id"])
            else:
                self.assertEqual(t["resolution"], "", t["id"])

    def test_an_open_tension_states_what_it_would_cost(self):
        for t in T.TENSIONS:
            if t["state"] == "open":
                self.assertNotEqual(t["cost"], "done", t["id"])

    def test_the_counts_in_the_header_match(self):
        text = (ROOT / "docs" / "tensions.md").read_text()
        open_n = sum(1 for t in T.TENSIONS if t["state"] == "open")
        self.assertIn(f"{len(T.TENSIONS)} entries", text)
        self.assertIn(f"{open_n} open", text)


if __name__ == "__main__":
    unittest.main()
