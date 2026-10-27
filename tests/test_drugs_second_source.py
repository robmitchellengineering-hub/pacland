"""Class 5 for drug discovery: two databases, one nominal quantity."""
import unittest

from pacland.drugs import second_source as ss


class TestCrossSource(unittest.TestCase):
    def test_the_two_sources_agree_on_the_central_value(self):
        r = ss.cross_source()
        self.assertTrue(r["agree"], r["verdict"])
        self.assertLess(r["median_ratio"], ss.AGREEMENT_FACTOR)

    def test_the_data_is_actually_two_independent_bodies(self):
        c, p = ss.profile("chembl"), ss.profile("pubchem")
        self.assertGreater(c["n"], 500)
        self.assertGreater(p["n"], 500)
        self.assertNotEqual(c["median_nm"], p["median_nm"])   # same quantity, different curation

    def test_the_verdict_names_both_numbers(self):
        r = ss.cross_source()
        self.assertIn("central value", r["verdict"])
        self.assertIn("disagrees with itself", r["verdict"])


class TestTheFinding(unittest.TestCase):
    def test_each_source_disagrees_with_itself_by_orders_of_magnitude(self):
        r = ss.cross_source()
        self.assertGreater(r["chembl"]["fold_range_10_90"], 100)
        self.assertGreater(r["pubchem"]["fold_range_10_90"], 100)

    def test_the_spread_guard_is_not_trivial(self):
        ok, msg = ss.guard_spread_is_real()
        self.assertTrue(ok, msg)

    def test_self_comparison_is_exact(self):
        ok, msg = ss.guard_cross_source()
        self.assertTrue(ok, msg)

    def test_the_audit_is_green(self):
        self.assertTrue(ss.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
