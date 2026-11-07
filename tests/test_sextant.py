"""SEXTANT engine — each rule must be able to fail (mutation-tested by construction)."""
import math
import unittest

from pacland.sextant import FORCED, FREE, IMPOSSIBLE, run


class TestSextant(unittest.TestCase):
    def test_chsh_is_forced_at_tsirelson(self):
        r = run("what's the maximum CHSH violation?")
        self.assertEqual(r["verdict"], FORCED)
        self.assertIsNotNone(r["simulate"])
        self.assertAlmostEqual(r["simulate"], 2 * math.sqrt(2), places=9)

    def test_bell_wall_is_two(self):
        r = run("classical CHSH bound")
        self.assertEqual(r["verdict"], FORCED)
        self.assertEqual(r["simulate"], 2.0)

    def test_no_cloning_is_impossible(self):
        self.assertEqual(run("clone")["verdict"], IMPOSSIBLE)

    def test_generation_is_free(self):
        self.assertEqual(run("is N_gen fixed?")["verdict"], FREE)

    def test_unknown_question_is_unknown_not_pass(self):
        r = run("what colour is the Higgs?")
        self.assertEqual(r["verdict"], "UNKNOWN")

    def test_every_claim_has_falsifier_and_remedy(self):
        from pacland.sextant import CLAIMS

        ids = set()
        for c in CLAIMS:
            self.assertTrue(c.id, "claim id empty")
            self.assertNotIn(c.id, ids, f"duplicate id {c.id}")
            ids.add(c.id)
            self.assertTrue(c.question, f"{c.id} has no question")
            self.assertTrue(c.falsifier, f"{c.id} has no falsifier")
            self.assertTrue(c.remedy, f"{c.id} has no remedy")
            self.assertIn(c.verdict, (FORCED, FREE, IMPOSSIBLE), c.id)


if __name__ == "__main__":
    unittest.main()
