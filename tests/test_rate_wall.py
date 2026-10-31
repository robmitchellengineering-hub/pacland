"""The rate wall — the measured loss, and the honest boundary of the claim."""
import unittest

from pacland.exactness import rate_wall as W


class TestTheRates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = W.the_wall()

    def test_every_rate_carries_its_budget(self):
        for r in self.w["rows"]:
            self.assertGreater(r["tries"], 0)
            self.assertIn("where", r)

    def test_the_loss_is_at_convergence_not_proposal(self):
        # validity barely moves; points-per-valid collapses
        self.assertLess(self.w["validity_loss"], 0.10)
        self.assertGreater(self.w["convergence_ratio"], 50)

    def test_the_ratio_is_quoted_with_its_direction(self):
        self.assertIn("collapses", self.w["statement"])

    def test_the_hypothesis_is_labelled_a_hypothesis(self):
        self.assertIn("solve dimension doubles", self.w["hypothesis"])
        self.assertIn("alternative", self.w["hypothesis"])

    def test_the_blocker_is_named(self):
        self.assertIn("does not expose per-trial residuals", self.w["test_that_would_settle_it"])

    def test_degree_is_excluded_as_the_cause(self):
        self.assertIn("degree 1 and 2", self.w["degree_is_not_the_cause"])


class TestTheNumbersReproduce(unittest.TestCase):
    def test_points_per_valid_is_computed_not_quoted(self):
        rows = W.rates()
        h2 = [r for r in rows if r["h12"] == 2][0]
        self.assertAlmostEqual(h2["points_per_valid"], 53 / 384, places=9)

    def test_the_two_h12_five_runs_are_both_included(self):
        rows = [r for r in W.rates() if r["h12"] == 5]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["points"] == 2 for r in rows))


if __name__ == "__main__":
    unittest.main()
