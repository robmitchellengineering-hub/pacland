"""The calibration gate: perfect calibration scores zero, overconfidence scores high, and the
certificate's pass/fail decision is calibrated against forged results."""
import unittest

from pacland import calibration as cal


class TestExpectedCalibrationError(unittest.TestCase):
    def test_perfectly_calibrated_scores_zero(self):
        # confidence 0.7 on 10 items, 7 correct -> accuracy 0.7, ECE 0
        conf = [0.7] * 10
        out = [True] * 7 + [False] * 3
        ece, _ = cal.expected_calibration_error(conf, out, n_bins=2)
        self.assertAlmostEqual(ece, 0.0, places=6)

    def test_overconfident_scores_high(self):
        # confidence 1.0 on 10 items, half wrong -> ECE 0.5
        conf = [1.0] * 10
        out = [True] * 5 + [False] * 5
        ece, _ = cal.expected_calibration_error(conf, out, n_bins=2)
        self.assertAlmostEqual(ece, 0.5, places=6)


class TestGateQuantumCertificate(unittest.TestCase):
    def test_pass_fail_decision_is_calibrated(self):
        r = cal.gate_quantum_certificate("ghz", 12, tol=1e-9, seed=1)
        self.assertTrue(r["decision_calibrated"])
        self.assertEqual(r["false_accept"], 0)
        self.assertEqual(r["false_refuse"], 0)
        self.assertGreaterEqual(r["true_refuse"], 1)  # the forgeries were refused

    def test_graded_ece_is_nonzero(self):
        # the referee is a hard threshold, not a probabilistic predictor — the gap is real
        r = cal.gate_quantum_certificate("ghz", 12, tol=1e-9, seed=2)
        self.assertGreater(r["ece"], 0.0)


class TestProperScoringHonesty(unittest.TestCase):
    def test_honesty_minimizes_the_brier_score(self):
        h = cal.honesty_theorem(q=0.7)
        self.assertTrue(h["honest_minimizes"])
        self.assertEqual(h["minimizer"], 0.7)
        # the overconfident report (1.0) and the underconfident report (0.0) score worse
        self.assertLess(h["expected_brier"][0.7], h["expected_brier"][1.0])
        self.assertLess(h["expected_brier"][0.7], h["expected_brier"][0.0])

    def test_calibrated_forecaster_scores_better_than_overconfident(self):
        # truth 0.7, repeated; a forecaster reporting 0.7 beats one reporting 1.0
        conf_cal = [0.7] * 100
        conf_over = [1.0] * 100
        out = [True] * 70 + [False] * 30
        self.assertLess(cal.mean_brier_score(conf_cal, out), cal.mean_brier_score(conf_over, out))


if __name__ == "__main__":
    unittest.main()
