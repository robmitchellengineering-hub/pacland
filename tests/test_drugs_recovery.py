"""Drug discovery against an invented truth: classes 4 and 2 in a third discipline."""
import unittest

from pacland.drugs import recovery as rec


class TestGate(unittest.TestCase):
    def test_the_audit_is_green(self):
        r = rec.audit()
        self.assertTrue(r["all_pass"], [c for c in r["checks"] if not c["pass"]])
        self.assertEqual(r["n"], 3)


class TestRecovery(unittest.TestCase):
    def test_a_noiseless_curve_returns_its_own_parameters(self):
        r = rec.recovery()
        self.assertTrue(r["pass"])
        self.assertLess(r["ic50_error_rel"], rec.EXACT)
        self.assertLess(r["hill_error_rel"], rec.EXACT)

    def test_a_different_curve_is_also_recovered(self):
        truth = rec.Curve(top=90.0, bottom=5.0, ic50=12.0, hill=1.6)
        r = rec.recovery(truth)
        self.assertTrue(r["pass"], r["estimate"])


class TestSeededFaults(unittest.TestCase):
    def test_pinned_asymptotes_bias_the_ic50(self):
        ok, msg = rec.guard_fixed_asymptotes()
        self.assertTrue(ok, msg)
        self.assertIn("detected = True", msg)

    def test_units_scale_the_ic50_and_leave_the_slope_alone(self):
        ok, msg = rec.guard_units()
        self.assertTrue(ok, msg)
        self.assertIn("moved = True", msg)


class TestWhatThisIsWorth(unittest.TestCase):
    def test_the_bias_is_large_not_marginal(self):
        # the number that makes the point: a textbook-pinned fit is not slightly off
        xs = rec.concentrations()
        truth = rec.Curve()
        ys = rec.sample(truth, xs)
        trapped = rec.fit(xs, ys, fixed_bottom=0.0, fixed_top=100.0)
        self.assertGreater(abs(trapped.ic50 - truth.ic50) / truth.ic50, 0.2)


if __name__ == "__main__":
    unittest.main()
