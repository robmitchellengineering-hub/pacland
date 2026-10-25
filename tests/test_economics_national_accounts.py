"""National-accounts tests — the identity closes, the real decomposition does not."""
import copy
import unittest

from pacland.economics import national_accounts as N


class TestFixture(unittest.TestCase):
    def test_thirty_two_quarters(self):
        self.assertEqual(len(N.quarters()), 32)

    def test_every_record_has_both_sides(self):
        for r in N.quarters():
            for k in ("PCE", "GPDI", "GCE", "NETEXP"):
                self.assertIn(k, r["nominal"], r["quarter"])
            # the real side is named by its own series, not by the nominal labels
            for k in ("GDPC1", "PCECC96", "GPDIC1", "GCEC1", "EXPGSC1", "IMPGSC1"):
                self.assertIn(k, r["real"], r["quarter"])


class TestExactBlock(unittest.TestCase):
    def test_additivity_closes(self):
        ok, msg = N.guard_additivity()
        self.assertTrue(ok, msg)

    def test_contributions_sum_to_growth(self):
        ok, msg = N.guard_contributions_sum()
        self.assertTrue(ok, msg)

    def test_shares_sum_to_one(self):
        ok, msg = N.guard_shares_sum_to_one()
        self.assertTrue(ok, msg)

    def test_a_broken_identity_is_caught(self):
        data = copy.deepcopy(N.load())
        data["quarters"][5]["nominal"]["GCE"] += 50.0
        ok, msg = N.guard_additivity(data)
        self.assertFalse(ok)
        self.assertIn("LEAKS", msg)


class TestLeakingBlock(unittest.TestCase):
    def test_the_real_decomposition_does_not_close(self):
        rep = N.defect_report()
        self.assertGreater(rep["chain_residual_max_abs"], 1.0)

    def test_the_leak_is_reported_with_its_size(self):
        ok, msg = N.guard_the_leak_is_reported()
        self.assertTrue(ok, msg)
        self.assertIn("chain-link residual", msg)

    def test_2020_dominates_the_leak(self):
        rep = N.defect_report()
        self.assertGreater(rep["chain_residual_max_abs"],
                           rep["chain_residual_max_abs_excl_2020"])

    def test_real_contributions_handle_negative_net_exports(self):
        recs = N.quarters()
        for i in range(1, len(recs)):
            c = N.real_contributions(recs[i], recs[i - 1])
            self.assertEqual(c, c)  # no NaN, no domain error


class TestCoverage(unittest.TestCase):
    def test_inventory_is_settled(self):
        cov = N.coverage()
        self.assertEqual(cov["n_total"], 6)
        self.assertEqual(cov["n_proved"], 3)
        self.assertEqual(cov["n_specification"], 3)
        self.assertTrue(cov["complete"])

    def test_the_bridge_is_named_as_a_specification(self):
        self.assertIn("bridge_equations", N.coverage()["specification"])

    def test_summary_states_both_halves(self):
        s = N.summary()
        self.assertIn("CLOSES (rounding)", s)
        self.assertIn("NOT exact", s)


if __name__ == "__main__":
    unittest.main()
