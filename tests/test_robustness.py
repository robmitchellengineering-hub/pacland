"""The robustness engine — a number is a fact only once its choice-dependence is printed."""
import unittest

from pacland.exactness import robustness as R


class TestTheVerdicts(unittest.TestCase):
    def test_a_tight_spread_is_stable(self):
        r = R.assess("x", {"a": 0.500, "b": 0.505, "c": 0.495})
        self.assertTrue(r.stable)
        self.assertIsNone(r.dominant)

    def test_a_wide_spread_is_choice_dependent(self):
        r = R.assess("x", {"a": 0.10, "b": 0.30})
        self.assertEqual(r.verdict, "choice-dependent")
        self.assertIn("b vs a", r.dominant)

    def test_the_tolerance_is_stated_so_a_reader_can_disagree_with_the_number(self):
        # the same values are stable at 60% and choice-dependent at 10%
        vals = {"a": 0.10, "b": 0.30}
        self.assertTrue(R.assess("x", vals, tolerance=2.0).stable)
        self.assertFalse(R.assess("x", vals, tolerance=0.10).stable)

    def test_an_empty_input_is_refused(self):
        with self.assertRaises(ValueError):
            R.assess("x", {})


class TestTheCorpusSusyCustomer(unittest.TestCase):
    """The 21.17% headline, judged."""

    @classmethod
    def setUpClass(cls):
        cls.r = R.corpus_susy_fraction()

    def test_it_is_not_stable(self):
        self.assertEqual(self.r.verdict, "choice-dependent")

    def test_the_h12_split_is_the_dominant_choice(self):
        self.assertIn("h12", self.r.dominant)

    def test_the_pooled_number_sits_between_the_strata(self):
        v = self.r.values
        pooled = v["row-weighted, all rows"]
        strata = [v["h12 = 2 rows only"], v["h12 = 3 rows only"], v["h12 = 4 rows only"]]
        self.assertLessEqual(min(strata), pooled)
        self.assertGreaterEqual(max(strata), pooled)

    def test_the_stratified_rates_differ_by_an_order_of_magnitude(self):
        v = self.r.values
        self.assertGreater(v["h12 = 2 rows only"], 10 * v["h12 = 4 rows only"])

    def test_the_note_says_what_the_pooled_number_is_partly_about(self):
        self.assertIn("allocated", self.r.note)


class TestTheEngineCanFail(unittest.TestCase):
    def test_a_planted_choice_dependence_is_caught(self):
        # a statistic that is 0.2 under one weighting and 0.4 under another, with a tight bootstrap
        r = R.assess("planted", {"row-weighted": 0.20, "family-weighted": 0.40})
        self.assertEqual(r.verdict, "choice-dependent")
        self.assertAlmostEqual(r.spread, 0.20, places=12)

    def test_a_genuinely_flat_statistic_passes(self):
        r = R.assess("flat", {f"c{i}": 0.5000 + i * 1e-6 for i in range(5)})
        self.assertTrue(r.stable)


if __name__ == "__main__":
    unittest.main()
