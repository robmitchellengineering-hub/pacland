"""Build 2 — retro-fit confidence labels and the first calibration number."""
import unittest

from pacland.retrofit import (
    CONFIDENCE_PRIOR,
    Forecast,
    LEDGER,
    calibrate,
    prior_from_label,
    report,
)


class TestPriorFromLabel(unittest.TestCase):
    def test_maps_every_label(self):
        self.assertEqual(prior_from_label("High"), 0.85)
        self.assertEqual(prior_from_label("medium-high"), 0.70)
        self.assertEqual(prior_from_label("MEDIUM"), 0.50)
        self.assertEqual(prior_from_label(" low "), 0.25)

    def test_unknown_label_refuses(self):
        with self.assertRaises(ValueError):
            prior_from_label("certain-ish")

    def test_mapping_is_documented_and_complete(self):
        self.assertEqual(set(CONFIDENCE_PRIOR), {"high", "medium-high", "medium", "low"})


class TestCalibrate(unittest.TestCase):
    def test_ledger_first_number(self):
        # B1 (0.85, False), #11 (0.70, False), #8 (0.85, True)
        c = calibrate(list(LEDGER))
        self.assertEqual(c["n"], 3)
        # Brier = (0.7225 + 0.49 + 0.0225)/3
        self.assertAlmostEqual(c["brier"], 1.235 / 3, places=4)
        # log = (-ln .15 + -ln .30 + -ln .85)/3
        import math
        expected_log = (-math.log(0.15) - math.log(0.30) - math.log(0.85)) / 3
        self.assertAlmostEqual(c["log"], expected_log, places=4)

    def test_empty_refuses(self):
        with self.assertRaises(ValueError):
            calibrate([])

    def test_calibrated_forecaster_beats_overconfident(self):
        # Rule of Three arm: a synthetic forecaster at the base rate scores ~0.25;
        # an overconfident one scores worse. Machinery must detect the difference.
        truths = [True, True, False, False]
        at_base_rate = [Forecast("c", 0.5, t) for t in truths]
        overconfident = [Forecast("o", 0.9, t) for t in truths]
        self.assertLess(calibrate(at_base_rate)["brier"], calibrate(overconfident)["brier"])

    def test_flipping_an_outcome_moves_the_score(self):
        base = calibrate(list(LEDGER))["brier"]
        flipped = [Forecast(f.name, f.prior, not f.held) for f in LEDGER]
        self.assertNotEqual(calibrate(flipped)["brier"], base)


class TestReport(unittest.TestCase):
    def test_report_names_the_number_and_verdict(self):
        text = report()
        self.assertIn("Brier", text)
        self.assertIn("scored claims", text)


if __name__ == "__main__":
    unittest.main()
