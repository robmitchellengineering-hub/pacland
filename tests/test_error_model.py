import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.error_model import CalibrationVerdict, ErrorModel, Kind, calibrate


class TestCalibrate(unittest.TestCase):
    def test_well_calibrated(self):
        verdict = calibrate(
            claimed_delta_beta=0.5, p_hat_e=0.1, m=1000, delta_e=0.05
        )
        self.assertEqual(verdict, CalibrationVerdict.WELL_CALIBRATED)

    def test_miscalibrated(self):
        verdict = calibrate(
            claimed_delta_beta=0.05, p_hat_e=0.3, m=1000, delta_e=0.05
        )
        self.assertEqual(verdict, CalibrationVerdict.MISCALIBRATED)

    def test_insufficient_data(self):
        verdict = calibrate(
            claimed_delta_beta=0.1, p_hat_e=0.0, m=0, delta_e=0.05
        )
        self.assertEqual(verdict, CalibrationVerdict.INSUFFICIENT_DATA)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calibrate(claimed_delta_beta=1.5, p_hat_e=0.0, m=10, delta_e=0.05)
        with self.assertRaises(ValueError):
            calibrate(claimed_delta_beta=0.1, p_hat_e=1.5, m=10, delta_e=0.05)


class TestErrorModel(unittest.TestCase):
    def test_roundtrip(self):
        em = ErrorModel(
            bias=0.01, scale=0.005, beta=0.02, delta_beta=0.05,
            kind=Kind.INTERVAL, validated=True,
        )
        self.assertEqual(em.kind, Kind.INTERVAL)
        self.assertTrue(em.validated)


if __name__ == "__main__":
    unittest.main()
