"""The invariant law — stated before the measurement, and the arithmetic it rests on."""
import math
import unittest

from pacland.exactness import invariant as I


class TestTheLaw(unittest.TestCase):
    def test_b3_is_2h12_plus_2(self):
        self.assertEqual(I.b3_of(2), 6)
        self.assertEqual(I.b3_of(5), 12)

    def test_c_is_fitted_from_the_two_anchors(self):
        c = I.fit_c()
        self.assertAlmostEqual(c, math.log(0.1325 / 0.00137) / 6, places=12)
        self.assertAlmostEqual(c, 0.763, places=2)

    def test_the_predictions_are_what_was_written_down(self):
        t = {r["h12"]: r for r in I.prediction_table()}
        self.assertAlmostEqual(t[3]["rate_per_try"], 0.029, places=2)
        self.assertAlmostEqual(t[4]["rate_per_try"], 0.0064, places=3)

    def test_the_predictions_come_from_the_law_not_from_data(self):
        # change the anchors and the prediction must move with them
        alt = ((2, 6, 0.100), (5, 12, 0.001))
        self.assertNotAlmostEqual(I.predicted_rate(3), I.predicted_rate(3, c=I.fit_c(alt)), places=4)


class TestTheVerdict(unittest.TestCase):
    def test_without_measurement_it_says_awaiting(self):
        v = I.verdict({})
        self.assertEqual(v["status"], "awaiting measurement")
        self.assertIn("before the run", v["note"])

    def test_a_match_confirms(self):
        v = I.verdict({3: 0.029, 4: 0.0064})
        self.assertEqual(v["status"], "confirmed")
        self.assertIn("same integer", v["composition"])

    def test_a_miss_refutes(self):
        v = I.verdict({3: 0.13, 4: 0.13})
        self.assertEqual(v["status"], "refuted")
        self.assertIn("not one invariant", v["composition"])

    def test_the_tolerance_is_a_factor_of_three(self):
        # 2.9x off still confirms; 29x off does not -- a stated band, so the verdict is auditable
        self.assertEqual(I.verdict({3: 0.080, 4: 0.018})["status"], "confirmed")
        self.assertEqual(I.verdict({3: 0.0029, 4: 0.00064})["status"], "refuted")


if __name__ == "__main__":
    unittest.main()


class TestThePartialVerdict(unittest.TestCase):
    """What the first run actually established, recorded rather than smoothed over."""

    def test_the_first_run_is_recorded_as_partial(self):
        v = I.verdict(observed=I.OBSERVED)
        self.assertIn("provisional", v["status"])

    def test_h12_three_is_recorded_as_unmeasurable_with_the_reason(self):
        o = I.OBSERVED[3]
        self.assertEqual(o["status"], "unmeasurable")
        self.assertEqual(o["raise_count"], o["calls"])
        self.assertIn("sentinel", o["why"])

    def test_h12_four_is_above_prediction(self):
        o = I.OBSERVED[4]
        self.assertTrue(all(c > o["predicted_per_call"] for c in o["sample"]))

    def test_the_composition_is_negative_if_the_law_fails(self):
        v = I.verdict(observed=I.OBSERVED)
        self.assertIn("not one invariant", v["composition"])
