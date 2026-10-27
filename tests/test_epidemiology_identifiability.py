"""Epidemiology: a known effect, a confounder, and the wall that remains."""
import unittest

from pacland.epidemiology import recovery as rec


class TestGate(unittest.TestCase):
    def test_the_audit_is_green(self):
        r = rec.audit()
        self.assertTrue(r["all_pass"], [c for c in r["checks"] if not c["pass"]])
        self.assertEqual(r["n"], 3)


class TestClassFour(unittest.TestCase):
    def test_the_stratified_estimate_recovers_the_truth_exactly(self):
        r = rec.recovery()
        self.assertTrue(r["pass"])
        self.assertLess(abs(r["adjusted"] - r["truth"]), 1e-9)

    def test_the_crude_estimate_is_wrong_by_a_lot(self):
        r = rec.recovery()
        self.assertGreater(r["crude_relative_error"], 0.5)

    def test_the_bias_disappears_when_the_confounder_is_removed(self):
        ok, msg = rec.guard_confounding()
        self.assertTrue(ok, msg)


class TestClassOne(unittest.TestCase):
    def test_persons_are_conserved(self):
        ok, msg = rec.persons_conserved(rec.cohort())
        self.assertTrue(ok, msg)

    def test_a_table_that_double_counts_is_refused(self):
        ok, msg = rec.guard_conservation()
        self.assertTrue(ok, msg)
        self.assertIn("refused = True", msg)


class TestClassTwo(unittest.TestCase):
    def test_a_homogeneous_effect_is_invariant_to_binning(self):
        r = rec.binning_invariance(heterogeneity=1.0)
        self.assertTrue(r["invariant"])

    def test_a_heterogeneous_effect_is_not(self):
        r = rec.binning_invariance(heterogeneity=2.0)
        self.assertFalse(r["invariant"])
        self.assertGreater(r["drift"], 0.01)


if __name__ == "__main__":
    unittest.main()
