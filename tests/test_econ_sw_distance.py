"""Minimum distance: the fit is exact, the parameters are not identified, and that is the finding."""
import unittest

from pacland.economics import sw_distance as D


class TestMoments(unittest.TestCase):
    def test_model_moments_are_symmetric_and_finite(self):
        m = D.model_moments([0.1] * 7, lags=(0,))
        n = 5
        for a in range(n):
            for b in range(n):
                self.assertAlmostEqual(m[0][a * n + b], m[0][b * n + a], places=6)

    def test_data_moments_have_positive_variances(self):
        m = D.data_moments(lags=(0,))
        for i in range(5):
            self.assertGreater(m[0][i * 5 + i], 0.0)

    def test_the_design_has_one_column_per_shock(self):
        cols = D._design(None, (0,))
        self.assertEqual(len(cols), 7)


class TestIdentification(unittest.TestCase):
    def test_the_control_fit_is_perfect(self):
        rec = D.recovery()
        self.assertGreater(rec["r2"], 0.99)

    def test_but_the_scales_are_not_recovered(self):
        rec = D.recovery()
        self.assertFalse(rec["pass"])
        self.assertGreater(rec["worst_relative_error"], 0.1)

    def test_non_negative_least_squares_behaves(self):
        # a tiny exact system: x = [2, 0] must be recovered exactly
        cols = [[1.0, 0.0], [0.0, 1.0]]
        out = D._nnls(cols, [4.0, 0.0])
        self.assertAlmostEqual(out[0], 4.0)
        self.assertEqual(out[1], 0.0)


class TestAudit(unittest.TestCase):
    def test_the_audit_records_both_facts(self):
        a = D.audit()
        self.assertTrue(a["all_pass"])
        self.assertFalse(a["usable"])
