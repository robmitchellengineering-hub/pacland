"""The SEXTANT runner loop: generate → test → promote/drop → record (no prose, structured)."""
import tempfile
import unittest
from pathlib import Path

from pacland import runner


class TestRunner(unittest.TestCase):
    def test_generate_combine_ou_gap(self):
        c = runner.generate(["ou-curvature", "gronwall-decay"], "combine")
        self.assertEqual(c.id, "ou-gap-lower-bound")
        self.assertEqual(c.strategy, "combine")
        self.assertEqual(c.test, "ou-gap")

    def test_generate_specialize_su2(self):
        c = runner.generate(["confinement-frontier"], "specialize")
        self.assertEqual(c.id, "su2-weak-coupling-area-law")
        self.assertEqual(c.strategy, "specialize")
        self.assertEqual(c.test, "su2-weak-coupling")

    def test_run_ou_gap_survives(self):
        c = runner.generate(["ou-curvature", "gronwall-decay"], "combine")
        v = runner.run(c)
        self.assertTrue(v.survived)
        self.assertEqual(v.verdict, "SURVIVED")
        self.assertIn("spectral gap = exactly 1", v.evidence)

    def test_advance_promotes_and_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_rec, old_disc = runner.RECORD, runner.DISCOVERIES
            runner.RECORD = Path(tmp) / "runner.jsonl"
            runner.DISCOVERIES = Path(tmp) / "discoveries.jsonl"
            try:
                v = runner.advance(["ou-curvature", "gronwall-decay"], "combine")
                self.assertTrue(v.survived)
                self.assertTrue(runner.DISCOVERIES.exists())
                self.assertTrue(runner.RECORD.exists())
                self.assertEqual(len(runner.list_discoveries()), 1)
                self.assertEqual(runner.list_discoveries()[0]["id"], "ou-gap-lower-bound")
            finally:
                runner.RECORD, runner.DISCOVERIES = old_rec, old_disc

    def test_decompose_emits_next_sublemma(self):
        c = runner.next_sublemma("ym-mass-gap")
        self.assertEqual(c.strategy, "decompose")
        self.assertIn("Dobrushin", c.statement)
        self.assertTrue(c.falsifier)
        self.assertEqual(c.source_facts, ("ym-mass-gap",))

    def test_decompose_runnable_maps_to_falsifier(self):
        # the area-law candidate of confinement-frontier has a runnable Creutz-ratio falsifier
        c = runner.generate(["confinement-frontier"], "specialize")
        self.assertEqual(c.test, "su2-weak-coupling")

    def test_manual_candidate_is_not_an_error(self):
        c = runner.next_sublemma("ym-mass-gap")
        v = runner.run(c)
        self.assertEqual(v.verdict, "MANUAL")
        self.assertIsNone(v.survived)
        self.assertIn("thinking agent", v.evidence)


if __name__ == "__main__":
    unittest.main()
