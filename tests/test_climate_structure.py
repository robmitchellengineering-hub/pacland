"""Climate's conservation inventory — sourced, measured, and honest about the gap."""
import unittest

from pacland.climate import structure as S


class TestInventory(unittest.TestCase):
    def test_five_invariants(self):
        self.assertEqual(len(S.INVARIANTS), 5)

    def test_every_invariant_is_sourced(self):
        ok, msg = S.guard_invariants_are_sourced()
        self.assertTrue(ok, msg)

    def test_the_keys_are_the_expected_laws(self):
        self.assertEqual({i.key for i in S.INVARIANTS},
                         {"energy", "water", "carbon", "ocean_mass", "salinity"})

    def test_an_unsourced_invariant_is_refused(self):
        bad = S.Invariant("probe", "", "", "identity, unmeasured here")
        saved = S.INVARIANTS
        try:
            S.INVARIANTS = saved + (bad,)
            ok, msg = S.guard_invariants_are_sourced()
        finally:
            S.INVARIANTS = saved
        self.assertFalse(ok)
        self.assertIn("UNSOURCED", msg)


class TestClosure(unittest.TestCase):
    def test_it_closes_with_all_reservoirs(self):
        ok, msg = S.guard_closure_is_reported()
        self.assertTrue(ok, msg)

    def test_it_does_not_close_on_the_upper_ocean_alone(self):
        f = S.closure_finding()
        self.assertGreater(abs(f["residual_upper_ocean"]), 0.05)
        self.assertLess(abs(f["residual_full"]), abs(f["residual_upper_ocean"]))

    def test_the_finding_says_so(self):
        self.assertTrue(S.closure_finding()["closes_only_with_all_reservoirs"])


class TestCoverage(unittest.TestCase):
    def test_all_five_are_measured_here(self):
        cov = S.coverage()
        self.assertEqual(cov["n_measured"], 5)   # all five: carbon and water both measured now
        self.assertEqual(cov["n_unmeasured"], 0)
        self.assertTrue(cov["complete"])

    def test_the_unmeasured_ones_are_named(self):
        """The guard's job is that nothing is silently unmeasured. With none left, it still has
        to pass — an empty list is a *result*, not a missing entry."""
        ok, msg = S.guard_unmeasured_invariants_are_named()
        self.assertTrue(ok, msg)
        self.assertEqual(S.coverage()["unmeasured"], [])

    def test_summary_states_the_split(self):
        s = S.summary()
        self.assertIn("5 of 5", s)


if __name__ == "__main__":
    unittest.main()
